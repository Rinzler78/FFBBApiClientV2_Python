#!/usr/bin/env python3
"""Extract senior PRO/NATIONAL/LIGUE_FEMININE contacts near a geographic point.

Uses Meilisearch geo-search on engagements, then enriches via facade
contact methods (get_engagement_contacts, get_club_contacts).
Produces a hierarchical Markdown report sorted by distance, a CSV export,
and a professional HTML report with an interactive Leaflet/OSM map.

Usage:
    python examples/extract_contacts.py --lat 50.629 --lng 3.057 --city-name Lille
    python examples/extract_contacts.py --lat 48.856 --lng 2.352 --city-name Paris --radius 50
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.directus_ffbb.config import API_FFBB_BASE_URL, ENDPOINT_ASSETS
from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.exceptions import FFBBApiError
from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_hit import EngagementsHit
from ffbb_api_client_v2.models.age_group import AgeGroup
from ffbb_api_client_v2.models.contact_info import ContactInfo
from ffbb_api_client_v2.models.echelon import Echelon

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("ffbb_api_client_v2.utils.converter_utils").setLevel(logging.ERROR)

# Echelons considered pro-level (top-tier competitions)
PRO_ECHELONS: frozenset[Echelon] = frozenset(
    {Echelon.LIGUE_FEMININE, Echelon.BASKET_FAUTEUIL}
)

# Echelons considered national-level
NATIONAL_ECHELONS: frozenset[Echelon] = frozenset({Echelon.NATIONAL})

# All echelons we accept
ACCEPTED_ECHELONS: frozenset[Echelon] = PRO_ECHELONS | NATIONAL_ECHELONS

# Display labels and sort priority, derived from the sets above
NIVEAU_LABELS = {"PRO": "Pro", "NATIONAL": "National"}
NIVEAU_PRIORITY = {"Pro": 0, "National": 1}

_COMPETITIONS_BASE = "https://competitions.ffbb.com"
_ASSET_BASE = f"{API_FFBB_BASE_URL}{ENDPOINT_ASSETS}"


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate the great-circle distance between two points (km)."""
    r = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def slugify(text: str) -> str:
    """Create a URL-safe slug for Markdown anchors."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


def _contact_id(c) -> str:
    """Generate a stable HTML-safe id for a contact (nom-prenom-tel-email)."""
    raw = f"{getattr(c, 'nom', '')}-{getattr(c, 'prenom', '')}"
    if getattr(c, "telephone", ""):
        raw += f"-{c.telephone}"
    elif getattr(c, "email", ""):
        raw += f"-{c.email}"
    return f"contact-{slugify(raw)}"


def _md_escape(text: str) -> str:
    """Escape pipe characters for Markdown tables."""
    return text.replace("|", "\\|")


def _format_phone(raw: str) -> str:
    """Format a French phone number as 06 12 34 56 78."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits.startswith("33"):
        digits = "0" + digits[2:]
    if len(digits) == 10:
        return " ".join(digits[i : i + 2] for i in range(0, 10, 2))
    return raw


def _directions_url(lat: float | None, lng: float | None, address: str) -> str:
    """Build a Google Maps directions URL."""
    if lat is not None and lng is not None:
        return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"
    if address:
        from urllib.parse import quote

        return f"https://www.google.com/maps/dir/?api=1&destination={quote(address)}"
    return ""


# ---------------------------------------------------------------------------
# Report model
# ---------------------------------------------------------------------------


@dataclass
class ReportContact:
    """A single person's contact information."""

    role: str
    nom: str
    prenom: str
    telephone: str
    email: str
    source: str


@dataclass
class ReportTeam:
    """An engagement team within a club."""

    sexe: str
    niveau: str
    division: str
    poules: list[str]
    ranking_url: str
    competition_logo_url: str
    ranking_position: int | None
    ranking_total: int | None
    next_match_date: str
    next_match_opponent: str
    next_match_salle_name: str
    next_match_salle_address: str
    next_match_salle_map_url: str
    contacts: list[ReportContact]

    @property
    def label(self) -> str:
        parts = [p for p in [self.sexe, self.niveau, self.division] if p]
        label = " · ".join(parts) if parts else self.niveau
        if self.poules:
            label += f" — {' / '.join(self.poules)}"
        return label


@dataclass
class ReportClub:
    """A club with its teams and club-level contacts."""

    nom: str
    adresse: str
    lat: float | None
    lng: float | None
    site_web: str
    url_ffbb: str
    logo_url: str
    telephone: str
    mail: str
    salle_nom: str
    salle_adresse: str
    salle_map_url: str
    teams: list[ReportTeam]
    club_contacts: list[ReportContact]

    @property
    def total_contacts(self) -> int:
        return sum(len(t.contacts) for t in self.teams) + len(self.club_contacts)


@dataclass
class ReportCity:
    """A city with its clubs."""

    ville: str
    code_postal: str
    distance_km: float | None
    lat: float | None
    lng: float | None
    clubs: list[ReportClub]

    @property
    def total_clubs(self) -> int:
        return len(self.clubs)

    @property
    def total_teams(self) -> int:
        return sum(len(c.teams) for c in self.clubs)

    @property
    def total_contacts(self) -> int:
        return sum(c.total_contacts for c in self.clubs)


