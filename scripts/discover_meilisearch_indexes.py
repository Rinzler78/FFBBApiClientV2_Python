#!/usr/bin/env python3
"""
Discover Meilisearch indexes by brute-forcing index names via POST /multi-search.

Tests patterns:
- ffbbserver_* (server-side indexes)
- ffbbnational_* (national indexes)
- ffbbregional_*, ffbb_*, ffbb* (other patterns)

An index exists if multi-search returns results (even empty).
An index does NOT exist if multi-search returns an "index_not_found" error.

Usage:
    python scripts/discover_meilisearch_indexes.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

from ffbb_api_client_v2._http.client import http_post_json
from ffbb_api_client_v2.config import (
    DEFAULT_USER_AGENT,
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
    MEILISEARCH_INDEX_UIDS,
)
from ffbb_api_client_v2.facade.token_manager import TokenManager

PROJECT_ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Candidate index names to test
CANDIDATE_SUFFIXES = [
    # Known entities from Directus API
    "competitions",
    "organismes",
    "rencontres",
    "salles",
    "terrains",
    "tournois",
    "pratiques",
    # Possible additional entities
    "joueurs",
    "licencies",
    "licences",
    "equipes",
    "clubs",
    "entraineurs",
    "arbitres",
    "officiels",
    "classements",
    "rankings",
    "poules",
    "saisons",
    "calendriers",
    "resultats",
    "statistiques",
    "stats",
    "matchs",
    "rencontres_lives",
    "lives",
    "documents",
    "actualites",
    "news",
    "articles",
    "evenements",
    "events",
    "formations",
    "regions",
    "departements",
    "communes",
    "villes",
    "adresses",
    "contacts",
    "photos",
    "videos",
    "medias",
    "palmares",
    "trophees",
    "selections",
    "convocations",
    "inscriptions",
    "engagements",
    "transferts",
    "mutations",
    "affiliations",
    "cotisations",
    "comptes",
    "users",
    "utilisateurs",
    "configurations",
    "parametres",
]

PREFIXES = [
    "ffbbserver_",
    "ffbbnational_",
    "ffbbregional_",
    "ffbb_",
    "ffbb",
]


def test_index_exists(
    base_url: str, headers: dict[str, str], index_uid: str
) -> dict[str, Any]:
    """Test if an index exists via POST /multi-search."""
    url = f"{base_url}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
    data = {
        "queries": [
            {
                "indexUid": index_uid,
                "q": "",
                "limit": 0,
            }
        ]
    }
    try:
        result = http_post_json(url, headers, data)
        if not result:
            return {"exists": False, "error": "empty_response"}

        if "results" in result and isinstance(result["results"], list):
            first = result["results"][0] if result["results"] else {}
            hits = first.get("estimatedTotalHits", first.get("totalHits", 0))
            return {
                "exists": True,
                "estimated_total_hits": hits,
                "processing_time_ms": first.get("processingTimeMs"),
            }

        # Error response
        code = result.get("code", "unknown")
        if code == "index_not_found":
            return {"exists": False, "error": "index_not_found"}
        return {"exists": False, "error": code, "message": result.get("message", "")}

    except Exception as e:
        return {"exists": False, "error": str(e)}


def main() -> None:
    logger.info("=== Meilisearch Index Discovery (Brute-Force) ===")

    tokens = TokenManager.get_tokens()
    if not tokens or not tokens.meilisearch_token:
        logger.error("Failed to fetch Meilisearch token")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {tokens.meilisearch_token}",
        "Content-Type": "application/json",
        "user-agent": DEFAULT_USER_AGENT,
    }

    # Generate all candidate index names
    candidates: set[str] = set()
    for prefix in PREFIXES:
        for suffix in CANDIDATE_SUFFIXES:
            candidates.add(f"{prefix}{suffix}")

    # Remove already known indexes (still test them for validation)
    known = set(MEILISEARCH_INDEX_UIDS)

    logger.info(f"Testing {len(candidates)} candidate index names...")
    logger.info(f"Known indexes: {sorted(known)}")

    found: dict[str, Any] = {}
    not_found: list[str] = []
    errors: dict[str, str] = {}

    for i, candidate in enumerate(sorted(candidates), 1):
        if i % 20 == 0:
            logger.info(f"  Progress: {i}/{len(candidates)}...")
        result = test_index_exists(MEILISEARCH_BASE_URL, headers, candidate)
        if result["exists"]:
            status = "KNOWN" if candidate in known else "NEW"
            logger.info(
                f"  FOUND [{status}]: {candidate} "
                f"(~{result.get('estimated_total_hits', '?')} hits)"
            )
            found[candidate] = result
        elif result["error"] == "index_not_found":
            not_found.append(candidate)
        else:
            errors[candidate] = result.get("error", "unknown")
            logger.warning(f"  ERROR: {candidate} -> {result}")

    # Report
    new_indexes = {k: v for k, v in found.items() if k not in known}
    confirmed_known = {k: v for k, v in found.items() if k in known}

    report = {
        "summary": {
            "total_candidates_tested": len(candidates),
            "total_found": len(found),
            "new_indexes": len(new_indexes),
            "confirmed_known": len(confirmed_known),
            "not_found": len(not_found),
            "errors": len(errors),
        },
        "new_indexes": new_indexes,
        "confirmed_known": confirmed_known,
        "errors": errors if errors else None,
    }

    output_path = PROJECT_ROOT / "data" / "meilisearch_index_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    logger.info(f"\nReport saved to {output_path}")

    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Candidates tested: {len(candidates)}")
    print(f"Indexes found: {len(found)}")
    print(f"  Confirmed known: {len(confirmed_known)}")
    print(f"  NEW discoveries: {len(new_indexes)}")
    print(f"Not found: {len(not_found)}")
    if errors:
        print(f"Errors: {len(errors)}")

    if new_indexes:
        print("\n=== NEW INDEXES DISCOVERED ===")
        for uid, data in sorted(new_indexes.items()):
            print(f"  {uid}: ~{data.get('estimated_total_hits', '?')} hits")
    else:
        print("\nNo new indexes discovered.")

    if confirmed_known:
        print("\n=== CONFIRMED KNOWN INDEXES ===")
        for uid, data in sorted(confirmed_known.items()):
            print(f"  {uid}: ~{data.get('estimated_total_hits', '?')} hits")


if __name__ == "__main__":
    main()
