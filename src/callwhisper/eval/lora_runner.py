from __future__ import annotations

import argparse
import gc
import json
import random
from pathlib import Path
from statistics import mean
from typing import Any

from .loader import ManifestRow, load_manifest
from .normalizer import normalize_text


DEFAULT_ADAPTER_DIR = "models/whisper-small-lora-gramvaani-pilot-seed0/final_adapter"
DEFAULT_PROCESSOR_DIR = "models/whisper-small-lora-gramvaani-pilot-seed0/processor"
DEFAULT_RUN_NAME = "whisper-small-lora-gramvaani-pilot-seed0_reload"


def set_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import torch
    except ImportError:
        return
    torch.manual_seed(seed)


def resolve_device(device: str) -> str:
    if device != "auto":
        return device
    try:
        import torch
    except ImportError:
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"


def require_eval_dependencies() -> tuple[Any, Any, Any, Any, Any, Any, Any]:
    try:
        import librosa
        import torch
        from jiwer import cer as jiwer_cer
        from jiwer import wer as jiwer_wer
        from peft import PeftModel
        from transformers import WhisperForConditionalGeneration, WhisperProcessor
    except ImportError as exc:
        raise RuntimeError(
            "Missing LoRA eval dependencies. Run "
            '`pip install -e ".[finetune]"` before adapter evaluation.'
        ) from exc
    return (
        librosa,
        torch,
        jiwer_cer,
        jiwer_wer,
        PeftModel,
        WhisperForConditionalGeneration,
        WhisperProcessor,
    )


def progress(iterable: list[ManifestRow], desc: str) -> Any:
    try:
        from tqdm import tqdm
    except ImportError:
        return iterable
    return tqdm(iterable, desc=desc)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())

    def cell(value: Any) -> str:
        if isinstance(value, float):
            return f"{value:.6g}"
        return str(value) if value is not None else ""

    rendered_rows = [[cell(row.get(header, "")) for header in headers] for row in rows]
    widths = [
        max(len(header), *(len(row[index]) for row in rendered_rows))
        for index, header in enumerate(headers)
    ]
    header_line = (
        "| "
        + " | ".join(header.ljust(widths[index]) for index, header in enumerate(headers))
        + " |"
    )
    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    body = [
        "| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(headers))) + " |"
        for row in rendered_rows
    ]
    return "\n".join([header_line, separator, *body])


def load_processor(processor_dir: Path | None, base_model: str) -> Any:
    *_, WhisperForConditionalGeneration, WhisperProcessor = require_eval_dependencies()
    del WhisperForConditionalGeneration
    source = processor_dir if processor_dir is not None and processor_dir.exists() else base_model
    return WhisperProcessor.from_pretrained(str(source))


def configure_generation_model(eval_model: Any) -> Any:
    # Newer transformers versions reject generation overrides written to
    # model.config. Keep decoding controls on generation_config instead.
    if hasattr(eval_model, "generation_config"):
        eval_model.generation_config.forced_decoder_ids = None
        eval_model.generation_config.suppress_tokens = []
    eval_model.eval()
    return eval_model


def load_base_eval_model(base_model: str, device: str) -> Any:
    *_, WhisperForConditionalGeneration, _WhisperProcessor = require_eval_dependencies()
    eval_model = WhisperForConditionalGeneration.from_pretrained(base_model).to(device)
    return configure_generation_model(eval_model)


def load_lora_eval_model(base_model: str, adapter_dir: Path, device: str) -> Any:
    *_, PeftModel, WhisperForConditionalGeneration, _WhisperProcessor = require_eval_dependencies()
    if not adapter_dir.exists():
        raise FileNotFoundError(f"Adapter directory not found: {adapter_dir}")
    base = WhisperForConditionalGeneration.from_pretrained(base_model).to(device)
    adapted = PeftModel.from_pretrained(base, adapter_dir)
    adapted = adapted.merge_and_unload().to(device)
    return configure_generation_model(adapted)


def build_generate_kwargs(row: ManifestRow, language_mode: str, num_beams: int) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "num_beams": num_beams,
        "do_sample": False,
        "max_new_tokens": 225,
    }
    if language_mode == "auto":
        return kwargs
    if language_mode == "hi" or (language_mode == "manifest" and row.language == "hi"):
        kwargs.update({"language": "hi", "task": "transcribe"})
        return kwargs
    if language_mode == "manifest":
        return kwargs
    raise ValueError(f"Unknown language mode: {language_mode}")


