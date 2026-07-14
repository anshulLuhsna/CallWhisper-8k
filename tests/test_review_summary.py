from pathlib import Path

import pytest

from callwhisper.eval.review_summary import parse_review_markdown, summarize_reviews


def test_parse_and_summarize_completed_review(tmp_path: Path) -> None:
    review = tmp_path / "review.md"
    review.write_text(
        """## 01. `clip-a`

- Classification: model_failure
- Speech understandable (`yes` / `partly` / `no`): yes
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: clear
- Reviewer notes: missed the first phrase

## 02. `clip-b`

- Classification: questionable_reference
- Speech understandable (`yes` / `partly` / `no`): partly
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): wrong - extra words
- Audio notes: mild echo
- Reviewer notes: hypothesis matches the audio
""",
        encoding="utf-8",
    )

    entries = parse_review_markdown(review)
    summary = summarize_reviews(entries)

    assert [entry["audio_id"] for entry in entries] == ["clip-a", "clip-b"]
    assert summary["classification_counts"] == {
        "model_failure": 1,
        "questionable_reference": 1,
    }
    assert summary["reference_quality_counts"] == {"good": 1, "wrong": 1}


def test_incomplete_review_is_rejected(tmp_path: Path) -> None:
    review = tmp_path / "review.md"
    review.write_text(
        """## 01. `clip-a`

- Classification:
- Speech understandable (`yes` / `partly` / `no`): yes
- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`): good
- Audio notes: clear
- Reviewer notes: none
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="empty fields: classification"):
        parse_review_markdown(review)
