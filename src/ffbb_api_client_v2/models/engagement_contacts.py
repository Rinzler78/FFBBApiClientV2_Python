from __future__ import annotations

from dataclasses import dataclass

from ..directus_ffbb.models.get_engagements_response import GetEngagementsResponse
from ..directus_ffbb.models.get_entraineurs_response import GetEntraineursResponse
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
class EngagementContacts:
    """Contacts for an engagement (team): correspondant + coaches."""

    engagement: GetEngagementsResponse
    correspondant: ContactInfo | None
    entraineur: ContactInfo | None
    entraineur_adjoint: ContactInfo | None


def extract_correspondant(engagement: GetEngagementsResponse) -> ContactInfo | None:
    """Extract correspondant contact from an engagement."""
    phone = _normalize_phone(
        engagement.telephonePortableCorrespondantEquipe
        or engagement.telephoneFixeCorrespondantEquipe
        or engagement.telephoneTravailCorrespondantEquipe
    )
    email = engagement.emailCorrespondantEquipe or ""
    if not phone and not email:
        return None
    return ContactInfo(
        titre=ContactRole.CORRESPONDANT_EQUIPE,
        nom=_sanitize_name(engagement.nomCorrespondantEquipe),
        prenom="",
        telephone=phone,
        email=email,
        source="directus:get_engagement",
    )


def extract_entraineur_contact(
    entraineur: GetEntraineursResponse | None, titre: ContactRole
) -> ContactInfo | None:
    """Extract contact info from an entraineur."""
    if not entraineur:
        return None
    phone = _normalize_phone(
        entraineur.telephonePortable
        or entraineur.telephoneDomicile
        or entraineur.telephoneTravail
    )
    email = entraineur.email or ""
    if not phone and not email:
        return None
    return ContactInfo(
        titre=titre,
        nom=_sanitize_name(entraineur.nom),
        prenom=_sanitize_name(entraineur.prenom),
        telephone=phone,
        email=email,
        source="directus:get_entraineur",
    )
