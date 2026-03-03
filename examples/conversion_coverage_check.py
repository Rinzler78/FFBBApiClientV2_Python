#!/usr/bin/env python3
"""Conversion Coverage Check - Detect unhandled from_* conversion values.

Fetches thousands of real API records via Meilisearch and Directus,
captures all WARNING logs from converter_utils during parsing, and
reports any conversion warning -- surfacing exactly which key/value/enum
is unhandled.

This script is useful for:
- Detecting new enum values introduced by the FFBB API
- Finding unexpected types in API responses
- Validating that all from_* converters handle real-world data

Usage:
    python examples/conversion_coverage_check.py
    python examples/conversion_coverage_check.py --section A   # Meilisearch only
    python examples/conversion_coverage_check.py --section B   # Directus only
    python examples/conversion_coverage_check.py --section C   # FK resolution only
    python examples/conversion_coverage_check.py --section D   # Enum sweeps only
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from typing import Any

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

# Logger targeted by all from_* helpers
_CONVERTER_LOGGER = "ffbb_api_client_v2.utils.converter_utils"

# Rate-limit delay between API calls (seconds)
_RATE_DELAY = 0.3

# Meilisearch max per query
_MLS_LIMIT = 1000

# Directus bulk page ceiling
_DIR_MAX = 2000

# Max FK IDs to resolve per type
_FK_BATCH = 10


# ---------------------------------------------------------------------------
# WarningCollector
# ---------------------------------------------------------------------------
class WarningCollector(logging.Handler):
    """Captures WARNING+ log records from converter_utils."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self._records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self._records.append(record)

    def drain(self) -> list[str]:
        """Return formatted messages and clear buffer."""
        msgs = [self.format(r) for r in self._records]
        self._records.clear()
        return msgs


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _extract_ids(items: list[Any] | None, limit: int = _FK_BATCH) -> list[int]:
    if not items:
        return []
    ids: list[int] = []
    for item in items:
        if isinstance(item, int):
            ids.append(item)
        elif isinstance(item, dict) and "id" in item:
            try:
                ids.append(int(item["id"]))
            except (ValueError, TypeError):
                pass
        else:
            item_id = getattr(item, "id", None)
            if item_id is not None:
                try:
                    ids.append(int(item_id))
                except (ValueError, TypeError):
                    pass
        if len(ids) >= limit:
            break
    return ids


def _extract_str_ids(items: list[Any] | None, limit: int = _FK_BATCH) -> list[str]:
    if not items:
        return []
    ids: list[str] = []
    for item in items:
        if isinstance(item, str):
            ids.append(item)
        elif isinstance(item, dict) and "id" in item:
            ids.append(str(item["id"]))
        else:
            item_id = getattr(item, "id", None)
            if item_id is not None:
                ids.append(str(item_id))
        if len(ids) >= limit:
            break
    return ids


def _report(label: str, warnings: list[str]) -> bool:
    """Print check result. Returns True if warnings found."""
    if warnings:
        print(f"  WARN  {label}: {len(warnings)} warning(s)")
        for w in warnings[:20]:
            print(f"         - {w}")
        if len(warnings) > 20:
            print(f"         ... and {len(warnings) - 20} more")
        return True
    print(f"  OK    {label}")
    return False


