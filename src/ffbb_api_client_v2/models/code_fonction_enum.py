from __future__ import annotations

from enum import Enum

from .contact_role_enum import ContactRoleEnum


class CodeFonctionEnum(str, Enum):
    """CodeEnum fonction for club members (dirigeants)."""

    PRESIDENT = "PRES"
    CORRESPONDANT = "CP"
    REFERENT_SECURITE = "PSB"


CODE_FONCTION_TO_CONTACT_ROLE: dict[CodeFonctionEnum, ContactRoleEnum] = {
    CodeFonctionEnum.PRESIDENT: ContactRoleEnum.PRESIDENT,
    CodeFonctionEnum.CORRESPONDANT: ContactRoleEnum.CORRESPONDANT_CLUB,
    CodeFonctionEnum.REFERENT_SECURITE: ContactRoleEnum.REFERENT_SECURITE,
}
