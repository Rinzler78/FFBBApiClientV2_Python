#!/usr/bin/env python3
"""Conversion Coverage Check - Detect unhandled from_* conversion values.

Fetches thousands of real API records via Meilisearch and Directus,
captures all WARNING logs from converter_utils during parsing, and
reports any conversion warning or exception -- surfacing exactly which
key/value/enum is unhandled or which call raised an error.

This script is useful for:
- Detecting new enum values introduced by the FFBB API
- Finding unexpected types in API responses
- Validating that all from_* converters handle real-world data
- Catching runtime exceptions during model parsing

Usage:
    python examples/conversion_coverage_check.py
    python examples/conversion_coverage_check.py --section A   # Meilisearch only
    python examples/conversion_coverage_check.py --section B   # Directus only
    python examples/conversion_coverage_check.py --section C   # FK resolution only
    python examples/conversion_coverage_check.py --section D   # Enum sweeps only
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Ensure local src/ takes precedence over editable installs
_SCRIPT_DIR = Path(__file__).resolve().parent
_SRC_DIR = str(_SCRIPT_DIR.parent / "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from ffbb_api_client_v2 import FFBBAPIClientV2, TokenManager  # noqa: E402

# Logger targeted by all from_* helpers
_CONVERTER_LOGGER = "ffbb_api_client_v2.utils.converter_utils"

# Rate-limit delay between API calls (seconds)
_RATE_DELAY = 0.3

# Meilisearch max per query
_MLS_LIMIT = 1000

# Directus bulk page ceiling
_DIR_MAX = 2000

# Max FK IDs to resolve per type
_FK_BATCH = 10


# ---------------------------------------------------------------------------
# Data collectors
# ---------------------------------------------------------------------------
class WarningCollector(logging.Handler):
    """Captures WARNING+ log records from converter_utils."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self._records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self._records.append(record)

    def drain(self) -> list[str]:
        """Return formatted messages and clear buffer."""
        msgs = [self.format(r) for r in self._records]
        self._records.clear()
        return msgs

    def drain_grouped(self) -> list[tuple[str, int, list[str]]]:
        """Return deduplicated warnings as (signature, count, example_values).

        Groups warnings by a normalized signature (function + key + error kind),
        counts occurrences, and collects distinct concrete values seen.
        """
        msgs = [self.format(r) for r in self._records]
        self._records.clear()

        groups: dict[str, list[str]] = {}
        for msg in msgs:
            sig = _warning_signature(msg)
            groups.setdefault(sig, []).append(msg)

        result: list[tuple[str, int, list[str]]] = []
        for sig, occurrences in groups.items():
            distinct_values = _extract_distinct_values(occurrences)
            result.append((sig, len(occurrences), distinct_values))
        result.sort(key=lambda x: -x[1])
        return result


# Regex patterns for normalizing warning messages into signatures
_RE_CANNOT_PARSE = re.compile(r"(from_int\('[^']+'\): cannot parse )'[^']*'( as int)")
_RE_UNEXPECTED_TYPE = re.compile(
    r"(from_int\('[^']+'\): unexpected type \w+) \(value: [^)]*\)"
)
_RE_FROM_OBJ = re.compile(r"(from_obj\('[^']+'\): expected dict or None, got \w+)")
_RE_UNKNOWN_ENUM = re.compile(r"(from_enum\([^,]+, '[^']+'\): unknown value )'([^']*)'")
_RE_FROM_UUID = re.compile(r"(from_uuid\('[^']+'\): invalid UUID) '.{0,80}")
_RE_FROM_STR = re.compile(r"(from_str\('[^']+'\): cannot convert \w+ to str)")
_RE_PARSE_VALUE = re.compile(r"cannot parse '([^']*)' as int")
_RE_ENUM_VALUE = re.compile(r"unknown value '([^']*)'")
_RE_UUID_VALUE = re.compile(r"invalid UUID '([^']{0,40})")


