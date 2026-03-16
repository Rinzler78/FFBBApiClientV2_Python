#!/usr/bin/env python3
"""Extract basketball contacts near a city (coordinates resolved automatically).

Uses Meilisearch geo-search on engagements, then enriches via facade
contact methods (get_engagement_contacts, get_club_contacts).
Produces a hierarchical Markdown report sorted by distance, a CSV export,
and a professional HTML report with an interactive Leaflet/OSM map.

Usage:
    python examples/extract_contacts.py --city-name Lille
    python examples/extract_contacts.py --city-name Paris --radius 50
    python examples/extract_contacts.py --city-name Lyon --echelon NATIONAL DEPARTEMENT
    python examples/extract_contacts.py --city-name Lille --sexe MASCULINE --age-group SENIOR VETERAN
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import os
import re
import time
import unicodedata
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager
from ffbb_api_client_v2.directus_ffbb.config import API_FFBB_BASE_URL, ENDPOINT_ASSETS
from ffbb_api_client_v2.directus_ffbb.models.get_engagements_response import (
    GetEngagementsResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_entraineurs_response import (
    GetEntraineursResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.exceptions import FFBBApiError
from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_facet_distribution import (
    EngagementsFacetDistribution,
)
from ffbb_api_client_v2.meilisearch_ffbb.models.engagements_hit import EngagementsHit
from ffbb_api_client_v2.models.age_group_enum import AgeGroupEnum
from ffbb_api_client_v2.models.categorie_code import CategorieCode
from ffbb_api_client_v2.models.contact_info import ContactInfo
from ffbb_api_client_v2.models.echelon_enum import EchelonEnum
from ffbb_api_client_v2.models.sexe_enum import SexeEnum

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("ffbb_api_client_v2.utils.converter_utils").setLevel(logging.ERROR)

# Echelons considered pro-level (top-tier competitions)
PRO_ECHELONS: frozenset[EchelonEnum] = frozenset(
    {EchelonEnum.PRO, EchelonEnum.LIGUE_FEMININE, EchelonEnum.BASKET_FAUTEUIL}
)

# Echelons considered national-level
NATIONAL_ECHELONS: frozenset[EchelonEnum] = frozenset({EchelonEnum.NATIONAL})

# All echelons we accept
ACCEPTED_ECHELONS: frozenset[EchelonEnum] = PRO_ECHELONS | NATIONAL_ECHELONS

# Display labels and sort priority, derived from the sets above
NIVEAU_LABELS = {
    "PRO": "Pro",
    "NATIONAL": "National",
    "PRE_NATIONAL": "Pre-National",
    "REGIONAL": "Regional",
    "PRE_REGIONAL": "Pre-Regional",
    "DEPARTEMENTAL": "Departemental",
    "FEDERAL": "Federal",
    "EXCELLENCE": "Excellence",
    "ASSOCIATION_REGIONALE": "Association Regionale",
    "ASSOCIATION_DEPARTEMENTALE": "Association Departementale",
    "OTHER": "Autre",
}
NIVEAU_PRIORITY = {
    "Pro": 0,
    "National": 1,
    "Pre-National": 2,
    "Excellence": 3,
    "Regional": 4,
    "Pre-Regional": 5,
    "Federal": 6,
    "Departemental": 7,
    "Association Regionale": 8,
    "Autre": 9,
}

# Map EchelonEnum enum members to classification labels
_ECHELON_TO_LABEL: dict[EchelonEnum, str] = {
    EchelonEnum.PRO: "PRO",
    EchelonEnum.LIGUE_FEMININE: "PRO",
    EchelonEnum.BASKET_FAUTEUIL: "PRO",
    EchelonEnum.NATIONAL: "NATIONAL",
    EchelonEnum.PRE_NATIONAL: "PRE_NATIONAL",
    EchelonEnum.EXCELLENCE: "EXCELLENCE",
    EchelonEnum.REGION: "REGIONAL",
    EchelonEnum.PRE_REGIONAL: "PRE_REGIONAL",
    EchelonEnum.FEDERAL: "FEDERAL",
    EchelonEnum.DEPARTEMENT: "DEPARTEMENTAL",
    EchelonEnum.ASSOCIATION_REGIONALE: "ASSOCIATION_REGIONALE",
    EchelonEnum.ASSOCIATION_DEPARTEMENTALE: "ASSOCIATION_DEPARTEMENTALE",
}

_MATCH_TYPE_LABELS: dict[str, str] = {
    "COUPE": "Coupe",
    "DIV": "Championnat",
    "PLAT": "Plateau",
}

_COMPETITIONS_BASE = "https://competitions.ffbb.com"
_ASSET_BASE = f"{API_FFBB_BASE_URL}{ENDPOINT_ASSETS}"


# ---------------------------------------------------------------------------
# Pre-compiled regex patterns (avoid recompilation per call)
# ---------------------------------------------------------------------------
_RE_INVALID_CHARS = re.compile(r"[^\w\s-]")
_RE_SPACES_DASHES = re.compile(r"[-\s]+")
_RE_NON_DIGITS = re.compile(r"\D")

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


_MATCH_TYPE_CSS: dict[str, str] = {
    "COUPE": "team-chip--next-coupe",
    "PLAT": "team-chip--next-plateau",
}


def _next_match_label(match_type: str) -> str:
    """Return a human-readable label for the next match chip."""
    suffix = _MATCH_TYPE_LABELS.get(match_type)
    if suffix:
        return f"Prochain ({suffix})"
    return "Prochain"


def _next_match_css(match_type: str) -> str:
    """Return extra CSS class for the next-match chip based on match type."""
    return _MATCH_TYPE_CSS.get(match_type, "")


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
    text = _RE_INVALID_CHARS.sub("", text.lower())
    return _RE_SPACES_DASHES.sub("-", text).strip("-")


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
    digits = _RE_NON_DIGITS.sub("", raw)
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
    next_match_type: str
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

    # Active filters (None = all accepted)
    filter_echelons: frozenset[EchelonEnum] | None = None
    filter_age_groups: frozenset[AgeGroupEnum] | None = None
    filter_sexes: frozenset[SexeEnum] | None = None

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
        """Unique contacts count (deduplicated by identity), cached."""
        cached = getattr(self, "_cached_total_contacts", None)
        if cached is not None:
            return cached
        seen: set[str] = set()
        for city in self.cities:
            for club in city.clubs:
                for c in club.club_contacts:
                    seen.add(_contact_id(c))
                for team in club.teams:
                    for c in team.contacts:
                        seen.add(_contact_id(c))
        object.__setattr__(self, "_cached_total_contacts", len(seen))
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
    # Build helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_team_report(
        sexe: str,
        niveau: str,
        division: str,
        t_rows: list[_CollectedRow],
    ) -> ReportTeam:
        """Build a ReportTeam from a group of collected rows for the same team."""
        effective_rows = _select_effective_team_rows(t_rows)
        poules = sorted({p for r in effective_rows for p in r.poules if p})
        ranking_url = ""
        competition_logo_url = ""
        ranking_position: int | None = None
        ranking_total: int | None = None
        next_match_date = ""
        next_match_opponent = ""
        next_match_type = ""
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
                next_match_type = r.next_match_type
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
        return ReportTeam(
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
            next_match_type=next_match_type,
            next_match_salle_name=next_match_salle_name,
            next_match_salle_address=next_match_salle_address,
            next_match_salle_map_url=next_match_salle_map_url,
            contacts=contacts,
        )

    @staticmethod
    def _build_club_report(
        club_name: str,
        club_rows: list[_CollectedRow],
        club_infos: dict[str, _ClubInfo],
    ) -> ReportClub:
        """Build a ReportClub from its collected rows and optional club info."""
        adresse = club_rows[0].adresse_club if club_rows else ""
        ci = club_infos.get(club_name)

        club_contact_rows = [r for r in club_rows if "get_organisme" in r.source]
        team_rows = [r for r in club_rows if "get_organisme" not in r.source]

        team_groups: dict[tuple[str, str, str], list[_CollectedRow]] = defaultdict(list)
        for r in team_rows:
            team_groups[(r.sexe, r.niveau, r.division)].append(r)

        report_teams = [
            ContactReport._build_team_report(sexe, niveau, division, t_rows)
            for (sexe, niveau, division), t_rows in sorted(
                team_groups.items(),
                key=lambda item: (
                    NIVEAU_PRIORITY.get(item[0][1], 99),
                    item[0][2],
                    item[0][0],
                ),
            )
        ]
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
        return ReportClub(
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
        *,
        filter_echelons: frozenset[EchelonEnum] | None = None,
        filter_age_groups: frozenset[AgeGroupEnum] | None = None,
        filter_sexes: frozenset[SexeEnum] | None = None,
    ) -> ContactReport:
        """Build a hierarchical report from flat collected rows."""

        # Group: ville -> club
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
            geo = city_geo.get(ville)
            report_clubs = [
                ContactReport._build_club_report(club_name, club_rows, club_infos)
                for club_name, club_rows in sorted(ville_clubs[ville].items())
            ]
            report_cities.append(
                ReportCity(
                    ville=ville,
                    code_postal=city_postcodes.get(ville, ""),
                    distance_km=city_distances.get(ville),
                    lat=geo.lat if geo else None,
                    lng=geo.lng if geo else None,
                    clubs=report_clubs,
                )
            )

        # Ensure the target city always appears (even with 0 matching teams)
        if not any(c.ville.lower() == city_name.lower() for c in report_cities):
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
            filter_echelons=filter_echelons,
            filter_age_groups=filter_age_groups,
            filter_sexes=filter_sexes,
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

    @staticmethod
    def _format_filter(values: frozenset | None, default: str) -> str:
        if values is None:
            return default
        return ", ".join(sorted(v.name for v in values))

    def _write_md_header(self, f) -> None:
        f.write(f"# Contacts Basketball Senior — {self.city_name}\n\n")
        f.write("### Recherche\n\n")
        f.write("| Parametre | Valeur |\n")
        f.write("|:----------|:-------|\n")
        f.write(f"| Ville | **{self.city_name}** |\n")
        f.write(f"| Position | {self.lat:.4f}, {self.lng:.4f} |\n")
        f.write(f"| Rayon | {self.radius:.0f} km |\n")
        f.write(f"| Echelons | {self._format_filter(self.filter_echelons, 'Tous')} |\n")
        f.write(f"| SexeEnum | {self._format_filter(self.filter_sexes, 'Tous')} |\n")
        f.write(
            f"| Tranches d'ages | {self._format_filter(self.filter_age_groups, 'Toutes')} |\n\n"
        )
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
                f"Aucune equipe qualifiee a **{self.city_name}**. "
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
                    f"*Aucune equipe qualifiee a **{_md_escape(city.ville)}**."
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
            "NiveauEnum",
            "Division",
            "Poule",
            "SexeEnum",
            "Role",
            "Nom",
            "Prenom",
            "Telephone",
            "Email",
            "SourceEnum",
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

    @property
    def all_roles(self) -> list[str]:
        """Sorted unique roles across all contacts, cached."""
        cached = getattr(self, "_cached_all_roles", None)
        if cached is not None:
            return cached
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
        result = sorted(role_set, key=str.casefold)
        object.__setattr__(self, "_cached_all_roles", result)
        return result

    def _write_html_head_and_sidebar(
        self,
        f,
        salle_entries: list,
    ) -> None:
        """Write <head>, skip-link, and desktop sidebar nav."""
        h = _html_escape
        f.write("<!DOCTYPE html>\n<html lang='fr'>\n<head>\n")
        f.write("<meta charset='utf-8'>\n")
        f.write(
            "<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
        )
        f.write(f"<title>Liste de contacts — {h(self.city_name)}</title>\n")
        f.write(
            "<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'"
            " integrity='sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=' crossorigin=''/>\n"
            "<link rel='stylesheet' href='https://unpkg.com/leaflet.markercluster@1.5.3"
            "/dist/MarkerCluster.css' crossorigin=''/>\n"
            "<link rel='stylesheet' href='https://unpkg.com/leaflet.markercluster@1.5.3"
            "/dist/MarkerCluster.Default.css' crossorigin=''/>\n"
        )
        f.write(f"<style>\n{_HTML_CSS}</style>\n</head>\n<body>\n")
        f.write(
            "<a class='skip-link' href='#main-content'>Aller au contenu principal</a>\n"
        )
        f.write("<nav class='sidebar' id='sidebar'>\n")
        f.write(f"<div class='sidebar-title'>{h(self.city_name)}</div>\n")
        f.write("<ul class='sidebar-list'>\n")
        for city in self.cities:
            anchor = f"city-{slugify(city.ville)}"
            dist = f"{city.distance_km:.0f}" if city.distance_km is not None else "?"
            city_label = (
                f"{city.ville} ({city.code_postal})" if city.code_postal else city.ville
            )
            f.write(
                f"<li data-city-link='{h(anchor)}'><a href='#{anchor}'>"
                f"{h(city_label)}<span class='sidebar-dist'>{dist} km</span></a></li>\n"
            )
        f.write(
            "<li class='sidebar-annuaire'><a href='#annuaire'>&#x1F4D6; Annuaire</a></li>\n"
        )
        if salle_entries:
            f.write(
                "<li class='sidebar-annuaire'><a href='#salles'>&#x1F4CD; Salles</a></li>\n"
            )
        f.write("</ul>\n</nav>\n\n")

    def _write_html_top_grid(
        self,
        f,
        role_options: list[str],
        max_distance_slider: int,
        salle_entries: list,
    ) -> None:
        """Write the top grid: left column (hero, stats, controls) + right column (map)."""
        h = _html_escape
        f.write("<div class='top-grid'>\n<div class='top-grid__left'>\n")
        # Hero header
        f.write(
            "<header class='hero'>\n<div class='hero-main'>\n<div>\n"
            "<p class='hero-kicker'>Recherche FFBB</p>\n"
            "<h1>Liste de contacts</h1>\n</div>\n"
            f"<p class='hero-date'>{h(self.timestamp)}</p>\n</div>\n"
            "<p class='hero-subtitle'>Extraction des clubs et contacts dans un rayon "
            "personnalise autour de la ville de recherche.</p>\n"
            "<ul class='hero-facts'>\n"
        )
        for label, value in [
            ("Ville", self.city_name),
            ("Rayon", f"{self.radius:.0f} km"),
            ("Position", f"{self.lat:.4f}, {self.lng:.4f}"),
            ("Echelons", self._format_filter(self.filter_echelons, "Tous")),
            ("Tranches d'age", self._format_filter(self.filter_age_groups, "Toutes")),
            ("SexeEnum", self._format_filter(self.filter_sexes, "Tous")),
        ]:
            f.write(
                "<li class='hero-fact'>"
                f"<span class='hero-fact__label'>{h(label)}</span>"
                f"<span class='hero-fact__value'>{h(value)}</span></li>\n"
            )
        f.write("</ul>\n</header>\n\n")
        # Stats
        f.write("<section class='summary'>\n<div class='stat-grid'>\n")
        for label, val in [
            ("Villes", self.total_cities),
            ("Clubs", self.total_clubs),
            ("Equipes", self.total_teams),
            ("Contacts", self.total_contacts),
        ]:
            f.write(
                f"<div class='stat'><span class='stat-val'>{val}</span>"
                f"<span class='stat-label'>{label}</span></div>\n"
            )
        f.write("</div>\n</section>\n\n")
        # Filter controls
        f.write(
            "<section class='controls' aria-labelledby='controls-title'>\n"
            "<h2 id='controls-title' class='visually-hidden'>Recherche et filtres</h2>\n"
            "<div class='controls-bar'>\n"
            "<label class='control-field control-field--search' for='ui-search'>"
            "<span>Recherche</span>"
            "<input id='ui-search' type='search' placeholder='Club, ville, contact, email...' "
            "autocomplete='off'></label>\n"
            "<div class='controls-actions'>\n"
            f"<p class='controls-result' id='ui-results'>{self.total_clubs} clubs affiches</p>\n"
            "<button type='button' id='ui-reset' class='control-reset'>Reinitialiser</button>\n"
            "</div>\n</div>\n"
            "<details class='controls-advanced'>\n<summary>Filtres avances</summary>\n"
            "<div class='controls-grid'>\n"
        )
        f.write(
            "<label class='control-field' for='ui-city'><span>Ville</span><select id='ui-city'>"
        )
        f.write("<option value='all'>Toutes les villes</option>")
        for city in self.cities:
            f.write(
                f"<option value='{h(slugify(city.ville))}'>{h(city.ville)}</option>"
            )
        f.write(
            "</select></label>\n"
            "<label class='control-field' for='ui-level'><span>NiveauEnum</span>"
            "<select id='ui-level'><option value='all'>Tous les niveaux</option>"
            "<option value='pro'>Pro</option><option value='national'>National</option>"
            "</select></label>\n"
            "<label class='control-field' for='ui-role'><span>Role</span><select id='ui-role'>"
            "<option value='all'>Tous les roles</option>"
        )
        for role in role_options:
            f.write(f"<option value='{h(slugify(role))}'>{h(role)}</option>")
        f.write(
            "</select></label>\n"
            "<label class='control-field control-field--range' for='ui-distance'>"
            f"<span>Distance max: <strong id='ui-distance-value'>{max_distance_slider}</strong> km</span>"
            f"<input id='ui-distance' type='range' min='0' max='{max_distance_slider}' "
            f"value='{max_distance_slider}' step='1'></label>\n"
            "<label class='control-field' for='ui-sort'><span>Tri</span><select id='ui-sort'>"
            "<option value='distance'>Distance</option><option value='city'>Ville (A-Z)</option>"
            "<option value='club'>Club (A-Z)</option><option value='contacts'>Nb contacts</option>"
            "</select></label>\n"
            "</div>\n</details>\n</section>\n</div>\n"  # end .top-grid__left
        )
        # Map
        f.write(
            "<section id='map-section' class='top-grid__right'>\n"
            "<div id='map' aria-label='Carte des clubs'></div>\n"
            "<noscript><p class='noscript-msg'>Activez JavaScript pour afficher la carte interactive."
            "</p></noscript>\n</section>\n</div>\n\n"  # end .top-grid
        )

    def _write_html_mobile_nav(self, f, salle_entries: list) -> None:
        """Write mobile navigation details block."""
        h = _html_escape
        f.write(
            f"<details class='mobile-nav'>\n<summary>Navigation villes ({self.total_cities})</summary>\n<ul>\n"
        )
        for city in self.cities:
            anchor = f"city-{slugify(city.ville)}"
            dist = f"{city.distance_km:.0f} km" if city.distance_km is not None else "?"
            city_label = (
                f"{city.ville} ({city.code_postal})" if city.code_postal else city.ville
            )
            f.write(
                f"<li data-city-link='{h(anchor)}'><a href='#{anchor}'>{h(city_label)} — {dist}</a></li>\n"
            )
        f.write("<li><a href='#annuaire'>&#x1F4D6; Annuaire des contacts</a></li>\n")
        if salle_entries:
            f.write("<li><a href='#salles'>&#x1F4CD; Salles</a></li>\n")
        f.write("</ul>\n</details>\n\n")

    def _write_html_cities_container(
        self,
        f,
        max_distance_slider: int,
        salle_anchor_by_signature: dict[tuple[str, str, str], str],
    ) -> None:
        """Write all city sections with club cards."""
        h = _html_escape
        f.write("<div id='cities-container'>\n")
        for city in self.cities:
            label = (
                f"{city.ville} ({city.code_postal})" if city.code_postal else city.ville
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
                "<details class='city-details' open>\n"
                "<summary class='city-summary'>"
                f"<span class='city-summary__title'>{h(label)}</span>"
                f"<span class='city-summary__meta'>{dist} · {city.total_clubs} club(s) · "
                f"{city.total_teams} equipe(s) · {city.total_contacts} contact(s)</span>"
                "</summary>\n<div class='city-body'>\n"
            )
            if city.clubs:
                f.write("<div class='city-clubs'>\n")
                for idx, club in enumerate(city.clubs, start=1):
                    card_id = f"club-{slugify(city.ville)}-{slugify(club.nom)}-{idx}"
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
                    f"<p class='empty-city'>Aucune equipe qualifiee a <strong>{h(self.city_name)}</strong>."
                    f" Recherche elargie a {self.radius:.0f}&nbsp;km.</p>\n"
                )
            f.write(
                "<p class='nav'><a href='#map-section'>&#x2191; Carte</a> · "
                "<a href='#main-content'>Filtres</a></p>\n"
                "</div>\n</details>\n</section>\n\n"
            )
        f.write("</div>\n\n")

    def to_html(self, path: Path) -> None:
        """Write a professional HTML report with interactive Leaflet map."""
        role_options = self.all_roles
        max_city_distance = max(
            (city.distance_km for city in self.cities if city.distance_km is not None),
            default=self.radius,
        )
        max_distance_slider = max(
            5, int(math.ceil(max(max_city_distance, self.radius)))
        )
        salle_entries, salle_anchor_by_signature = self._collect_salles()

        with path.open("w", encoding="utf-8") as f:
            self._write_html_head_and_sidebar(f, salle_entries)
            f.write("<main class='content' id='main-content'>\n")
            self._write_html_top_grid(
                f, role_options, max_distance_slider, salle_entries
            )
            self._write_html_mobile_nav(f, salle_entries)
            self._write_html_cities_container(
                f, max_distance_slider, salle_anchor_by_signature
            )
            self._write_html_annuaire(f)
            self._write_html_salles(f, salle_entries)
            h = _html_escape
            f.write(
                f"<footer>Genere le {h(self.timestamp)} par ffbb-api-client-v2</footer>\n"
                "</main>\n\n"
                "<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'"
                " integrity='sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=' crossorigin=''></script>\n"
                "<script src='https://unpkg.com/leaflet.markercluster@1.5.3"
                "/dist/leaflet.markercluster.js' crossorigin=''></script>\n"
                "<script>\n"
            )
            self._write_leaflet_js(f)
            self._write_report_ui_js(f)
            f.write("</script>\n</body>\n</html>\n")

    @staticmethod
    def _build_club_card_search_data(
        club: ReportClub,
        city_name: str,
    ) -> tuple[list[str], set[str], str, int]:
        """Build search tokens, role tokens, search blob, and total contact count for a club card."""
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
            for attr in (
                "niveau",
                "division",
                "next_match_opponent",
                "next_match_salle_name",
                "next_match_salle_address",
            ):
                val = getattr(team, attr, "")
                if val:
                    search_tokens.append(val)
            for contact in team.contacts:
                if contact.role:
                    role_tokens.add(slugify(contact.role))
                    search_tokens.append(contact.role)
                search_tokens.extend(
                    [contact.nom, contact.prenom, contact.email, contact.telephone]
                )
        search_blob = " ".join(t for t in search_tokens if t).lower()
        total_contacts = len(club.club_contacts) + sum(
            len(t.contacts) for t in club.teams
        )
        return level_tokens, role_tokens, search_blob, total_contacts

    def _write_club_header_row(
        self,
        f,
        club: ReportClub,
        city_name: str,
        city_distance_km: float,
        total_contacts: int,
        salle_anchor_fn: Any,
    ) -> None:
        """Write the club header row: logo + address + meta."""
        h = _html_escape
        f.write("<div class='club-header'>\n")
        if club.logo_url:
            f.write(
                f"<img class='club-logo' src='{h(club.logo_url)}' alt='Logo {h(club.nom)}'"
                f" loading='lazy' decoding='async' onerror=\"this.style.display='none'\">\n"
            )
        else:
            f.write("<span class='club-logo-placeholder'>&#x1F3C0;</span>\n")
        f.write(f"<div class='club-info'>\n<h3 class='club-name'>{h(club.nom)}</h3>\n")
        if club.adresse:
            map_url = _directions_url(club.lat, club.lng, club.adresse)
            if map_url:
                f.write(
                    f"<p class='address'><a href='{h(map_url)}' target='_blank' "
                    f"rel='noopener noreferrer' class='address-link' title='Voir sur la carte'>"
                    f"{h(club.adresse)}</a></p>\n"
                )
            else:
                f.write(f"<p class='address'>{h(club.adresse)}</p>\n")
        if club.salle_nom or club.salle_adresse or club.salle_map_url:
            salle_label = self._salle_label(club.salle_nom, club.salle_adresse)
            salle_id = salle_anchor_fn(
                club.salle_nom, club.salle_adresse, club.salle_map_url
            )
            if salle_id and salle_label:
                f.write(
                    f"<p class='address address--secondary'>Salle club: "
                    f"<a href='#{h(salle_id)}' class='salle-ref-link'>{h(salle_label)}</a></p>\n"
                )
            elif salle_label:
                f.write(
                    f"<p class='address address--secondary'>Salle club: {h(salle_label)}</p>\n"
                )
        f.write(
            f"<p class='club-meta'>{h(city_name)} · {city_distance_km:.1f} km · "
            f"{len(club.teams)} equipe(s) · {total_contacts} contact(s)</p>\n"
        )
        f.write("</div>\n</div>\n")

    @staticmethod
    def _write_club_action_links(f, club: ReportClub) -> None:
        """Write the action links row (directions, website, FFBB, phone, email)."""
        h = _html_escape
        links: list[str] = []
        dir_url = _directions_url(club.lat, club.lng, club.adresse)
        if dir_url:
            links.append(
                f"<a href='{h(dir_url)}' target='_blank' rel='noopener noreferrer'"
                f" title='Itineraire Google Maps' class='action-link'>&#x1F4CD; Itineraire</a>"
            )
        if club.site_web:
            url = (
                club.site_web
                if club.site_web.startswith("http")
                else "https://" + club.site_web
            )
            links.append(
                f"<a href='{h(url)}' target='_blank' rel='noopener noreferrer'"
                f" title='Site web du club' class='action-link'>&#x1F310; Site web</a>"
            )
        if club.url_ffbb:
            ffbb = (
                club.url_ffbb
                if club.url_ffbb.startswith("http")
                else f"{_COMPETITIONS_BASE}{club.url_ffbb}"
            )
            links.append(
                f"<a href='{h(ffbb)}' target='_blank' rel='noopener noreferrer'"
                f" title='Page FFBB' class='action-link'>&#x1F3C6; Page FFBB</a>"
            )
        if club.telephone:
            tel_clean = re.sub(r"\D", "", club.telephone)
            links.append(
                f"<a href='tel:{h(tel_clean)}' class='action-link'>"
                f"&#x1F4DE; {h(_format_phone(club.telephone))}</a>"
            )
        if club.mail:
            links.append(
                f"<a href='mailto:{h(club.mail)}' class='action-link'>&#x2709; {h(club.mail)}</a>"
            )
        if links:
            f.write("<div class='club-actions'>\n" + " ".join(links) + "\n</div>\n")

    def _write_club_team_section(
        self,
        f,
        team: ReportTeam,
        index: int,
        card_id: str,
        salle_anchor_fn: Any,
    ) -> None:
        """Write a single team section within a club card."""
        h = _html_escape
        team_role_tokens = sorted({slugify(c.role) for c in team.contacts if c.role})
        team_level = slugify(team.niveau) if team.niveau else ""
        sexe_cls = "team--masculin" if team.sexe.startswith("M") else "team--feminin"
        f.write(
            f"<section class='team team-filterable {sexe_cls}' "
            f"data-team-level='{h(team_level)}' data-team-roles='{h(' '.join(team_role_tokens))}'>\n"
            "<div class='team-heading'><span class='team-label'>Equipe</span>"
        )
        if team.competition_logo_url:
            f.write(
                f"<img src='{h(team.competition_logo_url)}' alt='{h(team.division or team.niveau)}'"
                f" class='competition-logo' width='28' height='28' loading='lazy'> "
            )
        niveau_class = _niveau_css_class(team.niveau)
        sexe_badge = "M" if team.sexe.startswith("M") else "F"
        f.write(
            f"<span class='badge {niveau_class}'>{h(team.niveau)}</span>"
            f" <span class='badge badge-sexe'>{sexe_badge}</span>"
        )
        if team.division:
            f.write(f" <span class='badge badge-div'>{h(team.division)}</span>")
        f.write(
            f"<span class='team-count'>{len(team.contacts)} contact(s)</span></div>\n<div class='team-body'>\n"
        )
        # Meta chips
        team_meta_items: list[str] = []
        if team.poules:
            team_meta_items.append(
                "<span class='team-chip team-chip--poule'>"
                f"<span class='team-chip__label'>Poule(s)</span>"
                f"<span class='team-chip__value'>{h(' / '.join(team.poules))}</span></span>"
            )
        if team.ranking_position is not None and team.ranking_total is not None:
            team_meta_items.append(
                "<span class='team-chip team-chip--ranking'>"
                f"<span class='team-chip__label'>Classement</span>"
                f"<span class='team-chip__value'>{team.ranking_position} / {team.ranking_total}</span></span>"
            )
        if team.next_match_date:
            match_type_label = _next_match_label(team.next_match_type)
            chip_classes = "team-chip team-chip--next"
            match_css = _next_match_css(team.next_match_type)
            if match_css:
                chip_classes += f" {match_css}"
            salle_line = ""
            if (
                team.next_match_salle_name
                or team.next_match_salle_address
                or team.next_match_salle_map_url
            ):
                salle_label = self._salle_label(
                    team.next_match_salle_name, team.next_match_salle_address
                )
                salle_id = salle_anchor_fn(
                    team.next_match_salle_name,
                    team.next_match_salle_address,
                    team.next_match_salle_map_url,
                )
                if salle_id and salle_label:
                    salle_line = (
                        f"<span class='team-chip__hall'>Lieu match: "
                        f"<a href='#{h(salle_id)}' class='team-chip__hall-link'>{h(salle_label)}</a></span>"
                    )
                elif salle_label:
                    salle_line = f"<span class='team-chip__hall'>Lieu match: {h(salle_label)}</span>"
            opponent_html = ""
            if team.next_match_opponent:
                opponent_html = (
                    f"<span class='team-chip__vs'>contre</span>"
                    f"<span class='team-chip__opponent' title='{h(team.next_match_opponent)}'>"
                    f"{h(team.next_match_opponent)}</span>"
                )
            team_meta_items.append(
                f"<span class='{chip_classes}'>"
                f"<span class='team-chip__label'>{h(match_type_label)}</span>"
                f"<span class='team-chip__next-main'><span class='team-chip__when'>{h(team.next_match_date)}</span>"
                f"{opponent_html}</span>{salle_line}</span>"
            )
        if team_meta_items or team.ranking_url:
            f.write("<div class='team-meta'>")
            if team_meta_items:
                f.write("".join(team_meta_items))
            if team.ranking_url:
                f.write(
                    f"<a href='{h(team.ranking_url)}' target='_blank' rel='noopener noreferrer'"
                    f" class='team-meta-link'>Voir classement &#x2197;</a>"
                )
            f.write("</div>\n")
        self._write_html_contact_table(
            f, team.contacts, with_refs=True, table_id=f"{card_id}-team-{index}"
        )
        f.write("</div>\n</section>\n")

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
        level_tokens, role_tokens, search_blob, total_contacts = (
            self._build_club_card_search_data(club, city_name)
        )

        def salle_anchor_fn(name: str, address: str, map_url: str) -> str:
            return salle_anchor_by_signature.get(
                self._salle_signature(name, address, map_url), ""
            )

        f.write(
            f"<article class='club-card' id='{h(card_id)}' data-card-id='{h(card_id)}' "
            f"data-city='{h(slugify(city_name))}' data-distance='{city_distance_km:.2f}' "
            f"data-club-name='{h(club.nom.lower())}' data-levels='{h(' '.join(level_tokens))}' "
            f"data-roles='{h(' '.join(sorted(role_tokens)))}' data-search='{h(search_blob)}' "
            f"data-contact-count='{total_contacts}'>\n"
        )
        self._write_club_header_row(
            f, club, city_name, city_distance_km, total_contacts, salle_anchor_fn
        )
        self._write_club_action_links(f, club)

        if club.club_contacts:
            club_role_tokens = sorted(
                {slugify(c.role) for c in club.club_contacts if c.role}
            )
            f.write(
                f"<section class='team team-filterable team--club' data-team-level='' "
                f"data-team-roles='{h(' '.join(club_role_tokens))}'>\n"
                "<div class='team-heading'><span class='badge badge-club'>Contacts club</span>"
                f"<span class='team-count'>{len(club.club_contacts)} contact(s)</span></div>\n"
                "<div class='team-body'>\n"
            )
            self._write_html_contact_table(
                f, club.club_contacts, with_refs=True, table_id=f"{card_id}-club"
            )
            f.write("</div>\n</section>\n")

        for index, team in enumerate(club.teams, start=1):
            self._write_club_team_section(f, team, index, card_id, salle_anchor_fn)

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

    def _collect_map_markers(self) -> str:
        """Collect all club coordinates and popup data as a JSON string for Leaflet."""
        markers: list[dict] = []
        for city in self.cities:
            for index, club in enumerate(city.clubs, start=1):
                if club.lat is None or club.lng is None:
                    continue
                card_id = f"club-{slugify(city.ville)}-{slugify(club.nom)}-{index}"
                dir_url = _directions_url(club.lat, club.lng, club.adresse)
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
                        "lat": club.lat,
                        "lng": club.lng,
                        "popup": popup,
                        "name": club.nom,
                        "logo_url": club.logo_url,
                        "card_id": card_id,
                    }
                )
        return json.dumps(markers, ensure_ascii=False)

    def _write_leaflet_map_setup_js(self, f) -> None:
        """Write Leaflet map init + radius circle JS."""
        f.write(f"""\
