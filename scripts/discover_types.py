#!/usr/bin/env python3
"""
Discover real types for properties currently typed as None (from_none).

This script makes real API calls (MeiliSearch + REST) to collect raw JSON data,
flattens it to map every JSON path to observed values, infers Python types,
and generates a corrections report.

Usage:
    python scripts/discover_types.py
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so we can import the client library
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ffbb_api_client_v2.config import (  # noqa: E402
    API_FFBB_BASE_URL,
    DEFAULT_USER_AGENT,
    ENDPOINT_COMMUNES,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_CONFIGURATION,
    ENDPOINT_ENGAGEMENTS,
    ENDPOINT_ENTRAINEURS,
    ENDPOINT_FORMATIONS,
    ENDPOINT_LIVES,
    ENDPOINT_OFFICIELS,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_PRATIQUES,
    ENDPOINT_RENCONTRES,
    ENDPOINT_SAISONS,
    ENDPOINT_SALLES,
    ENDPOINT_TERRAINS,
    ENDPOINT_TOURNOIS,
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
    MEILISEARCH_INDEX_ENGAGEMENTS,
    MEILISEARCH_INDEX_FORMATIONS,
)
from ffbb_api_client_v2.helpers.http_requests_utils import (  # noqa: E402
    http_get_json,
    http_post_json,
    url_with_params,
)
from ffbb_api_client_v2.utils.token_manager import TokenManager  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MEILI_BATCH_SIZE = 1000
MEILI_MAX_HITS = 100_000
REST_SAMPLE_SIZE = 50
REST_POULE_SAMPLE_SIZE = 20
REST_DELAY = 0.5  # seconds between REST calls
DATA_DIR = PROJECT_ROOT / "data"

# ---------------------------------------------------------------------------
# FROM_NONE_REGISTRY — 48 properties across 13 files
# ---------------------------------------------------------------------------
# Each entry: (file, class, python_name, json_key)
FROM_NONE_REGISTRY: list[tuple[str, str, str, str]] = [
    # document_flyer.py — DocumentFlyer (16)
    ("document_flyer.py", "DocumentFlyer", "charset", "charset"),
    ("document_flyer.py", "DocumentFlyer", "duration", "duration"),
    ("document_flyer.py", "DocumentFlyer", "embed", "embed"),
    ("document_flyer.py", "DocumentFlyer", "description", "description"),
    ("document_flyer.py", "DocumentFlyer", "location", "location"),
    ("document_flyer.py", "DocumentFlyer", "tags", "tags"),
    ("document_flyer.py", "DocumentFlyer", "credits", "credits"),
    (
        "document_flyer.py",
        "DocumentFlyer",
        "newsbridge_media_id",
        "newsbridge_media_id",
    ),
    (
        "document_flyer.py",
        "DocumentFlyer",
        "newsbridge_metadatas",
        "newsbridge_metadatas",
    ),
    ("document_flyer.py", "DocumentFlyer", "newsbridge_name", "newsbridge_name"),
    (
        "document_flyer.py",
        "DocumentFlyer",
        "newsbridge_recorded_at",
        "newsbridge_recorded_at",
    ),
    ("document_flyer.py", "DocumentFlyer", "focal_point_x", "focal_point_x"),
    ("document_flyer.py", "DocumentFlyer", "focal_point_y", "focal_point_y"),
    ("document_flyer.py", "DocumentFlyer", "uploaded_by", "uploaded_by"),
    ("document_flyer.py", "DocumentFlyer", "modified_by", "modified_by"),
    ("document_flyer.py", "DocumentFlyer", "newsbridge_mission", "newsbridge_mission"),
    # organisateur.py — Organisateur (6)
    ("organisateur.py", "Organisateur", "adresse_club_pro", "adresseClubPro"),
    ("organisateur.py", "Organisateur", "commune_club_pro", "communeClubPro"),
    ("organisateur.py", "Organisateur", "salle", "salle"),
    ("organisateur.py", "Organisateur", "type_association", "type_association"),
    ("organisateur.py", "Organisateur", "date_affiliation", "dateAffiliation"),
    ("organisateur.py", "Organisateur", "logo_base64", "logo_base64"),
    # organisme_id_pere.py — OrganismeIDPere (5)
    ("organisme_id_pere.py", "OrganismeIDPere", "adresse_club_pro", "adresseClubPro"),
    ("organisme_id_pere.py", "OrganismeIDPere", "commune_club_pro", "communeClubPro"),
    ("organisme_id_pere.py", "OrganismeIDPere", "salle", "salle"),
    ("organisme_id_pere.py", "OrganismeIDPere", "type_association", "type_association"),
    ("organisme_id_pere.py", "OrganismeIDPere", "date_affiliation", "dateAffiliation"),
    # cartographie.py — Cartographie (2)
    ("cartographie.py", "Cartographie", "date_created", "date_created"),
    ("cartographie.py", "Cartographie", "date_updated", "date_updated"),
    # commune.py — Commune (1)
    ("commune.py", "Commune", "code_insee", "codeInsee"),
    # folder.py — Folder (1)
    ("folder.py", "Folder", "parent", "parent"),
    # multi_search_result_organismes.py — OrganismesHit (1)
    (
        "multi_search_result_organismes.py",
        "OrganismesHit",
        "adresse_club_pro",
        "adresseClubPro",
    ),
    # multi_search_result_terrains.py — TerrainsHit (3)
    (
        "multi_search_result_terrains.py",
        "TerrainsHit",
        "nb_participant_prevu",
        "nbParticipantPrevu",
    ),
    (
        "multi_search_result_terrains.py",
        "TerrainsHit",
        "adresse_complement",
        "adresseComplement",
    ),
    ("multi_search_result_terrains.py", "TerrainsHit", "thumbnail", "thumbnail"),
    # multi_search_result_rencontres.py — RencontresHit (1)
    ("multi_search_result_rencontres.py", "RencontresHit", "thumbnail", "thumbnail"),
    # multi_search_result_competitions.py — CompetitionsHit (1)
    (
        "multi_search_result_competitions.py",
        "CompetitionsHit",
        "id_competition_pere",
        "idCompetitionPere",
    ),
    # multi_search_result_pratiques.py — PratiquesHit (6)
    (
        "multi_search_result_pratiques.py",
        "PratiquesHit",
        "date_created",
        "date_created",
    ),
    (
        "multi_search_result_pratiques.py",
        "PratiquesHit",
        "date_updated",
        "date_updated",
    ),
    ("multi_search_result_pratiques.py", "PratiquesHit", "facebook", "facebook"),
    ("multi_search_result_pratiques.py", "PratiquesHit", "twitter", "twitter"),
    ("multi_search_result_pratiques.py", "PratiquesHit", "latitude", "latitude"),
    ("multi_search_result_pratiques.py", "PratiquesHit", "longitude", "longitude"),
    # multi_search_result_salles.py — SallesHit (1)
    ("multi_search_result_salles.py", "SallesHit", "thumbnail", "thumbnail"),
    # multi_search_result_tournois.py — TournoisHit (1)
    ("multi_search_result_tournois.py", "TournoisHit", "thumbnail", "thumbnail"),
]

# Map MeiliSearch index → class names whose json_keys appear directly in hits
MEILI_INDEX_TO_CLASSES: dict[str, list[str]] = {
    "ffbbserver_organismes": ["OrganismesHit"],
    "ffbbserver_rencontres": ["RencontresHit"],
    "ffbbserver_terrains": ["TerrainsHit"],
    "ffbbserver_salles": ["SallesHit"],
    "ffbbserver_tournois": ["TournoisHit"],
    "ffbbserver_competitions": ["CompetitionsHit"],
    "ffbbnational_pratiques": ["PratiquesHit"],
    MEILISEARCH_INDEX_ENGAGEMENTS: ["EngagementsHit"],
    MEILISEARCH_INDEX_FORMATIONS: ["FormationsHit"],
}

# Build lookup: class_name → list of json_keys to watch
CLASS_JSON_KEYS: dict[str, list[str]] = {}
for _, cls, _, jk in FROM_NONE_REGISTRY:
    CLASS_JSON_KEYS.setdefault(cls, []).append(jk)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class PathStats:
    """Statistics for a single JSON path."""

    total: int = 0
    none_count: int = 0
    non_none_count: int = 0
    types: dict[str, int] = field(default_factory=dict)
    samples: list[Any] = field(default_factory=list)

    MAX_SAMPLES = 10

    def add_value(self, value: Any) -> None:
        self.total += 1
        if value is None:
            self.none_count += 1
            return
        self.non_none_count += 1
        type_name = type(value).__name__
        self.types[type_name] = self.types.get(type_name, 0) + 1
        if len(self.samples) < self.MAX_SAMPLES:
            self.samples.append(value)

    def to_dict(self) -> dict[str, Any]:
        # Truncate long sample strings for readability
        safe_samples = []
        for s in self.samples:
            if isinstance(s, str) and len(s) > 200:
                safe_samples.append(s[:200] + "...")
            elif isinstance(s, (dict, list)):
                txt = json.dumps(s, default=str, ensure_ascii=False)
                safe_samples.append(txt[:200] + "..." if len(txt) > 200 else txt)
            else:
                safe_samples.append(s)
        return {
            "total": self.total,
            "none_count": self.none_count,
            "non_none_count": self.non_none_count,
            "types": self.types,
            "samples": safe_samples,
        }


# ---------------------------------------------------------------------------
# TokenFetcher
# ---------------------------------------------------------------------------
class TokenFetcher:
    """Fetch API tokens using the project's TokenManager."""

    @staticmethod
    def fetch() -> tuple[str, str]:
        tokens = TokenManager.get_tokens()
        logger.info("Tokens acquired (API + MeiliSearch)")
        return tokens.api_token, tokens.meilisearch_token


