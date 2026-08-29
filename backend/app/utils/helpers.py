"""
===========================================================
QuantFormer Backend — Helper Utilities
===========================================================

System probes, time formatting, and mathematical helpers
used across multiple backend modules.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional

import psutil
import torch


# ===========================================================
# Application Startup Timestamp
# ===========================================================

_startup_time: Optional[float] = None


def mark_startup() -> None:
    """Record the application startup timestamp."""
    global _startup_time
    _startup_time = time.time()


def get_uptime_seconds() -> float:
    """Return seconds elapsed since application startup."""
    if _startup_time is None:
        return 0.0
    return round(time.time() - _startup_time, 2)


def get_uptime_human() -> str:
    """Return human-readable uptime string (e.g. '2h 15m 30s')."""
    seconds = int(get_uptime_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


# ===========================================================
# Timestamp Helpers
# ===========================================================

def utc_now_iso() -> str:
    """Return current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def local_now_iso() -> str:
    """Return current local time as an ISO 8601 string."""
    return datetime.now().isoformat()


# ===========================================================
# System Information Probes
# ===========================================================

def get_gpu_info() -> Dict[str, Any]:
    """
    Return GPU status and memory information.

    Returns a dict with:
      available : bool
      device_name : str or None
      memory_allocated_mb : float or None
      memory_total_mb : float or None
      cuda_version : str or None
    """
    if not torch.cuda.is_available():
        return {
            "available": False,
            "device_name": None,
            "memory_allocated_mb": None,
            "memory_total_mb": None,
            "cuda_version": None,
        }

    return {
        "available": True,
        "device_name": torch.cuda.get_device_name(0),
        "memory_allocated_mb": round(
            torch.cuda.memory_allocated(0) / (1024 ** 2), 2
        ),
        "memory_total_mb": round(
            torch.cuda.get_device_properties(0).total_mem / (1024 ** 2), 2
        ),
        "cuda_version": torch.version.cuda,
    }


def get_system_info() -> Dict[str, Any]:
    """
    Return CPU and RAM usage information.

    Returns a dict with:
      cpu_usage_percent : float
      ram_total_mb : float
      ram_used_mb : float
      ram_usage_percent : float
    """
    memory = psutil.virtual_memory()

    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
        "ram_total_mb": round(memory.total / (1024 ** 2), 2),
        "ram_used_mb": round(memory.used / (1024 ** 2), 2),
        "ram_usage_percent": memory.percent,
    }


def get_device() -> torch.device:
    """Return the best available torch device (CUDA or CPU)."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ===========================================================
# Math / Inference Helpers
# ===========================================================

def softmax_to_percentages(probabilities: list) -> list:
    """
    Convert a list of softmax probabilities to percentages
    rounded to 2 decimal places.
    """
    return [round(p * 100, 2) for p in probabilities]


class LatencyTimer:
    """
    Context manager to measure elapsed wall-clock time in
    milliseconds for inference latency tracking.

    Usage:
        with LatencyTimer() as timer:
            result = model(input)
        print(f"Inference took {timer.elapsed_ms} ms")
    """

    def __init__(self):
        self._start: float = 0.0
        self._end: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self._end = time.perf_counter()

    @property
    def elapsed_ms(self) -> float:
        """Elapsed time in milliseconds, rounded to 2 decimal places."""
        return round((self._end - self._start) * 1000, 2)
