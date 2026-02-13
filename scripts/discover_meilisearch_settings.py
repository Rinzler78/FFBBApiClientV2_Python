#!/usr/bin/env python3
"""
Discover Meilisearch index settings (filterable, sortable, searchable attributes).

Strategy 1: GET /indexes/{uid}/settings for each index
Strategy 2 (fallback): POST /multi-search with facets: ["*"]

Generates data/meilisearch_settings_discovery.json.

Usage:
    python scripts/discover_meilisearch_settings.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ffbb_api_client_v2._http.client import (  # noqa: E402
    http_get_json,
    http_post_json,
)
from ffbb_api_client_v2.config import (  # noqa: E402
    DEFAULT_USER_AGENT,
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
    MEILISEARCH_INDEX_UIDS,
)
from ffbb_api_client_v2.facade.token_manager import TokenManager  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_index_settings(
    base_url: str, headers: dict[str, str], index_uid: str
) -> dict[str, Any] | None:
    """Try GET /indexes/{uid}/settings."""
    url = f"{base_url}indexes/{index_uid}/settings"
    try:
        result = http_get_json(url, headers)
        if isinstance(result, dict) and "message" not in result:
            return result
        logger.warning(
            f"  Settings API returned error for {index_uid}: {result.get('message', 'unknown')}"
        )
        return None
    except Exception as e:
        logger.warning(f"  Settings API failed for {index_uid}: {e}")
        return None


def get_filterable_via_facets(
    base_url: str, headers: dict[str, str], index_uid: str
) -> list[str] | None:
    """Fallback: POST multi-search with facets: ["*"] to discover filterable attributes."""
    url = f"{base_url}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
    data = {
        "queries": [
            {
                "indexUid": index_uid,
                "q": "",
                "facets": ["*"],
                "limit": 1,
            }
        ]
    }
    try:
        result = http_post_json(url, headers, data)
        if not result or "results" not in result:
            return None
        results = result["results"]
        if results and "facetDistribution" in results[0]:
            return sorted(results[0]["facetDistribution"].keys())
        return []
    except Exception as e:
        logger.warning(f"  Facets fallback failed for {index_uid}: {e}")
        return None


def discover_index(
    base_url: str, headers: dict[str, str], index_uid: str
) -> dict[str, Any]:
    """Discover settings for a single index."""
    result: dict[str, Any] = {
        "index_uid": index_uid,
        "settings_api": None,
        "facets_fallback": None,
        "filterable_attributes": [],
        "sortable_attributes": [],
        "searchable_attributes": [],
        "displayed_attributes": [],
        "ranking_rules": [],
    }

    # Strategy 1: GET settings
    settings = get_index_settings(base_url, headers, index_uid)
    if settings:
        result["settings_api"] = "success"
        result["filterable_attributes"] = settings.get("filterableAttributes", [])
        result["sortable_attributes"] = settings.get("sortableAttributes", [])
        result["searchable_attributes"] = settings.get("searchableAttributes", [])
        result["displayed_attributes"] = settings.get("displayedAttributes", [])
        result["ranking_rules"] = settings.get("rankingRules", [])
        result["stop_words"] = settings.get("stopWords", [])
        result["synonyms"] = settings.get("synonyms", {})
        result["distinct_attribute"] = settings.get("distinctAttribute")
        result["pagination"] = settings.get("pagination", {})
        result["faceting"] = settings.get("faceting", {})
        result["raw_settings"] = settings
        return result

    # Strategy 2: facets fallback
    result["settings_api"] = "failed"
    facets = get_filterable_via_facets(base_url, headers, index_uid)
    if facets is not None:
        result["facets_fallback"] = "success"
        result["filterable_attributes"] = facets
    else:
        result["facets_fallback"] = "failed"

    return result


def main() -> None:
    logger.info("=== Meilisearch Settings Discovery ===")

    tokens = TokenManager.get_tokens()
    if not tokens or not tokens.meilisearch_token:
        logger.error("Failed to fetch Meilisearch token")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {tokens.meilisearch_token}",
        "Content-Type": "application/json",
        "user-agent": DEFAULT_USER_AGENT,
    }

    report: dict[str, Any] = {"indexes": {}}

    for index_uid in MEILISEARCH_INDEX_UIDS:
        logger.info(f"Discovering settings for: {index_uid}")
        report["indexes"][index_uid] = discover_index(
            MEILISEARCH_BASE_URL, headers, index_uid
        )
        data = report["indexes"][index_uid]
        logger.info(
            f"  -> filterable: {len(data['filterable_attributes'])}, "
            f"sortable: {len(data['sortable_attributes'])}"
        )

    # Summary
    report["summary"] = {
        "total_indexes": len(MEILISEARCH_INDEX_UIDS),
        "settings_api_success": sum(
            1 for d in report["indexes"].values() if d["settings_api"] == "success"
        ),
        "facets_fallback_used": sum(
            1 for d in report["indexes"].values() if d["settings_api"] == "failed"
        ),
    }

    output_path = PROJECT_ROOT / "data" / "meilisearch_settings_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    logger.info(f"Report saved to {output_path}")

    # Print summary
    print("\n=== SUMMARY ===")
    for uid, data in report["indexes"].items():
        print(f"\n{uid}:")
        print(
            f"  Source: {'settings API' if data['settings_api'] == 'success' else 'facets fallback'}"
        )
        print(f"  Filterable: {data['filterable_attributes']}")
        print(f"  Sortable: {data['sortable_attributes']}")


if __name__ == "__main__":
    main()
