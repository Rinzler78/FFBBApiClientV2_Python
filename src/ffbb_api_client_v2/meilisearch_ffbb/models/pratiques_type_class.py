from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...utils.converter_utils import from_int


@dataclass
class PratiquesTypeClass:
    basket_inclusif: int | None = None
    basket_santé: int | None = None
    basket_tonik: int | None = None
    centre_génération_basket: int | None = None
    micro_basket: int | None = None

    @staticmethod
    def from_dict(obj: Any) -> PratiquesTypeClass:
        assert isinstance(obj, dict)
        basket_inclusif = from_int(obj, "Basket Inclusif")
        basket_santé = from_int(obj, "Basket Santé")
        basket_tonik = from_int(obj, "Basket Tonik")
        centre_génération_basket = from_int(obj, "Centre Génération Basket")
        micro_basket = from_int(obj, "Micro Basket")
        return PratiquesTypeClass(
            basket_inclusif=basket_inclusif,
            basket_santé=basket_santé,
            basket_tonik=basket_tonik,
            centre_génération_basket=centre_génération_basket,
            micro_basket=micro_basket,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.basket_inclusif is not None:
            result["Basket Inclusif"] = self.basket_inclusif
        if self.basket_santé is not None:
            result["Basket Santé"] = self.basket_santé
        if self.basket_tonik is not None:
            result["Basket Tonik"] = self.basket_tonik
        if self.centre_génération_basket is not None:
            result["Centre Génération Basket"] = self.centre_génération_basket
        if self.micro_basket is not None:
            result["Micro Basket"] = self.micro_basket
        return result
