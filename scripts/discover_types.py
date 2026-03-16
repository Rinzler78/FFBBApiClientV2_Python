#!/usr/bin/env python3
"""
Discover real types for incorrectly typed model properties.

This script:
  1. Dynamically scans source code (AST) to find properties typed as
     dict[str, Any], list[Any], Any | None, or using raw obj.get().
  2. Builds model signatures from all from_dict methods for structural matching.
  3. Makes real API calls (MeiliSearch + REST) to collect raw JSON data.
     All HTTP responses are cached in SQLite (24h TTL) so re-runs are instant.
  4. Infers correct Python types using observed data, structural matching,
     and a name-based concordance table.
  5. Generates a comprehensive corrections report.

Usage:
    python scripts/discover_types.py              # normal run (uses cache)
    python scripts/discover_types.py --clear-cache  # force fresh data
    python scripts/discover_types.py --workers 4    # limit parallelism
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import logging
import os
import re
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from requests_cache import CachedSession as RawCachedSession

import ffbb_api_client_v2.directus_ffbb.config as _directus_config
import ffbb_api_client_v2.meilisearch_ffbb.config as _meili_config
from ffbb_api_client_v2.config import (
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
)
from ffbb_api_client_v2.directus.client import DEFAULT_USER_AGENT
from ffbb_api_client_v2.directus_ffbb.config import (
    API_FFBB_BASE_URL,
    ENDPOINT_CONFIGURATION,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"

# Regex for camelCase → snake_case conversion
_CAMEL_RE1 = re.compile(r"(.)([A-Z][a-z]+)")
_CAMEL_RE2 = re.compile(r"([a-z0-9])([A-Z])")


def _camel_to_snake(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case."""
    s = _CAMEL_RE1.sub(r"\1_\2", name)
    return _CAMEL_RE2.sub(r"\1_\2", s).lower()


def _json_type_to_python(
    types: dict[str, int],
    none_count: int,
    total: int,
    json_key: str,
    *,
    samples: list[Any] | None = None,
) -> tuple[str, str]:
    """Map observed JSON types to Python type annotation and converter.

    Returns:
        (suggested_type, suggested_converter) tuple.
    """
    nullable = none_count > 0
    suffix = " | None" if nullable else ""

    if not types:
        # Always None → guess from name, fallback str | None
        hint = infer_from_name(_camel_to_snake(json_key))
        if hint:
            return hint[0], f'{hint[1]}(obj, "{json_key}")'
        return f"str{suffix}", f'from_str(obj, "{json_key}")'

    type_names = set(types.keys())

    if type_names == {"str"}:
        # Refine: check if actually datetime or UUID
        if samples:
            str_samples = [s for s in samples if isinstance(s, str)]
            if str_samples:
                if all(ISO_DATETIME_RE.match(s) for s in str_samples):
                    return f"datetime{suffix}", f'from_datetime(obj, "{json_key}")'
                if all(UUID_RE.match(s) for s in str_samples):
                    return f"UUID{suffix}", f'from_uuid(obj, "{json_key}")'
        return f"str{suffix}", f'from_str(obj, "{json_key}")'
    if type_names == {"int"}:
        return f"int{suffix}", f'from_int(obj, "{json_key}")'
    if type_names == {"float"}:
        return f"float{suffix}", f'from_float(obj, "{json_key}")'
    if type_names == {"bool"}:
        return f"bool{suffix}", f'from_bool(obj, "{json_key}")'
    if type_names == {"dict"}:
        return (
            f"dict[str, Any]{suffix}",
            f'from_obj(SubClass.from_dict, obj, "{json_key}")',
        )
    if type_names == {"list"}:
        return f"list[Any]{suffix}", f'from_list(item_fn, obj, "{json_key}")'
    if type_names <= {"int", "float"}:
        return f"float{suffix}", f'from_float(obj, "{json_key}")'

    # Mixed types
    parts = []
    for tn in sorted(type_names):
        if tn == "str":
            parts.append("str")
        elif tn == "int":
            parts.append("int")
        elif tn == "float":
            parts.append("float")
        elif tn == "bool":
            parts.append("bool")
        else:
            parts.append(tn)
    return " | ".join(parts) + suffix, f'# mixed types for "{json_key}"'


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MEILI_BATCH_SIZE = 1000  # MeiliSearch supports large batches
MEILI_MAX_HITS = 5000
REST_PAGE_SIZE = 1000  # large pages = fewer HTTP round-trips
REST_MAX_ITEMS = 100_000  # collect as much data as possible
REST_RETRY_MAX = 3  # retry 502/504 errors
REST_RETRY_BACKOFF = 5.0  # seconds initial backoff for retries
REST_PARALLEL_WORKERS = os.cpu_count() or 8  # use all CPU threads
CACHE_TTL = 86400  # 24 hours — cached responses stay valid for a day
DATA_DIR = PROJECT_ROOT / "data"

# Model source directories to scan
MODEL_DIRS = [
    SRC_ROOT / "ffbb_api_client_v2" / "models",
    SRC_ROOT / "ffbb_api_client_v2" / "meilisearch_ffbb" / "models",
    SRC_ROOT / "ffbb_api_client_v2" / "directus_ffbb" / "models",
]


# ---------------------------------------------------------------------------
# FK chain map — cross-endpoint relations for deeper discovery
# ---------------------------------------------------------------------------
FK_CHAIN_MAP: dict[tuple[str, str], str] = {
    # (source_endpoint, fk_json_key) -> target_endpoint
    ("rencontres", "competitionId"): "competitions",
    ("rencontres", "idOrganismeEquipe1"): "organismes",
    ("rencontres", "idOrganismeEquipe2"): "organismes",
    ("rencontres", "idPoule"): "poules",
    ("rencontres", "salle"): "salles",
    ("rencontres", "saison"): "saisons",
    ("competitions", "saison"): "saisons",
    ("competitions", "organisateur"): "organismes",
    ("competitions", "competition_origine"): "competitions",
    ("engagements", "idCompetition"): "competitions",
    ("engagements", "idOrganisme"): "organismes",
    ("engagements", "idPoule"): "poules",
    ("organismes", "commune"): "communes",
    ("organismes", "salle"): "salles",
    ("organismes", "organisme_id_pere"): "organismes",
    ("poules", "id_competition"): "competitions",
    ("tournois", "commune"): "communes",
}


