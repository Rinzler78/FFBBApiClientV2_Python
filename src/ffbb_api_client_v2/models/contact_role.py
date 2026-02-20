from __future__ import annotations

from enum import Enum


class ContactRole(str, Enum):
    """Role/titre for a contact person."""

    CLUB = "Club"
    CORRESPONDANT_EQUIPE = "Correspondant"
    ENTRAINEUR = "Entraîneur"
    ENTRAINEUR_ADJOINT = "Entraîneur adjoint"
    PRESIDENT = "Président"
    CORRESPONDANT_CLUB = "Correspondant club"
    REFERENT_SECURITE = "Référent sécurité"
    MEMBRE = "Membre"
