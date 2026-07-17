"""Speaker-clustered bootstrap analysis for paired ASR channel evaluations."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Sequence

import numpy as np


def load_prediction_rows(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}") from exc
    if not rows:
        raise ValueError(f"Prediction file is empty: {path}")
    return rows


def build_count_arrays(
    reference_rows: Sequence[dict],
    candidate_rows: Sequence[dict],
) -> tuple[list[str], list[str], dict[tuple[str, str], np.ndarray]]:
    """Validate paired rows and return per-speaker error/reference-word arrays."""
    all_rows = [list(reference_rows), list(candidate_rows)]
    model_labels = [str(rows[0]["model_label"]) for rows in all_rows]
    if model_labels[0] == model_labels[1]:
        raise ValueError("Reference and candidate model labels must differ")

    speaker_sets = [{str(row["sample_key"]) for row in rows} for rows in all_rows]
    condition_sets = [{str(row["condition"]) for row in rows} for rows in all_rows]
    if speaker_sets[0] != speaker_sets[1]:
        raise ValueError("Prediction files do not contain identical speaker/sample keys")
    if condition_sets[0] != condition_sets[1]:
        raise ValueError("Prediction files do not contain identical conditions")
    if "original" not in condition_sets[0]:
        raise ValueError("Paired bootstrap requires an original condition")

    speakers = sorted(speaker_sets[0])
    conditions = ["original", *sorted(condition_sets[0] - {"original"})]
    speaker_index = {speaker: index for index, speaker in enumerate(speakers)}
    arrays: dict[tuple[str, str], np.ndarray] = {}

    for model_label, rows in zip(model_labels, all_rows, strict=True):
        if any(str(row["model_label"]) != model_label for row in rows):
            raise ValueError(f"Prediction file mixes model labels: {model_label}")
        expected = {(speaker, condition) for speaker in speakers for condition in conditions}
        observed: set[tuple[str, str]] = set()
        for row in rows:
            key = (str(row["sample_key"]), str(row["condition"]))
            if key in observed:
                raise ValueError(f"Duplicate prediction row for {model_label}: {key}")
            observed.add(key)
        if observed != expected:
            missing = sorted(expected - observed)[:5]
            extra = sorted(observed - expected)[:5]
            raise ValueError(f"Incomplete paired rows for {model_label}; missing={missing}, extra={extra}")

        for condition in conditions:
            counts = np.zeros((len(speakers), 2), dtype=np.int64)
            for row in rows:
                if str(row["condition"]) != condition:
                    continue
                index = speaker_index[str(row["sample_key"])]
                errors = int(row["errors"])
                reference_words = int(row["reference_words"])
                if errors < 0 or reference_words <= 0:
                    raise ValueError(f"Invalid score counts for {model_label}: {row}")
                counts[index] = (errors, reference_words)
            arrays[model_label, condition] = counts

        arrays[model_label, "pooled_telephone"] = sum(
            (arrays[model_label, condition] for condition in conditions[1:]),
            start=np.zeros((len(speakers), 2), dtype=np.int64),
        )

    return model_labels, conditions, arrays


def _corpus_wer(counts: np.ndarray) -> float:
    return float(counts[:, 0].sum() / counts[:, 1].sum())


def paired_bootstrap_rows(
    reference_rows: Sequence[dict],
    candidate_rows: Sequence[dict],
    *,
    replicates: int = 20_000,
    seed: int = 0,
    chunk_size: int = 1_000,
) -> list[dict]:
    """Bootstrap corpus-WER metrics by resampling paired speakers with replacement."""
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    model_labels, conditions, arrays = build_count_arrays(reference_rows, candidate_rows)
    reference_model, candidate_model = model_labels
    transformed = conditions[1:]
    slices = [*conditions, "pooled_telephone"]
    speakers = arrays[reference_model, "original"].shape[0]

    point_wer = {
        (model, slice_name): _corpus_wer(arrays[model, slice_name])
        for model in model_labels
        for slice_name in slices
    }
    point_penalty = {
        (model, slice_name): point_wer[model, slice_name] - point_wer[model, "original"]
        for model in model_labels
        for slice_name in [*transformed, "pooled_telephone"]
    }

    metric_keys: list[tuple[str, str, str | None]] = []
    for model in model_labels:
        for slice_name in [*transformed, "pooled_telephone"]:
            metric_keys.append(("channel_penalty", slice_name, model))
    for slice_name in slices:
        metric_keys.append(("model_gap", slice_name, None))
    for slice_name in [*transformed, "pooled_telephone"]:
        metric_keys.append(("channel_penalty_gap", slice_name, None))

    samples = {key: np.empty(replicates, dtype=np.float64) for key in metric_keys}
    rng = np.random.default_rng(seed)
    for start in range(0, replicates, chunk_size):
        size = min(chunk_size, replicates - start)
        indices = rng.integers(0, speakers, size=(size, speakers))
        bootstrap_wer: dict[tuple[str, str], np.ndarray] = {}
        for model in model_labels:
            for slice_name in slices:
                counts = arrays[model, slice_name]
                errors = counts[indices, 0].sum(axis=1)
                reference_words = counts[indices, 1].sum(axis=1)
                bootstrap_wer[model, slice_name] = errors / reference_words

        for model in model_labels:
            for slice_name in [*transformed, "pooled_telephone"]:
                key = ("channel_penalty", slice_name, model)
                samples[key][start : start + size] = (
                    bootstrap_wer[model, slice_name] - bootstrap_wer[model, "original"]
                )
        for slice_name in slices:
            key = ("model_gap", slice_name, None)
            samples[key][start : start + size] = (
                bootstrap_wer[candidate_model, slice_name]
                - bootstrap_wer[reference_model, slice_name]
            )
        for slice_name in [*transformed, "pooled_telephone"]:
            key = ("channel_penalty_gap", slice_name, None)
            candidate_penalty = (
                bootstrap_wer[candidate_model, slice_name]
                - bootstrap_wer[candidate_model, "original"]
            )
            reference_penalty = (
                bootstrap_wer[reference_model, slice_name]
                - bootstrap_wer[reference_model, "original"]
            )
            samples[key][start : start + size] = candidate_penalty - reference_penalty

    output = []
    for metric, slice_name, model in metric_keys:
        if metric == "channel_penalty":
            estimate = point_penalty[model, slice_name]
        elif metric == "model_gap":
            estimate = (
                point_wer[candidate_model, slice_name] - point_wer[reference_model, slice_name]
            )
        else:
            estimate = (
                point_penalty[candidate_model, slice_name]
                - point_penalty[reference_model, slice_name]
            )
        lower, upper = np.percentile(samples[metric, slice_name, model], [2.5, 97.5])
        output.append(
            {
                "metric": metric,
                "model_label": model,
                "slice": slice_name,
                "estimate": float(estimate),
                "ci_95_lower": float(lower),
                "ci_95_upper": float(upper),
                "speakers": speakers,
                "replicates": replicates,
                "seed": seed,
                "reference_model": reference_model,
                "candidate_model": candidate_model,
            }
        )
    return output


def write_outputs(rows: Sequence[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "paired_bootstrap_v1.json"
    csv_path = output_dir / "paired_bootstrap_v1.csv"
    markdown_path = output_dir / "paired_bootstrap_v1.md"
    json_path.write_text(json.dumps(list(rows), indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    columns = ["metric", "model_label", "slice", "estimate", "ci_95_lower", "ci_95_upper"]
    lines = [
        "# Paired Speaker Bootstrap v1",
        "",
        "95% percentile intervals from paired speaker-level resampling.",
        "",
        "| " + " | ".join(columns) + " |",
        "|" + "|".join("---" for _ in columns) + "|",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = row[column]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value or ""))
        lines.append("| " + " | ".join(values) + " |")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-predictions", type=Path, required=True)
    parser.add_argument("--candidate-predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = paired_bootstrap_rows(
        load_prediction_rows(args.reference_predictions),
        load_prediction_rows(args.candidate_predictions),
        replicates=args.replicates,
        seed=args.seed,
    )
    write_outputs(rows, args.output_dir)
    print(f"Wrote paired bootstrap outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
