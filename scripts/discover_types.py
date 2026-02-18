#!/usr/bin/env python3
"""
Discover real types for incorrectly typed model properties.

This script:
  1. Dynamically scans source code (AST) to find properties typed as
     dict[str, Any], list[Any], Any | None, or using raw obj.get().
  2. Builds model signatures from all from_dict methods for structural matching.
  3. Makes real API calls (MeiliSearch + REST) to collect raw JSON data.
  4. Infers correct Python types using observed data, structural matching,
     and a name-based concordance table.
  5. Generates a comprehensive corrections report.

Usage:
    python scripts/discover_types.py
"""

from __future__ import annotations

import ast
import json
import logging
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so we can import the client library
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

# Import config modules for dynamic constant discovery
import ffbb_api_client_v2.directus_ffbb.config as _directus_config  # noqa: E402
import ffbb_api_client_v2.meilisearch_ffbb.config as _meili_config  # noqa: E402
from ffbb_api_client_v2._http.client import (  # noqa: E402
    http_get_json,
    http_post_json,
    url_with_params,
)
from ffbb_api_client_v2.config import (  # noqa: E402
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
)
from ffbb_api_client_v2.directus.client import DEFAULT_USER_AGENT  # noqa: E402
from ffbb_api_client_v2.directus_ffbb.config import (  # noqa: E402
    API_FFBB_BASE_URL,
)
from ffbb_api_client_v2.facade.token_manager import TokenManager  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MEILI_BATCH_SIZE = 5000  # MeiliSearch supports large batches
MEILI_MAX_HITS = sys.maxsize  # no limit — collect ALL hits from every index
REST_PAGE_SIZE = 1000  # 10x fewer HTTP requests
REST_MAX_ITEMS = sys.maxsize  # no limit — collect ALL items from every endpoint
REST_DELAY = 0.0  # no throttle — maximize speed
REST_RETRY_MAX = 3  # retry 502/504 errors
REST_RETRY_BACKOFF = 5.0  # seconds initial backoff for retries
REST_PARALLEL_WORKERS = 8  # max parallel network I/O
DATA_DIR = PROJECT_ROOT / "data"

# Model source directories to scan
MODEL_DIRS = [
    SRC_ROOT / "ffbb_api_client_v2" / "models",
    SRC_ROOT / "ffbb_api_client_v2" / "meilisearch_ffbb" / "models",
    SRC_ROOT / "ffbb_api_client_v2" / "directus_ffbb" / "models",
]


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
    # from_str(obj, "key"), from_int(obj, "key"), from_bool(obj, "key"), etc.
    if isinstance(call.func, ast.Name) and call.func.id.startswith("from_"):
        fn_name = call.func.id
        # from_obj(fn, obj, "key"), from_list(fn, obj, "key"), from_enum(cls, obj, "key")
        if fn_name in ("from_obj", "from_list", "from_enum"):
            if (
                len(call.args) >= 3
                and isinstance(call.args[2], ast.Constant)
                and isinstance(call.args[2].value, str)
            ):
                return call.args[2].value
        # from_str(obj, "key"), from_int(obj, "key"), etc.
        else:
            if (
                len(call.args) >= 2
                and isinstance(call.args[1], ast.Constant)
                and isinstance(call.args[1].value, str)
            ):
                return call.args[1].value

    # obj.get("key") or data.get("key")
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

    # list[dict[str, Any]] (with or without | None)
    if re.search(r"list\[dict\[str,\s*Any\]\]", s):
        return "list_dict_any"

    # dict[str, Any] (with or without | None)
    if re.search(r"dict\[str,\s*Any\]", s):
        return "dict_any"

    # list[Any] (with or without | None) — but not list[list[Any]]
    if re.search(r"(?<!\[)list\[Any\]", s):
        return "list_any"

    # Bare "Any | None" or "Any"
    if re.match(r"^Any(\s*\|\s*None)?$", s):
        return "any_none"

    # str | None on date-like fields (should be datetime | None)
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

    # Find from_dict method
    from_dict_method: ast.FunctionDef | None = None
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef) and item.name == "from_dict":
            from_dict_method = item
            break

    if not from_dict_method:
        return mapping

    # Pass 1: collect variable -> json_key from assignments
    var_to_key: dict[str, str] = {}
    for node in ast.walk(from_dict_method):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                key = _extract_json_key_from_expr(node.value)
                if key:
                    var_to_key[var_name] = key
                    mapping[var_name] = key

    # Pass 2: collect from keyword arguments in constructor calls
    for node in ast.walk(from_dict_method):
        if not isinstance(node, ast.keyword) or not node.arg:
            continue
        # Direct call in value: cls(field=data.get("key"))
        key = _extract_json_key_from_expr(node.value)
        if key:
            mapping[node.arg] = key
        # Variable reference: cls(field=var) where var was assigned earlier
        elif isinstance(node.value, ast.Name) and node.value.id in var_to_key:
            mapping[node.arg] = var_to_key[node.value.id]
        # IfExp: cls(field=var if cond else default)
        elif isinstance(node.value, ast.IfExp):
            if (
                isinstance(node.value.body, ast.Name)
                and node.value.body.id in var_to_key
            ):
                mapping[node.arg] = var_to_key[node.value.body.id]

    return mapping


