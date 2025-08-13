from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any, TypeVar, cast
from uuid import UUID

import dateutil.parser

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    """
    Convert None to Any.
    """
    assert x is None
    return x


def from_str(x: Any) -> str:
    """
    Convert string to str.
    """
    assert isinstance(x, str)
    return x


def from_union(fs, x) -> Any:
    """
    Convert union of functions to Any.
    """
    for f in fs:
        try:
            return f(x)
        except AssertionError:
            pass
        except Exception:
            # Silent failure is expected when trying different type conversions
            pass
    assert False


def from_float(x: Any) -> float:
    """
    Convert float or int to float.
    """
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def is_type(t: type[T], x: Any) -> T:
    """
    Check if x is of type t.
    """
    assert isinstance(x, t)
    return x


def to_float(x: Any) -> float:
    """
    Convert Any to float.
    """
    assert isinstance(x, float)
    return x


def from_int(x: Any) -> int:
    """
    Convert int to int.
    """
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_stringified_bool(x: str) -> bool:
    """
    Convert stringified bool to bool.
    """
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def from_datetime(x: Any) -> datetime | None:
    """
    Convert string to datetime.
    """
    return dateutil.parser.parse(x) if x else None


def to_class(c: type[T], x: Any) -> dict:
    """
    Convert Any to dictionary representation of class c.
    """
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    """
    Convert bool to bool.
    """
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> list[T]:
    """
    Convert list to list of type T.
    """
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_dict(f: Callable[[Any], T], x: Any) -> dict[str, T]:
    """
    Convert dict to dict of type T.
    """
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


def to_enum(c: type[EnumT], x: Any) -> EnumT:
    """
    Convert Any to EnumT.
    """
    assert isinstance(x, c)
    return x.value


def from_uuid(x: Any) -> UUID | None:
    """
    Convert Any to UUID.
    """
    return UUID(x) if x else None


def from_comma_separated_list(x: Any) -> list[str] | None:
    """
    Convert comma separated list to list of strings.
    """
    return [s.strip() for s in x.split(",")] if x else None
