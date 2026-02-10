#!/usr/bin/env python3
"""
Discover Directus API field depths by testing wildcard queries.

Tests depths *, *.*, *.*.*, *.*.*.*,  *.*.*.*.* for each endpoint.
Identifies the max useful depth (when response no longer adds fields).
Generates data/directus_field_discovery.json.

Usage:
    python scripts/discover_api_fields.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ffbb_api_client_v2.config import (  # noqa: E402
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
)
from ffbb_api_client_v2.helpers.http_requests_utils import (  # noqa: E402
    http_get_json,
    url_with_params,
)
from ffbb_api_client_v2.utils.token_manager import TokenManager  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

WILDCARD_DEPTHS = ["*", "*.*", "*.*.*", "*.*.*.*", "*.*.*.*.*"]

ENDPOINTS: dict[str, dict[str, Any]] = {
    "competitions": {
        "path": ENDPOINT_COMPETITIONS,
        "id": None,  # will use list mode (limit=1)
        "extra_params": {},
    },
    "organismes": {
        "path": ENDPOINT_ORGANISMES,
        "id": None,
        "extra_params": {},
    },
    "poules": {
        "path": ENDPOINT_POULES,
        "id": None,
        "extra_params": {},
    },
    "saisons": {
        "path": ENDPOINT_SAISONS,
        "id": None,
        "extra_params": {},
    },
}


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


def fetch_with_depth(
    base_url: str,
    headers: dict[str, str],
    endpoint: str,
    depth: str,
    item_id: int | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Fetch an endpoint with a specific wildcard depth."""
    if item_id:
        url = f"{base_url}{endpoint}/{item_id}"
    else:
        url = f"{base_url}{endpoint}"

    params: dict[str, Any] = {"fields[]": [depth], "limit": "1"}
    if extra_params:
        params.update(extra_params)

    final_url = url_with_params(url, params)
    try:
        return http_get_json(final_url, headers)
    except Exception as e:
        logger.warning(f"Error fetching {endpoint} at depth {depth}: {e}")
        return None


def discover_endpoint(
    base_url: str,
    headers: dict[str, str],
    name: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Discover fields for a single endpoint at all depths."""
    result: dict[str, Any] = {
        "endpoint": config["path"],
        "depths": {},
        "max_useful_depth": "*",
        "total_unique_fields": 0,
    }

    all_fields: set[str] = set()
    prev_count = 0

    for depth in WILDCARD_DEPTHS:
        logger.info(f"  Testing {name} at depth: {depth}")
        data = fetch_with_depth(
            base_url,
            headers,
            config["path"],
            depth,
            config.get("id"),
            config.get("extra_params"),
        )

        if not data:
            result["depths"][depth] = {
                "status": "error",
                "fields_count": 0,
                "new_fields": [],
            }
            continue

        actual_data = data.get("data", data)
        if isinstance(actual_data, list) and actual_data:
            actual_data = actual_data[0]

        fields = flatten_keys(actual_data)
        new_fields = fields - all_fields
        all_fields.update(fields)

        result["depths"][depth] = {
            "status": "ok",
            "fields_count": len(fields),
            "cumulative_count": len(all_fields),
            "new_fields_count": len(new_fields),
            "new_fields": sorted(new_fields),
        }

        if len(all_fields) > prev_count:
            result["max_useful_depth"] = depth
        prev_count = len(all_fields)

    result["total_unique_fields"] = len(all_fields)
    result["all_fields"] = sorted(all_fields)
    return result


def main() -> None:
    logger.info("=== Directus API Field Discovery ===")

    tokens = TokenManager.get_tokens()
    if not tokens or not tokens.api_token:
        logger.error("Failed to fetch API token")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {tokens.api_token}",
        "user-agent": DEFAULT_USER_AGENT,
    }

    report: dict[str, Any] = {}

    for name, config in ENDPOINTS.items():
        logger.info(f"Discovering fields for: {name}")
        report[name] = discover_endpoint(API_FFBB_BASE_URL, headers, name, config)
        logger.info(
            f"  -> {report[name]['total_unique_fields']} total fields, "
            f"max useful depth: {report[name]['max_useful_depth']}"
        )

    output_path = PROJECT_ROOT / "data" / "directus_field_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    logger.info(f"Report saved to {output_path}")

    # Print summary
    print("\n=== SUMMARY ===")
    for name, data in report.items():
        print(f"\n{name}:")
        print(f"  Max useful depth: {data['max_useful_depth']}")
        print(f"  Total unique fields: {data['total_unique_fields']}")
        for depth, info in data["depths"].items():
            if info.get("new_fields_count", 0) > 0:
                print(f"  {depth}: +{info['new_fields_count']} new fields")


if __name__ == "__main__":
    main()
