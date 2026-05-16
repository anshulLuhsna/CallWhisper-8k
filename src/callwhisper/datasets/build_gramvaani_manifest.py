from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_kaldi_text(path: Path) -> dict[str, str]:
    transcripts: dict[str, str] = {}
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            utt_id, _, transcript = line.partition(" ")
            if utt_id and transcript:
                transcripts[utt_id] = transcript.strip()
    return transcripts


def read_scp(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                rows.append((parts[0], parts[1]))
    return rows


def build_manifest(dataset_dir: Path, output_path: Path, limit: int) -> None:
    transcripts = read_kaldi_text(dataset_dir / "text")
    audio_rows = read_scp(dataset_dir / "mp3.scp")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=("audio_path", "reference_text", "slice", "condition", "language"),
        )
        writer.writeheader()
        for utt_id, relative_audio_path in audio_rows:
            transcript = transcripts.get(utt_id)
            if not transcript:
                continue
            audio_path = dataset_dir / relative_audio_path
            writer.writerow(
                {
                    "audio_path": str(audio_path).replace("./", ""),
                    "reference_text": transcript,
                    "slice": f"gramvaani_dev_{limit}",
                    "condition": "telephone_mp3",
                    "language": "hi",
                }
            )
            written += 1
            if written >= limit:
                break

    if written < limit:
        raise RuntimeError(f"Only wrote {written} rows, requested {limit}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a Gramvaani CSV manifest.")
    parser.add_argument("--dataset-dir", default="datasets/GV_Dev_5h")
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=50)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    build_manifest(Path(args.dataset_dir), Path(args.output), args.limit)


if __name__ == "__main__":
    main()