def _warning_signature(msg: str) -> str:
    """Normalize a warning message into a stable signature for grouping."""
    m = _RE_CANNOT_PARSE.search(msg)
    if m:
        return f"{m.group(1)}<value>{m.group(2)}"
    m = _RE_UNEXPECTED_TYPE.search(msg)
    if m:
        return m.group(1)
    m = _RE_FROM_OBJ.search(msg)
    if m:
        return m.group(1)
    m = _RE_UNKNOWN_ENUM.search(msg)
    if m:
        return f"{m.group(1)}'{m.group(2)}'"
    m = _RE_FROM_UUID.search(msg)
    if m:
        return f"{m.group(1)} <value>"
    m = _RE_FROM_STR.search(msg)
    if m:
        return m.group(1)
    # Fallback: truncate to prevent huge output from blob values
    return msg[:120]


def _extract_distinct_values(messages: list[str], max_vals: int = 5) -> list[str]:
    """Extract distinct concrete values from a group of similar warnings."""
    _value_patterns = [_RE_PARSE_VALUE, _RE_ENUM_VALUE, _RE_UUID_VALUE]
    values: list[str] = []
    seen: set[str] = set()
    for msg in messages:
        v = None
        for pat in _value_patterns:
            m = pat.search(msg)
            if m:
                v = m.group(1)
                break
        if v is None:
            continue
        # Truncate very long values (e.g. base64 blobs)
        if len(v) > 40:
            v = v[:40] + "..."
        if v not in seen:
            seen.add(v)
            values.append(v)
        if len(values) >= max_vals:
            break
    return values


@dataclass
class ExceptionRecord:
    """Stores a caught exception with context."""

    label: str
    exception_type: str
    message: str
    traceback_short: str
    context: str = ""


@dataclass
class CheckResult:
    """Aggregated result for a single check."""

    label: str
    # Each entry: (signature, count, example_values)
    warning_groups: list[tuple[str, int, list[str]]] = field(default_factory=list)
    exceptions: list[ExceptionRecord] = field(default_factory=list)
    records_parsed: int = 0

    @property
    def total_warnings(self) -> int:
        return sum(count for _, count, _ in self.warning_groups)

    @property
    def distinct_warnings(self) -> int:
        return len(self.warning_groups)

    @property
    def has_issues(self) -> bool:
        return bool(self.warning_groups or self.exceptions)


@dataclass
class SectionResult:
    """Aggregated results for a whole section."""

    name: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def total_warnings(self) -> int:
        return sum(c.total_warnings for c in self.checks)

    @property
    def distinct_warnings(self) -> int:
        return sum(c.distinct_warnings for c in self.checks)

    @property
    def total_exceptions(self) -> int:
        return sum(len(c.exceptions) for c in self.checks)

    @property
    def total_records(self) -> int:
        return sum(c.records_parsed for c in self.checks)

    @property
    def has_issues(self) -> bool:
        return any(c.has_issues for c in self.checks)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _extract_ids(items: list[Any] | None, limit: int = _FK_BATCH) -> list[int]:
    if not items:
        return []
    ids: list[int] = []
    for item in items:
        if isinstance(item, int):
            ids.append(item)
        elif isinstance(item, dict) and "id" in item:
            try:
                ids.append(int(item["id"]))
            except (ValueError, TypeError):
                pass
        else:
            item_id = getattr(item, "id", None)
            if item_id is not None:
                try:
                    ids.append(int(item_id))
                except (ValueError, TypeError):
                    pass
        if len(ids) >= limit:
            break
    return ids


def _extract_str_ids(items: list[Any] | None, limit: int = _FK_BATCH) -> list[str]:
    if not items:
        return []
    ids: list[str] = []
    for item in items:
        if isinstance(item, str):
            ids.append(item)
        elif isinstance(item, dict) and "id" in item:
            ids.append(str(item["id"]))
        else:
            item_id = getattr(item, "id", None)
            if item_id is not None:
                ids.append(str(item_id))
        if len(ids) >= limit:
            break
    return ids


def _count_hits(result: Any) -> int:
    """Count the number of hits/items in a search or list result."""
    if result is None:
        return 0
    if hasattr(result, "hits") and result.hits:
        return len(result.hits)
    if isinstance(result, list):
        return len(result)
    return 1


