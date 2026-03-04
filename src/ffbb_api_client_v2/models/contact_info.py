from __future__ import annotations

from dataclasses import dataclass

from .contact_role_enum import ContactRoleEnum


@dataclass
class ContactInfo:
    """Structured contact information."""

    titre: ContactRoleEnum
    nom: str
    prenom: str
    telephone: str
    email: str
    source: str
