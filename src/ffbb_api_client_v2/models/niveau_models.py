"""Backward-compatibility re-export shim for niveau module."""

from .categorie_type_enum import CategorieTypeEnum
from .niveau_extractor import NiveauExtractor, get_niveau_from_idcompetition
from .niveau_info import NiveauInfo
from .niveau_type_enum import NiveauTypeEnum

__all__ = [
    "CategorieTypeEnum",
    "NiveauExtractor",
    "NiveauInfo",
    "NiveauTypeEnum",
    "get_niveau_from_idcompetition",
]
