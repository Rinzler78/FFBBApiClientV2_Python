#!/usr/bin/env python3
"""
Discover Directus API field depths by testing wildcard queries.

Tests depths *, *.*, *.*.*, *.*.*.*,  *.*.*.*.* for each endpoint.
Identifies the max useful depth (when response no longer adds fields).
Uses the official get_fields() API to analyze schema before runtime testing.
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

from ffbb_api_client_v2._http.client import (  # noqa: E402
    http_get_json,
    url_with_params,
)
from ffbb_api_client_v2.config import (  # noqa: E402
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
)
from ffbb_api_client_v2.directus_ffbb.client import (  # noqa: E402
    ApiFFBBAppClient,
)
from ffbb_api_client_v2.facade.token_manager import TokenManager  # noqa: E402

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


def analyze_schema_fields(
    client: ApiFFBBAppClient, collection_name: str
) -> dict[str, Any]:
    """Analyze fields using official Directus get_fields() API."""
    logger.info(f"Analyzing schema for: {collection_name}")

    # Get fields from official Directus API
    fields = client.get_fields(collection=collection_name)

    if not fields:
        return {
            "collection": collection_name,
            "field_count": 0,
            "fields": [],
            "relationships": {},
            "schema_depths": {},
        }

    # Build relationship graph
    relationships: dict[str, str] = {}
    schema_fields: list[str] = []

    for field in fields:
        field_name = field.get("field")
        meta = field.get("meta", {})
        schema = field.get("schema", {})
        field_type = field.get("type")

        if field_name:
            schema_fields.append(field_name)

            # Check for relationships
            special = meta.get("special", [])
            if (
                "m2o" in special
                or field_type == "integer"
                and schema.get("foreign_key_table")
            ):
                target = schema.get("foreign_key_table")
                if target:
                    relationships[field_name] = target

    # Predict theoretical depths from schema
    schema_depths = {"*": schema_fields.copy()}
    if relationships:
        for i in range(1, 5):
            depth = "*." * i + "*"
            schema_depths[depth] = [f"{rel}.*" for rel in relationships.keys()]

    return {
        "collection": collection_name,
        "field_count": len(fields),
        "fields": schema_fields,
        "relationships": relationships,
        "schema_depths": schema_depths,
    }


def main() -> None:
    logger.info("=== Directus API Field Discovery (Enhanced with Schema Analysis) ===")

    tokens = TokenManager.get_tokens()
    if not tokens or not tokens.api_token:
        logger.error("Failed to fetch API token")
        sys.exit(1)

    # Initialize official API client for schema discovery
    client = ApiFFBBAppClient(bearer_token=tokens.api_token, debug=True)
    logger.info("Using official Directus get_fields() API for schema analysis")

    headers = {
        "Authorization": f"Bearer {tokens.api_token}",
        "user-agent": DEFAULT_USER_AGENT,
    }

    report: dict[str, Any] = {}

    for name, config in ENDPOINTS.items():
        # Extract collection name from endpoint path
        collection_name = config["path"].replace("/items/", "")

        logger.info(f"\nDiscovering fields for: {name}")

        # Step 1: Analyze schema using official get_fields() API
        schema_analysis = analyze_schema_fields(client, collection_name)
        logger.info(
            f"  Schema analysis: {schema_analysis['field_count']} fields, "
            f"{len(schema_analysis['relationships'])} relationships"
        )

        # Step 2: Runtime discovery via wildcard testing
        runtime_discovery = discover_endpoint(API_FFBB_BASE_URL, headers, name, config)

        # Combine both approaches
        report[name] = {
            "endpoint": config["path"],
            "collection": collection_name,
            "schema_analysis": schema_analysis,
            "runtime_discovery": runtime_discovery,
            "max_useful_depth": runtime_discovery["max_useful_depth"],
            "total_unique_fields": runtime_discovery["total_unique_fields"],
            "all_fields": runtime_discovery["all_fields"],
        }

        logger.info(
            f"  Runtime discovery: {report[name]['total_unique_fields']} total fields, "
            f"max useful depth: {report[name]['max_useful_depth']}"
        )

    output_path = PROJECT_ROOT / "data" / "directus_field_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    logger.info(f"\nReport saved to {output_path}")

    # Print summary
    print("\n=== SUMMARY ===")
    for name, data in report.items():
        print(f"\n{name} ({data['collection']}):")
        print(f"  Schema fields: {data['schema_analysis']['field_count']}")
        print(f"  Runtime max depth: {data['max_useful_depth']}")
        print(f"  Total unique fields: {data['total_unique_fields']}")
        if data["schema_analysis"]["relationships"]:
            print(
                f"  Relationships: {list(data['schema_analysis']['relationships'].keys())}"
            )
        for depth, info in data["runtime_discovery"]["depths"].items():
            if info.get("new_fields_count", 0) > 0:
                print(f"  {depth}: +{info['new_fields_count']} new fields")


if __name__ == "__main__":
    main()
