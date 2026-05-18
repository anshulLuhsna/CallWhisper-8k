from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from tqdm import tqdm

from .loader import ManifestRow, load_manifest
from .runner import score_row, set_seed, summarize, write_outputs


def resolve_device(device: str) -> int:
    if device != "auto":
        return int(device)
    try:
        import torch
    except ImportError:
        return -1
    return 0 if torch.cuda.is_available() else -1


def build_generate_kwargs(language_mode: str) -> dict[str, str]:
    if language_mode == "auto":
        return {}
    if language_mode in {"manifest", "hi"}:
        return {"language": "hi", "task": "transcribe"}
    raise ValueError(f"Unknown language mode: {language_mode}")


def transcribe_rows(
    rows: list[ManifestRow],
    model_id: str,
    language_mode: str,
    seed: int,
    device: str,
    chunk_length_s: int,
) -> list[dict[str, Any]]:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "transformers is not installed. Run `pip install -e .[colab]` before HF evaluation."
        ) from exc

    set_seed(seed)
    asr = pipeline(
        task="automatic-speech-recognition",
        model=model_id,
        chunk_length_s=chunk_length_s,
        device=resolve_device(device),
    )
    generate_kwargs = build_generate_kwargs(language_mode)

    outputs: list[dict[str, Any]] = []
    for row in tqdm(rows, desc=model_id):
        if not row.audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {row.audio_path}")
        result = asr(str(row.audio_path), generate_kwargs=generate_kwargs)
        hypothesis = str(result.get("text", "")).strip()
        outputs.append(score_row(row, hypothesis, model_id, language_mode))
    return outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Hugging Face ASR model on a manifest.")
    parser.add_argument("--manifest", required=True, help="CSV manifest path")
    parser.add_argument("--model-id", required=True, help="Hugging Face model ID")
    parser.add_argument(
        "--language-mode",
        choices=("manifest", "auto", "hi"),
        default="manifest",
        help="Use manifest Hindi hints, auto-detect language, or force Hindi",
    )
    parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducible decoding")
    parser.add_argument("--device", default="auto", help="Transformers device, e.g. auto/0/-1")
    parser.add_argument("--chunk-length-s", type=int, default=30, help="ASR chunk length in seconds")
    parser.add_argument("--output-json", default=None, help="Optional path for JSON results")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = load_manifest(args.manifest)
    results = transcribe_rows(
        rows=rows,
        model_id=args.model_id,
        language_mode=args.language_mode,
        seed=args.seed,
        device=args.device,
        chunk_length_s=args.chunk_length_s,
    )
    summary = summarize(results)
    write_outputs(results, Path(args.output_json) if args.output_json else None)
    print(
        f"files={summary['num_files']} model={args.model_id} "
        f"wer={summary['wer']:.4f} cer={summary['cer']:.4f}"
    )


if __name__ == "__main__":
    main()
