"""Backward-compatibility re-export shim for poules models."""

from .get_poule_response import GetPouleResponse
from .poules_query import PoulesQuery

__all__ = ["GetPouleResponse", "PoulesQuery"]
