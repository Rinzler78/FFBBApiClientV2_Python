from typing import Any, Optional

from .Cartographie import Cartographie
from .converters import from_none, from_str, from_union, to_class


class Salle:
    id: Optional[str] = None
    libelle: Optional[str] = None
    adresse: Optional[str] = None
    adresse_complement: Optional[str] = None
    cartographie: Optional[Cartographie] = None

    def __init__(
        self,
        id: Optional[str],
        libelle: Optional[str],
        adresse: Optional[str],
        adresse_complement: Optional[str],
        cartographie: Optional[Cartographie],
    ) -> None:
        self.id = id
        self.libelle = libelle
        self.lower_libelle = libelle.lower() if libelle else None

        self.adresse = adresse
        self.lower_adresse = adresse.lower() if adresse else None

        self.adresse_complement = adresse_complement
        self.lower_adresse_complement = (
            adresse_complement.lower() if adresse_complement else None
        )
        self.cartographie = cartographie

    @staticmethod
    def from_dict(obj: Any) -> "Salle":
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        libelle = from_union([from_str, from_none], obj.get("libelle"))
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        adresse_complement = from_union(
            [from_str, from_none], obj.get("adresseComplement")
        )
        cartographie = from_union(
            [Cartographie.from_dict, from_none], obj.get("cartographie")
        )
        return Salle(id, libelle, adresse, adresse_complement, cartographie)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.libelle is not None:
            result["libelle"] = from_union([from_str, from_none], self.libelle)
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.adresse_complement is not None:
            result["adresseComplement"] = from_union(
                [from_str, from_none], self.adresse_complement
            )
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [lambda x: to_class(Cartographie, x), from_none], self.cartographie
            )
        return result
