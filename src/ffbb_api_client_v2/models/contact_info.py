from __future__ import annotations

from dataclasses import dataclass

from .contact_role import ContactRole


@dataclass
class ContactInfo:
    """Structured contact information."""

    titre: ContactRole
    nom: str
    prenom: str
    telephone: str
    email: str
    source: str
