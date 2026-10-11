"""Choose the hardware device for running PyTorch."""

import torch


def get_device() -> torch.device:
    """Return the Apple GPU (mps) if available, otherwise the CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")