# ---------------------------------------------------------------------------
# ID Discovery
# ---------------------------------------------------------------------------
def discover_ids(
    client: FFBBAPIClientV2, collector: WarningCollector
) -> dict[str, list]:
    """Chain through live data to collect IDs for FK resolution."""
    print("\n--- Discovering IDs for FK resolution ---")
    ids: dict[str, list] = {
        "organismes": [],
        "salles": [],
        "engagements": [],
        "competitions": [],
        "poules": [],
        "rencontres": [],
        "terrains": [],
        "tournois": [],
        "formations": [],
    }

    # 1) Search organismes
    org_result = client.search_organismes(None, limit=_MLS_LIMIT)
    if org_result and org_result.hits:
        for hit in org_result.hits[:_FK_BATCH]:
            if hit.id is not None:
                try:
                    ids["organismes"].append(int(hit.id))
                except (ValueError, TypeError):
                    pass

    # 2) Get organisme details -> salle + engagement IDs
    for org_id in ids["organismes"][:5]:
        time.sleep(_RATE_DELAY)
        org = client.get_organisme(org_id)
        if org is not None:
            if isinstance(org.salle, int):
                ids["salles"].append(org.salle)
            remaining = _FK_BATCH - len(ids["engagements"])
            if remaining > 0:
                ids["engagements"].extend(_extract_ids(org.engagements, remaining))
            remaining = _FK_BATCH - len(ids["competitions"])
            if remaining > 0:
                ids["competitions"].extend(_extract_ids(org.competitions, remaining))

    # 3) Engagement details -> competition + poule IDs
    for eng_id in ids["engagements"][:5]:
        time.sleep(_RATE_DELAY)
        eng = client.get_engagement(eng_id)
        if eng is not None:
            if isinstance(eng.idCompetition, int):
                if eng.idCompetition not in ids["competitions"]:
                    ids["competitions"].append(eng.idCompetition)
            if isinstance(eng.idPoule, int):
                ids["poules"].append(eng.idPoule)

    # 4) Poule details -> rencontre IDs
    for poule_id in ids["poules"][:3]:
        time.sleep(_RATE_DELAY)
        poule = client.get_poule(poule_id)
        if poule is not None:
            remaining = _FK_BATCH - len(ids["rencontres"])
            if remaining > 0:
                ids["rencontres"].extend(_extract_ids(poule.rencontres, remaining))

    # 5-7) Search for terrains, tournois, formations
    for key, search_fn in [
        ("terrains", client.search_terrains),
        ("tournois", client.search_tournois),
    ]:
        time.sleep(_RATE_DELAY)
        result = search_fn(None, limit=100)
        if result and result.hits:
            for hit in result.hits[:_FK_BATCH]:
                if hit.id is not None:
                    try:
                        ids[key].append(int(hit.id))
                    except (ValueError, TypeError):
                        pass

    time.sleep(_RATE_DELAY)
    form_result = client.search_formations(None, limit=100)
    if form_result and form_result.hits:
        ids["formations"] = _extract_str_ids(form_result.hits, _FK_BATCH)

    # Drain discovery warnings (not part of checks)
    collector.drain()

    for key, vals in ids.items():
        print(f"  {key}: {len(vals)} IDs")
    return ids


# ---------------------------------------------------------------------------
# Section runners
# ---------------------------------------------------------------------------
def run_section_a(client: FFBBAPIClientV2, collector: WarningCollector) -> int:
    """Section A: Meilisearch bulk search coverage."""
    print("\n=== Section A: Meilisearch Bulk Search ===")
    total_warns = 0

    checks: list[tuple[str, Any, list[str | None]]] = [
        (
            "search_organismes",
            client.search_organismes,
            [None, "Paris", "Lyon", "Marseille"],
        ),
        (
            "search_competitions",
            client.search_competitions,
            [None, "Championnat", "Coupe", "3x3", "Plateau"],
        ),
        (
            "search_rencontres",
            client.search_rencontres,
            [None, "Paris", "3x3", "Handisport"],
        ),
        ("search_salles", client.search_salles, [None, "Paris", "Lyon"]),
        ("search_terrains", client.search_terrains, [None, "Paris", "Lyon"]),
        (
            "search_tournois",
            client.search_tournois,
            [None, "3x3", "Féminin", "Masculin"],
        ),
        (
            "search_pratiques",
            client.search_pratiques,
            [None, "basket", "santé", "inclusif"],
        ),
        ("search_engagements", client.search_engagements, [None, "Paris", "Pro"]),
        ("search_formations", client.search_formations, [None, "arbitrage"]),
    ]

    for label, search_fn, queries in checks:
        collector.drain()
        for q in queries:
            search_fn(q, limit=_MLS_LIMIT)
        warnings = collector.drain()
        if _report(label, warnings):
            total_warns += len(warnings)
        time.sleep(_RATE_DELAY)

    return total_warns


def run_section_b(client: FFBBAPIClientV2, collector: WarningCollector) -> int:
    """Section B: Directus bulk list coverage."""
    print("\n=== Section B: Directus Bulk List ===")
    total_warns = 0

    checks: list[tuple[str, Any, dict]] = [
        ("get_saisons", client.get_saisons, {"filter_criteria": None}),
        ("list_all_rencontres", client.list_all_rencontres, {"max_items": _DIR_MAX}),
        ("list_all_salles", client.list_all_salles, {"max_items": _DIR_MAX}),
        ("list_all_terrains", client.list_all_terrains, {"max_items": _DIR_MAX}),
        ("list_all_tournois", client.list_all_tournois, {"max_items": _DIR_MAX}),
        ("list_all_engagements", client.list_all_engagements, {"max_items": _DIR_MAX}),
        ("list_all_formations", client.list_all_formations, {"max_items": _DIR_MAX}),
        ("list_all_pratiques", client.list_all_pratiques, {"max_items": _DIR_MAX}),
        ("list_all_communes", client.list_all_communes, {"max_items": _DIR_MAX}),
        ("get_lives", client.get_lives, {}),
    ]

    for label, list_fn, kwargs in checks:
        collector.drain()
        list_fn(**kwargs)
        warnings = collector.drain()
        if _report(label, warnings):
            total_warns += len(warnings)
        time.sleep(_RATE_DELAY)

    return total_warns


