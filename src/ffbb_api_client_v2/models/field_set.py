from enum import Enum


class FieldSet(Enum):
    """Enum for different field sets."""

    BASIC = "basic"
    DEFAULT = "default"
    DETAILED = "detailed"
    WILDCARD = "wildcard"
