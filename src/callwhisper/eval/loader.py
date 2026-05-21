from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv


REQUIRED_COLUMNS = ("audio_path", "reference_text", "slice", "condition", "language")


@dataclass(frozen=True)
class ManifestRow:
    audio_path: Path
    reference_text: str
    slice: str
    condition: str
    language: str


def load_manifest(path: str | Path, repo_root: str | Path | None = None) -> list[ManifestRow]:
    manifest_path = Path(path)
    root = Path(repo_root) if repo_root is not None else Path.cwd()
    manifest_parent = manifest_path.parent

    with manifest_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Manifest {manifest_path} is missing columns: {', '.join(missing)}")

        rows: list[ManifestRow] = []
        for index, raw in enumerate(reader, start=2):
            audio_path = Path(raw["audio_path"])
            if not audio_path.is_absolute():
                root_candidate = root / audio_path
                manifest_candidate = manifest_parent / audio_path
                audio_path = root_candidate if root_candidate.exists() else manifest_candidate
            reference_text = raw["reference_text"].strip()
            if not reference_text:
                raise ValueError(f"Manifest {manifest_path} row {index} has an empty reference_text")
            rows.append(
                ManifestRow(
                    audio_path=audio_path,
                    reference_text=reference_text,
                    slice=raw["slice"].strip(),
                    condition=raw["condition"].strip(),
                    language=raw["language"].strip(),
                )
            )
    return rows