def _safe_call(
    fn: Any,
    args: tuple = (),
    kwargs: dict | None = None,
    label: str = "",
    context: str = "",
) -> tuple[Any, ExceptionRecord | None]:
    """Call fn(*args, **kwargs), returning (result, exception_record | None)."""
    if kwargs is None:
        kwargs = {}
    try:
        result = fn(*args, **kwargs)
        return result, None
    except Exception as exc:
        tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
        short_tb = "".join(tb[-3:]) if len(tb) > 3 else "".join(tb)
        record = ExceptionRecord(
            label=label,
            exception_type=type(exc).__name__,
            message=str(exc)[:200],
            traceback_short=short_tb.strip(),
            context=context,
        )
        return None, record


_MAX_GROUPS_DISPLAYED = 10


def _report_check(check: CheckResult) -> None:
    """Print check result line with deduplicated warnings."""
    parts = []
    if check.warning_groups:
        parts.append(
            f"{check.total_warnings} warn ({check.distinct_warnings} distinct)"
        )
    if check.exceptions:
        parts.append(f"{len(check.exceptions)} exc")

    if parts:
        detail = ", ".join(parts)
        print(f"  WARN  {check.label}: {detail}  ({check.records_parsed} records)")
        for sig, count, examples in check.warning_groups[:_MAX_GROUPS_DISPLAYED]:
            print(f"        [W] x{count:<5} {sig}")
            if examples:
                vals = ", ".join(repr(v) for v in examples[:5])
                print(f"                   values: [{vals}]")
        remaining = len(check.warning_groups) - _MAX_GROUPS_DISPLAYED
        if remaining > 0:
            print(f"        ... and {remaining} more distinct warning types")
        for e in check.exceptions[:_MAX_GROUPS_DISPLAYED]:
            print(f"        [E] {e.exception_type}: {e.message}")
            if e.context:
                print(f"            context: {e.context}")
        remaining_exc = len(check.exceptions) - _MAX_GROUPS_DISPLAYED
        if remaining_exc > 0:
            print(f"        ... and {remaining_exc} more exceptions")
    else:
        print(f"  OK    {check.label}  ({check.records_parsed} records)")


