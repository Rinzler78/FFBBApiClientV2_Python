#!/usr/bin/env python3
"""
Audit API fields vs Python models.

Compares real API fields (Directus + Meilisearch) against Python dataclass models.
Produces a JSON report showing fields to ADD, DELETE, or MODIFY.

Usage:
    python scripts/audit_api_models.py                 # uses discovery data + fresh Meilisearch
    python scripts/audit_api_models.py --fetch-fresh   # re-fetches everything from APIs
    python scripts/audit_api_models.py --only competitions organismes
    python scripts/audit_api_models.py --verbose
"""

from __future__ import annotations

import argparse
import ast
import dataclasses
import inspect
import json
import logging
import re
import textwrap
import typing
from dataclasses import fields as dc_fields
from datetime import datetime
from pathlib import Path
from typing import Any

from ffbb_api_client_v2._http.client import (
    http_get_json,
    http_post_json,
    url_with_params,
)
from ffbb_api_client_v2.config import (
    MEILISEARCH_BASE_URL,
    MEILISEARCH_ENDPOINT_MULTI_SEARCH,
)
from ffbb_api_client_v2.directus.client import DEFAULT_USER_AGENT
from ffbb_api_client_v2.directus_ffbb.config import (
    API_FFBB_BASE_URL,
    ENDPOINT_COMPETITIONS,
    ENDPOINT_ORGANISMES,
    ENDPOINT_POULES,
    ENDPOINT_SAISONS,
)
from ffbb_api_client_v2.directus_ffbb.models.get_competition_response import (
    GetCompetitionResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_poule_response import (
    GetPouleResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_saisons_response import (
    GetSaisonsResponse,
)
from ffbb_api_client_v2.facade.token_manager import TokenManager
from ffbb_api_client_v2.models.competitions_hit import CompetitionsHit
from ffbb_api_client_v2.models.engagements_hit import EngagementsHit
from ffbb_api_client_v2.models.formations_hit import FormationsHit
from ffbb_api_client_v2.models.organismes_hit import OrganismesHit
from ffbb_api_client_v2.models.pratiques_hit import PratiquesHit
from ffbb_api_client_v2.models.rencontres_hit import RencontresHit
from ffbb_api_client_v2.models.salles_hit import SallesHit
from ffbb_api_client_v2.models.terrains_hit import TerrainsHit
from ffbb_api_client_v2.models.tournois_hit import TournoisHit

PROJECT_ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

DATA_DIR = PROJECT_ROOT / "data"

# ---------------------------------------------------------------------------
# Endpoint → Model mappings
# ---------------------------------------------------------------------------
DIRECTUS_MAP: dict[str, type] = {
    "competitions": GetCompetitionResponse,
    "organismes": GetOrganismeResponse,
    "poules": GetPouleResponse,
    "saisons": GetSaisonsResponse,
}

MEILISEARCH_MAP: dict[str, type] = {
    "ffbbserver_competitions": CompetitionsHit,
    "ffbbserver_organismes": OrganismesHit,
    "ffbbserver_rencontres": RencontresHit,
    "ffbbserver_terrains": TerrainsHit,
    "ffbbserver_salles": SallesHit,
    "ffbbserver_tournois": TournoisHit,
    "ffbbnational_pratiques": PratiquesHit,
    "ffbbserver_engagements": EngagementsHit,
    "ffbbserver_formations": FormationsHit,
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
_CAMEL_RE1 = re.compile(r"(.)([A-Z][a-z]+)")
_CAMEL_RE2 = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    s = _CAMEL_RE1.sub(r"\1_\2", name)
    return _CAMEL_RE2.sub(r"\1_\2", s).lower()


def normalize_path(path: str) -> str:
    """Normalize a field path: camelCase → snake_case, remove [] markers."""
    parts = path.replace("[]", "").split(".")
    return ".".join(camel_to_snake(p) for p in parts if p)


def _resolve_type(annotation: Any) -> Any:
    """Resolve a type annotation to its base type, stripping Optional/Union/list."""
    origin = typing.get_origin(annotation)
    if origin is typing.Union:
        # X | None → X
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        return args[0] if args else None
    if origin is list:
        inner = typing.get_args(annotation)
        return inner[0] if inner else None
    if isinstance(annotation, type):
        return annotation
    return None


def _type_name(t: Any) -> str:
    """Get a readable type name from a type annotation."""
    if t is type(None):
        return "None"
    if isinstance(t, str):
        return t
    origin = typing.get_origin(t)
    if origin is typing.Union:
        parts = [_type_name(a) for a in typing.get_args(t)]
        return " | ".join(parts)
    if origin is list:
        args = typing.get_args(t)
        inner = _type_name(args[0]) if args else "Any"
        return f"list[{inner}]"
    if isinstance(t, type):
        return t.__name__
    return str(t)


# ---------------------------------------------------------------------------
# ModelIntrospector
# ---------------------------------------------------------------------------
class ModelIntrospector:
    """Extract field information from Python dataclass models."""

    @staticmethod
    def introspect_model(cls: type) -> list[dict[str, Any]]:
        """Get all fields from a dataclass, excluding computed (init=False) fields."""
        if not dataclasses.is_dataclass(cls):
            return []
        result = []
        for f in dc_fields(cls):
            if not f.init:
                continue  # skip lower_* computed fields
            result.append(
                {
                    "name": f.name,
                    "type": (
                        _type_name(f.type) if isinstance(f.type, type) else str(f.type)
                    ),
                    "annotation": f.type,
                }
            )
        return result

    @staticmethod
    def extract_json_keys_from_to_dict(cls: Any) -> dict[str, str]:
        """Parse to_dict() via AST to extract mapping: python_attr → json_key.

        Looks for patterns like: result["jsonKey"] = self.python_attr
        """
        mapping: dict[str, str] = {}
        to_dict = getattr(cls, "to_dict", None)
        if to_dict is None:
            return mapping
        try:
            source = inspect.getsource(to_dict)
        except (TypeError, OSError):
            return mapping

        source = textwrap.dedent(source)
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return mapping

        for node in ast.walk(tree):
            # Match: result["key"] = self.attr  or  result["key"] = ...
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.slice, ast.Constant)
                    and isinstance(target.slice.value, str)
                ):
                    json_key = target.slice.value
                    # Try to extract self.attr_name from value
                    value = node.value
                    attr_name = ModelIntrospector._extract_self_attr(value)
                    if attr_name:
                        mapping[attr_name] = json_key

        return mapping

    @staticmethod
    def extract_json_keys_from_from_dict(cls: Any) -> dict[str, str]:
        """Parse from_dict() via AST to extract mapping: python_attr → json_key.

        For Meilisearch hits: looks for from_xxx(obj, "jsonKey") patterns.
        For Directus models: looks for data.get("jsonKey") patterns.
        """
        mapping: dict[str, str] = {}
        from_dict = getattr(cls, "from_dict", None)
        if from_dict is None:
            return mapping
        try:
            source = inspect.getsource(from_dict)
        except (TypeError, OSError):
            return mapping

        source = textwrap.dedent(source)
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return mapping

        # Strategy 1: Match `var = from_xxx(obj, "key")` or `from_xxx(Cls, obj, "key")`
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                    call = node.value
                    json_key = ModelIntrospector._extract_string_arg(call)
                    if json_key:
                        mapping[target.id] = json_key

        # Strategy 2: Match `data.get("key")` in return statement constructor args
        # This handles Directus models
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg:
                # keyword arg in constructor: arg=xxx(..., "key") or arg=data.get("key")
                json_key = ModelIntrospector._extract_get_key(node.value)
                if json_key:
                    mapping[node.arg] = json_key

        return mapping

    @staticmethod
    def _extract_self_attr(node: ast.AST) -> str | None:
        """Extract 'attr' from self.attr, or from deeper expressions."""
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "self":
                return node.attr
        # Handle self.attr.value, self.attr.isoformat(), etc.
        if isinstance(node, ast.Call):
            return ModelIntrospector._extract_self_attr(node.func)
        if isinstance(node, ast.Attribute):
            return ModelIntrospector._extract_self_attr(node.value)
        # Handle list comprehension: [x.to_dict() for x in self.attr]
        if isinstance(node, ast.ListComp):
            for gen in node.generators:
                attr = ModelIntrospector._extract_self_attr(gen.iter)
                if attr:
                    return attr
        # Handle str(self.attr)
        if isinstance(node, ast.Call) and node.args:
            return ModelIntrospector._extract_self_attr(node.args[0])
        return None

    @staticmethod
    def _extract_string_arg(call: ast.Call) -> str | None:
        """Extract the JSON key string argument from a from_xxx() call."""
        # from_str(obj, "key"), from_int(obj, "key"), from_bool(obj, "key") etc.
        # from_enum(Enum, obj, "key"), from_obj(Cls.from_dict, obj, "key")
        # from_list(fn, obj, "key")
        for arg in call.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                return arg.value
        return None

    @staticmethod
    def _extract_get_key(node: ast.AST) -> str | None:
        """Extract key from data.get("key") or wrapping calls like str(data.get("key"))."""
        if isinstance(node, ast.Call):
            # Direct: data.get("key")
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                return node.args[0].value
            # Wrapped: str(data.get("key")), int(data.get("key")), etc.
            if node.args:
                for arg in node.args:
                    result = ModelIntrospector._extract_get_key(arg)
                    if result:
                        return result
        # Ternary: X if Y else Z
        if isinstance(node, ast.IfExp):
            result = ModelIntrospector._extract_get_key(node.body)
            if result:
                return result
            return ModelIntrospector._extract_get_key(node.orelse)
        return None

    @staticmethod
    def flatten_model(
        cls: type,
        prefix: str = "",
        visited: set[int] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Flatten a dataclass model into dot-separated paths with json_key mapping.

        Returns: {normalized_path: {"json_path": ..., "python_attr": ..., "type": ...}}
        """
        if visited is None:
            visited = set()

        cls_id = id(cls)
        if cls_id in visited:
            return {}
        visited.add(cls_id)

        if not dataclasses.is_dataclass(cls):
            return {}

        result: dict[str, dict[str, Any]] = {}

        # Get json key mapping from to_dict or from_dict
        json_mapping: dict[str, str] = {}
        if hasattr(cls, "to_dict"):
            json_mapping = ModelIntrospector.extract_json_keys_from_to_dict(cls)
        if not json_mapping and hasattr(cls, "from_dict"):
            json_mapping = ModelIntrospector.extract_json_keys_from_from_dict(cls)

        model_fields = ModelIntrospector.introspect_model(cls)

        for field_info in model_fields:
            attr_name = field_info["name"]
            annotation = field_info["annotation"]
            type_str = field_info["type"]

            # Get json key (fallback to attr name for Directus models)
            json_key = json_mapping.get(attr_name, attr_name)
            json_path = f"{prefix}.{json_key}" if prefix else json_key

            # Resolve inner type for recursion
            inner_type = _resolve_type(annotation)

            # Check if inner type is a dataclass we should recurse into
            is_nested = (
                inner_type is not None
                and isinstance(inner_type, type)
                and dataclasses.is_dataclass(inner_type)
            )

            if is_nested:
                assert isinstance(inner_type, type)
                # Recurse into nested dataclass
                nested = ModelIntrospector.flatten_model(
                    inner_type, json_path, visited.copy()
                )
                result.update(nested)
                # Also record the parent field itself (as an object/list)
                norm_path = normalize_path(json_path)
                result[norm_path] = {
                    "json_path": json_path,
                    "python_attr": attr_name,
                    "type": type_str,
                    "is_object": True,
                }
            else:
                norm_path = normalize_path(json_path)
                result[norm_path] = {
                    "json_path": json_path,
                    "python_attr": attr_name,
                    "type": type_str,
                    "is_object": False,
                }

        return result

    @staticmethod
    def flatten_directus_model(
        cls: type,
        prefix: str = "",
        visited: set[int] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """Flatten a Directus response model with inner nested classes.

        Directus models use camelCase field names that match JSON keys directly.
        Nested models are inner classes (e.g., CategorieModel).
        """
        if visited is None:
            visited = set()

        cls_id = id(cls)
        if cls_id in visited:
            return {}
        visited.add(cls_id)

        if not dataclasses.is_dataclass(cls):
            return {}

        result: dict[str, dict[str, Any]] = {}
        model_fields = ModelIntrospector.introspect_model(cls)

        # Resolve type hints in the class context
        try:
            hints = typing.get_type_hints(cls)
        except Exception:
            hints = {}

        for field_info in model_fields:
            attr_name = field_info["name"]
            annotation = hints.get(attr_name, field_info["annotation"])
            type_str = _type_name(annotation)

            # For Directus models, field name IS the json key
            json_key = attr_name
            json_path = f"{prefix}.{json_key}" if prefix else json_key

            # Resolve inner type
            inner_type = _resolve_type(annotation)

            # Check for nested dataclass (inner classes or imported models)
            is_nested = (
                inner_type is not None
                and isinstance(inner_type, type)
                and dataclasses.is_dataclass(inner_type)
            )

            if is_nested:
                assert isinstance(inner_type, type)
                nested = ModelIntrospector.flatten_directus_model(
                    inner_type, json_path, visited.copy()
                )
                result.update(nested)
                norm_path = normalize_path(json_path)
                result[norm_path] = {
                    "json_path": json_path,
                    "python_attr": attr_name,
                    "type": type_str,
                    "is_object": True,
                }
            else:
                norm_path = normalize_path(json_path)
                result[norm_path] = {
                    "json_path": json_path,
                    "python_attr": attr_name,
                    "type": type_str,
                    "is_object": False,
                }

        return result


# ---------------------------------------------------------------------------
# ApiFieldCollector
# ---------------------------------------------------------------------------
class ApiFieldCollector:
    """Collect real API fields from discovery data and live fetches."""

    def __init__(self, api_token: str | None, meili_token: str | None) -> None:
        self.api_token = api_token
        self.meili_token = meili_token
        self.api_headers = (
            {
                "user-agent": DEFAULT_USER_AGENT,
                "Authorization": f"Bearer {api_token}",
            }
            if api_token
            else {}
        )
        self.meili_headers = (
            {
                "user-agent": DEFAULT_USER_AGENT,
                "Authorization": f"Bearer {meili_token}",
                "Content-Type": "application/json",
            }
            if meili_token
            else {}
        )
        self.meili_url = f"{MEILISEARCH_BASE_URL}{MEILISEARCH_ENDPOINT_MULTI_SEARCH}"

    def collect_directus(
        self, endpoint_name: str, fetch_fresh: bool = False
    ) -> set[str]:
        """Collect Directus API fields from discovery JSON (+ optional fresh fetch).

        Returns set of dot-separated field paths (in their original case).
        """
        fields: set[str] = set()

        # Primary source: discovery JSON
        discovery_path = DATA_DIR / "directus_field_discovery.json"
        if discovery_path.exists():
            with open(discovery_path, encoding="utf-8") as f:
                discovery = json.load(f)
            endpoint_data = discovery.get(endpoint_name, {})
            all_fields = endpoint_data.get("all_fields", [])
            fields.update(all_fields)
            logger.info(
                "  Directus %s: %d fields from discovery JSON",
                endpoint_name,
                len(all_fields),
            )

        # Optional fresh fetch
        if fetch_fresh and self.api_token:
            fresh = self._fetch_directus_sample(endpoint_name)
            before = len(fields)
            fields.update(fresh)
            logger.info(
                "  Directus %s: +%d new fields from fresh fetch",
                endpoint_name,
                len(fields) - before,
            )

        return fields

    def collect_meilisearch(self, index_uid: str) -> set[str]:
        """Fetch one batch from a Meilisearch index and flatten all field paths."""
        if not self.meili_token:
            logger.warning("  No Meilisearch token, skipping %s", index_uid)
            return set()

        payload = {"queries": [{"indexUid": index_uid, "limit": 20, "offset": 0}]}
        try:
            resp = http_post_json(
                self.meili_url, self.meili_headers, data=payload, timeout=30
            )
        except Exception as exc:
            logger.warning("  Meilisearch %s failed: %s", index_uid, exc)
            return set()

        results = resp.get("results", [])
        if not results:
            return set()
        hits = results[0].get("hits", [])
        if not hits:
            return set()

        # Flatten all hits to get all possible field paths
        all_paths: set[str] = set()
        for hit in hits:
            paths = self._flatten_keys(hit)
            all_paths.update(paths)

        logger.info(
            "  Meilisearch %s: %d hits → %d unique field paths",
            index_uid,
            len(hits),
            len(all_paths),
        )
        return all_paths

    def _fetch_directus_sample(self, endpoint_name: str) -> set[str]:
        """Fetch 1 sample from a Directus endpoint with deep wildcard."""
        endpoint_paths = {
            "competitions": ENDPOINT_COMPETITIONS,
            "organismes": ENDPOINT_ORGANISMES,
            "poules": ENDPOINT_POULES,
            "saisons": ENDPOINT_SAISONS,
        }
        path = endpoint_paths.get(endpoint_name)
        if not path:
            return set()

        base_url = f"{API_FFBB_BASE_URL}{path}"
        url = url_with_params(base_url, {"fields[]": ["*.*.*.*.*"], "limit": "1"})
        try:
            resp = http_get_json(url, self.api_headers, timeout=30)
        except Exception as exc:
            logger.warning("  Fresh fetch %s failed: %s", endpoint_name, exc)
            return set()

        data = resp.get("data", resp)
        if isinstance(data, list) and data:
            data = data[0]
        if not isinstance(data, dict):
            return set()

        return self._flatten_keys(data)

    @staticmethod
    def _flatten_keys(obj: Any, prefix: str = "") -> set[str]:
        """Recursively flatten JSON keys into dot-separated paths."""
        keys: set[str] = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                full_key = f"{prefix}.{k}" if prefix else k
                keys.add(full_key)
                keys.update(ApiFieldCollector._flatten_keys(v, full_key))
        elif isinstance(obj, list):
            for item in obj:
                keys.update(ApiFieldCollector._flatten_keys(item, prefix))
        return keys


# ---------------------------------------------------------------------------
# FieldComparator
# ---------------------------------------------------------------------------
class FieldComparator:
    """Compare API fields against model fields."""

    # Types considered compatible even if they differ
    COMPATIBLE_PAIRS: list[tuple[str, str]] = [
        ("str", "datetime"),
        ("str", "Enum"),
        ("dict", "dataclass"),
        ("int", "bool"),  # JSON 0/1 → bool
    ]

    @staticmethod
    def compare(
        api_fields: set[str],
        model_fields: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """Compare API field paths vs model field paths.

        Returns dict with to_add, to_delete, matches counts.
        """
        # Normalize API paths
        api_normalized: dict[str, str] = {}
        for path in api_fields:
            norm = normalize_path(path)
            # Keep the original (un-normalized) path for reporting
            api_normalized[norm] = path

        model_normalized = set(model_fields.keys())

        api_set = set(api_normalized.keys())
        to_add_keys = api_set - model_normalized
        to_delete_keys = model_normalized - api_set
        overlap = api_set & model_normalized

        to_add = []
        for norm_key in sorted(to_add_keys):
            to_add.append(
                {
                    "normalized_path": norm_key,
                    "json_path": api_normalized[norm_key],
                }
            )

        to_delete = []
        for norm_key in sorted(to_delete_keys):
            info = model_fields[norm_key]
            to_delete.append(
                {
                    "normalized_path": norm_key,
                    "json_path": info.get("json_path", norm_key),
                    "python_attr": info.get("python_attr", ""),
                    "current_type": info.get("type", ""),
                }
            )

        matches = len(overlap)

        return {
            "to_add": to_add,
            "to_delete": to_delete,
            "matches": matches,
        }


# ---------------------------------------------------------------------------
# AuditReporter
# ---------------------------------------------------------------------------
class AuditReporter:
    """Generate audit reports."""

    @staticmethod
    def build_report(
        directus_results: dict[str, dict[str, Any]],
        meilisearch_results: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """Build the full JSON audit report."""
        report: dict[str, Any] = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "directus_endpoints": len(directus_results),
                "meilisearch_indexes": len(meilisearch_results),
            },
            "directus": directus_results,
            "meilisearch": meilisearch_results,
            "summary": {},
        }

        # Compute summary
        total_add = sum(len(r["to_add"]) for r in directus_results.values()) + sum(
            len(r["to_add"]) for r in meilisearch_results.values()
        )

        total_delete = sum(
            len(r["to_delete"]) for r in directus_results.values()
        ) + sum(len(r["to_delete"]) for r in meilisearch_results.values())

        total_matches = sum(r["matches"] for r in directus_results.values()) + sum(
            r["matches"] for r in meilisearch_results.values()
        )

        total_api = total_matches + total_add

        report["summary"] = {
            "total_to_add": total_add,
            "total_to_delete": total_delete,
            "total_matches": total_matches,
            "overall_model_coverage": (
                round(total_matches / total_api * 100, 1) if total_api > 0 else 0
            ),
        }

        return report

    @staticmethod
    def console_summary(report: dict[str, Any]) -> None:
        """Print a readable summary to console."""
        print("\n" + "=" * 72)
        print("  API vs MODEL AUDIT REPORT")
        print("=" * 72)

        summary = report["summary"]
        print(
            f"\n  Overall: {summary['total_matches']} matches, "
            f"{summary['total_to_add']} to add, "
            f"{summary['total_to_delete']} to delete"
        )
        print(f"  Model coverage: {summary['overall_model_coverage']}%")

        # Directus
        if report["directus"]:
            print("\n" + "-" * 72)
            print("  DIRECTUS ENDPOINTS")
            print("-" * 72)
            for name, data in report["directus"].items():
                _print_endpoint(name, data)

        # Meilisearch
        if report["meilisearch"]:
            print("\n" + "-" * 72)
            print("  MEILISEARCH INDEXES")
            print("-" * 72)
            for name, data in report["meilisearch"].items():
                _print_endpoint(name, data)

        print("\n" + "=" * 72)


def _print_endpoint(name: str, data: dict[str, Any]) -> None:
    """Print audit results for a single endpoint/index."""
    add_count = len(data["to_add"])
    del_count = len(data["to_delete"])
    matches = data["matches"]
    total_api = matches + add_count
    coverage = round(matches / total_api * 100, 1) if total_api > 0 else 100

    status = "OK" if add_count == 0 and del_count == 0 else "DRIFT"
    print(
        f"\n  [{status}] {name}  "
        f"(model: {data['model_class']}, "
        f"api: {data['api_fields']}, model: {data['model_fields']}, "
        f"coverage: {coverage}%)"
    )

    if add_count > 0:
        print(f"    + TO ADD ({add_count}):")
        for item in data["to_add"][:15]:
            print(f"      + {item['json_path']}")
        if add_count > 15:
            print(f"      ... and {add_count - 15} more")

    if del_count > 0:
        print(f"    - TO DELETE ({del_count}):")
        for item in data["to_delete"][:10]:
            print(
                f"      - {item['json_path']}  "
                f"({item['python_attr']}: {item['current_type']})"
            )
        if del_count > 10:
            print(f"      ... and {del_count - 10} more")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def audit_directus(
    collector: ApiFieldCollector,
    endpoint_name: str,
    model_cls: type,
    fetch_fresh: bool,
) -> dict[str, Any]:
    """Run audit for a single Directus endpoint."""
    logger.info("Auditing Directus: %s → %s", endpoint_name, model_cls.__name__)

    # Collect API fields
    api_fields = collector.collect_directus(endpoint_name, fetch_fresh)

    # Introspect model
    model_fields = ModelIntrospector.flatten_directus_model(model_cls)

    # Compare
    comparison = FieldComparator.compare(api_fields, model_fields)

    # Get model source file
    try:
        source_file = str(Path(inspect.getfile(model_cls)).relative_to(PROJECT_ROOT))
    except (TypeError, ValueError):
        source_file = "unknown"

    return {
        "model_class": model_cls.__name__,
        "model_file": source_file,
        "api_fields": len(api_fields),
        "model_fields": len(model_fields),
        **comparison,
    }


def audit_meilisearch(
    collector: ApiFieldCollector,
    index_uid: str,
    model_cls: type,
) -> dict[str, Any]:
    """Run audit for a single Meilisearch index."""
    logger.info("Auditing Meilisearch: %s → %s", index_uid, model_cls.__name__)

    # Collect API fields
    api_fields = collector.collect_meilisearch(index_uid)

    # Introspect model (Meilisearch hits have to_dict)
    model_fields = ModelIntrospector.flatten_model(model_cls)

    # Compare
    comparison = FieldComparator.compare(api_fields, model_fields)

    # Get model source file
    try:
        source_file = str(Path(inspect.getfile(model_cls)).relative_to(PROJECT_ROOT))
    except (TypeError, ValueError):
        source_file = "unknown"

    return {
        "model_class": model_cls.__name__,
        "model_file": source_file,
        "api_fields": len(api_fields),
        "model_fields": len(model_fields),
        **comparison,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit API fields vs Python models")
    parser.add_argument(
        "--fetch-fresh",
        action="store_true",
        help="Re-fetch data from live APIs instead of using cached discovery",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="NAME",
        help="Only audit specific endpoints/indexes (e.g., competitions organismes)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=== API vs Model Audit ===")

    # Fetch tokens (needed for fresh fetch and Meilisearch)
    api_token = None
    meili_token = None

    # Determine if we need tokens
    need_meili = True
    need_api = args.fetch_fresh

    if args.only:
        only_set = set(args.only)
        need_meili = bool(only_set & set(MEILISEARCH_MAP.keys()))
        need_api = args.fetch_fresh and bool(only_set & set(DIRECTUS_MAP.keys()))

    if need_meili or need_api:
        logger.info("Fetching API tokens...")
        try:
            tokens = TokenManager.get_tokens()
            if tokens:
                api_token = tokens.api_token
                meili_token = tokens.meilisearch_token
                logger.info("Tokens acquired")
            else:
                logger.warning(
                    "Could not fetch tokens — Meilisearch audit will be skipped"
                )
        except Exception as exc:
            logger.warning("Token fetch failed: %s", exc)

    collector = ApiFieldCollector(api_token, meili_token)

    # Determine which endpoints to audit
    directus_targets = dict(DIRECTUS_MAP)
    meili_targets = dict(MEILISEARCH_MAP)

    if args.only:
        only_set = set(args.only)
        directus_targets = {k: v for k, v in directus_targets.items() if k in only_set}
        meili_targets = {k: v for k, v in meili_targets.items() if k in only_set}

    # Run Directus audits
    directus_results: dict[str, dict[str, Any]] = {}
    for name, model_cls in directus_targets.items():
        directus_results[name] = audit_directus(
            collector, name, model_cls, args.fetch_fresh
        )

    # Run Meilisearch audits
    meilisearch_results: dict[str, dict[str, Any]] = {}
    for index_uid, model_cls in meili_targets.items():
        meilisearch_results[index_uid] = audit_meilisearch(
            collector, index_uid, model_cls
        )

    # Build and save report
    report = AuditReporter.build_report(directus_results, meilisearch_results)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    report_path = DATA_DIR / "api_audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    logger.info("Report written to %s", report_path)

    # Console summary
    AuditReporter.console_summary(report)

    logger.info("Done.")


if __name__ == "__main__":
    main()
