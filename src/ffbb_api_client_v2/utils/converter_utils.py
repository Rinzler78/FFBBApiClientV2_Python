from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime, time, timedelta, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

if TYPE_CHECKING:
    from ..models.categorie_code import CategorieCode
    from ..models.phone_number import PhoneNumber

import dateutil.parser

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

logger = logging.getLogger(__name__)


def from_officiels_list(x: Any) -> list | None:
    """
    Handle officiels field which can be either:
    - A comma-separated string (old format)
    - A list of dicts (new format)
    - None
    """
    if x is None:
        return None
    if isinstance(x, list):
        return x  # Return as-is if already a list
    if isinstance(x, str):
        return [s.strip() for s in x.split(",")] if x else None
    return None


# ---------------------------------------------------------------------------
# from_TYPE helpers — direct dict-key extraction with type coercion
# ---------------------------------------------------------------------------


def from_str(obj: dict, key: str) -> str | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, str):
        return x
    try:
        return str(x)
    except (TypeError, ValueError):
        logger.warning(
            "from_str(%r): cannot convert %s to str (value: %.100r)",
            key,
            type(x).__name__,
            x,
        )
        return None


def from_int(obj: dict, key: str) -> int | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, int) and not isinstance(x, bool):
        return x
    if isinstance(x, str):
        if not x.strip():
            return None
        try:
            return int(x)
        except ValueError:
            logger.warning("from_int(%r): cannot parse %r as int", key, x)
            return None
    if isinstance(x, float):
        return int(x)
    logger.warning(
        "from_int(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_float(obj: dict, key: str) -> float | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, (float, int)) and not isinstance(x, bool):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x)
        except ValueError:
            logger.warning("from_float(%r): cannot parse %r as float", key, x)
            return None
    logger.warning(
        "from_float(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_bool(obj: dict, key: str) -> bool | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, bool):
        return x
    if isinstance(x, str):
        if x.lower() == "true":
            return True
        if x.lower() == "false":
            return False
        logger.warning("from_bool(%r): cannot parse %r as bool", key, x)
        return None
    logger.warning(
        "from_bool(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_datetime(obj: dict, key: str) -> datetime | None:
    x = obj.get(key)
    if not x:
        return None
    if isinstance(x, str):
        try:
            result: datetime = dateutil.parser.parse(x)
            return result
        except (ValueError, dateutil.parser.ParserError):
            logger.warning("from_datetime(%r): cannot parse %r as datetime", key, x)
            return None
    logger.warning(
        "from_datetime(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_time(obj: dict, key: str) -> time | None:
    x = obj.get(key)
    if not x:
        return None
    if isinstance(x, str):
        # Format HH:MM:SS (Meilisearch)
        if ":" in x:
            parts = x.split(":")
            try:
                return time(
                    int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0
                )
            except (ValueError, IndexError):
                logger.warning("from_time(%r): cannot parse %r as time", key, x)
                return None
        # Format HHMM (REST API, 4-digit)
        if x.isdigit() and len(x) == 4:
            try:
                return time(int(x[:2]), int(x[2:]))
            except ValueError:
                logger.warning("from_time(%r): cannot parse %r as time", key, x)
                return None
        logger.warning("from_time(%r): cannot parse %r as time", key, x)
        return None
    if isinstance(x, time):
        return x
    logger.warning(
        "from_time(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_duration(obj: dict, key: str) -> timedelta | None:
    """Parse a duration string like '37h00' or '6h55' into a timedelta.

    Also handles numeric values (int/float) interpreted as hours,
    and plain numeric strings.
    """
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, timedelta):
        return x
    if isinstance(x, (int, float)):
        return timedelta(hours=int(x), minutes=int((x % 1) * 60))
    if isinstance(x, str):
        x = x.strip()
        if not x:
            return None
        # Format "37h00", "6h55", "10h50"
        if "h" in x.lower():
            parts = x.lower().split("h", 1)
            try:
                hours = int(parts[0])
                minutes = int(parts[1]) if parts[1] else 0
                return timedelta(hours=hours, minutes=minutes)
            except ValueError:
                logger.warning("from_duration(%r): cannot parse %r", key, x)
                return None
        # Plain numeric string → interpret as hours
        try:
            val = float(x)
            return timedelta(hours=int(val), minutes=int((val % 1) * 60))
        except ValueError:
            logger.warning("from_duration(%r): cannot parse %r", key, x)
            return None
    logger.warning(
        "from_duration(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_timestamp(obj: dict, key: str) -> datetime | None:
    """Parse a Unix timestamp (int or numeric string) into a datetime (UTC)."""
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return datetime.fromtimestamp(x, tz=timezone.utc)
    if isinstance(x, str):
        x = x.strip()
        if not x:
            return None
        try:
            return datetime.fromtimestamp(int(x), tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            logger.warning("from_timestamp(%r): cannot parse %r as timestamp", key, x)
            return None
    logger.warning(
        "from_timestamp(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None


def from_categorie_code(obj: dict, key: str) -> CategorieCode | None:
    from ..models.categorie_code import CategorieCode

    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, str):
        return CategorieCode(x)
    return None


def from_enum(enum_class: type[EnumT], obj: dict, key: str) -> EnumT | None:
    x = obj.get(key)
    if x is None:
        return None
    try:
        return enum_class(x)
    except ValueError:
        logger.warning(
            "from_enum(%s, %r): unknown value %r",
            enum_class.__name__,
            key,
            x,
        )
        return None


def from_obj(from_dict_fn: Callable[[Any], T], obj: dict, key: str) -> T | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, dict):
        return from_dict_fn(x)
    # Directus returns FK (str/int) when field depth is shallow (*),
    # and the full object when depth is deep (*.*).
    # This should not happen if the API always uses max field depth.
    logger.warning(
        "from_obj(%r): expected dict or None, got %s",
        key,
        type(x).__name__,
    )
    return None


def from_list(item_fn: Callable[[Any], T], obj: dict, key: str) -> list[T] | None:
    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, list):
        return [item_fn(item) for item in x]
    logger.warning(
        "from_list(%r): expected list or None, got %s",
        key,
        type(x).__name__,
    )
    return None


def from_uuid(obj: dict, key: str) -> UUID | None:
    x = obj.get(key)
    if not x:
        return None
    try:
        return UUID(x) if isinstance(x, str) else None
    except ValueError:
        logger.warning("from_uuid(%r): invalid UUID %r", key, x)
        return None


def from_phone(obj: dict, key: str) -> PhoneNumber | None:
    """Parse a phone number string into a PhoneNumber (normalized digits + '+')."""
    from ..models.phone_number import PhoneNumber

    x = obj.get(key)
    if x is None:
        return None
    if isinstance(x, str):
        if not x.strip():
            return None
        return PhoneNumber(x)
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return PhoneNumber(str(int(x)))
    logger.warning(
        "from_phone(%r): unexpected type %s (value: %.100r)",
        key,
        type(x).__name__,
        x,
    )
    return None
