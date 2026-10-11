"""Make every document in a text file complete and separator-terminated."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

END_OF_TEXT = "<|endoftext|>"


def drop_leading_fragment(text: str, separator: str = END_OF_TEXT) -> str:
    """Remove everything up to and including the first separator."""
    _, found, rest = text.partition(separator)
    if not found:
        raise ValueError("No separator found; cannot locate the first full document")
    return rest.lstrip("\n")


def ensure_trailing_separator(text: str, separator: str = END_OF_TEXT) -> str:
    """Append the separator on its own line if the text does not end with it."""
    body = text.rstrip("\n")
    return body if body.endswith(separator) else f"{body}\n{separator}"


def fix_boundaries(path: Path) -> None:
    """Drop the partial first document and terminate the last one, in place."""
    text = path.read_text(encoding="utf-8")
    fixed = ensure_trailing_separator(drop_leading_fragment(text))
    path.write_text(fixed, encoding="utf-8")
    logger.info("Fixed boundaries of %s: %d -> %d chars", path, len(text), len(fixed))
