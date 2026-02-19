#!/usr/bin/env python3
"""
Discover Directus API field depths by testing wildcard queries.

Tests depths *, *.*, *.*.*, *.*.*.*,  *.*.*.*.* for each endpoint.
Identifies the max useful depth (when response no longer adds fields).
Computes optimal fields per endpoint (FK-only for delegated relations).
Generates data/directus_field_discovery.json.

Usage:
    python scripts/discover_api_fields.py
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from requests_cache import CachedSession

from ffbb_api_client_v2._http.client import (
    HttpClient,
    url_with_params,
)
from ffbb_api_client_v2.directus.client import DEFAULT_USER_AGENT
from ffbb_api_client_v2.directus_ffbb.config import (
    API_FFBB_BASE_URL,
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
from ffbb_api_client_v2.directus_ffbb.models.communes_fields import CommunesFields
from ffbb_api_client_v2.directus_ffbb.models.competition_fields import CompetitionFields
from ffbb_api_client_v2.directus_ffbb.models.engagements_fields import EngagementsFields
from ffbb_api_client_v2.directus_ffbb.models.entraineurs_fields import EntraineursFields
from ffbb_api_client_v2.directus_ffbb.models.formations_fields import FormationsFields
from ffbb_api_client_v2.directus_ffbb.models.officiels_fields import OfficielsFields
from ffbb_api_client_v2.directus_ffbb.models.organisme_fields import OrganismeFields
from ffbb_api_client_v2.directus_ffbb.models.poule_fields import PouleFields
from ffbb_api_client_v2.directus_ffbb.models.pratiques_fields import PratiquesFields
from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
    QueryFieldsManager,
)
from ffbb_api_client_v2.directus_ffbb.models.rencontres_fields import RencontresFields
from ffbb_api_client_v2.directus_ffbb.models.saison_fields import SaisonFields
from ffbb_api_client_v2.directus_ffbb.models.salles_fields import SallesFields
from ffbb_api_client_v2.directus_ffbb.models.terrains_fields import TerrainsFields
from ffbb_api_client_v2.directus_ffbb.models.tournois_fields import TournoisFields
from ffbb_api_client_v2.facade.token_manager import TokenManager
from ffbb_api_client_v2.utils.retry_utils import RetryConfig, TimeoutConfig

PROJECT_ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

MAX_DEPTH = 10  # safety cap — loop will break earlier on error

# Adaptive timeout based on previous depth's actual response time.
# NOTE: HttpClient passes TimeoutConfig.total_timeout to requests as a single
# value (not a (connect, read) tuple), so total_timeout is the effective timeout.
BASE_TIMEOUT = 30.0  # used when no real timing data (first depth, all cached)
MIN_TIMEOUT = 10.0  # absolute minimum for any request
TIMEOUT_MULTIPLIER = 20.0  # adaptive: next timeout = prev_elapsed * multiplier
CACHE_THRESHOLD = 0.5  # responses faster than this are considered cache hits
MAX_TIMEOUT = 300.0  # absolute cap

FETCH_LIMIT = 50
MAX_WORKERS = 4  # concurrent endpoint discovery threads


def compute_adaptive_timeout(prev_elapsed: float | None) -> float:
    """Compute request timeout for the next depth level.

    - If prev_elapsed is real (non-cached): next = prev * multiplier, min MIN_TIMEOUT
    - If no real timing data (first depth or cached): use BASE_TIMEOUT
    """
    if prev_elapsed is not None and prev_elapsed >= CACHE_THRESHOLD:
        return min(max(prev_elapsed * TIMEOUT_MULTIPLIER, MIN_TIMEOUT), MAX_TIMEOUT)
    return BASE_TIMEOUT


def make_depth(level: int) -> str:
    """Build wildcard depth string: 1->'*', 2->'*.*', 3->'*.*.*', etc."""
    return ".".join("*" * level)


# ---------------------------------------------------------------------------
# 14 Directus endpoints
# ---------------------------------------------------------------------------
ENDPOINTS: dict[str, dict[str, Any]] = {
    "competitions": {"path": ENDPOINT_COMPETITIONS},
    "organismes": {"path": ENDPOINT_ORGANISMES},
    "poules": {"path": ENDPOINT_POULES},
    "saisons": {"path": ENDPOINT_SAISONS},
    "rencontres": {"path": ENDPOINT_RENCONTRES},
    "salles": {"path": ENDPOINT_SALLES},
    "terrains": {"path": ENDPOINT_TERRAINS},
    "tournois": {"path": ENDPOINT_TOURNOIS},
    "engagements": {"path": ENDPOINT_ENGAGEMENTS},
    "formations": {"path": ENDPOINT_FORMATIONS},
    "communes": {"path": ENDPOINT_COMMUNES},
    "officiels": {"path": ENDPOINT_OFFICIELS},
    "entraineurs": {"path": ENDPOINT_ENTRAINEURS},
    "pratiques": {"path": ENDPOINT_PRATIQUES},
}

# ---------------------------------------------------------------------------
# Endpoint -> Fields class mapping
# ---------------------------------------------------------------------------
FIELDS_CLASSES: dict[str, type[QueryFieldsManager]] = {
    "competitions": CompetitionFields,
    "organismes": OrganismeFields,
    "poules": PouleFields,
    "saisons": SaisonFields,
    "rencontres": RencontresFields,
    "salles": SallesFields,
    "terrains": TerrainsFields,
    "tournois": TournoisFields,
    "engagements": EngagementsFields,
    "formations": FormationsFields,
    "communes": CommunesFields,
    "officiels": OfficielsFields,
    "entraineurs": EntraineursFields,
    "pratiques": PratiquesFields,
}

# ---------------------------------------------------------------------------
# Collections that have a dedicated endpoint (FK-only strategy)
# ---------------------------------------------------------------------------
COLLECTIONS_WITH_ENDPOINTS = {
    "ffbbserver_competitions",
    "ffbbserver_organismes",
    "ffbbserver_poules",
    "ffbbserver_saisons",
    "ffbbserver_rencontres",
    "ffbbserver_salles",
    "ffbbserver_terrains",
    "ffbbserver_tournois",
    "ffbbserver_engagements",
    "ffbbserver_formations",
    "ffbbserver_communes",
    "ffbbserver_officiels",
    "ffbbserver_entraineurs",
    "ffbbnational_pratiques",
}

# ---------------------------------------------------------------------------
# Relation field -> target collection
# None = embedded object (no dedicated endpoint, keep full depth)
# ---------------------------------------------------------------------------
FIELD_TO_COLLECTION: dict[str, str | None] = {
    # Relations with dedicated endpoints -> FK only
    "salle": "ffbbserver_salles",
    "commune": "ffbbserver_communes",
    "competitions": "ffbbserver_competitions",
    "engagements": "ffbbserver_engagements",
    "rencontres": "ffbbserver_rencontres",
    "officiels": "ffbbserver_officiels",
    "entraineurs": "ffbbserver_entraineurs",
    "entraineur": "ffbbserver_entraineurs",
    "entraineurAdjoint": "ffbbserver_entraineurs",
    "tournois": "ffbbserver_tournois",
    "terrains": "ffbbserver_terrains",
    "formations": "ffbbserver_formations",
    "poules": "ffbbserver_poules",
    "saison": "ffbbserver_saisons",
    "idPoule": "ffbbserver_poules",
    "idCompetition": "ffbbserver_competitions",
    "id_competition": "ffbbserver_competitions",
    "idCompetitionPere": "ffbbserver_competitions",
    "competition_origine": "ffbbserver_competitions",
    "competitionId": "ffbbserver_competitions",
    "organisateur": "ffbbserver_organismes",
    "organisme_id_pere": "ffbbserver_organismes",
    "idOrganisme": "ffbbserver_organismes",
    "organisme": "ffbbserver_organismes",
    "idOrganismeEquipe1": "ffbbserver_organismes",
    "idOrganismeEquipe2": "ffbbserver_organismes",
    "idEngagement": "ffbbserver_engagements",
    "idEngagementEquipe1": "ffbbserver_engagements",
    "idEngagementEquipe2": "ffbbserver_engagements",
    "idEngagement_equipe1": "ffbbserver_engagements",
    "idEngagement_equipe2": "ffbbserver_engagements",
    "rencontres_domiciles": "ffbbserver_rencontres",
    "rencontres_exterieur": "ffbbserver_rencontres",
    # Junction table FK back-references (M2M)
    "ffbbserver_tournois_id": "ffbbserver_tournois",
    "ffbbserver_organismes_id": "ffbbserver_organismes",
    "idOrganisme_id": "ffbbserver_organismes",
    # Embedded objects (no dedicated endpoint) -> keep full depth
    "phases": None,
    "cartographie": None,
    "logo": None,
    "categorie": None,
    "gsId": None,
    "membres": None,
    "labellisation": None,
    "offresPratiques": None,
    "classements": None,
    "organismes_fils": None,
    "typeCompetitionGenerique": None,
    "classement": None,
    "niveau": None,
    "positions": None,
    "domain": None,
    "theme": None,
    "sessions": None,
    "tournoiType": None,
    "tournoiTypes3x3": None,
    "document_flyer": None,
    "affiche": None,
    "image": None,
    "type_association": None,
    "natureSol": None,
    "idLabellisationProgramme": None,
    "officiel": None,
    "fonction": None,
}


# ---------------------------------------------------------------------------
# Cache setup
# ---------------------------------------------------------------------------
def create_cached_session() -> CachedSession:
    """Create a sqlite-backed cached session (30 min expiry)."""
    cache_path = PROJECT_ROOT / "data" / "discovery_http_cache"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    session = CachedSession(
        str(cache_path),
        backend="sqlite",
        expire_after=1800,
        allowable_methods=("GET",),
    )
    logger.info(f"HTTP cache: sqlite at {cache_path}.sqlite (expire=1800s)")
    return session


# ---------------------------------------------------------------------------
# Helpers
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


def flatten_keys_with_types(obj: Any, prefix: str = "") -> dict[str, str]:
    """Flatten JSON keys with value type info: 'scalar', 'object', 'list', 'null'."""
    result: dict[str, str] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if v is None:
                result[full_key] = "null"
            elif isinstance(v, dict):
                result[full_key] = "object"
                result.update(flatten_keys_with_types(v, full_key))
            elif isinstance(v, list):
                result[full_key] = "list"
                for item in v:
                    result.update(flatten_keys_with_types(item, full_key))
            else:
                result[full_key] = f"scalar({type(v).__name__})"
    return result


@dataclass
class FetchResult:
    """Result of a single depth fetch."""

    data: dict[str, Any] | None = None
    ok: bool = False
    error: str | None = None  # short error category
    status_code: int | None = None  # HTTP status if available
    elapsed: float = 0.0


def fetch_with_depth(
    headers: dict[str, str],
    endpoint: str,
    depth: str,
    cached_session: CachedSession,
    timeout_config: TimeoutConfig,
    retry_config: RetryConfig,
    tag: str = "",
    item_id: int | None = None,
    extra_params: dict[str, Any] | None = None,
) -> FetchResult:
    """Fetch an endpoint with a specific wildcard depth.

    Uses the shared cached_session, timeout_config, and retry_config.
    Returns a FetchResult with structured error information.
    """
    from requests.exceptions import ConnectionError as ReqConnectionError
    from requests.exceptions import ReadTimeout, Timeout

    from ffbb_api_client_v2.exceptions import (
        FFBBApiError,
        FFBBAuthError,
        FFBBNetworkError,
        FFBBNotFoundError,
        FFBBRateLimitError,
        FFBBServerError,
    )

    if item_id:
        url = f"{API_FFBB_BASE_URL}{endpoint}/{item_id}"
    else:
        url = f"{API_FFBB_BASE_URL}{endpoint}"

    params: dict[str, Any] = {
        "fields[]": [depth],
        "limit": str(FETCH_LIMIT),
        "sort": "-date_updated",
    }
    if extra_params:
        params.update(extra_params)

    final_url = url_with_params(url, params)
    logger.info(f"{tag}   GET {final_url}")
    t0 = time.monotonic()
    try:
        result = HttpClient.http_get_json(
            final_url,
            headers,
            cached_session=cached_session,
            timeout_config=timeout_config,
            retry_config=retry_config,
        )
        elapsed = time.monotonic() - t0
        items_count = 0
        resp_size = len(json.dumps(result, default=str)) if result else 0
        if result:
            data = result.get("data", result)
            if isinstance(data, list):
                items_count = len(data)
            elif isinstance(data, dict):
                items_count = 1
        logger.info(
            f"{tag}   -> 200 OK | {elapsed:.1f}s | {items_count} item(s) | "
            f"{resp_size:,} bytes"
        )
        return FetchResult(data=result, ok=True, elapsed=elapsed)

    except (ReadTimeout, Timeout) as e:
        elapsed = time.monotonic() - t0
        logger.warning(f"{tag}   -> TIMEOUT | {elapsed:.1f}s | {type(e).__name__}: {e}")
        return FetchResult(error="timeout", elapsed=elapsed)

    except FFBBNetworkError as e:
        elapsed = time.monotonic() - t0
        logger.warning(f"{tag}   -> NETWORK | {elapsed:.1f}s | {e}")
        return FetchResult(error="network", elapsed=elapsed)

    except FFBBAuthError as e:
        elapsed = time.monotonic() - t0
        logger.warning(f"{tag}   -> AUTH {e.status_code} | {elapsed:.1f}s | {e}")
        return FetchResult(error="auth", status_code=e.status_code, elapsed=elapsed)

    except FFBBNotFoundError as e:
        elapsed = time.monotonic() - t0
        logger.warning(f"{tag}   -> 404 NOT FOUND | {elapsed:.1f}s | {e}")
        return FetchResult(error="not_found", status_code=404, elapsed=elapsed)

    except FFBBRateLimitError as e:
        elapsed = time.monotonic() - t0
        logger.warning(f"{tag}   -> 429 RATE LIMIT | {elapsed:.1f}s | {e}")
        return FetchResult(error="rate_limit", status_code=429, elapsed=elapsed)

    except FFBBServerError as e:
        elapsed = time.monotonic() - t0
        logger.warning(f"{tag}   -> SERVER {e.status_code} | {elapsed:.1f}s | {e}")
        return FetchResult(error="server", status_code=e.status_code, elapsed=elapsed)

    except FFBBApiError as e:
        elapsed = time.monotonic() - t0
        logger.warning(
            f"{tag}   -> API ERROR {e.status_code} | {elapsed:.1f}s | "
            f"{type(e).__name__}: {e}"
        )
        return FetchResult(
            error="api_error", status_code=e.status_code, elapsed=elapsed
        )

    except ReqConnectionError as e:
        elapsed = time.monotonic() - t0
        logger.warning(
            f"{tag}   -> CONNECTION | {elapsed:.1f}s | {type(e).__name__}: {e}"
        )
        return FetchResult(error="connection", elapsed=elapsed)

    except Exception as e:
        elapsed = time.monotonic() - t0
        logger.warning(
            f"{tag}   -> UNEXPECTED | {elapsed:.1f}s | {type(e).__name__}: {e}"
        )
        return FetchResult(error="unexpected", elapsed=elapsed)


def compute_optimal_fields(
    all_discovered_fields: set[str],
    configured_fields: list[str] | None = None,
) -> dict[str, Any]:
    """Determine optimal fields for an endpoint.

    For each discovered field path, walk segments left to right.
    At the first segment that is a FK to a collection with a dedicated endpoint,
    truncate there and keep only that prefix. This handles nested FK at any depth
    (e.g. phases.poules -> stops at poules because poules has an endpoint).

    When configured_fields is provided, the optimal set is the intersection of
    FK-truncated discovered fields with the configured set. This gives a
    realistic view of what we actually need vs what the API offers.
    """
    # Phase 1: FK truncation on all discovered fields
    fk_truncated: set[str] = set()
    delegated: dict[str, str] = {}

    for field in all_discovered_fields:
        parts = field.split(".")
        truncated = False
        for i, segment in enumerate(parts):
            collection = FIELD_TO_COLLECTION.get(segment)
            if collection is not None and collection in COLLECTIONS_WITH_ENDPOINTS:
                # FK found -> keep path up to and including this segment
                fk_path = ".".join(parts[: i + 1])
                fk_truncated.add(fk_path)
                delegated[fk_path] = collection
                truncated = True
                break
        if not truncated:
            fk_truncated.add(field)

    # Phase 2: If configured_fields provided, optimal = configured ∩ fk_truncated
    # (i.e., only keep configured fields that actually exist in the API after
    # FK truncation). This prevents reporting hundreds of embedded sub-fields
    # we intentionally don't fetch as "missing".
    if configured_fields is not None:
        configured_set = set(configured_fields)
        optimal = configured_set & fk_truncated
        # Also include FK-only paths that are in configured but might be
        # expressed differently (e.g. configured has "commune" and
        # fk_truncated has "commune")
        for fk_path, collection in delegated.items():
            if fk_path in configured_set:
                optimal.add(fk_path)
    else:
        optimal = fk_truncated

    return {
        "optimal_fields": sorted(optimal),
        "optimal_count": len(optimal),
        "delegated_relations": delegated,
        "fk_truncated_count": len(fk_truncated),
    }


# ---------------------------------------------------------------------------
# Discovery logic
# ---------------------------------------------------------------------------
def discover_endpoint(
    headers: dict[str, str],
    name: str,
    config: dict[str, Any],
    cached_session: CachedSession,
    retry_config: RetryConfig,
) -> dict[str, Any]:
    """Discover fields for a single endpoint, increasing depth until error."""
    tag = f"[{name}] "
    result: dict[str, Any] = {
        "endpoint": config["path"],
        "depths": {},
        "max_useful_depth": "*",
        "total_unique_fields": 0,
    }

    all_fields: set[str] = set()
    all_fields_with_types: dict[str, str] = {}
    prev_count = 0
    prev_elapsed: float | None = None  # last non-cached response time
    seen_suffix_sets: list[frozenset[str]] = []  # for cycle detection

    endpoint_t0 = time.monotonic()

    for level in range(1, MAX_DEPTH + 1):
        depth = make_depth(level)
        request_timeout = compute_adaptive_timeout(prev_elapsed)
        level_timeout = TimeoutConfig(
            connect_timeout=request_timeout,
            read_timeout=request_timeout,
            total_timeout=request_timeout,
        )
        timeout_source = (
            f"adaptive from {prev_elapsed:.1f}s × {TIMEOUT_MULTIPLIER}"
            if prev_elapsed is not None and prev_elapsed >= CACHE_THRESHOLD
            else f"base ({BASE_TIMEOUT}s)"
        )
        logger.info(
            f"{tag}[depth {level}] fields={depth} "
            f"(limit={FETCH_LIMIT}, timeout={request_timeout:.1f}s — {timeout_source})"
        )

        fetch = fetch_with_depth(
            headers,
            config["path"],
            depth,
            cached_session,
            level_timeout,
            retry_config,
            tag=tag,
            item_id=config.get("id"),
            extra_params=config.get("extra_params"),
        )

        if not fetch.ok:
            result["depths"][depth] = {
                "status": "error",
                "error": fetch.error,
                "status_code": fetch.status_code,
                "elapsed": round(fetch.elapsed, 1),
                "fields_count": 0,
                "new_fields": [],
            }
            logger.warning(
                f"{tag}[depth {level}] {fetch.error}"
                f"{f' (HTTP {fetch.status_code})' if fetch.status_code else ''}"
                f" | stopping depth exploration"
            )
            break

        # Merge fields from all returned items
        raw = fetch.data
        actual_data = raw.get("data", raw) if raw else raw
        fields: set[str] = set()
        fields_with_types: dict[str, str] = {}
        if isinstance(actual_data, list):
            for item in actual_data:
                fields.update(flatten_keys(item))
                fields_with_types.update(flatten_keys_with_types(item))
        elif isinstance(actual_data, dict):
            fields = flatten_keys(actual_data)
            fields_with_types = flatten_keys_with_types(actual_data)

        new_fields = fields - all_fields
        all_fields.update(fields)
        all_fields_with_types.update(fields_with_types)

        result["depths"][depth] = {
            "status": "ok",
            "elapsed": round(fetch.elapsed, 1),
            "fields_count": len(fields),
            "cumulative_count": len(all_fields),
            "new_fields_count": len(new_fields),
            "new_fields": sorted(new_fields),
        }

        is_cached = fetch.elapsed < CACHE_THRESHOLD
        logger.info(
            f"{tag}[depth {level}] "
            f"{len(fields)} fields, +{len(new_fields)} new, "
            f"{len(all_fields)} cumulative ({fetch.elapsed:.1f}s"
            f"{' [cached]' if is_cached else ''})"
        )

        # Track last real (non-cached) response time for adaptive timeout
        if not is_cached:
            prev_elapsed = fetch.elapsed

        if len(all_fields) > prev_count:
            result["max_useful_depth"] = depth
        prev_count = len(all_fields)

        if not new_fields and level > 1:
            logger.info(
                f"{tag}[depth {level}] no new fields, " f"stopping depth exploration"
            )
            break

        # Detect recursive cycles: extract 2-segment suffixes of new fields
        # and compare with previous depths. If already seen, it's a loop.
        if new_fields and level > 2:
            suffixes = frozenset(
                ".".join(f.split(".")[-2:]) if "." in f else f for f in new_fields
            )
            if suffixes in seen_suffix_sets:
                logger.info(
                    f"{tag}[depth {level}] recursive cycle detected "
                    f"(+{len(new_fields)} fields are deeper nestings of "
                    f"known patterns), stopping"
                )
                break
            seen_suffix_sets.append(suffixes)

    endpoint_elapsed = time.monotonic() - endpoint_t0
    result["total_unique_fields"] = len(all_fields)
    result["all_fields"] = sorted(all_fields)
    result["field_types"] = dict(sorted(all_fields_with_types.items()))
    logger.info(
        f"{tag}done in {endpoint_elapsed:.1f}s: "
        f"{len(all_fields)} unique fields, max depth={result['max_useful_depth']}"
    )
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def process_endpoint(
    name: str,
    config: dict[str, Any],
    headers: dict[str, str],
    retry_config: RetryConfig,
    idx: int,
    total: int,
) -> tuple[str, dict[str, Any]]:
    """Process a single endpoint: discovery + comparison.

    Thread-safe: creates its own CachedSession.
    Returns (endpoint_name, report_entry).
    """
    tag = f"[{name}] "

    # Thread-local CachedSession — each thread gets its own SQLite connection
    cached_session = create_cached_session()

    collection_name = config["path"].replace("items/", "", 1)

    logger.info(
        f"\n{'='*60}\n"
        f"{tag}[{idx}/{total}] Discovering: {name} ({collection_name})\n"
        f"{'='*60}"
    )

    # Step 1: Runtime discovery via wildcard testing
    runtime_discovery = discover_endpoint(
        headers, name, config, cached_session, retry_config
    )

    # Step 2: Get configured fields from *Fields class
    fields_cls = FIELDS_CLASSES.get(name)
    configured_fields: list[str] = []
    if fields_cls:
        configured_fields = fields_cls.get_fields()

    discovered_set = set(runtime_discovery.get("all_fields", []))
    configured_set = set(configured_fields)

    # Step 3: Compute optimal fields (intersection of FK-truncated with configured)
    optimal = compute_optimal_fields(discovered_set, configured_fields)

    # Step 4: Compare
    # Over-fetched: fields we configure but API doesn't return (even after FK truncation)
    fk_truncated_set = set()
    for field in discovered_set:
        parts = field.split(".")
        truncated = False
        for i, segment in enumerate(parts):
            collection = FIELD_TO_COLLECTION.get(segment)
            if collection is not None and collection in COLLECTIONS_WITH_ENDPOINTS:
                fk_truncated_set.add(".".join(parts[: i + 1]))
                truncated = True
                break
        if not truncated:
            fk_truncated_set.add(field)

    over_fetched = sorted(configured_set - fk_truncated_set)

    # Missing: configured fields that ARE in the FK-truncated set = optimal
    # (these exist in the API). Anything NOT in optimal is over-fetched.
    # By construction: missing = optimal - configured = ∅ (empty)
    # because optimal = configured ∩ fk_truncated.
    missing_fields: list[str] = []

    # Informational: FK-truncated fields available but not configured
    available_unconfigured = sorted(fk_truncated_set - configured_set)

    entry = {
        "endpoint": config["path"],
        "collection": collection_name,
        "runtime_discovery": {
            "depths": runtime_discovery["depths"],
            "max_useful_depth": runtime_discovery["max_useful_depth"],
        },
        "max_useful_depth": runtime_discovery["max_useful_depth"],
        "discovered_fields": runtime_discovery.get("all_fields", []),
        "discovered_count": runtime_discovery["total_unique_fields"],
        "field_types": runtime_discovery.get("field_types", {}),
        "optimal_fields": optimal["optimal_fields"],
        "optimal_count": optimal["optimal_count"],
        "fk_truncated_count": optimal.get("fk_truncated_count", 0),
        "delegated_relations": optimal["delegated_relations"],
        "configured_fields": sorted(configured_fields),
        "configured_count": len(configured_fields),
        "missing_fields": missing_fields,
        "over_fetched": over_fetched,
        "available_unconfigured": available_unconfigured,
    }

    logger.info(
        f"{tag}Runtime: {runtime_discovery['total_unique_fields']} discovered, "
        f"max depth: {runtime_discovery['max_useful_depth']}"
    )
    logger.info(
        f"{tag}Optimal: {optimal['optimal_count']} fields, "
        f"configured: {len(configured_fields)}, "
        f"over-fetched: {len(over_fetched)}"
    )

    return (name, entry)


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover Directus API fields")
    parser.add_argument(
        "--workers",
        type=int,
        default=MAX_WORKERS,
        help=f"Number of parallel workers (default: {MAX_WORKERS})",
    )
    args = parser.parse_args()

    logger.info("=== Directus API Field Discovery (All 14 Endpoints) ===")

    logger.info("Fetching API token...")
    for attempt in range(3):
        try:
            tokens = TokenManager.get_tokens()
            if tokens and tokens.api_token:
                logger.info("API token OK")
                break
        except Exception as e:
            logger.warning(
                f"Token fetch attempt {attempt + 1}/3 failed: "
                f"{type(e).__name__}: {e}"
            )
            if attempt == 2:
                logger.error("Failed to fetch API token after 3 attempts")
                sys.exit(1)
            logger.info("Retrying in 5s...")
            time.sleep(5)
    else:
        logger.error("Failed to fetch API token")
        sys.exit(1)

    # Retry config for runtime wildcard discovery (timeout is adaptive per depth)
    retry_config = RetryConfig(max_attempts=1)
    logger.info(
        f"Runtime discovery: adaptive timeout "
        f"(base={BASE_TIMEOUT}s, min={MIN_TIMEOUT}s, "
        f"multiplier={TIMEOUT_MULTIPLIER}x prev, "
        f"cache_threshold={CACHE_THRESHOLD}s, max={MAX_TIMEOUT}s), "
        f"retries={retry_config.max_attempts}, "
        f"workers={args.workers}"
    )

    headers = {
        "Authorization": f"Bearer {tokens.api_token}",
        "user-agent": DEFAULT_USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
    }

    total_endpoints = len(ENDPOINTS)
    global_t0 = time.monotonic()

    # Parallel discovery: each thread gets its own CachedSession (thread-local
    # SQLite connection) to avoid "database is locked" errors.
    report: dict[str, Any] = {}

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for idx, (name, config) in enumerate(ENDPOINTS.items(), 1):
            future = executor.submit(
                process_endpoint,
                name,
                config,
                headers,
                retry_config,
                idx,
                total_endpoints,
            )
            futures[future] = name

        for future in as_completed(futures):
            ep_name = futures[future]
            try:
                result_name, result_entry = future.result()
                report[result_name] = result_entry
            except Exception as e:
                logger.error(f"  FATAL: {ep_name} raised {type(e).__name__}: {e}")

    # Reorder report to match ENDPOINTS declaration order
    ordered_report: dict[str, Any] = {}
    for name in ENDPOINTS:
        if name in report:
            ordered_report[name] = report[name]

    # Save JSON report
    output_path = PROJECT_ROOT / "data" / "directus_field_discovery.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(ordered_report, f, indent=2, default=str)

    global_elapsed = time.monotonic() - global_t0
    logger.info(f"\nReport saved to {output_path}")
    logger.info(
        f"Total: {total_endpoints} endpoints discovered in {global_elapsed:.1f}s "
        f"({global_elapsed / 60:.1f} min)"
    )

    # Print console summary
    print("\n=== RAPPORT COUVERTURE CHAMPS ===")
    all_ok = True
    for name, data in ordered_report.items():
        print(f"\n{name} ({data['endpoint']}):")
        print(
            f"  Decouverts:  {data['discovered_count']} champs "
            f"(profondeur max: {data['max_useful_depth']})"
        )
        print(
            f"  Configures:  {data['configured_count']} champs "
            f"(sur {data.get('fk_truncated_count', '?')} disponibles apres FK)"
        )
        if data["delegated_relations"]:
            delegated_str = ", ".join(
                f"{k} -> {v}" for k, v in data["delegated_relations"].items()
            )
            print(f"  Delegues (FK only): {delegated_str}")
        if data["over_fetched"]:
            all_ok = False
            print(
                f"  ERREUR Sur-fetched: {len(data['over_fetched'])} champs "
                f"non retournes par l'API : "
                f"{', '.join(data['over_fetched'][:10])}"
                f"{'...' if len(data['over_fetched']) > 10 else ''}"
            )
        if not data["over_fetched"]:
            print("  OK - aucune difference")

    print("\n" + "=" * 60)
    if all_ok:
        print("RESULTAT: OK - aucune difference sur les 14 endpoints")
    else:
        endpoints_with_errors = [
            n for n, d in ordered_report.items() if d["over_fetched"]
        ]
        print(
            f"RESULTAT: {len(endpoints_with_errors)} endpoint(s) avec erreurs : "
            f"{', '.join(endpoints_with_errors)}"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()