# ---------------------------------------------------------------------------
# SourceCodeScanner — dynamic discovery of incorrectly typed properties
# ---------------------------------------------------------------------------
class SourceCodeScanner:
    """Scan model source files with AST to find incorrectly typed properties."""

    @staticmethod
    def scan_all(model_dirs: list[Path]) -> list[IncorrectProperty]:
        """Scan all model directories and return incorrectly typed properties."""
        results: list[IncorrectProperty] = []
        for model_dir in model_dirs:
            if not model_dir.exists():
                continue
            for py_file in sorted(model_dir.glob("*.py")):
                if py_file.name.startswith("__"):
                    continue
                try:
                    results.extend(SourceCodeScanner._scan_file(py_file))
                except SyntaxError as e:
                    logger.warning("Syntax error in %s: %s", py_file, e)
        return results

    @staticmethod
    def _scan_file(file_path: Path) -> list[IncorrectProperty]:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        results: list[IncorrectProperty] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            if not _is_dataclass(node):
                continue

            # Extract json_key mapping from from_dict
            json_key_map = _extract_json_keys_from_method(node)

            # Check each field annotation
            for field_name, annotation_node in SourceCodeScanner._get_field_annotations(
                node
            ):
                annotation_str = ast.unparse(annotation_node)
                category = _classify_annotation(annotation_str, field_name)
                if category:
                    json_key = json_key_map.get(field_name, field_name)
                    rel_path = str(
                        file_path.relative_to(SRC_ROOT / "ffbb_api_client_v2")
                    )
                    results.append(
                        IncorrectProperty(
                            file=rel_path,
                            class_name=node.name,
                            python_name=field_name,
                            json_key=json_key,
                            current_type=annotation_str,
                            category=category,
                        )
                    )

        return results

    @staticmethod
    def _get_field_annotations(
        class_node: ast.ClassDef,
    ) -> list[tuple[str, ast.expr]]:
        """Get (field_name, annotation_node) for class-level annotated assignments."""
        results: list[tuple[str, ast.expr]] = []
        for node in class_node.body:
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                results.append((node.target.id, node.annotation))
        return results


# ---------------------------------------------------------------------------
# ModelSignature & ModelSignatureRegistry — for structural matching
# ---------------------------------------------------------------------------
@dataclass
class ModelSignature:
    class_name: str
    module_path: str  # relative to src/ffbb_api_client_v2/
    json_keys: frozenset[str]


