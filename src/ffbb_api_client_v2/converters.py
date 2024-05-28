from datetime import datetime
from typing import Any, Callable, List, Type, TypeVar, cast

import dateutil.parser

T = TypeVar("T")


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
        except Exception:
            pass
    assert False


def from_float(x: Any) -> float:
    """
    Convert float or int to float.
    """
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def is_type(t: Type[T], x: Any) -> T:
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


def from_datetime(x: Any) -> datetime:
    """
    Convert string to datetime.
    """
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    """
    Convert list to list of type T.
    """
    assert isinstance(x, list)
    return [f(y) for y in x]