(function() {{
  var center = [{self.lat}, {self.lng}];
  var mapEl = document.getElementById('map');
  if (!mapEl || typeof L === 'undefined') {{ return; }}
  var map = L.map('map').setView(center, 8);
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18
  }}).addTo(map);
  var radiusCircle = L.circle(center, {{
    radius: {self.radius * 1000}, color: '#416BD7', fillColor: '#416BD7',
    fillOpacity: 0.08, weight: 2, dashArray: '8 4'
  }}).addTo(map);
""")

    @staticmethod
    def _write_leaflet_icon_helpers_js(f) -> None:
        """Write JS escapeHtml + buildClubIcon helper functions."""
        f.write("""\
  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  function buildClubIcon(m) {
    var safeName = escapeHtml(m.name || 'Club');
    var rawLogo = typeof m.logo_url === 'string' ? m.logo_url.trim() : '';
    if (/^https?:\\/\\//i.test(rawLogo)) {
      return L.divIcon({className:'club-marker',
        html:'<div class="club-pin club-pin--logo" title="'+safeName+'">'
          +'<img class="club-pin__img" src="'+escapeHtml(rawLogo)+'" alt="" loading="lazy"></div>',
        iconSize:[30,30],iconAnchor:[15,15],popupAnchor:[0,-15]});
    }
    return L.divIcon({className:'club-marker',
      html:'<div class="club-pin club-pin--fallback" title="'+safeName+'">'
        +'<span class="club-pin__emoji" aria-hidden="true">&#x1F3C0;</span></div>',
      iconSize:[30,30],iconAnchor:[15,15],popupAnchor:[0,-15]});
  }
