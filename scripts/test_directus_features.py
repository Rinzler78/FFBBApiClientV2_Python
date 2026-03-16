#!/usr/bin/env python3
"""Test advanced Directus features on the FFBB API.

This script systematically probes which advanced Directus features
are supported by the live FFBB API (api.ffbb.com).

Usage:
    export API_FFBB_BEARER_TOKEN="your-token"
    python scripts/test_directus_features.py
"""

from __future__ import annotations

import json
import os

from ffbb_api_client_v2._http.client import HttpClient
from ffbb_api_client_v2.config import API_FFBB_BASE_URL

DEFAULT_USER_AGENT = "okhttp/4.12.0"


def get_headers() -> dict[str, str]:
    token = os.environ.get("API_FFBB_APP_BEARER_TOKEN")
    if not token:
        print("ERROR: Set API_FFBB_APP_BEARER_TOKEN environment variable")
        raise RuntimeError("API_FFBB_APP_BEARER_TOKEN environment variable not set")
    return {
        "Authorization": f"Bearer {token}",
        "user-agent": DEFAULT_USER_AGENT,
    }


def test_feature(name: str, url: str, headers: dict[str, str]) -> dict | None:
    """Test a single feature and report result."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url[:120]}...")
    try:
        result = HttpClient.http_get_json(url, headers)
        if isinstance(result, dict):
            if "errors" in result:
                print(f"  FAILED: {result['errors']}")
                return None
            data = result.get("data")
            meta = result.get("meta")
            if data is not None:
                count = len(data) if isinstance(data, list) else 1
                print(f"  SUCCESS: {count} items")
                if meta:
                    print(f"  Meta: {json.dumps(meta, indent=2)}")
                return result
            # aggregate/groupBy may return data directly
            print(f"  RESULT: {json.dumps(result, indent=2)[:500]}")
            return result
        print(f"  UNEXPECTED: {type(result)}")
        return result
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main() -> None:
    headers = get_headers()
    results: dict[str, str] = {}

    # 1. Test aggregate[count]=*
    print("\n" + "#" * 60)
    print("# DIRECTUS FEATURE TESTS")
    print("#" * 60)

    # aggregate count
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/rencontres",
        {"aggregate[count]": "*", "limit": "1"},
    )
    r = test_feature("aggregate[count]=*", url, headers)
    results["aggregate_count"] = "OK" if r and "errors" not in r else "FAILED"

    # aggregate countDistinct
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/rencontres",
        {"aggregate[countDistinct]": "id", "limit": "1"},
    )
    r = test_feature("aggregate[countDistinct]=id", url, headers)
    results["aggregate_countDistinct"] = "OK" if r and "errors" not in r else "FAILED"

    # groupBy
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/rencontres",
        {"groupBy[]": "saison", "aggregate[count]": "*", "limit": "5"},
    )
    r = test_feature("groupBy[]=saison + aggregate[count]=*", url, headers)
    results["groupBy"] = "OK" if r and "errors" not in r else "FAILED"

    # limit=-1 (fetch all)
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/saisons",
        {"limit": "-1", "fields[]": ["id", "libelle"]},
    )
    r = test_feature("limit=-1 (fetch all)", url, headers)
    results["limit_minus_1"] = "OK" if r and "errors" not in r else "FAILED"

    # Temporal functions: year() in filter
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/rencontres",
        {
            "filter": '{"year(date_rencontre)":{"_eq":2025}}',
            "limit": "1",
            "fields[]": ["id", "date_rencontre"],
        },
    )
    r = test_feature("filter with year() function", url, headers)
    results["temporal_year"] = "OK" if r and "errors" not in r else "FAILED"

    # alias
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/organismes/1",
        {
            "alias[active_competitions]": "competitions",
            "fields[]": ["id", "nom"],
        },
    )
    r = test_feature("alias[active_competitions]=competitions", url, headers)
    results["alias"] = "OK" if r and "errors" not in r else "FAILED"

    # export=json
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/saisons",
        {"export": "json", "limit": "2", "fields[]": ["id", "libelle"]},
    )
    r = test_feature("export=json", url, headers)
    results["export_json"] = "OK" if r else "FAILED"

    # backlink=false with wildcard
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/organismes/1",
        {"fields[]": ["*.*"], "backlink": "false"},
    )
    r = test_feature("backlink=false with *.*", url, headers)
    results["backlink_false"] = "OK" if r and "errors" not in r else "FAILED"

    # page-based pagination
    url = HttpClient.url_with_params(
        f"{API_FFBB_BASE_URL}items/saisons",
        {
            "page": "1",
            "limit": "5",
            "meta": "total_count,filter_count",
            "fields[]": ["id"],
        },
    )
    r = test_feature("page-based pagination (page=1)", url, headers)
    results["page_pagination"] = "OK" if r and "errors" not in r else "FAILED"

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for feature, status in results.items():
        icon = "+" if status == "OK" else "-"
        print(f"  [{icon}] {feature}: {status}")


if __name__ == "__main__":
    main()
