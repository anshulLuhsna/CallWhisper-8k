from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run_ffmpeg(input_path: Path, output_path: Path, *filters: str) -> None:
    """Run ffmpeg with mono 16 kHz WAV output for Whisper-compatible audio."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input audio not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(input_path),
    ]
    if filters:
        command.extend(["-af", ",".join(filters)])
    command.extend(["-ac", "1", "-ar", "16000", str(output_path)])

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise RuntimeError("ffmpeg is required for audio preprocessing") from exc


def to_whisper_wav(input_path: Path, output_path: Path) -> None:
    """Convert any supported audio file to mono 16 kHz WAV."""
    run_ffmpeg(input_path, output_path)


def normalize_volume(input_path: Path, output_path: Path) -> None:
    """Convert to mono 16 kHz WAV and normalize loudness."""
    run_ffmpeg(input_path, output_path, "loudnorm=I=-20:TP=-1.5:LRA=11")


def phone_bandpass(input_path: Path, output_path: Path) -> None:
    """Apply a simple telephone-band filter, then output mono 16 kHz WAV."""
    run_ffmpeg(input_path, output_path, "highpass=f=300", "lowpass=f=3400")


def roundtrip_8k(input_path: Path, output_path: Path) -> None:
    """Resample through 8 kHz, then return to mono 16 kHz WAV for Whisper."""
    run_ffmpeg(input_path, output_path, "aresample=8000", "aresample=16000")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preprocess one audio file for CallWhisper-8k.")
    parser.add_argument("input", help="Input audio path")
    parser.add_argument("output", help="Output WAV path")
    parser.add_argument(
        "--method",
        choices=("whisper_wav", "normalize", "bandpass", "roundtrip_8k"),
        default="whisper_wav",
        help="Preprocessing method to apply",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    methods = {
        "whisper_wav": to_whisper_wav,
        "normalize": normalize_volume,
        "bandpass": phone_bandpass,
        "roundtrip_8k": roundtrip_8k,
    }
    methods[args.method](input_path, output_path)


if __name__ == "__main__":
    main()
