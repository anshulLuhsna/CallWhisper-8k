"""Build a focused human-review sheet from two per-sample ASR result files."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank one model's worst ASR files and compare them with another model."
    )
    parser.add_argument(
        "--primary-json", required=True, help="Result JSON for the model under review"
    )
    parser.add_argument(
        "--comparison-json", required=True, help="Result JSON for a comparison model"
    )
    parser.add_argument("--primary-label", required=True, help="Short primary model label")
    parser.add_argument("--comparison-label", required=True, help="Short comparison model label")
    parser.add_argument("--top-n", type=int, default=15, help="Number of files to review")
    parser.add_argument("--output-csv", required=True, help="Review CSV output")
    parser.add_argument("--output-md", required=True, help="Review Markdown output")
    parser.add_argument("--audio-output-dir", default=None, help="Optional folder for copied audio")
    parser.add_argument(
        "--repo-root", default=".", help="Repository root for resolving local audio"
    )
    return parser.parse_args()


def load_samples(path: str | Path) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    samples = payload.get("samples")
    if not isinstance(samples, list) or not samples:
        raise ValueError(f"Result JSON {path} has no non-empty samples list")
    return samples


def sample_id(sample: dict[str, Any]) -> str:
    return Path(str(sample["audio_path"])).stem


def build_review_rows(
    primary_samples: list[dict[str, Any]],
    comparison_samples: list[dict[str, Any]],
    top_n: int,
) -> list[dict[str, Any]]:
    comparison_by_id = {sample_id(sample): sample for sample in comparison_samples}
    if len(comparison_by_id) != len(comparison_samples):
        raise ValueError("Comparison result contains duplicate audio IDs")

    ranked = sorted(
        primary_samples,
        key=lambda sample: (float(sample["wer"]), float(sample["cer"])),
        reverse=True,
    )[:top_n]
    rows = []
    for rank, primary in enumerate(ranked, start=1):
        audio_id = sample_id(primary)
        comparison = comparison_by_id.get(audio_id)
        if comparison is None:
            raise ValueError(f"Comparison result is missing audio ID {audio_id}")
        if primary["reference_text"] != comparison["reference_text"]:
            raise ValueError(f"Reference mismatch for audio ID {audio_id}")
        primary_wer = float(primary["wer"])
        comparison_wer = float(comparison["wer"])
        rows.append(
            {
                "rank": rank,
                "audio_id": audio_id,
                "audio_path": str(primary["audio_path"]),
                "slice": primary.get("slice", ""),
                "reference_text": primary["reference_text"],
                "primary_hypothesis": primary["hypothesis_text"],
                "primary_wer": primary_wer,
                "primary_cer": float(primary["cer"]),
                "comparison_hypothesis": comparison["hypothesis_text"],
                "comparison_wer": comparison_wer,
                "comparison_cer": float(comparison["cer"]),
                "primary_minus_comparison_wer": primary_wer - comparison_wer,
                "classification": "",
                "speech_understandable": "",
                "reference_quality": "",
                "audio_notes": "",
                "reviewer_notes": "",
            }
        )
    return rows


def pairwise_outcomes(
    primary_samples: list[dict[str, Any]],
    comparison_samples: list[dict[str, Any]],
) -> dict[str, int]:
    comparison_by_id = {sample_id(sample): sample for sample in comparison_samples}
    outcomes = {"primary_better": 0, "tied": 0, "primary_worse": 0}
    for primary in primary_samples:
        audio_id = sample_id(primary)
        comparison = comparison_by_id.get(audio_id)
        if comparison is None:
            raise ValueError(f"Comparison result is missing audio ID {audio_id}")
        primary_wer = float(primary["wer"])
        comparison_wer = float(comparison["wer"])
        if primary_wer < comparison_wer:
            outcomes["primary_better"] += 1
        elif primary_wer > comparison_wer:
            outcomes["primary_worse"] += 1
        else:
            outcomes["tied"] += 1
    return outcomes


def resolve_audio(audio_path: str, repo_root: Path) -> Path:
    original = Path(audio_path)
    candidates = [
        original,
        repo_root / "datasets" / "GV_Dev_5h" / "Audio" / original.name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not resolve audio file {original.name}")


def copy_review_audio(rows: list[dict[str, Any]], output_dir: Path, repo_root: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        source = resolve_audio(str(row["audio_path"]), repo_root)
        destination = output_dir / f"{int(row['rank']):02d}_{source.name}"
        shutil.copy2(source, destination)
        row["review_audio_path"] = str(destination)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def markdown_quote(text: object) -> str:
    value = str(text).strip().replace("\n", " ").replace("|", "\\|")
    return "> " + value if value else "> *(empty transcription)*"


def write_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    primary_label: str,
    comparison_label: str,
    outcomes: dict[str, int],
) -> None:
    total = sum(outcomes.values())
    lines = [
        "# ARTPARK Native 8 kHz Error Review v1",
        "",
        f"This sheet ranks the highest-WER `{primary_label}` predictions and shows `{comparison_label}` on the same files. Rankings select review candidates; they do not determine the human classification.",
        "",
        "For each file, listen once or twice and fill the five review fields. Compare both hypotheses against what is actually audible, not only against the supplied reference.",
        "",
        "Allowed primary classification: `model_failure`, `bad_audio`, `questionable_reference`, `mixed`, or `uncertain`.",
        "",
        "## Pairwise Context",
        "",
        f"Across all {total} files, `{primary_label}` had lower per-file WER than `{comparison_label}` on {outcomes['primary_better']} files, tied on {outcomes['tied']}, and had higher WER on {outcomes['primary_worse']}. The review list below still focuses on `{primary_label}`'s largest remaining errors, even when it remains better than the comparison model.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {int(row['rank']):02d}. `{row['audio_id']}`",
                "",
                f"- Review audio: `{row.get('review_audio_path', row['audio_path'])}`",
                f"- {primary_label}: WER `{row['primary_wer']:.4f}`, CER `{row['primary_cer']:.4f}`",
                f"- {comparison_label}: WER `{row['comparison_wer']:.4f}`, CER `{row['comparison_cer']:.4f}`",
                f"- WER delta ({primary_label} minus {comparison_label}): `{row['primary_minus_comparison_wer']:.4f}`",
                "",
                "Reference:",
                "",
                markdown_quote(row["reference_text"]),
                "",
                f"{primary_label} hypothesis:",
                "",
                markdown_quote(row["primary_hypothesis"]),
                "",
                f"{comparison_label} hypothesis:",
                "",
                markdown_quote(row["comparison_hypothesis"]),
                "",
                "- Classification:",
                "- Speech understandable (`yes` / `partly` / `no`):",
                "- Reference quality (`good` / `incomplete` / `wrong` / `uncertain`):",
                "- Audio notes:",
                "- Reviewer notes:",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    primary_samples = load_samples(args.primary_json)
    comparison_samples = load_samples(args.comparison_json)
    rows = build_review_rows(
        primary_samples,
        comparison_samples,
        args.top_n,
    )
    if args.audio_output_dir:
        copy_review_audio(rows, Path(args.audio_output_dir), Path(args.repo_root))
    write_csv(Path(args.output_csv), rows)
    write_markdown(
        Path(args.output_md),
        rows,
        args.primary_label,
        args.comparison_label,
        pairwise_outcomes(primary_samples, comparison_samples),
    )
    print(f"Wrote {args.output_csv}")
    print(f"Wrote {args.output_md}")
    if args.audio_output_dir:
        print(f"Copied {len(rows)} audio files to {args.audio_output_dir}")


if __name__ == "__main__":
    main()
