#!/usr/bin/env python3
"""Test advanced Meilisearch features on the FFBB API.

This script systematically probes which advanced Meilisearch features
are supported by the live FFBB Meilisearch instance.

Usage:
    export MEILISEARCH_BEARER_TOKEN="your-token"
    python scripts/test_meilisearch_features.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ffbb_api_client_v2.helpers.http_requests_utils import http_post_json  # noqa: E402

MEILISEARCH_URL = "https://meilisearch-prod.ffbb.app/"
DEFAULT_USER_AGENT = "okhttp/4.12.0"


def get_headers() -> dict[str, str]:
    token = os.environ.get("MEILISEARCH_BEARER_TOKEN")
    if not token:
        print("ERROR: Set MEILISEARCH_BEARER_TOKEN environment variable")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "user-agent": DEFAULT_USER_AGENT,
    }


def test_feature(
    name: str, body: dict, headers: dict[str, str], endpoint: str = "multi-search"
) -> dict | None:
    """Test a single Meilisearch feature and report result."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    try:
        url = f"{MEILISEARCH_URL}{endpoint}"
        result = http_post_json(url, headers, body)
        if isinstance(result, dict):
            if "code" in result and "type" in result:
                print(f"  FAILED: {result.get('message', 'Unknown error')}")
                print(f"  Code: {result.get('code')}")
                if result.get("link"):
                    print(f"  Docs: {result.get('link')}")
                return None
            # Success
            if "hits" in result:
                print(f"  SUCCESS: {len(result['hits'])} hits")
                if "estimatedTotalHits" in result:
                    print(f"  estimatedTotalHits: {result['estimatedTotalHits']}")
            elif "results" in result:
                for i, r in enumerate(result["results"]):
                    hits = len(r.get("hits", []))
                    idx = r.get("indexUid", "?")
                    print(f"  [{i}] {idx}: {hits} hits")
            else:
                print(f"  RESULT: {json.dumps(result, indent=2)[:500]}")
            return result
        print(f"  UNEXPECTED: {type(result)}")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main() -> None:
    headers = get_headers()
    results: dict[str, str] = {}

    print("\n" + "#" * 60)
    print("# MEILISEARCH FEATURE TESTS")
    print("#" * 60)

    # 1. Federation
    body = {
        "queries": [
            {"indexUid": "ffbbserver_organismes", "q": "Paris"},
            {"indexUid": "ffbbserver_competitions", "q": "Paris"},
        ],
        "federation": {},
    }
    r = test_feature("federation (merged results)", body, headers)
    results["federation"] = "OK" if r and "hits" in r else "FAILED"

    # 2. Federation with weights
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Lyon",
                "federationOptions": {"weight": 2.0},
            },
            {
                "indexUid": "ffbbserver_salles",
                "q": "Lyon",
                "federationOptions": {"weight": 1.0},
            },
        ],
        "federation": {"limit": 10},
    }
    r = test_feature("federation with weights", body, headers)
    results["federation_weights"] = "OK" if r and "hits" in r else "FAILED"

    # 3. matchingStrategy: "all"
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Paris Basketball Club",
                "matchingStrategy": "all",
                "limit": 5,
            }
        ]
    }
    r = test_feature("matchingStrategy: all", body, headers)
    results["matching_strategy_all"] = "OK" if r and "results" in r else "FAILED"

    # 4. matchingStrategy: "frequency"
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Paris Basket",
                "matchingStrategy": "frequency",
                "limit": 5,
            }
        ]
    }
    r = test_feature("matchingStrategy: frequency", body, headers)
    results["matching_strategy_freq"] = "OK" if r and "results" in r else "FAILED"

    # 5. rankingScoreThreshold
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Paris",
                "rankingScoreThreshold": 0.5,
                "showRankingScore": True,
                "limit": 5,
            }
        ]
    }
    r = test_feature("rankingScoreThreshold + showRankingScore", body, headers)
    results["ranking_score_threshold"] = "OK" if r and "results" in r else "FAILED"
    if r and "results" in r:
        hits = r["results"][0].get("hits", [])
        if hits:
            sample = hits[0]
            if "_rankingScore" in sample:
                print(f"  Sample _rankingScore: {sample['_rankingScore']}")

    # 6. attributesToHighlight
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Marseille",
                "attributesToHighlight": ["*"],
                "limit": 3,
            }
        ]
    }
    r = test_feature("attributesToHighlight: ['*']", body, headers)
    results["highlight"] = "OK" if r and "results" in r else "FAILED"
    if r and "results" in r:
        hits = r["results"][0].get("hits", [])
        if hits and "_formatted" in hits[0]:
            print("  _formatted field present in hits")

    # 7. Geo-search: _geoRadius
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "",
                "filter": "_geoRadius(48.8566, 2.3522, 10000)",
                "sort": ["_geoPoint(48.8566, 2.3522):asc"],
                "limit": 5,
            }
        ]
    }
    r = test_feature("_geoRadius (Paris, 10km)", body, headers)
    results["geo_radius"] = "OK" if r and "results" in r else "FAILED"
    if r and "results" in r:
        hits = r["results"][0].get("hits", [])
        if hits and "_geo" in hits[0]:
            geo = hits[0]["_geo"]
            print(f"  First hit _geo: lat={geo.get('lat')}, lng={geo.get('lng')}")

    # 8. distinct
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Paris",
                "distinct": "type_association.libelle",
                "limit": 10,
            }
        ]
    }
    r = test_feature("distinct on type_association.libelle", body, headers)
    results["distinct"] = "OK" if r and "results" in r else "FAILED"

    # 9. attributesToSearchOn
    body = {
        "queries": [
            {
                "indexUid": "ffbbserver_organismes",
                "q": "Paris",
                "attributesToSearchOn": ["nom"],
                "limit": 5,
            }
        ]
    }
    r = test_feature("attributesToSearchOn: ['nom']", body, headers)
    results["attrs_to_search_on"] = "OK" if r and "results" in r else "FAILED"

    # 10. Try to detect Meilisearch version via /version
    print(f"\n{'='*60}")
    print("Testing: Meilisearch version")
    try:
        from ffbb_api_client_v2.helpers.http_requests_utils import http_get_json

        version_result = http_get_json(f"{MEILISEARCH_URL}version", headers)
        if version_result and "pkgVersion" in version_result:
            print(f"  Meilisearch version: {version_result['pkgVersion']}")
            results["version"] = version_result["pkgVersion"]
        else:
            print(f"  Could not determine version: {version_result}")
            results["version"] = "UNKNOWN"
    except Exception as e:
        print(f"  ERROR: {e}")
        results["version"] = "ERROR"

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for feature, status in results.items():
        icon = (
            "+"
            if status == "OK"
            or (feature == "version" and status not in ("FAILED", "ERROR", "UNKNOWN"))
            else "-"
        )
        print(f"  [{icon}] {feature}: {status}")


if __name__ == "__main__":
    main()
