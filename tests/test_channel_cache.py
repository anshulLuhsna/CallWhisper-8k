from __future__ import annotations

from pathlib import Path

import pytest

import callwhisper.datasets.channel_cache as channel_cache


def _rows(count: int) -> list[dict[str, str]]:
    return [
        {
            "utterance_id": f"utt-{index}",
            "source_audio_path": f"Audio/utt-{index}.mp3",
            "condition": "original" if index % 2 == 0 else "bandlimit_8k",
        }
        for index in range(count)
    ]


def test_cache_chunks_resume_and_restore(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    rows = _rows(5)
    dataset_dir = tmp_path / "dataset"
    persistent_dir = tmp_path / "persistent"
    scratch_dir = tmp_path / "scratch"
    cache_dir = tmp_path / "cache"
    calls: list[str] = []

    def fake_transform(source: Path, destination: Path, condition: str) -> None:
        calls.append(destination.name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(f"{source}:{condition}".encode())

    monkeypatch.setattr(channel_cache, "transform_audio", fake_transform)
    manifest = channel_cache.build_cache_chunks(
        rows,
        dataset_dir=dataset_dir,
        persistent_dir=persistent_dir,
        scratch_dir=scratch_dir,
        chunk_size=2,
        workers=2,
    )

    assert manifest["unique_files"] == 5
    assert len(manifest["chunks"]) == 3
    assert len(calls) == 5

    channel_cache.build_cache_chunks(
        rows,
        dataset_dir=dataset_dir,
        persistent_dir=persistent_dir,
        scratch_dir=scratch_dir,
        chunk_size=2,
        workers=2,
    )
    assert len(calls) == 5

    channel_cache.restore_cache_chunks(
        rows,
        persistent_dir=persistent_dir,
        cache_dir=cache_dir,
        scratch_dir=scratch_dir,
    )
    assert all((cache_dir / channel_cache.cache_relative_path(row)).exists() for row in rows)


def test_restore_rejects_a_different_view_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    rows = _rows(2)

    def fake_transform(source: Path, destination: Path, condition: str) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(b"audio")

    monkeypatch.setattr(channel_cache, "transform_audio", fake_transform)
    channel_cache.build_cache_chunks(
        rows,
        dataset_dir=tmp_path / "dataset",
        persistent_dir=tmp_path / "persistent",
        scratch_dir=tmp_path / "scratch",
        chunk_size=2,
    )
    changed = [*rows, *_rows(3)[2:]]

    with pytest.raises(ValueError, match="different view set"):
        channel_cache.restore_cache_chunks(
            changed,
            persistent_dir=tmp_path / "persistent",
            cache_dir=tmp_path / "cache",
            scratch_dir=tmp_path / "scratch",
        )
