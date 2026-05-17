from __future__ import annotations

import argparse
import csv
from pathlib import Path

from tqdm import tqdm

from callwhisper.eval.loader import load_manifest

from .telephony import normalize_volume, phone_bandpass, roundtrip_8k, to_whisper_wav


METHODS = {
    "whisper_wav": to_whisper_wav,
    "normalize": normalize_volume,
    "bandpass": phone_bandpass,
    "roundtrip_8k": roundtrip_8k,
}


def preprocess_manifest(
    manifest_path: Path,
    output_audio_dir: Path,
    output_manifest: Path,
    method: str,
) -> None:
    if method not in METHODS:
        raise ValueError(f"Unknown method {method}. Choose from: {', '.join(METHODS)}")

    rows = load_manifest(manifest_path)
    preprocess = METHODS[method]
    output_audio_dir.mkdir(parents=True, exist_ok=True)
    output_manifest.parent.mkdir(parents=True, exist_ok=True)

    with output_manifest.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=("audio_path", "reference_text", "slice", "condition", "language"),
        )
        writer.writeheader()
        for index, row in enumerate(tqdm(rows, desc=f"preprocess-{method}"), start=1):
            output_audio_path = output_audio_dir / f"{index:04d}_{row.audio_path.stem}.wav"
            preprocess(row.audio_path, output_audio_path)
            writer.writerow(
                {
                    "audio_path": str(output_audio_path),
                    "reference_text": row.reference_text,
                    "slice": row.slice,
                    "condition": method,
                    "language": row.language,
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preprocess every audio file in a manifest.")
    parser.add_argument("--manifest", required=True, help="Input CSV manifest")
    parser.add_argument("--output-audio-dir", required=True, help="Directory for processed WAV files")
    parser.add_argument("--output-manifest", required=True, help="Output CSV manifest")
    parser.add_argument(
        "--method",
        choices=tuple(METHODS),
        default="whisper_wav",
        help="Preprocessing method",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    preprocess_manifest(
        manifest_path=Path(args.manifest),
        output_audio_dir=Path(args.output_audio_dir),
        output_manifest=Path(args.output_manifest),
        method=args.method,
    )


if __name__ == "__main__":
    main()
