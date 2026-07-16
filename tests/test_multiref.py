from __future__ import annotations

import math

import pytest

from callwhisper.eval.multiref import (
    alignment_multireference_corpus_score,
    alignment_multireference_score,
    normalize_vaani_text,
)


def test_normalize_vaani_text_removes_annotations_and_punctuation() -> None:
    assert normalize_vaani_text("यह {English} [noise] ठीक है!") == "यह ठीक है"


def test_any_reference_can_make_hypothesis_fully_correct() -> None:
    score = alignment_multireference_score(
        ["मैं घर गया", "मैं घर गयी", "मैं घर को गया"],
        "मैं घर गयी",
    )

    assert score.errors == 0
    assert score.wer == 0.0


def test_substitution_counts_when_every_reference_rejects_token() -> None:
    score = alignment_multireference_score(["a b", "a c", "a d"], "a x")

    assert score.substitutions == 1
    assert score.insertions == 0
    assert score.deletions == 0
    assert score.reference_words == 2
    assert score.wer == 0.5


def test_inserted_token_is_free_when_one_reference_contains_it() -> None:
    score = alignment_multireference_score(["a b", "a x b", "a b"], "a x b")

    assert score.errors == 0
    assert score.reference_words == 3


def test_deletion_counts_only_when_shared_by_every_reference() -> None:
    shared = alignment_multireference_score(["a x b", "a x b", "a x b"], "a b")
    disputed = alignment_multireference_score(["a x b", "a b", "a x b"], "a b")

    assert shared.deletions == 1
    assert math.isclose(shared.wer, 1 / 3)
    assert disputed.deletions == 0
    assert disputed.wer == 0.0


def test_corpus_score_aggregates_counts_before_wer() -> None:
    score = alignment_multireference_corpus_score(
        [
            (["a b", "a b", "a b"], "a x"),
            (["c d e", "c d e", "c d e"], "c d e"),
        ]
    )

    assert score.substitutions == 1
    assert score.reference_words == 5
    assert score.wer == 0.2


def test_empty_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="reference"):
        alignment_multireference_score([], "hypothesis")
    with pytest.raises(ValueError, match="empty corpus"):
        alignment_multireference_corpus_score([])
