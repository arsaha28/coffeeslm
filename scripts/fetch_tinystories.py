"""Download TinyStories V2 (first 500 MB of train + full valid) to data/raw/tinystories/."""

from pathlib import Path

from coffee_slm.data.download import download
from coffee_slm.data.trim import trim_to_last_separator
from coffee_slm.logging_setup import setup_logging

BASE_URL = "https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main"
OUT_DIR = Path("data/raw/tinystories")
TRAIN_MAX_BYTES = 500 * 1024 * 1024


def main() -> None:
    setup_logging(log_file=Path("logs/fetch_tinystories.log"))
    train = OUT_DIR / "train.txt"
    download(f"{BASE_URL}/TinyStoriesV2-GPT4-train.txt", train, max_bytes=TRAIN_MAX_BYTES)
    trim_to_last_separator(train)
    download(f"{BASE_URL}/TinyStoriesV2-GPT4-valid.txt", OUT_DIR / "valid.txt")


if __name__ == "__main__":
    main()
