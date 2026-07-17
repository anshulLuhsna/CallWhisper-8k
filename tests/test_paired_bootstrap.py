from __future__ import annotations

import math

import pytest

from callwhisper.eval.paired_bootstrap import build_count_arrays, paired_bootstrap_rows


def _rows(model: str, original_errors: list[int], transformed_errors: list[int]) -> list[dict]:
    rows = []
    for index, (original, transformed) in enumerate(
        zip(original_errors, transformed_errors, strict=True)
    ):
        for condition, errors in (("original", original), ("telephone", transformed)):
            rows.append(
                {
                    "model_label": model,
                    "sample_key": f"speaker-{index}",
                    "condition": condition,
                    "errors": errors,
                    "reference_words": 10,
                }
            )
    return rows


def test_build_count_arrays_rejects_missing_pair() -> None:
    reference = _rows("reference", [1, 1], [2, 2])
    candidate = _rows("candidate", [2, 2], [4, 4])[:-1]

    with pytest.raises(ValueError, match="speaker/sample keys|conditions|Incomplete"):
        build_count_arrays(reference, candidate)


def test_paired_bootstrap_reports_model_and_penalty_gaps() -> None:
    reference = _rows("reference", [1, 1, 1, 1], [2, 2, 2, 2])
    candidate = _rows("candidate", [2, 2, 2, 2], [5, 5, 5, 5])
    rows = paired_bootstrap_rows(reference, candidate, replicates=100, seed=7, chunk_size=20)
    by_key = {(row["metric"], row["model_label"], row["slice"]): row for row in rows}

    reference_penalty = by_key["channel_penalty", "reference", "telephone"]
    model_gap = by_key["model_gap", None, "telephone"]
    penalty_gap = by_key["channel_penalty_gap", None, "telephone"]

    assert math.isclose(reference_penalty["estimate"], 0.1)
    assert math.isclose(model_gap["estimate"], 0.3)
    assert math.isclose(penalty_gap["estimate"], 0.2)
    assert model_gap["ci_95_lower"] > 0
    assert penalty_gap["ci_95_lower"] > 0


def test_paired_bootstrap_validates_arguments() -> None:
    reference = _rows("reference", [1], [2])
    candidate = _rows("candidate", [2], [3])

    with pytest.raises(ValueError, match="replicates"):
        paired_bootstrap_rows(reference, candidate, replicates=0)
