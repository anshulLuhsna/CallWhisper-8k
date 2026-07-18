"""Create deterministic, leakage-aware manifests for channel adaptation."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence

from .paired_telephony import CONDITIONS, stable_key


TELEPHONE_CONDITIONS = tuple(condition for condition in CONDITIONS if condition != "original")


def effective_label_token_count(token_ids: Sequence[int], bos_token_id: int | None) -> int:
    """Count labels after the Whisper collator removes a shared BOS token."""
    if token_ids and bos_token_id is not None and token_ids[0] == bos_token_id:
        return len(token_ids) - 1
    return len(token_ids)


def recording_group_id(utterance_id: str) -> str:
    """Return the released filename prefix shared by clips from one recording group."""
    value = str(utterance_id).strip()
    head, separator, tail = value.rpartition("-")
    if not separator or not head or not tail:
        raise ValueError(f"Unexpected GramVaani utterance ID: {utterance_id!r}")
    return head


def stable_fraction(*parts: object) -> float:
    return int(stable_key(*parts)[:16], 16) / float(16**16)


def split_inventory(
    rows: Iterable[dict[str, Any]],
    *,
    eval_fraction: float = 0.05,
    seed: int = 0,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split whole recording groups into train and internal evaluation sets."""
    if not 0 < eval_fraction < 1:
        raise ValueError("eval_fraction must be between 0 and 1")

    train_rows: list[dict[str, Any]] = []
    eval_rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for source_row in rows:
        row = dict(source_row)
        utterance_id = str(row.get("utterance_id", "")).strip()
        if not utterance_id:
            raise ValueError("Inventory row is missing utterance_id")
        if utterance_id in seen_ids:
            raise ValueError(f"Duplicate utterance_id: {utterance_id}")
        seen_ids.add(utterance_id)
        group_id = recording_group_id(utterance_id)
        row["recording_group_id"] = group_id
        target = (
            eval_rows
            if stable_fraction(seed, "internal_eval", group_id) < eval_fraction
            else train_rows
        )
        target.append(row)

    if not train_rows or not eval_rows:
        raise ValueError("Deterministic split produced an empty partition")
    train_groups = {row["recording_group_id"] for row in train_rows}
    eval_groups = {row["recording_group_id"] for row in eval_rows}
    overlap = train_groups & eval_groups
    if overlap:
        raise AssertionError(f"Recording-group leakage detected: {sorted(overlap)[:5]}")
    return train_rows, eval_rows


def deterministic_limit(
    rows: Iterable[dict[str, Any]], limit: int | None, *, seed: int = 0
) -> list[dict[str, Any]]:
    values = list(rows)
    if limit is None:
        return sorted(values, key=lambda row: str(row["utterance_id"]))
    if limit <= 0:
        raise ValueError("limit must be positive")
    ranked = sorted(
        values,
        key=lambda row: stable_key(seed, "source_limit", row["utterance_id"]),
    )
    return ranked[: min(limit, len(ranked))]


def _view_row(source_row: dict[str, Any], condition: str, role: str) -> dict[str, Any]:
    utterance_id = str(source_row["utterance_id"])
    return {
        "view_id": f"{utterance_id}__{role}__{condition}",
        "utterance_id": utterance_id,
        "recording_group_id": source_row["recording_group_id"],
        "source_audio_path": source_row["audio_path"],
        "reference_text": source_row["reference_text"],
        "duration_s": source_row["duration_s"],
        "sample_rate_hz": source_row["sample_rate_hz"],
        "source_rate_group": source_row["source_rate_group"],
        "condition": condition,
    }


def build_training_views(
    rows: Iterable[dict[str, Any]],
    *,
    seed: int = 0,
    channel_stress_source_fraction: float = 1 / 3,
) -> list[dict[str, Any]]:
    """Keep every telephone source and add balanced codec stress to a subset.

    GramVaani is already telephone speech, so ``original`` means the released
    source channel rather than clean wideband replay. At the default fraction,
    original sources are 75% of all training views and extra channel-stress
    views are 25%.
    """
    if not 0 <= channel_stress_source_fraction <= 1:
        raise ValueError("channel_stress_source_fraction must be between 0 and 1")
    views: list[dict[str, Any]] = []
    for source_row in rows:
        utterance_id = str(source_row["utterance_id"])
        views.append(_view_row(source_row, "original", "train_source"))
        if (
            stable_fraction(seed, "channel_stress", utterance_id)
            < channel_stress_source_fraction
        ):
            condition_index = int(
                stable_key(seed, "train_condition", utterance_id)[:8], 16
            )
            condition = TELEPHONE_CONDITIONS[
                condition_index % len(TELEPHONE_CONDITIONS)
            ]
            views.append(_view_row(source_row, condition, "train_channel_stress"))
    return sorted(views, key=lambda row: row["view_id"])


