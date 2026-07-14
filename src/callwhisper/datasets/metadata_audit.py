"""Audit whether GramVaani source-rate slices differ in speaker and quality metadata."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable

from tqdm.auto import tqdm

from callwhisper.datasets.gramvaani_inventory import probe_audio, read_keyed_text


UNKNOWN_VALUES = {"", "na", "n/a", "none", "null", "unknown"}


def normalize_label(value: str | None) -> str:
    normalized = (value or "").strip()
    lowered = normalized.lower()
    return "unknown" if lowered in UNKNOWN_VALUES or lowered.endswith("_unknown") else normalized


def read_utt2labels(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames or "Uttids" not in reader.fieldnames:
            raise ValueError(f"Expected a tab-separated Uttids column in {path}")
        rows: dict[str, dict[str, str]] = {}
        for row in reader:
            utterance_id = row["Uttids"].strip()
            if utterance_id in rows:
                raise ValueError(f"Duplicate ID {utterance_id!r} in {path}")
            rows[utterance_id] = {
                key: normalize_label(value)
                for key, value in row.items()
                if key is not None and key != "Uttids"
            }
    return rows


def manifest_ids(path: Path | None) -> set[str] | None:
    if path is None:
        return None
    with path.open(encoding="utf-8", newline="") as handle:
        return {Path(row["audio_path"]).stem for row in csv.DictReader(handle)}


def inventory_from_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"utterance_id", "sample_rate_hz"}
    missing = required - set(rows[0] if rows else [])
    if missing:
        raise ValueError(f"Inventory {path} is missing columns: {sorted(missing)}")
    return [
        {
            **row,
            "sample_rate_hz": int(row["sample_rate_hz"]),
            "source_rate_group": row.get("source_rate_group")
            or ("native_8khz" if int(row["sample_rate_hz"]) == 8000 else "higher_rate"),
        }
        for row in rows
    ]


def probe_dataset(
    dataset_dir: Path, selected_ids: set[str] | None, workers: int
) -> list[dict[str, Any]]:
    scp_path = next(
        (path for path in (dataset_dir / "mp3.scp", dataset_dir / "wav.scp") if path.exists()),
        None,
    )
    if scp_path is None:
        raise FileNotFoundError(f"Expected mp3.scp or wav.scp under {dataset_dir}")

    audio_index = read_keyed_text(scp_path)
    candidates = [
        (
            utterance_id,
            relative_path.removeprefix("./"),
            (dataset_dir / relative_path).resolve(),
        )
        for utterance_id, relative_path in sorted(audio_index.items())
        if selected_ids is None or utterance_id in selected_ids
    ]
    missing_files = [str(path) for _, _, path in candidates if not path.exists()]
    if missing_files:
        raise FileNotFoundError(
            f"Missing {len(missing_files)} audio files; first: {missing_files[0]}"
        )

    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(probe_audio, audio_path): (utterance_id, relative_path)
            for utterance_id, relative_path, audio_path in candidates
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Probing source rates"):
            utterance_id, relative_path = futures[future]
            metadata = future.result()
            sample_rate = int(metadata["sample_rate_hz"])
            rows.append(
                {
                    "utterance_id": utterance_id,
                    "audio_path": relative_path,
                    "sample_rate_hz": sample_rate,
                    "source_rate_group": "native_8khz" if sample_rate == 8000 else "higher_rate",
                }
            )
    return sorted(rows, key=lambda row: row["utterance_id"])


def join_metadata(
    inventory: Iterable[dict[str, Any]], labels: dict[str, dict[str, str]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in inventory:
        metadata = labels.get(item["utterance_id"], {})
        rows.append(
            {
                **item,
                "gender": normalize_label(metadata.get("Gender")),
                "accent": normalize_label(metadata.get("Accent")),
                "district": normalize_label(metadata.get("District")),
                "state": normalize_label(metadata.get("State")),
                "other": normalize_label(metadata.get("Other")),
            }
        )
    return rows


def cross_tab(rows: Iterable[dict[str, Any]], column: str) -> dict[str, dict[str, int]]:
    groups: dict[str, Counter[str]] = {}
    for row in rows:
        category = normalize_label(str(row.get(column, "")))
        rate_group = str(row["source_rate_group"])
        groups.setdefault(category, Counter())[rate_group] += 1
    return {
        category: {
            "native_8khz": counts.get("native_8khz", 0),
            "higher_rate": counts.get("higher_rate", 0),
            "total": sum(counts.values()),
        }
        for category, counts in sorted(
            groups.items(), key=lambda item: (-sum(item[1].values()), item[0])
        )
    }


def cramers_v(table: dict[str, dict[str, int]]) -> float | None:
    matrix = [
        [counts["native_8khz"], counts["higher_rate"]]
        for counts in table.values()
        if counts["total"] > 0
    ]
    if len(matrix) < 2:
        return None
    total = sum(sum(row) for row in matrix)
    column_totals = [sum(row[index] for row in matrix) for index in range(2)]
    chi_square = 0.0
    for row in matrix:
        row_total = sum(row)
        for index, observed in enumerate(row):
            expected = row_total * column_totals[index] / total
            if expected:
                chi_square += (observed - expected) ** 2 / expected
    denominator = total * min(len(matrix) - 1, 1)
    return math.sqrt(chi_square / denominator) if denominator else None


def native_rate_odds_ratio(
    table: dict[str, dict[str, int]], first: str, second: str
) -> float | None:
    first_counts = table.get(first)
    second_counts = table.get(second)
    if not first_counts or not second_counts:
        return None
    cells = (
        first_counts["native_8khz"],
        first_counts["higher_rate"],
        second_counts["native_8khz"],
        second_counts["higher_rate"],
    )
    if any(value == 0 for value in cells):
        return None
    return (cells[0] / cells[1]) / (cells[2] / cells[3])


def quality_markers(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, int]]:
    markers = ("inaudible", "audio_jump", "background_noise", "multiple_speakers")
    result: dict[str, dict[str, int]] = {}
    rows_list = list(rows)
    for marker in markers:
        result[marker] = {
            rate_group: sum(
                marker in str(row["other"]).lower()
                for row in rows_list
                if row["source_rate_group"] == rate_group
            )
            for rate_group in ("native_8khz", "higher_rate")
        }
    return result


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    gender = cross_tab(rows, "gender")
    accent = cross_tab(rows, "accent")
    state = cross_tab(rows, "state")
    rates = Counter(str(row["sample_rate_hz"]) for row in rows)
    return {
        "files": len(rows),
        "source_rate_counts": dict(Counter(row["source_rate_group"] for row in rows)),
        "sample_rate_counts": dict(sorted(rates.items(), key=lambda item: int(item[0]))),
        "gender_by_source_rate": gender,
        "accent_by_source_rate": accent,
        "state_by_source_rate": state,
        "quality_markers_by_source_rate": quality_markers(rows),
        "association": {
            "gender_source_rate_cramers_v": cramers_v(gender),
            "accent_source_rate_cramers_v": cramers_v(accent),
            "state_source_rate_cramers_v": cramers_v(state),
            "male_vs_female_native_8khz_odds_ratio": native_rate_odds_ratio(
                gender, "Male", "Female"
            ),
        },
    }


def _format_table(table: dict[str, dict[str, int]], limit: int | None = None) -> str:
    rows = list(table.items())[:limit]
    lines = [
        "| Category | Native 8 kHz | Higher rate | Total | Native 8 kHz share |",
        "|---|---:|---:|---:|---:|",
    ]
    for category, counts in rows:
        share = counts["native_8khz"] / counts["total"] if counts["total"] else 0.0
        lines.append(
            f"| {category} | {counts['native_8khz']} | {counts['higher_rate']} | "
            f"{counts['total']} | {share:.1%} |"
        )
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any]) -> str:
    association = summary["association"]
    rate_counts = summary["source_rate_counts"]
    lines = [
        "# GramVaani Source-Rate Confound Audit v1",
        "",
        "## Finding",
        "",
        "The native-8-kHz and higher-rate GramVaani groups are compositionally different. "
        "A raw WER difference between them is observational and must not be interpreted as "
        "the causal cost of 8 kHz bandwidth.",
        "",
        f"Audited files: `{summary['files']}`. Native 8 kHz: "
        f"`{rate_counts.get('native_8khz', 0)}`. Higher rate: "
        f"`{rate_counts.get('higher_rate', 0)}`.",
        "",
        "## Gender Metadata",
        "",
        "Gender values are dataset-provided metadata, not independently verified identity labels.",
        "",
        _format_table(summary["gender_by_source_rate"]),
        "",
        f"Cramer's V for gender versus source-rate group: "
        f"`{association['gender_source_rate_cramers_v']:.3f}`.",
    ]
    odds_ratio = association["male_vs_female_native_8khz_odds_ratio"]
    if odds_ratio is not None:
        lines.extend(
            [
                "",
                "Using only the dataset's `Male` and `Female` labels, the odds that a male-labeled "
                f"clip is native 8 kHz are `{odds_ratio:.2f}x` the corresponding female-labeled odds.",
            ]
        )
    lines.extend(
        [
            "",
            "## Accent Metadata",
            "",
            _format_table(summary["accent_by_source_rate"], limit=12),
            "",
            f"Cramer's V for accent versus source-rate group: "
            f"`{association['accent_source_rate_cramers_v']:.3f}`.",
            "",
            "## State Metadata",
            "",
            _format_table(summary["state_by_source_rate"], limit=12),
            "",
            f"Cramer's V for state versus source-rate group: "
            f"`{association['state_source_rate_cramers_v']:.3f}`.",
            "",
            "## Quality Markers",
            "",
            "These counts come from substring matches in the dataset's `Other` metadata field.",
            "",
            "| Marker | Native 8 kHz | Higher rate |",
            "|---|---:|---:|",
        ]
    )
    for marker, counts in summary["quality_markers_by_source_rate"].items():
        lines.append(
            f"| {marker} | {counts.get('native_8khz', 0)} | {counts.get('higher_rate', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Consequence",
            "",
            "Use the native source-rate slice as a real-world deployment view, but use paired "
            "transformations of the same utterances to estimate a channel penalty. Speaker, content, "
            "region, reference, and recording should stay fixed while only the channel changes.",
            "",
            "## Reproduction",
            "",
            "```bash",
            "callwhisper-metadata-audit \\",
            "  --dataset-dir datasets/GV_Dev_5h \\",
            "  --output-prefix results/gramvaani_source_rate_confound_audit_v1",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "utterance_id",
        "audio_path",
        "sample_rate_hz",
        "source_rate_group",
        "gender",
        "accent",
        "district",
        "state",
        "other",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--inventory-csv")
    parser.add_argument("--manifest")
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--workers", type=int, default=16)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    dataset_dir = Path(args.dataset_dir).resolve()
    selected_ids = manifest_ids(Path(args.manifest)) if args.manifest else None
    if args.inventory_csv:
        inventory = inventory_from_csv(Path(args.inventory_csv))
        if selected_ids is not None:
            inventory = [row for row in inventory if row["utterance_id"] in selected_ids]
    else:
        inventory = probe_dataset(dataset_dir, selected_ids, args.workers)
    labels = read_utt2labels(dataset_dir / "utt2labels")
    rows = join_metadata(inventory, labels)
    summary = summarize(rows)

    prefix = Path(args.output_prefix)
    json_path = prefix.with_suffix(".json")
    md_path = prefix.with_suffix(".md")
    csv_path = prefix.parent / f"{prefix.name}_rows.csv"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    write_rows(csv_path, rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {md_path}, {json_path}, and {csv_path}")


if __name__ == "__main__":
    main()
