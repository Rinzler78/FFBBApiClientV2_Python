#!/usr/bin/env python3
"""Extract senior PRO/NATIONAL/LIGUE_FEMININE contacts near Lille.

Uses Meilisearch geo-search on engagements, then enriches via facade
contact methods (get_engagement_contacts, get_club_contacts).
"""

from __future__ import annotations

import argparse
import csv
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.exceptions import FFBBServerError
from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_hit import EngagementsHit
from ffbb_api_client_v2.models.contact_info import ContactInfo
from ffbb_api_client_v2.models.echelon import Echelon

LILLE_LAT = 50.62925
LILLE_LNG = 3.057256

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("ffbb_api_client_v2.utils.converter_utils").setLevel(logging.ERROR)

PHONE_PATTERN = re.compile(r"[^0-9+]")

NIVEAU_LABELS = {
    "PRO": "Pro",
    "NATIONAL": "National",
    "LIGUE_FEMININE": "Ligue Feminine",
}

NIVEAU_PRIORITY = {
    "Pro": 0,
    "National": 1,
    "Ligue Feminine": 2,
}


@dataclass
class ClubInfo:
    """Cached club info extracted from organisme response."""

    nom: str
    ville: str
    adresse: str


@dataclass
class ContactRow:
    ville: str
    adresse_club: str
    club: str
    niveau: str
    division: str
    poules: list[str]
    sexe: str
    titre: str
    nom: str
    prenom: str
    telephone: str
    email: str
    source: str

    @property
    def poules_str(self) -> str:
        unique = sorted({p for p in self.poules if p})
        return " / ".join(unique) if unique else ""

    def to_csv_row(self) -> list[str]:
        return [
            self.ville,
            self.adresse_club,
            self.club,
            self.niveau,
            self.division,
            self.poules_str,
            self.sexe,
            self.titre,
            self.nom,
            self.prenom,
            self.telephone,
            self.email,
            self.source,
        ]


def classify_engagement_level(hit: EngagementsHit) -> str | None:
    """Classify an engagement hit into a level category.

    Returns the level string or None if the engagement should be filtered out.
    Only keeps PRO, NATIONAL, and LIGUE_FEMININE.
    """
    if hit.club_pro:
        return "PRO"

    if hit.niveau and hit.niveau.code:
        echelon = hit.niveau.code.echelon
        if echelon == Echelon.NATIONAL:
            return "NATIONAL"
        if echelon == Echelon.LIGUE_FEMININE:
            return "LIGUE_FEMININE"

    return None


def extract_division(hit: EngagementsHit) -> str:
    """Extract the division code from an engagement hit (e.g. NM2, NF3, LF2)."""
    if hit.niveau and hit.niveau.code:
        return str(hit.niveau.code)
    return ""


def extract_poule(hit: EngagementsHit) -> str:
    """Extract the poule name from an engagement hit."""
    if hit.id_poule and hit.id_poule.nom:
        return hit.id_poule.nom
    return ""


def extract_club_info(organisme: GetOrganismeResponse) -> ClubInfo:
    """Extract ville and address from organisme cartographie."""
    nom = organisme.nom or ""
    ville = ""
    adresse = ""
    carto = organisme.cartographie
    if carto:
        ville = carto.ville or ""
        parts = [p for p in [carto.adresse, carto.code_postal, carto.ville] if p]
        adresse = ", ".join(parts)
    return ClubInfo(nom=nom, ville=ville, adresse=adresse)


def contact_to_row(
    contact: ContactInfo,
    ville: str,
    adresse_club: str,
    club: str,
    niveau: str,
    division: str,
    poule: str,
    sexe: str,
) -> ContactRow:
    return ContactRow(
        ville=ville,
        adresse_club=adresse_club,
        club=club,
        niveau=niveau,
        division=division,
        poules=[poule],
        sexe=sexe,
        titre=contact.titre.value,
        nom=contact.nom,
        prenom=contact.prenom,
        telephone=contact.telephone,
        email=contact.email,
        source=contact.source,
    )


