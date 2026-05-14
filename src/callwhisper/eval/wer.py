from __future__ import annotations

from jiwer import wer as jiwer_wer

from .normalizer import normalize_text


def word_error_rate(reference: str, hypothesis: str) -> float:
    return float(jiwer_wer(normalize_text(reference), normalize_text(hypothesis)))
