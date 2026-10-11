"""Trim a text file so it ends on a complete document."""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

END_OF_TEXT = b"<|endoftext|>"
TAIL_BYTES = 1024 * 1024  # search only the last 1 MB; one story is far shorter


def trim_to_last_separator(path: Path, separator: bytes = END_OF_TEXT) -> int:
    """Cut the file right after its last separator, dropping a partial document."""
    size = path.stat().st_size
    tail_start = max(0, size - TAIL_BYTES)
    with path.open("rb") as f:
        f.seek(tail_start)
        cut = f.read().rfind(separator)
    if cut == -1:
        raise ValueError(f"No separator in the last {TAIL_BYTES} bytes of {path}")
    new_size = tail_start + cut + len(separator)
    os.truncate(path, new_size)
    logger.info("Trimmed %s: removed %d bytes of partial text", path, size - new_size)
    return new_size