def write_outputs(rows: list[ContactRow], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "lille_senior_contacts.md"
    csv_path = out_dir / "lille_senior_contacts.csv"

    rows.sort(
        key=lambda row: (
            row.ville,
            row.club,
            NIVEAU_PRIORITY.get(row.niveau, 99),
            row.division,
            row.poules_str,
            row.sexe,
            row.nom,
        )
    )

    grouped: dict[tuple[str, str, str], list[ContactRow]] = defaultdict(list)
    for row in rows:
        grouped[(row.sexe, row.niveau, row.ville)].append(row)

    with md_path.open("w", encoding="utf-8") as md_file:
        md_file.write("# Contacts seniors Elite / National\n\n")
        if not rows:
            md_file.write("Aucun contact trouve.\n")
        for (sexe, niveau, ville), items in grouped.items():
            md_file.write(f"## {sexe} | {niveau} | {ville}\n\n")
            md_file.write(
                "| Club | Adresse | Division | Poule | Titre | Nom"
                " | Prenom | Tel | Email | Source |\n"
            )
            md_file.write(
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            )
            for item in items:
                md_file.write(
                    f"| {item.club} | {item.adresse_club} | {item.division}"
                    f" | {item.poules_str} | {item.titre} | {item.nom}"
                    f" | {item.prenom} | {item.telephone} | {item.email}"
                    f" | {item.source} |\n"
                )
            md_file.write("\n")

    csv_headers = [
        "Ville",
        "Adresse",
        "Club",
        "Niveau",
        "Division",
        "Poule",
        "Sexe",
        "Titre",
        "Nom",
        "Prenom",
        "Telephone",
        "Email",
        "Source",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(csv_headers)
        for row in rows:
            writer.writerow(row.to_csv_row())

    logger.info("Markdown report: %s", md_path)
    logger.info("CSV report: %s", csv_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract Lille-area senior Elite/National contacts"
    )
    parser.add_argument(
        "--radius", type=float, default=100.0, help="Radius around Lille (km)"
    )
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument(
        "--dry-run", action="store_true", help="Print planned actions without tokens"
    )
    args = parser.parse_args()

    if args.dry_run:
        logger.info(
            "Dry run: would search engagements around Lille with radius %s km",
            args.radius,
        )
        return

    logger.info("Searching engagements around Lille (radius %.1f km)", args.radius)

    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )

    # Step 1: Geo search engagements via Meilisearch
    result = client.search_engagements_by_geo(
        lat=LILLE_LAT,
        lng=LILLE_LNG,
        radius_km=args.radius,
        limit=5000,
    )
    if not result or not result.hits:
        logger.warning("No engagements found around Lille.")
        return

    logger.info(
        "Found %d engagements around Lille within %.1f km",
        len(result.hits),
        args.radius,
    )

    # Step 2: Filter by level (PRO, NATIONAL, LIGUE_FEMININE only)
    qualified: list[tuple[EngagementsHit, str]] = []
    for hit in result.hits:
        level = classify_engagement_level(hit)
        if level:
            qualified.append((hit, level))

    logger.info("Qualified engagements: %d / %d", len(qualified), len(result.hits))

    if not qualified:
        logger.warning("No qualifying engagements found.")
        write_outputs([], args.out_dir)
        return

    # Step 3: Enrich via facade contact methods
    # Cache club info (ville, adresse, nom) per organisme
    club_cache: dict[int, ClubInfo | None] = {}
    rows_by_key: dict[tuple[str, ...], ContactRow] = {}

    for hit, level in qualified:
        sexe = hit.sexe or "Indefini"
        club_name = hit.nom_club or hit.nom_organisme or ""
        ville = ""
        adresse_club = ""

        niveau = NIVEAU_LABELS.get(level, level)
        division = extract_division(hit)
        poule = extract_poule(hit)

        # Get engagement contacts (correspondant + coaches)
        try:
            eng_id = int(hit.id) if hit.id else None
        except (ValueError, TypeError):
            eng_id = None

        contacts: list[ContactInfo] = []

        if eng_id:
            try:
                eng_contacts = client.get_engagement_contacts(eng_id)
                if eng_contacts:
                    for c in [
                        eng_contacts.correspondant,
                        eng_contacts.entraineur,
                        eng_contacts.entraineur_adjoint,
                    ]:
                        if c:
                            contacts.append(c)

                    # Get club contacts (deduplicated by organisme)
                    org_id = eng_contacts.engagement.idOrganisme
                    if org_id is not None:
                        if org_id not in club_cache:
                            try:
                                club_contacts = client.get_club_contacts(org_id)
                                if club_contacts:
                                    info = extract_club_info(club_contacts.organisme)
                                    club_cache[org_id] = info
                                    if club_contacts.club_contact:
                                        contacts.append(club_contacts.club_contact)
                                    contacts.extend(club_contacts.membres)
                                else:
                                    club_cache[org_id] = None
                            except FFBBServerError as e:
                                logger.warning(
                                    "Server error fetching club %s: %s", org_id, e
                                )
                                club_cache[org_id] = None

                        # Use cached club info
                        cached = club_cache.get(org_id)
                        if cached:
                            club_name = cached.nom or club_name
                            ville = cached.ville
                            adresse_club = cached.adresse
            except FFBBServerError as e:
                logger.warning("Server error fetching engagement %s: %s", eng_id, e)

        for contact in contacts:
            # Dedup key: per person per club per division — poules are aggregated
            key = (
                ville,
                club_name,
                niveau,
                division,
                sexe,
                contact.titre,
                contact.nom,
                contact.prenom,
                contact.telephone,
                contact.email,
            )
            if key in rows_by_key:
                rows_by_key[key].poules.append(poule)
            else:
                rows_by_key[key] = contact_to_row(
                    contact,
                    ville,
                    adresse_club,
                    club_name,
                    niveau,
                    division,
                    poule,
                    sexe,
                )

    rows = list(rows_by_key.values())

    # Step 4: Output
    write_outputs(rows, args.out_dir)
    logger.info("Total contacts found: %d", len(rows))


if __name__ == "__main__":
    main()
