#!/usr/bin/env python3
"""
Discover Directus collections accessible via the FFBB API.

Uses a dual strategy:
1. Introspection: Try native Directus endpoints (/server/info, /collections,
   /fields, /relations) which may be blocked by permissions.
2. Brute-force: Probe ~50 candidate collection names via GET /items/{name}?limit=1
   to discover accessible collections and their fields.

Generates data/directus_collections_discovery.json.

Usage:
    python scripts/discover_directus_collections.py
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ffbb_api_client_v2._http.client import HttpClient
from ffbb_api_client_v2.directus.client import DEFAULT_USER_AGENT
from ffbb_api_client_v2.directus_ffbb.config import (
    API_FFBB_BASE_URL,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_CONFIGURATION,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
)
from ffbb_api_client_v2.facade.token_manager import TokenManager

PROJECT_ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Known Directus endpoints from config.py (items/* only)
KNOWN_ENDPOINTS: dict[str, str] = {
    "configuration": ENDPOINT_CONFIGURATION,
    "ffbbserver_competitions": ENDPOINT_COMPETITIONS,
    "ffbbserver_poules": ENDPOINT_POULES,
    "ffbbserver_saisons": ENDPOINT_SAISONS,
    "ffbbserver_organismes": ENDPOINT_ORGANISMES,
}

# Candidate collection names to probe via brute-force
# Sources: config.py endpoints, Meilisearch index UIDs, model field entities,
# Directus system collections, common FFBB entity names
CANDIDATE_COLLECTIONS = [
    # --- Known from config.py ---
    "configuration",
    "ffbbserver_competitions",
    "ffbbserver_poules",
    "ffbbserver_saisons",
    "ffbbserver_organismes",
    # --- Meilisearch index mirrors (may exist as Directus collections) ---
    "ffbbserver_rencontres",
    "ffbbserver_terrains",
    "ffbbserver_salles",
    "ffbbserver_tournois",
    "ffbbserver_engagements",
    "ffbbserver_formations",
    "ffbbnational_pratiques",
    # --- Entities seen in model field paths ---
    "ffbbserver_categories",
    "ffbbserver_communes",
    "ffbbserver_phases",
    "ffbbserver_journees",
    "ffbbserver_classements",
    "ffbbserver_equipes",
    "ffbbserver_joueurs",
    "ffbbserver_licencies",
    "ffbbserver_licences",
    "ffbbserver_clubs",
    "ffbbserver_arbitres",
    "ffbbserver_entraineurs",
    "ffbbserver_officiels",
    "ffbbserver_resultats",
    "ffbbserver_statistiques",
    "ffbbserver_calendriers",
    "ffbbserver_matchs",
    "ffbbserver_lives",
    "ffbbserver_actualites",
    "ffbbserver_documents",
    "ffbbserver_medias",
    "ffbbserver_photos",
    "ffbbserver_videos",
    "ffbbserver_evenements",
    "ffbbserver_inscriptions",
    "ffbbserver_transferts",
    "ffbbserver_mutations",
    "ffbbserver_affiliations",
    "ffbbserver_palmares",
    "ffbbserver_selections",
    "ffbbserver_convocations",
    # --- National prefix variants ---
    "ffbbnational_competitions",
    "ffbbnational_organismes",
    "ffbbnational_rencontres",
    "ffbbnational_formations",
    # --- Directus system collections ---
    "directus_users",
    "directus_roles",
    "directus_files",
    "directus_folders",
    "directus_activity",
    "directus_collections",
    "directus_fields",
    "directus_permissions",
    "directus_settings",
]


# ---------------------------------------------------------------------------
# Strategy 1: Directus Introspection API
# ---------------------------------------------------------------------------

INTROSPECTION_ENDPOINTS = {
    "server_info": "server/info",
    "collections": "collections",
    "fields": "fields",
    "relations": "relations",
}


def try_introspection_endpoint(
    base_url: str, headers: dict[str, str], path: str
) -> tuple[int, Any]:
    """Try a Directus introspection endpoint. Returns (status_code, json_or_None)."""
    url = f"{base_url}{path}"
    try:
        response = HttpClient.http_get(url, headers)
        status = response.status_code
        if status == 200:
            return status, response.json()
        return status, None
    except Exception as e:
        logger.warning(f"  Error fetching {path}: {e}")
        return 0, None


def run_introspection(base_url: str, headers: dict[str, str]) -> dict[str, Any]:
    """Run all introspection endpoints and return parsed results."""
    results: dict[str, Any] = {}

    for name, path in INTROSPECTION_ENDPOINTS.items():
        logger.info(f"  Trying introspection: {path}")
        status, data = try_introspection_endpoint(base_url, headers, path)

        if status == 200 and data is not None:
            logger.info(f"    -> ACCESSIBLE (HTTP {status})")
            if name == "server_info":
                results[name] = data.get("data", data)
            elif name == "collections":
                results[name] = parse_collections_response(data)
            elif name == "fields":
                results[name] = parse_fields_response(data)
            elif name == "relations":
                results[name] = parse_relations_response(data)
        else:
            logger.info(f"    -> BLOCKED (HTTP {status})")
            results[name] = None

    return results


def parse_collections_response(data: Any) -> list[dict[str, Any]]:
    """Parse /collections response into a summary list."""
    raw = data.get("data", []) if isinstance(data, dict) else []
    collections = []
    for item in raw:
        collections.append(
            {
                "collection": item.get("collection"),
                "hidden": (
                    item.get("meta", {}).get("hidden", False)
                    if item.get("meta")
                    else None
                ),
                "singleton": (
                    item.get("meta", {}).get("singleton", False)
                    if item.get("meta")
                    else None
                ),
                "note": item.get("meta", {}).get("note") if item.get("meta") else None,
            }
        )
    return collections


def parse_fields_response(data: Any) -> dict[str, Any]:
    """Parse /fields response grouped by collection."""
    raw = data.get("data", []) if isinstance(data, dict) else []
    grouped: dict[str, list[str]] = {}
    for item in raw:
        collection = item.get("collection", "unknown")
        field = item.get("field", "unknown")
        grouped.setdefault(collection, []).append(field)
    return {
        col: {"count": len(fields), "fields": sorted(fields)}
        for col, fields in sorted(grouped.items())
    }


def parse_relations_response(data: Any) -> list[dict[str, Any]]:
    """Parse /relations response into a summary list."""
    raw = data.get("data", []) if isinstance(data, dict) else []
    relations = []
    for item in raw:
        relations.append(
            {
                "many_collection": item.get("many_collection"),
                "many_field": item.get("many_field"),
                "one_collection": item.get("one_collection"),
                "one_field": item.get("one_field"),
            }
        )
    return relations


# ---------------------------------------------------------------------------
# Strategy 2: Brute-force collection probing
# ---------------------------------------------------------------------------


def flatten_keys(obj: Any, prefix: str = "") -> set[str]:
    """Recursively flatten JSON keys into dot-separated paths."""
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.add(full_key)
            keys.update(flatten_keys(v, full_key))
    elif isinstance(obj, list):
        for item in obj:
            keys.update(flatten_keys(item, prefix))
    return keys


def probe_collection(
    base_url: str, headers: dict[str, str], collection: str
) -> dict[str, Any]:
    """Probe a single collection via GET /items/{collection}?limit=1&fields[]=*.*."""
    url = HttpClient.url_with_params(
        f"{base_url}items/{collection}",
        {"limit": "1", "fields[]": ["*.*"]},
    )
    try:
        response = HttpClient.http_get(url, headers)
        status = response.status_code

        if status == 200:
            data = response.json()
            actual_data = data.get("data", data)
            if isinstance(actual_data, list) and actual_data:
                sample = actual_data[0]
            elif isinstance(actual_data, dict):
                sample = actual_data
            else:
                return {
                    "exists": True,
                    "status": status,
                    "field_count": 0,
                    "fields": [],
                    "empty": True,
                }

            fields = flatten_keys(sample)
            return {
                "exists": True,
                "status": status,
                "field_count": len(fields),
                "fields": sorted(fields),
            }
        elif status == 403:
            return {"exists": None, "status": status, "reason": "forbidden"}
        elif status == 401:
            return {"exists": None, "status": status, "reason": "unauthorized"}
        else:
            return {"exists": False, "status": status}

    except Exception as e:
        return {"exists": False, "status": 0, "error": str(e)}


def run_brute_force(
    base_url: str, headers: dict[str, str]
) -> dict[str, dict[str, Any]]:
    """Probe all candidate collections."""
    results: dict[str, dict[str, Any]] = {}

    for i, collection in enumerate(sorted(set(CANDIDATE_COLLECTIONS)), 1):
        if i % 10 == 0:
            logger.info(f"  Progress: {i}/{len(set(CANDIDATE_COLLECTIONS))}...")
        result = probe_collection(base_url, headers, collection)

        if result["exists"] is True:
            status_label = "KNOWN" if collection in KNOWN_ENDPOINTS else "NEW"
            logger.info(
                f"  FOUND [{status_label}]: items/{collection} "
                f"({result.get('field_count', 0)} fields)"
            )
        elif result["exists"] is None:
            logger.info(f"  FORBIDDEN: items/{collection} (HTTP {result['status']})")

        results[collection] = result

    return results


# ---------------------------------------------------------------------------
# Summary & Output
# ---------------------------------------------------------------------------


def print_summary(
    introspection: dict[str, Any],
    brute_force: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Print summary report and return summary dict."""
    found = {k: v for k, v in brute_force.items() if v.get("exists") is True}
    forbidden = {k: v for k, v in brute_force.items() if v.get("exists") is None}
    not_found = [k for k, v in brute_force.items() if v.get("exists") is False]

    new_collections = {k: v for k, v in found.items() if k not in KNOWN_ENDPOINTS}
    confirmed_known = {k: v for k, v in found.items() if k in KNOWN_ENDPOINTS}

    introspection_available = {
        name: introspection.get(name) is not None for name in INTROSPECTION_ENDPOINTS
    }

    summary = {
        "introspection_available": introspection_available,
        "candidates_tested": len(set(CANDIDATE_COLLECTIONS)),
        "collections_found": len(found),
        "new_collections": len(new_collections),
        "confirmed_known": len(confirmed_known),
        "forbidden_collections": len(forbidden),
        "not_found": len(not_found),
    }

    print("\n" + "=" * 60)
    print("  DIRECTUS COLLECTION DISCOVERY REPORT")
    print("=" * 60)

    print("\n  Introspection Endpoints:")
    for name in INTROSPECTION_ENDPOINTS:
        status = "ACCESSIBLE" if introspection_available[name] else "BLOCKED"
        print(f"    /{name}: {status}")

    print(f"\n  Candidates tested: {len(set(CANDIDATE_COLLECTIONS))}")
    print(f"  Collections found: {len(found)}")
    print(f"    Confirmed known: {len(confirmed_known)}")
    print(f"    NEW discoveries: {len(new_collections)}")
    print(f"  Forbidden (may exist): {len(forbidden)}")
    print(f"  Not found: {len(not_found)}")

    if confirmed_known:
        print("\n  CONFIRMED KNOWN COLLECTIONS:")
        for name, data in sorted(confirmed_known.items()):
            print(f"    items/{name}: {data.get('field_count', 0)} fields")

    if new_collections:
        print("\n  NEW COLLECTIONS DISCOVERED:")
        for name, data in sorted(new_collections.items()):
            print(f"    items/{name}: {data.get('field_count', 0)} fields")

    if forbidden:
        print("\n  FORBIDDEN COLLECTIONS:")
        for name, data in sorted(forbidden.items()):
            print(f"    items/{name}: HTTP {data.get('status')}")

    print("\n  COMPARISON WITH config.py:")
    for name, endpoint in sorted(KNOWN_ENDPOINTS.items()):
        if name in found:
            print(f"    {endpoint}: OK")
        elif name in forbidden:
            print(f"    {endpoint}: FORBIDDEN")
        else:
            print(f"    {endpoint}: NOT FOUND")

    print("=" * 60)

    return summary