@dataclass
class ContactReport:
    """Full report: search parameters + hierarchical results."""

    # Search parameters
    city_name: str
    lat: float
    lng: float
    radius: float
    timestamp: str

    # Results
    cities: list[ReportCity]

    @property
    def total_cities(self) -> int:
        return len(self.cities)

    @property
    def total_clubs(self) -> int:
        return sum(c.total_clubs for c in self.cities)

    @property
    def total_teams(self) -> int:
        return sum(c.total_teams for c in self.cities)

    @property
    def total_contacts(self) -> int:
        """Unique contacts count (deduplicated by identity)."""
        seen: set[str] = set()
        for city in self.cities:
            for club in city.clubs:
                for c in club.club_contacts:
                    seen.add(_contact_id(c))
                for team in club.teams:
                    for c in team.contacts:
                        seen.add(_contact_id(c))
        return len(seen)

    @property
    def total_contact_mentions(self) -> int:
        """Total contact mentions (including duplicates across teams)."""
        return sum(c.total_contacts for c in self.cities)

    @property
    def center_teams(self) -> dict[str, list[str]]:
        """Teams in the center city, grouped by niveau."""
        result: dict[str, list[str]] = defaultdict(list)
        for city in self.cities:
            if city.ville.lower() == self.city_name.lower():
                for club in city.clubs:
                    for team in club.teams:
                        label = f"{team.sexe} {team.division}".strip()
                        result[team.niveau].append(label)
        return dict(result)

    @staticmethod
    def _salle_signature(
        name: str,
        address: str,
        map_url: str,
    ) -> tuple[str, str, str]:
        return (name.strip(), address.strip(), map_url.strip())

    @staticmethod
    def _salle_label(name: str, address: str) -> str:
        cleaned_name = (name or "").strip()
        if cleaned_name:
            return cleaned_name
        cleaned_address = (address or "").strip()
        if not cleaned_address:
            return ""
        first_part = cleaned_address.split(",", 1)[0].strip()
        return first_part or cleaned_address

    def _collect_salles(
        self,
    ) -> tuple[list[dict[str, str]], dict[tuple[str, str, str], str]]:
        """Collect unique salles and map each salle signature to an anchor id."""
        entries: list[dict[str, str]] = []
        signature_to_anchor: dict[tuple[str, str, str], str] = {}
        dedupe_key_to_anchor: dict[str, str] = {}

        def register(name: str, address: str, map_url: str) -> None:
            signature = self._salle_signature(name, address, map_url)
            label = self._salle_label(signature[0], signature[1])
            if not label and not signature[1] and not signature[2]:
                return

            dedupe_key = (
                signature[2].lower()
                if signature[2]
                else f"{slugify(signature[0])}:{slugify(signature[1])}"
            )
            anchor = dedupe_key_to_anchor.get(dedupe_key)
            if anchor is None:
                idx = len(entries) + 1
                anchor = f"salle-{idx}-{(slugify(label) or 'salle')[:40]}"
                dedupe_key_to_anchor[dedupe_key] = anchor
                entries.append(
                    {
                        "anchor": anchor,
                        "label": label or f"Salle {idx}",
                        "address": signature[1],
                        "map_url": signature[2],
                    }
                )
            signature_to_anchor[signature] = anchor

        for city in self.cities:
            for club in city.clubs:
                register(club.salle_nom, club.salle_adresse, club.salle_map_url)
                for team in club.teams:
                    register(
                        team.next_match_salle_name,
                        team.next_match_salle_address,
                        team.next_match_salle_map_url,
                    )

        return entries, signature_to_anchor

    # ------------------------------------------------------------------
    # Build from flat rows
    # ------------------------------------------------------------------

    @staticmethod
    def build(
        city_name: str,
        lat: float,
        lng: float,
        radius: float,
        rows: list[_CollectedRow],
        city_distances: dict[str, float],
        city_postcodes: dict[str, str],
        club_infos: dict[str, _ClubInfo],
        city_geo: dict[str, _CityGeo],
    ) -> ContactReport:
        """Build a hierarchical report from flat collected rows."""

        # Group: ville -> club -> (sexe, niveau, division) -> rows
        ville_clubs: dict[str, dict[str, list[_CollectedRow]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for row in rows:
            ville_clubs[row.ville][row.club].append(row)

        sorted_villes = sorted(
            ville_clubs.keys(),
            key=lambda v: city_distances.get(v, float("inf")),
        )

        report_cities: list[ReportCity] = []
        for ville in sorted_villes:
            cp = city_postcodes.get(ville, "")
            dist = city_distances.get(ville)
            clubs_dict = ville_clubs[ville]

            geo = city_geo.get(ville)
            city_lat = geo.lat if geo else None
            city_lng = geo.lng if geo else None

            report_clubs: list[ReportClub] = []
            for club_name in sorted(clubs_dict.keys()):
                club_rows = clubs_dict[club_name]
                adresse = club_rows[0].adresse_club if club_rows else ""

                # Lookup club info for enriched fields
                ci = club_infos.get(club_name)

                # Separate club-level vs team-level
                club_contact_rows = [
                    r for r in club_rows if "get_organisme" in r.source
                ]
                team_rows = [r for r in club_rows if "get_organisme" not in r.source]

                # Group teams
                team_groups: dict[tuple[str, str, str], list[_CollectedRow]] = (
                    defaultdict(list)
                )
                for r in team_rows:
                    team_groups[(r.sexe, r.niveau, r.division)].append(r)

                report_teams: list[ReportTeam] = []
                for (sexe, niveau, division), t_rows in sorted(
                    team_groups.items(),
                    key=lambda item: (
                        NIVEAU_PRIORITY.get(item[0][1], 99),
                        item[0][2],
                        item[0][0],
                    ),
                ):
                    effective_rows = _select_effective_team_rows(t_rows)
                    poules = sorted({p for r in effective_rows for p in r.poules if p})
                    ranking_url = ""
                    competition_logo_url = ""
                    ranking_position: int | None = None
                    ranking_total: int | None = None
                    next_match_date = ""
                    next_match_opponent = ""
                    next_match_salle_name = ""
                    next_match_salle_address = ""
                    next_match_salle_map_url = ""
                    for r in effective_rows:
                        if not ranking_url and r.ranking_url:
                            ranking_url = r.ranking_url
                        if not competition_logo_url and r.competition_logo_url:
                            competition_logo_url = r.competition_logo_url
                        if ranking_position is None and r.ranking_position is not None:
                            ranking_position = r.ranking_position
                        if ranking_total is None and r.ranking_total is not None:
                            ranking_total = r.ranking_total
                        if not next_match_date and r.next_match_date:
                            next_match_date = r.next_match_date
                        if not next_match_opponent and r.next_match_opponent:
                            next_match_opponent = r.next_match_opponent
                        if not next_match_salle_name and r.next_match_salle_name:
                            next_match_salle_name = r.next_match_salle_name
                        if not next_match_salle_address and r.next_match_salle_address:
                            next_match_salle_address = r.next_match_salle_address
                        if not next_match_salle_map_url and r.next_match_salle_map_url:
                            next_match_salle_map_url = r.next_match_salle_map_url
                    contacts = [
                        ReportContact(
                            role=r.titre,
                            nom=r.nom,
                            prenom=r.prenom,
                            telephone=r.telephone,
                            email=r.email,
                            source=r.source,
                        )
                        for r in sorted(effective_rows, key=lambda x: (x.nom, x.prenom))
                    ]
                    report_teams.append(
                        ReportTeam(
                            sexe=sexe,
                            niveau=niveau,
                            division=division,
                            poules=poules,
                            ranking_url=ranking_url,
                            competition_logo_url=competition_logo_url,
                            ranking_position=ranking_position,
                            ranking_total=ranking_total,
                            next_match_date=next_match_date,
                            next_match_opponent=next_match_opponent,
                            next_match_salle_name=next_match_salle_name,
                            next_match_salle_address=next_match_salle_address,
                            next_match_salle_map_url=next_match_salle_map_url,
                            contacts=contacts,
                        )
                    )

                club_contacts = [
                    ReportContact(
                        role=r.titre,
                        nom=r.nom,
                        prenom=r.prenom,
                        telephone=r.telephone,
                        email=r.email,
                        source=r.source,
                    )
                    for r in sorted(club_contact_rows, key=lambda x: (x.nom, x.prenom))
                ]

                report_clubs.append(
                    ReportClub(
                        nom=club_name,
                        adresse=adresse,
                        lat=ci.lat if ci else None,
                        lng=ci.lng if ci else None,
                        site_web=ci.site_web if ci else "",
                        url_ffbb=ci.url_ffbb if ci else "",
                        logo_url=ci.logo_url if ci else "",
                        telephone=ci.telephone if ci else "",
                        mail=ci.mail if ci else "",
                        salle_nom=ci.salle_nom if ci else "",
                        salle_adresse=ci.salle_adresse if ci else "",
                        salle_map_url=ci.salle_map_url if ci else "",
                        teams=report_teams,
                        club_contacts=club_contacts,
                    )
                )

            report_cities.append(
                ReportCity(
                    ville=ville,
                    code_postal=cp,
                    distance_km=dist,
                    lat=city_lat,
                    lng=city_lng,
                    clubs=report_clubs,
                )
            )

        # Ensure the target city always appears (even with 0 matching teams)
        target_present = any(
            c.ville.lower() == city_name.lower() for c in report_cities
        )
        if not target_present:
            report_cities.insert(
                0,
                ReportCity(
                    ville=city_name,
                    code_postal="",
                    distance_km=0.0,
                    lat=lat,
                    lng=lng,
                    clubs=[],
                ),
            )

        return ContactReport(
            city_name=city_name,
            lat=lat,
            lng=lng,
            radius=radius,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
            cities=report_cities,
        )

    # ------------------------------------------------------------------
    # Export: Markdown
    # ------------------------------------------------------------------

    def to_markdown(self, path: Path) -> None:
        """Write the hierarchical Markdown report."""
        with path.open("w", encoding="utf-8") as f:
            self._write_md_header(f)
            self._write_md_center_city(f)
            self._write_md_cities_table(f)
            self._write_md_clubs_table(f)
            self._write_md_contacts(f)
            f.write(f"*Genere le {self.timestamp} par ffbb-api-client-v2*\n")

    def _write_md_header(self, f) -> None:
        f.write(f"# Contacts Basketball Senior — {self.city_name}\n\n")
        f.write("### Recherche\n\n")
        f.write("| Parametre | Valeur |\n")
        f.write("|:----------|:-------|\n")
        f.write(f"| Ville | **{self.city_name}** |\n")
        f.write(f"| Position | {self.lat:.4f}, {self.lng:.4f} |\n")
        f.write(f"| Rayon | {self.radius:.0f} km |\n")
        f.write("| Niveaux | Pro, National |\n")
        f.write("| Sexe | Masculin, Feminin |\n")
        f.write("| Tranches d'ages | Senior |\n\n")
        f.write(f"*{self.timestamp}*\n\n")
        f.write("---\n\n")

    def _write_md_center_city(self, f) -> None:
        f.write(f"## {self.city_name}\n\n")
        ct = self.center_teams
        if ct:
            f.write(f"Equipes au niveau recherche a **{self.city_name}** :\n\n")
            for niveau in sorted(ct, key=lambda n: NIVEAU_PRIORITY.get(n, 99)):
                teams = sorted(ct[niveau])
                f.write(f"- **{niveau}** : {', '.join(teams)}\n")
            f.write("\n")
        else:
            f.write(
                f"Aucune equipe Pro ou National a **{self.city_name}**. "
                f"Recherche elargie a {self.radius:.0f} km.\n\n"
            )
        f.write("---\n\n")

    def _write_md_cities_table(self, f) -> None:
        f.write(f"## Villes ({self.total_cities})\n\n")
        f.write("| # | Ville | Dist. | Clubs | Equipes | Contacts |\n")
        f.write("|--:|:------|------:|------:|--------:|---------:|\n")
        for idx, city in enumerate(self.cities, 1):
            label = (
                f"{city.ville} ({city.code_postal})" if city.code_postal else city.ville
            )
            anchor = f"contacts-{slugify(city.ville)}"
            dist = f"{city.distance_km:.1f} km" if city.distance_km is not None else "?"
            f.write(
                f"| {idx} | [{_md_escape(label)}](#{anchor})"
                f" | {dist} | {city.total_clubs}"
                f" | {city.total_teams} | {city.total_contacts} |\n"
            )
        f.write("\n---\n\n")

    def _write_md_clubs_table(self, f) -> None:
        f.write(f"## Clubs ({self.total_clubs})\n\n")
        f.write("| # | Club | Ville | Dist. | Equipes | Contacts |\n")
        f.write("|--:|:-----|:------|------:|--------:|---------:|\n")
        idx = 0
        for city in self.cities:
            for club in city.clubs:
                idx += 1
                dist = (
                    f"{city.distance_km:.1f} km"
                    if city.distance_km is not None
                    else "?"
                )
                f.write(
                    f"| {idx} | {_md_escape(club.nom)}"
                    f" | {_md_escape(city.ville)}"
                    f" | {dist} | {len(club.teams)}"
                    f" | {club.total_contacts} |\n"
                )
        f.write("\n---\n\n")

    def _write_md_contacts(self, f) -> None:
        f.write(f"## Contacts ({self.total_contacts})\n\n")
        for city in self.cities:
            label = (
                f"{city.ville} ({city.code_postal})" if city.code_postal else city.ville
            )
            dist = (
                f"{city.distance_km:.1f} km"
                if city.distance_km is not None
                else "distance inconnue"
            )
            f.write(f"### {_md_escape(label)} — {dist}\n\n")

            if not city.clubs:
                f.write(
                    f"*Aucune equipe Pro ou National a **{_md_escape(city.ville)}**."
                    f" Recherche elargie a {self.radius:.0f} km.*\n\n"
                )

            for club in city.clubs:
                f.write(f"#### {_md_escape(club.nom)}\n\n")
                if club.adresse:
                    f.write(f"> {_md_escape(club.adresse)}\n\n")

                for team in club.teams:
                    f.write(f"**{_md_escape(team.label)}**\n\n")
                    f.write("| Role | Nom | Prenom | Tel | Email |\n")
                    f.write("|:-----|:----|:-------|:----|:------|\n")
                    for c in team.contacts:
                        f.write(
                            f"| {_md_escape(c.role)}"
                            f" | {_md_escape(c.nom)}"
                            f" | {_md_escape(c.prenom)}"
                            f" | {_md_escape(c.telephone)}"
                            f" | {_md_escape(c.email)} |\n"
                        )
                    f.write("\n")

                if club.club_contacts:
                    f.write("**Contacts club**\n\n")
                    f.write("| Role | Nom | Prenom | Tel | Email |\n")
                    f.write("|:-----|:----|:-------|:----|:------|\n")
                    for c in club.club_contacts:
                        f.write(
                            f"| {_md_escape(c.role)}"
                            f" | {_md_escape(c.nom)}"
                            f" | {_md_escape(c.prenom)}"
                            f" | {_md_escape(c.telephone)}"
                            f" | {_md_escape(c.email)} |\n"
                        )
                    f.write("\n")

            f.write(
                f"[↑ Villes](#villes-{self.total_cities})"
                f" · [↑ Clubs](#clubs-{self.total_clubs})"
                "\n\n---\n\n"
            )

    # ------------------------------------------------------------------
    # Export: CSV
    # ------------------------------------------------------------------

    def to_csv(self, path: Path) -> None:
        """Write a flat CSV export."""
        headers = [
            "Ville",
            "Code_Postal",
            "Distance_km",
            "Adresse",
            "Club",
            "Niveau",
            "Division",
            "Poule",
            "Sexe",
            "Role",
            "Nom",
            "Prenom",
            "Telephone",
            "Email",
            "Source",
        ]
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(headers)
            for city in self.cities:
                dist = f"{city.distance_km:.1f}" if city.distance_km is not None else ""
                for club in city.clubs:
                    for team in club.teams:
                        poule = " / ".join(team.poules) if team.poules else ""
                        for c in team.contacts:
                            writer.writerow(
                                [
                                    city.ville,
                                    city.code_postal,
                                    dist,
                                    club.adresse,
                                    club.nom,
                                    team.niveau,
                                    team.division,
                                    poule,
                                    team.sexe,
                                    c.role,
                                    c.nom,
                                    c.prenom,
                                    c.telephone,
                                    c.email,
                                    c.source,
                                ]
                            )
                    for c in club.club_contacts:
                        writer.writerow(
                            [
                                city.ville,
                                city.code_postal,
                                dist,
                                club.adresse,
                                club.nom,
                                "",
                                "",
                                "",
                                "",
                                c.role,
                                c.nom,
                                c.prenom,
                                c.telephone,
                                c.email,
                                c.source,
                            ]
                        )

    # ------------------------------------------------------------------
    # Export: HTML (Leaflet + OSM interactive map)
    # ------------------------------------------------------------------

    def to_html(self, path: Path) -> None:
        """Write a professional HTML report with interactive Leaflet map."""
        h = _html_escape
        role_set: set[str] = set()
        for city in self.cities:
            for club in city.clubs:
                for contact in club.club_contacts:
                    if contact.role:
                        role_set.add(contact.role)
                for team in club.teams:
                    for contact in team.contacts:
                        if contact.role:
                            role_set.add(contact.role)
        role_options = sorted(role_set, key=str.casefold)
        max_city_distance = max(
            (city.distance_km for city in self.cities if city.distance_km is not None),
            default=self.radius,
        )
        max_distance_slider = max(
            5,
            int(math.ceil(max(max_city_distance, self.radius))),
        )
        salle_entries, salle_anchor_by_signature = self._collect_salles()

        with path.open("w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html lang='fr'>\n<head>\n")
            f.write("<meta charset='utf-8'>\n")
            f.write(
                "<meta name='viewport'"
                " content='width=device-width, initial-scale=1'>\n"
            )
            f.write(
                f"<title>Contacts Basketball Senior" f" — {h(self.city_name)}</title>\n"
            )
            # Leaflet CSS + MarkerCluster CSS
            f.write(
                "<link rel='stylesheet'"
                " href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'"
                " integrity='sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY='"
                " crossorigin=''/>\n"
                "<link rel='stylesheet'"
                " href='https://unpkg.com/leaflet.markercluster@1.5.3"
                "/dist/MarkerCluster.css' crossorigin=''/>\n"
                "<link rel='stylesheet'"
                " href='https://unpkg.com/leaflet.markercluster@1.5.3"
                "/dist/MarkerCluster.Default.css' crossorigin=''/>\n"
            )
            f.write("<style>\n")
            f.write(_HTML_CSS)
            f.write("</style>\n</head>\n<body>\n")
            f.write(
                "<a class='skip-link' href='#main-content'>"
                "Aller au contenu principal</a>\n"
            )

            # --- Sidebar (desktop nav) ---
            f.write("<nav class='sidebar' id='sidebar'>\n")
            f.write(f"<div class='sidebar-title'>{h(self.city_name)}</div>\n")
            f.write("<ul class='sidebar-list'>\n")
            for city in self.cities:
                anchor = f"city-{slugify(city.ville)}"
                dist = (
                    f"{city.distance_km:.0f}" if city.distance_km is not None else "?"
                )
                f.write(
                    f"<li data-city-link='{h(anchor)}'><a href='#{anchor}'>{h(city.ville)}"
                    f"<span class='sidebar-dist'>{dist} km</span></a></li>\n"
                )
            f.write(
                "<li class='sidebar-annuaire'>"
                "<a href='#annuaire'>&#x1F4D6; Annuaire</a></li>\n"
            )
            if salle_entries:
                f.write(
                    "<li class='sidebar-annuaire'>"
                    "<a href='#salles'>&#x1F4CD; Salles</a></li>\n"
                )
            f.write("</ul>\n</nav>\n\n")

            # --- Main content ---
            f.write("<main class='content' id='main-content'>\n")

            # Header
            f.write("<header class='hero'>\n")
            f.write("<div class='hero-main'>\n")
            f.write("<div>\n")
            f.write("<p class='hero-kicker'>Recherche FFBB</p>\n")
            f.write(
                f"<h1>Contacts Basketball Senior" f" &mdash; {h(self.city_name)}</h1>\n"
            )
            f.write("</div>\n")
            f.write(f"<p class='hero-date'>{h(self.timestamp)}</p>\n")
            f.write("</div>\n")
            f.write(
                "<p class='hero-subtitle'>"
                "Extraction des clubs et contacts seniors Pro/National dans un rayon "
                "personnalise autour de la ville de recherche."
                "</p>\n"
            )
            f.write("<ul class='hero-facts'>\n")
            for label, value in [
                ("Ville", self.city_name),
                ("Position", f"{self.lat:.4f}, {self.lng:.4f}"),
                ("Rayon", f"{self.radius:.0f} km"),
                ("Niveaux", "Pro, National"),
                ("Sexe", "Masculin, Feminin"),
                ("Ages", "Senior"),
            ]:
                f.write(
                    "<li class='hero-fact'>"
                    f"<span class='hero-fact__label'>{h(label)}</span>"
                    f"<span class='hero-fact__value'>{h(value)}</span>"
                    "</li>\n"
                )
            f.write("</ul>\n")
            f.write("</header>\n\n")

            # Summary stats
            f.write("<section class='summary'>\n")
            f.write("<div class='stat-grid'>\n")
            for label, val in [
                ("Villes", self.total_cities),
                ("Clubs", self.total_clubs),
                ("Equipes", self.total_teams),
                ("Contacts", self.total_contacts),
                ("Mentions", self.total_contact_mentions),
            ]:
                f.write(
                    f"<div class='stat'>"
                    f"<span class='stat-val'>{val}</span>"
                    f"<span class='stat-label'>{label}</span></div>\n"
                )
            f.write("</div>\n</section>\n\n")

            # Search/filter/sort controls
            f.write("<section class='controls' aria-labelledby='controls-title'>\n")
            f.write(
                "<h2 id='controls-title' class='visually-hidden'>"
                "Recherche et filtres</h2>\n"
            )
            f.write("<div class='controls-bar'>\n")
            f.write(
                "<label class='control-field control-field--search' for='ui-search'>"
                "<span>Recherche</span>"
                "<input id='ui-search' type='search' "
                "placeholder='Club, ville, contact, email...' "
                "autocomplete='off'></label>\n"
            )
            f.write("<div class='controls-actions'>\n")
            f.write(
                "<p class='controls-result' id='ui-results'>"
                f"{self.total_clubs} clubs affiches</p>\n"
            )
            f.write(
                "<button type='button' id='ui-reset' class='control-reset'>"
                "Reinitialiser</button>\n"
            )
            f.write("</div>\n")
            f.write("</div>\n")
            f.write("<details class='controls-advanced'>\n")
            f.write("<summary>Filtres avances</summary>\n")
            f.write("<div class='controls-grid'>\n")
            f.write("<label class='control-field' for='ui-city'>")
            f.write("<span>Ville</span>")
            f.write("<select id='ui-city'>")
            f.write("<option value='all'>Toutes les villes</option>")
            for city in self.cities:
                city_slug = slugify(city.ville)
                f.write(f"<option value='{h(city_slug)}'>{h(city.ville)}</option>")
            f.write("</select></label>\n")
            f.write("<label class='control-field' for='ui-level'>")
            f.write("<span>Niveau</span>")
            f.write("<select id='ui-level'>")
            f.write("<option value='all'>Tous les niveaux</option>")
            f.write("<option value='pro'>Pro</option>")
            f.write("<option value='national'>National</option>")
            f.write("</select></label>\n")
            f.write("<label class='control-field' for='ui-role'>")
            f.write("<span>Role</span>")
            f.write("<select id='ui-role'>")
            f.write("<option value='all'>Tous les roles</option>")
            for role in role_options:
                f.write(f"<option value='{h(slugify(role))}'>{h(role)}</option>")
            f.write("</select></label>\n")
            f.write(
                "<label class='control-field control-field--range' for='ui-distance'>"
            )
            f.write(
                "<span>Distance max: <strong id='ui-distance-value'>"
                f"{max_distance_slider}</strong> km</span>"
            )
            f.write(
                f"<input id='ui-distance' type='range' min='0' max='{max_distance_slider}' "
                f"value='{max_distance_slider}' step='1'>"
            )
            f.write("</label>\n")
            f.write("<label class='control-field' for='ui-sort'>")
            f.write("<span>Tri</span>")
            f.write("<select id='ui-sort'>")
            f.write("<option value='distance'>Distance</option>")
            f.write("<option value='city'>Ville (A-Z)</option>")
            f.write("<option value='club'>Club (A-Z)</option>")
            f.write("<option value='contacts'>Nb contacts</option>")
            f.write("</select></label>\n")
            f.write("</div>\n")
            f.write("</details>\n")
            f.write("</section>\n\n")

            # Map
            f.write("<section id='map-section'>\n")
            f.write("<h2>Carte</h2>\n")
            f.write("<div id='map' aria-label='Carte des clubs'></div>\n")
            f.write(
                "<noscript><p class='noscript-msg'>"
                "Activez JavaScript pour afficher la carte interactive."
                "</p></noscript>\n"
            )
            f.write("</section>\n\n")

            # Mobile nav (replaces sidebar on small screens)
            f.write("<details class='mobile-nav'>\n")
            f.write(f"<summary>Navigation villes ({self.total_cities})</summary>\n")
            f.write("<ul>\n")
            for city in self.cities:
                anchor = f"city-{slugify(city.ville)}"
                dist = (
                    f"{city.distance_km:.0f} km"
                    if city.distance_km is not None
                    else "?"
                )
                f.write(
                    f"<li data-city-link='{h(anchor)}'><a href='#{anchor}'>"
                    f"{h(city.ville)} — {dist}</a></li>\n"
                )
            f.write(
                "<li><a href='#annuaire'>" "&#x1F4D6; Annuaire des contacts</a></li>\n"
            )
            if salle_entries:
                f.write("<li><a href='#salles'>&#x1F4CD; Salles</a></li>\n")
            f.write("</ul>\n</details>\n\n")

            # Contacts detail by city
            f.write("<div id='cities-container'>\n")
            for city in self.cities:
                label = (
                    f"{city.ville} ({city.code_postal})"
                    if city.code_postal
                    else city.ville
                )
                dist = (
                    f"{city.distance_km:.1f} km"
                    if city.distance_km is not None
                    else "distance inconnue"
                )
                anchor = f"city-{slugify(city.ville)}"
                city_slug = slugify(city.ville)
                city_distance = (
                    city.distance_km
                    if city.distance_km is not None
                    else max_distance_slider
                )
                is_target = city.ville.lower() == self.city_name.lower()
                f.write(
                    f"<section class='city-section' id='{anchor}' "
                    f"data-city='{h(city_slug)}' data-distance='{city_distance:.2f}' "
                    f"data-search='{h(city.ville.lower())}'>\n"
                )
                f.write("<details class='city-details' open>\n")
                f.write(
                    "<summary class='city-summary'>"
                    f"<span class='city-summary__title'>{h(label)}</span>"
                    f"<span class='city-summary__meta'>{dist} · {city.total_clubs} club(s) · "
                    f"{city.total_teams} equipe(s) · {city.total_contacts} contact(s)</span>"
                    "</summary>\n"
                )
                f.write("<div class='city-body'>\n")
                if city.clubs:
                    f.write("<div class='city-clubs'>\n")
                    for idx, club in enumerate(city.clubs, start=1):
                        card_id = (
                            f"club-{slugify(city.ville)}-{slugify(club.nom)}-{idx}"
                        )
                        self._write_html_club_card(
                            f,
                            club,
                            card_id=card_id,
                            city_name=city.ville,
                            city_distance_km=city_distance,
                            salle_anchor_by_signature=salle_anchor_by_signature,
                        )
                    f.write("</div>\n")
                elif is_target:
                    f.write(
                        "<p class='empty-city'>Aucune equipe Pro ou National"
                        f" a <strong>{h(self.city_name)}</strong>."
                        f" Recherche elargie a {self.radius:.0f}&nbsp;km.</p>\n"
                    )
                f.write(
                    "<p class='nav'><a href='#map-section'>&#x2191; Carte</a> · "
                    "<a href='#main-content'>Filtres</a></p>\n"
                )
                f.write("</div>\n</details>\n</section>\n\n")
            f.write("</div>\n\n")

            # Annuaire — all contacts, deduplicated
            self._write_html_annuaire(f)
            self._write_html_salles(f, salle_entries)

            # Footer
            f.write(
                f"<footer>Genere le {h(self.timestamp)}"
                f" par ffbb-api-client-v2</footer>\n"
            )
            f.write("</main>\n\n")

            # --- Leaflet JS + MarkerCluster JS ---
            f.write(
                "<script"
                " src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'"
                " integrity='sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo='"
                " crossorigin=''></script>\n"
                "<script"
                " src='https://unpkg.com/leaflet.markercluster@1.5.3"
                "/dist/leaflet.markercluster.js'"
                " crossorigin=''></script>\n"
            )
            f.write("<script>\n")
            self._write_leaflet_js(f)
            self._write_report_ui_js(f)
            f.write("</script>\n")
            f.write("</body>\n</html>\n")

    def _write_html_club_card(
        self,
        f,
        club: ReportClub,
        *,
        card_id: str,
        city_name: str,
        city_distance_km: float,
        salle_anchor_by_signature: dict[tuple[str, str, str], str],
    ) -> None:
        """Write a single club card with logo, links, teams, contacts."""
        h = _html_escape
        level_tokens = sorted({slugify(t.niveau) for t in club.teams if t.niveau})
        role_tokens: set[str] = set()
        search_tokens = [
            city_name,
            club.nom,
            club.adresse,
            club.mail,
            club.telephone,
            club.salle_nom,
            club.salle_adresse,
        ]
        for contact in club.club_contacts:
            if contact.role:
                role_tokens.add(slugify(contact.role))
                search_tokens.append(contact.role)
            search_tokens.extend(
                [contact.nom, contact.prenom, contact.email, contact.telephone]
            )
        for team in club.teams:
            if team.niveau:
                search_tokens.append(team.niveau)
            if team.division:
                search_tokens.append(team.division)
            if team.next_match_opponent:
                search_tokens.append(team.next_match_opponent)
            if team.next_match_salle_name:
                search_tokens.append(team.next_match_salle_name)
            if team.next_match_salle_address:
                search_tokens.append(team.next_match_salle_address)
            for contact in team.contacts:
                if contact.role:
                    role_tokens.add(slugify(contact.role))
                    search_tokens.append(contact.role)
                search_tokens.extend(
                    [contact.nom, contact.prenom, contact.email, contact.telephone]
                )
        search_blob = " ".join(token for token in search_tokens if token).lower()
        total_contacts = len(club.club_contacts) + sum(
            len(t.contacts) for t in club.teams
        )

        def salle_anchor(name: str, address: str, map_url: str) -> str:
            signature = self._salle_signature(name, address, map_url)
            return salle_anchor_by_signature.get(signature, "")

        f.write(
            f"<article class='club-card' id='{h(card_id)}' "
            f"data-card-id='{h(card_id)}' data-city='{h(slugify(city_name))}' "
            f"data-distance='{city_distance_km:.2f}' "
            f"data-club-name='{h(club.nom.lower())}' "
            f"data-levels='{h(' '.join(level_tokens))}' "
            f"data-roles='{h(' '.join(sorted(role_tokens)))}' "
            f"data-search='{h(search_blob)}' "
            f"data-contact-count='{total_contacts}'>\n"
        )

        # Club header row
        f.write("<div class='club-header'>\n")
        if club.logo_url:
            f.write(
                f"<img class='club-logo' src='{h(club.logo_url)}'"
                f" alt='Logo {h(club.nom)}' loading='lazy' decoding='async'"
                f" onerror=\"this.style.display='none'\">\n"
            )
        else:
            f.write("<span class='club-logo-placeholder'>&#x1F3C0;</span>\n")
        f.write("<div class='club-info'>\n")
        f.write(f"<h3 class='club-name'>{h(club.nom)}</h3>\n")
        if club.adresse:
            map_url = _directions_url(club.lat, club.lng, club.adresse)
            if map_url:
                f.write(
                    f"<p class='address'><a href='{h(map_url)}' target='_blank' "
                    "rel='noopener noreferrer' class='address-link' "
                    "title='Voir sur la carte'>"
                    f"{h(club.adresse)}</a></p>\n"
                )
            else:
                f.write(f"<p class='address'>{h(club.adresse)}</p>\n")
        if club.salle_nom or club.salle_adresse or club.salle_map_url:
            salle_label = self._salle_label(club.salle_nom, club.salle_adresse)
            salle_id = salle_anchor(
                club.salle_nom,
                club.salle_adresse,
                club.salle_map_url,
            )
            if salle_id and salle_label:
                f.write(
                    "<p class='address address--secondary'>Salle club: "
                    f"<a href='#{h(salle_id)}' class='salle-ref-link'>"
                    f"{h(salle_label)}</a></p>\n"
                )
            elif salle_label:
                f.write(
                    "<p class='address address--secondary'>Salle club: "
                    f"{h(salle_label)}</p>\n"
                )
        f.write(
            f"<p class='club-meta'>{h(city_name)} · {city_distance_km:.1f} km · "
            f"{len(club.teams)} equipe(s) · {total_contacts} contact(s)</p>\n"
        )
        f.write("</div>\n</div>\n")

        # Action links row
        links: list[str] = []
        dir_url = _directions_url(club.lat, club.lng, club.adresse)
        if dir_url:
            links.append(
                f"<a href='{h(dir_url)}' target='_blank' rel='noopener noreferrer'"
                f" title='Itineraire Google Maps'"
                f" class='action-link'>&#x1F4CD; Itineraire</a>"
            )
        if club.site_web:
            url = club.site_web
            if not url.startswith("http"):
                url = "https://" + url
            links.append(
                f"<a href='{h(url)}' target='_blank' rel='noopener noreferrer'"
                f" title='Site web du club'"
                f" class='action-link'>&#x1F310; Site web</a>"
            )
        if club.url_ffbb:
            ffbb_url = club.url_ffbb
            if not ffbb_url.startswith("http"):
                ffbb_url = f"{_COMPETITIONS_BASE}{ffbb_url}"
            links.append(
                f"<a href='{h(ffbb_url)}' target='_blank' rel='noopener noreferrer'"
                f" title='Page FFBB'"
                f" class='action-link'>&#x1F3C6; Page FFBB</a>"
            )
        if club.telephone:
            tel_clean = re.sub(r"\D", "", club.telephone)
            links.append(
                f"<a href='tel:{h(tel_clean)}'"
                f" class='action-link'>&#x1F4DE; {h(_format_phone(club.telephone))}</a>"
            )
        if club.mail:
            links.append(
                f"<a href='mailto:{h(club.mail)}'"
                f" class='action-link'>&#x2709; {h(club.mail)}</a>"
            )
        if links:
            f.write("<div class='club-actions'>\n")
            f.write(" ".join(links))
            f.write("\n</div>\n")

        if club.club_contacts:
            club_role_tokens = sorted(
                {
                    slugify(contact.role)
                    for contact in club.club_contacts
                    if contact.role
                }
            )
            f.write(
                "<section class='team team-filterable team--club' "
                f"data-team-level='' data-team-roles='{h(' '.join(club_role_tokens))}'>\n"
            )
            f.write(
                "<div class='team-heading'>"
                "<span class='badge badge-club'>Contacts club</span>"
                f"<span class='team-count'>{len(club.club_contacts)} contact(s)</span>"
                "</div>\n"
            )
            f.write("<div class='team-body'>\n")
            self._write_html_contact_table(
                f,
                club.club_contacts,
                with_refs=True,
                table_id=f"{card_id}-club",
            )
            f.write("</div>\n</section>\n")

        for index, team in enumerate(club.teams, start=1):
            team_role_tokens = sorted(
                {slugify(contact.role) for contact in team.contacts if contact.role}
            )
            team_level = slugify(team.niveau) if team.niveau else ""
            f.write(
                "<section class='team team-filterable' "
                f"data-team-level='{h(team_level)}' "
                f"data-team-roles='{h(' '.join(team_role_tokens))}'>\n"
            )
            f.write("<div class='team-heading'>")
            f.write("<span class='team-label'>Equipe</span>")
            if team.competition_logo_url:
                f.write(
                    f"<img src='{h(team.competition_logo_url)}'"
                    f" alt='{h(team.division or team.niveau)}' class='competition-logo'"
                    f" width='28' height='28' loading='lazy'> "
                )
            niveau_class = _niveau_css_class(team.niveau)
            sexe_badge = "M" if team.sexe.startswith("M") else "F"
            f.write(
                f"<span class='badge {niveau_class}'>{h(team.niveau)}</span>"
                f" <span class='badge badge-sexe'>{sexe_badge}</span>"
            )
            if team.division:
                f.write(f" <span class='badge badge-div'>{h(team.division)}</span>")
            f.write(f"<span class='team-count'>{len(team.contacts)} contact(s)</span>")
            f.write("</div>\n")
            f.write("<div class='team-body'>\n")
            team_meta_items: list[str] = []
            if team.poules:
                team_meta_items.append(
                    "<span class='team-chip team-chip--poule'>"
                    "<span class='team-chip__label'>Poule(s)</span>"
                    f"<span class='team-chip__value'>{h(' / '.join(team.poules))}</span>"
                    "</span>"
                )
            if team.ranking_position is not None and team.ranking_total is not None:
                team_meta_items.append(
                    "<span class='team-chip team-chip--ranking'>"
                    "<span class='team-chip__label'>Classement</span>"
                    "<span class='team-chip__value'>"
                    f"{team.ranking_position} / {team.ranking_total}</span>"
                    "</span>"
                )
            if club.salle_nom or club.salle_adresse or club.salle_map_url:
                salle_club_label = self._salle_label(
                    club.salle_nom,
                    club.salle_adresse,
                )
                salle_club_id = salle_anchor(
                    club.salle_nom,
                    club.salle_adresse,
                    club.salle_map_url,
                )
                if salle_club_label:
                    if salle_club_id:
                        salle_club_value = (
                            f"<a href='#{h(salle_club_id)}' class='team-chip__hall-link'>"
                            f"{h(salle_club_label)}</a>"
                        )
                    else:
                        salle_club_value = h(salle_club_label)
                    team_meta_items.append(
                        "<span class='team-chip team-chip--home'>"
                        "<span class='team-chip__label'>Salle club</span>"
                        f"<span class='team-chip__value'>{salle_club_value}</span>"
                        "</span>"
                    )
            if team.next_match_date and team.next_match_opponent:
                salle_line = ""
                if (
                    team.next_match_salle_name
                    or team.next_match_salle_address
                    or team.next_match_salle_map_url
                ):
                    salle_label = self._salle_label(
                        team.next_match_salle_name,
                        team.next_match_salle_address,
                    )
                    salle_id = salle_anchor(
                        team.next_match_salle_name,
                        team.next_match_salle_address,
                        team.next_match_salle_map_url,
                    )
                    if salle_id and salle_label:
                        salle_line = (
                            "<span class='team-chip__hall'>Lieu match: "
                            f"<a href='#{h(salle_id)}' class='team-chip__hall-link'>"
                            f"{h(salle_label)}</a></span>"
                        )
                    elif salle_label:
                        salle_line = (
                            "<span class='team-chip__hall'>Lieu match: "
                            f"{h(salle_label)}</span>"
                        )
                team_meta_items.append(
                    "<span class='team-chip team-chip--next'>"
                    "<span class='team-chip__label'>Prochain</span>"
                    "<span class='team-chip__next-main'>"
                    f"<span class='team-chip__when'>{h(team.next_match_date)}</span>"
                    "<span class='team-chip__vs'>contre</span>"
                    f"<span class='team-chip__opponent' title='{h(team.next_match_opponent)}'>"
                    f"{h(team.next_match_opponent)}</span>"
                    "</span>"
                    f"{salle_line}"
                    "</span>"
                )
            elif team.next_match_date:
                salle_line = ""
                if (
                    team.next_match_salle_name
                    or team.next_match_salle_address
                    or team.next_match_salle_map_url
                ):
                    salle_label = self._salle_label(
                        team.next_match_salle_name,
                        team.next_match_salle_address,
                    )
                    salle_id = salle_anchor(
                        team.next_match_salle_name,
                        team.next_match_salle_address,
                        team.next_match_salle_map_url,
                    )
                    if salle_id and salle_label:
                        salle_line = (
                            "<span class='team-chip__hall'>Lieu match: "
                            f"<a href='#{h(salle_id)}' class='team-chip__hall-link'>"
                            f"{h(salle_label)}</a></span>"
                        )
                    elif salle_label:
                        salle_line = (
                            "<span class='team-chip__hall'>Lieu match: "
                            f"{h(salle_label)}</span>"
                        )
                team_meta_items.append(
                    "<span class='team-chip team-chip--next'>"
                    "<span class='team-chip__label'>Prochain</span>"
                    "<span class='team-chip__next-main'>"
                    f"<span class='team-chip__when'>{h(team.next_match_date)}</span>"
                    "</span>"
                    f"{salle_line}"
                    "</span>"
                )
            if team_meta_items or team.ranking_url:
                f.write("<div class='team-meta'>")
                if team_meta_items:
                    f.write("".join(team_meta_items))
                if team.ranking_url:
                    f.write(
                        f"<a href='{h(team.ranking_url)}' target='_blank' "
                        "rel='noopener noreferrer' class='team-meta-link'>"
                        "Voir classement &#x2197;</a>"
                    )
                f.write("</div>\n")
            self._write_html_contact_table(
                f,
                team.contacts,
                with_refs=True,
                table_id=f"{card_id}-team-{index}",
            )
            f.write("</div>\n</section>\n")

        f.write("</article>\n")

    @staticmethod
    def _write_html_contact_table(
        f,
        contacts: list[ReportContact],
        *,
        with_refs: bool = False,
        table_id: str | None = None,
    ) -> None:
        h = _html_escape
        rows: list[dict[str, str]] = []
        for contact in contacts:
            nom_full = f"{contact.nom} {contact.prenom}".strip()
            cid = _contact_id(contact)
            nom_cell = h(nom_full)
            if with_refs:
                nom_cell = (
                    f"<a href='#{h(cid)}' class='contact-ref'"
                    f" title='Voir dans l&#39;annuaire'>{h(nom_full)}</a>"
                )
            tel_display = ""
            tel_clean = ""
            if contact.telephone:
                tel_display = _format_phone(contact.telephone)
                tel_clean = re.sub(r"\D", "", contact.telephone)
            rows.append(
                {
                    "cid": cid,
                    "nom": nom_full,
                    "nom_cell": nom_cell,
                    "role": contact.role,
                    "role_class": _role_css_class(contact.role),
                    "role_token": slugify(contact.role),
                    "tel": tel_display,
                    "tel_href": tel_clean,
                    "email": contact.email or "",
                }
            )

        table_dom_id = table_id or "contacts"
        f.write("<div class='contacts-block'>\n")
        f.write(f"<table class='contacts' id='{h(table_dom_id)}'>\n<thead><tr>")
        for col in ["Role", "Nom", "Tel", "Email"]:
            f.write(f"<th>{col}</th>")
        f.write("</tr></thead>\n<tbody>\n")
        for row in rows:
            email_cell = ""
            if row["email"]:
                email_cell = (
                    f"<a href='mailto:{h(row['email'])}'>{h(row['email'])}</a>"
                    f"<button type='button' class='copy-btn copy-btn--inline'"
                    f" data-copy='{h(row['email'])}' "
                    f" aria-label='Copier l email de {h(row['nom'])}'>Copier</button>"
                )
            tel_cell = ""
            if row["tel_href"]:
                tel_cell = (
                    f"<a href='tel:{h(row['tel_href'])}'>{h(row['tel'])}</a>"
                    f"<button type='button' class='copy-btn copy-btn--inline'"
                    f" data-copy='{h(row['tel'])}' "
                    f" aria-label='Copier le telephone de {h(row['nom'])}'>Copier</button>"
                )
            f.write(
                f"<tr data-role='{h(row['role_token'])}'>"
                f"<td><span class='badge {row['role_class']}'>{h(row['role'])}</span></td>"
                f"<td>{row['nom_cell']}</td>"
                f"<td>{tel_cell}</td>"
                f"<td>{email_cell}</td></tr>\n"
            )
        f.write("</tbody></table>\n")
        f.write("<div class='contacts-cards'>\n")
        for row in rows:
            f.write(
                f"<article class='contact-card' data-role='{h(row['role_token'])}' "
                f"data-contact-search='{h(row['nom'].lower())} {h(row['role'].lower())}'>\n"
            )
            f.write(
                f"<p class='contact-card__title'>{row['nom_cell']}</p>"
                f"<p class='contact-card__role'><span class='badge {row['role_class']}'>"
                f"{h(row['role'])}</span></p>\n"
            )
            if row["tel_href"]:
                f.write(
                    "<p class='contact-card__line'><span>Tel</span>"
                    f"<a href='tel:{h(row['tel_href'])}'>{h(row['tel'])}</a>"
                    f"<button type='button' class='copy-btn'"
                    f" data-copy='{h(row['tel'])}'>Copier</button></p>\n"
                )
            if row["email"]:
                f.write(
                    "<p class='contact-card__line'><span>Email</span>"
                    f"<a href='mailto:{h(row['email'])}'>{h(row['email'])}</a>"
                    f"<button type='button' class='copy-btn'"
                    f" data-copy='{h(row['email'])}'>Copier</button></p>\n"
                )
            f.write("</article>\n")
        f.write("</div>\n</div>\n")

    def _write_leaflet_js(self, f) -> None:
        """Write the Leaflet map initialization script."""

        # Collect all club markers
        markers: list[dict] = []
        for city in self.cities:
            for index, club in enumerate(city.clubs, start=1):
                lat = club.lat
                lng = club.lng
                if lat is None or lng is None:
                    continue
                card_id = f"club-{slugify(city.ville)}-{slugify(club.nom)}-{index}"
                dir_url = _directions_url(lat, lng, club.adresse)
                popup = f"<strong>{_html_escape(club.nom)}</strong>"
                if club.adresse:
                    popup += f"<br><em>{_html_escape(club.adresse)}</em>"
                if dir_url:
                    popup += (
                        f"<br><a href='{_html_escape(dir_url)}'"
                        " target='_blank' rel='noopener noreferrer'>Itineraire</a>"
                    )
                popup += (
                    f"<br><a href='#{_html_escape(card_id)}' class='js-open-card' "
                    f"data-card-id='{_html_escape(card_id)}'>Voir la fiche</a>"
                )
                markers.append(
                    {
                        "lat": lat,
                        "lng": lng,
                        "popup": popup,
                        "name": club.nom,
                        "logo_url": club.logo_url,
                        "card_id": card_id,
                    }
                )

        markers_json = json.dumps(markers, ensure_ascii=False)

        f.write(f"""\
(function() {{
      var center = [{self.lat}, {self.lng}];
      var mapEl = document.getElementById('map');
      if (!mapEl || typeof L === 'undefined') {{
        return;
      }}
      var map = L.map('map').setView(center, 8);
      L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 18
      }}).addTo(map);

  // Radius circle
  L.circle(center, {{
    radius: {self.radius * 1000},
    color: '#F26522',
    fillColor: '#F26522',
    fillOpacity: 0.05,
    weight: 2,
    dashArray: '8 4'
  }}).addTo(map);

  function escapeHtml(value) {{
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }}

  function buildClubIcon(markerData) {{
    var safeName = escapeHtml(markerData.name || 'Club');
    var rawLogo = typeof markerData.logo_url === 'string'
      ? markerData.logo_url.trim()
      : '';
    var hasHttpLogo = /^https?:\\/\\//i.test(rawLogo);
    if (hasHttpLogo) {{
      return L.divIcon({{
        className: 'club-marker',
        html: '<div class="club-pin club-pin--logo" title="' + safeName + '">'
          + '<img class="club-pin__img" src="' + escapeHtml(rawLogo) + '"'
          + ' alt="" loading="lazy"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
      }});
    }}

    return L.divIcon({{
      className: 'club-marker',
      html: '<div class="club-pin club-pin--fallback" title="' + safeName + '">'
        + '<span class="club-pin__emoji" aria-hidden="true">&#x1F3C0;</span>'
        + '</div>',
      iconSize: [30, 30],
      iconAnchor: [15, 15],
      popupAnchor: [0, -15]
    }});
  }}

      var clusters = L.markerClusterGroup({{
        maxClusterRadius: 40,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
    iconCreateFunction: function(cluster) {{
      var n = cluster.getChildCount();
      return L.divIcon({{
        html: '<div style="background:#F26522;color:#fff;'
          + 'border-radius:50%;width:32px;height:32px;'
          + 'display:flex;align-items:center;justify-content:center;'
          + 'font-weight:700;font-size:13px;border:2px solid #fff;'
          + 'box-shadow:0 0 6px rgba(0,0,0,0.3)">' + n + '</div>',
        className: 'club-cluster',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      }});
    }}
      }});

      var data = {markers_json};
      var markerEntries = [];
      var markerByCardId = Object.create(null);
      data.forEach(function(m) {{
        var marker = L.marker([m.lat, m.lng], {{icon: buildClubIcon(m)}})
          .bindPopup(m.popup);
        if (m.name) {{
      marker.bindTooltip(escapeHtml(m.name), {{
        direction: 'top',
        offset: [0, -18],
        sticky: true,
            opacity: 0.95
          }});
        }}
        markerEntries.push({{cardId: m.card_id || '', marker: marker}});
        if (m.card_id) {{
          markerByCardId[m.card_id] = marker;
          marker.on('click', function() {{
            document.dispatchEvent(
              new CustomEvent('ffbb:marker-selected', {{
                detail: {{cardId: m.card_id}}
              }})
            );
          }});
        }}
      }});

      function updateClusters(visibleCardIds, preserveView) {{
        var hasFilter = Array.isArray(visibleCardIds);
        var visibleSet = Object.create(null);
        if (hasFilter) {{
          visibleCardIds.forEach(function(cardId) {{
            visibleSet[cardId] = true;
          }});
        }}
        clusters.clearLayers();
        var bounds = L.latLngBounds([center]);
        var visibleCount = 0;
        markerEntries.forEach(function(entry) {{
          var include = !hasFilter || !!visibleSet[entry.cardId];
          if (!include) {{
            return;
          }}
          clusters.addLayer(entry.marker);
          bounds.extend(entry.marker.getLatLng());
          visibleCount += 1;
        }});
        if (!map.hasLayer(clusters)) {{
          map.addLayer(clusters);
        }}
        if (!preserveView && visibleCount > 0) {{
          map.fitBounds(bounds, {{padding: [30, 30], maxZoom: 11}});
        }}
      }}

      updateClusters(null, false);

      window.__ffbbMapBridge = {{
        setVisibleCards: function(cardIds, preserveView) {{
          updateClusters(cardIds, !!preserveView);
        }},
        focusCard: function(cardId, openPopup) {{
          var marker = markerByCardId[cardId];
          if (!marker) {{
            return;
          }}
          map.panTo(marker.getLatLng(), {{animate: true, duration: 0.35}});
          if (openPopup !== false) {{
            marker.openPopup();
          }}
        }}
      }};
    }})();
    """)

    @staticmethod
    def _write_report_ui_js(f) -> None:
        """Write client-side UI interactions (filters, sorting, copy, sync)."""
        f.write("""\
    (function() {
      var searchInput = document.getElementById('ui-search');
      var cityInput = document.getElementById('ui-city');
      var levelInput = document.getElementById('ui-level');
      var roleInput = document.getElementById('ui-role');
      var distanceInput = document.getElementById('ui-distance');
      var distanceValue = document.getElementById('ui-distance-value');
      var sortInput = document.getElementById('ui-sort');
      var resultNode = document.getElementById('ui-results');
      var resetButton = document.getElementById('ui-reset');
      var citiesContainer = document.getElementById('cities-container');
      if (!searchInput || !cityInput || !levelInput || !roleInput || !distanceInput || !citiesContainer) {
        return;
      }

      var citySections = Array.prototype.slice.call(
        document.querySelectorAll('.city-section')
      );
      var clubCards = Array.prototype.slice.call(
        document.querySelectorAll('.club-card')
      );
      var maxDistance = Number(distanceInput.max || distanceInput.value || 0);
      var activeCardId = '';

      function normalize(value) {
        return String(value || '')
          .normalize('NFD')
          .replace(/[\\u0300-\\u036f]/g, '')
          .toLowerCase()
          .trim();
      }

      function parseTokens(raw) {
        return String(raw || '')
          .split(/\\s+/)
          .map(function(token) { return token.trim(); })
          .filter(Boolean);
      }

      function updateDistanceLabel() {
        if (distanceValue) {
          distanceValue.textContent = String(distanceInput.value || '0');
        }
      }

      function sortCitySections(mode) {
        if (!citiesContainer) {
          return;
        }
        var sorted = citySections.slice().sort(function(a, b) {
          if (mode === 'city') {
            return (a.dataset.city || '').localeCompare(b.dataset.city || '', 'fr');
          }
          var da = Number(a.dataset.distance || 9999);
          var db = Number(b.dataset.distance || 9999);
          return da - db;
        });
        sorted.forEach(function(section) {
          citiesContainer.appendChild(section);
        });
      }

      function sortClubCards(mode) {
        Array.prototype.forEach.call(
          document.querySelectorAll('.city-clubs'),
          function(group) {
            var cards = Array.prototype.slice.call(group.querySelectorAll('.club-card'));
            cards.sort(function(a, b) {
              if (mode === 'contacts') {
                var ca = Number(a.dataset.contactCount || 0);
                var cb = Number(b.dataset.contactCount || 0);
                return cb - ca;
              }
              var na = a.dataset.clubName || '';
              var nb = b.dataset.clubName || '';
              return na.localeCompare(nb, 'fr');
            });
            cards.forEach(function(card) {
              group.appendChild(card);
            });
          }
        );
      }

      function applySort() {
        var mode = sortInput ? sortInput.value : 'distance';
        if (mode === 'city') {
          sortCitySections('city');
        } else {
          sortCitySections('distance');
        }
        if (mode === 'club' || mode === 'contacts') {
          sortClubCards(mode);
        }
      }

      function updateCityNavigation() {
        Array.prototype.forEach.call(
          document.querySelectorAll('[data-city-link]'),
          function(item) {
            var sectionId = item.getAttribute('data-city-link');
            if (!sectionId) {
              return;
            }
            var section = document.getElementById(sectionId);
            if (!section) {
              return;
            }
            item.hidden = !!section.hidden;
          }
        );
      }

      function applyTeamFilters(card, levelValue, roleValue) {
        var blocks = Array.prototype.slice.call(
          card.querySelectorAll('.team-filterable')
        );
        if (!blocks.length) {
          return true;
        }
        var hasVisible = false;
        blocks.forEach(function(block) {
          var isClubBlock = block.classList.contains('team--club');
          var levelTokens = parseTokens(block.dataset.teamLevel);
          var roleTokens = parseTokens(block.dataset.teamRoles);
          var levelOk = levelValue === 'all'
            ? true
            : !isClubBlock && levelTokens.indexOf(levelValue) >= 0;
          var roleOk = roleValue === 'all'
            ? true
            : roleTokens.indexOf(roleValue) >= 0;
          var show = levelOk && roleOk;
          block.hidden = !show;
          if (show) {
            hasVisible = true;
          }
        });
        return hasVisible;
      }

      function applyFilters() {
        var term = normalize(searchInput.value);
        var cityValue = cityInput.value || 'all';
        var levelValue = levelInput.value || 'all';
        var roleValue = roleInput.value || 'all';
        var maxDistanceValue = Number(distanceInput.value || maxDistance);
        var visibleCardIds = [];
        var visibleContactCount = 0;

        clubCards.forEach(function(card) {
          var cardSearch = normalize(card.dataset.search);
          var cardCity = card.dataset.city || '';
          var cardDistance = Number(card.dataset.distance || 9999);
          var searchOk = !term || cardSearch.indexOf(term) >= 0;
          var cityOk = cityValue === 'all' || cardCity === cityValue;
          var distanceOk = cardDistance <= maxDistanceValue;
          var teamsOk = applyTeamFilters(card, levelValue, roleValue);
          var visible = searchOk && cityOk && distanceOk && teamsOk;
          card.hidden = !visible;
          if (visible) {
            visibleCardIds.push(card.id);
            visibleContactCount += Number(card.dataset.contactCount || 0);
          }
        });

        citySections.forEach(function(section) {
          var cards = Array.prototype.slice.call(section.querySelectorAll('.club-card'));
          if (cards.length) {
            section.hidden = !cards.some(function(card) { return !card.hidden; });
            return;
          }
          var cityOk = cityValue === 'all' || (section.dataset.city || '') === cityValue;
          var searchOk = !term || normalize(section.dataset.search).indexOf(term) >= 0;
          var distanceOk = Number(section.dataset.distance || 0) <= maxDistanceValue;
          section.hidden = !(cityOk && searchOk && distanceOk && levelValue === 'all' && roleValue === 'all');
        });

        updateCityNavigation();

        if (resultNode) {
          resultNode.textContent = visibleCardIds.length
            + ' club(s) affiche(s) · '
            + visibleContactCount
            + ' contact(s)';
        }
        if (window.__ffbbMapBridge && typeof window.__ffbbMapBridge.setVisibleCards === 'function') {
          window.__ffbbMapBridge.setVisibleCards(visibleCardIds, true);
        }
      }

      function setActiveCard(cardId, options) {
        if (!cardId) {
          return;
        }
        var card = document.getElementById(cardId);
        if (!card || card.hidden) {
          return;
        }
        var opts = options || {};
        if (activeCardId && activeCardId !== cardId) {
          var old = document.getElementById(activeCardId);
          if (old) {
            old.classList.remove('is-highlighted');
          }
        }
        activeCardId = cardId;
        card.classList.add('is-highlighted');
        var cityDetails = card.closest('.city-details');
        if (cityDetails) {
          cityDetails.open = true;
        }
        if (opts.scroll) {
          card.scrollIntoView({behavior: 'smooth', block: 'center'});
        }
        if (
          opts.map !== false
          && window.__ffbbMapBridge
          && typeof window.__ffbbMapBridge.focusCard === 'function'
        ) {
          window.__ffbbMapBridge.focusCard(cardId, opts.openPopup !== false);
        }
      }

      function copyText(value) {
        if (!value) {
          return Promise.resolve(false);
        }
        if (navigator.clipboard && window.isSecureContext) {
          return navigator.clipboard.writeText(value).then(function() { return true; });
        }
        return new Promise(function(resolve) {
          var input = document.createElement('textarea');
          input.value = value;
          input.setAttribute('readonly', '');
          input.style.position = 'absolute';
          input.style.left = '-9999px';
          document.body.appendChild(input);
          input.select();
          try {
            document.execCommand('copy');
            resolve(true);
          } catch (error) {
            resolve(false);
          } finally {
            document.body.removeChild(input);
          }
        });
      }

      clubCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
          setActiveCard(card.id, {scroll: false, openPopup: false});
        });
        card.addEventListener('focusin', function() {
          setActiveCard(card.id, {scroll: false, openPopup: false});
        });
        card.addEventListener('click', function(event) {
          if (event.target.closest('a, button, summary, input, select')) {
            return;
          }
          setActiveCard(card.id, {scroll: false});
        });
      });

      document.addEventListener('ffbb:marker-selected', function(event) {
        var cardId = event.detail && event.detail.cardId;
        if (cardId) {
          setActiveCard(cardId, {scroll: true, map: false, openPopup: false});
        }
      });

      document.addEventListener('click', function(event) {
        var cardLink = event.target.closest('.js-open-card');
        if (cardLink) {
          event.preventDefault();
          var cardId = cardLink.getAttribute('data-card-id');
          setActiveCard(cardId, {scroll: true, map: false, openPopup: false});
          return;
        }
        var copyButton = event.target.closest('.copy-btn');
        if (!copyButton) {
          return;
        }
        var payload = copyButton.getAttribute('data-copy');
          copyText(payload).then(function(ok) {
            var previous = copyButton.textContent;
            copyButton.textContent = ok ? 'Copiee' : 'Erreur';
          setTimeout(function() {
            copyButton.textContent = previous || 'Copier';
          }, 1000);
        });
      });

      [searchInput, cityInput, levelInput, roleInput].forEach(function(input) {
        input.addEventListener('input', applyFilters);
        input.addEventListener('change', applyFilters);
      });

      distanceInput.addEventListener('input', function() {
        updateDistanceLabel();
        applyFilters();
      });

      if (sortInput) {
        sortInput.addEventListener('change', function() {
          applySort();
          applyFilters();
        });
      }

      if (resetButton) {
        resetButton.addEventListener('click', function() {
          searchInput.value = '';
          cityInput.value = 'all';
          levelInput.value = 'all';
          roleInput.value = 'all';
          distanceInput.value = String(maxDistance);
          if (sortInput) {
            sortInput.value = 'distance';
          }
          updateDistanceLabel();
          applySort();
          applyFilters();
        });
      }

      updateDistanceLabel();
      applySort();
      applyFilters();
    })();
    """)

    def _write_html_annuaire(self, f) -> None:
        """Write the 'Annuaire' section with all contacts deduplicated."""
        h = _html_escape

        # Collect all contacts with their context (club, team)
        # Deduplicate by (nom, prenom, telephone, email)
        seen: dict[str, dict] = {}  # cid -> entry
        for city in self.cities:
            for club in city.clubs:
                # Club-level contacts
                for c in club.club_contacts:
                    cid = _contact_id(c)
                    if cid not in seen:
                        seen[cid] = {
                            "contact": c,
                            "mentions": [],
                        }
                    seen[cid]["mentions"].append(f"{club.nom} (contact club)")
                # Team contacts
                for team in club.teams:
                    for c in team.contacts:
                        cid = _contact_id(c)
                        if cid not in seen:
                            seen[cid] = {
                                "contact": c,
                                "mentions": [],
                            }
                        seen[cid]["mentions"].append(f"{club.nom} — {team.label}")

        if not seen:
            return

        # Sort by nom, prenom
        entries = sorted(
            seen.items(),
            key=lambda x: (x[1]["contact"].nom, x[1]["contact"].prenom),
        )

        f.write("<section class='annuaire-section' id='annuaire'>\n")
        f.write(f"<h2>Annuaire des contacts ({len(entries)})</h2>\n")
        f.write(
            "<p class='annuaire-desc'>"
            "Liste complete des contacts sans doublons."
            " Cliquez sur un nom pour revenir au club correspondant."
            "</p>\n"
        )
        f.write("<table class='contacts annuaire-table'>\n")
        f.write("<thead><tr>")
        for col in ["Nom", "Role", "Tel", "Email", "Mentions"]:
            f.write(f"<th>{col}</th>")
        f.write("</tr></thead>\n<tbody>\n")

        for cid, entry in entries:
            c = entry["contact"]
            mentions = entry["mentions"]
            nom_full = f"{c.nom} {c.prenom}".strip()
            email_cell = (
                f"<a href='mailto:{h(c.email)}'>{h(c.email)}</a>" if c.email else ""
            )
            tel_cell = ""
            if c.telephone:
                tel_clean = re.sub(r"\D", "", c.telephone)
                tel_cell = (
                    f"<a href='tel:{h(tel_clean)}'>"
                    f"{h(_format_phone(c.telephone))}</a>"
                )
            role_class = _role_css_class(c.role)
            mentions_html = "<br>".join(h(m) for m in mentions)
            f.write(
                f"<tr id='{h(cid)}'>"
                f"<td><strong>{h(nom_full)}</strong></td>"
                f"<td><span class='badge {role_class}'>"
                f"{h(c.role)}</span></td>"
                f"<td>{tel_cell}</td>"
                f"<td>{email_cell}</td>"
                f"<td class='mentions'>{mentions_html}</td>"
                f"</tr>\n"
            )

        f.write("</tbody></table>\n")
        f.write("<p class='nav'>" "<a href='#map-section'>&#x2191; Carte</a>" "</p>\n")
        f.write("</section>\n\n")

    def _write_html_salles(self, f, salles: list[dict[str, str]]) -> None:
        """Write a deduplicated hall index section at the end of the report."""
        if not salles:
            return
        h = _html_escape
        f.write("<section class='salles-section' id='salles'>\n")
        f.write(f"<h2>Salles referees ({len(salles)})</h2>\n")
        f.write(
            "<p class='annuaire-desc'>"
            "Reference des salles mentionnees dans les clubs et prochains matchs."
            "</p>\n"
        )
        f.write("<ol class='salles-list'>\n")
        for salle in salles:
            f.write(f"<li class='salle-item' id='{h(salle['anchor'])}'>\n")
            f.write("<p class='salle-item__title'>" f"{h(salle['label'])}</p>\n")
            if salle["address"]:
                f.write(f"<p class='salle-item__meta'>{h(salle['address'])}</p>\n")
            if salle["map_url"]:
                f.write(
                    "<p class='salle-item__actions'>"
                    f"<a href='{h(salle['map_url'])}' target='_blank' "
                    "rel='noopener noreferrer'>Ouvrir sur la carte &#x2197;</a>"
                    "</p>\n"
                )
            f.write("</li>\n")
        f.write("</ol>\n")
        f.write(
            "<p class='nav'>"
            "<a href='#main-content'>&#x2191; Haut de page</a>"
            "</p>\n"
        )
        f.write("</section>\n\n")


def _html_escape(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _niveau_css_class(niveau: str) -> str:
    if "Pro" in niveau:
        return "badge-pro"
    if "National" in niveau:
        return "badge-national"
    return "badge-ligue"


def _role_css_class(role: str) -> str:
    r = role.lower()
    if "president" in r:
        return "badge-president"
    if "entraineur" in r or "coach" in r:
        return "badge-coach"
    if "correspondant" in r:
        return "badge-correspondant"
    return "badge-role"


_HTML_CSS = """\
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
:root {
  --bg: #FAFBFC;
  --surface: #FFFFFF;
  --text: #1F2937;
  --muted: #6B7280;
  --border: #E5E7EB;
  --accent: #F26522;
  --accent-dark: #D4540E;
  --accent-light: #FFF4ED;
  --focus: #0EA5E9;
  --radius: 8px;
  --sidebar-w: 220px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
[hidden] { display: none !important; }
html {
  width: 100%;
  overflow-x: hidden;
}
body {
  width: 100%;
  overflow-x: hidden;
  font-family: 'Manrope', 'Segoe UI', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  background:
    radial-gradient(circle at 8% 5%, rgba(242, 101, 34, 0.12), transparent 32%),
    radial-gradient(circle at 90% 0%, rgba(14, 165, 233, 0.08), transparent 28%),
    var(--bg);
}
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0.5rem;
  background: var(--text);
  color: #fff;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  z-index: 999;
}
.skip-link:focus {
  left: 0.75rem;
}
a:focus-visible,
button:focus-visible,
input:focus-visible,
select:focus-visible,
summary:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0; left: 0;
  width: var(--sidebar-w);
  height: 100vh;
  overflow-y: auto;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 1rem 0;
  z-index: 100;
}
.sidebar-title {
  padding: 0 1rem 0.75rem;
  font-weight: 700;
  font-size: 1rem;
  color: var(--accent);
  border-bottom: 2px solid var(--accent);
  margin-bottom: 0.5rem;
}
.sidebar-list {
  list-style: none;
  padding: 0;
}
.sidebar-list li a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.35rem 1rem;
  color: var(--text);
  text-decoration: none;
  font-size: 0.82rem;
  transition: background 0.15s;
}
.sidebar-list li a:hover {
  background: var(--accent-light);
  color: var(--accent-dark);
}
.sidebar-dist {
  font-size: 0.72rem;
  color: var(--muted);
  white-space: nowrap;
}

/* Main content */
.content {
  margin-left: var(--sidebar-w);
  width: calc(100% - var(--sidebar-w));
  max-width: none;
  margin-right: 0;
  padding: 2rem clamp(1rem, 2.5vw, 2.5rem);
}

/* Header */
.hero {
  margin-bottom: 1.15rem;
  padding: 1rem 1.1rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  background:
    linear-gradient(180deg, #FFFFFF 0%, #FFF7F0 100%);
}
.hero-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.9rem;
}
.hero-kicker {
  margin: 0;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  font-weight: 700;
}
h1 {
  font-size: clamp(1.3rem, 2.6vw, 1.65rem);
  margin: 0.2rem 0 0;
  color: var(--accent);
}
.hero-date {
  margin: 0;
  color: var(--muted);
  font-size: 0.78rem;
  white-space: nowrap;
}
.hero-subtitle {
  margin: 0.55rem 0 0.75rem;
  color: #4B5563;
  font-size: 0.88rem;
}
.hero-facts {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
  margin: 0;
  padding: 0;
}
.hero-fact {
  border: 1px solid #F3E6DC;
  border-radius: 8px;
  padding: 0.45rem 0.55rem;
  background: #fff;
}
.hero-fact__label {
  display: block;
  color: var(--muted);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.hero-fact__value {
  display: block;
  margin-top: 0.12rem;
  font-size: 0.85rem;
  color: var(--text);
  font-weight: 600;
}
h2 {
  font-size: 1.2rem;
  margin: 1.5rem 0 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
.visually-hidden {
  position: absolute !important;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Stats */
.summary { margin: 1rem 0 1.5rem; }
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.75rem;
  text-align: center;
}
.stat-val {
  display: block;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent);
}
.stat-label {
  display: block;
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Controls */
.controls {
  margin: 0.65rem 0 0.85rem;
  padding: 0.55rem 0.7rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: #fff;
}
.controls-bar {
  display: flex;
  gap: 0.6rem;
  align-items: center;
  flex-wrap: wrap;
}
.controls-actions {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  margin-left: auto;
}
.controls-advanced {
  margin-top: 0.5rem;
}
.controls-advanced > summary {
  cursor: pointer;
  color: var(--accent-dark);
  font-size: 0.8rem;
  font-weight: 700;
  user-select: none;
  list-style: none;
}
.controls-advanced > summary::-webkit-details-marker { display: none; }
.controls-advanced > summary::before {
  content: "▸";
  margin-right: 0.3rem;
}
.controls-advanced[open] > summary::before { content: "▾"; }
.controls-advanced[open] .controls-grid { margin-top: 0.55rem; }
.controls-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.5rem;
}
.control-field {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.control-field > span {
  color: var(--muted);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.control-field--search {
  flex: 1 1 420px;
  min-width: 220px;
}
.control-field input,
.control-field select {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.32rem 0.45rem;
  font: inherit;
  background: #fff;
  font-size: 0.86rem;
}
.control-field--range input { padding: 0; }
.controls-result {
  font-size: 0.76rem;
  color: var(--muted);
  margin: 0;
  white-space: normal;
}
.control-reset {
  border: 1px solid var(--border);
  background: #FFFAF7;
  color: var(--text);
  border-radius: 6px;
  padding: 0.28rem 0.52rem;
  font-size: 0.78rem;
  line-height: 1.2;
  cursor: pointer;
}
.control-reset:hover { background: var(--accent-light); }

/* Map */
#map {
  height: clamp(280px, 48vh, 520px);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
}
.club-marker {
  background: transparent;
  border: 0;
}
.club-pin {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}
.club-pin--logo { background: #FFFFFF; }
.club-pin--fallback {
  background: linear-gradient(135deg, #F26522, #D4540E);
}
.club-pin__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.club-pin__emoji {
  font-size: 0.95rem;
  line-height: 1;
}
.noscript-msg {
  padding: 2rem;
  text-align: center;
  color: var(--muted);
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

/* Mobile nav */
.mobile-nav {
  display: none;
  margin-bottom: 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.5rem 1rem;
}
.mobile-nav summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--accent);
}
.mobile-nav ul {
  list-style: none;
  padding: 0.5rem 0;
}
.mobile-nav li a {
  display: block;
  padding: 0.3rem 0;
  color: var(--text);
  text-decoration: none;
  font-size: 0.85rem;
}

/* Club card */
.city-section { margin-bottom: 1rem; }
.city-details {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
}
.city-summary {
  list-style: none;
  cursor: pointer;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.6rem;
}
.city-summary__title {
  font-weight: 700;
  color: var(--text);
}
.city-summary__meta {
  font-size: 0.78rem;
  color: var(--muted);
}
.city-body { padding: 0 0.9rem 0.85rem; }
.city-clubs { margin-top: 0.5rem; }
.empty-city {
  background: #FEF3C7;
  border-left: 4px solid #F59E0B;
  border-radius: var(--radius);
  padding: 0.75rem 1rem;
  color: #92400E;
  font-style: italic;
}
.club-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  margin-bottom: 1rem;
  box-shadow: 0 8px 22px rgba(17, 24, 39, 0.04);
  transition: border-color 0.15s, box-shadow 0.2s, transform 0.2s;
}
.club-card:hover {
  border-color: #F7C3A5;
  box-shadow: 0 14px 28px rgba(17, 24, 39, 0.08);
}
.club-card.is-highlighted {
  border-color: var(--focus);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.15), 0 14px 28px rgba(17, 24, 39, 0.09);
  transform: translateY(-1px);
}
.club-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}
.club-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
  border-radius: 4px;
  flex-shrink: 0;
}
.club-logo-placeholder {
  font-size: 1.5rem;
  width: 36px;
  text-align: center;
  flex-shrink: 0;
}
.club-info { flex: 1; min-width: 0; }
.club-name {
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
  color: var(--text);
}
p.address {
  font-size: 0.82rem;
  color: var(--muted);
  font-style: italic;
  margin: 0;
}
.address--secondary {
  margin-top: 0.12rem;
  font-style: normal;
  color: #556170;
}
.address-link {
  color: inherit;
  text-decoration: underline dotted;
  text-underline-offset: 2px;
}
.address-link:hover {
  color: var(--accent-dark);
}
.salle-ref-link {
  color: var(--accent-dark);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.salle-ref-link:hover {
  color: var(--accent);
}
.club-meta {
  margin-top: 0.2rem;
  color: var(--muted);
  font-size: 0.76rem;
}
.club-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.action-link {
  font-size: 0.78rem;
  color: var(--accent-dark);
  text-decoration: none;
  padding: 0.2rem 0.5rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  transition: background 0.15s;
  white-space: nowrap;
}
.action-link:hover {
  background: var(--accent-light);
  text-decoration: none;
}

/* Teams */
.team {
  margin-top: 0.45rem;
  border: 1px solid #F1F5F9;
  border-radius: 8px;
  overflow: clip;
}
.team-heading {
  padding: 0.45rem 0.55rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.4rem;
  background: #FCFCFD;
  border-bottom: 1px solid #F1F5F9;
}
.team-body {
  padding: 0.35rem 0.55rem 0.45rem;
}
.team-count {
  margin-left: auto;
  font-size: 0.72rem;
  color: var(--muted);
  font-weight: 600;
}
.team-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--muted);
  font-weight: 700;
}

/* Badges */
.badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  vertical-align: middle;
}
.badge-pro { background: #FFE8D9; color: #B45309; }
.badge-national { background: #FEE2E2; color: #DC2626; }
.badge-ligue { background: #DBEAFE; color: #2563EB; }
.badge-sexe { background: #F3F4F6; color: #4B5563; }
.badge-div { background: #F3F4F6; color: #6B7280; font-weight: 400; }
.badge-club { background: var(--accent-light); color: var(--accent-dark); }
.badge-president { background: #FEF3C7; color: #92400E; }
.badge-coach { background: #D1FAE5; color: #065F46; }
.badge-correspondant { background: #DBEAFE; color: #1E40AF; }
.badge-role { background: #F3F4F6; color: #4B5563; }
.team-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.4rem;
  margin: 0.35rem 0 0.15rem;
}
.team-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  max-width: 100%;
  border: 1px solid #E2E8F0;
  border-radius: 999px;
  padding: 0.22rem 0.52rem;
  background: #FFFFFF;
  color: #334155;
  font-size: 0.76rem;
}
.team-chip--poule {
  background: #F8FAFC;
  border-color: #E2E8F0;
}
.team-chip--ranking {
  background: #FFF7ED;
  border-color: #FED7AA;
}
.team-chip--home {
  background: #F8FAFC;
  border-color: #CBD5E1;
}
.team-chip--next {
  background: #EFF6FF;
  border-color: #BFDBFE;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 0.16rem 0.42rem;
  align-items: start;
  border-radius: 10px;
  padding: 0.32rem 0.56rem;
}
.team-chip__label {
  font-size: 0.64rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: #64748B;
  font-weight: 700;
}
.team-chip__value,
.team-chip__when {
  font-weight: 600;
  color: #0F172A;
}
.team-chip__vs {
  color: #64748B;
  font-size: 0.72rem;
}
.team-chip__next-main {
  min-width: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.24rem;
}
.team-chip__opponent {
  font-weight: 600;
  color: #0F172A;
  max-width: none;
  white-space: normal;
  overflow: visible;
  text-overflow: clip;
  line-height: 1.3;
}
.team-chip__hall {
  grid-column: 1 / -1;
  font-size: 0.7rem;
  color: #475569;
  line-height: 1.32;
}
.team-chip__hall-link {
  color: var(--accent-dark);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.team-meta-link {
  margin-left: auto;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.24rem 0.58rem;
  background: #FFFFFF;
  font-size: 0.78rem;
  color: var(--accent);
  text-decoration: none;
}
.team-meta-link:hover {
  text-decoration: none;
  background: var(--accent-light);
}
.competition-logo {
  vertical-align: middle;
  margin-right: 0.35rem;
  border-radius: 4px;
}

/* Contact tables */
.contacts-block { margin-top: 0.35rem; }
table.contacts {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  margin-top: 0.4rem;
  margin-bottom: 0.25rem;
}
table.contacts th {
  background: #F9FAFB;
  font-weight: 600;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  padding: 0.35rem 0.6rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
table.contacts td {
  padding: 0.3rem 0.6rem;
  border-bottom: 1px solid #F3F4F6;
  font-size: 0.82rem;
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
}
table.contacts tr:hover { background: #FFFBF5; }
table.contacts a { color: var(--accent-dark); }
.contacts-cards { display: none; }
.contact-card {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: #fff;
  padding: 0.55rem 0.65rem;
  margin-top: 0.5rem;
}
.contact-card__title { font-weight: 700; }
.contact-card__role { margin-top: 0.2rem; }
.contact-card__line {
  margin-top: 0.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  font-size: 0.83rem;
}
.contact-card__line > span {
  color: var(--muted);
  min-width: 44px;
}
.copy-btn {
  border: 1px solid var(--border);
  background: #fff;
  color: var(--text);
  border-radius: 999px;
  padding: 0.1rem 0.45rem;
  font-size: 0.68rem;
  cursor: pointer;
}
.copy-btn:hover { background: var(--accent-light); }
.copy-btn--inline { margin-left: 0.35rem; }

/* Nav links */
p.nav {
  margin-top: 0.5rem;
  font-size: 0.82rem;
  color: var(--muted);
}
p.nav a { color: var(--accent); text-decoration: none; }
p.nav a:hover { text-decoration: underline; }

/* Contact references (links to annuaire) */
a.contact-ref {
  color: var(--accent-dark);
  text-decoration: none;
  border-bottom: 1px dotted var(--accent);
}
a.contact-ref:hover {
  color: var(--accent);
  border-bottom-style: solid;
}

/* Club contacts section (at top of club card) */
.club-contacts-section {
  background: var(--accent-light);
  border-radius: var(--radius);
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
}

/* Sidebar annuaire link */
.sidebar-annuaire {
  margin-top: 0.5rem;
  border-top: 1px solid var(--border);
  padding-top: 0.5rem;
}
.sidebar-annuaire a {
  font-weight: 600;
  color: var(--accent) !important;
}

/* Annuaire section */
.annuaire-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 3px solid var(--accent);
}
.annuaire-desc {
  font-size: 0.85rem;
  color: var(--muted);
  margin-bottom: 1rem;
}
.annuaire-table td.mentions {
  font-size: 0.75rem;
  color: var(--muted);
  max-width: 250px;
}
.annuaire-table tr:target {
  background: var(--accent-light) !important;
  animation: highlight-fade 2s ease-out;
}
.salles-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}
.salles-list {
  margin: 0.75rem 0 0;
  padding-left: 1.15rem;
}
.salle-item {
  margin: 0 0 0.65rem;
  padding: 0.35rem 0.45rem;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  background: #fff;
}
.salle-item__title {
  margin: 0;
  font-weight: 700;
  font-size: 0.88rem;
}
.salle-item__meta {
  margin: 0.15rem 0 0;
  color: var(--muted);
  font-size: 0.8rem;
}
.salle-item__actions {
  margin: 0.18rem 0 0;
  font-size: 0.78rem;
}
.salle-item__actions a {
  color: var(--accent-dark);
}
@keyframes highlight-fade {
  0% { background: #FFD6A5; }
  100% { background: var(--accent-light); }
}

/* Footer */
footer {
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  font-size: 0.78rem;
  color: var(--muted);
  font-style: italic;
}

/* Print */
@media print {
  .sidebar, #map-section, .mobile-nav, p.nav, .club-actions, .controls, .copy-btn { display: none; }
  .content { margin-left: 0; max-width: none; padding: 0; }
  body { font-size: 11px; background: #fff; }
  .club-card { border: 1px solid #ccc; box-shadow: none; break-inside: avoid; }
  .stat { border: 1px solid #ccc; }
  a { color: var(--text); }
  a[href]::after { content: ' (' attr(href) ')'; font-size: 0.7rem; color: #999; }
  a[href^="mailto:"]::after, a[href^="tel:"]::after { content: none; }
}

/* Responsive */
@media (max-width: 1023px) {
  .sidebar { display: none; }
  .content {
    margin-left: 0;
    width: auto;
    max-width: none;
    padding: 1.5rem 1rem;
  }
  .hero-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .controls-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .mobile-nav { display: block; }
}
@media (max-width: 767px) {
  body { font-size: 13px; }
  h1 { font-size: 1.35rem; }
  h2 { font-size: 1.05rem; }
  .hero {
    padding: 0.8rem 0.85rem;
  }
  .hero-main {
    flex-direction: column;
    align-items: flex-start;
  }
  .hero-facts { grid-template-columns: 1fr; }
  .controls {
    margin: 0.34rem 0 0.48rem;
    padding: 0.33rem 0.4rem;
  }
  .controls-bar {
    flex-direction: row;
    align-items: center;
    gap: 0.25rem;
  }
  .control-field--search {
    min-width: 0;
    flex: 1 1 auto;
  }
  .controls-actions {
    display: none;
  }
  .controls-advanced {
    margin-top: 0.2rem;
  }
  .controls-advanced > summary {
    display: inline-flex;
    align-items: center;
    padding: 0.14rem 0.44rem;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: #fff;
    font-size: 0.72rem;
  }
  .controls-advanced[open] .controls-grid { margin-top: 0.35rem; }
  .controls-grid {
    grid-template-columns: 1fr;
    gap: 0.36rem;
  }
  .control-field > span {
    font-size: 0.62rem;
  }
  .control-field input,
  .control-field select {
    font-size: 0.8rem;
    padding: 0.24rem 0.36rem;
  }
  .controls-result {
    font-size: 0.72rem;
  }
  .control-reset {
    font-size: 0.74rem;
    padding: 0.23rem 0.48rem;
  }
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  #map { height: clamp(240px, 44vh, 320px); }
  .club-card { padding: 0.85rem; }
  .club-header { gap: 0.6rem; }
  .club-logo, .club-logo-placeholder { width: 32px; height: 32px; }
  .club-actions { gap: 0.3rem; }
  .action-link { font-size: 0.72rem; }
  .city-summary { flex-direction: column; align-items: flex-start; }
  .city-summary__meta { font-size: 0.74rem; }
  .team-heading {
    gap: 0.28rem;
  }
  .team-label {
    width: 100%;
  }
  .team-meta {
    align-items: stretch;
    gap: 0.3rem;
  }
  .team-chip {
    width: 100%;
    border-radius: 9px;
    padding: 0.3rem 0.45rem;
  }
  .team-chip--next {
    padding: 0.34rem 0.48rem;
  }
  .team-meta-link {
    margin-left: 0;
    width: 100%;
    text-align: center;
  }
  .contacts-block table.contacts { display: none; }
  .contacts-block .contacts-cards { display: block; }
  .annuaire-table td.mentions {
    white-space: normal;
    min-width: 0;
  }
  .annuaire-section {
    overflow-x: auto;
  }
  .annuaire-table {
    min-width: 100%;
  }
}
"""


# ---------------------------------------------------------------------------
# Internal collection types (used during enrichment, before building report)
# ---------------------------------------------------------------------------


@dataclass
class _CityGeo:
    ville: str
    lat: float
    lng: float


@dataclass
class _ClubInfo:
    nom: str
    ville: str
    adresse: str
    code_postal: str
    lat: float | None
    lng: float | None
    site_web: str
    url_ffbb: str
    logo_url: str
    telephone: str
    mail: str
    salle_nom: str
    salle_adresse: str
    salle_map_url: str


@dataclass
class _CollectedRow:
    ville: str
    adresse_club: str
    club: str
    code_postal: str
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
    engagement_id: int | None
    engagement_updated_at: datetime | None
    ranking_url: str
    competition_logo_url: str
    ranking_position: int | None
    ranking_total: int | None
    next_match_at: datetime | None
    next_match_date: str
    next_match_opponent: str
    next_match_salle_name: str
    next_match_salle_address: str
    next_match_salle_map_url: str


@dataclass
class _TeamCompetitionSnapshot:
    ranking_position: int | None = None
    ranking_total: int | None = None
    next_match_date: datetime | None = None
    next_match_opponent: str = ""
    next_match_salle_name: str = ""
    next_match_salle_address: str = ""
    next_match_salle_map_url: str = ""


# ---------------------------------------------------------------------------
# Engagement classification helpers
# ---------------------------------------------------------------------------


def _is_senior(hit: EngagementsHit) -> bool:
    """Return True if the engagement is a senior category (or unparsable)."""
    if hit.categorie and hit.categorie.code:
        age = hit.categorie.code.age_group
        return age is None or age == AgeGroup.SENIOR
    return True


def classify_engagement_level(hit: EngagementsHit) -> str | None:
    """Return the level string (PRO/NATIONAL) or None.

    Classification is based solely on the engagement's echelon, NOT
    on the ``club_pro`` flag (which marks the *club*, not the team).
    """
    if not _is_senior(hit):
        return None
    if hit.niveau and hit.niveau.code:
        echelon = hit.niveau.code.echelon
        if echelon in PRO_ECHELONS:
            return "PRO"
        if echelon in NATIONAL_ECHELONS:
            return "NATIONAL"
    return None


def _extract_division(hit: EngagementsHit) -> str:
    if hit.niveau and hit.niveau.code:
        return str(hit.niveau.code)
    return ""


def _extract_poule(hit: EngagementsHit) -> str:
    if hit.id_poule and hit.id_poule.nom:
        return hit.id_poule.nom
    return ""


def _extract_ranking_url(hit: EngagementsHit) -> str:
    if hit.competitions_url:
        return f"{_COMPETITIONS_BASE}{hit.competitions_url}"
    return ""


def _extract_competition_logo_url(hit: EngagementsHit) -> str:
    """Extract the official competition logo URL from nested hit data.

    Path: hit.id_competition.type_competition_generique.logo.id → UUID
    """
    comp = hit.id_competition
    if comp and comp.type_competition_generique:
        logo = comp.type_competition_generique.logo
        if logo and logo.id:
            return f"{_ASSET_BASE}{logo.id}"
    return ""


def _extract_club_page_url(hit: EngagementsHit) -> str:
    """Derive the club page URL from the team's competitions_url.

    ``competitions_url`` has the form
    ``/ligues/.../clubs/XXX/equipes/YYY``.  Stripping ``/equipes/YYY``
    gives the club page path.
    """
    if hit.competitions_url:
        path = hit.competitions_url
        idx = path.find("/equipes/")
        if idx != -1:
            return f"{_COMPETITIONS_BASE}{path[:idx]}"
        # No /equipes/ suffix — return the path as-is (could be a club page)
        return f"{_COMPETITIONS_BASE}{path}"
    return ""


def _parse_match_datetime(value: object) -> datetime | None:
    """Parse an API match date into ``datetime`` when possible."""
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if not raw:
        return None
    # Directus often sends UTC suffix "Z" which fromisoformat does not accept.
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _extract_engagement_id(value: object) -> str:
    """Extract engagement ID from nested match payload objects."""
    if isinstance(value, dict):
        candidate = value.get("id")
        return str(candidate) if candidate is not None else ""
    if value is None:
        return ""
    if hasattr(value, "id"):
        candidate = getattr(value, "id", None)
        return str(candidate) if candidate is not None else ""
    return str(value)


def _format_next_match_date(value: datetime | None) -> str:
    """Format next-match date using a compact, context-aware style."""
    if value is None:
        return ""
    local_value = _as_local_naive(value)
    if local_value is None:
        return ""

    now = datetime.now()
    today = now.date()
    target = local_value.date()
    delta_days = (target - today).days

    show_time = not (local_value.hour == 0 and local_value.minute == 0)

    def time_part() -> str:
        if not show_time:
            return ""
        if local_value.minute == 0:
            return f"{local_value:%H}h"
        return f"{local_value:%Hh%M}"

    weekday_fr = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche",
    ]
    month_fr = [
        "janv",
        "fev",
        "mars",
        "avr",
        "mai",
        "juin",
        "juil",
        "aout",
        "sept",
        "oct",
        "nov",
        "dec",
    ]

    if delta_days == 0:
        base = "Aujourd'hui"
    elif delta_days == 1:
        base = "Demain"
    elif delta_days == 2:
        base = "Apres-demain"
    elif 0 < delta_days <= 6:
        base = weekday_fr[target.weekday()]
    elif -6 <= delta_days < 0:
        base = f"{weekday_fr[target.weekday()]} {target.day}"
    elif target.year == today.year:
        base = f"{target.day} {month_fr[target.month - 1]}"
    else:
        base = f"{target.day} {month_fr[target.month - 1]} {target.year}"

    match_time = time_part()
    if match_time:
        return f"{base} {match_time}"
    return base


def _compose_salle_address(
    *,
    adresse: str,
    complement: str,
    code_postal: str,
    ville: str,
) -> str:
    parts = [p for p in [adresse, complement, code_postal, ville] if p]
    return ", ".join(parts)


def _extract_salle_details(salle) -> tuple[str, str, str]:
    """Return salle label/address/map link from a salle payload."""
    if salle is None:
        return "", "", ""

    label = (salle.libelle or salle.libelle2 or "").strip()
    carto = salle.cartographie
    carto_address = (carto.adresse if carto else "") or ""
    carto_cp = (carto.code_postal if carto else "") or ""
    carto_city = (carto.ville if carto else "") or ""
    address = _compose_salle_address(
        adresse=(salle.adresse or carto_address or "").strip(),
        complement=(salle.adresseComplement or "").strip(),
        code_postal=carto_cp.strip(),
        ville=carto_city.strip(),
    )
    map_url = _directions_url(
        carto.latitude if carto else None,
        carto.longitude if carto else None,
        address,
    )
    return label, address, map_url


def _resolve_salle_details(
    client: FFBBAPIClientV2,
    salle_id: int,
    cache: dict[int, tuple[str, str, str]],
) -> tuple[str, str, str]:
    """Fetch salle details once and reuse through local cache."""
    if salle_id in cache:
        return cache[salle_id]
    try:
        details = _extract_salle_details(client.get_salle(salle_id))
    except FFBBApiError:
        details = ("", "", "")
    cache[salle_id] = details
    return details


def _team_name_key(value: str) -> str:
    """Normalize team name for resilient matching across payload sources."""
    return "name:" + slugify(value or "")


def _is_better_match_candidate(
    candidate_date: datetime | None,
    current_date: datetime | None,
) -> bool:
    """Return True when candidate should replace current next-match selection."""
    if candidate_date is None:
        return False
    if current_date is None:
        return True
    now = datetime.now()

    if candidate_date.tzinfo is not None:
        candidate_date = candidate_date.astimezone().replace(tzinfo=None)
    if current_date.tzinfo is not None:
        current_date = current_date.astimezone().replace(tzinfo=None)

    candidate_future = candidate_date >= now
    current_future = current_date >= now
    if candidate_future and not current_future:
        return True
    if current_future and not candidate_future:
        return False
    return candidate_date < current_date


def _as_local_naive(value: datetime | None) -> datetime | None:
    """Convert datetime to local naive value for safe comparisons."""
    if value is None:
        return None
    if value.tzinfo is not None:
        return value.astimezone().replace(tzinfo=None)
    return value


def _select_effective_team_rows(rows: list[_CollectedRow]) -> list[_CollectedRow]:
    """Keep only rows belonging to the most likely effective engagement."""
    groups: dict[int | None, list[_CollectedRow]] = defaultdict(list)
    for row in rows:
        groups[row.engagement_id].append(row)

    if len(groups) <= 1:
        return rows

    now = datetime.now()

    def score(
        group_rows: list[_CollectedRow],
    ) -> tuple[float, float, float, float, float]:
        next_dates = [
            dt
            for dt in (_as_local_naive(r.next_match_at) for r in group_rows)
            if dt is not None
        ]
        future_dates = [dt for dt in next_dates if dt >= now]
        next_future = min(future_dates) if future_dates else None
        if next_future is not None:
            has_future = 1.0
            proximity_score = -(next_future - now).total_seconds()
        else:
            has_future = 0.0
            proximity_score = float("-inf")

        updates = [
            dt
            for dt in (_as_local_naive(r.engagement_updated_at) for r in group_rows)
            if dt is not None
        ]
        update_score = max((dt.timestamp() for dt in updates), default=float("-inf"))
        ranking_score = (
            1.0 if any(r.ranking_position is not None for r in group_rows) else 0.0
        )
        engagement_id = group_rows[0].engagement_id
        engagement_score = float(engagement_id) if engagement_id is not None else -1.0
        return (
            has_future,
            proximity_score,
            update_score,
            ranking_score,
            engagement_score,
        )

    selected = max(groups.values(), key=score)
    return selected


def _load_poule_snapshots(
    client: FFBBAPIClientV2,
    poule_id: int,
    salle_cache: dict[int, tuple[str, str, str]] | None = None,
) -> dict[str, _TeamCompetitionSnapshot]:
    """Load ranking + next match info for all teams in one poule."""
    snapshots: dict[str, _TeamCompetitionSnapshot] = {}
    if salle_cache is None:
        salle_cache = {}

    engagements = client.list_engagements(
        limit=250,
        filter_criteria=f'{{"idPoule":{{"_eq":{poule_id}}}}}',
    )
    rank_total = len(engagements) if engagements else 0
    for engagement in engagements:
        if not engagement.id:
            continue
        snapshot = snapshots.get(str(engagement.id), _TeamCompetitionSnapshot())
        if engagement.position is not None and engagement.position > 0:
            snapshot.ranking_position = engagement.position
        if rank_total > 1:
            snapshot.ranking_total = rank_total

        snapshots[str(engagement.id)] = snapshot
        for name in (engagement.nom, engagement.nomEquipe, engagement.nomUsuel):
            if name:
                snapshots[_team_name_key(name)] = snapshot

    matches = client.list_rencontres(
        limit=500,
        filter_criteria=f'{{"idPoule":{{"_eq":{poule_id}}}}}',
        sort=["date_rencontre"],
    )
    for match in matches:
        if match.joue is True:
            continue

        date_value = match.date_rencontre or match.date
        nom1 = match.nomEquipe1 or ""
        nom2 = match.nomEquipe2 or ""
        id1 = str(match.idEngagementEquipe1) if match.idEngagementEquipe1 else ""
        id2 = str(match.idEngagementEquipe2) if match.idEngagementEquipe2 else ""
        key1 = id1 or (_team_name_key(nom1) if nom1 else "")
        key2 = id2 or (_team_name_key(nom2) if nom2 else "")

        if key1:
            current = snapshots.get(key1, _TeamCompetitionSnapshot())
            if _is_better_match_candidate(date_value, current.next_match_date):
                current.next_match_date = date_value
                current.next_match_opponent = nom2
                current.next_match_salle_name = ""
                current.next_match_salle_address = ""
                current.next_match_salle_map_url = ""
                if match.salle:
                    (
                        current.next_match_salle_name,
                        current.next_match_salle_address,
                        current.next_match_salle_map_url,
                    ) = _resolve_salle_details(client, match.salle, salle_cache)
            snapshots[key1] = current
            if id1:
                snapshots[id1] = current
            if nom1:
                snapshots[_team_name_key(nom1)] = current
        if key2:
            current = snapshots.get(key2, _TeamCompetitionSnapshot())
            if _is_better_match_candidate(date_value, current.next_match_date):
                current.next_match_date = date_value
                current.next_match_opponent = nom1
                current.next_match_salle_name = ""
                current.next_match_salle_address = ""
                current.next_match_salle_map_url = ""
                if match.salle:
                    (
                        current.next_match_salle_name,
                        current.next_match_salle_address,
                        current.next_match_salle_map_url,
                    ) = _resolve_salle_details(client, match.salle, salle_cache)
            snapshots[key2] = current
            if id2:
                snapshots[id2] = current
            if nom2:
                snapshots[_team_name_key(nom2)] = current

    return snapshots


def _extract_next_match_from_engagement(
    engagement: GetEngagementsResponse,
    engagement_id: int,
) -> tuple[datetime | None, str]:
    """Best-effort next-match extraction from engagement payload."""
    selected_date: datetime | None = None
    selected_opponent = ""
    own_id = str(engagement_id)

    match_rows = []
    match_rows.extend(
        engagement.rencontres_domiciles
        if isinstance(engagement.rencontres_domiciles, list)
        else []
    )
    match_rows.extend(
        engagement.rencontres_exterieur
        if isinstance(engagement.rencontres_exterieur, list)
        else []
    )

    for row in match_rows:
        if not isinstance(row, dict):
            continue
        joue = row.get("joue")
        if joue is True:
            continue
        date_value = _parse_match_datetime(
            row.get("date_rencontre") or row.get("dateRencontre")
        )
        id1 = _extract_engagement_id(
            row.get("idEngagementEquipe1") or row.get("id_engagement_equipe1")
        )
        id2 = _extract_engagement_id(
            row.get("idEngagementEquipe2") or row.get("id_engagement_equipe2")
        )
        nom1 = row.get("nomEquipe1") or row.get("nom_equipe1") or ""
        nom2 = row.get("nomEquipe2") or row.get("nom_equipe2") or ""

        if own_id == id1:
            opponent = str(nom2) if nom2 else ""
        elif own_id == id2:
            opponent = str(nom1) if nom1 else ""
        else:
            opponent = str(nom2 or nom1) if (nom2 or nom1) else ""

        if _is_better_match_candidate(date_value, selected_date):
            selected_date = date_value
            selected_opponent = opponent

    return selected_date, selected_opponent


def _extract_club_info(
    organisme: GetOrganismeResponse,
    hit_logo_fallback: str = "",
    hit_club_url_fallback: str = "",
    salle_nom: str = "",
    salle_adresse: str = "",
    salle_map_url: str = "",
) -> _ClubInfo:
    nom = organisme.nom or ""
    ville = ""
    adresse = ""
    code_postal = ""
    lat: float | None = None
    lng: float | None = None
    carto = organisme.cartographie
    if carto:
        ville = carto.ville or ""
        code_postal = carto.code_postal or ""
        parts = [p for p in [carto.adresse, carto.code_postal, carto.ville] if p]
        adresse = ", ".join(parts)
        lat = carto.latitude
        lng = carto.longitude

    site_web = organisme.url_site_web or ""
    url_ffbb = organisme.url_competition or hit_club_url_fallback
    logo_url = ""
    if organisme.logo:
        logo_url = f"{_ASSET_BASE}{organisme.logo}"
    elif hit_logo_fallback:
        logo_url = hit_logo_fallback
    telephone = organisme.telephone or ""
    mail = organisme.mail or ""

    return _ClubInfo(
        nom=nom,
        ville=ville,
        adresse=adresse,
        code_postal=code_postal,
        lat=lat,
        lng=lng,
        site_web=site_web,
        url_ffbb=url_ffbb,
        logo_url=logo_url,
        telephone=telephone,
        mail=mail,
        salle_nom=salle_nom,
        salle_adresse=salle_adresse,
        salle_map_url=salle_map_url,
    )


def _contact_to_row(
    contact: ContactInfo,
    ville: str,
    adresse_club: str,
    club: str,
    code_postal: str,
    niveau: str,
    division: str,
    poule: str,
    sexe: str,
    engagement_id: int | None,
    engagement_updated_at: datetime | None,
    ranking_url: str,
    competition_logo_url: str,
    ranking_position: int | None,
    ranking_total: int | None,
    next_match_at: datetime | None,
    next_match_date: str,
    next_match_opponent: str,
    next_match_salle_name: str,
    next_match_salle_address: str,
    next_match_salle_map_url: str,
) -> _CollectedRow:
    return _CollectedRow(
        ville=ville,
        adresse_club=adresse_club,
        club=club,
        code_postal=code_postal,
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
        engagement_id=engagement_id,
        engagement_updated_at=engagement_updated_at,
        ranking_url=ranking_url,
        competition_logo_url=competition_logo_url,
        ranking_position=ranking_position,
        ranking_total=ranking_total,
        next_match_at=next_match_at,
        next_match_date=next_match_date,
        next_match_opponent=next_match_opponent,
        next_match_salle_name=next_match_salle_name,
        next_match_salle_address=next_match_salle_address,
        next_match_salle_map_url=next_match_salle_map_url,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract senior Elite/National basketball contacts near a point"
    )
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lng", type=float, required=True, help="Longitude")
    parser.add_argument(
        "--city-name",
        type=str,
        required=True,
        help="Name of the search point (used in filenames and report title)",
    )
    parser.add_argument(
        "--radius", type=float, default=100.0, help="Radius in km (default: 100)"
    )
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument(
        "--dry-run", action="store_true", help="Print planned actions without API calls"
    )
    args = parser.parse_args()

    slug = args.city_name.lower().replace(" ", "_")

    if args.dry_run:
        logger.info(
            "[dry-run] %s (%.5f, %.5f), rayon %.1f km → %s/%s_senior_contacts.{md,csv,html}",
            args.city_name,
            args.lat,
            args.lng,
            args.radius,
            args.out_dir,
            slug,
        )
        return

    logger.info(
        "[1/5] Recherche geo engagements: %s (%.5f, %.5f), rayon %.1f km",
        args.city_name,
        args.lat,
        args.lng,
        args.radius,
    )

    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )

    # Step 1: Geo search engagements via Meilisearch
    result = client.search_engagements_by_geo(
        lat=args.lat,
        lng=args.lng,
        radius_km=args.radius,
        limit=5000,
    )
    if not result or not result.hits:
        logger.warning("Aucun engagement trouve autour de %s.", args.city_name)
        return

    logger.info("[1/5] %d engagements bruts trouves", len(result.hits))

    # Step 2: Filter by level (PRO, NATIONAL, LIGUE_FEMININE — senior only)
    qualified: list[tuple[EngagementsHit, str]] = []
    level_counts: dict[str, int] = defaultdict(int)
    for hit in result.hits:
        level = classify_engagement_level(hit)
        if level:
            qualified.append((hit, level))
            level_counts[level] += 1

    if not qualified:
        logger.warning("[2/5] Aucun engagement Pro/National/Ligue Feminine.")
        return

    breakdown = ", ".join(
        f"{NIVEAU_LABELS.get(k, k)}: {v}" for k, v in sorted(level_counts.items())
    )
    logger.info(
        "[2/5] %d engagements qualifies / %d (%s)",
        len(qualified),
        len(result.hits),
        breakdown,
    )

    # Step 3: Enrich via facade contact methods
    club_cache: dict[int, _ClubInfo | None] = {}
    poule_cache: dict[int, dict[str, _TeamCompetitionSnapshot]] = {}
    salle_cache: dict[int, tuple[str, str, str]] = {}
    rows_by_key: dict[tuple[object, ...], _CollectedRow] = {}
    city_geo: dict[str, _CityGeo] = {}
    api_calls = 0
    errors = 0

    for i, (hit, level) in enumerate(qualified, 1):
        sexe = hit.sexe or ""
        club_name = hit.nom_club or hit.nom_organisme or ""
        ville = ""
        adresse_club = ""
        code_postal = ""

        niveau = NIVEAU_LABELS.get(level, level)
        division = _extract_division(hit)
        poule = _extract_poule(hit)
        ranking_url = _extract_ranking_url(hit)
        competition_logo_url = _extract_competition_logo_url(hit)
        ranking_position: int | None = None
        ranking_total: int | None = None
        engagement_updated_at: datetime | None = None
        next_match_at: datetime | None = None
        next_match_date = ""
        next_match_opponent = ""
        next_match_salle_name = ""
        next_match_salle_address = ""
        next_match_salle_map_url = ""
        team_lookup_name = hit.nom or hit.nom_equipe or ""

        # Logo fallback from Meilisearch hit
        hit_logo = hit.logo or hit.thumbnail or ""

        try:
            eng_id = int(hit.id) if hit.id else None
        except (ValueError, TypeError):
            eng_id = None

        contacts: list[ContactInfo] = []

        if eng_id:
            engagement_poule_id: int | None = None
            try:
                api_calls += 1
                eng_contacts = client.get_engagement_contacts(eng_id)
                if eng_contacts:
                    engagement_updated_at = (
                        eng_contacts.engagement.date_updated
                        or eng_contacts.engagement.date_created
                    )
                    if (
                        ranking_position is None
                        and eng_contacts.engagement.position is not None
                        and eng_contacts.engagement.position > 0
                    ):
                        ranking_position = eng_contacts.engagement.position
                    if ranking_total is None and isinstance(
                        eng_contacts.engagement.classement, list
                    ):
                        classement_count = len(eng_contacts.engagement.classement)
                        ranking_total = (
                            classement_count if classement_count > 1 else None
                        )
                    if not next_match_date:
                        fallback_date, fallback_opponent = (
                            _extract_next_match_from_engagement(
                                eng_contacts.engagement,
                                eng_id,
                            )
                        )
                        if fallback_date:
                            next_match_at = fallback_date
                            next_match_date = _format_next_match_date(fallback_date)
                            next_match_opponent = fallback_opponent
                    if eng_contacts.engagement.idPoule is not None:
                        engagement_poule_id = eng_contacts.engagement.idPoule
                    for c in [
                        eng_contacts.correspondant,
                        eng_contacts.entraineur,
                        eng_contacts.entraineur_adjoint,
                    ]:
                        if c:
                            contacts.append(c)

                    org_id = eng_contacts.engagement.idOrganisme
                    if org_id is not None:
                        if org_id not in club_cache:
                            try:
                                api_calls += 1
                                club_contacts = client.get_club_contacts(org_id)
                                if club_contacts:
                                    salle_nom = ""
                                    salle_adresse = ""
                                    salle_map_url = ""
                                    if club_contacts.organisme.salle is not None:
                                        (
                                            salle_nom,
                                            salle_adresse,
                                            salle_map_url,
                                        ) = _resolve_salle_details(
                                            client,
                                            club_contacts.organisme.salle,
                                            salle_cache,
                                        )
                                    info = _extract_club_info(
                                        club_contacts.organisme,
                                        hit_logo_fallback=hit_logo,
                                        hit_club_url_fallback=_extract_club_page_url(
                                            hit
                                        ),
                                        salle_nom=salle_nom,
                                        salle_adresse=salle_adresse,
                                        salle_map_url=salle_map_url,
                                    )
                                    club_cache[org_id] = info
                                    if club_contacts.club_contact:
                                        contacts.append(club_contacts.club_contact)
                                    contacts.extend(club_contacts.membres)
                                else:
                                    club_cache[org_id] = None
                            except FFBBApiError as e:
                                errors += 1
                                logger.debug("Erreur club org_id=%s: %s", org_id, e)
                                club_cache[org_id] = None

                        cached = club_cache.get(org_id)
                        if cached:
                            club_name = cached.nom or club_name
                            ville = cached.ville
                            adresse_club = cached.adresse
                            code_postal = cached.code_postal

                            if (
                                ville
                                and ville not in city_geo
                                and cached.lat is not None
                                and cached.lng is not None
                            ):
                                city_geo[ville] = _CityGeo(
                                    ville=ville,
                                    lat=cached.lat,
                                    lng=cached.lng,
                                )
            except FFBBApiError as e:
                errors += 1
                logger.debug("Erreur engagement id=%s: %s", eng_id, e)

            poule_id: int | None = None
            try:
                if hit.id_poule and hit.id_poule.id:
                    poule_id = int(hit.id_poule.id)
            except (TypeError, ValueError):
                poule_id = None
            if poule_id is None and engagement_poule_id is not None:
                poule_id = engagement_poule_id

            if poule_id is not None:
                if poule_id not in poule_cache:
                    try:
                        api_calls += 1
                        poule_cache[poule_id] = _load_poule_snapshots(
                            client,
                            poule_id,
                            salle_cache=salle_cache,
                        )
                    except FFBBApiError as e:
                        errors += 1
                        logger.debug("Erreur poule id=%s: %s", poule_id, e)
                        poule_cache[poule_id] = {}

                snapshot_lookup = poule_cache.get(poule_id, {})
                snapshot = snapshot_lookup.get(str(eng_id))
                if not snapshot and team_lookup_name:
                    snapshot = snapshot_lookup.get(_team_name_key(team_lookup_name))
                if snapshot:
                    ranking_position = snapshot.ranking_position
                    ranking_total = snapshot.ranking_total
                    next_match_at = snapshot.next_match_date
                    next_match_date = _format_next_match_date(snapshot.next_match_date)
                    next_match_opponent = snapshot.next_match_opponent
                    next_match_salle_name = snapshot.next_match_salle_name
                    next_match_salle_address = snapshot.next_match_salle_address
                    next_match_salle_map_url = snapshot.next_match_salle_map_url

        if i % 10 == 0 or i == len(qualified):
            logger.info(
                "[3/5] Enrichissement: %d/%d engagements, %d clubs en cache,"
                " %d appels API",
                i,
                len(qualified),
                len(club_cache),
                api_calls,
            )

        # Fallback geo from Meilisearch hit
        if ville and ville not in city_geo and hit.geo:
            if hit.geo.lat is not None and hit.geo.lng is not None:
                city_geo[ville] = _CityGeo(
                    ville=ville,
                    lat=hit.geo.lat,
                    lng=hit.geo.lng,
                )

        for contact in contacts:
            is_team_contact = "get_organisme" not in contact.source
            engagement_key = eng_id if is_team_contact else None
            key = (
                ville,
                club_name,
                niveau,
                division,
                sexe,
                engagement_key,
                contact.titre,
                contact.nom,
                contact.prenom,
                contact.telephone,
                contact.email,
            )
            if key in rows_by_key:
                rows_by_key[key].poules.append(poule)
                row = rows_by_key[key]
                if (
                    row.engagement_updated_at is None
                    and engagement_updated_at is not None
                ):
                    row.engagement_updated_at = engagement_updated_at
                if row.ranking_position is None and ranking_position is not None:
                    row.ranking_position = ranking_position
                if row.ranking_total is None and ranking_total is not None:
                    row.ranking_total = ranking_total
                if row.next_match_at is None and next_match_at is not None:
                    row.next_match_at = next_match_at
                if not row.next_match_date and next_match_date:
                    row.next_match_date = next_match_date
                if not row.next_match_opponent and next_match_opponent:
                    row.next_match_opponent = next_match_opponent
                if not row.next_match_salle_name and next_match_salle_name:
                    row.next_match_salle_name = next_match_salle_name
                if not row.next_match_salle_address and next_match_salle_address:
                    row.next_match_salle_address = next_match_salle_address
                if not row.next_match_salle_map_url and next_match_salle_map_url:
                    row.next_match_salle_map_url = next_match_salle_map_url
            else:
                rows_by_key[key] = _contact_to_row(
                    contact,
                    ville,
                    adresse_club,
                    club_name,
                    code_postal,
                    niveau,
                    division,
                    poule,
                    sexe,
                    engagement_key,
                    engagement_updated_at,
                    ranking_url,
                    competition_logo_url,
                    ranking_position,
                    ranking_total,
                    next_match_at,
                    next_match_date,
                    next_match_opponent,
                    next_match_salle_name,
                    next_match_salle_address,
                    next_match_salle_map_url,
                )

    all_rows = list(rows_by_key.values())

    if errors:
        logger.warning("[3/5] %d erreurs API ignorees (details en DEBUG)", errors)

    # Step 4: Compute distances
    city_distances: dict[str, float] = {}
    for v, geo in city_geo.items():
        city_distances[v] = haversine_km(args.lat, args.lng, geo.lat, geo.lng)

    city_postcodes: dict[str, str] = {}
    for row in all_rows:
        if row.ville and row.code_postal and row.ville not in city_postcodes:
            city_postcodes[row.ville] = row.code_postal

    cities_with_geo = len(city_distances)
    cities_without = len({r.ville for r in all_rows if r.ville}) - cities_with_geo
    logger.info(
        "[4/5] Distances calculees: %d villes geoloc, %d sans coordonnees",
        cities_with_geo,
        max(0, cities_without),
    )

    # Build club_infos dict keyed by club name for report
    club_infos: dict[str, _ClubInfo] = {}
    for info in club_cache.values():
        if info:
            club_infos[info.nom] = info

    # Step 5: Build report and export
    report = ContactReport.build(
        city_name=args.city_name,
        lat=args.lat,
        lng=args.lng,
        radius=args.radius,
        rows=all_rows,
        city_distances=city_distances,
        city_postcodes=city_postcodes,
        club_infos=club_infos,
        city_geo=city_geo,
    )

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{slug}_senior_contacts.md"
    csv_path = out_dir / f"{slug}_senior_contacts.csv"
    html_path = out_dir / f"{slug}_senior_contacts.html"

    report.to_markdown(md_path)
    report.to_csv(csv_path)
    report.to_html(html_path)

    logger.info(
        "[5/5] %d contacts, %d clubs, %d villes → %s, %s, %s",
        report.total_contacts,
        report.total_clubs,
        report.total_cities,
        md_path,
        csv_path,
        html_path,
    )


if __name__ == "__main__":
    main()