# ---------------------------------------------------------------------------
# RawHttpClient — direct HTTP using requests + requests_cache
# ---------------------------------------------------------------------------
class RawHttpClient:
    """HTTP client using requests directly (not the lib's HttpClient).

    Uses requests_cache with SQLite WAL for thread-safe caching.
    """

    def __init__(self, cache_dir: Path, cache_ttl: int = CACHE_TTL):
        self._cache_dir = cache_dir
        self._cache_ttl = cache_ttl
        self._thread_local = threading.local()

    def _get_session(self) -> RawCachedSession:
        """Return a thread-local cached session."""
        if not hasattr(self._thread_local, "session"):
            cache_path = self._cache_dir / "discover_types_cache"
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._thread_local.session = RawCachedSession(
                str(cache_path),
                backend="sqlite",
                expire_after=self._cache_ttl,
                allowable_methods=("GET", "POST"),
                wal=True,
            )
        return self._thread_local.session

    @staticmethod
    def build_url(
        base: str, endpoint: str, params: dict[str, Any] | None = None
    ) -> str:
        """Build URL with [] not encoded (Directus returns 403 on %5B%5D)."""
        url = f"{base}{endpoint}"
        if not params:
            return url
        parts: list[str] = []
        for key, val in params.items():
            if isinstance(val, list):
                for v in val:
                    parts.append(f"{key}={v}")
            elif val is not None:
                parts.append(f"{key}={val}")
        return f"{url}?{'&'.join(parts)}"

    def get_json(
        self,
        url: str,
        headers: dict[str, str],
        timeout: int = 60,
        max_retries: int = REST_RETRY_MAX,
        backoff: float = REST_RETRY_BACKOFF,
    ) -> dict[str, Any] | list[Any] | None:
        """GET with retry on 502/504, skip on 403/404."""
        session = self._get_session()
        for attempt in range(max_retries + 1):
            try:
                response = session.get(url, headers=headers, timeout=timeout)
                cached = getattr(response, "from_cache", False)
                logger.debug(
                    "  [cache %s] GET %s",
                    "HIT" if cached else "MISS",
                    url[:120],
                )
                status = response.status_code
                if status in (403, 404):
                    logger.debug("  [%d] GET %s — skipped", status, url[:100])
                    return None
                if status >= 500:
                    raise RuntimeError(f"HTTP {status}")
                response.raise_for_status()
                return response.json()
            except Exception as exc:
                exc_str = str(exc)
                is_retryable = any(
                    code in exc_str for code in ("502", "504", "timed out")
                )
                if is_retryable and attempt < max_retries:
                    wait = backoff * (2**attempt)
                    logger.warning(
                        "GET %s failed (attempt %d/%d): %s — retrying in %.0fs",
                        url[:100],
                        attempt + 1,
                        max_retries + 1,
                        exc,
                        wait,
                    )
                    time.sleep(wait)
                else:
                    logger.warning("GET %s failed: %s", url[:100], exc)
                    return None
        return None

    def post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
        timeout: int = 60,
    ) -> dict[str, Any] | None:
        """POST for MeiliSearch multi-search."""
        session = self._get_session()
        try:
            response = session.post(url, headers=headers, json=payload, timeout=timeout)
            cached = getattr(response, "from_cache", False)
            logger.debug(
                "  [cache %s] POST %s",
                "HIT" if cached else "MISS",
                url[:100],
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            logger.warning("POST %s failed: %s", url[:100], exc)
            return None

    def acquire_tokens(self) -> tuple[str, str]:
        """Get API + MeiliSearch tokens from env vars or /items/configuration."""
        api = os.getenv("API_FFBB_APP_BEARER_TOKEN")
        meili = os.getenv("MEILISEARCH_BEARER_TOKEN")
        if api and meili:
            return api, meili

        url = f"{API_FFBB_BASE_URL}{ENDPOINT_CONFIGURATION}"
        session = self._get_session()
        resp = session.get(url, headers={"user-agent": DEFAULT_USER_AGENT}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        actual = data.get("data", data)
        return actual["key_dh"], actual["key_ms"]


# ---------------------------------------------------------------------------
# IncorrectProperty — result of source code scanning
# ---------------------------------------------------------------------------
@dataclass
class IncorrectProperty:
    """A property with an incorrect or imprecise type annotation."""

    file: str  # relative to src/
    class_name: str
    python_name: str
    json_key: str
    current_type: str  # annotation string
    category: str  # dict_any, list_any, any_none, list_dict_any


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------
def _is_dataclass(node: ast.ClassDef) -> bool:
    """Check if a class has @dataclass decorator."""
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "dataclass":
            return True
        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
            if dec.func.id == "dataclass":
                return True
    return False


def _extract_json_key_from_call(call: ast.Call) -> str | None:
    """Extract json_key string from a converter call or obj.get() call."""
    if isinstance(call.func, ast.Name) and call.func.id.startswith("from_"):
        fn_name = call.func.id
        if fn_name in ("from_obj", "from_list", "from_enum"):
            if (
                len(call.args) >= 3
                and isinstance(call.args[2], ast.Constant)
                and isinstance(call.args[2].value, str)
            ):
                return call.args[2].value
        else:
            if (
                len(call.args) >= 2
                and isinstance(call.args[1], ast.Constant)
                and isinstance(call.args[1].value, str)
            ):
                return call.args[1].value

    if isinstance(call.func, ast.Attribute) and call.func.attr == "get":
        if (
            call.args
            and isinstance(call.args[0], ast.Constant)
            and isinstance(call.args[0].value, str)
        ):
            return call.args[0].value

    return None


def _extract_json_key_from_expr(expr: ast.expr) -> str | None:
    """Recursively search an expression tree for a json_key."""
    for child in ast.walk(expr):
        if isinstance(child, ast.Call):
            key = _extract_json_key_from_call(child)
            if key:
                return key
    return None


def _classify_annotation(
    annotation_str: str,
    field_name: str = "",
) -> str | None:
    """Classify an annotation string as an incorrect type, or None if OK."""
    s = annotation_str.strip()

    if re.search(r"list\[dict\[str,\s*Any\]\]", s):
        return "list_dict_any"
    if re.search(r"dict\[str,\s*Any\]", s):
        return "dict_any"
    if re.search(r"(?<!\[)list\[Any\]", s):
        return "list_any"
    if re.match(r"^Any(\s*\|\s*None)?$", s):
        return "any_none"
    if re.match(r"^str(\s*\|\s*None)?$", s) and field_name:
        hint = infer_from_name(field_name)
        if hint and hint[0] != "str | None":
            return "str_wrong_type"

    return None


def _extract_json_keys_from_method(
    class_node: ast.ClassDef,
) -> dict[str, str]:
    """Extract python_name -> json_key mapping from from_dict method."""
    mapping: dict[str, str] = {}

    from_dict_method: ast.FunctionDef | None = None
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "from_dict":
            from_dict_method = item
            break

    if not from_dict_method:
        return mapping

    var_to_key: dict[str, str] = {}
    for node in ast.walk(from_dict_method):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                key = _extract_json_key_from_expr(node.value)
                if key:
                    var_to_key[var_name] = key
                    mapping[var_name] = key

    for node in ast.walk(from_dict_method):
        if not isinstance(node, ast.keyword) or not node.arg:
            continue
        key = _extract_json_key_from_expr(node.value)
        if key:
            mapping[node.arg] = key
        elif isinstance(node.value, ast.Name) and node.value.id in var_to_key:
            mapping[node.arg] = var_to_key[node.value.id]
        elif isinstance(node.value, ast.IfExp):
            if (
                isinstance(node.value.body, ast.Name)
                and node.value.body.id in var_to_key
            ):
                mapping[node.arg] = var_to_key[node.value.body.id]

    return mapping


# ---------------------------------------------------------------------------
# Combined AST scanner — single pass for both IncorrectProperty + signatures
# ---------------------------------------------------------------------------
@dataclass
class ModelSignature:
    class_name: str
    module_path: str
    json_keys: frozenset[str]
    # Enrichment fields for actionable reports
    json_to_python: dict[str, str] = field(
        default_factory=dict
    )  # json_key -> python_attr
    annotation_lines: dict[str, int] = field(
        default_factory=dict
    )  # python_attr -> line number
    class_line: int = 0  # line number of class definition


@dataclass
class ASTScanResult:
    """Result of combined AST scanning."""

    incorrect_props: list[IncorrectProperty]
    signatures: list[ModelSignature]


def scan_source_combined(model_dirs: list[Path]) -> ASTScanResult:
    """Single-pass AST scan: find incorrect properties AND build signatures."""
    props: list[IncorrectProperty] = []
    sigs: list[ModelSignature] = []

    for model_dir in model_dirs:
        if not model_dir.exists():
            continue
        for py_file in sorted(model_dir.glob("*.py")):
            if py_file.name.startswith("__"):
                continue
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source)
            except SyntaxError as e:
                logger.warning("Syntax error in %s: %s", py_file, e)
                continue

            rel_path = str(py_file.relative_to(SRC_ROOT / "ffbb_api_client_v2"))

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                if not _is_dataclass(node):
                    continue

                json_key_map = _extract_json_keys_from_method(node)

                # Build reverse mapping: json_key -> python_attr
                json_to_python: dict[str, str] = {v: k for k, v in json_key_map.items()}

                # Collect annotation line numbers
                annotation_lines: dict[str, int] = {}
                for field_node in node.body:
                    if isinstance(field_node, ast.AnnAssign) and isinstance(
                        field_node.target, ast.Name
                    ):
                        annotation_lines[field_node.target.id] = field_node.lineno

                # Build signature
                if len(json_key_map) >= 2:
                    sigs.append(
                        ModelSignature(
                            class_name=node.name,
                            module_path=rel_path,
                            json_keys=frozenset(json_key_map.values()),
                            json_to_python=json_to_python,
                            annotation_lines=annotation_lines,
                            class_line=node.lineno,
                        )
                    )

                # Check for incorrect annotations
                for field_node in node.body:
                    if isinstance(field_node, ast.AnnAssign) and isinstance(
                        field_node.target, ast.Name
                    ):
                        field_name = field_node.target.id
                        annotation_str = ast.unparse(field_node.annotation)
                        category = _classify_annotation(annotation_str, field_name)
                        if category:
                            json_key = json_key_map.get(field_name, field_name)
                            props.append(
                                IncorrectProperty(
                                    file=rel_path,
                                    class_name=node.name,
                                    python_name=field_name,
                                    json_key=json_key,
                                    current_type=annotation_str,
                                    category=category,
                                )
                            )

    return ASTScanResult(incorrect_props=props, signatures=sigs)


class ModelSignatureRegistry:
    """Match observed JSON key sets against model signatures."""

    def __init__(self, signatures: list[ModelSignature]) -> None:
        self.signatures = signatures

    def match(
        self, observed_keys: set[str], min_overlap: float = 0.4
    ) -> list[tuple[str, str, float]]:
        """Return [(class_name, module_path, jaccard_score)] sorted by score desc."""
        results: list[tuple[str, str, float]] = []
        for sig in self.signatures:
            if len(sig.json_keys) < 2:
                continue
            intersection = observed_keys & sig.json_keys
            union = observed_keys | sig.json_keys
            score = len(intersection) / len(union) if union else 0
            if score >= min_overlap:
                results.append((sig.class_name, sig.module_path, score))
        return sorted(results, key=lambda x: -x[2])


# ---------------------------------------------------------------------------
# Dynamic discovery of config constants and class-to-source mappings
# ---------------------------------------------------------------------------
def _discover_config_constants(module: Any, prefix: str) -> dict[str, str]:
    """Discover string constants from a module by prefix."""
    prefix_len = len(prefix)
    return {
        attr[prefix_len:].lower(): getattr(module, attr)
        for attr in dir(module)
        if attr.startswith(prefix) and isinstance(getattr(module, attr), str)
    }


def _build_meili_class_to_index(
    model_dirs: list[Path], meili_constants: dict[str, str]
) -> dict[str, str]:
    """Dynamically map Hit class names to MeiliSearch index UIDs."""
    meili_dir = next((d for d in model_dirs if "meilisearch_ffbb" in str(d)), None)
    if not meili_dir or not meili_dir.exists():
        return {}

    mapping: dict[str, str] = {}
    for py_file in sorted(meili_dir.glob("*_hit.py")):
        base = py_file.stem.replace("_hit", "")
        index_uid = meili_constants.get(base)
        if not index_uid:
            continue
        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name.endswith("Hit"):
                mapping[node.name] = index_uid
    return mapping


def _build_rest_class_to_prefix(
    model_dirs: list[Path], endpoint_map: dict[str, str]
) -> dict[str, str]:
    """Dynamically map Response class names to REST flattener prefixes."""
    directus_dir = next((d for d in model_dirs if "directus_ffbb" in str(d)), None)
    if not directus_dir or not directus_dir.exists():
        return {}

    mapping: dict[str, str] = {}
    for py_file in sorted(directus_dir.glob("get_*_response.py")):
        stem = py_file.stem
        base = stem[4:].rsplit("_response", 1)[0]

        if base in endpoint_map:
            endpoint_base = base
        elif base + "s" in endpoint_map:
            endpoint_base = base + "s"
        else:
            endpoint_base = base

        source = py_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ClassDef)
                and node.name.startswith("Get")
                and node.name.endswith("Response")
            ):
                mapping[node.name] = f"rest/{endpoint_base}"
    return mapping


def _build_endpoint_fields_map(
    model_dirs: list[Path], endpoint_map: dict[str, str]
) -> dict[str, list[str]]:
    """Dynamically map endpoint base names to their field lists.

    Scans *_fields.py modules, imports each QueryFieldsManager subclass,
    and calls get_fields() to get the exact field list for each endpoint.

    Returns:
        Dict mapping endpoint base name (e.g. "rencontres") to field list.
    """
    directus_dir = next((d for d in model_dirs if "directus_ffbb" in str(d)), None)
    if not directus_dir or not directus_dir.exists():
        return {}

    mapping: dict[str, list[str]] = {}

    for py_file in sorted(directus_dir.glob("*_fields.py")):
        if py_file.name == "query_fields_manager.py":
            continue

        # e.g. "rencontres_fields" -> "rencontres", "saison_fields" -> "saison"
        stem = py_file.stem  # e.g. "rencontres_fields"
        base = stem.rsplit("_fields", 1)[0]  # e.g. "rencontres"

        # Find the matching endpoint key (handle singular/plural)
        endpoint_key: str | None = None
        for candidate in (base, base + "s", base + "es"):
            if candidate in endpoint_map:
                endpoint_key = candidate
                break

        if not endpoint_key:
            continue

        # Dynamically import the module and find the Fields class
        module_name = f"ffbb_api_client_v2.directus_ffbb.models.{stem}"
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            logger.warning("Could not import %s: %s", module_name, e)
            continue

        # Find the QueryFieldsManager subclass in this module
        from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
            QueryFieldsManager,
        )

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, QueryFieldsManager)
                and attr is not QueryFieldsManager
            ):
                try:
                    fields = attr.get_fields()
                    mapping[endpoint_key] = fields
                    break
                except Exception as e:
                    logger.warning("get_fields() failed for %s: %s", attr_name, e)

    return mapping


