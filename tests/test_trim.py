import pytest

from coffee_slm.data.trim import trim_to_last_separator

SEP = "<|endoftext|>"


def _write(tmp_path, text: str):
    path = tmp_path / "stories.txt"
    path.write_text(text)
    return path


def test_drops_partial_last_story(tmp_path):
    path = _write(tmp_path, f"Story one.{SEP}Story two.{SEP}Story thr")
    trim_to_last_separator(path)
    assert path.read_text() == f"Story one.{SEP}Story two.{SEP}"


def test_keeps_file_that_already_ends_cleanly(tmp_path):
    text = f"Story one.{SEP}"
    path = _write(tmp_path, text)
    assert trim_to_last_separator(path) == len(text)
    assert path.read_text() == text


def test_raises_when_no_separator(tmp_path):
    path = _write(tmp_path, "just a partial story")
    with pytest.raises(ValueError):
        trim_to_last_separator(path)
