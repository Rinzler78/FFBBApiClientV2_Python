"""Shared utilities for scripts."""

from __future__ import annotations

from typing import Any


def flatten_keys(obj: Any, prefix: str = "") -> set[str]:
    """Recursively flatten JSON keys into dot-separated paths.

    Args:
        obj: JSON-like object (dict, list, or scalar)
        prefix: Prefix for nested keys

    Returns:
        Set of dot-separated key paths
    """
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.add(full_key)
            keys.update(flatten_keys(v, full_key))
    elif isinstance(obj, list):
        for item in obj:
            keys.update(flatten_keys(item, prefix))
    return keys
