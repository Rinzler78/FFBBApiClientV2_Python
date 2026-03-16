#!/usr/bin/env python3
"""Validate FK expansion behavior for categorie and type_competition_generique.

Confirms that these fields always return dicts (expanded objects) rather
than scalar IDs, validating the FK converter changes planned in Phase 4.

Usage:
    python scripts/validate_fk_expansion.py

Requires FFBB_BEARER_TOKEN and FFBB_MEILISEARCH_TOKEN environment variables
(or auto-discovery via TokenManager).
"""

from __future__ import annotations

import sys
import time

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager

_RATE_DELAY = 0.3
_SAMPLE_SIZE = 20


def main() -> int:
    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )

    # Fields to validate: FK fields that might return dicts or scalars
    fk_fields = ["categorie", "typeCompetitionGenerique"]

    print("=== FK Expansion Validation ===")
    print(f"Fields: {fk_fields}")
    print(f"Sample size: {_SAMPLE_SIZE}")
    print()

    # Get competition IDs from Meilisearch
    print("Fetching competition IDs from Meilisearch...")
    search_results = client.search_multiple_competitions()
    if not search_results or not search_results.results:
        print("No competitions found via search")
        raise RuntimeError("No competitions found via search")

    comp_ids: list[str] = []
    for result in search_results.results:
        if result.hits:
            for hit in result.hits:
                if hasattr(hit, "id") and hit.id:
                    comp_ids.append(str(hit.id))
    comp_ids = comp_ids[:_SAMPLE_SIZE]
    print(f"Found {len(comp_ids)} competition IDs")
    print()

    # Check each competition's raw response
    totals: dict[str, dict[str, int]] = {
        f: {"dict": 0, "scalar": 0, "null": 0, "other": 0} for f in fk_fields
    }

    for comp_id in comp_ids:
        try:
            resp = client.get_competition(int(comp_id))
            if resp is None:
                continue

            # Get raw dict from the data field
            raw = resp.data.to_dict() if resp.data else {}

            for fk_field in fk_fields:
                val = raw.get(fk_field)
                if val is None:
                    totals[fk_field]["null"] += 1
                elif isinstance(val, dict):
                    totals[fk_field]["dict"] += 1
                elif isinstance(val, (int, str)):
                    totals[fk_field]["scalar"] += 1
                    print(f"  SCALAR: {comp_id}.{fk_field} = {val!r}")
                else:
                    totals[fk_field]["other"] += 1
                    print(f"  OTHER: {comp_id}.{fk_field} = {type(val).__name__}")

        except Exception as e:
            print(f"  ERROR: {comp_id}: {e}")
            raise  # Re-raise unexpected errors

        time.sleep(_RATE_DELAY)

    # Report
    print("\n=== Results ===")
    all_ok = True
    for fk_field, counts in totals.items():
        print(f"\n{fk_field}:")
        for kind, count in counts.items():
            marker = "  " if kind in ("dict", "null") else "!!"
            print(f"  {marker} {kind}: {count}")
        if counts["scalar"] > 0 or counts["other"] > 0:
            all_ok = False
            print(f"  >> WARNING: {fk_field} has non-dict values!")

    print()
    if all_ok:
        print("PASS: All FK fields return dicts (or null). Safe to use from_obj.")
    else:
        print("FAIL: Some FK fields return scalars. Need from_str converters.")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
