#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.directus_ffbb.config import ENDPOINT_ENGAGEMENTS

LILLE_LAT = 50.62925
LILLE_LNG = 3.057256

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PHONE_PATTERN = re.compile(r"[^0-9+]")


@dataclass
class ContactRow:
    ville: str
    niveau: str
    sexe: str
    club: str
    equipe: str
    titre: str
    nom: str
    prenom: str
    telephone: str
    source: str

    def to_csv_row(self) -> list[str]:
        return [
            self.ville,
            self.niveau,
            self.sexe,
            self.club,
            self.equipe,
            self.titre,
            self.nom,
            self.prenom,
            self.telephone,
            self.source,
        ]


def normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    cleaned = PHONE_PATTERN.sub("", raw.strip())
    return cleaned or None


def sanitize_name(name: str | None) -> str:
    return (name.strip() if name else "").title()


def determine_level(engagement: dict[str, Any]) -> str | None:
    comp = engagement.get("idCompetition") or {}
    if comp.get("pro"):
        return "PRO"
    code = (comp.get("code") or "").upper()
    nom = (comp.get("nom") or "").upper()
    if any(
        target in code or target in nom
        for target in ["NM1", "NM2", "NM3", "NF1", "NF2", "NF3"]
    ):
        return "NATIONAL"
    return None


def is_senior(engagement: dict[str, Any]) -> bool:
    cat = engagement.get("categorie")
    if isinstance(cat, dict):
        code = (cat.get("code") or "").upper()
        libelle = (cat.get("libelle") or "").upper()
    else:
        code = (cat or "").upper()
        libelle = ""
    keywords = ["SE", "SENIOR", "SENIORS"]
    return any(keyword in code or keyword in libelle for keyword in keywords)


