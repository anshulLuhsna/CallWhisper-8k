import csv
import json
from pathlib import Path

import pytest

from callwhisper.datasets.channel_adaptation import (
    build_artifacts,
    build_internal_eval_views,
    build_paired_eval_views,
    build_training_views,
    effective_label_token_count,
    recording_group_id,
    split_inventory,
)


def row(utterance_id: str, rate_group: str = "native_8khz") -> dict[str, str]:
    return {
        "utterance_id": utterance_id,
        "audio_path": f"Audio/{utterance_id}.mp3",
        "reference_text": f"reference {utterance_id}",
        "duration_s": "10.0",
        "sample_rate_hz": "8000",
        "channels": "1",
        "source_rate_group": rate_group,
        "transcript_flags": "",
    }


def test_effective_label_token_count_removes_only_leading_bos() -> None:
    assert effective_label_token_count([50258, 1, 2], 50258) == 2
    assert effective_label_token_count([1, 2, 3], 50258) == 3
    assert effective_label_token_count([], 50258) == 0


def test_recording_group_id() -> None:
    assert recording_group_id("01-00003-02") == "01-00003"
    with pytest.raises(ValueError):
        recording_group_id("bad")


def test_split_keeps_recording_groups_together() -> None:
    rows = [row(f"01-{group:05d}-{clip:02d}") for group in range(100) for clip in (1, 2)]
    train, internal_eval = split_inventory(rows, eval_fraction=0.2, seed=7)
    train_groups = {item["recording_group_id"] for item in train}
    eval_groups = {item["recording_group_id"] for item in internal_eval}
    assert train_groups.isdisjoint(eval_groups)
    assert len(train) + len(internal_eval) == len(rows)


def test_training_views_keep_sources_and_add_balanced_channel_stress() -> None:
    rows = [
        {**row(f"01-{index:05d}-01"), "recording_group_id": f"01-{index:05d}"}
        for index in range(1000)
    ]
    views = build_training_views(rows, seed=0)
    conditions = {item["condition"] for item in views}
    assert conditions == {
        "original",
        "bandlimit_8k",
        "bandlimit_8k_g711_alaw",
        "bandlimit_8k_g711_mulaw",
        "bandlimit_8k_gsm_fr",
    }
    original_share = sum(item["condition"] == "original" for item in views) / len(views)
    assert 0.72 < original_share < 0.78
    assert sum(item["condition"] == "original" for item in views) == len(rows)


def test_internal_eval_has_one_view_per_source() -> None:
    rows = [
        {**row(f"01-{index:05d}-01"), "recording_group_id": f"01-{index:05d}"}
        for index in range(100)
    ]
    views = build_internal_eval_views(rows, seed=0)
    assert len(views) == len(rows)
    assert len({item["utterance_id"] for item in views}) == len(rows)


def test_paired_eval_expands_every_condition() -> None:
    rows = [
        {**row(f"01-{index:05d}-01"), "recording_group_id": f"01-{index:05d}"}
        for index in range(10)
    ]
    views = build_paired_eval_views(rows)
    assert len(views) == 50
    by_source = {}
    for item in views:
        by_source.setdefault(item["utterance_id"], set()).add(item["condition"])
    assert all(len(conditions) == 5 for conditions in by_source.values())


def test_build_artifacts_writes_auditable_manifests(tmp_path: Path) -> None:
    inventory_path = tmp_path / "inventory.csv"
    rows = [row(f"01-{group:05d}-{clip:02d}") for group in range(100) for clip in (1, 2)]
    with inventory_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    output_dir = tmp_path / "out"
    summary = build_artifacts(
        inventory_path,
        output_dir,
        eval_fraction=0.2,
        seed=3,
        max_train_sources=50,
        max_eval_sources=20,
    )

    assert summary["recording_group_overlap"] == 0
    assert summary["train_source_rows"] == 50
    assert summary["internal_eval_view_rows"] == 20
    assert summary["split_semantics"].startswith("recording-group-disjoint")
    persisted = json.loads(
        (output_dir / "channel_adaptation_split_summary.json").read_text(encoding="utf-8")
    )
    assert persisted == summary
    for name in (
        "train_source.csv",
        "internal_eval_source.csv",
        "train_views.csv",
        "internal_eval_views.csv",
    ):
        assert (output_dir / name).exists()
