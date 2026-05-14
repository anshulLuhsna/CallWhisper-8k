from __future__ import annotations

import re
import unicodedata


_ASCII_PUNCTUATION = re.compile(r"[!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]")
_WHITESPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Conservative ASR normalization that avoids destructive Devanagari rewrites."""
    normalized = unicodedata.normalize("NFC", text).strip()
    normalized = normalized.lower()
    normalized = _ASCII_PUNCTUATION.sub(" ", normalized)
    normalized = _WHITESPACE.sub(" ", normalized)
    return normalized.strip()
