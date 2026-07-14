from pathlib import Path

import pytest

from callwhisper.datasets.gramvaani_inventory import (
    frozen_ids_from_manifests,
    read_keyed_text,
    transcript_flags,
)


def test_read_keyed_text(tmp_path: Path) -> None:
    source = tmp_path / "text"
    source.write_text("clip-a first transcript\nclip-b second transcript\n", encoding="utf-8")

    assert read_keyed_text(source) == {
        "clip-a": "first transcript",
        "clip-b": "second transcript",
    }


def test_read_keyed_text_rejects_duplicate_ids(tmp_path: Path) -> None:
    source = tmp_path / "text"
    source.write_text("clip-a one\nclip-a two\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate ID"):
        read_keyed_text(source)


def test_frozen_ids_and_transcript_flags(tmp_path: Path) -> None:
    manifest = tmp_path / "frozen.csv"
    manifest.write_text(
        "audio_path,reference_text\ndatasets/Audio/clip-a.mp3,hello\n", encoding="utf-8"
    )

    assert frozen_ids_from_manifests([manifest]) == {"clip-a"}
    assert transcript_flags("one <inaudible> two <incomplete>") == "<inaudible>;<incomplete>"