""")

    @staticmethod
    def _write_leaflet_clusters_js(f, markers_json: str) -> None:
        """Write Leaflet marker clusters + data loading + updateClusters function."""
        f.write(f"""\
  var clusters = L.markerClusterGroup({{maxClusterRadius:40,spiderfyOnMaxZoom:true,
    showCoverageOnHover:false,
    iconCreateFunction:function(cluster){{
      var n=cluster.getChildCount();
      return L.divIcon({{
        html:'<div style="background:#416BD7;color:#fff;border-radius:50%;width:32px;height:32px;'
          +'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;'
          +'border:2px solid #fff;box-shadow:0 0 6px rgba(0,0,0,0.3)">'+n+'</div>',
        className:'club-cluster',iconSize:[32,32],iconAnchor:[16,16]}});
    }}}});
  var data = {markers_json};
  var markerEntries=[];
  var markerByCardId=Object.create(null);
  data.forEach(function(m){{
    var marker=L.marker([m.lat,m.lng],{{icon:buildClubIcon(m)}}).bindPopup(m.popup);
    if(m.name){{marker.bindTooltip(escapeHtml(m.name),{{direction:'top',offset:[0,-18],sticky:true,opacity:0.95}});}}
    markerEntries.push({{cardId:m.card_id||'',marker:marker}});
    if(m.card_id){{
      markerByCardId[m.card_id]=marker;
      marker.on('click',function(){{document.dispatchEvent(new CustomEvent('ffbb:marker-selected',{{detail:{{cardId:m.card_id}}}}));}});
    }}
  }});
  function updateClusters(visibleCardIds,preserveView){{
    var hasFilter=Array.isArray(visibleCardIds);
    var visibleSet=Object.create(null);
    if(hasFilter){{visibleCardIds.forEach(function(id){{visibleSet[id]=true;}});}}
    clusters.clearLayers();
    var bounds=radiusCircle.getBounds();
    var n=0;
    markerEntries.forEach(function(e){{
      if(hasFilter&&!visibleSet[e.cardId]){{return;}}
      clusters.addLayer(e.marker);bounds.extend(e.marker.getLatLng());n+=1;
    }});
    if(!map.hasLayer(clusters)){{map.addLayer(clusters);}}
    if(!preserveView&&n>0){{map.fitBounds(bounds,{{padding:[10,10],maxZoom:11}});}}
  }}
  updateClusters(null,false);