def extract_contacts(
    engagement: dict[str, Any],
    club: dict[str, Any],
    entraineur_data: dict[str, Any] | None,
    entraineur_adjoint_data: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    contacts: list[dict[str, Any]] = []

    def append(
        title: str, nom: str | None, prenom: str | None, phone: str | None, source: str
    ) -> None:
        normalized = normalize_phone(phone)
        if not normalized:
            logger.debug("Skipping %s; phone missing", title)
            return
        contacts.append(
            {
                "titre": title,
                "nom": sanitize_name(nom),
                "prenom": sanitize_name(prenom),
                "telephone": normalized,
                "source": source,
            }
        )

    # Correspondant équipe
    append(
        "Correspondant équipe",
        engagement.get("nomCorrespondantEquipe"),
        None,
        engagement.get("telephonePortableCorrespondantEquipe")
        or engagement.get("telephoneFixeCorrespondantEquipe")
        or engagement.get("telephoneTravailCorrespondantEquipe"),
        "directus:get_engagement",
    )

    if entraineur_data:
        append(
            "Entraîneur",
            entraineur_data.get("nom"),
            entraineur_data.get("prenom"),
            entraineur_data.get("telephonePortable")
            or entraineur_data.get("telephoneDomicile")
            or entraineur_data.get("telephoneTravail"),
            "directus:get_entraineur",
        )
    if entraineur_adjoint_data:
        append(
            "Entraîneur adjoint",
            entraineur_adjoint_data.get("nom"),
            entraineur_adjoint_data.get("prenom"),
            entraineur_adjoint_data.get("telephonePortable")
            or entraineur_adjoint_data.get("telephoneDomicile")
            or entraineur_adjoint_data.get("telephoneTravail"),
            "directus:get_entraineur",
        )

    # Club members
    for member in club.get("membres", []):
        phone = member.get("telephonePortable") or member.get("telephoneFixe")
        append(
            f"Membre · {member.get('codeFonction') or 'fonction inconnue'}",
            member.get("nom"),
            member.get("prenom"),
            phone,
            "directus:get_organisme",
        )

    return contacts


def fetch_club_members(organisme_data: Any) -> Sequence[dict[str, Any]]:
    return organisme_data.get("membres", []) if isinstance(organisme_data, dict) else []


def read_json_field(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not value:
        return ""
    return str(value)


def collect_contacts(
    meili_hits: Sequence[Any], client: FFBBAPIClientV2
) -> list[ContactRow]:
    rows: list[ContactRow] = []
    seen = set()

    for hit in meili_hits:
        club_code = getattr(hit, "code", None)
        organisme_id = getattr(hit, "id", None)
        if not club_code or not organisme_id:
            continue
        try:
            org_id = int(organisme_id)
        except (TypeError, ValueError):
            logger.warning("Skipping club with invalid id %s", organisme_id)
            continue

        logger.info("Fetching organisme %s (ID %s)", club_code, org_id)
        org_response = client.get_organisme(org_id)
        if not org_response:
            logger.warning("No organisme detail for %s", club_code)
            continue

        club_dict = org_response.__dict__
        ville = (
            (
                org_response.commune.libelle
                if org_response.commune and org_response.commune.libelle
                else ""
            )
            or hit.commune.libelle
            if getattr(hit, "commune", None)
            else ""
        )
        engagement_count = 0
        club_contacts_added = 0
        logger.info("Listing engagements for club %s", club_code)
        for engagement in client.list_engagements(
            limit=200,
            filter_criteria=json.dumps({"idOrganisme": {"code": {"_eq": club_code}}}),
        ):
            raw = client.api_ffbb_client._get_item(
                f"{ENDPOINT_ENGAGEMENTS}/{engagement.id}",
                fields="*",
            )
            engagement_count += 1
            if not raw:
                continue
            if not is_senior(raw):
                continue
            level = determine_level(raw)
            if not level:
                continue
            sexe = (
                raw.get("sexe") or raw.get("idCompetition", {}).get("sexe") or ""
            ).strip() or "Indéfini"
            equipe_name = raw.get("nomEquipe") or raw.get("nom") or ""
            entraineur_data = None
            if raw.get("entraineur"):
                entraineur_data = client.api_ffbb_client.get_entraineur(
                    int(raw["entraineur"])
                )
                entraineur_data = entraineur_data.__dict__ if entraineur_data else None
            entraineur_adjoint_data = None
            if raw.get("entraineurAdjoint"):
                entraineur_adjoint_data = client.api_ffbb_client.get_entraineur(
                    int(raw["entraineurAdjoint"])
                )
                entraineur_adjoint_data = (
                    entraineur_adjoint_data.__dict__
                    if entraineur_adjoint_data
                    else None
                )
            contacts = extract_contacts(
                raw, club_dict, entraineur_data, entraineur_adjoint_data
            )
            for contact in contacts:
                key = (
                    ville,
                    level,
                    sexe,
                    club_code,
                    equipe_name,
                    contact["titre"],
                    contact["nom"],
                    contact["prenom"],
                    contact["telephone"],
                )
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    ContactRow(
                        ville=ville,
                        niveau=level,
                        sexe=sexe,
                        club=org_response.nom or club_code,
                        equipe=equipe_name,
                        titre=contact["titre"],
                        nom=contact["nom"],
                        prenom=contact["prenom"],
                        telephone=contact["telephone"],
                        source=contact["source"],
                    )
                )
                club_contacts_added += 1
        logger.info(
            "Processed club %s: %d engagements scanned, %d unique contacts retained",
            club_code,
            engagement_count,
            club_contacts_added,
        )
    return rows


def write_outputs(rows: list[ContactRow], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "lille_senior_contacts.md"
    csv_path = out_dir / "lille_senior_contacts.csv"

    rows.sort(
        key=lambda row: (
            row.ville,
            0 if row.niveau == "PRO" else 1,
            row.sexe,
            row.club,
            row.equipe,
            row.titre,
            row.nom,
        )
    )

    grouped = defaultdict(list)
    for row in rows:
        grouped[(row.ville, row.niveau, row.sexe)].append(row)

    with md_path.open("w", encoding="utf-8") as md_file:
        md_file.write("# Contacts seniors PRO/National — Lille +100 km\n\n")
        if not rows:
            md_file.write("Aucun contact trouvé pour les critères demandés.\n")
        for (ville, niveau, sexe), items in grouped.items():
            md_file.write(f"## {ville} | {niveau} | {sexe}\n\n")
            md_file.write("| Titre | Nom | Prénom | Téléphone | Source |\n")
            md_file.write("| --- | --- | --- | --- | --- |\n")
            for item in items:
                md_file.write(
                    f"| {item.titre} | {item.nom} | {item.prenom} | {item.telephone} | {item.source} |\n"
                )
            md_file.write("\n")

    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "ville",
                "niveau",
                "sexe",
                "club",
                "equipe",
                "titre",
                "nom",
                "prenom",
                "telephone",
                "source",
            ]
        )
        for row in rows:
            writer.writerow(row.to_csv_row())

    logger.info("Markdown report: %s", md_path)
    logger.info("CSV report: %s", csv_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract Lille-area senior PRO/National contacts"
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
            "Dry run: would search organisms around Lille with radius %s km",
            args.radius,
        )
        return

    logger.info("Searching organisms around Lille (radius %.1f km)", args.radius)

    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )
    hits = client.meilisearch_ffbb_client.search_organismes_by_geo(
        lat=LILLE_LAT, lng=LILLE_LNG, radius_km=args.radius, limit=200
    )
    if not hits or not hits.hits:
        logger.warning("No clubs found around Lille.")
        return

    logger.info(
        "Found %d clubs around Lille within %.1f km", len(hits.hits), args.radius
    )

    rows = collect_contacts(hits.hits, client)
    write_outputs(rows, args.out_dir)


if __name__ == "__main__":
    main()
