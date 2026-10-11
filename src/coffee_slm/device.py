"""Choose the hardware device for running PyTorch."""

import logging

import torch

logger = logging.getLogger(__name__)


def get_device() -> torch.device:
    """Return the Apple GPU (mps) if available, otherwise the CPU."""
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    logger.info("Using device: %s", device)
    return device