# ---------------------------------------------------------------------------
# RawDataCollector
# ---------------------------------------------------------------------------
class RawDataCollector:
    """Makes raw HTTP calls to MeiliSearch and REST APIs."""

    def __init__(self, api_token: str, meili_token: str) -> None:
        self.api_headers = {
            "user-agent": DEFAULT_USER_AGENT,
            "Authorization": f"Bearer {api_token}",
        }
        self.meili_headers = {
            "user-agent": DEFAULT_USER_AGENT,
            "Authorization": f"Bearer {meili_token}",
            "Content-Type": "application/json",
        }
        self.meili_url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
        self.stats: dict[str, Any] = {"hits_per_index": {}, "rest_calls": {}}

    # -- MeiliSearch --------------------------------------------------------

    def collect_meilisearch(self, index_uid: str) -> list[dict[str, Any]]:
        """Paginate through a MeiliSearch index, returning raw hit dicts."""
        all_hits: list[dict[str, Any]] = []
        offset = 0

        while offset < MEILI_MAX_HITS:
            payload = {
                "queries": [
                    {
                        "indexUid": index_uid,
                        "limit": MEILI_BATCH_SIZE,
                        "offset": offset,
                    }
                ]
            }
            try:
                resp = http_post_json(
                    self.meili_url,
                    self.meili_headers,
                    data=payload,
                    timeout=30,
                )
            except Exception as exc:
                logger.warning(
                    "MeiliSearch %s offset=%d failed: %s", index_uid, offset, exc
                )
                break

            results = resp.get("results", [])
            if not results:
                break
            hits = results[0].get("hits", [])
            if not hits:
                break

            all_hits.extend(hits)
            estimated_total = results[0].get("estimatedTotalHits", 0)
            logger.info(
                "  %s: fetched %d hits (offset=%d, estimated=%d)",
                index_uid,
                len(all_hits),
                offset,
                estimated_total,
            )

            if len(hits) < MEILI_BATCH_SIZE:
                break
            offset += MEILI_BATCH_SIZE

        self.stats["hits_per_index"][index_uid] = len(all_hits)
        return all_hits

    # -- REST Directus API --------------------------------------------------

    def _rest_get(self, url: str) -> dict[str, Any] | None:
        """Single REST GET with rate limiting."""
        try:
            resp = http_get_json(url, self.api_headers, timeout=30)
            time.sleep(REST_DELAY)
            return resp
        except Exception as exc:
            logger.warning("REST GET %s failed: %s", url, exc)
            time.sleep(REST_DELAY)
            return None

    def collect_rest_wildcard(
        self, endpoint: str, ids: list[Any]
    ) -> list[dict[str, Any]]:
        """Fetch items by ID with fields[]=*.*.*"""
        results: list[dict[str, Any]] = []
        call_key = f"{endpoint}/wildcard"
        success = 0

        for item_id in ids:
            base_url = f"{API_FFBB_BASE_URL}{endpoint}/{item_id}"
            url = url_with_params(base_url, {"fields[]": ["*.*.*"]})
            resp = self._rest_get(url)
            if resp and isinstance(resp, dict):
                data = resp.get("data", resp)
                if isinstance(data, dict):
                    results.append(data)
                    success += 1
                elif isinstance(data, list):
                    results.extend(data)
                    success += 1

        self.stats["rest_calls"][call_key] = {
            "requested": len(ids),
            "success": success,
        }
        logger.info("  REST %s: %d/%d successful", call_key, success, len(ids))
        return results

    def collect_rest_targeted(
        self, endpoint: str, ids: list[Any], extra_fields: list[str]
    ) -> list[dict[str, Any]]:
        """Fetch items by ID with specific targeted fields."""
        results: list[dict[str, Any]] = []
        call_key = f"{endpoint}/targeted"
        success = 0

        # Build fields list: base + extra from_none fields
        all_fields = ["*.*.*"] + extra_fields

        for item_id in ids:
            base_url = f"{API_FFBB_BASE_URL}{endpoint}/{item_id}"
            url = url_with_params(base_url, {"fields[]": all_fields})
            resp = self._rest_get(url)
            if resp and isinstance(resp, dict):
                data = resp.get("data", resp)
                if isinstance(data, dict):
                    results.append(data)
                    success += 1
                elif isinstance(data, list):
                    results.extend(data)
                    success += 1

        self.stats["rest_calls"][call_key] = {
            "requested": len(ids),
            "success": success,
        }
        logger.info("  REST %s: %d/%d successful", call_key, success, len(ids))
        return results

    def collect_rest_list(
        self, endpoint: str, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Fetch a list endpoint (saisons, etc.)."""
        base_url = f"{API_FFBB_BASE_URL}{endpoint}"
        params: dict[str, Any] = {}
        if fields:
            params["fields[]"] = fields
        url = url_with_params(base_url, params) if params else base_url

        resp = self._rest_get(url)
        if not resp:
            return []

        data = resp.get("data", resp)
        if isinstance(data, list):
            self.stats["rest_calls"][endpoint] = {"count": len(data)}
            return data
        if isinstance(data, dict):
            self.stats["rest_calls"][endpoint] = {"count": 1}
            return [data]
        return []

    def collect_lives(self) -> dict[str, Any] | None:
        """Fetch lives.json (no fields param)."""
        url = f"{API_FFBB_BASE_URL}{ENDPOINT_LIVES}"
        resp = self._rest_get(url)
        if resp:
            self.stats["rest_calls"]["lives"] = {"fetched": True}
        return resp


# ---------------------------------------------------------------------------
# JsonFlattener
# ---------------------------------------------------------------------------
class JsonFlattener:
    """Flatten nested JSON into path → list[value] mappings."""

    def __init__(self) -> None:
        self.paths: dict[str, PathStats] = {}

    def flatten(self, obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                child_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    self.flatten(value, child_prefix)
                else:
                    self._record(child_prefix, value)
        elif isinstance(obj, list):
            arr_prefix = f"{prefix}[]" if prefix else "[]"
            for item in obj:
                self.flatten(item, arr_prefix)
        else:
            self._record(prefix, obj)

    def _record(self, path: str, value: Any) -> None:
        if path not in self.paths:
            self.paths[path] = PathStats()
        self.paths[path].add_value(value)

    def get_stats(self, path: str) -> PathStats | None:
        return self.paths.get(path)

    def find_matching_paths(self, json_key: str) -> list[str]:
        """Find all flattened paths ending with the given json_key."""
        suffix = f".{json_key}"
        return [p for p in self.paths if p.endswith(suffix) or p == json_key]


# ---------------------------------------------------------------------------
# TypeInferrer
# ---------------------------------------------------------------------------

# Regex patterns for type refinement
ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


@dataclass
class TypeInference:
    """Result of type inference for a single property."""

    file: str
    class_name: str
    python_name: str
    json_key: str
    current_type: str
    inferred_type: str
    converter: str
    evidence: dict[str, Any]


class TypeInferrer:
    """Analyze collected values and infer Python types."""

    @staticmethod
    def infer(stats: PathStats) -> tuple[str, str]:
        """Return (inferred_type, converter_function) from observed values."""
        if stats.non_none_count == 0:
            return "None", "from_none(obj, key)  # confirmed always None"

        type_counts = stats.types

        # Single type
        if len(type_counts) == 1:
            type_name = next(iter(type_counts))
            return TypeInferrer._infer_single(type_name, stats.samples)

        # Mixed types
        type_parts: list[str] = []
        converter_parts: list[str] = []
        for tn in sorted(type_counts.keys()):
            # Filter samples by type
            type_samples = [s for s in stats.samples if type(s).__name__ == tn]
            py_type, conv = TypeInferrer._infer_single(tn, type_samples)
            # Remove " | None" suffix for union building
            py_type = py_type.replace(" | None", "")
            type_parts.append(py_type)
            converter_parts.append(conv.split("(")[0])  # just the fn name

        union_type = " | ".join(type_parts) + " | None"
        converter = f"from_union([{', '.join(converter_parts)}], obj, key)"
        return union_type, converter

    @staticmethod
    def _infer_single(type_name: str, samples: list[Any]) -> tuple[str, str]:
        """Infer type from a single JSON type + samples."""
        if type_name == "str":
            return TypeInferrer._refine_str(samples)
        if type_name == "int":
            return "int | None", 'from_int(obj, "KEY")'
        if type_name == "float":
            return "float | None", 'from_float(obj, "KEY")'
        if type_name == "bool":
            return "bool | None", 'from_bool(obj, "KEY")'
        if type_name == "dict":
            return "dict | None", "from_obj(SubClass.from_dict, obj, key)"
        if type_name == "list":
            return "list | None", "from_list(item_fn, obj, key)"
        return f"{type_name} | None", "# unknown type"

    @staticmethod
    def _refine_str(samples: list[Any]) -> tuple[str, str]:
        """Refine string type: datetime, UUID, or plain str."""
        str_samples = [s for s in samples if isinstance(s, str)]
        if not str_samples:
            return "str | None", 'from_str(obj, "KEY")'

        # Check datetime pattern
        dt_matches = sum(1 for s in str_samples if ISO_DATETIME_RE.match(s))
        if dt_matches == len(str_samples):
            return "datetime | None", 'from_datetime(obj, "KEY")'

        # Check UUID pattern
        uuid_matches = sum(1 for s in str_samples if UUID_RE.match(s))
        if uuid_matches == len(str_samples):
            return "UUID | None", 'from_uuid(obj, "KEY")'

        return "str | None", 'from_str(obj, "KEY")'


# ---------------------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------------------
class ReportGenerator:
    """Generate JSON reports and console summary."""

    @staticmethod
    def generate_raw_report(
        flattener: JsonFlattener,
        collector_stats: dict[str, Any],
    ) -> dict[str, Any]:
        report: dict[str, Any] = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                **collector_stats,
            },
            "paths": {},
        }
        for path, stats in sorted(flattener.paths.items()):
            report["paths"][path] = stats.to_dict()
        return report

    @staticmethod
    def generate_corrections(
        flattener: JsonFlattener,
        meili_flattener: JsonFlattener,
    ) -> dict[str, Any]:
        corrections: list[dict[str, Any]] = []
        resolved = 0
        confirmed_none = 0

        for file_name, class_name, py_name, json_key in FROM_NONE_REGISTRY:
            # Gather stats from all flatteners, merging them
            merged = PathStats()

            # Search in both flatteners
            for fl in [flattener, meili_flattener]:
                matching_paths = fl.find_matching_paths(json_key)
                for mp in matching_paths:
                    ps = fl.get_stats(mp)
                    if ps:
                        merged.total += ps.total
                        merged.none_count += ps.none_count
                        merged.non_none_count += ps.non_none_count
                        for tn, cnt in ps.types.items():
                            merged.types[tn] = merged.types.get(tn, 0) + cnt
                        remaining = PathStats.MAX_SAMPLES - len(merged.samples)
                        if remaining > 0:
                            merged.samples.extend(ps.samples[:remaining])

            inferred_type, converter = TypeInferrer.infer(merged)
            # Replace KEY placeholder with actual json_key
            converter = converter.replace("KEY", json_key)

            if inferred_type == "None":
                confirmed_none += 1
            else:
                resolved += 1

            corrections.append(
                {
                    "file": f"src/ffbb_api_client_v2/models/{file_name}",
                    "class": class_name,
                    "property": py_name,
                    "json_key": json_key,
                    "current_type": "None",
                    "inferred_type": inferred_type,
                    "converter": converter,
                    "evidence": {
                        "total": merged.total,
                        "non_none": merged.non_none_count,
                        "samples": merged.to_dict()["samples"],
                    },
                }
            )

        return {
            "summary": {
                "total": len(FROM_NONE_REGISTRY),
                "resolved": resolved,
                "confirmed_none": confirmed_none,
            },
            "corrections": corrections,
        }

    @staticmethod
    def print_console_summary(corrections_report: dict[str, Any]) -> None:
        summary = corrections_report["summary"]
        print("\n" + "=" * 70)
        print("TYPE DISCOVERY RESULTS")
        print("=" * 70)
        print(f"Total properties analyzed: {summary['total']}")
        print(f"  Resolved (type found):   {summary['resolved']}")
        print(f"  Confirmed None:          {summary['confirmed_none']}")
        print("-" * 70)

        for c in corrections_report["corrections"]:
            status = "NONE" if c["inferred_type"] == "None" else "FOUND"
            marker = "  " if status == "NONE" else ">>"
            print(
                f"{marker} {c['class']}.{c['property']}: "
                f"{c['current_type']} -> {c['inferred_type']}  "
                f"(evidence: {c['evidence']['non_none']}/{c['evidence']['total']})"
            )
            if c["evidence"]["samples"] and c["inferred_type"] != "None":
                sample_str = str(c["evidence"]["samples"][0])
                if len(sample_str) > 80:
                    sample_str = sample_str[:80] + "..."
                print(f"     sample: {sample_str}")

        print("=" * 70)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------
def main() -> None:
    logger.info("=== Type Discovery Script ===")

    # 0. Ensure data/ directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Fetch tokens
    logger.info("Phase 0: Fetching tokens...")
    api_token, meili_token = TokenFetcher.fetch()

    collector = RawDataCollector(api_token, meili_token)
    meili_flattener = JsonFlattener()  # MeiliSearch hits
    rest_flattener = JsonFlattener()  # REST API responses

    # 2. Phase 1: MeiliSearch collection
    logger.info("Phase 1: MeiliSearch collection...")
    meili_ids: dict[str, list[Any]] = {}  # index → list of IDs for REST phase

    for index_uid in MEILI_INDEX_TO_CLASSES:
        logger.info("Collecting from %s...", index_uid)
        hits = collector.collect_meilisearch(index_uid)

        # Extract IDs for REST phase
        ids = []
        for hit in hits:
            hit_id = hit.get("id")
            if hit_id is not None:
                ids.append(hit_id)
        meili_ids[index_uid] = ids

        # Flatten hits for type discovery
        for hit in hits:
            meili_flattener.flatten(hit, f"meilisearch/{index_uid}/hits[]")

    # 3. Phase 2: REST API collection
    logger.info("Phase 2: REST API collection...")

    # Responses dir for raw JSON samples
    responses_dir = DATA_DIR / "responses"
    responses_dir.mkdir(parents=True, exist_ok=True)

    def _save_samples(endpoint_name: str, data: list[dict[str, Any]]) -> None:
        """Save 2-3 raw response samples to data/responses/."""
        samples = data[:3]
        if samples:
            out_path = responses_dir / f"{endpoint_name}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(samples, f, indent=2, default=str, ensure_ascii=False)
            logger.info("  Saved %d samples to %s", len(samples), out_path)

    # 2a. Wildcard: organismes
    org_ids = meili_ids.get("ffbbserver_organismes", [])[:REST_SAMPLE_SIZE]
    if org_ids:
        logger.info("Fetching %d organismes (wildcard)...", len(org_ids))
        org_data = collector.collect_rest_wildcard(ENDPOINT_ORGANISMES, org_ids)
        for item in org_data:
            rest_flattener.flatten(item, "rest/organismes")
        _save_samples("organismes", org_data)

    # 2a. Wildcard: competitions
    comp_ids = meili_ids.get("ffbbserver_competitions", [])[:REST_SAMPLE_SIZE]
    if comp_ids:
        logger.info("Fetching %d competitions (wildcard)...", len(comp_ids))
        comp_data = collector.collect_rest_wildcard(ENDPOINT_COMPETITIONS, comp_ids)
        # Extract poule IDs from nested competition data
        poule_ids: list[Any] = []
        for item in comp_data:
            rest_flattener.flatten(item, "rest/competitions")
            # Look for nested phases → poules
            phases = item.get("phases", [])
            if isinstance(phases, list):
                for phase in phases:
                    if isinstance(phase, dict):
                        poules = phase.get("poules", [])
                        if isinstance(poules, list):
                            for poule in poules:
                                if isinstance(poule, dict):
                                    pid = poule.get("id")
                                    if pid is not None:
                                        poule_ids.append(pid)
        _save_samples("competitions", comp_data)

        # 2a. Wildcard: poules
        poule_sample = poule_ids[:REST_POULE_SAMPLE_SIZE]
        if poule_sample:
            logger.info("Fetching %d poules (wildcard)...", len(poule_sample))
            poule_data = collector.collect_rest_wildcard(ENDPOINT_POULES, poule_sample)
            for item in poule_data:
                rest_flattener.flatten(item, "rest/poules")
            _save_samples("poules", poule_data)

    # 2a. Wildcard: saisons
    logger.info("Fetching saisons...")
    saisons_data = collector.collect_rest_list(ENDPOINT_SAISONS, ["*.*.*"])
    for item in saisons_data:
        rest_flattener.flatten(item, "rest/saisons")
    _save_samples("saisons", saisons_data)

    # 2a. lives.json
    logger.info("Fetching lives.json...")
    lives_data = collector.collect_lives()
    if lives_data:
        rest_flattener.flatten(lives_data, "rest/lives")
        _save_samples(
            "lives", [lives_data] if isinstance(lives_data, dict) else lives_data
        )

    # --- NEW: 11 additional REST endpoints ---

    # List endpoints (communes, officiels, entraineurs, pratiques)
    for endpoint, name in [
        (ENDPOINT_COMMUNES, "communes"),
        (ENDPOINT_OFFICIELS, "officiels"),
        (ENDPOINT_ENTRAINEURS, "entraineurs"),
        (ENDPOINT_PRATIQUES, "pratiques"),
    ]:
        logger.info("Fetching %s (list)...", name)
        list_data = collector.collect_rest_list(endpoint, ["*.*.*"])
        for item in list_data:
            rest_flattener.flatten(item, f"rest/{name}")
        _save_samples(name, list_data)

    # Wildcard by ID endpoints (using IDs from MeiliSearch)
    meili_to_rest = [
        ("ffbbserver_rencontres", ENDPOINT_RENCONTRES, "rencontres"),
        ("ffbbserver_salles", ENDPOINT_SALLES, "salles"),
        ("ffbbserver_terrains", ENDPOINT_TERRAINS, "terrains"),
        ("ffbbserver_tournois", ENDPOINT_TOURNOIS, "tournois"),
        (MEILISEARCH_INDEX_ENGAGEMENTS, ENDPOINT_ENGAGEMENTS, "engagements"),
        (MEILISEARCH_INDEX_FORMATIONS, ENDPOINT_FORMATIONS, "formations"),
    ]
    for index_uid, endpoint, name in meili_to_rest:
        ids = meili_ids.get(index_uid, [])[:REST_SAMPLE_SIZE]
        if ids:
            logger.info("Fetching %d %s (wildcard)...", len(ids), name)
            endpoint_data = collector.collect_rest_wildcard(endpoint, ids)
            for item in endpoint_data:
                rest_flattener.flatten(item, f"rest/{name}")
            _save_samples(name, endpoint_data)

    # Single endpoint: configuration
    logger.info("Fetching configuration...")
    config_data = collector.collect_rest_list(ENDPOINT_CONFIGURATION, ["*.*.*"])
    for item in config_data:
        rest_flattener.flatten(item, "rest/configuration")
    _save_samples("configuration", config_data)

    # 2b. Targeted: organismes with explicit from_none fields
    if org_ids:
        logger.info("Fetching %d organismes (targeted)...", len(org_ids))
        targeted_org = collector.collect_rest_targeted(
            ENDPOINT_ORGANISMES,
            org_ids,
            [
                "adresseClubPro",
                "communeClubPro",
                "salle.*",
                "type_association.*",
                "dateAffiliation",
                "logo_base64",
                "commune.codeInsee",
                "cartographie.date_created",
                "cartographie.date_updated",
                "document_flyer.*",
            ],
        )
        for item in targeted_org:
            rest_flattener.flatten(item, "rest/organismes_targeted")

    # 2b. Targeted: competitions with from_none fields
    if comp_ids:
        logger.info("Fetching %d competitions (targeted)...", len(comp_ids))
        targeted_comp = collector.collect_rest_targeted(
            ENDPOINT_COMPETITIONS,
            comp_ids,
            ["idCompetitionPere.*"],
        )
        for item in targeted_comp:
            rest_flattener.flatten(item, "rest/competitions_targeted")

    # 4. Generate reports
    logger.info("Phase 3: Generating reports...")

    # Merge both flatteners for the raw report
    combined_flattener = JsonFlattener()
    combined_flattener.paths.update(meili_flattener.paths)
    combined_flattener.paths.update(rest_flattener.paths)

    raw_report = ReportGenerator.generate_raw_report(
        combined_flattener, collector.stats
    )
    corrections_report = ReportGenerator.generate_corrections(
        rest_flattener, meili_flattener
    )

    # Write JSON files
    raw_path = DATA_DIR / "type_discovery_raw.json"
    corrections_path = DATA_DIR / "type_discovery_corrections.json"

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_report, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Raw report written to %s", raw_path)

    with open(corrections_path, "w", encoding="utf-8") as f:
        json.dump(corrections_report, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Corrections report written to %s", corrections_path)

    # 5. Phase 4: Enum candidate detection
    logger.info("Phase 4: Detecting enum candidates...")
    enum_candidates: list[dict[str, Any]] = []

    for path, stats in combined_flattener.paths.items():
        # Only consider str-typed paths with low cardinality
        if stats.non_none_count < 10:
            continue
        if "str" not in stats.types:
            continue
        # Collect all unique string values from samples
        str_samples = [s for s in stats.samples if isinstance(s, str)]
        if not str_samples:
            continue
        # Estimate unique values — we only have up to MAX_SAMPLES
        unique_values = sorted(set(str_samples))
        # If cardinality is low relative to observations, it's likely an enum
        if len(unique_values) < 50:
            enum_candidates.append(
                {
                    "json_path": path,
                    "unique_values": unique_values,
                    "count": len(unique_values),
                    "total_observations": stats.total,
                    "non_none_observations": stats.non_none_count,
                }
            )

    enum_candidates.sort(key=lambda x: x["count"])
    enum_path = DATA_DIR / "enum_candidates.json"
    with open(enum_path, "w", encoding="utf-8") as f:
        json.dump(enum_candidates, f, indent=2, ensure_ascii=False)
    logger.info(
        "Enum candidates: %d paths written to %s", len(enum_candidates), enum_path
    )

    # Console summary
    ReportGenerator.print_console_summary(corrections_report)

    logger.info("Done.")


if __name__ == "__main__":
    main()
