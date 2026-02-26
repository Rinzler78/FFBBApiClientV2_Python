from __future__ import annotations

from dataclasses import dataclass, field

from ..directus_ffbb.models.get_organisme_response import GetOrganismeResponse
from .code_fonction import CODE_FONCTION_TO_CONTACT_ROLE
from .contact_info import ContactInfo
from .contact_role import ContactRole
from .phone_number import PhoneNumber


def _normalize_phone(raw: str | None) -> str:
    if not raw:
        return ""
    return str(PhoneNumber(raw))


def _sanitize_name(name: str | None) -> str:
    return (name.strip() if name else "").title()


@dataclass
class ClubContacts:
    """Contacts for a club: club info + members/dirigeants."""

    organisme: GetOrganismeResponse
    club_contact: ContactInfo | None
    membres: list[ContactInfo] = field(default_factory=list)


def extract_club_info(organisme: GetOrganismeResponse) -> ContactInfo | None:
    """Extract club-level contact info (mail/telephone)."""
    phone = _normalize_phone(organisme.telephone)
    email = organisme.mail or ""
    if not phone and not email:
        return None
    return ContactInfo(
        titre=ContactRole.CLUB,
        nom=organisme.nom or "",
        prenom="",
        telephone=phone,
        email=email,
        source="directus:get_organisme",
    )


def extract_membres_contacts(organisme: GetOrganismeResponse) -> list[ContactInfo]:
    """Extract contacts from club members (dirigeants)."""
    contacts: list[ContactInfo] = []
    for membre in organisme.membres:
        phone = _normalize_phone(membre.telephone_portable or membre.telephone_fixe)
        email = membre.mail or ""
        if not phone and not email:
            continue
        contacts.append(
            ContactInfo(
                titre=(
                    CODE_FONCTION_TO_CONTACT_ROLE.get(
                        membre.code_fonction, ContactRole.MEMBRE
                    )
                    if membre.code_fonction
                    else ContactRole.MEMBRE
                ),
                nom=_sanitize_name(membre.nom),
                prenom=_sanitize_name(membre.prenom),
                telephone=phone,
                email=email,
                source="directus:get_organisme:membre",
            )
        )
    return contacts