""")

    @staticmethod
    def _write_leaflet_bridge_js(f) -> None:
        """Write the window.__ffbbMapBridge public API + close IIFE."""
        f.write("""\
  window.__ffbbMapBridge = {
    setVisibleCards: function(cardIds, preserveView) { updateClusters(cardIds, !!preserveView); },
    focusCard: function(cardId, openPopup) {
      var marker = markerByCardId[cardId];
      if (!marker) { return; }
      map.panTo(marker.getLatLng(), {animate: true, duration: 0.35});
      if (openPopup !== false) { marker.openPopup(); }
    }
  };
})();
""")

    def _write_leaflet_js(self, f) -> None:
        """Write the Leaflet map initialization script (delegates to sub-writers)."""
        markers_json = self._collect_map_markers()
        self._write_leaflet_map_setup_js(f)
        self._write_leaflet_icon_helpers_js(f)
        self._write_leaflet_clusters_js(f, markers_json)
        self._write_leaflet_bridge_js(f)

    @staticmethod
    @staticmethod
    def _write_ui_declarations_js(f) -> None:
        """Write IIFE open + state declarations + utility/sort/helper functions."""
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

""")

    @staticmethod
    def _write_ui_filters_and_card_js(f) -> None:
        """Write applyFilters, setActiveCard, copyText functions."""
        f.write("""\
      function applyFilters() {
        var term = normalize(searchInput.value);
        var cityValue = cityInput.value || 'all';
        var levelValue = levelInput.value || 'all';
        var roleValue = roleInput.value || 'all';
        var maxDistanceValue = Number(distanceInput.value || maxDistance);
        var visibleCardIds = [];
        var visibleContactCount = 0;

""")

    @staticmethod
    def _write_ui_event_handlers_js(f) -> None:
        """Write event handler registrations + IIFE close."""
        f.write("""\
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

    @staticmethod
    def _write_report_ui_js(f) -> None:
        """Write client-side UI interactions (delegates to sub-writers)."""
        ContactReport._write_ui_declarations_js(f)
        ContactReport._write_ui_filters_and_card_js(f)
        ContactReport._write_ui_event_handlers_js(f)

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Work+Sans:wght@500;600;700;800&display=swap');
:root {
  --bg: #F3F6FB;
  --surface: #FFFFFF;
  --surface-soft: #F7F9FD;
  --text: #0D141A;
  --muted: #5F6B7A;
  --border: #D9E1F0;
  --accent: #416BD7;
  --accent-dark: #101840;
  --accent-light: #E9EFFC;
  --accent-link: #176BE0;
  --focus: #176BE0;
  --radius: 14px;
  --sidebar-w: 236px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; min-width: 0; }
[hidden] { display: none !important; }
html {
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
}
body {
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
  font-family: 'Inter', 'Roboto', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  background:
    radial-gradient(circle at 11% 2%, rgba(65, 107, 215, 0.13), transparent 32%),
    radial-gradient(circle at 86% -3%, rgba(16, 24, 64, 0.10), transparent 30%),
    var(--bg);
}
img, table, svg { max-width: 100%; }
a { color: var(--accent-link); }
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0.5rem;
  background: var(--accent-dark);
  color: #fff;
  padding: 0.5rem 0.75rem;
  border-radius: 999px;
  z-index: 999;
}
.skip-link:focus { left: 0.75rem; }
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
  top: 0;
  left: 0;
  width: var(--sidebar-w);
  height: 100vh;
  overflow-y: auto;
  background: linear-gradient(180deg, #FFFFFF 0%, #F3F7FF 100%);
  border-right: 1px solid var(--border);
  padding: 1rem 0;
  z-index: 100;
}
.sidebar-title {
  padding: 0 1rem 0.85rem;
  font-family: 'Work Sans', 'Inter', sans-serif;
  font-weight: 800;
  font-size: 1rem;
  color: var(--accent-dark);
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
  gap: 0.5rem;
  padding: 0.42rem 1rem;
  color: #1F2A44;
  text-decoration: none;
  font-size: 0.82rem;
  transition: background 0.15s ease, color 0.15s ease;
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
  padding: 2rem clamp(1rem, 2.6vw, 2.6rem);
}
.content > * { max-width: 100%; }

/* Hero */
.hero {
  margin-bottom: 1.1rem;
  padding: 1.1rem 1.2rem;
  border: 1px solid rgba(65, 107, 215, 0.25);
  border-radius: 20px;
  background:
    linear-gradient(128deg, #FFFFFF 0%, #F6F9FF 54%, #EDF2FF 100%);
  box-shadow: 0 14px 30px rgba(16, 24, 64, 0.08);
}
.hero-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.9rem;
}
.hero-kicker {
  margin: 0;
  font-size: 0.69rem;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--accent);
  font-weight: 800;
}
h1 {
  font-family: 'Work Sans', 'Inter', sans-serif;
  font-size: clamp(1.35rem, 2.5vw, 1.8rem);
  font-weight: 800;
  margin: 0.22rem 0 0;
  color: var(--accent-dark);
}
.hero-date {
  margin: 0;
  color: #32405E;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(65, 107, 215, 0.24);
  border-radius: 999px;
  padding: 0.2rem 0.58rem;
  font-size: 0.75rem;
  white-space: nowrap;
}
.hero-subtitle {
  margin: 0.55rem 0 0.68rem;
  color: #32405E;
  font-size: 0.86rem;
  max-width: 72ch;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.38rem;
  margin-top: 0.48rem;
}
.hero-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50px;
  text-decoration: none;
  font-size: 0.76rem;
  font-weight: 700;
  padding: 0.24rem 0.66rem;
  border: 1px solid transparent;
}
.hero-action--primary {
  background: var(--accent-dark);
  color: #fff;
}
.hero-action--primary:hover {
  background: #1A255F;
}
.hero-action--ghost {
  color: var(--accent-dark);
  border-color: rgba(16, 24, 64, 0.26);
  background: rgba(255, 255, 255, 0.7);
}
.hero-action--ghost:hover {
  background: #fff;
}
.hero-facts {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.46rem;
  margin: 0;
  padding: 0;
}
.hero-fact {
  border: 1px solid rgba(65, 107, 215, 0.22);
  border-radius: 12px;
  padding: 0.38rem 0.5rem;
  background: rgba(255, 255, 255, 0.82);
}
.hero-fact__label {
  display: block;
  color: #6A7691;
  font-size: 0.66rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
}
.hero-fact__value {
  display: block;
  margin-top: 0.08rem;
  font-size: 0.82rem;
  color: var(--accent-dark);
  font-weight: 700;
  overflow-wrap: anywhere;
}
h2 {
  font-family: 'Work Sans', 'Inter', sans-serif;
  font-size: 1.15rem;
  margin: 1.4rem 0 0.72rem;
  padding-bottom: 0.38rem;
  border-bottom: 1px solid var(--border);
  color: var(--accent-dark);
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
.summary { margin: 0.95rem 0 1.2rem; }
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(118px, 1fr));
  gap: 0.62rem;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 0.66rem 0.56rem;
  text-align: center;
  box-shadow: 0 6px 14px rgba(16, 24, 64, 0.05);
}
.stat-val {
  display: block;
  font-size: 1.48rem;
  font-weight: 800;
  line-height: 1.12;
  color: var(--accent-dark);
}
.stat-label {
  display: block;
  font-size: 0.68rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Controls */
.controls {
  margin: 0.6rem 0 0.8rem;
  padding: 0.45rem 0.55rem;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 8px 16px rgba(16, 24, 64, 0.05);
}
.controls-bar {
  display: flex;
  gap: 0.45rem;
  align-items: center;
  flex-wrap: wrap;
}
.controls-actions {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-left: auto;
}
.controls-advanced {
  margin-top: 0.35rem;
}
.controls-advanced > summary {
  cursor: pointer;
  color: var(--accent-dark);
  font-size: 0.74rem;
  font-weight: 700;
  user-select: none;
  list-style: none;
  display: inline-flex;
  align-items: center;
  border: 1px solid rgba(16, 24, 64, 0.2);
  border-radius: 999px;
  padding: 0.14rem 0.52rem;
  background: #fff;
}
.controls-advanced > summary::-webkit-details-marker { display: none; }
.controls-advanced > summary::before {
  content: "▸";
  margin-right: 0.28rem;
}
.controls-advanced[open] > summary::before { content: "▾"; }
.controls-advanced[open] .controls-grid { margin-top: 0.42rem; }
.controls-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.42rem;
}
.control-field {
  display: flex;
  flex-direction: column;
  gap: 0.16rem;
}
.control-field > span {
  color: var(--muted);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.control-field--search {
  flex: 1 1 360px;
  min-width: 160px;
}
.control-field input,
.control-field select {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.3rem 0.58rem;
  font: inherit;
  background: #fff;
  font-size: 0.82rem;
  color: var(--text);
}
.control-field--range input {
  border-radius: 0;
  padding: 0;
}
.controls-result {
  font-size: 0.72rem;
  color: var(--muted);
  margin: 0;
}
.control-reset {
  border: 1px solid rgba(16, 24, 64, 0.22);
  background: var(--accent-dark);
  color: #fff;
  border-radius: 999px;
  padding: 0.22rem 0.58rem;
  font-size: 0.74rem;
  line-height: 1.2;
  cursor: pointer;
}
.control-reset:hover {
  background: #1A255F;
}

/* Top grid — hero/stats/controls left, map right on desktop */
.top-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
  align-items: stretch;
  margin-bottom: 1.2rem;
}
.top-grid__right {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  border-radius: 20px;
  overflow: clip;
  box-shadow: 0 14px 30px rgba(16, 24, 64, 0.08);
}
.top-grid__right #map {
  flex: 1;
  height: auto;
  min-height: 320px;
  margin-bottom: 0;
  border-radius: 0;
}

/* Map */
#map {
  height: clamp(280px, 47vh, 520px);
  border-radius: 18px;
  border: 1px solid var(--border);
  margin-bottom: 1rem;
  overflow: clip;
}
.club-marker { background: transparent; border: 0; }
.club-pin {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(16, 24, 64, 0.35);
}
.club-pin--logo { background: #FFFFFF; }
.club-pin--fallback {
  background: linear-gradient(135deg, #416BD7, #101840);
}
.club-pin__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.club-pin__emoji { font-size: 0.95rem; line-height: 1; }
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
  margin-bottom: 0.85rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 0.45rem 0.8rem;
}
.mobile-nav summary {
  cursor: pointer;
  font-weight: 700;
  color: var(--accent-dark);
}
.mobile-nav ul {
  list-style: none;
  padding: 0.45rem 0 0.1rem;
}
.mobile-nav li a {
  display: block;
  padding: 0.22rem 0;
  color: var(--text);
  text-decoration: none;
  font-size: 0.82rem;
}

/* City & club cards */
.city-section { margin-bottom: 0.88rem; }
.city-details {
  border: 1px solid var(--border);
  border-radius: 16px;
  background: var(--surface);
  overflow: clip;
}
.city-summary {
  list-style: none;
  cursor: pointer;
  padding: 0.66rem 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.62rem;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFF 100%);
}
.city-summary__title {
  font-family: 'Work Sans', 'Inter', sans-serif;
  font-weight: 700;
  color: var(--accent-dark);
}
.city-summary__meta {
  font-size: 0.75rem;
  color: var(--muted);
  overflow-wrap: anywhere;
  text-align: right;
}
.city-body { padding: 0 0.78rem 0.78rem; }
.city-clubs { margin-top: 0.45rem; }
.empty-city {
  background: #FFF6E8;
  border-left: 4px solid #F0A537;
  border-radius: 12px;
  padding: 0.68rem 0.82rem;
  color: #855102;
  font-style: italic;
}
.club-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 14px;
  padding: 0.92rem 1rem;
  margin-bottom: 0.82rem;
  box-shadow: 0 10px 22px rgba(16, 24, 64, 0.06);
  transition: border-color 0.15s ease, box-shadow 0.2s ease, transform 0.2s ease;
}
.club-card:hover {
  border-color: #9FB5EA;
  box-shadow: 0 14px 26px rgba(16, 24, 64, 0.10);
}
.club-card.is-highlighted {
  border-color: var(--focus);
  box-shadow: 0 0 0 3px rgba(23, 107, 224, 0.18), 0 14px 26px rgba(16, 24, 64, 0.13);
  transform: translateY(-1px);
}
.club-header {
  display: flex;
  align-items: center;
  gap: 0.68rem;
  margin-bottom: 0.48rem;
}
.club-logo {
  width: 38px;
  height: 38px;
  object-fit: contain;
  border-radius: 6px;
  flex-shrink: 0;
  background: #fff;
  border: 1px solid #E4EAF7;
}
.club-logo-placeholder {
  font-size: 1.45rem;
  width: 38px;
  text-align: center;
  flex-shrink: 0;
}
.club-info { flex: 1; }
.club-name {
  font-family: 'Work Sans', 'Inter', sans-serif;
  font-size: 0.98rem;
  font-weight: 700;
  margin: 0;
  color: var(--accent-dark);
}
p.address {
  font-size: 0.8rem;
  color: var(--muted);
  margin: 0;
  overflow-wrap: anywhere;
}
.address--secondary {
  margin-top: 0.08rem;
  color: #4F5D74;
}
.address-link {
  color: inherit;
  text-decoration: underline dotted;
  text-underline-offset: 2px;
}
.address-link:hover { color: var(--accent-link); }
.salle-ref-link {
  color: var(--accent-dark);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.salle-ref-link:hover { color: var(--accent-link); }
.club-meta {
  margin-top: 0.16rem;
  color: var(--muted);
  font-size: 0.73rem;
}
.club-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.36rem;
  margin-bottom: 0.62rem;
  padding-bottom: 0.62rem;
  border-bottom: 1px solid #E7ECF7;
}
.action-link {
  font-size: 0.74rem;
  color: var(--accent-dark);
  text-decoration: none;
  padding: 0.18rem 0.48rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: #fff;
  white-space: nowrap;
}
.action-link:hover {
  background: var(--accent-light);
  text-decoration: none;
}

/* Teams */
.team {
  margin-top: 0.42rem;
  border: 1px solid #E9EEF8;
  border-radius: 12px;
  overflow: clip;
}
.team-heading {
  padding: 0.4rem 0.5rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.35rem;
  background: #F8FAFF;
  border-bottom: 1px solid #E9EEF8;
}
.team-body { padding: 0.32rem 0.5rem 0.42rem; }
.team-count {
  margin-left: auto;
  font-size: 0.69rem;
  color: var(--muted);
  font-weight: 700;
}
.team-label {
  font-size: 0.64rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
  font-weight: 700;
}
.team--club {
  border-color: #D4C9A8;
  background: #FBF8F0;
}
.team--club .team-heading {
  background: #F3EDD8;
  border-bottom-color: #D4C9A8;
}
.team--club .team-body {
  background: #FBF8F0;
}
.team--masculin {
  border-color: #B8D4F0;
  background: #EFF6FF;
}
.team--masculin .team-heading {
  background: #DBEAFE;
  border-bottom-color: #B8D4F0;
}
.team--masculin .team-body {
  background: #EFF6FF;
}
.team--feminin {
  border-color: #F0B8D4;
  background: #FFF0F6;
}
.team--feminin .team-heading {
  background: #FCE4F0;
  border-bottom-color: #F0B8D4;
}
.team--feminin .team-body {
  background: #FFF0F6;
}

/* Badges */
.badge {
  display: inline-block;
  font-size: 0.66rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  vertical-align: middle;
}
.badge-pro { background: #E7EEFF; color: #1E4DB8; }
.badge-national { background: #EBF3FF; color: #114AB0; }
.badge-ligue { background: #EEF1F8; color: #3E4B67; }
.badge-sexe { background: #F1F3F8; color: #4C566E; }
.badge-div { background: #F1F3F8; color: #5D677F; font-weight: 500; text-transform: none; }
.badge-club { background: #E9EFFC; color: var(--accent-dark); }
.badge-president { background: #FFF2D7; color: #84520B; }
.badge-coach { background: #DDF8EC; color: #0F694D; }
.badge-correspondant { background: #E7EEFF; color: #1F4EAF; }
.badge-role { background: #EEF1F8; color: #4E5A71; }
.team-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.34rem;
  margin: 0.3rem 0 0.12rem;
}
.team-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  max-width: 100%;
  border: 1px solid #DDE5F5;
  border-radius: 999px;
  padding: 0.2rem 0.5rem;
  background: #FFFFFF;
  color: #2E3D5A;
  font-size: 0.73rem;
}
.team-chip--poule {
  background: #F7F9FD;
  border-color: #DDE5F5;
}
.team-chip--ranking {
  background: #EEF3FF;
  border-color: #CBD9F8;
}
.team-chip--next {
  background: #E9EFFC;
  border-color: #CBD9F8;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 0.14rem 0.38rem;
  align-items: start;
  border-radius: 10px;
  padding: 0.28rem 0.52rem;
}
.team-chip--next-coupe {
  background: #FFF5E6;
  border-color: #F0D5A0;
}
.team-chip--next-coupe .team-chip__label {
  color: #8B5E0F;
}
.team-chip--next-coupe .team-chip__value,
.team-chip--next-coupe .team-chip__when,
.team-chip--next-coupe .team-chip__opponent {
  color: #7A4F00;
}
.team-chip--next-coupe .team-chip__vs {
  color: #9E7530;
}
.team-chip--next-plateau {
  background: #F0F8EC;
  border-color: #C8DDB8;
}
.team-chip--next-plateau .team-chip__label {
  color: #3D6B1E;
}
.team-chip--next-plateau .team-chip__value,
.team-chip--next-plateau .team-chip__when,
.team-chip--next-plateau .team-chip__opponent {
  color: #2D5312;
}
.team-chip--next-plateau .team-chip__vs {
  color: #507A30;
}
.team-chip__label {
  font-size: 0.61rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: #5C6C8B;
  font-weight: 700;
}
.team-chip__value,
.team-chip__when {
  font-weight: 700;
  color: var(--accent-dark);
}
.team-chip__vs {
  color: #596A89;
  font-size: 0.7rem;
}
.team-chip__next-main {
  min-width: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.2rem;
}
.team-chip__opponent {
  font-weight: 700;
  color: var(--accent-dark);
  max-width: none;
  white-space: normal;
  overflow: visible;
  text-overflow: clip;
  line-height: 1.3;
  overflow-wrap: anywhere;
}
.team-chip__hall {
  grid-column: 1 / -1;
  font-size: 0.68rem;
  color: #475878;
  line-height: 1.3;
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
  padding: 0.2rem 0.55rem;
  background: #fff;
  font-size: 0.74rem;
  color: var(--accent-link);
  text-decoration: none;
  white-space: nowrap;
}
.team-meta-link:hover {
  text-decoration: none;
  background: var(--accent-light);
}
.competition-logo {
  vertical-align: middle;
  margin-right: 0.3rem;
  border-radius: 4px;
}

/* Contact tables */
.contacts-block { margin-top: 0.3rem; }
table.contacts {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  margin-top: 0.34rem;
  margin-bottom: 0.2rem;
}
table.contacts th {
  background: #F6F8FD;
  font-weight: 700;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  padding: 0.33rem 0.55rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
  color: #495773;
}
table.contacts td {
  padding: 0.27rem 0.55rem;
  border-bottom: 1px solid #EEF2FA;
  font-size: 0.8rem;
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
}
table.contacts tr:hover { background: #F5F8FF; }
table.contacts a { color: var(--accent-link); }
.contacts-cards { display: none; }
.contact-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  background: #fff;
  padding: 0.5rem 0.6rem;
  margin-top: 0.45rem;
}
.contact-card__title { font-weight: 700; }
.contact-card__role { margin-top: 0.18rem; }
.contact-card__line {
  margin-top: 0.28rem;
  display: flex;
  align-items: center;
  gap: 0.45rem;
  flex-wrap: wrap;
  font-size: 0.8rem;
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
  font-size: 0.66rem;
  cursor: pointer;
}
.copy-btn:hover { background: var(--accent-light); }
.copy-btn--inline { margin-left: 0.32rem; }

/* Nav links */
p.nav {
  margin-top: 0.45rem;
  font-size: 0.8rem;
  color: var(--muted);
}
p.nav a { color: var(--accent-link); text-decoration: none; }
p.nav a:hover { text-decoration: underline; }

/* Contact references */
a.contact-ref {
  color: var(--accent-dark);
  text-decoration: none;
  border-bottom: 1px dotted var(--accent-link);
}
a.contact-ref:hover {
  color: var(--accent-link);
  border-bottom-style: solid;
}

/* Club contacts (reserved) */
.club-contacts-section {
  background: var(--accent-light);
  border-radius: var(--radius);
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
}

/* Sidebar anchors */
.sidebar-annuaire {
  margin-top: 0.5rem;
  border-top: 1px solid var(--border);
  padding-top: 0.5rem;
}
.sidebar-annuaire a {
  font-weight: 700;
  color: var(--accent-dark) !important;
}

/* Annuaire + salles */
.annuaire-section {
  margin-top: 1.8rem;
  padding-top: 0.95rem;
  border-top: 2px solid var(--accent);
}
.annuaire-desc {
  font-size: 0.82rem;
  color: var(--muted);
  margin-bottom: 0.75rem;
}
.annuaire-table td.mentions {
  font-size: 0.74rem;
  color: var(--muted);
  max-width: 250px;
}
.annuaire-table tr:target {
  background: var(--accent-light) !important;
  animation: highlight-fade 2s ease-out;
}
.salles-section {
  margin-top: 1.8rem;
  padding-top: 0.95rem;
  border-top: 1px solid var(--border);
}
.salles-list {
  margin: 0.62rem 0 0;
  padding-left: 1.15rem;
}
.salle-item {
  margin: 0 0 0.58rem;
  padding: 0.33rem 0.42rem;
  border: 1px solid #DDE5F5;
  border-radius: 10px;
  background: #fff;
}
.salle-item__title {
  margin: 0;
  font-weight: 700;
  font-size: 0.84rem;
  color: var(--accent-dark);
}
.salle-item__meta {
  margin: 0.14rem 0 0;
  color: var(--muted);
  font-size: 0.78rem;
}
.salle-item__actions {
  margin: 0.15rem 0 0;
  font-size: 0.76rem;
}
.salle-item__actions a { color: var(--accent-link); }
@keyframes highlight-fade {
  0% { background: #DDE8FF; }
  100% { background: var(--accent-light); }
}

/* Footer */
footer {
  margin-top: 2.4rem;
  padding-top: 0.95rem;
  border-top: 1px solid var(--border);
  font-size: 0.76rem;
  color: var(--muted);
  font-style: italic;
}

/* Print */
@media print {
  .sidebar, #map-section, .mobile-nav, p.nav, .club-actions, .controls, .copy-btn { display: none; }
  .content { margin-left: 0; max-width: none; width: 100%; padding: 0; }
  body { font-size: 11px; background: #fff; }
  .club-card { border: 1px solid #ccc; box-shadow: none; break-inside: avoid; }
  .stat { border: 1px solid #ccc; }
  a { color: var(--text); }
  a[href]::after { content: ' (' attr(href) ')'; font-size: 0.7rem; color: #999; }
  a[href^="mailto:"]::after, a[href^="tel:"]::after { content: none; }
}

/* Responsive */
@media (max-width: 1100px) {
  .top-grid {
    display: block;
  }
  .top-grid__right {
    position: static;
  }
  .sidebar { display: none; }
  .content {
    margin-left: 0;
    width: 100%;
    max-width: none;
    padding: 1.35rem 0.9rem;
  }
  .mobile-nav { display: block; }
  .hero-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .controls-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
  body { font-size: 13px; }
  h1 { font-size: 1.3rem; }
  h2 { font-size: 1.02rem; }
  .hero {
    padding: 0.8rem 0.82rem;
    border-radius: 16px;
  }
  .hero-main {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.45rem;
  }
  .hero-actions {
    margin-top: 0.36rem;
  }
  .hero-facts {
    grid-template-columns: 1fr;
    gap: 0.32rem;
  }
  .controls {
    margin: 0.32rem 0 0.5rem;
    padding: 0.3rem 0.34rem;
  }
  .controls-bar {
    gap: 0.24rem;
  }
  .control-field--search {
    min-width: 0;
    flex: 1 1 auto;
  }
  .control-field--search > span {
    display: none;
  }
  .controls-actions {
    display: none;
  }
  .controls-advanced {
    margin-top: 0.22rem;
  }
  .controls-advanced > summary {
    font-size: 0.7rem;
    padding: 0.12rem 0.42rem;
  }
  .controls-grid {
    grid-template-columns: 1fr;
    gap: 0.34rem;
  }
  .control-field > span { font-size: 0.6rem; }
  .control-field input,
  .control-field select {
    font-size: 0.79rem;
    padding: 0.22rem 0.42rem;
  }
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  #map { height: clamp(235px, 43vh, 318px); border-radius: 14px; }
  .city-summary { flex-direction: column; align-items: flex-start; }
  .city-summary__meta {
    font-size: 0.73rem;
    text-align: left;
  }
  .club-card {
    padding: 0.78rem;
    border-radius: 12px;
  }
  .club-header { gap: 0.56rem; }
  .club-logo, .club-logo-placeholder { width: 32px; height: 32px; }
  .action-link { font-size: 0.7rem; }
  .team-heading { gap: 0.26rem; }
  .team-label { width: 100%; }
  .team-meta {
    align-items: stretch;
    gap: 0.28rem;
  }
  .team-chip {
    width: 100%;
    border-radius: 9px;
    padding: 0.28rem 0.4rem;
  }
  .team-chip--next {
    padding: 0.3rem 0.42rem;
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
    next_match_type: str
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


def classify_engagement_level(
    hit: EngagementsHit,
    accepted_echelons: frozenset[EchelonEnum] | None = None,
    accepted_age_groups: frozenset[AgeGroupEnum] | None = None,
    accepted_sexes: frozenset[SexeEnum] | None = None,
    _sexes_values: frozenset[str] | None = None,
) -> str | None:
    """Return the level label or None (excluded).

    When a filter parameter is ``None``, all values are accepted.
    Pass ``_sexes_values`` (pre-computed ``frozenset(s.value for s in accepted_sexes)``)
    to avoid rebuilding the set on every call.
    """
    # SexeEnum filter
    if accepted_sexes is not None:
        accepted_values = _sexes_values or frozenset(s.value for s in accepted_sexes)
        if (hit.sexe or "") not in accepted_values:
            return None

    # Age-group filter
    if accepted_age_groups is not None:
        if hit.categorie and hit.categorie.code:
            age = hit.categorie.code.age_group
            if age is not None and age not in accepted_age_groups:
                return None

    # EchelonEnum filter + label
    if hit.niveau and hit.niveau.code:
        echelon = hit.niveau.code.echelon
        if accepted_echelons is not None and echelon not in accepted_echelons:
            return None
        return _ECHELON_TO_LABEL.get(echelon, "OTHER")
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


def _load_all_poule_snapshots(
    client: FFBBAPIClientV2,
    poule_ids: set[int],
    salle_cache: dict[int, tuple[str, str, str]] | None = None,
) -> dict[int, dict[str, _TeamCompetitionSnapshot]]:
    """Batch-load ranking + next match info for multiple poules at once.

    Makes 2 API calls total (one for engagements, one for rencontres)
    instead of 2 per poule.
    """
    if not poule_ids:
        return {}
    if salle_cache is None:
        salle_cache = {}

    # 1. Batch-fetch all engagements for all poules
    all_engagements = client.list_engagements_by_poules(list(poule_ids))
    eng_by_poule: dict[int, list[GetEngagementsResponse]] = defaultdict(list)
    for eng in all_engagements:
        if eng.idPoule is not None:
            eng_by_poule[eng.idPoule].append(eng)

    # 2. Batch-fetch all rencontres for all poules
    all_rencontres = client.list_rencontres_by_poules(
        list(poule_ids), sort=["date_rencontre"]
    )
    ren_by_poule: dict[int, list] = defaultdict(list)
    for match in all_rencontres:
        if match.idPoule is not None:
            ren_by_poule[match.idPoule].append(match)

    # 3. Assemble snapshots per poule (reuses _load_poule_snapshots logic)
    result: dict[int, dict[str, _TeamCompetitionSnapshot]] = {}
    for pid in poule_ids:
        snapshots: dict[str, _TeamCompetitionSnapshot] = {}

        # Rankings from engagements
        engagements = eng_by_poule.get(pid, [])
        rank_total = len(engagements)
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

        # Next matches from rencontres
        matches = ren_by_poule.get(pid, [])
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

        result[pid] = snapshots

    return result


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
    next_match_type: str,
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
        next_match_type=next_match_type,
        next_match_salle_name=next_match_salle_name,
        next_match_salle_address=next_match_salle_address,
        next_match_salle_map_url=next_match_salle_map_url,
    )


# ---------------------------------------------------------------------------
# City resolution & CLI enum parsing
# ---------------------------------------------------------------------------


def resolve_city_coordinates(
    client: FFBBAPIClientV2,
    city_name: str,
) -> tuple[float, float, str, frozenset[str]]:
    """Resolve a city name to (lat, lng, code_postal, club_codes) via Meilisearch.

    Two-step approach:
    1. Text search to discover matching **commune names** (e.g. "Paris" →
       "Paris", "Paris 1er Arrondissement", "Paris 2ème", …).
    2. For each matching commune, ``search_organismes_by_city`` to retrieve
       ALL clubs registered in that commune.
    """
    # Step 1: text search → discover matching commune names + coordinates
    result = client.search_organismes(name=city_name, limit=200)
    coords: list[tuple[float, float]] = []
    code_postal: str = ""
    commune_names: set[str] = set()
    city_lower = city_name.lower()

    if result and result.hits:
        for hit in result.hits:
            if hit.geo and hit.geo.lat is not None and hit.geo.lng is not None:
                coords.append((hit.geo.lat, hit.geo.lng))
            if not code_postal and hit.commune and hit.commune.code_postal:
                code_postal = hit.commune.code_postal
            if (
                hit.commune
                and hit.commune.lower_libelle
                and (
                    hit.commune.lower_libelle == city_lower
                    or hit.commune.lower_libelle.startswith(city_lower + " ")
                )
            ):
                commune_names.add(hit.commune.libelle)

    if not coords:
        logger.error("Impossible de résoudre les coordonnées pour '%s'.", city_name)
        raise SystemExit(1)

    coords.sort()
    mid = len(coords) // 2
    lat, lng = coords[mid][0], coords[mid][1]
    logger.info(
        "Ville '%s' coords → (%.5f, %.5f, CP %s) via %d organismes, " "%d communes: %s",
        city_name,
        lat,
        lng,
        code_postal or "?",
        len(result.hits) if result and result.hits else 0,
        len(commune_names),
        (
            ", ".join(sorted(commune_names))
            if len(commune_names) <= 10
            else f"{len(commune_names)} communes"
        ),
    )

    # Step 2: search organismes in each matching commune → comprehensive club codes
    club_codes: set[str] = set()
    for commune in sorted(commune_names):
        r = client.search_organismes_by_city(commune, limit=200)
        if r and r.hits:
            for hit in r.hits:
                if hit.code:
                    club_codes.add(hit.code)
    logger.info(
        "Ville '%s' clubs → %d clubs dans %d communes",
        city_name,
        len(club_codes),
        len(commune_names),
    )
    return lat, lng, code_postal, frozenset(club_codes)


def _parse_enum_args(
    raw: list[str], enum_cls: type[Enum], label: str, parser: argparse.ArgumentParser
) -> frozenset:
    """Parse CLI args into a frozenset of enum members, validated by name."""
    name_map = {e.name: e for e in enum_cls}
    result = []
    for val in raw:
        key = val.upper()
        if key not in name_map:
            parser.error(
                f"Unknown {label}: '{val}'. Valid values: {', '.join(name_map)}"
            )
        result.append(name_map[key])
    return frozenset(result)


# ---------------------------------------------------------------------------
# Adaptive radius constants & helper
# ---------------------------------------------------------------------------

_CITY_RADIUS_KM = 50.0
_MAX_WORKERS = os.cpu_count() or 8


def _resolve_niveau_codes(
    facet_distribution: EngagementsFacetDistribution | None,
    accepted_echelons: frozenset[EchelonEnum] | None,
    accepted_age_groups: frozenset[AgeGroupEnum] | None,
) -> list[str] | None:
    """Parse facet niveau.code distribution and return matching codes.

    Returns None if no filtering is needed (all accepted).
    """
    if accepted_echelons is None and accepted_age_groups is None:
        return None
    if not facet_distribution or not facet_distribution.niveau_code:
        return None
    matching: list[str] = []
    for code_str in facet_distribution.niveau_code:
        cc = CategorieCode(code_str)
        if not cc.is_parsed:
            count = facet_distribution.niveau_code[code_str]
            logger.warning(
                "CodeEnum niveau non reconnu: '%s' (%d engagements ignores)",
                code_str,
                count,
            )
            continue
        if accepted_echelons is not None and cc.echelon not in accepted_echelons:
            continue
        if accepted_age_groups is not None:
            if cc.age_group is not None and cc.age_group not in accepted_age_groups:
                continue
        matching.append(code_str)
    return matching if matching else None


def _resolve_sexe_filter(
    accepted_sexes: frozenset[SexeEnum] | None,
) -> list[str] | None:
    """Map SexeEnum enums to Meilisearch idCompetition.sexe filter values."""
    if accepted_sexes is None:
        return None
    return [s.value for s in accepted_sexes]


def _search_and_classify(
    client: FFBBAPIClientV2,
    lat: float,
    lng: float,
    radius_km: float,
    accepted_echelons: frozenset | None,
    accepted_age_groups: frozenset | None,
    accepted_sexes: frozenset | None,
) -> tuple[object, list[tuple[EngagementsHit, str]], dict[str, int]]:
    """Run geo search + classify in one pass. Returns (result, qualified, level_counts)."""
    # 1. Facet discovery — lightweight query to get niveau.code distribution
    discovery = client.search_engagements_by_geo(
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        limit=1,
    )

    # 2. Resolve filters from facet distribution
    facet_dist = discovery.facet_distribution if discovery else None
    niveau_codes = _resolve_niveau_codes(
        facet_dist, accepted_echelons, accepted_age_groups
    )
    sexes = _resolve_sexe_filter(accepted_sexes)

    # 3. Filtered query — Meilisearch does the heavy lifting
    result = client.search_engagements_filtered(
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        limit=5000,
        sexes=sexes,
        niveau_codes=niveau_codes,
    )

    # 4. Classify — still needed for label assignment + hit.sexe check
    qualified: list[tuple[EngagementsHit, str]] = []
    level_counts: dict[str, int] = defaultdict(int)
    sexes_values = (
        frozenset(s.value for s in accepted_sexes) if accepted_sexes else None
    )
    if result and result.hits:
        for hit in result.hits:
            level = classify_engagement_level(
                hit,
                accepted_echelons,
                accepted_age_groups,
                accepted_sexes,
                _sexes_values=sexes_values,
            )
            if level:
                qualified.append((hit, level))
                level_counts[level] += 1
    return result, qualified, level_counts


# ---------------------------------------------------------------------------
# Main phase helpers
# ---------------------------------------------------------------------------


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Extract basketball contacts near a city"
    )
    parser.add_argument(
        "--city-name",
        type=str,
        required=True,
        help="City name — coordinates resolved automatically via Meilisearch",
    )
    parser.add_argument(
        "--radius", type=float, default=None, help="Radius in km (default: auto 10→50)"
    )
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument(
        "--dry-run", action="store_true", help="Print planned actions without API calls"
    )
    parser.add_argument(
        "--echelon",
        type=str,
        nargs="+",
        default=None,
        help="Echelons to include (e.g. --echelon NATIONAL LIGUE_FEMININE). "
        f"Valid: {', '.join(e.name for e in EchelonEnum)}. Default: all",
    )
    parser.add_argument(
        "--sexe",
        type=str,
        nargs="+",
        default=None,
        help="SexeEnum filter — use enum names (e.g. --sexe MASCULINE FEMININE). "
        f"Valid: {', '.join(e.name for e in SexeEnum)}. Default: all",
    )
    parser.add_argument(
        "--age-group",
        type=str,
        nargs="+",
        default=None,
        help="Age groups (e.g. --age-group SENIOR VETERAN). "
        f"Valid: {', '.join(a.name for a in AgeGroupEnum)}. Default: all",
    )
    return parser


def _parse_cli_filters(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> tuple[
    frozenset[EchelonEnum] | None,
    frozenset[AgeGroupEnum] | None,
    frozenset[SexeEnum] | None,
]:
    """Parse and validate echelon/age-group/sexe filter args into enum frozensets."""
    accepted_echelons: frozenset[EchelonEnum] | None = (
        _parse_enum_args(args.echelon, EchelonEnum, "echelon", parser)
        if args.echelon
        else None
    )
    accepted_age_groups: frozenset[AgeGroupEnum] | None = (
        _parse_enum_args(args.age_group, AgeGroupEnum, "age-group", parser)
        if args.age_group
        else None
    )
    accepted_sexes: frozenset[SexeEnum] | None = (
        _parse_enum_args(args.sexe, SexeEnum, "sexe", parser) if args.sexe else None
    )
    return accepted_echelons, accepted_age_groups, accepted_sexes


def _step1_geo_search_engagements(
    client: FFBBAPIClientV2,
    city_name: str,
    lat: float,
    lng: float,
    explicit_radius: float | None,
    city_club_codes: set[str],
    accepted_echelons: frozenset[EchelonEnum] | None,
    accepted_age_groups: frozenset[AgeGroupEnum] | None,
    accepted_sexes: frozenset[SexeEnum] | None,
) -> tuple[Any, list[Any], dict[str, int], float]:
    """Geo-search Meilisearch for engagements; apply city-club filter or fallback.

    Returns (result, qualified, level_counts, search_radius).
    """
    if explicit_radius is not None:
        search_radius = explicit_radius
        logger.info(
            "[1/5] Recherche geo engagements: %s (%.5f, %.5f), rayon %.1f km (explicite)",
            city_name,
            lat,
            lng,
            search_radius,
        )
        result, qualified, level_counts = _search_and_classify(
            client,
            lat,
            lng,
            search_radius,
            accepted_echelons,
            accepted_age_groups,
            accepted_sexes,
        )
    else:
        search_radius = _CITY_RADIUS_KM
        logger.info(
            "[1/5] Recherche geo engagements: %s (%.5f, %.5f), rayon %.1f km (ville, %d clubs)",
            city_name,
            lat,
            lng,
            search_radius,
            len(city_club_codes),
        )
        result, qualified, level_counts = _search_and_classify(
            client,
            lat,
            lng,
            search_radius,
            accepted_echelons,
            accepted_age_groups,
            accepted_sexes,
        )
        all_qualified = qualified[:]
        if city_club_codes:
            filtered = [(h, l) for h, l in qualified if h.code_club in city_club_codes]
            if filtered:
                qualified = filtered
                level_counts = defaultdict(int)
                for _, l in qualified:
                    level_counts[l] += 1
                logger.info(
                    "[1/5] Ville %s: %d bruts, %d qualifies, %d apres filtre (%d clubs)",
                    city_name,
                    len(result.hits) if result and result.hits else 0,
                    len(all_qualified),
                    len(qualified),
                    len(city_club_codes),
                )
            else:
                logger.info(
                    "[1/5] Ville %s: %d bruts, %d qualifies, 0 apres filtre → fallback %.0f km",
                    city_name,
                    len(result.hits) if result and result.hits else 0,
                    len(all_qualified),
                    search_radius,
                )
        else:
            logger.info(
                "[1/5] Ville %s: %d bruts, %d qualifies (rayon %.0f km, pas de clubs ville)",
                city_name,
                len(result.hits) if result and result.hits else 0,
                len(qualified),
                search_radius,
            )
    return result, qualified, level_counts, search_radius


def _step3_enrich_contacts(
    client: FFBBAPIClientV2,
    qualified: list[Any],
    salle_cache: dict[int, tuple[str, str, str]],
) -> tuple[
    dict[tuple, _CollectedRow],
    dict[int, _ClubInfo | None],
    dict[int, Any],
    dict[int, dict[str, _TeamCompetitionSnapshot]],
    dict[str, _CityGeo],
    int,
]:
    """Enrich qualified engagements with contact data (phases A-D).

    Returns (rows_by_key, club_cache, club_contacts_raw, poule_cache, city_geo, errors).
    """
    from ffbb_api_client_v2.models.club_contacts import ClubContacts as _CC
    from ffbb_api_client_v2.models.contact_role_enum import (
        ContactRoleEnum as _ContactRole,
    )
    from ffbb_api_client_v2.models.engagement_contacts import EngagementContacts as _EC
    from ffbb_api_client_v2.models.engagement_contacts import (
        extract_correspondant as _extract_correspondant,
    )
    from ffbb_api_client_v2.models.engagement_contacts import (
        extract_entraineur_contact as _extract_entraineur_contact,
    )

    club_cache: dict[int, _ClubInfo | None] = {}
    poule_cache: dict[int, dict[str, _TeamCompetitionSnapshot]] = {}
    rows_by_key: dict[tuple, _CollectedRow] = {}
    city_geo: dict[str, _CityGeo] = {}
    errors = 0

    # Pre-parse eng_ids
    eng_ids: list[int] = []
    eng_id_by_hit: dict[int, int] = {}
    for idx, (hit, _level) in enumerate(qualified):
        try:
            eid = int(hit.id) if hit.id else None
        except (ValueError, TypeError):
            eid = None
        if eid:
            eng_ids.append(eid)
            eng_id_by_hit[idx] = eid

    def _fetch_club(oid: int) -> tuple[int, _CC | None]:
        return oid, client.get_club_contacts(oid)

    # Phase A: Batch-fetch engagements + entraineurs
    eng_results: dict[int, _EC | None] = {}
    if eng_ids:
        tA = time.perf_counter()
        logger.info("[3/5] Phase A: batch engagements (%d ids)...", len(eng_ids))
        try:
            all_engagements = client.list_engagements_by_ids(eng_ids)
        except FFBBApiError as e:
            all_engagements = []
            errors += 1
            logger.warning("Erreur batch engagements: %s", e)

        eng_by_id: dict[int, GetEngagementsResponse] = {}
        trainer_ids: set[int] = set()
        for eng in all_engagements:
            try:
                eid = int(eng.id)
            except (ValueError, TypeError) as e:
                logger.debug(
                    "Skipping engagement with non-integer id %r: %s",
                    getattr(eng, "id", None),
                    e,
                )
                continue
            eng_by_id[eid] = eng
            if eng.entraineur is not None:
                trainer_ids.add(eng.entraineur)
            if eng.entraineurAdjoint is not None:
                trainer_ids.add(eng.entraineurAdjoint)

        trainer_by_id: dict[int, GetEntraineursResponse] = {}
        if trainer_ids:
            try:
                all_trainers = client.list_entraineurs_by_ids(list(trainer_ids))
            except FFBBApiError as e:
                all_trainers = []
                errors += 1
                logger.warning("Erreur batch entraineurs: %s", e)
            for tr in all_trainers:
                try:
                    trainer_by_id[int(tr.idLicence)] = tr
                except (ValueError, TypeError, AttributeError) as e:
                    logger.debug(
                        "Skipping trainer with invalid idLicence %r: %s",
                        getattr(tr, "idLicence", None),
                        e,
                    )
                    continue

        for eid in eng_ids:
            eng = eng_by_id.get(eid)
            if eng is None:
                eng_results[eid] = None
                continue
            correspondant = _extract_correspondant(eng)
            entraineur = (
                _extract_entraineur_contact(
                    trainer_by_id.get(eng.entraineur), _ContactRole.ENTRAINEUR
                )
                if eng.entraineur is not None
                else None
            )
            entraineur_adj = (
                _extract_entraineur_contact(
                    trainer_by_id.get(eng.entraineurAdjoint),
                    _ContactRole.ENTRAINEUR_ADJOINT,
                )
                if eng.entraineurAdjoint is not None
                else None
            )
            eng_results[eid] = _EC(eng, correspondant, entraineur, entraineur_adj)
        logger.info(
            "[3/5] Phase A terminee: %d/%d engagements en %.2fs",
            len(eng_results),
            len(eng_ids),
            time.perf_counter() - tA,
        )

    # Phase B: Prefetch club contacts in parallel
    org_ids: set[int] = set()
    org_hit_fallback: dict[int, EngagementsHit] = {}
    for idx, (hit, _level) in enumerate(qualified):
        eid = eng_id_by_hit.get(idx)
        if eid is None:
            continue
        ec = eng_results.get(eid)
        if ec and ec.engagement.idOrganisme is not None:
            oid = ec.engagement.idOrganisme
            if oid not in org_ids:
                org_ids.add(oid)
                org_hit_fallback[oid] = hit

    club_contacts_raw: dict[int, _CC | None] = {}
    if org_ids:
        tB = time.perf_counter()
        logger.info(
            "[3/5] Phase B: prefetch clubs (%d unique org_ids)...", len(org_ids)
        )
        with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as pool:
            futures = {pool.submit(_fetch_club, oid): oid for oid in org_ids}
            for future in as_completed(futures):
                oid = futures[future]
                try:
                    _, cc = future.result()
                    club_contacts_raw[oid] = cc
                except FFBBApiError as e:
                    club_contacts_raw[oid] = None
                    errors += 1
                    logger.warning("Erreur club org_id=%s: %s", oid, e)
        logger.info(
            "[3/5] Phase B terminee: %d/%d clubs en %.2fs",
            len(club_contacts_raw),
            len(org_ids),
            time.perf_counter() - tB,
        )

    # Build club_cache from raw contacts
    for oid, cc in club_contacts_raw.items():
        if cc:
            salle_nom, salle_adresse, salle_map_url = ("", "", "")
            if cc.organisme.salle is not None:
                salle_nom, salle_adresse, salle_map_url = _resolve_salle_details(
                    client, cc.organisme.salle, salle_cache
                )
            fallback_hit = org_hit_fallback.get(oid)
            hit_logo = (
                fallback_hit.logo or fallback_hit.thumbnail or ""
                if fallback_hit
                else ""
            )
            hit_club_url = _extract_club_page_url(fallback_hit) if fallback_hit else ""
            club_cache[oid] = _extract_club_info(
                cc.organisme,
                hit_logo_fallback=hit_logo,
                hit_club_url_fallback=hit_club_url,
                salle_nom=salle_nom,
                salle_adresse=salle_adresse,
                salle_map_url=salle_map_url,
            )
        else:
            club_cache[oid] = None

    # Phase C: Batch-fetch poule snapshots
    poule_ids: set[int] = set()
    poule_id_for_hit: dict[int, int | None] = {}
    for idx, (hit, _level) in enumerate(qualified):
        eid = eng_id_by_hit.get(idx)
        poule_id: int | None = None
        try:
            if hit.id_poule and hit.id_poule.id:
                poule_id = int(hit.id_poule.id)
        except (TypeError, ValueError):
            poule_id = None
        if poule_id is None and eid is not None:
            ec = eng_results.get(eid)
            if ec and ec.engagement.idPoule is not None:
                poule_id = ec.engagement.idPoule
        poule_id_for_hit[idx] = poule_id
        if poule_id is not None:
            poule_ids.add(poule_id)

    if poule_ids:
        tC = time.perf_counter()
        logger.info(
            "[3/5] Phase C: batch poules (%d unique poule_ids)...", len(poule_ids)
        )
        try:
            poule_cache.update(
                _load_all_poule_snapshots(client, poule_ids, salle_cache)
            )
        except FFBBApiError as e:
            errors += 1
            logger.warning("Erreur batch poules: %s", e)
        logger.info(
            "[3/5] Phase C terminee: %d/%d poules en %.2fs",
            len(poule_cache),
            len(poule_ids),
            time.perf_counter() - tC,
        )

    # Phase D: Sequential assembly
    tD = time.perf_counter()
    logger.info("[3/5] Phase D: assemblage des contacts...")
    _club_contacts_added: set[int] = set()
    for idx, (hit, level) in enumerate(qualified):
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
        next_match_type = (
            hit.id_competition.type_competition.value
            if (
                hit.id_competition is not None
                and hit.id_competition.type_competition is not None
            )
            else ""
        )
        next_match_salle_name = ""
        next_match_salle_address = ""
        next_match_salle_map_url = ""
        team_lookup_name = hit.nom or hit.nom_equipe or ""
        eng_id = eng_id_by_hit.get(idx)
        contacts: list[ContactInfo] = []

        if eng_id:
            eng_contacts = eng_results.get(eng_id)
            if eng_contacts:
                engagement_updated_at = (
                    eng_contacts.engagement.date_updated
                    or eng_contacts.engagement.date_created
                )
                if (
                    eng_contacts.engagement.position is not None
                    and eng_contacts.engagement.position > 0
                ):
                    ranking_position = eng_contacts.engagement.position
                if isinstance(eng_contacts.engagement.classement, list):
                    classement_count = len(eng_contacts.engagement.classement)
                    if classement_count > 1:
                        ranking_total = classement_count
                fallback_date, fallback_opponent = _extract_next_match_from_engagement(
                    eng_contacts.engagement,
                    eng_id,
                )
                if fallback_date:
                    next_match_at = fallback_date
                    next_match_date = _format_next_match_date(fallback_date)
                    next_match_opponent = fallback_opponent
                for c in [
                    eng_contacts.correspondant,
                    eng_contacts.entraineur,
                    eng_contacts.entraineur_adjoint,
                ]:
                    if c:
                        contacts.append(c)

                org_id = eng_contacts.engagement.idOrganisme
                if org_id is not None:
                    if org_id not in _club_contacts_added:
                        _club_contacts_added.add(org_id)
                        cc = club_contacts_raw.get(org_id)
                        if cc:
                            if cc.club_contact:
                                contacts.append(cc.club_contact)
                            contacts.extend(cc.membres)

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
                                ville=ville, lat=cached.lat, lng=cached.lng
                            )

            poule_id = poule_id_for_hit.get(idx)
            if poule_id is not None:
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

        if ville and ville not in city_geo and hit.geo:
            if hit.geo.lat is not None and hit.geo.lng is not None:
                city_geo[ville] = _CityGeo(
                    ville=ville, lat=hit.geo.lat, lng=hit.geo.lng
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
                    row.next_match_type = next_match_type
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
                    next_match_type,
                    next_match_salle_name,
                    next_match_salle_address,
                    next_match_salle_map_url,
                )

    logger.info(
        "[3/5] Enrichissement termine: %d contacts, %d clubs, %d poules, %d erreurs — assemblage %.2fs",
        len(rows_by_key),
        len(club_cache),
        len(poule_cache),
        errors,
        time.perf_counter() - tD,
    )
    return rows_by_key, club_cache, club_contacts_raw, poule_cache, city_geo, errors


def _step4_compute_distances(
    lat: float,
    lng: float,
    city_geo: dict[str, _CityGeo],
    all_rows: list[_CollectedRow],
    city_name: str,
    city_code_postal: str,
) -> tuple[dict[str, float], dict[str, str], dict[str, _ClubInfo]]:
    """Compute city distances and build city_postcodes + club_infos.

    Returns (city_distances, city_postcodes, club_infos).
    """
    city_distances: dict[str, float] = {
        v: haversine_km(lat, lng, geo.lat, geo.lng) for v, geo in city_geo.items()
    }
    city_postcodes: dict[str, str] = {}
    for row in all_rows:
        if row.ville and row.code_postal and row.ville not in city_postcodes:
            city_postcodes[row.ville] = row.code_postal
    if city_code_postal and city_name not in city_postcodes:
        city_postcodes[city_name] = city_code_postal
    return city_distances, city_postcodes


def _step5_build_and_export(
    city_name: str,
    lat: float,
    lng: float,
    search_radius: float,
    all_rows: list[_CollectedRow],
    city_distances: dict[str, float],
    city_postcodes: dict[str, str],
    club_cache: dict[int, _ClubInfo | None],
    city_geo: dict[str, _CityGeo],
    accepted_echelons: frozenset[EchelonEnum] | None,
    accepted_age_groups: frozenset[AgeGroupEnum] | None,
    accepted_sexes: frozenset[SexeEnum] | None,
    out_dir: Path,
    slug: str,
    t_start: float,
) -> None:
    """Build ContactReport and export MD/CSV/HTML files."""
    t5 = time.perf_counter()
    club_infos: dict[str, _ClubInfo] = {
        info.nom: info for info in club_cache.values() if info
    }
    report = ContactReport.build(
        city_name=city_name,
        lat=lat,
        lng=lng,
        radius=search_radius,
        rows=all_rows,
        city_distances=city_distances,
        city_postcodes=city_postcodes,
        club_infos=club_infos,
        city_geo=city_geo,
        filter_echelons=accepted_echelons,
        filter_age_groups=accepted_age_groups,
        filter_sexes=accepted_sexes,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{slug}_senior_contacts.md"
    csv_path = out_dir / f"{slug}_senior_contacts.csv"
    html_path = out_dir / f"{slug}_senior_contacts.html"
    report.to_markdown(md_path)
    report.to_csv(csv_path)
    report.to_html(html_path)
    t_total = time.perf_counter() - t_start
    logger.info(
        "[5/5] %d contacts, %d clubs, %d villes → %s, %s, %s — export %.2fs, total %.2fs",
        report.total_contacts,
        report.total_clubs,
        report.total_cities,
        md_path,
        csv_path,
        html_path,
        time.perf_counter() - t5,
        t_total,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()
    slug = args.city_name.lower().replace(" ", "_")

    accepted_echelons, accepted_age_groups, accepted_sexes = _parse_cli_filters(
        args, parser
    )

    # Resolve city + create client
    t_start = time.perf_counter()
    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )
    t0 = time.perf_counter()
    lat, lng, city_code_postal, city_club_codes = resolve_city_coordinates(
        client, args.city_name
    )
    logger.info("[0/5] Résolution ville: %.2fs", time.perf_counter() - t0)

    if args.dry_run:
        effective_radius = args.radius if args.radius is not None else _CITY_RADIUS_KM
        logger.info(
            "[dry-run] %s (%.5f, %.5f), rayon %.1f km → %s/%s_senior_contacts.{md,csv,html}",
            args.city_name,
            lat,
            lng,
            effective_radius,
            args.out_dir,
            slug,
        )
        return

    # Step 1 + 2: Geo search engagements + qualify
    t1 = time.perf_counter()
    result, qualified, level_counts, search_radius = _step1_geo_search_engagements(
        client,
        args.city_name,
        lat,
        lng,
        args.radius,
        city_club_codes,
        accepted_echelons,
        accepted_age_groups,
        accepted_sexes,
    )
    t1_elapsed = time.perf_counter() - t1
    if not result or not result.hits:
        logger.warning(
            "Aucun engagement trouve autour de %s. (%.2fs)", args.city_name, t1_elapsed
        )
        return
    logger.info(
        "[1/5] %d engagements bruts trouves (rayon %.1f km) en %.2fs",
        len(result.hits),
        search_radius,
        t1_elapsed,
    )
    if not qualified:
        logger.warning("[2/5] Aucun engagement qualifie avec les filtres donnes.")
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

    # Step 3: Enrich contacts (phases A-D)
    t3 = time.perf_counter()
    salle_cache: dict[int, tuple[str, str, str]] = {}
    rows_by_key, club_cache, _club_contacts_raw, _poule_cache, city_geo, errors = (
        _step3_enrich_contacts(client, qualified, salle_cache)
    )
    logger.info(
        "[3/5] Enrichissement termine: %d contacts, %d clubs — %.2fs",
        len(rows_by_key),
        len(club_cache),
        time.perf_counter() - t3,
    )
    all_rows = list(rows_by_key.values())
    if errors:
        logger.warning("[3/5] %d erreurs API ignorees", errors)

    # Step 4: Compute distances
    t4 = time.perf_counter()
    city_distances, city_postcodes = _step4_compute_distances(
        lat, lng, city_geo, all_rows, args.city_name, city_code_postal
    )
    cities_with_geo = len(city_distances)
    cities_without = len({r.ville for r in all_rows if r.ville}) - cities_with_geo
    logger.info(
        "[4/5] Distances calculees: %d villes geoloc, %d sans coordonnees — %.2fs",
        cities_with_geo,
        max(0, cities_without),
        time.perf_counter() - t4,
    )

    # Step 5: Build report and export
    _step5_build_and_export(
        city_name=args.city_name,
        lat=lat,
        lng=lng,
        search_radius=search_radius,
        all_rows=all_rows,
        city_distances=city_distances,
        city_postcodes=city_postcodes,
        club_cache=club_cache,
        city_geo=city_geo,
        accepted_echelons=accepted_echelons,
        accepted_age_groups=accepted_age_groups,
        accepted_sexes=accepted_sexes,
        out_dir=args.out_dir,
        slug=slug,
        t_start=t_start,
    )


if __name__ == "__main__":
    main()
