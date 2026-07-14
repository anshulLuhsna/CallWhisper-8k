from pathlib import Path

import pytest

from callwhisper.datasets.metadata_audit import (
    cramers_v,
    cross_tab,
    join_metadata,
    native_rate_odds_ratio,
    normalize_label,
    read_utt2labels,
    summarize,
)


def test_read_utt2labels_and_normalize_unknowns(tmp_path: Path) -> None:
    source = tmp_path / "utt2labels"
    source.write_text(
        "Uttids\tAccent\tGender\tOther\nclip-a\tBihari\tMale\tinaudible\nclip-b\tNA\tFemale\tNA\n",
        encoding="utf-8",
    )

    assert normalize_label("NA") == "unknown"
    assert normalize_label("Gender_unknown") == "unknown"
    assert read_utt2labels(source) == {
        "clip-a": {"Accent": "Bihari", "Gender": "Male", "Other": "inaudible"},
        "clip-b": {"Accent": "unknown", "Gender": "Female", "Other": "unknown"},
    }


def test_summary_exposes_source_rate_confound() -> None:
    inventory = [
        {"utterance_id": "m8", "sample_rate_hz": 8000, "source_rate_group": "native_8khz"},
        {"utterance_id": "m48", "sample_rate_hz": 48000, "source_rate_group": "higher_rate"},
        {"utterance_id": "f44", "sample_rate_hz": 44100, "source_rate_group": "higher_rate"},
        {"utterance_id": "f48", "sample_rate_hz": 48000, "source_rate_group": "higher_rate"},
    ]
    labels = {
        "m8": {"Gender": "Male", "Accent": "Bihari", "State": "Bihar", "Other": "inaudible"},
        "m48": {"Gender": "Male", "Accent": "Bihari", "State": "Bihar", "Other": "NA"},
        "f44": {"Gender": "Female", "Accent": "NA", "State": "Delhi", "Other": "audio_jump"},
        "f48": {"Gender": "Female", "Accent": "NA", "State": "Delhi", "Other": "NA"},
    }

    rows = join_metadata(inventory, labels)
    gender = cross_tab(rows, "gender")
    result = summarize(rows)

    assert gender["Male"] == {"native_8khz": 1, "higher_rate": 1, "total": 2}
    assert gender["Female"] == {"native_8khz": 0, "higher_rate": 2, "total": 2}
    assert result["quality_markers_by_source_rate"]["inaudible"]["native_8khz"] == 1
    assert cramers_v(gender) == pytest.approx(1 / 3**0.5)
    assert native_rate_odds_ratio(gender, "Male", "Female") is None


def test_native_rate_odds_ratio() -> None:
    table = {
        "Male": {"native_8khz": 10, "higher_rate": 2, "total": 12},
        "Female": {"native_8khz": 2, "higher_rate": 8, "total": 10},
    }

    assert native_rate_odds_ratio(table, "Male", "Female") == pytest.approx(20.0)