class ModelSignatureRegistry:
    """Build model JSON key signatures dynamically from source code."""

    def __init__(self, signatures: list[ModelSignature]) -> None:
        self.signatures = signatures

    @classmethod
    def build_from_source(cls, model_dirs: list[Path]) -> ModelSignatureRegistry:
        """Parse all model files and extract from_dict JSON key signatures."""
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
                except SyntaxError:
                    continue

                for node in ast.walk(tree):
                    if not isinstance(node, ast.ClassDef):
                        continue
                    if not _is_dataclass(node):
                        continue

                    json_keys = _extract_json_keys_from_method(node)
                    if len(json_keys) < 2:
                        continue  # skip trivially small models

                    rel_path = str(py_file.relative_to(SRC_ROOT / "ffbb_api_client_v2"))
                    sigs.append(
                        ModelSignature(
                            class_name=node.name,
                            module_path=rel_path,
                            json_keys=frozenset(json_keys.values()),
                        )
                    )

        logger.info(
            "ModelSignatureRegistry: built %d signatures from source", len(sigs)
        )
        return cls(sigs)

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
    """Discover string constants from a module by prefix.

    Returns {base_name_lower: value}.
    E.g., prefix="ENDPOINT_" on directus_config gives:
        {"organismes": "items/ffbbserver_organismes", ...}
    """
    prefix_len = len(prefix)
    return {
        attr[prefix_len:].lower(): getattr(module, attr)
        for attr in dir(module)
        if attr.startswith(prefix) and isinstance(getattr(module, attr), str)
    }


def _build_meili_class_to_index(
    model_dirs: list[Path], meili_constants: dict[str, str]
) -> dict[str, str]:
    """Dynamically map Hit class names to MeiliSearch index UIDs.

    Scans *_hit.py files and matches the base name to MEILISEARCH_INDEX_*
    config constants.
    """
    meili_dir = next((d for d in model_dirs if "meilisearch_ffbb" in str(d)), None)
    if not meili_dir or not meili_dir.exists():
        return {}

    mapping: dict[str, str] = {}
    for py_file in sorted(meili_dir.glob("*_hit.py")):
        base = py_file.stem.replace("_hit", "")  # e.g. "engagements"
        index_uid = meili_constants.get(base)
        if not index_uid:
            logger.warning("No MEILISEARCH_INDEX_* constant for base=%s", base)
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
    """Dynamically map Response class names to REST flattener prefixes.

    Scans get_*_response.py files, derives the base name from the file name,
    and matches it against discovered endpoint keys to get the correct prefix
    (avoiding naive pluralization issues like 'configuration' → 'configurations').
    """
    directus_dir = next((d for d in model_dirs if "directus_ffbb" in str(d)), None)
    if not directus_dir or not directus_dir.exists():
        return {}

    mapping: dict[str, str] = {}
    for py_file in sorted(directus_dir.glob("get_*_response.py")):
        stem = py_file.stem  # e.g. "get_organisme_response"
        base = stem[4:].rsplit("_response", 1)[0]  # e.g. "organisme"

        # Match to an endpoint key: first exact, then with 's' suffix
        if base in endpoint_map:
            endpoint_base = base
        elif base + "s" in endpoint_map:
            endpoint_base = base + "s"
        else:
            endpoint_base = base  # fallback

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


# ---------------------------------------------------------------------------
# NAME_TYPE_HINTS — concordance table for always-None properties
# ---------------------------------------------------------------------------
# Order matters: first match wins. Default is str | None.
NAME_TYPE_HINTS: list[tuple[re.Pattern[str], str, str]] = [
    # Dates and timestamps
    (
        re.compile(r"(^date_|_date$|^date$|_recorded_at$|_at$|^debut$|^fin$)"),
        "datetime | None",
        "from_datetime",
    ),
    # Floating point
    (
        re.compile(r"(^focal_point_|^latitude$|^longitude$|_x$|_y$|^tarif|_hours$)"),
        "float | None",
        "from_float",
    ),
    # Integers
    (
        re.compile(
            r"(^numero|^nb_|_count$|^position$|^ordre$|^age_|^duration$"
            r"|^sort$|_prevu$|^capacite|^filesize$|^width$|^height$)"
        ),
        "int | None",
        "from_int",
    ),
    # Booleans
    (
        re.compile(r"(^is_|^has_|^club_pro$|^saison_en_cours$)"),
        "bool | None",
        "from_bool",
    ),
    # UUIDs
    (
        re.compile(r"(^uploaded_by$|^modified_by$|_uuid$|^uuid$|^parent$)"),
        "UUID | None",
        "from_uuid",
    ),
]