# ---------------------------------------------------------------------------
# ID Discovery
# ---------------------------------------------------------------------------
def discover_ids(
    client: FFBBAPIClientV2, collector: WarningCollector
) -> dict[str, list]:
    """Chain through live data to collect IDs for FK resolution."""
    print("\n--- Discovering IDs for FK resolution ---")
    ids: dict[str, list] = {
        "organismes": [],
        "salles": [],
        "engagements": [],
        "competitions": [],
        "poules": [],
        "rencontres": [],
        "terrains": [],
        "tournois": [],
        "formations": [],
    }

    # 1) Search organismes
    org_result, _ = _safe_call(
        client.search_organismes, (None,), {"limit": _MLS_LIMIT}, "discover_orgs"
    )
    if org_result and org_result.hits:
        for hit in org_result.hits[:_FK_BATCH]:
            if hit.id is not None:
                try:
                    ids["organismes"].append(int(hit.id))
                except (ValueError, TypeError):
                    pass

    # 2) Get organisme details -> salle + engagement IDs
    for org_id in ids["organismes"][:5]:
        time.sleep(_RATE_DELAY)
        org, _ = _safe_call(
            client.get_organisme, (org_id,), label="discover_org_detail"
        )
        if org is not None:
            if isinstance(org.salle, int):
                ids["salles"].append(org.salle)
            remaining = _FK_BATCH - len(ids["engagements"])
            if remaining > 0:
                ids["engagements"].extend(_extract_ids(org.engagements, remaining))
            remaining = _FK_BATCH - len(ids["competitions"])
            if remaining > 0:
                ids["competitions"].extend(_extract_ids(org.competitions, remaining))

    # 3) Engagement details -> competition + poule IDs
    for eng_id in ids["engagements"][:5]:
        time.sleep(_RATE_DELAY)
        eng, _ = _safe_call(client.get_engagement, (eng_id,), label="discover_eng")
        if eng is not None:
            if isinstance(eng.idCompetition, int):
                if eng.idCompetition not in ids["competitions"]:
                    ids["competitions"].append(eng.idCompetition)
            if isinstance(eng.idPoule, int):
                ids["poules"].append(eng.idPoule)

    # 4) Poule details -> rencontre IDs
    for poule_id in ids["poules"][:3]:
        time.sleep(_RATE_DELAY)
        poule, _ = _safe_call(client.get_poule, (poule_id,), label="discover_poule")
        if poule is not None:
            remaining = _FK_BATCH - len(ids["rencontres"])
            if remaining > 0:
                ids["rencontres"].extend(_extract_ids(poule.rencontres, remaining))

    # 5-6) Search for terrains, tournois
    for key, search_fn in [
        ("terrains", client.search_terrains),
        ("tournois", client.search_tournois),
    ]:
        time.sleep(_RATE_DELAY)
        result, _ = _safe_call(search_fn, (None,), {"limit": 100}, f"discover_{key}")
        if result and result.hits:
            for hit in result.hits[:_FK_BATCH]:
                if hit.id is not None:
                    try:
                        ids[key].append(int(hit.id))
                    except (ValueError, TypeError):
                        pass

    # 7) Search formations
    time.sleep(_RATE_DELAY)
    form_result, _ = _safe_call(
        client.search_formations, (None,), {"limit": 100}, "discover_formations"
    )
    if form_result and form_result.hits:
        ids["formations"] = _extract_str_ids(form_result.hits, _FK_BATCH)

    # Drain discovery warnings (not part of checks)
    collector.drain()

    for key, vals in ids.items():
        print(f"  {key}: {len(vals)} IDs")
    return ids


# ---------------------------------------------------------------------------
# Section runners
# ---------------------------------------------------------------------------
def run_section_a(
    client: FFBBAPIClientV2, collector: WarningCollector
) -> SectionResult:
    """Section A: Meilisearch bulk search coverage."""
    print("\n=== Section A: Meilisearch Bulk Search ===")
    section = SectionResult(name="A: Meilisearch Bulk Search")

    checks: list[tuple[str, Any, list[str | None]]] = [
        (
            "search_organismes",
            client.search_organismes,
            [None, "Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux"],
        ),
        (
            "search_competitions",
            client.search_competitions,
            [
                None,
                "Championnat",
                "Coupe",
                "3x3",
                "Plateau",
                "Pré-National",
                "Régional",
                "Départemental",
                "Entente",
            ],
        ),
        (
            "search_rencontres",
            client.search_rencontres,
            [None, "Paris", "3x3", "Handisport", "Entente", "Forfait"],
        ),
        (
            "search_salles",
            client.search_salles,
            [None, "Paris", "Lyon", "Gymnase", "Complexe"],
        ),
        (
            "search_terrains",
            client.search_terrains,
            [None, "Paris", "Lyon", "Extérieur", "Indoor"],
        ),
        (
            "search_tournois",
            client.search_tournois,
            [None, "3x3", "Féminin", "Masculin", "Mixte", "Jeunes"],
        ),
        (
            "search_pratiques",
            client.search_pratiques,
            [None, "basket", "santé", "inclusif", "micro", "découverte", "tonik"],
        ),
        (
            "search_engagements",
            client.search_engagements,
            [None, "Paris", "Pro", "Entente", "National", "Féminin"],
        ),
        (
            "search_formations",
            client.search_formations,
            [None, "arbitrage", "officiels", "entraîneur"],
        ),
    ]

    for label, search_fn, queries in checks:
        check = CheckResult(label=label)
        collector.drain()
        for q in queries:
            result, exc = _safe_call(
                search_fn, (q,), {"limit": _MLS_LIMIT}, label, f"query={q!r}"
            )
            if exc:
                check.exceptions.append(exc)
            else:
                check.records_parsed += _count_hits(result)
        check.warning_groups = collector.drain_grouped()
        _report_check(check)
        section.checks.append(check)
        time.sleep(_RATE_DELAY)

    return section


