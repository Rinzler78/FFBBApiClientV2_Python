"""Backward-compatibility re-export shim for saisons models."""

from .get_saisons_response import GetSaisonsResponse
from .saisons_query import SaisonsQuery

__all__ = ["GetSaisonsResponse", "SaisonsQuery"]