def infer_from_name(python_name: str) -> tuple[str, str] | None:
    """Infer type from property name using concordance table. Returns None if no match."""
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
    # Enhanced: capture dict key sets for structural matching
    dict_key_sets: list[frozenset[str]] = field(default_factory=list)
    # Enhanced: capture list element info
    list_element_types: dict[str, int] = field(default_factory=dict)
    list_element_key_sets: list[frozenset[str]] = field(default_factory=list)

    MAX_SAMPLES = 10
    MAX_KEY_SETS = 20

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

        # Capture dict key sets for structural matching
        if isinstance(value, dict) and len(self.dict_key_sets) < self.MAX_KEY_SETS:
            self.dict_key_sets.append(frozenset(value.keys()))

        # Capture list element info
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
        """Merge another PathStats into this one (for combining per-endpoint flatteners)."""
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
        return result


# ---------------------------------------------------------------------------
# JsonFlattener (enhanced with record_whole_keys)
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
                # Record whole value for watched keys (for structural matching)
                if key in self.record_whole_keys:
                    self._record(child_prefix, value)
                # Continue flattening for detailed leaf analysis
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
        """Find all flattened paths ending with the given json_key."""
        suffix = f".{json_key}"
        return [p for p in self.paths if p.endswith(suffix) or p == json_key]

    def find_paths_with_prefix(self, prefix: str, json_key: str) -> list[str]:
        """Find paths starting with prefix and ending with json_key."""
        suffix = f".{json_key}"
        return [
            p
            for p in self.paths
            if p.startswith(prefix) and (p.endswith(suffix) or p == json_key)
        ]


# ---------------------------------------------------------------------------
# TypeInferrer (enhanced with structural matching + name hints)
# ---------------------------------------------------------------------------
ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
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
    inference_method: str  # data, structure, name_hint, default
    match_score: float | None
    evidence: dict[str, Any]
    structural_match: dict[str, Any] | None


class TypeInferrer:
    """Analyze collected values and infer Python types."""

    def __init__(self, registry: ModelSignatureRegistry) -> None:
        self.registry = registry

    def infer(self, stats: PathStats, prop: IncorrectProperty) -> TypeInference:
        """Full inference pipeline for a single property."""
        inferred_type: str
        converter: str
        method: str
        match_score: float | None = None
        structural: dict[str, Any] | None = None

        if stats.non_none_count == 0:
            # No data observed — use name hint or default to str
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
            # First: try to infer from observed values (e.g. ISO datetime strings)
            if stats.non_none_count > 0:
                inferred_type, converter = self._infer_from_observed(stats, prop)
                method = "data"
                # If still str, fallback to name hint
                if inferred_type == "str | None":
                    hint = infer_from_name(prop.python_name)
                    if hint:
                        inferred_type, converter_fn = hint
                        converter = f'{converter_fn}(obj, "{prop.json_key}")'
                        method = "name_hint"
            else:
                # No data — use name hint
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
        """Infer type for dict[str, Any] properties using structural matching."""
        # Merge all observed dict keys
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

        # Fallback: report as dict with observed keys
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
        """Infer type for list[Any] properties."""
        # Check if list elements are dicts → structural match
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

        # Check if elements are simple types
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

        # Check if observed type is actually not a list (e.g. always None)
        if "list" not in stats.types and stats.non_none_count > 0:
            return self._infer_from_observed_as_tuple(stats, prop)

        # Unknown list element type
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
        """Wrap _infer_from_observed to return 5-tuple."""
        py_type, conv = self._infer_from_observed(stats, prop)
        return py_type, conv, "data", None, None

    def _infer_any(
        self, stats: PathStats, prop: IncorrectProperty
    ) -> tuple[str, str, str]:
        """Infer type for Any | None properties."""
        # Check if observed values are dicts → try structural match
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
        """Infer type from observed primitive values."""
        if stats.non_none_count == 0:
            hint = infer_from_name(prop.python_name)
            if hint:
                return hint[0], f'{hint[1]}(obj, "{prop.json_key}")'
            return "str | None", f'from_str(obj, "{prop.json_key}")  # default'

        type_counts = stats.types

        if len(type_counts) == 1:
            type_name = next(iter(type_counts))
            return self._infer_single(type_name, stats.samples, prop.json_key)

        # Mixed types — build union
        type_parts: list[str] = []
        converter_parts: list[str] = []
        for tn in sorted(type_counts.keys()):
            type_samples = [s for s in stats.samples if type(s).__name__ == tn]
            py_type, conv = self._infer_single(tn, type_samples, prop.json_key)
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
        type_name: str, samples: list[Any], json_key: str
    ) -> tuple[str, str]:
        if type_name == "str":
            return TypeInferrer._refine_str(samples, json_key)
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
    def _refine_str(samples: list[Any], json_key: str) -> tuple[str, str]:
        str_samples = [s for s in samples if isinstance(s, str)]
        if not str_samples:
            return "str | None", f'from_str(obj, "{json_key}")'

        dt_matches = sum(1 for s in str_samples if ISO_DATETIME_RE.match(s))
        if dt_matches == len(str_samples):
            return "datetime | None", f'from_datetime(obj, "{json_key}")'

        uuid_matches = sum(1 for s in str_samples if UUID_RE.match(s))
        if uuid_matches == len(str_samples):
            return "UUID | None", f'from_uuid(obj, "{json_key}")'

        return "str | None", f'from_str(obj, "{json_key}")'


