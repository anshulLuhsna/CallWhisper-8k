from __future__ import annotations

from jiwer import cer as jiwer_cer

from .normalizer import normalize_text


def character_error_rate(reference: str, hypothesis: str) -> float:
    return float(jiwer_cer(normalize_text(reference), normalize_text(hypothesis)))