def build_internal_eval_views(
    rows: Iterable[dict[str, Any]], *, seed: int = 0
) -> list[dict[str, Any]]:
    """Assign one balanced clean/channel condition to each held-out source clip."""
    views: list[dict[str, Any]] = []
    for source_row in rows:
        utterance_id = str(source_row["utterance_id"])
        condition_index = int(stable_key(seed, "eval_condition", utterance_id)[:8], 16)
        condition = CONDITIONS[condition_index % len(CONDITIONS)]
        views.append(_view_row(source_row, condition, "internal_eval"))
    return sorted(views, key=lambda row: row["view_id"])


def build_paired_eval_views(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Expand held-out sources across every fixed condition for a paired WER audit."""
    views = [
        _view_row(source_row, condition, "paired_internal_eval")
        for source_row in rows
        for condition in CONDITIONS
    ]
    return sorted(views, key=lambda row: row["view_id"])


def _hours(rows: Iterable[dict[str, Any]]) -> float:
    return sum(float(row["duration_s"]) for row in rows) / 3600


def summarize_artifacts(
    train_source: list[dict[str, Any]],
    eval_source: list[dict[str, Any]],
    train_views: list[dict[str, Any]],
    eval_views: list[dict[str, Any]],
    *,
    seed: int,
    eval_fraction: float,
) -> dict[str, Any]:
    train_groups = {row["recording_group_id"] for row in train_source}
    eval_groups = {row["recording_group_id"] for row in eval_source}
    return {
        "seed": seed,
        "eval_fraction": eval_fraction,
        "split_semantics": "recording-group-disjoint; speaker IDs are unavailable",
        "train_source_rows": len(train_source),
        "train_source_hours": _hours(train_source),
        "internal_eval_source_rows": len(eval_source),
        "internal_eval_source_hours": _hours(eval_source),
        "train_recording_groups": len(train_groups),
        "internal_eval_recording_groups": len(eval_groups),
        "recording_group_overlap": len(train_groups & eval_groups),
        "train_view_rows": len(train_views),
        "train_view_hours": _hours(train_views),
        "internal_eval_view_rows": len(eval_views),
        "internal_eval_view_hours": _hours(eval_views),
        "train_condition_counts": dict(sorted(Counter(row["condition"] for row in train_views).items())),
        "internal_eval_condition_counts": dict(
            sorted(Counter(row["condition"] for row in eval_views).items())
        ),
        "train_source_rate_counts": dict(
            sorted(Counter(row["source_rate_group"] for row in train_source).items())
        ),
        "internal_eval_source_rate_counts": dict(
            sorted(Counter(row["source_rate_group"] for row in eval_source).items())
        ),
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_artifacts(
    inventory_path: Path,
    output_dir: Path,
    *,
    eval_fraction: float = 0.05,
    seed: int = 0,
    max_train_sources: int | None = None,
    max_eval_sources: int | None = None,
) -> dict[str, Any]:
    inventory = read_csv(inventory_path)
    full_train_source, eval_source = split_inventory(
        inventory, eval_fraction=eval_fraction, seed=seed
    )
    train_source = deterministic_limit(full_train_source, max_train_sources, seed=seed)
    selected_eval_source = deterministic_limit(eval_source, max_eval_sources, seed=seed + 1)
    train_views = build_training_views(train_source, seed=seed)
    eval_views = build_internal_eval_views(selected_eval_source, seed=seed)
    summary = summarize_artifacts(
        train_source,
        eval_source,
        train_views,
        eval_views,
        seed=seed,
        eval_fraction=eval_fraction,
    )
    summary["inventory_rows"] = len(inventory)
    summary["full_train_source_rows_before_limit"] = len(full_train_source)
    summary["full_internal_eval_source_rows_before_limit"] = len(eval_source)
    summary["max_train_sources"] = max_train_sources
    summary["max_eval_sources"] = max_eval_sources

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "train_source.csv", train_source)
    write_csv(output_dir / "internal_eval_source.csv", eval_source)
    write_csv(output_dir / "train_views.csv", train_views)
    write_csv(output_dir / "internal_eval_views.csv", eval_views)
    (output_dir / "channel_adaptation_split_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--eval-fraction", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-train-sources", type=int)
    parser.add_argument("--max-eval-sources", type=int)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = build_artifacts(
        args.inventory,
        args.output_dir,
        eval_fraction=args.eval_fraction,
        seed=args.seed,
        max_train_sources=args.max_train_sources,
        max_eval_sources=args.max_eval_sources,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
