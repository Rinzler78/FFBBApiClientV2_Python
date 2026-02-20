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
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.exceptions import FFBBServerError
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
                    poules = sorted({p for r in t_rows for p in r.poules if p})
                    ranking_url = ""
                    competition_logo_url = ""
                    for r in t_rows:
                        if not ranking_url and r.ranking_url:
                            ranking_url = r.ranking_url
                        if not competition_logo_url and r.competition_logo_url:
                            competition_logo_url = r.competition_logo_url
                        if ranking_url and competition_logo_url:
                            break
                    contacts = [
                        ReportContact(
                            role=r.titre,
                            nom=r.nom,
                            prenom=r.prenom,
                            telephone=r.telephone,
                            email=r.email,
                            source=r.source,
                        )
                        for r in sorted(t_rows, key=lambda x: (x.nom, x.prenom))
                    ]
                    report_teams.append(
                        ReportTeam(
                            sexe=sexe,
                            niveau=niveau,
                            division=division,
                            poules=poules,
                            ranking_url=ranking_url,
                            competition_logo_url=competition_logo_url,
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
                    f"<li><a href='#{anchor}'>{h(city.ville)}"
                    f"<span class='sidebar-dist'>{dist} km</span></a></li>\n"
                )
            f.write(
                "<li class='sidebar-annuaire'>"
                "<a href='#annuaire'>&#x1F4D6; Annuaire</a></li>\n"
            )
            f.write("</ul>\n</nav>\n\n")

            # --- Main content ---
            f.write("<main class='content'>\n")

            # Header
            f.write("<header>\n")
            f.write(
                f"<h1>Contacts Basketball Senior" f" &mdash; {h(self.city_name)}</h1>\n"
            )
            f.write("<table class='params'>\n")
            f.write("<tr><th>Ville</th>")
            f.write(f"<td><strong>{h(self.city_name)}</strong></td></tr>\n")
            f.write("<tr><th>Position</th>")
            f.write(f"<td>{self.lat:.4f}, {self.lng:.4f}</td></tr>\n")
            f.write("<tr><th>Rayon</th>")
            f.write(f"<td>{self.radius:.0f} km</td></tr>\n")
            f.write("<tr><th>Niveaux</th><td>Pro, National</td></tr>\n")
            f.write("<tr><th>Sexe</th><td>Masculin, Feminin</td></tr>\n")
            f.write("<tr><th>Tranches d'ages</th><td>Senior</td></tr>\n")
            f.write("</table>\n")
            f.write(f"<p class='date'>{h(self.timestamp)}</p>\n")
            f.write("</header>\n\n")

            # Summary stats
            f.write("<section class='summary'>\n")
            f.write("<div class='stat-grid'>\n")
            for label, val in [
                ("Villes", self.total_cities),
                ("Clubs", self.total_clubs),
                ("Equipes", self.total_teams),
                ("Contacts", self.total_contacts),
            ]:
                f.write(
                    f"<div class='stat'>"
                    f"<span class='stat-val'>{val}</span>"
                    f"<span class='stat-label'>{label}</span></div>\n"
                )
            f.write("</div>\n</section>\n\n")

            # Map
            f.write("<section id='map-section'>\n")
            f.write("<h2>Carte</h2>\n")
            f.write("<div id='map'></div>\n")
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
                    f"<li><a href='#{anchor}'>" f"{h(city.ville)} — {dist}</a></li>\n"
                )
            f.write(
                "<li><a href='#annuaire'>" "&#x1F4D6; Annuaire des contacts</a></li>\n"
            )
            f.write("</ul>\n</details>\n\n")

            # Contacts detail by city
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
                is_target = city.ville.lower() == self.city_name.lower()
                f.write(
                    f"<section class='city-section' id='{anchor}'>\n"
                    f"<h2>{h(label)} &mdash; {dist}</h2>\n"
                )
                if city.clubs:
                    for club in city.clubs:
                        self._write_html_club_card(f, club)
                elif is_target:
                    f.write(
                        "<p class='empty-city'>Aucune equipe Pro ou National"
                        f" a <strong>{h(self.city_name)}</strong>."
                        f" Recherche elargie a {self.radius:.0f}&nbsp;km.</p>\n"
                    )
                f.write(
                    "<p class='nav'>" "<a href='#map-section'>&#x2191; Carte</a></p>\n"
                )
                f.write("</section>\n\n")

            # Annuaire — all contacts, deduplicated
            self._write_html_annuaire(f)

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
            f.write("</script>\n")
            f.write("</body>\n</html>\n")

    def _write_html_club_card(self, f, club: ReportClub) -> None:
        """Write a single club card with logo, links, teams, contacts."""
        h = _html_escape
        f.write("<div class='club-card'>\n")

        # Club header row
        f.write("<div class='club-header'>\n")
        if club.logo_url:
            f.write(
                f"<img class='club-logo' src='{h(club.logo_url)}'"
                f" alt='' loading='lazy'"
                f" onerror=\"this.style.display='none'\">\n"
            )
        else:
            f.write("<span class='club-logo-placeholder'>&#x1F3C0;</span>\n")
        f.write("<div class='club-info'>\n")
        f.write(f"<h3 class='club-name'>{h(club.nom)}</h3>\n")
        if club.adresse:
            f.write(f"<p class='address'>{h(club.adresse)}</p>\n")
        f.write("</div>\n</div>\n")

        # Action links row
        links: list[str] = []
        dir_url = _directions_url(club.lat, club.lng, club.adresse)
        if dir_url:
            links.append(
                f"<a href='{h(dir_url)}' target='_blank'"
                f" title='Itineraire Google Maps'"
                f" class='action-link'>&#x1F4CD; Itineraire</a>"
            )
        if club.site_web:
            url = club.site_web
            if not url.startswith("http"):
                url = "https://" + url
            links.append(
                f"<a href='{h(url)}' target='_blank'"
                f" title='Site web du club'"
                f" class='action-link'>&#x1F310; Site web</a>"
            )
        if club.url_ffbb:
            ffbb_url = club.url_ffbb
            if not ffbb_url.startswith("http"):
                ffbb_url = f"{_COMPETITIONS_BASE}{ffbb_url}"
            links.append(
                f"<a href='{h(ffbb_url)}' target='_blank'"
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

        # Club-level contacts FIRST (at the top of the club card)
        if club.club_contacts:
            f.write("<div class='team club-contacts-section'>\n")
            f.write("<span class='badge badge-club'>Contacts club</span>\n")
            self._write_html_contact_table(f, club.club_contacts, with_refs=True)
            f.write("</div>\n")

        # Teams with their contacts
        for team in club.teams:
            f.write("<div class='team'>\n")
            # Competition logo + badges
            if team.competition_logo_url:
                f.write(
                    f"<img src='{h(team.competition_logo_url)}'"
                    f" alt='{h(team.division)}' class='competition-logo'"
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
            if team.poules:
                f.write(
                    f" <span class='team-poules'>{h(' / '.join(team.poules))}</span>"
                )
            if team.ranking_url:
                f.write(
                    f" <a href='{h(team.ranking_url)}' target='_blank'"
                    f" class='ranking-link'>Classement &#x2197;</a>"
                )
            f.write("\n")
            self._write_html_contact_table(f, team.contacts, with_refs=True)
            f.write("</div>\n")

        f.write("</div>\n")

    @staticmethod
    def _write_html_contact_table(
        f,
        contacts: list[ReportContact],
        *,
        with_refs: bool = False,
    ) -> None:
        h = _html_escape
        f.write("<table class='contacts'>\n<thead><tr>")
        for col in ["Role", "Nom", "Tel", "Email"]:
            f.write(f"<th>{col}</th>")
        f.write("</tr></thead>\n<tbody>\n")
        for c in contacts:
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
            nom_full = f"{c.nom} {c.prenom}".strip()
            role_class = _role_css_class(c.role)
            cid = _contact_id(c)
            nom_cell = h(nom_full)
            if with_refs:
                nom_cell = (
                    f"<a href='#{h(cid)}' class='contact-ref'"
                    f" title='Voir dans l&#39;annuaire'>"
                    f"{h(nom_full)}</a>"
                )
            f.write(
                f"<tr><td><span class='badge {role_class}'>"
                f"{h(c.role)}</span></td>"
                f"<td>{nom_cell}</td>"
                f"<td>{tel_cell}</td>"
                f"<td>{email_cell}</td></tr>\n"
            )
        f.write("</tbody></table>\n")

    def _write_leaflet_js(self, f) -> None:
        """Write the Leaflet map initialization script."""
        h = _html_escape

        # Collect all club markers
        markers: list[dict] = []
        for city in self.cities:
            for club in city.clubs:
                lat = club.lat
                lng = club.lng
                if lat is None or lng is None:
                    continue
                dir_url = _directions_url(lat, lng, club.adresse)
                popup = f"<strong>{_html_escape(club.nom)}</strong>"
                if club.adresse:
                    popup += f"<br><em>{_html_escape(club.adresse)}</em>"
                if dir_url:
                    popup += (
                        f"<br><a href='{_html_escape(dir_url)}'"
                        f" target='_blank'>Itineraire</a>"
                    )
                markers.append(
                    {
                        "lat": lat,
                        "lng": lng,
                        "popup": popup,
                        "name": club.nom,
                    }
                )

        markers_json = json.dumps(markers, ensure_ascii=False)

        f.write(f"""\
(function() {{
  var center = [{self.lat}, {self.lng}];
  var map = L.map('map').setView(center, 8);
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 18
  }}).addTo(map);

  // Center marker (not in cluster)
  var centerIcon = L.divIcon({{
    className: 'center-marker',
    html: '<div style="background:#DC2626;width:16px;height:16px;'
      + 'border-radius:50%;border:3px solid #fff;'
      + 'box-shadow:0 0 6px rgba(0,0,0,0.4)"></div>',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  }});
  L.marker(center, {{icon: centerIcon, zIndexOffset: 1000}})
    .bindPopup('<strong>Centre de recherche</strong><br>{h(self.city_name)}')
    .addTo(map);

  // Radius circle
  L.circle(center, {{
    radius: {self.radius * 1000},
    color: '#F26522',
    fillColor: '#F26522',
    fillOpacity: 0.05,
    weight: 2,
    dashArray: '8 4'
  }}).addTo(map);

  // Club markers inside a cluster group
  var clubIcon = L.divIcon({{
    className: 'club-marker',
    html: '<div style="background:#F26522;width:12px;height:12px;'
      + 'border-radius:50%;border:2px solid #fff;'
      + 'box-shadow:0 0 4px rgba(0,0,0,0.3)"></div>',
    iconSize: [12, 12],
    iconAnchor: [6, 6]
  }});

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
  var bounds = L.latLngBounds([center]);
  data.forEach(function(m) {{
    var marker = L.marker([m.lat, m.lng], {{icon: clubIcon}})
      .bindPopup(m.popup);
    clusters.addLayer(marker);
    bounds.extend([m.lat, m.lng]);
  }});
  map.addLayer(clusters);

  if (data.length > 0) {{
    map.fitBounds(bounds, {{padding: [30, 30]}});
  }}
}})();
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
:root {
  --bg: #FAFBFC;
  --surface: #FFFFFF;
  --text: #1F2937;
  --muted: #6B7280;
  --border: #E5E7EB;
  --accent: #F26522;
  --accent-dark: #D4540E;
  --accent-light: #FFF4ED;
  --radius: 8px;
  --sidebar-w: 220px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
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
  max-width: 960px;
  padding: 2rem 2rem 2rem 2.5rem;
}

/* Header */
header {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 3px solid var(--accent);
}
h1 {
  font-size: 1.6rem;
  margin-bottom: 1rem;
  color: var(--accent);
}
h2 {
  font-size: 1.2rem;
  margin: 1.5rem 0 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
table.params {
  border-collapse: collapse;
  margin-bottom: 0.5rem;
}
table.params th {
  text-align: left;
  padding: 0.2rem 1rem 0.2rem 0;
  color: var(--muted);
  font-weight: normal;
  font-size: 0.85rem;
}
table.params td { padding: 0.2rem 0; font-size: 0.85rem; }
.date { color: var(--muted); font-size: 0.82rem; }

/* Stats */
.summary { margin: 1rem 0 1.5rem; }
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

/* Map */
#map {
  height: 420px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
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
  margin-top: 0.5rem;
  padding-top: 0.5rem;
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
.badge-pro { background: #EDE9FE; color: #7C3AED; }
.badge-national { background: #FEE2E2; color: #DC2626; }
.badge-ligue { background: #DBEAFE; color: #2563EB; }
.badge-sexe { background: #F3F4F6; color: #4B5563; }
.badge-div { background: #F3F4F6; color: #6B7280; font-weight: 400; }
.badge-club { background: var(--accent-light); color: var(--accent-dark); }
.badge-president { background: #FEF3C7; color: #92400E; }
.badge-coach { background: #D1FAE5; color: #065F46; }
.badge-correspondant { background: #DBEAFE; color: #1E40AF; }
.badge-role { background: #F3F4F6; color: #4B5563; }
.team-poules {
  font-size: 0.8rem;
  color: var(--muted);
  margin-left: 0.25rem;
}
.ranking-link {
  font-size: 0.78rem;
  color: var(--accent);
  text-decoration: none;
  margin-left: 0.5rem;
}
.ranking-link:hover { text-decoration: underline; }
.competition-logo {
  vertical-align: middle;
  margin-right: 0.35rem;
  border-radius: 4px;
}

/* Contact tables */
table.contacts {
  width: 100%;
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
}
table.contacts tr:hover { background: #FFFBF5; }
table.contacts a { color: var(--accent-dark); }

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
  .sidebar, #map-section, .mobile-nav, p.nav, .club-actions { display: none; }
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
  .content { margin-left: 0; padding: 1.5rem 1rem; }
  .mobile-nav { display: block; }
}
@media (max-width: 767px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  #map { height: 280px; }
  .club-actions { gap: 0.3rem; }
  .action-link { font-size: 0.72rem; }
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
    ranking_url: str
    competition_logo_url: str


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


def _extract_club_info(
    organisme: GetOrganismeResponse,
    hit_logo_fallback: str = "",
    hit_club_url_fallback: str = "",
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
    ranking_url: str,
    competition_logo_url: str,
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
        ranking_url=ranking_url,
        competition_logo_url=competition_logo_url,
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
    rows_by_key: dict[tuple[str, ...], _CollectedRow] = {}
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

        # Logo fallback from Meilisearch hit
        hit_logo = hit.logo or hit.thumbnail or ""

        try:
            eng_id = int(hit.id) if hit.id else None
        except (ValueError, TypeError):
            eng_id = None

        contacts: list[ContactInfo] = []

        if eng_id:
            try:
                api_calls += 1
                eng_contacts = client.get_engagement_contacts(eng_id)
                if eng_contacts:
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
                                    info = _extract_club_info(
                                        club_contacts.organisme,
                                        hit_logo_fallback=hit_logo,
                                        hit_club_url_fallback=_extract_club_page_url(
                                            hit
                                        ),
                                    )
                                    club_cache[org_id] = info
                                    if club_contacts.club_contact:
                                        contacts.append(club_contacts.club_contact)
                                    contacts.extend(club_contacts.membres)
                                else:
                                    club_cache[org_id] = None
                            except FFBBServerError as e:
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
            except FFBBServerError as e:
                errors += 1
                logger.debug("Erreur engagement id=%s: %s", eng_id, e)

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
                    ranking_url,
                    competition_logo_url,
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