def run_section_c(
    client: FFBBAPIClientV2,
    collector: WarningCollector,
    ids: dict[str, list],
) -> int:
    """Section C: FK resolution chain."""
    print("\n=== Section C: FK Resolution Chain ===")
    total_warns = 0

    fk_checks: list[tuple[str, str, Any]] = [
        ("get_organisme", "organismes", client.get_organisme),
        ("get_competition", "competitions", client.get_competition),
        ("get_poule", "poules", client.get_poule),
        ("get_engagement", "engagements", client.get_engagement),
        ("get_rencontre", "rencontres", client.get_rencontre),
        ("get_salle", "salles", client.get_salle),
        ("get_terrain", "terrains", client.get_terrain),
        ("get_tournoi", "tournois", client.get_tournoi),
        ("get_formation", "formations", client.get_formation),
    ]

    for label, id_key, get_fn in fk_checks:
        id_list = ids.get(id_key, [])
        if not id_list:
            print(f"  SKIP  {label}: no IDs discovered")
            continue
        collector.drain()
        for item_id in id_list[:_FK_BATCH]:
            get_fn(item_id)
            time.sleep(_RATE_DELAY)
        warnings = collector.drain()
        if _report(label, warnings):
            total_warns += len(warnings)

    return total_warns


def run_section_d(client: FFBBAPIClientV2, collector: WarningCollector) -> int:
    """Section D: High-diversity enum sweeps."""
    print("\n=== Section D: High-Diversity Enum Sweeps ===")
    total_warns = 0

    sweeps: list[tuple[str, Any, list[str | None]]] = [
        (
            "sweep_competitions",
            client.search_multiple_competitions,
            [None, "Championnat", "Coupe", "3x3", "Féminin", "Mixte"],
        ),
        (
            "sweep_rencontres",
            client.search_multiple_rencontres,
            [None, "Départemental", "Régional", "National", "3x3"],
        ),
        (
            "sweep_tournois",
            client.search_multiple_tournois,
            [None, "3x3", "5x5", "Féminin", "Masculin"],
        ),
        (
            "sweep_terrains",
            client.search_multiple_terrains,
            [None, "Paris", "Lyon", "Marseille"],
        ),
        (
            "sweep_pratiques",
            client.search_multiple_pratiques,
            [None, "basket", "santé", "inclusif", "tonik"],
        ),
    ]

    for label, search_fn, queries in sweeps:
        collector.drain()
        search_fn(queries, limit=_MLS_LIMIT)
        warnings = collector.drain()
        if _report(label, warnings):
            total_warns += len(warnings)
        time.sleep(_RATE_DELAY)

    return total_warns


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Conversion coverage check")
    parser.add_argument(
        "--section",
        choices=["A", "B", "C", "D"],
        help="Run only one section (A=Meilisearch, B=Directus, C=FK, D=Sweeps)",
    )
    args = parser.parse_args()

    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )

    collector = WarningCollector()
    logging.getLogger(_CONVERTER_LOGGER).addHandler(collector)

    sections = args.section.upper() if args.section else "ABCD"
    total_warns = 0

    # Discover IDs if FK resolution needed
    ids: dict[str, list] = {}
    if "C" in sections:
        ids = discover_ids(client, collector)

    if "A" in sections:
        total_warns += run_section_a(client, collector)
    if "B" in sections:
        total_warns += run_section_b(client, collector)
    if "C" in sections:
        total_warns += run_section_c(client, collector, ids)
    if "D" in sections:
        total_warns += run_section_d(client, collector)

    logging.getLogger(_CONVERTER_LOGGER).removeHandler(collector)

    # Summary
    print("\n" + "=" * 60)
    if total_warns == 0:
        print("ALL CHECKS PASSED - no conversion warnings detected")
    else:
        print(f"WARNINGS DETECTED: {total_warns} total conversion warning(s)")
        print("These indicate unhandled enum values or unexpected types in API data.")
    print("=" * 60)

    sys.exit(1 if total_warns > 0 else 0)


if __name__ == "__main__":
    main()
