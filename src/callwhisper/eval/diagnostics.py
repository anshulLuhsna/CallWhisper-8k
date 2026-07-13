"""Diagnostic reporting for per-sample ASR predictions."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
LATIN_RE = re.compile(r"[A-Za-z]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build benchmark diagnostics from per-sample prediction CSVs."
    )
    parser.add_argument(
        "--predictions-csv",
        action="append",
        default=[],
        help="Per-sample prediction CSV with reference_text and hypothesis_text columns.",
    )
    parser.add_argument(
        "--predictions-json",
        action="append",
        default=[],
        help="Evaluation JSON containing a top-level samples list.",
    )
    parser.add_argument(
        "--output-json",
        default="results/benchmark_diagnostics_v1.json",
        help="Path for diagnostic JSON output.",
    )
    parser.add_argument(
        "--output-md",
        default="results/benchmark_diagnostics_v1.md",
        help="Path for diagnostic Markdown output.",
    )
    parser.add_argument(
        "--top-examples",
        type=int,
        default=12,
        help="Number of high-risk examples to include in Markdown.",
    )
    parser.add_argument(
        "--report-title",
        default="Benchmark Diagnostics",
        help="Markdown report title.",
    )
    args = parser.parse_args()
    if not args.predictions_csv and not args.predictions_json:
        parser.error("provide at least one --predictions-csv or --predictions-json")
    return args


def token_count(text: str) -> int:
    return len(text.split())


def char_count(text: str) -> int:
    return len(text.replace(" ", ""))


def script_ratio(pattern: re.Pattern[str], text: str) -> float:
    chars = [char for char in text if not char.isspace()]
    if not chars:
        return 0.0
    return len(pattern.findall(text)) / len(chars)


def has_repeated_token_loop(text: str, min_repeat: int = 8) -> bool:
    tokens = text.split()
    if not tokens:
        return False
    run_token = tokens[0]
    run_length = 1
    for token in tokens[1:]:
        if token == run_token:
            run_length += 1
            if run_length >= min_repeat:
                return True
        else:
            run_token = token
            run_length = 1
    return False


def repeated_char_ratio(text: str) -> float:
    compact = text.replace(" ", "")
    if not compact:
        return 0.0
    repeated = 0
    previous = ""
    for char in compact:
        if char == previous:
            repeated += 1
        previous = char
    return repeated / len(compact)


def has_repeated_ngram_loop(text: str, ngram_size: int = 2, min_count: int = 8) -> bool:
    tokens = text.split()
    if len(tokens) < ngram_size * min_count:
        return False
    ngrams = Counter(tuple(tokens[i : i + ngram_size]) for i in range(len(tokens) - ngram_size + 1))
    return any(count >= min_count for count in ngrams.values())


def to_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def diagnose_row(row: dict[str, str]) -> dict[str, object]:
    ref = row.get("reference_text", "")
    hyp = row.get("hypothesis_text", "")
    ref_tokens = token_count(ref)
    hyp_tokens = token_count(hyp)
    ref_chars = char_count(ref)
    hyp_chars = char_count(hyp)
    token_length_ratio = hyp_tokens / ref_tokens if ref_tokens else None
    char_length_ratio = hyp_chars / ref_chars if ref_chars else None
    hyp_devanagari_ratio = script_ratio(DEVANAGARI_RE, hyp)
    ref_devanagari_ratio = script_ratio(DEVANAGARI_RE, ref)
    hyp_latin_ratio = script_ratio(LATIN_RE, hyp)
    script_drift = ref_devanagari_ratio >= 0.5 and hyp_latin_ratio >= 0.25
    empty_or_near_empty = hyp_tokens <= 1 and ref_tokens >= 3
    length_explosion = (
        token_length_ratio is not None and token_length_ratio >= 2.5 and hyp_tokens >= 8
    )
    length_collapse = (
        token_length_ratio is not None and token_length_ratio <= 0.25 and ref_tokens >= 8
    )
    repeated_token_loop = has_repeated_token_loop(hyp)
    repeated_ngram_loop = has_repeated_ngram_loop(hyp)
    repeated_char_loop = repeated_char_ratio(hyp) >= 0.35 and hyp_chars >= 25
    hallucination_risk = any(
        [
            length_explosion,
            repeated_token_loop,
            repeated_ngram_loop,
            repeated_char_loop,
            script_drift,
        ]
    )
    transcript_risk = "<incomplete>" in ref.lower()
    return {
        **row,
        "wer": to_float(row.get("wer")),
        "cer": to_float(row.get("cer")),
        "num_beams": int(row.get("num_beams", 0) or 0),
        "ref_tokens": ref_tokens,
        "hyp_tokens": hyp_tokens,
        "ref_chars": ref_chars,
        "hyp_chars": hyp_chars,
        "token_length_ratio": token_length_ratio,
        "char_length_ratio": char_length_ratio,
        "hyp_devanagari_ratio": hyp_devanagari_ratio,
        "hyp_latin_ratio": hyp_latin_ratio,
        "empty_or_near_empty": empty_or_near_empty,
        "length_explosion": length_explosion,
        "length_collapse": length_collapse,
        "repeated_token_loop": repeated_token_loop,
        "repeated_ngram_loop": repeated_ngram_loop,
        "repeated_char_loop": repeated_char_loop,
        "script_drift": script_drift,
        "hallucination_risk": hallucination_risk,
        "transcript_risk": transcript_risk,
    }


def read_predictions(paths: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in paths:
        with Path(path).open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(diagnose_row(row))
    return rows


def read_json_predictions(paths: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in paths:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        samples = payload.get("samples")
        if not isinstance(samples, list):
            raise ValueError(f"Prediction JSON {path} has no samples list")
        for sample in samples:
            if not isinstance(sample, dict):
                raise ValueError(f"Prediction JSON {path} contains a non-object sample")
            rows.append(diagnose_row(sample))
    return rows


def rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        key = (
            row.get("model"),
            row.get("slice"),
            row.get("condition"),
            row.get("num_beams"),
        )
        groups[key].append(row)

    summaries = []
    for (model, slice_name, condition, num_beams), group in sorted(groups.items()):
        total = len(group)
        wer_values = [row["wer"] for row in group if isinstance(row.get("wer"), float)]
        cer_values = [row["cer"] for row in group if isinstance(row.get("cer"), float)]
        summaries.append(
            {
                "model": model,
                "slice": slice_name,
                "condition": condition,
                "num_beams": num_beams,
                "files": total,
                "macro_wer": sum(wer_values) / len(wer_values) if wer_values else None,
                "macro_cer": sum(cer_values) / len(cer_values) if cer_values else None,
                "hallucination_risk_rate": rate(
                    sum(bool(row["hallucination_risk"]) for row in group), total
                ),
                "repetition_rate": rate(
                    sum(
                        bool(row["repeated_token_loop"])
                        or bool(row["repeated_ngram_loop"])
                        or bool(row["repeated_char_loop"])
                        for row in group
                    ),
                    total,
                ),
                "length_explosion_rate": rate(
                    sum(bool(row["length_explosion"]) for row in group), total
                ),
                "length_collapse_rate": rate(
                    sum(bool(row["length_collapse"]) for row in group), total
                ),
                "script_drift_rate": rate(sum(bool(row["script_drift"]) for row in group), total),
                "empty_or_near_empty_rate": rate(
                    sum(bool(row["empty_or_near_empty"]) for row in group), total
                ),
                "transcript_risk_files": sum(bool(row["transcript_risk"]) for row in group),
            }
        )
    return summaries


def fmt(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(column)) for column in columns) + " |")
    return "\n".join(lines)


def top_risk_examples(rows: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    risky = [
        row
        for row in rows
        if row["hallucination_risk"] or row["empty_or_near_empty"] or row["length_collapse"]
    ]
    return sorted(
        risky,
        key=lambda row: (
            bool(row["hallucination_risk"]),
            float(row.get("cer") or 0.0),
            float(row.get("wer") or 0.0),
        ),
        reverse=True,
    )[:limit]


def short_text(text: object, max_chars: int = 90) -> str:
    value = str(text or "").replace("\n", " ")
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3] + "..."


def write_markdown(
    output_path: Path,
    summaries: list[dict[str, object]],
    rows: list[dict[str, object]],
    top_examples: int,
    report_title: str,
) -> None:
    summary_columns = [
        "model",
        "slice",
        "num_beams",
        "files",
        "macro_wer",
        "macro_cer",
        "hallucination_risk_rate",
        "repetition_rate",
        "length_explosion_rate",
        "script_drift_rate",
        "empty_or_near_empty_rate",
    ]
    examples = []
    for row in top_risk_examples(rows, top_examples):
        examples.append(
            {
                "model": row.get("model"),
                "slice": row.get("slice"),
                "num_beams": row.get("num_beams"),
                "wer": row.get("wer"),
                "cer": row.get("cer"),
                "flags": ", ".join(
                    flag
                    for flag in [
                        "hallucination" if row["hallucination_risk"] else "",
                        "repetition"
                        if row["repeated_token_loop"]
                        or row["repeated_ngram_loop"]
                        or row["repeated_char_loop"]
                        else "",
                        "length_explosion" if row["length_explosion"] else "",
                        "script_drift" if row["script_drift"] else "",
                        "empty" if row["empty_or_near_empty"] else "",
                        "collapse" if row["length_collapse"] else "",
                    ]
                    if flag
                ),
                "reference": short_text(row.get("reference_text")),
                "hypothesis": short_text(row.get("hypothesis_text")),
            }
        )
    example_columns = [
        "model",
        "slice",
        "num_beams",
        "wer",
        "cer",
        "flags",
        "reference",
        "hypothesis",
    ]
    output_path.write_text(
        "\n".join(
            [
                f"# {report_title}",
                "",
                "This report adds deployment-oriented diagnostics on top of WER/CER.",
                "",
                "Source data: per-sample prediction exports. These diagnostics are heuristics, not final human labels.",
                "",
                "## Summary By Model And Slice",
                "",
                markdown_table(summaries, summary_columns),
                "",
                "## High-Risk Examples",
                "",
                markdown_table(examples, example_columns),
                "",
                "## Flag Definitions",
                "",
                "- `hallucination_risk_rate`: share of files with length explosion, repetition, repeated characters, or script drift.",
                "- `repetition_rate`: share of files with repeated token, n-gram, or character-loop patterns.",
                "- `length_explosion_rate`: hypothesis has at least 2.5x as many tokens as reference and at least 8 tokens.",
                "- `script_drift_rate`: mostly Devanagari reference but substantial Latin-script hypothesis.",
                "- `empty_or_near_empty_rate`: hypothesis has 0-1 tokens while reference has at least 3 tokens.",
                "",
                "Interpretation: these flags are meant to catch ASR behavior that can matter in voice-agent or call-analytics settings even when WER/CER already look bad.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    rows = read_predictions(args.predictions_csv)
    rows.extend(read_json_predictions(args.predictions_json))
    summaries = summarize(rows)
    payload = {"summary": summaries, "samples": rows}
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(output_md, summaries, rows, args.top_examples, args.report_title)
    print(f"Wrote {output_json}")
    print(f"Wrote {output_md}")


if __name__ == "__main__":
    main()
