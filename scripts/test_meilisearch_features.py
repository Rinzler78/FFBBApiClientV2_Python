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

from ffbb_api_client_v2._http.client import HttpClient
from ffbb_api_client_v2.config import MEILISEARCH_BASE_URL

DEFAULT_USER_AGENT = "okhttp/4.12.0"


def get_headers() -> dict[str, str]:
    token = os.environ.get("MEILISEARCH_BEARER_TOKEN")
    if not token:
        print("ERROR: Set MEILISEARCH_BEARER_TOKEN environment variable")
        raise RuntimeError("MEILISEARCH_BEARER_TOKEN environment variable not set")
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
        url = f"{MEILISEARCH_BASE_URL}{endpoint}"
        result = HttpClient.http_post_json(url, headers, body)
        if isinstance(result, dict):
            if "code" in result and "type" in result:
                print(f"  FAILED: {result.get('message', 'Unknown error')}")
                print(f"  CodeEnum: {result.get('code')}")
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


def _run_federation_tests(headers: dict[str, str]) -> dict[str, str]:
    """Run federation feature tests."""
    results: dict[str, str] = {}

    body = {
        "queries": [
            {"indexUid": "ffbbserver_organismes", "q": "Paris"},
            {"indexUid": "ffbbserver_competitions", "q": "Paris"},
        ],
        "federation": {},
    }
    r = test_feature("federation (merged results)", body, headers)
    results["federation"] = "OK" if r and "hits" in r else "FAILED"

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

    return results


def _run_search_strategy_tests(headers: dict[str, str]) -> dict[str, str]:
    """Run matching strategy and ranking tests."""
    results: dict[str, str] = {}

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
        if hits and "_rankingScore" in hits[0]:
            print(f"  Sample _rankingScore: {hits[0]['_rankingScore']}")

    return results


def _run_presentation_tests(headers: dict[str, str]) -> dict[str, str]:
    """Run highlight and search attribute tests."""
    results: dict[str, str] = {}

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

    return results


def _run_geo_and_filter_tests(headers: dict[str, str]) -> dict[str, str]:
    """Run geo-search and filter tests."""
    results: dict[str, str] = {}

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

    return results


def _check_server_version(headers: dict[str, str]) -> dict[str, str]:
    """Check Meilisearch server version."""
    print(f"\n{'='*60}")
    print("Testing: Meilisearch version")
    try:
        version_result = HttpClient.http_get_json(
            f"{MEILISEARCH_BASE_URL}version", headers
        )
        if version_result and "pkgVersion" in version_result:
            print(f"  Meilisearch version: {version_result['pkgVersion']}")
            return {"version": version_result["pkgVersion"]}
        print(f"  Could not determine version: {version_result}")
        return {"version": "UNKNOWN"}
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"version": "ERROR"}


def _print_summary(results: dict[str, str]) -> None:
    """Print test summary."""
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


def main() -> None:
    headers = get_headers()

    print("\n" + "#" * 60)
    print("# MEILISEARCH FEATURE TESTS")
    print("#" * 60)

    results: dict[str, str] = {}
    results.update(_run_federation_tests(headers))
    results.update(_run_search_strategy_tests(headers))
    results.update(_run_presentation_tests(headers))
    results.update(_run_geo_and_filter_tests(headers))
    results.update(_check_server_version(headers))

    _print_summary(results)


if __name__ == "__main__":
    main()
