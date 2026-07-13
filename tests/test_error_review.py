import pytest

from callwhisper.eval.error_review import build_review_rows, pairwise_outcomes


def sample(audio_id, reference, hypothesis, wer, cer):
    return {
        "audio_path": f"datasets/GV_Dev_5h/Audio/{audio_id}.mp3",
        "reference_text": reference,
        "hypothesis_text": hypothesis,
        "slice": "gramvaani_dev_100_8khz",
        "wer": wer,
        "cer": cer,
    }


def test_build_review_rows_ranks_primary_errors_and_aligns_comparison():
    primary = [
        sample("a", "एक दो तीन", "एक", 0.7, 0.5),
        sample("b", "चार पांच", "", 1.0, 1.0),
    ]
    comparison = [
        sample("a", "एक दो तीन", "एक दो", 0.3, 0.2),
        sample("b", "चार पांच", "चार", 0.5, 0.4),
    ]

    rows = build_review_rows(primary, comparison, top_n=1)

    assert len(rows) == 1
    assert rows[0]["audio_id"] == "b"
    assert rows[0]["primary_minus_comparison_wer"] == 0.5


def test_build_review_rows_rejects_reference_mismatch():
    primary = [sample("a", "एक दो", "एक", 0.5, 0.2)]
    comparison = [sample("a", "अलग संदर्भ", "एक", 0.5, 0.2)]

    with pytest.raises(ValueError, match="Reference mismatch"):
        build_review_rows(primary, comparison, top_n=1)


def test_pairwise_outcomes_counts_per_file_wins():
    primary = [
        sample("a", "एक दो", "एक", 0.5, 0.2),
        sample("b", "तीन चार", "तीन", 0.5, 0.2),
        sample("c", "पांच छह", "पांच", 0.5, 0.2),
    ]
    comparison = [
        sample("a", "एक दो", "", 1.0, 1.0),
        sample("b", "तीन चार", "तीन", 0.5, 0.2),
        sample("c", "पांच छह", "पांच छह", 0.0, 0.0),
    ]

    assert pairwise_outcomes(primary, comparison) == {
        "primary_better": 1,
        "tied": 1,
        "primary_worse": 1,
    }
