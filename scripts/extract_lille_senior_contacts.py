#!/usr/bin/env python3
"""Extract senior PRO/NATIONAL/PRE_NATIONAL/LIGUE_FEMININE contacts near Lille.

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

NIVEAU_PRIORITY = {
    "PRO": 0,
    "NATIONAL": 1,
    "PRE_NATIONAL": 2,
    "LIGUE_FEMININE": 3,
}


@dataclass
class ContactRow:
    ville: str
    niveau: str
    sexe: str
    club: str
    equipes: list[str]
    titre: str
    nom: str
    prenom: str
    telephone: str
    email: str
    source: str

    @property
    def equipes_str(self) -> str:
        return " / ".join(sorted(set(self.equipes)))

    def to_csv_row(self) -> list[str]:
        return [
            self.ville,
            self.niveau,
            self.sexe,
            self.club,
            self.equipes_str,
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
    """
    if hit.club_pro:
        return "PRO"

    if hit.niveau and hit.niveau.code:
        echelon = hit.niveau.code.echelon
        if echelon == Echelon.NATIONAL:
            return "NATIONAL"
        if echelon == Echelon.PRE_NATIONAL:
            return "PRE_NATIONAL"
        if echelon == Echelon.LIGUE_FEMININE:
            return "LIGUE_FEMININE"

    return None


def contact_to_row(
    contact: ContactInfo,
    ville: str,
    niveau: str,
    sexe: str,
    club: str,
    equipe: str,
) -> ContactRow:
    return ContactRow(
        ville=ville,
        niveau=niveau,
        sexe=sexe,
        club=club,
        equipes=[equipe],
        titre=contact.titre,
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
            row.sexe,
            NIVEAU_PRIORITY.get(row.niveau, 99),
            row.ville,
            row.club,
            row.equipes_str,
            row.nom,
        )
    )

    grouped: dict[tuple[str, str, str], list[ContactRow]] = defaultdict(list)
    for row in rows:
        grouped[(row.sexe, row.niveau, row.ville)].append(row)

    with md_path.open("w", encoding="utf-8") as md_file:
        md_file.write("# Contacts seniors PRO/NATIONAL/PRE_NATIONAL/LIGUE_FEMININE\n\n")
        if not rows:
            md_file.write("Aucun contact trouvé.\n")
        for (sexe, niveau, ville), items in grouped.items():
            md_file.write(f"## {sexe} | {niveau} | {ville}\n\n")
            md_file.write(
                "| Club | Équipes | Titre | Nom | Prénom | Tél | Email | Source |\n"
            )
            md_file.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
            for item in items:
                md_file.write(
                    f"| {item.club} | {item.equipes_str} | {item.titre} "
                    f"| {item.nom} | {item.prenom} | {item.telephone} "
                    f"| {item.email} | {item.source} |\n"
                )
            md_file.write("\n")

    csv_headers = [
        "ville",
        "niveau",
        "sexe",
        "club",
        "equipes",
        "titre",
        "nom",
        "prenom",
        "telephone",
        "email",
        "source",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_headers)
        for row in rows:
            writer.writerow(row.to_csv_row())

    logger.info("Markdown report: %s", md_path)
    logger.info("CSV report: %s", csv_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract Lille-area senior PRO/NATIONAL contacts"
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

    # Step 2: Filter by level
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
    # Dedup key: per person per club (without equipe) — equipes are aggregated
    rows_by_key: dict[tuple[str, ...], ContactRow] = {}
    seen_organismes: dict[int, object] = {}

    for hit, level in qualified:
        sexe = hit.sexe or "Indéfini"
        equipe_name = hit.nom_equipe or hit.nom or ""
        club_name = hit.nom_club or hit.nom_organisme or ""
        ville = ""
        if hit.geo:
            ville = hit.nom_comite or ""

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
                    if org_id and org_id not in seen_organismes:
                        try:
                            club_contacts = client.get_club_contacts(org_id)
                            seen_organismes[org_id] = club_contacts
                            if club_contacts:
                                if club_contacts.club_contact:
                                    contacts.append(club_contacts.club_contact)
                                contacts.extend(club_contacts.membres)
                                if club_contacts.organisme.nom:
                                    club_name = club_contacts.organisme.nom
                        except FFBBServerError as e:
                            logger.warning(
                                "Server error fetching club %s: %s", org_id, e
                            )
                            seen_organismes[org_id] = None
            except FFBBServerError as e:
                logger.warning("Server error fetching engagement %s: %s", eng_id, e)

        for contact in contacts:
            # Dedup key excludes equipe — same person in same club = one row
            key = (
                ville,
                level,
                sexe,
                club_name,
                contact.titre,
                contact.nom,
                contact.prenom,
                contact.telephone,
                contact.email,
            )
            if key in rows_by_key:
                # Aggregate equipe name into existing row
                rows_by_key[key].equipes.append(equipe_name)
            else:
                rows_by_key[key] = contact_to_row(
                    contact, ville, level, sexe, club_name, equipe_name
                )

    rows = list(rows_by_key.values())

    # Step 4: Output
    write_outputs(rows, args.out_dir)
    logger.info("Total contacts found: %d", len(rows))


if __name__ == "__main__":
    main()
