from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path

from callwhisper.eval.loader import REQUIRED_COLUMNS, ManifestRow, load_manifest


def probe_sample_rate(audio_path: Path) -> int:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=sample_rate",
        "-of",
        "json",
        str(audio_path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("ffprobe is required to split manifests by sample rate") from exc
    payload = json.loads(result.stdout)
    streams = payload.get("streams") or []
    if not streams or "sample_rate" not in streams[0]:
        raise RuntimeError(f"Could not read sample rate for {audio_path}")
    return int(streams[0]["sample_rate"])


def manifest_audio_path(audio_path: Path) -> str:
    try:
        return str(audio_path.relative_to(Path.cwd()))
    except ValueError:
        return str(audio_path)


def write_manifest(rows: list[ManifestRow], output_path: Path, slice_suffix: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "audio_path": manifest_audio_path(row.audio_path),
                    "reference_text": row.reference_text,
                    "slice": f"{row.slice}_{slice_suffix}",
                    "condition": row.condition,
                    "language": row.language,
                }
            )


def split_manifest(
    manifest_path: Path,
    low_output: Path,
    high_output: Path,
    low_sample_rate: int,
) -> dict[str, int]:
    rows = load_manifest(manifest_path)
    low_rows: list[ManifestRow] = []
    high_rows: list[ManifestRow] = []
    sample_rate_counts: dict[str, int] = {}

    for row in rows:
        sample_rate = probe_sample_rate(row.audio_path)
        sample_rate_counts[str(sample_rate)] = sample_rate_counts.get(str(sample_rate), 0) + 1
        if sample_rate == low_sample_rate:
            low_rows.append(row)
        else:
            high_rows.append(row)

    write_manifest(low_rows, low_output, f"{low_sample_rate // 1000}khz")
    write_manifest(high_rows, high_output, "highrate")
    return {
        "total": len(rows),
        f"{low_sample_rate}_hz": len(low_rows),
        "highrate": len(high_rows),
        **{f"source_{rate}_hz": count for rate, count in sorted(sample_rate_counts.items())},
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Split a manifest by source audio sample rate.")
    parser.add_argument("--manifest", required=True, help="Input CSV manifest")
    parser.add_argument("--low-output", required=True, help="Output CSV for low-rate audio")
    parser.add_argument("--high-output", required=True, help="Output CSV for higher-rate audio")
    parser.add_argument(
        "--low-sample-rate",
        type=int,
        default=8000,
        help="Sample rate that should go into the low-rate manifest",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = split_manifest(
        manifest_path=Path(args.manifest),
        low_output=Path(args.low_output),
        high_output=Path(args.high_output),
        low_sample_rate=args.low_sample_rate,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