def main() -> None:
    logger.info("=== Directus Collection Discovery ===")

    tokens = TokenManager.get_tokens()
    if not tokens or not tokens.api_token:
        logger.error("Failed to fetch API token")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {tokens.api_token}",
        "user-agent": DEFAULT_USER_AGENT,
    }

    # Strategy 1: Introspection
    logger.info("Strategy 1: Directus Introspection API")
    introspection = run_introspection(API_FFBB_BASE_URL, headers)

    # Strategy 2: Brute-force
    logger.info("Strategy 2: Brute-force collection probing")
    brute_force_results = run_brute_force(API_FFBB_BASE_URL, headers)

    # Classify brute-force results
    found = {k: v for k, v in brute_force_results.items() if v.get("exists") is True}
    forbidden = {
        k: v for k, v in brute_force_results.items() if v.get("exists") is None
    }
    not_found = [k for k, v in brute_force_results.items() if v.get("exists") is False]

    # Build report
    report = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "base_url": API_FFBB_BASE_URL,
        },
        "introspection": introspection,
        "brute_force": {
            "found": found,
            "forbidden": forbidden,
            "not_found": sorted(not_found),
        },
        "summary": {},  # filled by print_summary
    }

    report["summary"] = print_summary(introspection, brute_force_results)

    # Save report
    output_path = PROJECT_ROOT / "data" / "directus_collections_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    logger.info(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    main()
