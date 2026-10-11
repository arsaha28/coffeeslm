"""Download a file from a URL in chunks, optionally stopping at a size limit."""

import logging
import time
import urllib.request
from pathlib import Path

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024  # read 1 MB at a time
LOG_EVERY = 50 * 1024 * 1024  # log progress every 50 MB


def _next_read_size(written: int, max_bytes: int | None) -> int:
    """Bytes to read next so we never go past max_bytes."""
    if max_bytes is None:
        return CHUNK_SIZE
    return min(CHUNK_SIZE, max_bytes - written)


def download(url: str, dest: Path, max_bytes: int | None = None) -> int:
    """Stream url into dest, stopping after max_bytes if given. Return bytes written."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    start, written = time.perf_counter(), 0
    with urllib.request.urlopen(url) as response, dest.open("wb") as out:
        while chunk := response.read(_next_read_size(written, max_bytes)):
            out.write(chunk)
            written += len(chunk)
            if written // LOG_EVERY > (written - len(chunk)) // LOG_EVERY:
                logger.info("... %d MB downloaded", written // 1024**2)
    seconds = time.perf_counter() - start
    logger.info("Downloaded %s -> %s (%.1f MB in %.1fs)", url, dest, written / 1024**2, seconds)
    return written