# ---------------------------------------------------------------------------
# NAME_TYPE_HINTS — concordance table for always-None properties
# ---------------------------------------------------------------------------
NAME_TYPE_HINTS: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r"(^date_|_date$|^date$|_recorded_at$|_at$|^debut$|^fin$)"),
        "datetime | None",
        "from_datetime",
    ),
    (
        re.compile(r"(^focal_point_|^latitude$|^longitude$|_x$|_y$|^tarif)"),
        "float | None",
        "from_float",
    ),
    (
        re.compile(
            r"(^numero_journee$|^numero_equipe$|^numero_equ$|^numeroJournee$|^numeroEquipe$"
            r"|^nb_|_count$|^position$|^ordre$|^age_|^duration$"
            r"|^sort$|_prevu$|^capacite|^filesize$|^width$|^height$)"
        ),
        "int | None",
        "from_int",
    ),
    (
        re.compile(r"(^is_|^has_|^club_pro$|^saison_en_cours$)"),
        "bool | None",
        "from_bool",
    ),
    (
        re.compile(r"(^uploaded_by$|^modified_by$|_uuid$|^uuid$|^parent$)"),
        "UUID | None",
        "from_uuid",
    ),
]


def infer_from_name(python_name: str) -> tuple[str, str] | None:
    """Infer type from property name using concordance table."""
    for pattern, py_type, converter in NAME_TYPE_HINTS:
        if pattern.search(python_name):
            return py_type, converter
    return None


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
    dict_key_sets: list[frozenset[str]] = field(default_factory=list)
    list_element_types: dict[str, int] = field(default_factory=dict)
    list_element_key_sets: list[frozenset[str]] = field(default_factory=list)
    unique_str_values: set[str] = field(default_factory=set)
    all_values: set[Any] = field(default_factory=set)

    MAX_SAMPLES = 50
    MAX_KEY_SETS = 50
    MAX_UNIQUE_STR = 2000
    MAX_ALL_VALUES = 50_000

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
        if isinstance(value, str) and len(self.unique_str_values) < self.MAX_UNIQUE_STR:
            self.unique_str_values.add(value)

        # Track all hashable values for better inference
        if isinstance(value, (str, int, float, bool)):
            if len(self.all_values) < self.MAX_ALL_VALUES:
                self.all_values.add(value)

        if isinstance(value, dict) and len(self.dict_key_sets) < self.MAX_KEY_SETS:
            self.dict_key_sets.append(frozenset(value.keys()))

        if isinstance(value, list) and value:
            for elem in value[:5]:
                elem_type = type(elem).__name__
                self.list_element_types[elem_type] = (
                    self.list_element_types.get(elem_type, 0) + 1
                )
                if (
                    isinstance(elem, dict)
                    and len(self.list_element_key_sets) < self.MAX_KEY_SETS
                ):
                    self.list_element_key_sets.append(frozenset(elem.keys()))

    def merge(self, other: PathStats) -> None:
        """Merge another PathStats into this one."""
        self.total += other.total
        self.none_count += other.none_count
        self.non_none_count += other.non_none_count
        for tn, cnt in other.types.items():
            self.types[tn] = self.types.get(tn, 0) + cnt
        remaining = self.MAX_SAMPLES - len(self.samples)
        if remaining > 0:
            self.samples.extend(other.samples[:remaining])
        remaining_ks = self.MAX_KEY_SETS - len(self.dict_key_sets)
        if remaining_ks > 0:
            self.dict_key_sets.extend(other.dict_key_sets[:remaining_ks])
        for tn, cnt in other.list_element_types.items():
            self.list_element_types[tn] = self.list_element_types.get(tn, 0) + cnt
        remaining_lks = self.MAX_KEY_SETS - len(self.list_element_key_sets)
        if remaining_lks > 0:
            self.list_element_key_sets.extend(
                other.list_element_key_sets[:remaining_lks]
            )
        merged_str = self.unique_str_values | other.unique_str_values
        if len(merged_str) <= self.MAX_UNIQUE_STR:
            self.unique_str_values = merged_str
        else:
            self.unique_str_values = set(list(merged_str)[: self.MAX_UNIQUE_STR])

        # Merge all_values
        merged_all = self.all_values | other.all_values
        if len(merged_all) <= self.MAX_ALL_VALUES:
            self.all_values = merged_all
        else:
            self.all_values = set(list(merged_all)[: self.MAX_ALL_VALUES])

    def to_dict(self) -> dict[str, Any]:
        safe_samples = []
        for s in self.samples:
            if isinstance(s, str) and len(s) > 200:
                safe_samples.append(s[:200] + "...")
            elif isinstance(s, (dict, list)):
                txt = json.dumps(s, default=str, ensure_ascii=False)
                safe_samples.append(txt[:200] + "..." if len(txt) > 200 else txt)
            else:
                safe_samples.append(s)
        result: dict[str, Any] = {
            "total": self.total,
            "none_count": self.none_count,
            "non_none_count": self.non_none_count,
            "types": self.types,
            "samples": safe_samples,
        }
        if self.dict_key_sets:
            result["dict_key_sets"] = [sorted(ks) for ks in self.dict_key_sets[:3]]
        if self.list_element_types:
            result["list_element_types"] = self.list_element_types
        if self.list_element_key_sets:
            result["list_element_key_sets"] = [
                sorted(ks) for ks in self.list_element_key_sets[:3]
            ]
        if self.unique_str_values:
            result["unique_str_values"] = sorted(self.unique_str_values)
            result["unique_str_count"] = len(self.unique_str_values)
        if self.all_values:
            result["all_values_count"] = len(self.all_values)
        return result


