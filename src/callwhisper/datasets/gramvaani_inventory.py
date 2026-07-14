"""Build a leakage-safe audio inventory from a labelled GramVaani release."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import mean, median
from typing import Any

from tqdm.auto import tqdm


def read_keyed_text(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Malformed row in {path} at line {line_number}")
        key, value = parts
        if key in rows:
            raise ValueError(f"Duplicate ID {key!r} in {path}")
        rows[key] = value.strip()
    return rows


def frozen_ids_from_manifests(paths: list[Path]) -> set[str]:
    frozen: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                frozen.add(Path(row["audio_path"]).stem)
    return frozen


def probe_audio(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=sample_rate,channels:format=duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    if not streams:
        raise ValueError("no audio stream")
    stream = streams[0]
    return {
        "duration_s": round(float(payload["format"]["duration"]), 3),
        "sample_rate_hz": int(stream["sample_rate"]),
        "channels": int(stream["channels"]),
    }


def transcript_flags(text: str) -> str:
    markers = [marker for marker in ("<inaudible>", "<incomplete>") if marker in text.lower()]
    return ";".join(markers)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)


def build_inventory(
    dataset_dir: Path,
    frozen_ids: set[str],
    min_duration_s: float,
    max_duration_s: float,
    workers: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    text_path = dataset_dir / "text"
    scp_candidates = [dataset_dir / "mp3.scp", dataset_dir / "wav.scp"]
    scp_path = next((path for path in scp_candidates if path.exists()), None)
    if not text_path.exists() or scp_path is None:
        raise FileNotFoundError(f"Expected text and mp3.scp or wav.scp under {dataset_dir}")

    transcripts = read_keyed_text(text_path)
    audio_index = read_keyed_text(scp_path)
    rejected: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []

    for utterance_id in sorted(set(transcripts) | set(audio_index)):
        text = transcripts.get(utterance_id, "").strip()
        relative_audio = audio_index.get(utterance_id)
        base = {
            "utterance_id": utterance_id,
            "audio_path": "" if relative_audio is None else relative_audio.removeprefix("./"),
            "reference_text": text,
        }
        if utterance_id in frozen_ids:
            rejected.append({**base, "reason": "frozen_benchmark_id", "detail": ""})
        elif not text:
            rejected.append({**base, "reason": "missing_transcript", "detail": ""})
        elif relative_audio is None:
            rejected.append({**base, "reason": "missing_audio_index", "detail": ""})
        else:
            audio_path = (dataset_dir / relative_audio).resolve()
            if not audio_path.exists():
                rejected.append({**base, "reason": "missing_audio_file", "detail": ""})
            else:
                candidates.append({**base, "_resolved_audio_path": str(audio_path)})

    probed: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(probe_audio, Path(row["_resolved_audio_path"])): row
            for row in candidates
        }
        progress = tqdm(total=len(futures), desc="Probing GramVaani audio")
        for future in as_completed(futures):
            row = futures[future]
            try:
                probed[row["utterance_id"]] = future.result()
            except Exception as exc:
                rejected.append(
                    {
                        **row,
                        "reason": "audio_probe_failed",
                        "detail": f"{type(exc).__name__}: {exc}",
                    }
                )
            progress.update(1)
        progress.close()

    accepted: list[dict[str, Any]] = []
    for row in candidates:
        metadata = probed.get(row["utterance_id"])
        if metadata is None:
            continue
        duration_s = metadata["duration_s"]
        if duration_s < min_duration_s:
            rejected.append({**row, **metadata, "reason": "duration_too_short", "detail": ""})
        elif duration_s > max_duration_s:
            rejected.append({**row, **metadata, "reason": "duration_too_long", "detail": ""})
        else:
            accepted.append(
                {
                    **row,
                    **metadata,
                    "source_rate_group": "native_8khz"
                    if metadata["sample_rate_hz"] == 8000
                    else "higher_rate",
                    "transcript_flags": transcript_flags(row["reference_text"]),
                }
            )
    return accepted, sorted(rejected, key=lambda row: row["utterance_id"])


def summarize(
    accepted: list[dict[str, Any]], rejected: list[dict[str, Any]], frozen_count: int
) -> dict[str, Any]:
    durations = [float(row["duration_s"]) for row in accepted]
    return {
        "accepted_files": len(accepted),
        "accepted_hours": round(sum(durations) / 3600, 3),
        "frozen_ids_loaded": frozen_count,
        "source_rate_counts": dict(
            sorted(Counter(row["source_rate_group"] for row in accepted).items())
        ),
        "sample_rate_counts": dict(
            sorted(Counter(str(row["sample_rate_hz"]) for row in accepted).items())
        ),
        "transcript_flag_counts": dict(
            sorted(Counter(row["transcript_flags"] or "none" for row in accepted).items())
        ),
        "rejection_counts": dict(sorted(Counter(row["reason"] for row in rejected).items())),
        "duration_s": {
            "min": min(durations) if durations else None,
            "median": median(durations) if durations else None,
            "mean": mean(durations) if durations else None,
            "max": max(durations) if durations else None,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", required=True)
    parser.add_argument("--frozen-manifest", action="append", default=[])
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--min-duration-s", type=float, default=1.0)
    parser.add_argument("--max-duration-s", type=float, default=30.0)
    parser.add_argument("--workers", type=int, default=8)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    dataset_dir = Path(args.dataset_dir).resolve()
    output_dir = Path(args.output_dir)
    frozen_paths = [Path(path) for path in args.frozen_manifest]
    frozen_ids = frozen_ids_from_manifests(frozen_paths)
    accepted, rejected = build_inventory(
        dataset_dir,
        frozen_ids,
        args.min_duration_s,
        args.max_duration_s,
        args.workers,
    )

    inventory_fields = [
        "utterance_id",
        "audio_path",
        "reference_text",
        "duration_s",
        "sample_rate_hz",
        "channels",
        "source_rate_group",
        "transcript_flags",
    ]
    rejected_fields = [
        "utterance_id",
        "audio_path",
        "reference_text",
        "duration_s",
        "sample_rate_hz",
        "channels",
        "reason",
        "detail",
    ]
    write_csv(output_dir / "gv_train_100h_inventory.csv", accepted, inventory_fields)
    write_csv(output_dir / "gv_train_100h_rejected.csv", rejected, rejected_fields)
    summary = summarize(accepted, rejected, len(frozen_ids))
    summary_path = output_dir / "gv_train_100h_inventory_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote inventory artifacts to {output_dir}")


if __name__ == "__main__":
    main()
