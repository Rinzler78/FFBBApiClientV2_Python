from __future__ import annotations

import re

_STRIP_RE = re.compile(r"[^0-9+]")


class PhoneNumber(str):
    """Normalized phone number (digits and '+' only).

    Stores the cleaned form as the string value.
    Provides helpers for French phone formatting.
    """

    _raw: str

    def __new__(cls, raw: str) -> PhoneNumber:
        normalized = _STRIP_RE.sub("", raw.strip())
        instance = super().__new__(cls, normalized)
        instance._raw = raw
        return instance

    @property
    def raw(self) -> str:
        """Original value before normalization."""
        return self._raw

    @property
    def is_french(self) -> bool:
        """True if this looks like a French phone number."""
        return (self.startswith("0") and len(self) == 10) or (
            self.startswith("+33") and len(self) == 12
        )

    @property
    def international(self) -> str:
        """Return +33 international format for French numbers, self otherwise."""
        if self.startswith("0") and len(self) == 10:
            return "+33" + self[1:]
        return str(self)

    @property
    def formatted(self) -> str:
        """Human-readable French format: 'XX XX XX XX XX'."""
        local: str = str(self)
        if self.startswith("+33") and len(self) == 12:
            local = "0" + self[3:]
        if local.startswith("0") and len(local) == 10:
            return " ".join(local[i : i + 2] for i in range(0, 10, 2))
        return local