# ---------------------------------------------------------------------------
# JsonFlattener
# ---------------------------------------------------------------------------
class JsonFlattener:
    """Flatten nested JSON, recording watched keys as whole values."""

    def __init__(self, record_whole_keys: set[str] | None = None) -> None:
        self.paths: dict[str, PathStats] = {}
        self.record_whole_keys = record_whole_keys or set()

    def flatten(self, obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                child_prefix = f"{prefix}.{key}" if prefix else key
                if key in self.record_whole_keys:
                    self._record(child_prefix, value)
                if isinstance(value, (dict, list)):
                    self.flatten(value, child_prefix)
                elif key not in self.record_whole_keys:
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
        suffix = f".{json_key}"
        return [p for p in self.paths if p.endswith(suffix) or p == json_key]

    def find_paths_with_prefix(self, prefix: str, json_key: str) -> list[str]:
        suffix = f".{json_key}"
        return [
            p
            for p in self.paths
            if p.startswith(prefix) and (p.endswith(suffix) or p == json_key)
        ]


# ---------------------------------------------------------------------------
# TypeInferrer
# ---------------------------------------------------------------------------
ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
DURATION_RE = re.compile(r"^\d+h\d{2}$")


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
    inference_method: str
    match_score: float | None
    evidence: dict[str, Any]
    structural_match: dict[str, Any] | None


class TypeInferrer:
    """Analyze collected values and infer Python types."""

    def __init__(self, registry: ModelSignatureRegistry) -> None:
        self.registry = registry

    def infer(self, stats: PathStats, prop: IncorrectProperty) -> TypeInference:
        inferred_type: str
        converter: str
        method: str
        match_score: float | None = None
        structural: dict[str, Any] | None = None

        if stats.non_none_count == 0:
            hint = infer_from_name(prop.python_name)
            if hint:
                inferred_type, converter_fn = hint
                converter = f'{converter_fn}(obj, "{prop.json_key}")'
                method = "name_hint"
            else:
                inferred_type = "str | None"
                converter = (
                    f'from_str(obj, "{prop.json_key}")  # default, always None in data'
                )
                method = "default"
        elif prop.category in ("dict_any", "list_dict_any"):
            inferred_type, converter, method, match_score, structural = (
                self._infer_dict(stats, prop)
            )
        elif prop.category == "list_any":
            inferred_type, converter, method, match_score, structural = (
                self._infer_list(stats, prop)
            )
        elif prop.category == "any_none":
            inferred_type, converter, method = self._infer_any(stats, prop)
        elif prop.category == "str_wrong_type":
            if stats.non_none_count > 0:
                inferred_type, converter = self._infer_from_observed(stats, prop)
                method = "data"
                # No fallback to name_hint: observed data primes over field name
            else:
                hint = infer_from_name(prop.python_name)
                if hint:
                    inferred_type, converter_fn = hint
                    converter = f'{converter_fn}(obj, "{prop.json_key}")'
                    method = "name_hint"
                else:
                    inferred_type = prop.current_type
                    converter = f'from_str(obj, "{prop.json_key}")'
                    method = "default"
        else:
            inferred_type, converter = self._infer_from_observed(stats, prop)
            method = "data"

        return TypeInference(
            file=f"src/ffbb_api_client_v2/{prop.file}",
            class_name=prop.class_name,
            python_name=prop.python_name,
            json_key=prop.json_key,
            current_type=prop.current_type,
            inferred_type=inferred_type,
            converter=converter,
            inference_method=method,
            match_score=match_score,
            evidence={
                "total": stats.total,
                "non_none": stats.non_none_count,
                "types": stats.types,
                "samples": stats.to_dict()["samples"],
            },
            structural_match=structural,
        )

    def _infer_dict(
        self, stats: PathStats, prop: IncorrectProperty
    ) -> tuple[str, str, str, float | None, dict[str, Any] | None]:
        all_keys: set[str] = set()
        for ks in stats.dict_key_sets:
            all_keys.update(ks)

        if all_keys:
            matches = self.registry.match(all_keys)
            if matches:
                best_class, best_path, score = matches[0]
                structural = {
                    "matched_model": best_class,
                    "model_path": best_path,
                    "observed_keys": sorted(all_keys),
                    "score": round(score, 3),
                }
                return (
                    f"{best_class} | None",
                    f'from_obj({best_class}.from_dict, obj, "{prop.json_key}")  # score={score:.2f}',
                    "structure",
                    score,
                    structural,
                )

        return (
            "dict[str, Any] | None",
            f'# dict with keys: {sorted(all_keys) if all_keys else "unknown"}',
            "data",
            None,
            {"observed_keys": sorted(all_keys)} if all_keys else None,
        )

    def _infer_list(
        self, stats: PathStats, prop: IncorrectProperty
    ) -> tuple[str, str, str, float | None, dict[str, Any] | None]:
        if stats.list_element_key_sets:
            all_keys: set[str] = set()
            for ks in stats.list_element_key_sets:
                all_keys.update(ks)

            if all_keys:
                matches = self.registry.match(all_keys)
                if matches:
                    best_class, best_path, score = matches[0]
                    structural = {
                        "matched_model": best_class,
                        "model_path": best_path,
                        "observed_keys": sorted(all_keys),
                        "score": round(score, 3),
                    }
                    return (
                        f"list[{best_class}]",
                        f'from_list({best_class}.from_dict, obj, "{prop.json_key}")  # score={score:.2f}',
                        "structure",
                        score,
                        structural,
                    )

        if stats.list_element_types:
            if set(stats.list_element_types.keys()) == {"str"}:
                return (
                    "list[str] | None",
                    f'from_list(str, obj, "{prop.json_key}")',
                    "data",
                    None,
                    None,
                )
            if set(stats.list_element_types.keys()) == {"int"}:
                return (
                    "list[int] | None",
                    f'from_list(int, obj, "{prop.json_key}")',
                    "data",
                    None,
                    None,
                )
            if set(stats.list_element_types.keys()) == {"float"}:
                return (
                    "list[float] | None",
                    f'from_list(float, obj, "{prop.json_key}")',
                    "data",
                    None,
                    None,
                )

        if "list" not in stats.types and stats.non_none_count > 0:
            return self._infer_from_observed_as_tuple(stats, prop)

        key_info = {}
        if stats.list_element_key_sets:
            merged_keys: set[str] = set()
            for ks in stats.list_element_key_sets:
                merged_keys.update(ks)
            key_info = {"element_keys": sorted(merged_keys)}
        return (
            "list[Any] | None",
            f'# list element type unknown for "{prop.json_key}"',
            "data",
            None,
            key_info if key_info else None,
        )

    def _infer_from_observed_as_tuple(
        self, stats: PathStats, prop: IncorrectProperty
    ) -> tuple[str, str, str, float | None, dict[str, Any] | None]:
        py_type, conv = self._infer_from_observed(stats, prop)
        return py_type, conv, "data", None, None

    def _infer_any(
        self, stats: PathStats, prop: IncorrectProperty
    ) -> tuple[str, str, str]:
        if "dict" in stats.types and stats.dict_key_sets:
            all_keys: set[str] = set()
            for ks in stats.dict_key_sets:
                all_keys.update(ks)
            matches = self.registry.match(all_keys)
            if matches:
                best_class, _, score = matches[0]
                return (
                    f"{best_class} | None",
                    f'from_obj({best_class}.from_dict, obj, "{prop.json_key}")  # score={score:.2f}',
                    "structure",
                )

        py_type, conv = self._infer_from_observed(stats, prop)
        return py_type, conv, "data"

    def _infer_from_observed(
        self, stats: PathStats, prop: IncorrectProperty
    ) -> tuple[str, str]:
        if stats.non_none_count == 0:
            hint = infer_from_name(prop.python_name)
            if hint:
                return hint[0], f'{hint[1]}(obj, "{prop.json_key}")'
            return "str | None", f'from_str(obj, "{prop.json_key}")  # default'

        type_counts = stats.types

        if len(type_counts) == 1:
            type_name = next(iter(type_counts))
            return self._infer_single(type_name, stats, prop.json_key)

        type_parts: list[str] = []
        converter_parts: list[str] = []
        for tn in sorted(type_counts.keys()):
            py_type, conv = self._infer_single(tn, stats, prop.json_key)
            py_type = py_type.replace(" | None", "")
            type_parts.append(py_type)
            converter_parts.append(conv.split("(")[0])

        union_type = " | ".join(type_parts) + " | None"
        converter = (
            f"from_union([{', '.join(converter_parts)}], obj, \"{prop.json_key}\")"
        )
        return union_type, converter

    @staticmethod
    def _infer_single(
        type_name: str, stats: PathStats, json_key: str
    ) -> tuple[str, str]:
        if type_name == "str":
            return TypeInferrer._refine_str(stats, json_key)
        if type_name == "int":
            return "int | None", f'from_int(obj, "{json_key}")'
        if type_name == "float":
            return "float | None", f'from_float(obj, "{json_key}")'
        if type_name == "bool":
            return "bool | None", f'from_bool(obj, "{json_key}")'
        if type_name == "dict":
            return "dict | None", f'from_obj(SubClass.from_dict, obj, "{json_key}")'
        if type_name == "list":
            return "list | None", f'from_list(item_fn, obj, "{json_key}")'
        return f"{type_name} | None", "# unknown type"

    @staticmethod
    def _refine_str(stats: PathStats, json_key: str) -> tuple[str, str]:
        # Use all_values (complete set) for better inference
        str_values = {v for v in stats.all_values if isinstance(v, str)}
        if not str_values:
            # Fallback to samples if all_values is empty
            str_values = {s for s in stats.samples if isinstance(s, str)}
        if not str_values:
            return "str | None", f'from_str(obj, "{json_key}")'

        if all(ISO_DATETIME_RE.match(s) for s in str_values):
            return "datetime | None", f'from_datetime(obj, "{json_key}")'

        if all(UUID_RE.match(s) for s in str_values):
            return "UUID | None", f'from_uuid(obj, "{json_key}")'

        if all(DURATION_RE.match(s) for s in str_values):
            return "timedelta | None", f'from_duration(obj, "{json_key}")'

        return "str | None", f'from_str(obj, "{json_key}")'


# ---------------------------------------------------------------------------
# CollectionResult — output of data collection operations
# ---------------------------------------------------------------------------
@dataclass
class CollectionResult:
    """Result of a single data collection operation."""

    name: str
    source: str  # "rest" or "meili"
    filepath: str
    prefix: str
    count: int


def _deduplicate_items(items_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate by ID, preferring items with more keys (deeper)."""
    by_id: dict[str, dict[str, Any]] = {}
    for item in items_list:
        item_id = str(item.get("id", id(item)))
        if item_id in by_id:
            if len(item) > len(by_id[item_id]):
                by_id[item_id] = item
        else:
            by_id[item_id] = item
    return list(by_id.values())


# ---------------------------------------------------------------------------
# WaveCollector — 3-wave data collection with FK chaining
# ---------------------------------------------------------------------------
class WaveCollector:
    """Collect data in 3 waves: lists, single-items, FK chains."""

    def __init__(
        self,
        http: RawHttpClient,
        endpoints_dir: Path,
        workers: int,
        endpoint_fields_map: dict[str, list[str]],
        endpoint_map: dict[str, str],
        meili_index_uids: list[str],
    ):
        self.http = http
        self.endpoints_dir = endpoints_dir
        self.workers = workers
        self.endpoint_fields_map = endpoint_fields_map
        self.endpoint_map = endpoint_map
        self.meili_index_uids = meili_index_uids
        self.collected_ids: dict[str, set[str]] = {}

    def collect_all(
        self,
        api_token: str,
        meili_token: str,
        *,
        skip_deep: bool = False,
    ) -> list[CollectionResult]:
        """Run all collection waves."""
        api_headers = {
            "user-agent": DEFAULT_USER_AGENT,
            "Authorization": f"Bearer {api_token}",
        }
        meili_headers = {
            "user-agent": DEFAULT_USER_AGENT,
            "Authorization": f"Bearer {meili_token}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }

        # Wave 1: lists + MeiliSearch
        logger.info(
            "Wave 1: Fetch all lists + MeiliSearch (ThreadPool, %d workers)...",
            self.workers,
        )
        t_w1 = time.monotonic()
        wave1 = self._wave1_fetch_lists(api_headers, meili_headers)
        self._extract_ids(wave1)
        logger.info(
            "Wave 1 done in %.1fs — %d endpoints, IDs: %s",
            time.monotonic() - t_w1,
            len(wave1),
            {k: len(v) for k, v in self.collected_ids.items()},
        )

        if skip_deep:
            logger.info("Wave 2+3 skipped (--no-chained)")
            return wave1

        # Wave 2: single-item fetches for all collected IDs
        logger.info(
            "Wave 2: Single-item fetches (ThreadPool, %d workers)...", self.workers
        )
        t_w2 = time.monotonic()
        wave2 = self._wave2_single_item_fetches(api_headers)
        all_results = wave1 + wave2
        logger.info(
            "Wave 2 done in %.1fs — %d endpoints fetched",
            time.monotonic() - t_w2,
            len(wave2),
        )

        # Wave 3+: FK chain resolution loop
        logger.info("Wave 3+: FK chain resolution...")
        t_w3 = time.monotonic()
        fk_to_resolve = self._extract_fk_ids(all_results)
        wave_num = 3
        while fk_to_resolve:
            logger.info(
                "  Wave %d: %s FKs to resolve",
                wave_num,
                {k: len(v) for k, v in fk_to_resolve.items()},
            )
            wave_n = self._wave_fk_resolve(api_headers, fk_to_resolve, wave_num)
            if not wave_n:
                logger.info("  Wave %d: no new items — stopping", wave_num)
                break
            all_results.extend(wave_n)
            fk_to_resolve = self._extract_fk_ids(wave_n)
            wave_num += 1

        logger.info(
            "Wave 3+ done in %.1fs — %d total FK waves",
            time.monotonic() - t_w3,
            wave_num - 3,
        )
        return all_results

    # -- Wave 1 -------------------------------------------------------------

    def _wave1_fetch_lists(
        self,
        api_headers: dict[str, str],
        meili_headers: dict[str, str],
    ) -> list[CollectionResult]:
        """Fetch all paginated REST endpoints + MeiliSearch + specials."""
        results: list[CollectionResult] = []
        special_endpoints = {"lives", "configuration", "saisons"}

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures: dict[Any, str] = {}

            # Paginated REST endpoints
            for name, path in sorted(self.endpoint_map.items()):
                if name in special_endpoints:
                    continue
                futures[
                    ex.submit(self._fetch_rest_paginated, path, name, api_headers)
                ] = name

            # MeiliSearch indexes
            for uid in self.meili_index_uids:
                futures[ex.submit(self._fetch_meili_index, uid, meili_headers)] = uid

            # Special endpoints
            for special_name in sorted(special_endpoints):
                ep = self.endpoint_map.get(special_name)
                if not ep:
                    continue
                futures[
                    ex.submit(self._fetch_rest_special, ep, special_name, api_headers)
                ] = special_name

            for future in as_completed(futures):
                ep_name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as exc:
                    logger.error("  [fail] %s: %s", ep_name, exc)

        return results

    def _fetch_rest_paginated(
        self, endpoint: str, name: str, headers: dict[str, str]
    ) -> CollectionResult | None:
        """Fetch + save a paginated REST endpoint."""
        fields = self.endpoint_fields_map.get(name)
        if fields:
            logger.info("  [%s] using %d defined fields", name, len(fields))
        else:
            logger.warning("  [%s] no fields definition found, using wildcard", name)
            fields = ["*.*"]

        t_start = time.monotonic()
        seen_ids: set[str] = set()
        items: list[dict[str, Any]] = []
        offset = 0
        page = 0

        while len(items) < REST_MAX_ITEMS:
            params: dict[str, Any] = {"limit": REST_PAGE_SIZE, "offset": offset}
            if fields:
                params["fields[]"] = fields
            url = RawHttpClient.build_url(API_FFBB_BASE_URL, endpoint, params)
            resp = self.http.get_json(url, headers)
            if not resp:
                break

            data = resp.get("data", resp) if isinstance(resp, dict) else resp
            if isinstance(data, list):
                if not data:
                    break
                for item in data:
                    item_id = str(item.get("id", ""))
                    if item_id and item_id in seen_ids:
                        continue
                    if item_id:
                        seen_ids.add(item_id)
                    items.append(item)
                if page == 0 or (page + 1) % 10 == 0 or len(data) < REST_PAGE_SIZE:
                    logger.info(
                        "  [%s] page %d — %d items (total: %d)",
                        name,
                        page + 1,
                        len(data),
                        len(items),
                    )
                if len(data) < REST_PAGE_SIZE:
                    break
            elif isinstance(data, dict):
                items.append(data)
                break
            else:
                break

            offset += REST_PAGE_SIZE
            page += 1

        t_fetch = time.monotonic() - t_start
        if not items:
            logger.info("  [%s] fetch: %.1fs — 0 items", name, t_fetch)
            return None

        filepath = self.endpoints_dir / f"rest_{name}.json"
        self._save_items(filepath, items)
        logger.info("  [%s] %d items — fetch=%.1fs", name, len(items), t_fetch)
        return CollectionResult(name, "rest", str(filepath), f"rest/{name}", len(items))

    def _fetch_meili_index(
        self, index_uid: str, headers: dict[str, str]
    ) -> CollectionResult | None:
        """Fetch + save a MeiliSearch index."""
        meili_url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"
        offset = 0
        all_hits: list[dict[str, Any]] = []
        t_start = time.monotonic()

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
            resp = self.http.post_json(meili_url, headers, payload)
            if not resp:
                break

            results = resp.get("results", [])
            if not results:
                break
            hits = results[0].get("hits", [])
            if not hits:
                break

            all_hits.extend(hits)
            estimated_total = results[0].get("estimatedTotalHits", 0)
            elapsed = time.monotonic() - t_start
            logger.info(
                "  [%s] %d hits (offset=%d, estimated=%d) — %.1fs",
                index_uid,
                len(all_hits),
                offset,
                estimated_total,
                elapsed,
            )

            if len(hits) < MEILI_BATCH_SIZE:
                break
            offset += MEILI_BATCH_SIZE

        t_fetch = time.monotonic() - t_start
        if not all_hits:
            logger.info("  [%s] fetch: %.1fs — 0 hits", index_uid, t_fetch)
            return None

        filepath = self.endpoints_dir / f"meili_{index_uid}.json"
        self._save_items(filepath, all_hits)
        logger.info("  [%s] %d hits — fetch=%.1fs", index_uid, len(all_hits), t_fetch)
        return CollectionResult(
            index_uid,
            "meili",
            str(filepath),
            f"meilisearch/{index_uid}/hits[]",
            len(all_hits),
        )

    def _fetch_rest_special(
        self, endpoint: str, name: str, headers: dict[str, str]
    ) -> CollectionResult | None:
        """Fetch + save a special endpoint (lives, configuration, saisons)."""
        fields = self.endpoint_fields_map.get(name, ["*.*"])
        t_start = time.monotonic()

        if name == "lives":
            url = f"{API_FFBB_BASE_URL}{endpoint}"
            resp = self.http.get_json(url, headers)
            if not resp:
                return None
            items = resp if isinstance(resp, list) else [resp]
        else:
            params: dict[str, Any] = {}
            if fields:
                params["fields[]"] = fields
            url = RawHttpClient.build_url(API_FFBB_BASE_URL, endpoint, params)
            resp = self.http.get_json(url, headers)
            if not resp:
                return None
            data = resp.get("data", resp) if isinstance(resp, dict) else resp
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = [data]
            else:
                items = []

        t_fetch = time.monotonic() - t_start
        if not items:
            logger.info("  [%s] fetch: %.1fs — 0 items", name, t_fetch)
            return None

        filepath = self.endpoints_dir / f"rest_{name}.json"
        self._save_items(filepath, items)
        logger.info("  [%s] %d items — fetch=%.1fs", name, len(items), t_fetch)
        return CollectionResult(name, "rest", str(filepath), f"rest/{name}", len(items))

    # -- Wave 2 -------------------------------------------------------------

    def _wave2_single_item_fetches(
        self, headers: dict[str, str]
    ) -> list[CollectionResult]:
        """Fetch individual items by ID for each REST endpoint."""
        results: list[CollectionResult] = []

        # Only REST endpoints with collected IDs
        endpoints_with_ids = [
            (name, ids)
            for name, ids in self.collected_ids.items()
            if name in self.endpoint_map and ids
        ]

        if not endpoints_with_ids:
            return results

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures: dict[Any, str] = {}
            for name, ids in endpoints_with_ids:
                futures[
                    ex.submit(
                        self._fetch_single_items,
                        name,
                        sorted(ids),
                        headers,
                    )
                ] = name

            for future in as_completed(futures):
                ep_name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as exc:
                    logger.error("  [wave2-fail] %s: %s", ep_name, exc)

        return results

    def _fetch_single_items(
        self,
        name: str,
        item_ids: list[str],
        headers: dict[str, str],
    ) -> CollectionResult | None:
        """Fetch individual items by ID for one endpoint."""
        endpoint = self.endpoint_map[name]
        fields = self.endpoint_fields_map.get(name, ["*.*"])
        items: list[dict[str, Any]] = []

        for item_id in item_ids:
            params: dict[str, Any] = {"fields[]": fields}
            url = RawHttpClient.build_url(
                API_FFBB_BASE_URL, f"{endpoint}/{item_id}", params
            )
            resp = self.http.get_json(url, headers)
            if resp:
                data = resp.get("data", resp) if isinstance(resp, dict) else resp
                if isinstance(data, dict):
                    items.append(data)

        if not items:
            return None

        filepath = self.endpoints_dir / f"rest_{name}_single.json"
        self._save_items(filepath, items)
        logger.info(
            "  [wave2] [%s] %d/%d items fetched", name, len(items), len(item_ids)
        )

        # Register newly discovered IDs
        for item in items:
            item_id = str(item.get("id", ""))
            if item_id:
                self.collected_ids.setdefault(name, set()).add(item_id)

        return CollectionResult(name, "rest", str(filepath), f"rest/{name}", len(items))

    # -- Wave 3+: FK chain resolution --------------------------------------

    def _extract_fk_ids(self, results: list[CollectionResult]) -> dict[str, set[str]]:
        """Scan results for FK IDs that need resolution."""
        fk_to_resolve: dict[str, set[str]] = {}

        for result in results:
            if result.source != "rest":
                continue

            try:
                with open(result.filepath, encoding="utf-8") as f:
                    items = json.load(f)
            except Exception as e:
                logger.warning(
                    "Failed to read/parse FK file %s: %s", result.filepath, e
                )
                continue

            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue
                for (src_ep, fk_key), target_ep in FK_CHAIN_MAP.items():
                    if result.name != src_ep:
                        continue
                    value = item.get(fk_key)
                    fk_id = self._extract_fk_id(value)
                    if fk_id is None:
                        continue
                    # Skip if already collected
                    if fk_id in self.collected_ids.get(target_ep, set()):
                        continue
                    # Skip if target endpoint not configured
                    if target_ep not in self.endpoint_map:
                        continue
                    fk_to_resolve.setdefault(target_ep, set()).add(fk_id)

        return fk_to_resolve

    @staticmethod
    def _extract_fk_id(value: Any) -> str | None:
        """Extract ID from a FK value. None if null or expanded object."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return str(int(value))
        if isinstance(value, str) and value.strip():
            return value.strip()
        # If it's a dict (expanded object), skip — data already present
        return None

    def _wave_fk_resolve(
        self,
        headers: dict[str, str],
        fk_to_resolve: dict[str, set[str]],
        wave_num: int,
    ) -> list[CollectionResult]:
        """Fetch FK-referenced items in parallel."""
        results: list[CollectionResult] = []

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures: dict[Any, str] = {}
            for target_ep, ids in fk_to_resolve.items():
                futures[
                    ex.submit(
                        self._fetch_fk_items,
                        target_ep,
                        sorted(ids),
                        headers,
                        wave_num,
                    )
                ] = target_ep

            for future in as_completed(futures):
                ep_name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as exc:
                    logger.error("  [fk-fail] %s: %s", ep_name, exc)

        return results

    def _fetch_fk_items(
        self,
        name: str,
        item_ids: list[str],
        headers: dict[str, str],
        wave_num: int,
    ) -> CollectionResult | None:
        """Fetch FK-referenced items for one target endpoint."""
        endpoint = self.endpoint_map[name]
        fields = self.endpoint_fields_map.get(name, ["*.*"])
        items: list[dict[str, Any]] = []

        for item_id in item_ids:
            params: dict[str, Any] = {"fields[]": fields}
            url = RawHttpClient.build_url(
                API_FFBB_BASE_URL, f"{endpoint}/{item_id}", params
            )
            resp = self.http.get_json(url, headers)
            if resp:
                data = resp.get("data", resp) if isinstance(resp, dict) else resp
                if isinstance(data, dict):
                    items.append(data)
                    fk_id = str(data.get("id", item_id))
                    self.collected_ids.setdefault(name, set()).add(fk_id)

        if not items:
            return None

        filepath = self.endpoints_dir / f"rest_{name}_fk_hop{wave_num}.json"
        self._save_items(filepath, items)
        logger.info(
            "  [wave%d] [%s] %d/%d FK items fetched",
            wave_num,
            name,
            len(items),
            len(item_ids),
        )
        return CollectionResult(name, "rest", str(filepath), f"rest/{name}", len(items))

    # -- ID extraction ------------------------------------------------------

    def _extract_ids(self, results: list[CollectionResult]) -> None:
        """Extract and register IDs from collection results."""
        for result in results:
            if result.source != "rest":
                continue
            try:
                with open(result.filepath, encoding="utf-8") as f:
                    items = json.load(f)
            except Exception as e:
                logger.warning(
                    "Failed to read/parse ID file %s: %s", result.filepath, e
                )
                continue
            if not isinstance(items, list):
                continue
            ids: set[str] = set()
            for item in items:
                if isinstance(item, dict) and "id" in item:
                    ids.add(str(item["id"]))
            if ids:
                self.collected_ids.setdefault(result.name, set()).update(ids)

    # -- Helpers ------------------------------------------------------------

    @staticmethod
    def _save_items(filepath: Path, items: list[dict[str, Any]]) -> None:
        """Save items to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, default=str, ensure_ascii=False)


# ---------------------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------------------
class ReportGenerator:

    @staticmethod
    def generate_raw_report(
        flattener: JsonFlattener,
        collection_stats: dict[str, Any],
    ) -> dict[str, Any]:
        report: dict[str, Any] = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                **collection_stats,
            },
            "paths": {},
        }
        for path, stats in sorted(flattener.paths.items()):
            report["paths"][path] = stats.to_dict()
        return report

    @staticmethod
    def generate_corrections(
        inferences: list[TypeInference],
        signatures: list[ModelSignature] | None = None,
    ) -> dict[str, Any]:
        resolved_data = 0
        resolved_structure = 0
        resolved_name = 0
        defaulted = 0

        # Build class_name -> signature lookup for line numbers
        sig_lookup: dict[str, ModelSignature] = {}
        if signatures:
            for sig in signatures:
                sig_lookup[sig.class_name] = sig

        corrections: list[dict[str, Any]] = []
        for inf in inferences:
            if inf.inference_method == "data":
                resolved_data += 1
            elif inf.inference_method == "structure":
                resolved_structure += 1
            elif inf.inference_method == "name_hint":
                resolved_name += 1
            elif inf.inference_method == "default":
                defaulted += 1

            entry: dict[str, Any] = {
                "file": inf.file,
                "class": inf.class_name,
                "property": inf.python_name,
                "json_key": inf.json_key,
                "current_type": inf.current_type,
                "inferred_type": inf.inferred_type,
                "converter": inf.converter,
                "inference_method": inf.inference_method,
                "evidence": inf.evidence,
            }
            if inf.match_score is not None:
                entry["match_score"] = round(inf.match_score, 3)
            if inf.structural_match:
                entry["structural_match"] = inf.structural_match

            # Add line numbers for actionable editing
            sig = sig_lookup.get(inf.class_name)
            if sig:
                ann_line = sig.annotation_lines.get(inf.python_name)
                if ann_line:
                    entry["annotation_line"] = ann_line
                entry["class_line"] = sig.class_line

            corrections.append(entry)

        new_model_candidates: list[dict[str, Any]] = []
        seen_key_sets: set[frozenset[str]] = set()
        for inf in inferences:
            if (
                inf.structural_match
                and "observed_keys" in inf.structural_match
                and inf.inference_method != "structure"
            ):
                keys_fs = frozenset(inf.structural_match["observed_keys"])
                if keys_fs not in seen_key_sets and len(keys_fs) >= 2:
                    seen_key_sets.add(keys_fs)
                    new_model_candidates.append(
                        {
                            "suggested_name": f"New{inf.python_name.title().replace('_', '')}Model",
                            "observed_keys": inf.structural_match["observed_keys"],
                            "source_properties": [
                                {
                                    "class": inf.class_name,
                                    "property": inf.python_name,
                                }
                            ],
                        }
                    )

        return {
            "summary": {
                "total_scanned": len(inferences),
                "resolved_from_data": resolved_data,
                "resolved_from_structure": resolved_structure,
                "resolved_from_name_hint": resolved_name,
                "defaulted_to_str": defaulted,
            },
            "corrections": corrections,
            "new_model_candidates": new_model_candidates,
        }

    @staticmethod
    def print_console_summary(corrections_report: dict[str, Any]) -> None:
        summary = corrections_report["summary"]
        print("\n" + "=" * 70)
        print("TYPE DISCOVERY RESULTS")
        print("=" * 70)
        print(f"Total properties analyzed: {summary['total_scanned']}")
        print(f"  Resolved from data:      {summary['resolved_from_data']}")
        print(f"  Resolved from structure:  {summary['resolved_from_structure']}")
        print(f"  Resolved from name hint:  {summary['resolved_from_name_hint']}")
        print(f"  Defaulted to str:         {summary['defaulted_to_str']}")
        print("-" * 70)

        for c in corrections_report["corrections"]:
            method = c["inference_method"]
            if method == "structure":
                marker = "**"
            elif method == "data":
                marker = ">>"
            elif method == "name_hint":
                marker = "~~"
            else:
                marker = "  "

            score_str = ""
            if "match_score" in c:
                score_str = f" [score={c['match_score']:.2f}]"

            line_str = ""
            if "annotation_line" in c:
                line_str = f" L{c['annotation_line']}"

            print(
                f"{marker} {c['class']}.{c['property']}{line_str}: "
                f"{c['current_type']} -> {c['inferred_type']}  "
                f"({method}, evidence: {c['evidence']['non_none']}/{c['evidence']['total']})"
                f"{score_str}"
            )
            if c["evidence"]["samples"] and c["inference_method"] != "default":
                sample_str = str(c["evidence"]["samples"][0])
                if len(sample_str) > 80:
                    sample_str = sample_str[:80] + "..."
                print(f"     sample: {sample_str}")

        candidates = corrections_report.get("new_model_candidates", [])
        if candidates:
            print()
            print("-" * 70)
            print(f"NEW MODEL CANDIDATES: {len(candidates)}")
            print("-" * 70)
            for cand in candidates:
                print(f"  {cand['suggested_name']}: keys={cand['observed_keys']}")
                for sp in cand["source_properties"]:
                    print(f"    from: {sp['class']}.{sp['property']}")

        print("=" * 70)


# ---------------------------------------------------------------------------
# Phase helper functions
# ---------------------------------------------------------------------------
def _phase0_init_parallel(
    http: RawHttpClient,
) -> tuple[
    str | None,
    str | None,
    ASTScanResult,
    dict[str, Any],
]:
    """Phase 0: Parallel token fetch + AST scan + config discovery."""
    logger.info("Phase 0: Token fetch + AST scan + config discovery (parallel)...")
    with ThreadPoolExecutor(max_workers=3) as ex:
        future_tokens = ex.submit(http.acquire_tokens)
        future_ast = ex.submit(scan_source_combined, MODEL_DIRS)
        future_configs = ex.submit(_discover_configs_and_mappings)
        api_token, meili_token = future_tokens.result()
        logger.info("  Tokens acquired")
        ast_result = future_ast.result()
        logger.info(
            "  AST scan: %d incorrect props, %d signatures",
            len(ast_result.incorrect_props),
            len(ast_result.signatures),
        )
        configs = future_configs.result()
        logger.info(
            "  Config: %d REST endpoints, %d MeiliSearch indexes, %d field definitions",
            len(configs["endpoint_map"]),
            len(configs["meili_index_map"]),
            len(configs["endpoint_fields_map"]),
        )
    return api_token, meili_token, ast_result, configs


def _phase1_wave_collect(
    collector: WaveCollector,
    api_token: str | None,
    meili_token: str | None,
    skip_deep: bool,
    t0: float,
) -> tuple[list[CollectionResult], float, dict[str, Any]]:
    """Phase 1: Wave-based collection (Wave 1 + 2 + 3+)."""
    fetch_results = collector.collect_all(api_token, meili_token, skip_deep=skip_deep)
    t_fetch_phase = time.monotonic() - t0
    collection_stats: dict[str, Any] = {"rest": {}, "meilisearch": {}}
    for result in fetch_results:
        bucket = "meilisearch" if result.source == "meili" else "rest"
        collection_stats[bucket][result.name] = (
            collection_stats[bucket].get(result.name, 0) + result.count
        )
    logger.info(
        "Phase 1 done in %.1fs — %d collection results",
        t_fetch_phase,
        len(fetch_results),
    )
    return fetch_results, t_fetch_phase, collection_stats


def _phase2_flatten(
    fetch_results: list[CollectionResult],
    endpoints_dir: Path,
    flattened_dir: Path,
    record_whole_keys: set[str],
    flatten_workers: int,
) -> tuple[list[tuple[str, dict[str, PathStats]]], float]:
    """Phase 2: Deduplicate wave results, then flatten (ProcessPool)."""
    t_flatten_start = time.monotonic()
    logger.info(
        "Phase 2: Flatten %d endpoint files (ProcessPool, %d workers)...",
        len(fetch_results),
        flatten_workers,
    )
    # Deduplicate items across waves for same endpoint before flattening
    items_by_key: dict[tuple[str, str], list[str]] = {}
    for r in fetch_results:
        key = (r.source, r.name)
        items_by_key.setdefault(key, []).append(r.filepath)

    deduped_results: list[CollectionResult] = []
    for (source, name), filepaths in items_by_key.items():
        if len(filepaths) == 1:
            for r in fetch_results:
                if r.filepath == filepaths[0]:
                    deduped_results.append(r)
                    break
        else:
            all_items: list[dict[str, Any]] = []
            for fp in filepaths:
                try:
                    with open(fp, encoding="utf-8") as f:
                        items = json.load(f)
                    if isinstance(items, list):
                        all_items.extend(items)
                except Exception as e:
                    logger.warning("Failed to read/parse merge file %s: %s", fp, e)
                    continue
            if all_items:
                deduped = _deduplicate_items(all_items)
                merged_filepath = endpoints_dir / f"{source}_{name}_merged.json"
                with open(merged_filepath, "w", encoding="utf-8") as f:
                    json.dump(deduped, f, indent=2, default=str, ensure_ascii=False)
                prefix = (
                    f"rest/{name}" if source == "rest" else f"meilisearch/{name}/hits[]"
                )
                deduped_results.append(
                    CollectionResult(
                        name, source, str(merged_filepath), prefix, len(deduped)
                    )
                )
                logger.info(
                    "  [dedup] %s/%s: %d items -> %d deduped",
                    source,
                    name,
                    len(all_items),
                    len(deduped),
                )

    per_endpoint_paths: list[tuple[str, dict[str, PathStats]]] = []
    flat_dir_str = str(flattened_dir)
    with ProcessPoolExecutor(max_workers=flatten_workers) as pool:
        future_to_name: dict[Any, str] = {}
        for r in deduped_results:
            fut = pool.submit(
                _flatten_from_file,
                r.filepath,
                r.prefix,
                record_whole_keys,
                flat_dir_str,
                r.source,
                r.name,
            )
            future_to_name[fut] = r.name
        for fut in as_completed(future_to_name):
            ep_name = future_to_name[fut]
            try:
                result_name, paths_dict = fut.result()
                if paths_dict:
                    per_endpoint_paths.append((result_name, paths_dict))
                else:
                    logger.warning("  [flatten-skip] %s: empty", ep_name)
            except Exception as exc:
                logger.error("  [flatten-fail] %s: %s", ep_name, exc)

    t_flatten = time.monotonic() - t_flatten_start
    logger.info(
        "Phase 2 done in %.1fs — %d endpoints flattened",
        t_flatten,
        len(per_endpoint_paths),
    )
    return per_endpoint_paths, t_flatten


def _phase3_merge(
    per_endpoint_paths: list[tuple[str, dict[str, PathStats]]],
    record_whole_keys: set[str],
) -> tuple[JsonFlattener, float]:
    """Phase 3: Merge flattened paths (sequential)."""
    t_merge_start = time.monotonic()
    logger.info("Phase 3: Merging %d endpoint path dicts...", len(per_endpoint_paths))
    combined_flattener = JsonFlattener(record_whole_keys=record_whole_keys)
    for _, paths_dict in per_endpoint_paths:
        for path, stats in paths_dict.items():
            if path not in combined_flattener.paths:
                combined_flattener.paths[path] = stats
            else:
                combined_flattener.paths[path].merge(stats)
    t_merge = time.monotonic() - t_merge_start
    logger.info(
        "  Merged — %d unique paths in %.2fs", len(combined_flattener.paths), t_merge
    )
    return combined_flattener, t_merge


def _phase4_infer_types(
    incorrect_props: list[IncorrectProperty],
    combined_flattener: JsonFlattener,
    sig_registry: ModelSignatureRegistry,
    meili_class_to_index: dict[str, str],
    rest_class_to_prefix: dict[str, str],
    workers: int,
) -> tuple[list[TypeInference], float]:
    """Phase 4: Type inference (parallel ThreadPool)."""
    t_infer_start = time.monotonic()
    logger.info(
        "Phase 4: Inferring types for %d properties (parallel)...", len(incorrect_props)
    )
    inferrer = TypeInferrer(sig_registry)

    def _infer_one(prop: IncorrectProperty) -> TypeInference:
        merged = PathStats()
        if prop.file.startswith("meilisearch_ffbb/"):
            index_uid = meili_class_to_index.get(prop.class_name)
            if index_uid:
                prefix = f"meilisearch/{index_uid}/hits[]"
                paths = combined_flattener.find_paths_with_prefix(prefix, prop.json_key)
            else:
                paths = combined_flattener.find_matching_paths(prop.json_key)
            for mp in paths:
                ps = combined_flattener.get_stats(mp)
                if ps:
                    merged.merge(ps)
        elif prop.file.startswith("directus_ffbb/"):
            rest_prefix = rest_class_to_prefix.get(prop.class_name)
            if rest_prefix:
                paths = combined_flattener.find_paths_with_prefix(
                    rest_prefix, prop.json_key
                )
            else:
                paths = combined_flattener.find_matching_paths(prop.json_key)
            for mp in paths:
                ps = combined_flattener.get_stats(mp)
                if ps:
                    merged.merge(ps)
        else:
            paths = combined_flattener.find_matching_paths(prop.json_key)
            for mp in paths:
                ps = combined_flattener.get_stats(mp)
                if ps:
                    merged.merge(ps)
        return inferrer.infer(merged, prop)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        inferences = list(ex.map(_infer_one, incorrect_props))

    t_infer = time.monotonic() - t_infer_start
    logger.info("  Inference done — %d properties in %.2fs", len(inferences), t_infer)
    return inferences, t_infer


def _phase5_reports(
    combined_flattener: JsonFlattener,
    collection_stats: dict[str, Any],
    inferences: list[TypeInference],
    ast_result: ASTScanResult,
) -> tuple[dict[str, Any], float]:
    """Phase 5: Generate reports."""
    t_reports_start = time.monotonic()
    logger.info("Phase 5: Generating reports...")
    raw_report = ReportGenerator.generate_raw_report(
        combined_flattener, collection_stats
    )
    corrections_report = ReportGenerator.generate_corrections(
        inferences, signatures=ast_result.signatures
    )
    raw_path = DATA_DIR / "type_discovery_raw.json"
    corrections_path = DATA_DIR / "type_discovery_corrections.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_report, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Raw report written to %s", raw_path)
    with open(corrections_path, "w", encoding="utf-8") as f:
        json.dump(corrections_report, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Corrections report written to %s", corrections_path)
    t_reports = time.monotonic() - t_reports_start
    logger.info("  Reports done in %.2fs", t_reports)
    return corrections_report, t_reports


def _phase6_enum_candidates(
    combined_flattener: JsonFlattener,
    ast_result: ASTScanResult,
    rest_class_to_prefix: dict[str, str],
    meili_class_to_index: dict[str, str],
) -> float:
    """Phase 6: Enum candidate detection."""
    t_enum_start = time.monotonic()
    logger.info("Phase 6: Detecting enum candidates...")
    prefix_to_sig: dict[str, ModelSignature] = {}
    for sig in ast_result.signatures:
        if sig.class_name in rest_class_to_prefix:
            prefix_to_sig[rest_class_to_prefix[sig.class_name]] = sig
        elif sig.class_name in meili_class_to_index:
            idx = meili_class_to_index[sig.class_name]
            prefix_to_sig[f"meilisearch/{idx}/hits[]"] = sig

    enum_candidates: list[dict[str, Any]] = []
    for path, stats in combined_flattener.paths.items():
        if stats.non_none_count < 10:
            continue
        if "str" not in stats.types:
            continue
        if not stats.unique_str_values:
            continue
        unique_values = sorted(stats.unique_str_values)
        n_values = len(unique_values)
        if n_values > 50 or (n_values == 1 and unique_values[0] == ""):
            continue
        if all(v == "" for v in unique_values):
            continue
        if n_values <= 10 and stats.non_none_count >= 100:
            confidence = "high"
        elif (n_values <= 10 and stats.non_none_count >= 10) or (
            n_values <= 30 and stats.non_none_count >= 100
        ):
            confidence = "medium"
        else:
            confidence = "low"
        json_key: str | None = None
        python_class: str | None = None
        python_attr: str | None = None
        module_path: str | None = None
        for pfx, sig in prefix_to_sig.items():
            pfx_dot = f"{pfx}."
            if path.startswith(pfx_dot):
                remainder = path[len(pfx_dot) :]
                if "." not in remainder and "[]" not in remainder:
                    json_key = remainder
                    python_class = sig.class_name
                    module_path = sig.module_path
                    python_attr = sig.json_to_python.get(
                        remainder, _camel_to_snake(remainder)
                    )
                    break
        base_name = python_attr or (json_key and _camel_to_snake(json_key))
        suggested_enum_name: str | None = None
        if base_name:
            parts = base_name.split("_")
            suggested_enum_name = "".join(p.capitalize() for p in parts)
        entry: dict[str, Any] = {
            "json_path": path,
            "unique_values": unique_values,
            "count": n_values,
            "total_observations": stats.total,
            "non_none_observations": stats.non_none_count,
            "confidence": confidence,
        }
        if python_class:
            entry["python_class"] = python_class
        if module_path:
            entry["module"] = module_path
        if json_key:
            entry["json_key"] = json_key
        if python_attr:
            entry["python_attr"] = python_attr
        if suggested_enum_name:
            entry["suggested_enum_name"] = suggested_enum_name
        enum_candidates.append(entry)

    enum_candidates.sort(key=lambda x: (x["count"], x["json_path"]))
    enum_path = DATA_DIR / "enum_candidates.json"
    with open(enum_path, "w", encoding="utf-8") as f:
        json.dump(enum_candidates, f, indent=2, ensure_ascii=False)
    logger.info(
        "Enum candidates: %d paths written to %s", len(enum_candidates), enum_path
    )
    t_enum = time.monotonic() - t_enum_start
    logger.info("  Enum detection done in %.2fs", t_enum)
    return t_enum


def _phase7_missing_fields(
    ast_result: ASTScanResult,
    combined_flattener: JsonFlattener,
    rest_class_to_prefix: dict[str, str],
    meili_class_to_index: dict[str, str],
) -> tuple[list[dict[str, Any]], float]:
    """Phase 7: Missing fields detection."""
    t_missing_start = time.monotonic()
    logger.info("Phase 7: Detecting missing fields in models...")
    missing_fields_report: list[dict[str, Any]] = []
    for sig in ast_result.signatures:
        prefix: str | None = None
        if sig.class_name in rest_class_to_prefix:
            prefix = rest_class_to_prefix[sig.class_name]
        elif sig.class_name in meili_class_to_index:
            index_uid = meili_class_to_index[sig.class_name]
            prefix = f"meilisearch/{index_uid}/hits[]"
        if not prefix:
            continue
        prefix_dot = f"{prefix}."
        observed_keys: set[str] = set()
        for path in combined_flattener.paths:
            if not path.startswith(prefix_dot):
                continue
            rest = path[len(prefix_dot) :]
            if "." not in rest and "[]" not in rest:
                observed_keys.add(rest)
        if not observed_keys:
            continue
        model_keys = set(sig.json_keys)
        missing_in_model = sorted(observed_keys - model_keys)
        missing_in_api = sorted(model_keys - observed_keys)
        if missing_in_model or missing_in_api:
            entry: dict[str, Any] = {
                "class": sig.class_name,
                "module": sig.module_path,
                "prefix": prefix,
            }
            if missing_in_model:
                missing_details = []
                for key in missing_in_model:
                    full_path = f"{prefix}.{key}"
                    stats = combined_flattener.get_stats(full_path)
                    python_attr = _camel_to_snake(key)
                    detail: dict[str, Any] = {"key": key, "python_attr": python_attr}
                    if stats:
                        detail["types"] = stats.types
                        detail["total"] = stats.total
                        detail["none_count"] = stats.none_count
                        detail["nullable"] = stats.none_count > 0
                        has_nested = any(
                            p.startswith(f"{full_path}.")
                            for p in combined_flattener.paths
                        )
                        detail["is_relation"] = (
                            "dict" in stats.types
                            or has_nested
                            or (
                                "list" in stats.types
                                and bool(stats.list_element_key_sets)
                            )
                        )
                        suggested_type, suggested_converter = _json_type_to_python(
                            stats.types,
                            stats.none_count,
                            stats.total,
                            key,
                            samples=stats.samples,
                        )
                        detail["suggested_type"] = suggested_type
                        detail["suggested_converter"] = suggested_converter
                        if stats.samples:
                            sample = stats.samples[0]
                            sample_str = str(sample)
                            if len(sample_str) > 100:
                                sample_str = sample_str[:100] + "..."
                            detail["sample"] = sample_str
                    else:
                        detail["nullable"] = True
                        detail["is_relation"] = False
                        detail["suggested_type"] = "str | None"
                        detail["suggested_converter"] = f'from_str(obj, "{key}")'
                    detail["suggested_annotation"] = (
                        f"{python_attr}: {detail['suggested_type']} = None"
                        if "None" in detail["suggested_type"]
                        else f"{python_attr}: {detail['suggested_type']}"
                    )
                    missing_details.append(detail)
                entry["missing_in_model"] = missing_details
            if missing_in_api:
                missing_api_details = []
                for key in missing_in_api:
                    python_attr = sig.json_to_python.get(key, _camel_to_snake(key))
                    line = sig.annotation_lines.get(python_attr)
                    api_detail: dict[str, Any] = {
                        "key": key,
                        "python_attr": python_attr,
                    }
                    if line:
                        api_detail["line"] = line
                    api_detail["action"] = "verify_needed"
                    missing_api_details.append(api_detail)
                entry["missing_in_api"] = missing_api_details
            missing_fields_report.append(entry)

    missing_fields_report.sort(key=lambda x: x["class"])
    missing_path = DATA_DIR / "missing_fields.json"
    with open(missing_path, "w", encoding="utf-8") as f:
        json.dump(missing_fields_report, f, indent=2, ensure_ascii=False)
    total_missing_in_model = sum(
        len(e.get("missing_in_model", [])) for e in missing_fields_report
    )
    total_missing_in_api = sum(
        len(e.get("missing_in_api", [])) for e in missing_fields_report
    )
    logger.info(
        "  Missing fields: %d classes affected, %d fields missing in models, "
        "%d model fields absent from API",
        len(missing_fields_report),
        total_missing_in_model,
        total_missing_in_api,
    )
    logger.info("  Report written to %s", missing_path)
    t_missing = time.monotonic() - t_missing_start
    logger.info("  Missing fields detection done in %.2fs", t_missing)
    return missing_fields_report, t_missing


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Discover types for model properties")
    parser.add_argument(
        "--clear-cache", action="store_true", help="Clear HTTP cache before running"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=REST_PARALLEL_WORKERS,
        help=f"Number of parallel workers (default: {REST_PARALLEL_WORKERS})",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable DEBUG logging (shows cache HIT/MISS per request)",
    )
    parser.add_argument(
        "--no-chained",
        action="store_true",
        help="Skip Wave 2+3 (single-item + FK chain fetches for deeper discovery)",
    )
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=== Type Discovery Script ===")
    logger.info("  workers=%d, cache_ttl=%ds", args.workers, CACHE_TTL)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    http = RawHttpClient(DATA_DIR)

    # Handle --clear-cache
    if args.clear_cache:
        cache_db = DATA_DIR / "discover_types_cache.sqlite"
        if cache_db.exists():
            cache_db.unlink()
            logger.info("Cache cleared: %s", cache_db)
        else:
            logger.info("No cache to clear")

    # Phase 0 — tokens + AST + config (parallel)
    api_token, meili_token, ast_result, configs = _phase0_init_parallel(http)
    incorrect_props = ast_result.incorrect_props
    sig_registry = ModelSignatureRegistry(ast_result.signatures)
    endpoint_map = configs["endpoint_map"]
    meili_index_map = configs["meili_index_map"]
    meili_class_to_index = configs["meili_class_to_index"]
    rest_class_to_prefix = configs["rest_class_to_prefix"]
    endpoint_fields_map: dict[str, list[str]] = configs["endpoint_fields_map"]

    for prop in incorrect_props:
        logger.info(
            "    [%s] %s.%s (%s) -> json_key=%s",
            prop.category,
            prop.class_name,
            prop.python_name,
            prop.current_type,
            prop.json_key,
        )

    record_whole_keys: set[str] = {
        prop.json_key
        for prop in incorrect_props
        if prop.category in ("dict_any", "list_any", "list_dict_any", "any_none")
    }

    # Phase 1 — Wave-based collection
    endpoints_dir = DATA_DIR / "endpoints"
    endpoints_dir.mkdir(parents=True, exist_ok=True)
    cache_db = DATA_DIR / "discover_types_cache.sqlite"
    if cache_db.exists():
        cache_size_mb = cache_db.stat().st_size / (1024 * 1024)
        logger.info("  Cache exists: %s (%.1f MB)", cache_db, cache_size_mb)
    else:
        logger.info("  Cache empty — first run will fetch from network")

    t0 = time.monotonic()
    flattened_dir = DATA_DIR / "flattened"
    flattened_dir.mkdir(parents=True, exist_ok=True)

    collector = WaveCollector(
        http=http,
        endpoints_dir=endpoints_dir,
        workers=args.workers,
        endpoint_fields_map=endpoint_fields_map,
        endpoint_map=endpoint_map,
        meili_index_uids=list(meili_index_map.values()),
    )
    fetch_results, t_fetch_phase, collection_stats = _phase1_wave_collect(
        collector, api_token, meili_token, args.no_chained, t0
    )

    # Phase 2 — Flatten (ProcessPool)
    cpu_count = os.cpu_count() or 4
    flatten_workers = min(cpu_count, len(fetch_results)) if fetch_results else 1
    per_endpoint_paths, t_flatten = _phase2_flatten(
        fetch_results, endpoints_dir, flattened_dir, record_whole_keys, flatten_workers
    )

    # Phase 3 — Merge
    combined_flattener, t_merge = _phase3_merge(per_endpoint_paths, record_whole_keys)

    # Phase 4 — Type inference
    inferences, t_infer = _phase4_infer_types(
        incorrect_props,
        combined_flattener,
        sig_registry,
        meili_class_to_index,
        rest_class_to_prefix,
        args.workers,
    )

    # Phase 5 — Reports
    corrections_report, t_reports = _phase5_reports(
        combined_flattener, collection_stats, inferences, ast_result
    )

    # Phase 6 — Enum candidates
    t_enum = _phase6_enum_candidates(
        combined_flattener, ast_result, rest_class_to_prefix, meili_class_to_index
    )

    # Phase 7 — Missing fields
    missing_fields_report, t_missing = _phase7_missing_fields(
        ast_result, combined_flattener, rest_class_to_prefix, meili_class_to_index
    )

    # Print missing fields console summary
    if missing_fields_report:
        print()
        print("=" * 70)
        print("MISSING FIELDS REPORT")
        print("=" * 70)
        for entry in missing_fields_report:
            missing_in_model = entry.get("missing_in_model", [])
            missing_in_api = entry.get("missing_in_api", [])
            if missing_in_model:
                print(f"\n{entry['class']} ({entry['module']}):")
                print(f"  Fields in API but NOT in model ({len(missing_in_model)}):")
                for detail in missing_in_model:
                    types_str = ", ".join(
                        f"{t}:{c}" for t, c in detail.get("types", {}).items()
                    )
                    sample = detail.get("sample", "")
                    none_pct = ""
                    if detail.get("total", 0) > 0:
                        pct = detail.get("none_count", 0) / detail["total"] * 100
                        none_pct = f" null:{pct:.0f}%"
                    rel_flag = " [REL]" if detail.get("is_relation") else ""
                    print(
                        f"    + {detail['key']} -> {detail.get('python_attr', '?')}: "
                        f"{detail.get('suggested_type', '?')}{rel_flag}"
                        f"  ({types_str}{none_pct})"
                    )
                    if sample:
                        print(f"      sample: {sample[:60]}")
                    print(
                        f"      annotation: {detail.get('suggested_annotation', '?')}"
                    )
                    print(f"      converter:  {detail.get('suggested_converter', '?')}")
            if missing_in_api:
                if not missing_in_model:
                    print(f"\n{entry['class']} ({entry['module']}):")
                print(f"  Fields in model but NOT in API ({len(missing_in_api)}):")
                for api_detail in missing_in_api:
                    if isinstance(api_detail, dict):
                        line_str = (
                            f" L{api_detail['line']}" if api_detail.get("line") else ""
                        )
                        print(
                            f"    - {api_detail['key']} ({api_detail['python_attr']}{line_str})"
                            f"  [{api_detail.get('action', '?')}]"
                        )
                    else:
                        print(f"    - {api_detail}")
        print("=" * 70)

    # Console summary
    ReportGenerator.print_console_summary(corrections_report)

    total_time = time.monotonic() - t0
    logger.info("=== Timing Summary ===")
    logger.info("  Phase 0 (tokens+AST+config):   included in Phase 1")
    logger.info("  Phase 1 (wave collection):     %.1fs", t_fetch_phase)
    logger.info("  Phase 2 (flatten, Process):    %.1fs", t_flatten)
    logger.info("  Phase 3 (merge paths):         %.2fs", t_merge)
    logger.info("  Phase 4 (type inference):      %.2fs", t_infer)
    logger.info("  Phase 5 (reports):             %.2fs", t_reports)
    logger.info("  Phase 6 (enum detection):      %.2fs", t_enum)
    logger.info("  Phase 7 (missing fields):      %.2fs", t_missing)
    logger.info("  TOTAL:                         %.1fs", total_time)


def _flatten_from_file(
    filepath: str,
    prefix: str,
    record_whole_keys: set[str],
    flattened_dir: str,
    file_tag: str,
    name: str,
) -> tuple[str, dict[str, PathStats] | None]:
    """Load raw JSON from file, flatten, save flattened output.

    Designed to run in a subprocess via ProcessPoolExecutor.
    All arguments and return values are picklable.

    Returns:
        (name, paths_dict) where paths_dict maps path -> PathStats,
        or (name, None) if file is empty.
    """
    t_load_start = time.monotonic()
    with open(filepath, encoding="utf-8") as f:
        items: list[dict[str, Any]] = json.load(f)
    t_load = time.monotonic() - t_load_start

    if not items:
        return name, None

    t_flat_start = time.monotonic()
    flattener = JsonFlattener(record_whole_keys=record_whole_keys)
    for item in items:
        flattener.flatten(item, prefix)
    t_flat = time.monotonic() - t_flat_start

    t_save_start = time.monotonic()
    flat_filepath = Path(flattened_dir) / f"{file_tag}_{name}_flat.json"
    report: dict[str, Any] = {}
    for path, stats in sorted(flattener.paths.items()):
        report[path] = stats.to_dict()
    with open(flat_filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)
    t_save = time.monotonic() - t_save_start

    logger.info(
        "  [flatten] [%s] %d items, %d paths — load=%.1fs flat=%.1fs save=%.1fs",
        name,
        len(items),
        len(flattener.paths),
        t_load,
        t_flat,
        t_save,
    )
    return name, flattener.paths


def _discover_configs_and_mappings() -> dict[str, Any]:
    """Discover all config constants and class-to-source mappings.

    Factored into a function so it can run in parallel with token fetch + AST scan.
    """
    endpoint_map = _discover_config_constants(_directus_config, "ENDPOINT_")
    meili_index_map = _discover_config_constants(_meili_config, "MEILISEARCH_INDEX_")
    meili_class_to_index = _build_meili_class_to_index(MODEL_DIRS, meili_index_map)
    rest_class_to_prefix = _build_rest_class_to_prefix(MODEL_DIRS, endpoint_map)
    endpoint_fields_map = _build_endpoint_fields_map(MODEL_DIRS, endpoint_map)
    return {
        "endpoint_map": endpoint_map,
        "meili_index_map": meili_index_map,
        "meili_class_to_index": meili_class_to_index,
        "rest_class_to_prefix": rest_class_to_prefix,
        "endpoint_fields_map": endpoint_fields_map,
    }


if __name__ == "__main__":
    main()
