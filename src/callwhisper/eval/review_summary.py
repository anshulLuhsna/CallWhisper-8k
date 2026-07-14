"""Parse a completed Markdown error-review sheet into structured JSON."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(r"^## (?P<rank>\d+)\. `(?P<audio_id>[^`]+)`$")
FIELD_PATTERNS = {
    "classification": re.compile(r"^- Classification:\s*(.*)$"),
    "speech_understandable": re.compile(r"^- Speech understandable .*:\s*(.*)$"),
    "reference_quality": re.compile(r"^- Reference quality .*:\s*(.*)$"),
    "audio_notes": re.compile(r"^- Audio notes:\s*(.*)$"),
    "reviewer_notes": re.compile(r"^- Reviewer notes:\s*(.*)$"),
}
ALLOWED_CLASSIFICATIONS = {
    "model_failure",
    "bad_audio",
    "questionable_reference",
    "mixed",
    "uncertain",
}


def canonical_label(value: str) -> str:
    """Return the leading label from a review value with optional explanation."""
    return value.strip().lower().split(" - ", maxsplit=1)[0]


def parse_review_markdown(path: str | Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        heading_match = HEADING_RE.match(line)
        if heading_match:
            current = {
                "rank": int(heading_match.group("rank")),
                "audio_id": heading_match.group("audio_id"),
            }
            entries.append(current)
            continue
        if current is None:
            continue
        for field, pattern in FIELD_PATTERNS.items():
            match = pattern.match(line)
            if match:
                current[field] = match.group(1).strip()
                break

    if not entries:
        raise ValueError(f"No review entries found in {path}")
    for entry in entries:
        missing = [field for field in FIELD_PATTERNS if not entry.get(field)]
        if missing:
            raise ValueError(f"Review {entry['audio_id']} has empty fields: {', '.join(missing)}")
        classification = canonical_label(entry["classification"])
        if classification not in ALLOWED_CLASSIFICATIONS:
            raise ValueError(
                f"Review {entry['audio_id']} has invalid classification {classification!r}"
            )
        entry["classification"] = classification
    return entries


def summarize_reviews(entries: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "reviewed_files": len(entries),
        "classification_counts": dict(
            sorted(Counter(entry["classification"] for entry in entries).items())
        ),
        "speech_understandable_counts": dict(
            sorted(
                Counter(
                    canonical_label(entry["speech_understandable"]) for entry in entries
                ).items()
            )
        ),
        "reference_quality_counts": dict(
            sorted(
                Counter(canonical_label(entry["reference_quality"]) for entry in entries).items()
            )
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-md", required=True, help="Completed review Markdown file")
    parser.add_argument("--output-json", required=True, help="Structured JSON output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    entries = parse_review_markdown(args.review_md)
    payload = {
        "source_review": args.review_md,
        "summary": summarize_reviews(entries),
        "reviews": entries,
    }
    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