def run_section_b(
    client: FFBBAPIClientV2, collector: WarningCollector
) -> SectionResult:
    """Section B: Directus bulk list coverage."""
    print("\n=== Section B: Directus Bulk List ===")
    section = SectionResult(name="B: Directus Bulk List")

    checks: list[tuple[str, Any, dict]] = [
        ("get_saisons", client.get_saisons, {"filter_criteria": None}),
        ("list_all_rencontres", client.list_all_rencontres, {"max_items": _DIR_MAX}),
        ("list_all_salles", client.list_all_salles, {"max_items": _DIR_MAX}),
        ("list_all_terrains", client.list_all_terrains, {"max_items": _DIR_MAX}),
        ("list_all_tournois", client.list_all_tournois, {"max_items": _DIR_MAX}),
        ("list_all_engagements", client.list_all_engagements, {"max_items": _DIR_MAX}),
        ("list_all_formations", client.list_all_formations, {"max_items": _DIR_MAX}),
        ("list_all_pratiques", client.list_all_pratiques, {"max_items": _DIR_MAX}),
        ("list_all_communes", client.list_all_communes, {"max_items": _DIR_MAX}),
        ("get_lives", client.get_lives, {}),
    ]

    for label, list_fn, kwargs in checks:
        check = CheckResult(label=label)
        collector.drain()
        result, exc = _safe_call(list_fn, kwargs=kwargs, label=label)
        if exc:
            check.exceptions.append(exc)
        else:
            check.records_parsed = _count_hits(result)
        check.warning_groups = collector.drain_grouped()
        _report_check(check)
        section.checks.append(check)
        time.sleep(_RATE_DELAY)

    return section


def run_section_c(
    client: FFBBAPIClientV2,
    collector: WarningCollector,
    ids: dict[str, list],
) -> SectionResult:
    """Section C: FK resolution chain."""
    print("\n=== Section C: FK Resolution Chain ===")
    section = SectionResult(name="C: FK Resolution Chain")

    fk_checks: list[tuple[str, str, Any]] = [
        ("get_organisme", "organismes", client.get_organisme),
        ("get_competition", "competitions", client.get_competition),
        ("get_poule", "poules", client.get_poule),
        ("get_engagement", "engagements", client.get_engagement),
        ("get_rencontre", "rencontres", client.get_rencontre),
        ("get_salle", "salles", client.get_salle),
        ("get_terrain", "terrains", client.get_terrain),
        ("get_tournoi", "tournois", client.get_tournoi),
        ("get_formation", "formations", client.get_formation),
    ]

    for label, id_key, get_fn in fk_checks:
        id_list = ids.get(id_key, [])
        if not id_list:
            print(f"  SKIP  {label}: no IDs discovered")
            continue
        check = CheckResult(label=label)
        collector.drain()
        for item_id in id_list[:_FK_BATCH]:
            result, exc = _safe_call(
                get_fn, (item_id,), label=label, context=f"id={item_id!r}"
            )
            if exc:
                check.exceptions.append(exc)
            elif result is not None:
                check.records_parsed += 1
            time.sleep(_RATE_DELAY)
        check.warning_groups = collector.drain_grouped()
        _report_check(check)
        section.checks.append(check)

    return section


