from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_int, from_none, from_union


class Labellisation:
    basket_santé_résolutions: int | None = None
    micro_basket: int | None = None

    def __init__(
        self,
        basket_santé_résolutions: int | None,
        micro_basket: int | None,
    ) -> None:
        self.basket_santé_résolutions = basket_santé_résolutions
        self.micro_basket = micro_basket

    @staticmethod
    def from_dict(obj: Any) -> Labellisation:
        assert isinstance(obj, dict)
        basket_santé_résolutions = from_union(
            [from_int, from_none], obj.get("Basket Santé / Résolutions")
        )
        micro_basket = from_union([from_int, from_none], obj.get("Micro Basket"))
        return Labellisation(basket_santé_résolutions, micro_basket)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_santé_résolutions is not None:
            result["Basket Santé / Résolutions"] = from_union(
                [from_int, from_none], self.basket_santé_résolutions
            )
        if self.micro_basket is not None:
            result["Micro Basket"] = from_union(
                [from_int, from_none], self.micro_basket
            )
        return result
