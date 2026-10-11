import torch

from coffee_slm.device import get_device


def test_returns_usable_device():
    device = get_device()
    assert device.type in ("mps", "cpu")
    assert torch.ones(1, device=device).item() == 1.0


def test_falls_back_to_cpu_without_mps(monkeypatch):
    monkeypatch.setattr(torch.backends.mps, "is_available", lambda: False)
    assert get_device().type == "cpu"
