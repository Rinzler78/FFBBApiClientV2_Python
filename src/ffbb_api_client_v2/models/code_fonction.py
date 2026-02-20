from __future__ import annotations

from enum import Enum

from .contact_role import ContactRole


class CodeFonction(str, Enum):
    """Code fonction for club members (dirigeants)."""

    PRESIDENT = "PRES"
    CORRESPONDANT = "CP"
    REFERENT_SECURITE = "PSB"


CODE_FONCTION_TO_CONTACT_ROLE: dict[CodeFonction, ContactRole] = {
    CodeFonction.PRESIDENT: ContactRole.PRESIDENT,
    CodeFonction.CORRESPONDANT: ContactRole.CORRESPONDANT_CLUB,
    CodeFonction.REFERENT_SECURITE: ContactRole.REFERENT_SECURITE,
}