def run_section_d(
    client: FFBBAPIClientV2, collector: WarningCollector
) -> SectionResult:
    """Section D: High-diversity enum sweeps."""
    print("\n=== Section D: High-Diversity Enum Sweeps ===")
    section = SectionResult(name="D: High-Diversity Enum Sweeps")

    sweeps: list[tuple[str, Any, list[str | None]]] = [
        (
            "sweep_competitions",
            client.search_multiple_competitions,
            [
                None,
                "Championnat",
                "Coupe",
                "3x3",
                "Féminin",
                "Mixte",
                "Pré-National",
                "Départemental",
            ],
        ),
        (
            "sweep_rencontres",
            client.search_multiple_rencontres,
            [None, "Départemental", "Régional", "National", "3x3", "Entente"],
        ),
        (
            "sweep_tournois",
            client.search_multiple_tournois,
            [None, "3x3", "5x5", "Féminin", "Masculin", "Mixte", "Jeunes"],
        ),
        (
            "sweep_terrains",
            client.search_multiple_terrains,
            [None, "Paris", "Lyon", "Marseille", "Extérieur"],
        ),
        (
            "sweep_pratiques",
            client.search_multiple_pratiques,
            [None, "basket", "santé", "inclusif", "tonik", "micro", "découverte"],
        ),
    ]

    for label, search_fn, queries in sweeps:
        check = CheckResult(label=label)
        collector.drain()
        result, exc = _safe_call(search_fn, (queries,), {"limit": _MLS_LIMIT}, label)
        if exc:
            check.exceptions.append(exc)
        else:
            check.records_parsed = _count_hits(result)
        check.warning_groups = collector.drain_grouped()
        _report_check(check)
        section.checks.append(check)
        time.sleep(_RATE_DELAY)

    return section


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
def _print_summary(sections: list[SectionResult]) -> int:
    """Print final summary table. Returns total issue count."""
    total_warnings = sum(s.total_warnings for s in sections)
    total_distinct = sum(s.distinct_warnings for s in sections)
    total_exceptions = sum(s.total_exceptions for s in sections)
    total_records = sum(s.total_records for s in sections)
    total_issues = total_distinct + total_exceptions

    print("\n" + "=" * 72)
    print(
        f"{'Section':<35} {'Records':>8} " f"{'Warns':>6} {'Distinct':>8} {'Excpts':>6}"
    )
    print("-" * 72)
    for s in sections:
        marker = " *" if s.has_issues else ""
        print(
            f"  {s.name:<33} {s.total_records:>8} "
            f"{s.total_warnings:>6} {s.distinct_warnings:>8} "
            f"{s.total_exceptions:>6}{marker}"
        )
    print("-" * 72)
    print(
        f"  {'TOTAL':<33} {total_records:>8} "
        f"{total_warnings:>6} {total_distinct:>8} {total_exceptions:>6}"
    )
    print("=" * 72)

    if total_issues == 0:
        print("ALL CHECKS PASSED - no conversion warnings or exceptions detected")
    else:
        if total_distinct:
            print(
                f"WARNINGS: {total_warnings} occurrences across "
                f"{total_distinct} distinct issue(s)"
            )
        if total_exceptions:
            print(
                f"EXCEPTIONS: {total_exceptions} - "
                "runtime errors during model parsing."
            )
    print("=" * 72)
    return total_issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Conversion coverage check")
    parser.add_argument(
        "--section",
        choices=["A", "B", "C", "D"],
        help="Run only one section (A=Meilisearch, B=Directus, C=FK, D=Sweeps)",
    )
    args = parser.parse_args()

    tokens = TokenManager.get_tokens()
    client = FFBBAPIClientV2.create(
        api_bearer_token=tokens.api_token,
        meilisearch_bearer_token=tokens.meilisearch_token,
    )

    collector = WarningCollector()
    conv_logger = logging.getLogger(_CONVERTER_LOGGER)
    conv_logger.addHandler(collector)
    conv_logger.propagate = False  # prevent duplicate output to stderr

    run_sections = args.section.upper() if args.section else "ABCD"
    sections: list[SectionResult] = []

    # Discover IDs if FK resolution needed
    ids: dict[str, list] = {}
    if "C" in run_sections:
        ids = discover_ids(client, collector)

    if "A" in run_sections:
        sections.append(run_section_a(client, collector))
    if "B" in run_sections:
        sections.append(run_section_b(client, collector))
    if "C" in run_sections:
        sections.append(run_section_c(client, collector, ids))
    if "D" in run_sections:
        sections.append(run_section_d(client, collector))

    conv_logger.removeHandler(collector)
    conv_logger.propagate = True  # restore default

    total_issues = _print_summary(sections)
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
