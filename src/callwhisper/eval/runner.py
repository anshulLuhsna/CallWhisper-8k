from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from tqdm import tqdm

from .cer import character_error_rate
from .loader import ManifestRow, load_manifest
from .wer import word_error_rate


def transcribe_rows(rows: list[ManifestRow], model_name: str) -> list[dict[str, Any]]:
    try:
        import whisper
    except ImportError as exc:
        raise RuntimeError(
            "openai-whisper is not installed. Run `pip install -e .` before evaluation."
        ) from exc

    model = whisper.load_model(model_name)
    outputs: list[dict[str, Any]] = []
    for row in tqdm(rows, desc=f"whisper-{model_name}"):
        if not row.audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {row.audio_path}")
        result = model.transcribe(str(row.audio_path), language="hi" if row.language == "hi" else None)
        hypothesis = str(result.get("text", "")).strip()
        outputs.append(score_row(row, hypothesis, model_name))
    return outputs


def score_row(row: ManifestRow, hypothesis: str, model_name: str) -> dict[str, Any]:
    return {
        "model": model_name,
        "audio_path": str(row.audio_path),
        "reference_text": row.reference_text,
        "hypothesis_text": hypothesis,
        "slice": row.slice,
        "condition": row.condition,
        "language": row.language,
        "wer": word_error_rate(row.reference_text, hypothesis),
        "cer": character_error_rate(row.reference_text, hypothesis),
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        raise ValueError("Cannot summarize empty results")
    return {
        "num_files": len(results),
        "wer": mean(item["wer"] for item in results),
        "cer": mean(item["cer"] for item in results),
    }


def write_outputs(results: list[dict[str, Any]], output_json: Path | None) -> None:
    if output_json is None:
        return
    output_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {"summary": summarize(results), "samples": results}
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a CallWhisper-8k evaluation manifest.")
    parser.add_argument("--manifest", required=True, help="CSV manifest path")
    parser.add_argument("--model", default="tiny", help="Whisper model name, e.g. tiny/base/small")
    parser.add_argument("--output-json", default=None, help="Optional path for JSON results")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = load_manifest(args.manifest)
    results = transcribe_rows(rows, args.model)
    summary = summarize(results)
    write_outputs(results, Path(args.output_json) if args.output_json else None)
    print(
        f"files={summary['num_files']} model={args.model} "
        f"wer={summary['wer']:.4f} cer={summary['cer']:.4f}"
    )
