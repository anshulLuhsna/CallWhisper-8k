"""Alignment-based multi-reference WER for Vaani Benchmark V1.0."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable, Sequence

from jiwer import process_words


_BRACKETED_CONTENT = re.compile(r"\([^)]*\)|\[[^]]*\]|\{[^}]*\}|<[^>]*>")
_WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class MultiReferenceScore:
    substitutions: int
    insertions: int
    deletions: int
    reference_words: int
    hypothesis_words: int

    @property
    def errors(self) -> int:
        return self.substitutions + self.insertions + self.deletions

    @property
    def wer(self) -> float:
        if self.reference_words <= 0:
            raise ValueError("Multi-reference WER requires a positive effective reference length")
        return self.errors / self.reference_words

    def __add__(self, other: MultiReferenceScore) -> MultiReferenceScore:
        return MultiReferenceScore(
            substitutions=self.substitutions + other.substitutions,
            insertions=self.insertions + other.insertions,
            deletions=self.deletions + other.deletions,
            reference_words=self.reference_words + other.reference_words,
            hypothesis_words=self.hypothesis_words + other.hypothesis_words,
        )


def normalize_vaani_text(text: str) -> str:
    """Apply the benchmark card's annotation and punctuation normalization."""
    normalized = unicodedata.normalize("NFC", str(text)).lower()
    normalized = _BRACKETED_CONTENT.sub(" ", normalized)
    normalized = "".join(" " if unicodedata.category(char).startswith("P") else char for char in normalized)
    return _WHITESPACE.sub(" ", normalized).strip()


def alignment_multireference_score(
    references: Sequence[str], hypothesis: str
) -> MultiReferenceScore:
    """Score one utterance using Vaani's alignment-based multi-reference protocol.

    A hypothesis token is correct when any reference alignment marks it correct.
    Otherwise substitution takes priority over insertion. A deleted reference word
    counts only when it is deleted in every reference alignment.
    """
    if not references:
        raise ValueError("At least one reference is required")

    normalized_references = [normalize_vaani_text(reference) for reference in references]
    normalized_hypothesis = normalize_vaani_text(hypothesis)
    hypothesis_words = normalized_hypothesis.split()
    token_marks = [set() for _ in hypothesis_words]
    deleted_words_per_reference: list[set[str]] = []

    for reference in normalized_references:
        output = process_words(reference, normalized_hypothesis)
        reference_words = output.references[0]
        deleted_words: set[str] = set()
        for chunk in output.alignments[0]:
            if chunk.type in {"equal", "substitute", "insert"}:
                mark = {
                    "equal": "correct",
                    "substitute": "substitute",
                    "insert": "insert",
                }[chunk.type]
                for index in range(chunk.hyp_start_idx, chunk.hyp_end_idx):
                    token_marks[index].add(mark)
            elif chunk.type == "delete":
                deleted_words.update(reference_words[chunk.ref_start_idx : chunk.ref_end_idx])
            else:
                raise ValueError(f"Unsupported jiwer alignment type: {chunk.type}")
        deleted_words_per_reference.append(deleted_words)

    substitutions = 0
    insertions = 0
    for marks in token_marks:
        if "correct" in marks:
            continue
        if "substitute" in marks:
            substitutions += 1
        elif "insert" in marks:
            insertions += 1
        else:
            raise ValueError("Hypothesis token was not covered by any reference alignment")

    common_deletions = set.intersection(*deleted_words_per_reference)
    deletions = len(common_deletions)
    effective_reference_words = len(hypothesis_words) + deletions - insertions
    score = MultiReferenceScore(
        substitutions=substitutions,
        insertions=insertions,
        deletions=deletions,
        reference_words=effective_reference_words,
        hypothesis_words=len(hypothesis_words),
    )
    if score.reference_words <= 0:
        raise ValueError("Multi-reference WER produced a non-positive effective reference length")
    return score


def alignment_multireference_corpus_score(
    rows: Iterable[tuple[Sequence[str], str]],
) -> MultiReferenceScore:
    """Aggregate utterance counts before computing corpus WER."""
    total = MultiReferenceScore(0, 0, 0, 0, 0)
    seen = 0
    for references, hypothesis in rows:
        total += alignment_multireference_score(references, hypothesis)
        seen += 1
    if not seen:
        raise ValueError("Cannot score an empty corpus")
    return total
