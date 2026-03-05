from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_int


@dataclass
class Labellisation:
    basket_santé_résolutions: int | None = None
    micro_basket: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> Labellisation:
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, got {obj.__class__.__name__}")
        basket_santé_résolutions = from_int(obj, "Basket Santé / Résolutions")
        micro_basket = from_int(obj, "Micro Basket")
        return Labellisation(
            basket_santé_résolutions=basket_santé_résolutions,
            micro_basket=micro_basket,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_santé_résolutions is not None:
            result["Basket Santé / Résolutions"] = self.basket_santé_résolutions
        if self.micro_basket is not None:
            result["Micro Basket"] = self.micro_basket
        return result