def transcribe_one(
    eval_model: Any,
    processor: Any,
    audio_path: Path,
    device: str,
    generate_kwargs: dict[str, Any],
) -> str:
    librosa, torch, *_ = require_eval_dependencies()
    array, _sample_rate = librosa.load(str(audio_path), sr=16000, mono=True)
    inputs = processor.feature_extractor(array, sampling_rate=16000, return_tensors="pt")
    input_features = inputs.input_features.to(device)
    with torch.no_grad():
        pred_ids = eval_model.generate(input_features, **generate_kwargs)
    return processor.batch_decode(pred_ids, skip_special_tokens=True)[0].strip()


def corpus_metrics(predictions: list[dict[str, Any]]) -> dict[str, float]:
    _librosa, _torch, jiwer_cer, jiwer_wer, *_ = require_eval_dependencies()
    refs = [normalize_text(item["reference_text"]) for item in predictions]
    hyps = [normalize_text(item["hypothesis_text"]) for item in predictions]
    return {
        "corpus_wer": float(jiwer_wer(refs, hyps)),
        "corpus_cer": float(jiwer_cer(refs, hyps)),
    }


def sample_metrics(reference: str, hypothesis: str) -> dict[str, float]:
    from .cer import character_error_rate
    from .wer import word_error_rate

    return {
        "wer": word_error_rate(reference, hypothesis),
        "cer": character_error_rate(reference, hypothesis),
    }


def summarize_predictions(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if not predictions:
        raise ValueError("Cannot summarize empty predictions")
    return {
        "files": len(predictions),
        "macro_wer": float(mean(item["wer"] for item in predictions)),
        "macro_cer": float(mean(item["cer"] for item in predictions)),
        **corpus_metrics(predictions),
    }


def evaluate_model_on_manifest(
    eval_model: Any,
    processor: Any,
    rows: list[ManifestRow],
    manifest_path: Path,
    model_label: str,
    base_model: str,
    adapter_dir: Path | None,
    run_name: str,
    language_mode: str,
    device: str,
    num_beams: int,
    output_dir: Path,
) -> dict[str, Any]:
    predictions: list[dict[str, Any]] = []
    for row in progress(rows, desc=f"{model_label} {manifest_path.stem} beam{num_beams}"):
        if not row.audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {row.audio_path}")
        hypothesis = transcribe_one(
            eval_model,
            processor,
            row.audio_path,
            device,
            build_generate_kwargs(row, language_mode, num_beams),
        )
        predictions.append(
            {
                "model": model_label,
                "base_model": base_model,
                "adapter": str(adapter_dir) if adapter_dir is not None else None,
                "run_name": run_name,
                "manifest": str(manifest_path),
                "slice": row.slice,
                "condition": row.condition,
                "language": row.language,
                "language_mode": language_mode,
                "num_beams": num_beams,
                "audio_path": str(row.audio_path),
                "reference_text": row.reference_text,
                "hypothesis_text": hypothesis,
                **sample_metrics(row.reference_text, hypothesis),
            }
        )

    summary = {
        **summarize_predictions(predictions),
        "model": model_label,
        "base_model": base_model,
        "adapter": str(adapter_dir) if adapter_dir is not None else None,
        "run_name": run_name,
        "slice": predictions[0]["slice"],
        "condition": predictions[0]["condition"],
        "language_mode": language_mode,
        "num_beams": num_beams,
    }
    payload = {"summary": summary, "samples": predictions}
    out_json = output_dir / (
        f"{run_name}_{model_label}_{manifest_path.stem}_beam{num_beams}.json"
    )
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"file": str(out_json), **summary}


