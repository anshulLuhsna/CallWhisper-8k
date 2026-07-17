"""Build deterministic paired telephone-channel audio for ASR evaluation."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import wave
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


CONDITIONS = (
    "original",
    "bandlimit_8k",
    "bandlimit_8k_g711_alaw",
    "bandlimit_8k_g711_mulaw",
    "bandlimit_8k_gsm_fr",
)
REQUIRED_ENCODERS = {
    "bandlimit_8k_g711_alaw": "pcm_alaw",
    "bandlimit_8k_g711_mulaw": "pcm_mulaw",
    "bandlimit_8k_gsm_fr": "libgsm",
}
TELEPHONE_FILTER = "highpass=f=300,lowpass=f=3400"


def stable_key(*parts: object) -> str:
    payload = "\x1f".join(str(part) for part in parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sample_key(dataset_id: str, source_id: str) -> str:
    return stable_key(dataset_id, source_id)[:20]


def normalize_group(value: object) -> str:
    text = str(value or "").strip()
    return "unknown" if text.lower() in {"", "na", "n/a", "none", "null", "unknown"} else text


def deterministic_stratified_sample(
    rows: Iterable[dict[str, Any]],
    limit: int,
    seed: int,
    *,
    speaker_column: str = "speaker_id",
    stratum_columns: tuple[str, ...] = ("gender", "state"),
) -> list[dict[str, Any]]:
    """Round-robin strata while selecting at most one row per speaker."""
    if limit <= 0:
        raise ValueError("limit must be positive")

    best_by_speaker: dict[str, tuple[str, dict[str, Any]]] = {}
    for row in rows:
        speaker = normalize_group(row.get(speaker_column))
        if speaker == "unknown":
            speaker = f"unknown:{row.get('source_id', stable_key(json.dumps(row, sort_keys=True)))}"
        rank = stable_key(seed, speaker, row.get("source_id", ""))
        current = best_by_speaker.get(speaker)
        if current is None or rank < current[0]:
            best_by_speaker[speaker] = (rank, row)

    if len(best_by_speaker) < limit:
        raise ValueError(
            f"Requested {limit} rows but only {len(best_by_speaker)} unique speakers are available"
        )

    strata: dict[tuple[str, ...], list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for rank, row in best_by_speaker.values():
        stratum = tuple(normalize_group(row.get(column)) for column in stratum_columns)
        strata[stratum].append((rank, row))

    queues = {
        stratum: deque(row for _, row in sorted(items, key=lambda item: item[0]))
        for stratum, items in strata.items()
    }
    stratum_order = sorted(queues, key=lambda value: stable_key(seed, *value))
    selected: list[dict[str, Any]] = []
    while len(selected) < limit:
        made_progress = False
        for stratum in stratum_order:
            if queues[stratum] and len(selected) < limit:
                selected.append(queues[stratum].popleft())
                made_progress = True
        if not made_progress:
            break

    return selected


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ffmpeg_version() -> str:
    result = subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
    return result.stdout.splitlines()[0]


def available_audio_encoders() -> set[str]:
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("ffmpeg is required to build paired telephony audio") from exc
    encoders: set[str] = set()
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) >= 2 and fields[0].startswith("A"):
            encoders.add(fields[1])
    return encoders


def validate_codec_support(conditions: Iterable[str] = CONDITIONS) -> dict[str, bool]:
    requested = tuple(conditions)
    unknown = set(requested) - set(CONDITIONS)
    if unknown:
        raise ValueError(f"Unknown conditions: {sorted(unknown)}")
    encoders = available_audio_encoders()
    support = {
        condition: encoder in encoders
        for condition, encoder in REQUIRED_ENCODERS.items()
        if condition in requested
    }
    missing = [condition for condition, available in support.items() if not available]
    if missing:
        details = ", ".join(f"{name} ({REQUIRED_ENCODERS[name]})" for name in missing)
        raise RuntimeError(f"This ffmpeg build lacks required encoders: {details}")
    return support


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
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("ffprobe is required to validate paired telephony audio") from exc
    payload = json.loads(result.stdout)
    streams = payload.get("streams", [])
    if not streams:
        raise ValueError(f"No audio stream found in {path}")
    return {
        "sample_rate_hz": int(streams[0]["sample_rate"]),
        "channels": int(streams[0]["channels"]),
        "duration_s": float(payload["format"]["duration"]),
    }


def _run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Missing executable: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Command failed ({exc.returncode}): {' '.join(command)}\n{exc.stderr.strip()}"
        ) from exc


def _decode_to_whisper_wav(input_path: Path, output_path: Path, filters: str | None = None) -> None:
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(input_path),
        "-vn",
    ]
    if filters:
        command.extend(["-af", filters])
    command.extend(["-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(output_path)])
    _run(command)


def _pcm_frame_count(path: Path) -> int:
    with wave.open(str(path), "rb") as handle:
        if handle.getframerate() != 16000 or handle.getnchannels() != 1:
            raise ValueError(f"Expected mono 16 kHz PCM WAV: {path}")
        return handle.getnframes()


def _conform_whisper_wav_duration(
    input_path: Path, output_path: Path, expected_frames: int
) -> None:
    if expected_frames <= 0:
        raise ValueError("expected_frames must be positive")
    _decode_to_whisper_wav(
        input_path,
        output_path,
        f"apad,atrim=end_sample={expected_frames}",
    )


def transform_audio(source_path: Path, output_path: Path, condition: str) -> dict[str, Any]:
    """Apply one predeclared channel and return portable validation metadata."""
    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}")
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    source_container_probe = probe_audio(source_path)
    with tempfile.TemporaryDirectory(dir=output_path.parent) as temporary_dir:
        temporary = Path(temporary_dir)
        decoded_source = temporary / "decoded_source.wav"
        staged_output = temporary / "output.wav"
        _decode_to_whisper_wav(source_path, decoded_source)
        expected_frames = _pcm_frame_count(decoded_source)
        source_duration_s = expected_frames / 16000
        if condition == "original":
            staged_output = decoded_source
        elif condition == "bandlimit_8k":
            _decode_to_whisper_wav(
                decoded_source,
                staged_output,
                f"{TELEPHONE_FILTER},aresample=8000,aresample=16000",
            )
        elif condition in {"bandlimit_8k_g711_alaw", "bandlimit_8k_g711_mulaw"}:
            codec = REQUIRED_ENCODERS[condition]
            encoded = temporary / "encoded.wav"
            _run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-i",
                    str(decoded_source),
                    "-vn",
                    "-af",
                    TELEPHONE_FILTER,
                    "-ac",
                    "1",
                    "-ar",
                    "8000",
                    "-c:a",
                    codec,
                    str(encoded),
                ]
            )
            _decode_to_whisper_wav(encoded, staged_output)
        else:
            encoded = temporary / "encoded.gsm"
            _run(
                [
                    "ffmpeg",
                    "-y",
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-i",
                    str(decoded_source),
                    "-vn",
                    "-af",
                    TELEPHONE_FILTER,
                    "-ac",
                    "1",
                    "-ar",
                    "8000",
                    "-c:a",
                    "libgsm",
                    "-f",
                    "gsm",
                    str(encoded),
                ]
            )
            _decode_to_whisper_wav(encoded, staged_output)

        raw_output_probe = probe_audio(staged_output)
        raw_output_frames = _pcm_frame_count(staged_output)
        preconform_duration_delta = abs(raw_output_frames - expected_frames) / 16000
        hard_tolerance = max(0.5, source_duration_s * 0.05)
        if (
            raw_output_probe["sample_rate_hz"] != 16000
            or raw_output_probe["channels"] != 1
        ):
            raise ValueError(f"Invalid output format for {condition}: {raw_output_probe}")
        if preconform_duration_delta > hard_tolerance:
            raise ValueError(
                f"Duration changed by {preconform_duration_delta:.3f}s for {condition}; "
                f"hard tolerance={hard_tolerance:.3f}s"
            )
        duration_conformed = raw_output_frames != expected_frames
        if duration_conformed:
            conformed_output = temporary / "conformed_output.wav"
            _conform_whisper_wav_duration(
                staged_output, conformed_output, expected_frames
            )
            staged_output = conformed_output

        output_probe = probe_audio(staged_output)
        output_frames = _pcm_frame_count(staged_output)
        duration_delta = abs(output_frames - expected_frames) / 16000
        if output_frames != expected_frames:
            raise ValueError(
                f"Duration conformance failed by {abs(output_frames - expected_frames)} "
                f"PCM frames for {condition}"
            )
        shutil.move(staged_output, output_path)

    return {
        "condition": condition,
        "audio_path": str(output_path),
        "source_sha256": sha256_file(source_path),
        "output_sha256": sha256_file(output_path),
        "source_duration_s": source_duration_s,
        "source_container_duration_s": source_container_probe["duration_s"],
        "duration_s": output_frames / 16000,
        "duration_delta_s": duration_delta,
        "preconform_duration_delta_s": preconform_duration_delta,
        "duration_conformed": duration_conformed,
        "sample_rate_hz": output_probe["sample_rate_hz"],
        "channels": output_probe["channels"],
    }