# ---------------------------------------------------------------------------
# TokenFetcher
# ---------------------------------------------------------------------------
class TokenFetcher:
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

    def collect_meili_to_jsonl(self, index_uid: str, output_path: Path) -> int:
        """Paginate MeiliSearch index, write directly to JSONL (no temp files)."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        offset = 0
        total_hits = 0

        with open(output_path, "w", encoding="utf-8") as out:
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

                for hit in hits:
                    out.write(json.dumps(hit, default=str, ensure_ascii=False) + "\n")
                total_hits += len(hits)

                estimated_total = results[0].get("estimatedTotalHits", 0)
                logger.info(
                    "  %s: fetched %d hits (offset=%d, estimated=%d)",
                    index_uid,
                    total_hits,
                    offset,
                    estimated_total,
                )

                if len(hits) < MEILI_BATCH_SIZE:
                    break
                offset += MEILI_BATCH_SIZE

        self.stats["hits_per_index"][index_uid] = total_hits
        return total_hits

    # -- REST ---------------------------------------------------------------

    def _rest_get(self, url: str, timeout: int = 60) -> dict[str, Any] | None:
        for attempt in range(REST_RETRY_MAX + 1):
            try:
                resp = http_get_json(url, self.api_headers, timeout=timeout)
                time.sleep(REST_DELAY)
                return resp
            except Exception as exc:
                exc_str = str(exc)
                is_retryable = any(
                    code in exc_str for code in ("502", "504", "timed out")
                )
                if is_retryable and attempt < REST_RETRY_MAX:
                    wait = REST_RETRY_BACKOFF * (2**attempt)
                    logger.warning(
                        "REST GET %s failed (attempt %d/%d): %s — retrying in %.0fs",
                        url,
                        attempt + 1,
                        REST_RETRY_MAX + 1,
                        exc,
                        wait,
                    )
                    time.sleep(wait)
                else:
                    logger.warning("REST GET %s failed: %s", url, exc)
                    time.sleep(REST_DELAY)
                    return None
        return None

    def collect_rest_to_jsonl(
        self,
        endpoint: str,
        fields: list[str] | None,
        output_path: Path,
    ) -> int:
        """Paginate endpoint, deduplicate, write directly to JSONL (no temp files)."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        seen_ids: set[str] = set()
        count = 0
        offset = 0
        page = 0

        with open(output_path, "w", encoding="utf-8") as out:
            while True:
                params: dict[str, Any] = {"limit": REST_PAGE_SIZE, "offset": offset}
                if fields:
                    params["fields[]"] = fields
                base_url = f"{API_FFBB_BASE_URL}{endpoint}"
                url = url_with_params(base_url, params)

                resp = self._rest_get(url)
                if not resp:
                    break

                data = resp.get("data", resp)
                if isinstance(data, list):
                    if not data:
                        break
                    for item in data:
                        item_id = str(item.get("id", ""))
                        if item_id and item_id in seen_ids:
                            continue
                        if item_id:
                            seen_ids.add(item_id)
                        out.write(
                            json.dumps(item, default=str, ensure_ascii=False) + "\n"
                        )
                        count += 1
                    if page == 0 or (page + 1) % 10 == 0 or len(data) < REST_PAGE_SIZE:
                        logger.info(
                            "  %s: page %d — %d items (total: %d)",
                            endpoint,
                            page + 1,
                            len(data),
                            count,
                        )
                    if len(data) < REST_PAGE_SIZE:
                        break
                elif isinstance(data, dict):
                    out.write(json.dumps(data, default=str, ensure_ascii=False) + "\n")
                    count += 1
                    break
                else:
                    break

                offset += REST_PAGE_SIZE
                page += 1

        self.stats["rest_calls"][endpoint] = {"count": count}
        logger.info("  REST %s: %d items → %s", endpoint, count, output_path.name)
        return count

    def collect_rest_list(
        self, endpoint: str, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """Fetch a list endpoint (single page)."""
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

    def collect_lives(self, endpoint: str) -> dict[str, Any] | None:
        url = f"{API_FFBB_BASE_URL}{endpoint}"
        resp = self._rest_get(url)
        if resp:
            self.stats["rest_calls"]["lives"] = {"fetched": True}
        return resp


# ---------------------------------------------------------------------------
# Pipeline helpers — merge and flatten (parallelizable per endpoint)
# ---------------------------------------------------------------------------


def flatten_endpoint(
    jsonl_path: Path, prefix: str, record_whole_keys: set[str]
) -> JsonFlattener:
    """Flatten a JSONL file into a per-endpoint flattener (no shared state)."""
    flattener = JsonFlattener(record_whole_keys=record_whole_keys)
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                flattener.flatten(item, prefix)
    return flattener


# ---------------------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------------------
class ReportGenerator:

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
        inferences: list[TypeInference],
    ) -> dict[str, Any]:
        resolved_data = 0
        resolved_structure = 0
        resolved_name = 0
        defaulted = 0

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

            corrections.append(entry)

        # Detect new model candidates (unresolved dict structures)
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

            print(
                f"{marker} {c['class']}.{c['property']}: "
                f"{c['current_type']} -> {c['inferred_type']}  "
                f"({method}, evidence: {c['evidence']['non_none']}/{c['evidence']['total']})"
                f"{score_str}"
            )
            if c["evidence"]["samples"] and c["inference_method"] != "default":
                sample_str = str(c["evidence"]["samples"][0])
                if len(sample_str) > 80:
                    sample_str = sample_str[:80] + "..."
                print(f"     sample: {sample_str}")

        # New model candidates
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
# Main orchestrator
# ---------------------------------------------------------------------------
def main() -> None:
    logger.info("=== Type Discovery Script ===")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------------------------
    # Phase 0: Dynamic discovery of config constants and source code scanning
    # -----------------------------------------------------------------------
    logger.info("Phase 0: Dynamic discovery...")

    # 0a. Discover config constants dynamically from modules
    endpoint_map = _discover_config_constants(_directus_config, "ENDPOINT_")
    meili_index_map = _discover_config_constants(_meili_config, "MEILISEARCH_INDEX_")

    # Filter out the aggregate UIDS list constant (it's a list, not a string,
    # so _discover_config_constants already skips it)
    logger.info(
        "  Discovered %d REST endpoints: %s",
        len(endpoint_map),
        sorted(endpoint_map.keys()),
    )
    logger.info(
        "  Discovered %d MeiliSearch indexes: %s",
        len(meili_index_map),
        sorted(meili_index_map.keys()),
    )

    meili_index_uids = list(meili_index_map.values())

    # 0b. Build class → index/prefix mappings from source code
    meili_class_to_index = _build_meili_class_to_index(MODEL_DIRS, meili_index_map)
    rest_class_to_prefix = _build_rest_class_to_prefix(MODEL_DIRS, endpoint_map)

    logger.info("  meili_class_to_index: %s", meili_class_to_index)
    logger.info("  rest_class_to_prefix: %s", rest_class_to_prefix)

    # 0c. Build paginated endpoint list: ALL Directus endpoints (except special)
    special_endpoints = {"lives", "configuration", "saisons"}
    directus_dir = next((d for d in MODEL_DIRS if "directus_ffbb" in str(d)), None)
    directus_model_bases: set[str] = set()
    if directus_dir and directus_dir.exists():
        for py_file in directus_dir.glob("get_*_response.py"):
            stem = py_file.stem
            base = stem[4:].rsplit("_response", 1)[0]
            plural = base if base.endswith("s") else base + "s"
            directus_model_bases.add(plural)
    paginated_bases = sorted(directus_model_bases - special_endpoints)
    paginated_endpoints: list[tuple[str, str]] = [
        (endpoint_map[base], base) for base in paginated_bases if base in endpoint_map
    ]
    logger.info(
        "  paginated_endpoints: %s",
        [name for _, name in paginated_endpoints],
    )

    # 0e. Scan source code for incorrectly typed properties
    logger.info("Phase 0e: Scanning source code for incorrectly typed properties...")
    incorrect_props = SourceCodeScanner.scan_all(MODEL_DIRS)
    logger.info("  Found %d incorrectly typed properties", len(incorrect_props))

    for prop in incorrect_props:
        logger.info(
            "    [%s] %s.%s (%s) -> json_key=%s",
            prop.category,
            prop.class_name,
            prop.python_name,
            prop.current_type,
            prop.json_key,
        )

    # Build record_whole_keys from scanned properties
    record_whole_keys: set[str] = set()
    for prop in incorrect_props:
        if prop.category in ("dict_any", "list_any", "list_dict_any", "any_none"):
            record_whole_keys.add(prop.json_key)

    logger.info("  record_whole_keys: %d keys", len(record_whole_keys))

    # Build model signature registry
    logger.info("Phase 0f: Building model signature registry...")
    sig_registry = ModelSignatureRegistry.build_from_source(MODEL_DIRS)

    # -----------------------------------------------------------------------
    # Streaming pipeline: collect → merge → flatten per endpoint (no barrier)
    # -----------------------------------------------------------------------
    logger.info("Fetching tokens...")
    api_token, meili_token = TokenFetcher.fetch()
    collector = RawDataCollector(api_token, meili_token)

    responses_dir = DATA_DIR / "responses"
    responses_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.monotonic()

    def _pipeline_rest_paginated(
        endpoint: str, name: str
    ) -> tuple[str, str, JsonFlattener | None]:
        """Collect+dedup → flatten for a REST paginated endpoint (no temp files)."""
        jsonl_path = responses_dir / f"rest_{name}.jsonl"
        prefix = f"rest/{name}"
        count = collector.collect_rest_to_jsonl(endpoint, ["*.*"], jsonl_path)
        if count == 0:
            return name, "rest", None
        flattener = flatten_endpoint(jsonl_path, prefix, record_whole_keys)
        logger.info(
            "  [done] %s: %d items, %d paths", name, count, len(flattener.paths)
        )
        return name, "rest", flattener

    def _pipeline_rest_special(
        endpoint: str, name: str, fetch_fn: str
    ) -> tuple[str, str, JsonFlattener | None]:
        """Collect → flatten for special REST endpoints (single-page)."""
        jsonl_path = responses_dir / f"rest_{name}.jsonl"
        prefix = f"rest/{name}"
        if fetch_fn == "list":
            data = collector.collect_rest_list(endpoint, ["*.*"])
        elif fetch_fn == "lives":
            raw = collector.collect_lives(endpoint)
            if raw is None:
                data = []
            elif isinstance(raw, list):
                data = raw
            else:
                data = [raw]
        else:
            data = []
        if not data:
            return name, "rest", None
        # Write directly to JSONL
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, default=str, ensure_ascii=False) + "\n")
        logger.info("  [done] %s: %d items", name, len(data))
        flattener = flatten_endpoint(jsonl_path, prefix, record_whole_keys)
        return name, "rest", flattener

    def _pipeline_meili(
        index_uid: str,
    ) -> tuple[str, str, JsonFlattener | None]:
        """Collect → flatten for a MeiliSearch index (no temp files)."""
        jsonl_path = responses_dir / f"meili_{index_uid}.jsonl"
        prefix = f"meilisearch/{index_uid}/hits[]"
        count = collector.collect_meili_to_jsonl(index_uid, jsonl_path)
        if count == 0:
            return index_uid, "meilisearch", None
        flattener = flatten_endpoint(jsonl_path, prefix, record_whole_keys)
        logger.info(
            "  [done] %s: %d hits, %d paths", index_uid, count, len(flattener.paths)
        )
        return index_uid, "meilisearch", flattener

    logger.info(
        "Streaming pipeline: collect → merge → flatten (parallel per endpoint)..."
    )

    with ThreadPoolExecutor(max_workers=REST_PARALLEL_WORKERS) as ex:
        futures: dict[Any, str] = {}

        # REST paginated endpoints
        for endpoint, name in paginated_endpoints:
            futures[ex.submit(_pipeline_rest_paginated, endpoint, name)] = name

        # MeiliSearch indexes
        for uid in meili_index_uids:
            futures[ex.submit(_pipeline_meili, uid)] = uid

        # Special endpoints
        saisons_ep = endpoint_map.get("saisons")
        if saisons_ep:
            futures[
                ex.submit(_pipeline_rest_special, saisons_ep, "saisons", "list")
            ] = "saisons"
        config_ep = endpoint_map.get("configuration")
        if config_ep:
            futures[
                ex.submit(_pipeline_rest_special, config_ep, "configuration", "list")
            ] = "configuration"
        lives_ep = endpoint_map.get("lives")
        if lives_ep:
            futures[ex.submit(_pipeline_rest_special, lives_ep, "lives", "lives")] = (
                "lives"
            )

        # Collect results as they complete
        per_endpoint_flatteners: list[tuple[JsonFlattener, str, str]] = []
        for future in as_completed(futures):
            ep_name = futures[future]
            try:
                name, source_type, flattener = future.result()
                if flattener:
                    per_endpoint_flatteners.append((flattener, name, source_type))
                    logger.info(
                        "  [done] %s (%.1fs elapsed)", name, time.monotonic() - t0
                    )
                else:
                    logger.warning("  [skip] %s: no data", name)
            except Exception as exc:
                logger.error("  [fail] %s: %s", ep_name, exc)

    # Merge all per-endpoint flatteners into a combined flattener
    combined_flattener = JsonFlattener()
    for flattener, _, _ in per_endpoint_flatteners:
        for path, stats in flattener.paths.items():
            if path not in combined_flattener.paths:
                combined_flattener.paths[path] = stats
            else:
                combined_flattener.paths[path].merge(stats)

    t_pipeline = time.monotonic() - t0
    logger.info(
        "Pipeline done in %.1fs — %d endpoints, %d total paths",
        t_pipeline,
        len(per_endpoint_flatteners),
        len(combined_flattener.paths),
    )

    # -----------------------------------------------------------------------
    # Phase 4: INFERENCE — sequential type inference
    # -----------------------------------------------------------------------
    logger.info("Phase 4: Inferring types...")
    inferrer = TypeInferrer(sig_registry)
    inferences: list[TypeInference] = []

    for prop in incorrect_props:
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

        inference = inferrer.infer(merged, prop)
        inferences.append(inference)

    # -----------------------------------------------------------------------
    # Phase 5: Generate reports
    # -----------------------------------------------------------------------
    logger.info("Phase 5: Generating reports...")

    raw_report = ReportGenerator.generate_raw_report(
        combined_flattener, collector.stats
    )
    corrections_report = ReportGenerator.generate_corrections(inferences)

    raw_path = DATA_DIR / "type_discovery_raw.json"
    corrections_path = DATA_DIR / "type_discovery_corrections.json"

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_report, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Raw report written to %s", raw_path)

    with open(corrections_path, "w", encoding="utf-8") as f:
        json.dump(corrections_report, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Corrections report written to %s", corrections_path)

    # -----------------------------------------------------------------------
    # Phase 6: Enum candidate detection
    # -----------------------------------------------------------------------
    logger.info("Phase 6: Detecting enum candidates...")
    enum_candidates: list[dict[str, Any]] = []

    for path, stats in combined_flattener.paths.items():
        if stats.non_none_count < 10:
            continue
        if "str" not in stats.types:
            continue
        str_samples = [s for s in stats.samples if isinstance(s, str)]
        if not str_samples:
            continue
        unique_values = sorted(set(str_samples))
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

    total_time = time.monotonic() - t0
    logger.info("Done in %.1fs total.", total_time)


if __name__ == "__main__":
    main()
