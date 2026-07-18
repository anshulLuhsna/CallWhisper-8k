"""Build and restore resumable channel-audio cache archives."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tarfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, Iterable

from .paired_telephony import CONDITIONS, sha256_file, transform_audio


CACHE_SCHEMA_VERSION = 1
ProgressCallback = Callable[[int, int, str], None]


def cache_relative_path(row: dict[str, Any]) -> Path:
    condition = str(row["condition"])
    utterance_id = str(row["utterance_id"])
    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}")
    if not utterance_id or Path(utterance_id).name != utterance_id:
        raise ValueError(f"Unsafe utterance_id: {utterance_id!r}")
    return Path(condition) / f"{utterance_id}.wav"


def unique_cache_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for source_row in rows:
        row = dict(source_row)
        relative = cache_relative_path(row).as_posix()
        existing = unique.get(relative)
        if existing and existing["source_audio_path"] != row["source_audio_path"]:
            raise ValueError(f"Conflicting source paths for {relative}")
        unique[relative] = row
    return [unique[key] for key in sorted(unique)]


def cache_set_sha256(rows: Iterable[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in unique_cache_rows(rows):
        payload = {
            "relative_path": cache_relative_path(row).as_posix(),
            "source_audio_path": str(row["source_audio_path"]),
            "condition": str(row["condition"]),
        }
        digest.update(json.dumps(payload, sort_keys=True).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _chunk_digest(rows: list[dict[str, Any]]) -> str:
    return cache_set_sha256(rows)


def _safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.getmembers():
        if member.issym() or member.islnk():
            raise ValueError(f"Cache archive contains a link: {member.name}")
        target = (destination / member.name).resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"Unsafe cache archive path: {member.name}")
    archive.extractall(destination)


def build_cache_chunks(
    rows: Iterable[dict[str, Any]],
    *,
    dataset_dir: Path,
    persistent_dir: Path,
    scratch_dir: Path,
    chunk_size: int = 500,
    workers: int = 8,
    progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    """Build deterministic archives and checkpoint every completed chunk."""
    if chunk_size <= 0 or workers <= 0:
        raise ValueError("chunk_size and workers must be positive")
    cache_rows = unique_cache_rows(rows)
    if not cache_rows:
        raise ValueError("Cannot build an empty cache")

    persistent_dir.mkdir(parents=True, exist_ok=True)
    scratch_dir.mkdir(parents=True, exist_ok=True)
    chunks = [
        cache_rows[index : index + chunk_size] for index in range(0, len(cache_rows), chunk_size)
    ]
    chunk_records: list[dict[str, Any]] = []

    for chunk_index, chunk_rows in enumerate(chunks):
        chunk_name = f"chunk-{chunk_index:05d}"
        archive_path = persistent_dir / f"{chunk_name}.tar.gz"
        marker_path = persistent_dir / f"{chunk_name}.json"
        digest = _chunk_digest(chunk_rows)
        marker = None
        if archive_path.exists() and marker_path.exists():
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            if (
                marker.get("schema_version") != CACHE_SCHEMA_VERSION
                or marker.get("chunk_sha256") != digest
                or marker.get("file_count") != len(chunk_rows)
                or marker.get("archive_bytes") != archive_path.stat().st_size
            ):
                marker = None

        if marker is None:
            chunk_root = scratch_dir / chunk_name
            shutil.rmtree(chunk_root, ignore_errors=True)
            chunk_root.mkdir(parents=True)

            def materialize(row: dict[str, Any]) -> None:
                source = dataset_dir / str(row["source_audio_path"])
                destination = chunk_root / cache_relative_path(row)
                transform_audio(source, destination, str(row["condition"]))

            with ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(materialize, chunk_rows))

            local_archive = scratch_dir / f"{chunk_name}.tar.gz"
            local_archive.unlink(missing_ok=True)
            with tarfile.open(local_archive, "w:gz") as archive:
                for row in chunk_rows:
                    relative = cache_relative_path(row)
                    archive.add(chunk_root / relative, arcname=relative.as_posix())

            archive_bytes = local_archive.stat().st_size
            archive_sha256 = sha256_file(local_archive)
            partial_archive = archive_path.with_suffix(archive_path.suffix + ".partial")
            shutil.copyfile(local_archive, partial_archive)
            os.replace(partial_archive, archive_path)
            marker = {
                "schema_version": CACHE_SCHEMA_VERSION,
                "chunk_index": chunk_index,
                "chunk_sha256": digest,
                "file_count": len(chunk_rows),
                "archive_name": archive_path.name,
                "archive_bytes": archive_bytes,
                "archive_sha256": archive_sha256,
            }
            _atomic_json(marker_path, marker)
            shutil.rmtree(chunk_root)
            local_archive.unlink(missing_ok=True)

        chunk_records.append(marker)
        if progress:
            progress(chunk_index + 1, len(chunks), archive_path.name)

    manifest = {
        "schema_version": CACHE_SCHEMA_VERSION,
        "cache_set_sha256": cache_set_sha256(cache_rows),
        "unique_files": len(cache_rows),
        "chunk_size": chunk_size,
        "chunks": chunk_records,
    }
    _atomic_json(persistent_dir / "cache_manifest.json", manifest)
    return manifest


def restore_cache_chunks(
    rows: Iterable[dict[str, Any]],
    *,
    persistent_dir: Path,
    cache_dir: Path,
    scratch_dir: Path,
    progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    """Restore a complete persistent cache to fast local disk."""
    cache_rows = unique_cache_rows(rows)
    manifest_path = persistent_dir / "cache_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Missing completed cache manifest: {manifest_path}. Run the CPU cache notebook first."
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_digest = cache_set_sha256(cache_rows)
    if manifest.get("cache_set_sha256") != expected_digest:
        raise ValueError("Persistent cache was built for a different view set")

    cache_dir.mkdir(parents=True, exist_ok=True)
    scratch_dir.mkdir(parents=True, exist_ok=True)
    sentinel = cache_dir / ".restore_complete.json"
    if sentinel.exists():
        restored = json.loads(sentinel.read_text(encoding="utf-8"))
        if restored.get("cache_set_sha256") == expected_digest:
            return manifest

    chunks = manifest.get("chunks", [])
    for index, chunk in enumerate(chunks):
        archive_path = persistent_dir / chunk["archive_name"]
        if not archive_path.exists() or archive_path.stat().st_size != chunk["archive_bytes"]:
            raise FileNotFoundError(f"Missing or incomplete cache archive: {archive_path}")
        local_archive = scratch_dir / archive_path.name
        shutil.copyfile(archive_path, local_archive)
        if sha256_file(local_archive) != chunk["archive_sha256"]:
            raise ValueError(f"Cache archive checksum failed: {archive_path.name}")
        with tarfile.open(local_archive, "r:gz") as archive:
            _safe_extract(archive, cache_dir)
        local_archive.unlink()
        if progress:
            progress(index + 1, len(chunks), archive_path.name)

    missing = [
        cache_relative_path(row).as_posix()
        for row in cache_rows
        if not (cache_dir / cache_relative_path(row)).exists()
    ]
    if missing:
        raise RuntimeError(f"Restored cache is missing {len(missing)} files; first={missing[0]}")
    _atomic_json(sentinel, {"cache_set_sha256": expected_digest})
    return manifest
