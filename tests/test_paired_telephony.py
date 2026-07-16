from __future__ import annotations

import math
import subprocess
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from callwhisper.datasets.paired_telephony import (
    CONDITIONS,
    available_audio_encoders,
    deterministic_stratified_sample,
    probe_audio,
    sample_key,
    sha256_file,
    transform_audio,
)


def test_deterministic_stratified_sample_is_stable_and_speaker_unique() -> None:
    rows = [
        {
            "source_id": f"row-{index}",
            "speaker_id": f"speaker-{index // 2}",
            "gender": "Female" if index % 4 < 2 else "Male",
            "state": "A" if index % 3 else "B",
        }
        for index in range(24)
    ]

    first = deterministic_stratified_sample(rows, 8, seed=17)
    second = deterministic_stratified_sample(reversed(rows), 8, seed=17)

    assert [row["source_id"] for row in first] == [row["source_id"] for row in second]
    assert len({row["speaker_id"] for row in first}) == 8
    assert {row["gender"] for row in first} == {"Female", "Male"}


def test_deterministic_stratified_sample_rejects_too_many_speakers() -> None:
    rows = [{"source_id": "a", "speaker_id": "one", "gender": "unknown", "state": "x"}]
    with pytest.raises(ValueError, match="unique speakers"):
        deterministic_stratified_sample(rows, 2, seed=0)


def test_hash_helpers(tmp_path: Path) -> None:
    payload = tmp_path / "payload.bin"
    payload.write_bytes(b"callwhisper")

    assert sample_key("dataset", "row") == sample_key("dataset", "row")
    assert len(sample_key("dataset", "row")) == 20
    assert (
        sha256_file(payload) == "57d4c59b042a2550927b8c6537286143266c2ba534d4efe7db3b541e7a34ceed"
    )


def _write_sine(path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=1000:duration=0.25",
            "-ac",
            "1",
            "-ar",
            "16000",
            str(path),
        ],
        check=True,
    )


def _write_two_tones(path: Path) -> None:
    sample_rate = 16000
    time = np.arange(sample_rate, dtype=np.float64) / sample_rate
    audio = 0.35 * np.sin(2 * np.pi * 100 * time) + 0.35 * np.sin(2 * np.pi * 1000 * time)
    sf.write(path, audio, sample_rate)


def _tone_amplitude(path: Path, frequency_hz: int) -> float:
    audio, sample_rate = sf.read(path)
    spectrum = np.abs(np.fft.rfft(audio))
    frequencies = np.fft.rfftfreq(len(audio), d=1 / sample_rate)
    return float(spectrum[np.argmin(np.abs(frequencies - frequency_hz))])


@pytest.mark.parametrize("condition", CONDITIONS[:4])
def test_transform_audio_produces_valid_whisper_wav(tmp_path: Path, condition: str) -> None:
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode:
        pytest.skip("ffmpeg is unavailable")
    source = tmp_path / "source.wav"
    output = tmp_path / f"{condition}.wav"
    _write_sine(source)

    metadata = transform_audio(source, output, condition)
    probed = probe_audio(output)

    assert metadata["condition"] == condition
    assert probed["sample_rate_hz"] == 16000
    assert probed["channels"] == 1
    assert math.isclose(probed["duration_s"], 0.25, abs_tol=0.05)


def test_gsm_transform_when_encoder_is_available(tmp_path: Path) -> None:
    if "libgsm" not in available_audio_encoders():
        pytest.skip("local ffmpeg lacks libgsm")
    source = tmp_path / "source.wav"
    output = tmp_path / "bandlimit_8k_gsm_fr.wav"
    _write_sine(source)

    transform_audio(source, output, "bandlimit_8k_gsm_fr")

    assert probe_audio(output)["sample_rate_hz"] == 16000


def test_codec_stack_applies_telephone_highpass(tmp_path: Path) -> None:
    source = tmp_path / "two-tones.wav"
    output = tmp_path / "stacked-alaw.wav"
    _write_two_tones(source)

    transform_audio(source, output, "bandlimit_8k_g711_alaw")

    low_to_voice_ratio = _tone_amplitude(output, 100) / _tone_amplitude(output, 1000)
    assert low_to_voice_ratio < 0.2