def comparison_rows(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base_rows = {
        (item["slice"], item["num_beams"], item["files"]): item
        for item in summaries
        if item["model"].endswith("_base")
    }
    rows: list[dict[str, Any]] = []
    for item in summaries:
        if not item["model"].endswith("_lora"):
            continue
        key = (item["slice"], item["num_beams"], item["files"])
        base = base_rows.get(key)
        if base is None:
            continue
        rows.append(
            {
                "slice": item["slice"],
                "num_beams": item["num_beams"],
                "files": item["files"],
                "base_macro_wer": base["macro_wer"],
                "lora_macro_wer": item["macro_wer"],
                "delta_macro_wer": item["macro_wer"] - base["macro_wer"],
                "base_corpus_wer": base["corpus_wer"],
                "lora_corpus_wer": item["corpus_wer"],
                "delta_corpus_wer": item["corpus_wer"] - base["corpus_wer"],
            }
        )
    return sorted(rows, key=lambda row: (row["slice"], row["num_beams"]))


def write_summary_tables(run_name: str, output_dir: Path, summaries: list[dict[str, Any]]) -> None:
    summary_json_path = output_dir / f"{run_name}_eval_summary.json"
    summary_md_path = output_dir / f"{run_name}_eval_summary.md"
    comparison_md_path = output_dir / f"{run_name}_base_vs_lora_comparison.md"

    summary_json_path.write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary_md_path.write_text(markdown_table(summaries) + "\n", encoding="utf-8")

    comparisons = comparison_rows(summaries)
    if comparisons:
        comparison_md_path.write_text(
            markdown_table(comparisons) + "\n",
            encoding="utf-8",
        )

    print("Per-run summaries:")
    print(markdown_table(summaries))
    if comparisons:
        print("\nBase vs LoRA comparison:")
        print(markdown_table(comparisons))
    print(f"\nWrote {summary_json_path}")
    print(f"Wrote {summary_md_path}")
    if comparisons:
        print(f"Wrote {comparison_md_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reload a committed Whisper LoRA adapter and evaluate it on fixed manifests."
    )
    parser.add_argument(
        "--manifest",
        action="append",
        required=True,
        help="CSV manifest path. Repeat for multiple fixed slices.",
    )
    parser.add_argument(
        "--base-model",
        default="openai/whisper-small",
        help="Base HF Whisper model",
    )
    parser.add_argument("--adapter-dir", default=DEFAULT_ADAPTER_DIR, help="LoRA adapter directory")
    parser.add_argument(
        "--processor-dir",
        default=DEFAULT_PROCESSOR_DIR,
        help="Processor/tokenizer directory. Falls back to --base-model if missing.",
    )
    parser.add_argument("--output-dir", default="results/lora_reload_eval", help="Output directory")
    parser.add_argument(
        "--run-name",
        default=DEFAULT_RUN_NAME,
        help="Stable output filename prefix",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Root used to resolve relative manifest audio paths",
    )
    parser.add_argument(
        "--language-mode",
        choices=("manifest", "hi", "auto"),
        default="manifest",
        help="Use manifest Hindi hints, force Hindi, or let Whisper auto-detect.",
    )
    parser.add_argument(
        "--num-beams",
        action="append",
        type=int,
        default=None,
        help="Decode beam count",
    )
    parser.add_argument("--seed", type=int, default=0, help="Generation seed")
    parser.add_argument("--device", default="auto", help="auto, cpu, cuda, cuda:0, etc.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional debug row limit per manifest",
    )
    parser.add_argument("--skip-base", action="store_true", help="Only evaluate the LoRA adapter")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    set_seed(args.seed)
    device = resolve_device(args.device)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_paths = [Path(path) for path in args.manifest]
    rows_by_manifest = {
        manifest_path: load_manifest(manifest_path, repo_root=args.repo_root)[: args.limit]
        if args.limit is not None
        else load_manifest(manifest_path, repo_root=args.repo_root)
        for manifest_path in manifest_paths
    }
    num_beams_values = args.num_beams or [1, 5]
    processor = load_processor(Path(args.processor_dir), args.base_model)
    adapter_dir = Path(args.adapter_dir)

    all_summaries: list[dict[str, Any]] = []
    model_jobs = []
    if not args.skip_base:
        model_jobs.append(("hf_whisper_small_base", None, load_base_eval_model))
    model_jobs.append(("hf_whisper_small_lora", adapter_dir, load_lora_eval_model))

    for model_label, job_adapter_dir, loader in model_jobs:
        if job_adapter_dir is None:
            eval_model = loader(args.base_model, device)
        else:
            eval_model = loader(args.base_model, job_adapter_dir, device)
        for manifest_path, rows in rows_by_manifest.items():
            for num_beams in num_beams_values:
                all_summaries.append(
                    evaluate_model_on_manifest(
                        eval_model=eval_model,
                        processor=processor,
                        rows=rows,
                        manifest_path=manifest_path,
                        model_label=model_label,
                        base_model=args.base_model,
                        adapter_dir=job_adapter_dir,
                        run_name=args.run_name,
                        language_mode=args.language_mode,
                        device=device,
                        num_beams=num_beams,
                        output_dir=output_dir,
                    )
                )
        del eval_model
        gc.collect()
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

    write_summary_tables(args.run_name, output_dir, all_summaries)


if __name__ == "__main__":
    main()
