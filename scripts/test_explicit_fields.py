#!/usr/bin/env python3
"""Validate explicit fields vs wildcards for all Directus entities.

For each entity with a single-item endpoint, queries the API twice:
1. With WILDCARD fields → gets all available fields from the API
2. With get_default_fields() → gets the explicit field list

Compares the two to report:
- Fields returned by API but absent from default_fields (potential additions)
- Fields in default_fields but absent from API response (possibly obsolete)

Usage:
    export API_FFBB_APP_BEARER_TOKEN=...
    export MEILISEARCH_BEARER_TOKEN=...
    python scripts/test_explicit_fields.py
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ffbb_api_client_v2 import FFBBAPIClientV2  # noqa: E402
from ffbb_api_client_v2.directus_ffbb.client import ApiFFBBAppClient  # noqa: E402
from ffbb_api_client_v2.directus_ffbb.config import (  # noqa: E402
    ENDPOINT_COMMUNES,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_ENGAGEMENTS,
    ENDPOINT_ENTRAINEURS,
    ENDPOINT_FORMATIONS,
    ENDPOINT_OFFICIELS,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_PRATIQUES,
    ENDPOINT_RENCONTRES,
    ENDPOINT_SAISONS,
    ENDPOINT_SALLES,
    ENDPOINT_TERRAINS,
    ENDPOINT_TOURNOIS,
)
from ffbb_api_client_v2.directus_ffbb.models.communes_fields import (  # noqa: E402
    CommunesFields,
)
from ffbb_api_client_v2.directus_ffbb.models.competition_fields import (  # noqa: E402
    CompetitionFields,
)
from ffbb_api_client_v2.directus_ffbb.models.engagements_fields import (  # noqa: E402
    EngagementsFields,
)
from ffbb_api_client_v2.directus_ffbb.models.entraineurs_fields import (  # noqa: E402
    EntraineursFields,
)
from ffbb_api_client_v2.directus_ffbb.models.formations_fields import (  # noqa: E402
    FormationsFields,
)
from ffbb_api_client_v2.directus_ffbb.models.officiels_fields import (  # noqa: E402
    OfficielsFields,
)
from ffbb_api_client_v2.directus_ffbb.models.organisme_fields import (  # noqa: E402
    OrganismeFields,
)
from ffbb_api_client_v2.directus_ffbb.models.poule_fields import (  # noqa: E402
    PouleFields,
)
from ffbb_api_client_v2.directus_ffbb.models.pratiques_fields import (  # noqa: E402
    PratiquesFields,
)
from ffbb_api_client_v2.directus_ffbb.models.rencontres_fields import (  # noqa: E402
    RencontresFields,
)
from ffbb_api_client_v2.directus_ffbb.models.saison_fields import (  # noqa: E402
    SaisonFields,
)
from ffbb_api_client_v2.directus_ffbb.models.salles_fields import (  # noqa: E402
    SallesFields,
)
from ffbb_api_client_v2.directus_ffbb.models.terrains_fields import (  # noqa: E402
    TerrainsFields,
)
from ffbb_api_client_v2.directus_ffbb.models.tournois_fields import (  # noqa: E402
    TournoisFields,
)


def extract_field_paths(data: dict, prefix: str = "") -> set[str]:
    """Recursively extract dot-notation field paths from a JSON dict."""
    paths: set[str] = set()
    for key, value in data.items():
        full_path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            paths |= extract_field_paths(value, full_path)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            paths |= extract_field_paths(value[0], full_path)
        else:
            paths.add(full_path)
    return paths


def check_env():
    """Check required environment variables."""
    api_token = os.getenv("API_FFBB_APP_BEARER_TOKEN")
    mls_token = os.getenv("MEILISEARCH_BEARER_TOKEN")
    if not api_token or not mls_token:
        print("ERROR: Set API_FFBB_APP_BEARER_TOKEN and MEILISEARCH_BEARER_TOKEN")
        sys.exit(1)
    return api_token, mls_token


def discover_item_id(
    facade: FFBBAPIClientV2,
    entity_name: str,
) -> int | None:
    """Discover a valid item ID for an entity via Meilisearch search."""
    search_map = {
        "competitions": ("search_competitions", "Nationale"),
        "organismes": ("search_organismes", "Paris"),
        "rencontres": ("search_rencontres", ""),
        "terrains": ("search_terrains", ""),
        "salles": ("search_salles", ""),
        "tournois": ("search_tournois", ""),
        "pratiques": ("search_pratiques", "Basketball"),
        "engagements": ("search_engagements", ""),
        "formations": ("search_formations", ""),
    }

    if entity_name in search_map:
        method_name, query = search_map[entity_name]
        method = getattr(facade, method_name)
        results = method(query)
        if results and results.hits:
            return int(results.hits[0].id)

    return None


def compare_entity(
    api_client: ApiFFBBAppClient,
    facade: FFBBAPIClientV2,
    entity_name: str,
    endpoint: str,
    fields_class: type,
    item_id: int | None = None,
) -> dict:
    """Compare wildcard vs default fields for a single entity."""
    result = {
        "entity": entity_name,
        "status": "SKIP",
        "default_count": 0,
        "api_count": 0,
        "missing_from_default": set(),
        "missing_from_api": set(),
    }

    # Discover an item ID if not provided
    if item_id is None:
        item_id = discover_item_id(facade, entity_name)

    if item_id is None:
        print(f"  [{entity_name}] SKIP: No item ID found via search")
        return result

    print(f"  [{entity_name}] Using item_id={item_id}")

    # 1. Fetch with wildcard
    wildcard_endpoint = f"{endpoint}/{item_id}"
    try:
        wildcard_data = api_client._get_item(
            wildcard_endpoint, fields=[fields_class.WILDCARD]
        )
    except Exception as e:
        print(f"  [{entity_name}] ERROR fetching wildcard: {e}")
        result["status"] = "ERROR"
        return result

    if not wildcard_data:
        print(f"  [{entity_name}] SKIP: Wildcard query returned None")
        return result

    api_paths = extract_field_paths(wildcard_data)

    # 2. Get default fields
    default_fields = set(fields_class.get_default_fields())

    result["default_count"] = len(default_fields)
    result["api_count"] = len(api_paths)

    # 3. Compare
    # Fields from API not in default (potential additions)
    result["missing_from_default"] = api_paths - default_fields
    # Fields in default not from API (possibly obsolete or nested-path mismatches)
    result["missing_from_api"] = default_fields - api_paths

    result["status"] = "OK"
    return result


ENTITIES = [
    ("competitions", ENDPOINT_COMPETITIONS, CompetitionFields),
    ("organismes", ENDPOINT_ORGANISMES, OrganismeFields),
    ("poules", ENDPOINT_POULES, PouleFields),
    ("saisons", ENDPOINT_SAISONS, SaisonFields),
    ("communes", ENDPOINT_COMMUNES, CommunesFields),
    ("officiels", ENDPOINT_OFFICIELS, OfficielsFields),
    ("entraineurs", ENDPOINT_ENTRAINEURS, EntraineursFields),
    ("rencontres", ENDPOINT_RENCONTRES, RencontresFields),
    ("salles", ENDPOINT_SALLES, SallesFields),
    ("terrains", ENDPOINT_TERRAINS, TerrainsFields),
    ("tournois", ENDPOINT_TOURNOIS, TournoisFields),
    ("engagements", ENDPOINT_ENGAGEMENTS, EngagementsFields),
    ("formations", ENDPOINT_FORMATIONS, FormationsFields),
    ("pratiques", ENDPOINT_PRATIQUES, PratiquesFields),
]


def main():
    api_token, mls_token = check_env()

    print("Initializing FFBB API client...")
    facade = FFBBAPIClientV2.create(
        meilisearch_bearer_token=mls_token,
        api_bearer_token=api_token,
        debug=False,
    )
    api_client = facade.api_ffbb_client

    # For poules and saisons, discover IDs via competition
    poule_id = None
    saison_id = None

    # Find a poule via competition phases
    comp_results = facade.search_competitions("Nationale")
    if comp_results and comp_results.hits:
        comp = facade.get_competition(int(comp_results.hits[0].id))
        if comp and comp.phases:
            for phase in comp.phases:
                if phase.poules:
                    poule_id = int(phase.poules[0].id)
                    break

    # Saisons: fetch list and use first
    saison_data = api_client._list_items(ENDPOINT_SAISONS, fields=["id"], limit=1)
    if saison_data:
        saison_id = saison_data[0].get("id")

    # Find IDs for entities without direct Meilisearch search
    commune_data = api_client._list_items(ENDPOINT_COMMUNES, fields=["id"], limit=1)
    commune_id = commune_data[0].get("id") if commune_data else None

    officiel_data = api_client._list_items(ENDPOINT_OFFICIELS, fields=["id"], limit=1)
    officiel_id = officiel_data[0].get("id") if officiel_data else None

    entraineur_data = api_client._list_items(
        ENDPOINT_ENTRAINEURS, fields=["id"], limit=1
    )
    entraineur_id = entraineur_data[0].get("id") if entraineur_data else None

    # Map of overridden IDs
    override_ids = {
        "poules": poule_id,
        "saisons": saison_id,
        "communes": commune_id,
        "officiels": officiel_id,
        "entraineurs": entraineur_id,
    }

    print(f"\n{'='*70}")
    print("  WILDCARD vs DEFAULT FIELDS COMPARISON")
    print(f"{'='*70}")

    all_results = []
    for entity_name, endpoint, fields_class in ENTITIES:
        item_id = override_ids.get(entity_name)
        try:
            result = compare_entity(
                api_client, facade, entity_name, endpoint, fields_class, item_id
            )
            all_results.append(result)
        except Exception as e:
            print(f"  [{entity_name}] ERROR: {e}")
            all_results.append({"entity": entity_name, "status": "ERROR"})
        time.sleep(0.5)  # Rate limiting

    # Summary report
    print(f"\n{'='*70}")
    print("  SUMMARY REPORT")
    print(f"{'='*70}")

    for r in all_results:
        entity = r["entity"]
        status = r["status"]

        if status == "SKIP":
            print(f"\n  {entity}: SKIPPED (no item found)")
            continue
        if status == "ERROR":
            print(f"\n  {entity}: ERROR")
            continue

        print(f"\n  {entity}:")
        print(f"    Default fields: {r['default_count']}")
        print(f"    API fields (wildcard): {r['api_count']}")

        missing_default = r.get("missing_from_default", set())
        missing_api = r.get("missing_from_api", set())

        if missing_default:
            print(f"    API fields NOT in default ({len(missing_default)}):")
            for f in sorted(missing_default):
                print(f"      + {f}")

        if missing_api:
            print(f"    Default fields NOT in API ({len(missing_api)}):")
            for f in sorted(missing_api):
                print(f"      - {f}")

        if not missing_default and not missing_api:
            print("    PERFECT MATCH")

    return 0


if __name__ == "__main__":
    sys.exit(main())
