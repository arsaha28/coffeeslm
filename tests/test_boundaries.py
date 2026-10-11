import pytest

from coffee_slm.data.boundaries import (
    drop_leading_fragment,
    ensure_trailing_separator,
    fix_boundaries,
)

SEP = "<|endoftext|>"


def test_drop_leading_fragment_removes_separator_too():
    text = f"agment end.\n{SEP}\nStory two.\n{SEP}\nStory three."
    assert drop_leading_fragment(text) == f"Story two.\n{SEP}\nStory three."


def test_drop_leading_fragment_needs_a_separator():
    with pytest.raises(ValueError):
        drop_leading_fragment("no separator here")


def test_ensure_trailing_separator_adds_once():
    assert ensure_trailing_separator("Story.\n") == f"Story.\n{SEP}"
    assert ensure_trailing_separator(f"Story.\n{SEP}") == f"Story.\n{SEP}"


def test_fix_boundaries_on_file(tmp_path):
    path = tmp_path / "valid.txt"
    path.write_text(f"ment.\n{SEP}\nStory two.\n{SEP}\nStory three.")
    fix_boundaries(path)
    assert path.read_text() == f"Story two.\n{SEP}\nStory three.\n{SEP}"
