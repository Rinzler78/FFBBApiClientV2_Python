from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContactInfo:
    """Structured contact information."""

    titre: str
    nom: str
    prenom: str
    telephone: str
    email: str
    source: str
