from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..utils.converter_utils import from_obj, from_str
from .cartographie import Cartographie
from .commune import Commune


@dataclass
class Salle:
    id: str | None = None
    numero: str | None = None
    libelle: str | None = None
    libelle2: str | None = None
    adresse: str | None = None
    adresse_complement: str | None = None
    commune: Commune | None = None
    cartographie: Cartographie | None = None
    lower_libelle: str | None = field(init=False, default=None, repr=False)
    lower_adresse: str | None = field(init=False, default=None, repr=False)
    lower_adresse_complement: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_libelle = self.libelle.lower() if self.libelle else None
        self.lower_adresse = self.adresse.lower() if self.adresse else None
        self.lower_adresse_complement = (
            self.adresse_complement.lower() if self.adresse_complement else None
        )

    @staticmethod
    def from_dict(obj: Any) -> Salle:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        numero = from_str(obj, "numero")
        libelle = from_str(obj, "libelle")
        libelle2 = from_str(obj, "libelle2")
        adresse = from_str(obj, "adresse")
        adresse_complement = from_str(obj, "adresseComplement")
        commune = from_obj(Commune.from_dict, obj, "commune")
        cartographie = from_obj(Cartographie.from_dict, obj, "cartographie")
        return Salle(
            id=id,
            numero=numero,
            libelle=libelle,
            libelle2=libelle2,
            adresse=adresse,
            adresse_complement=adresse_complement,
            commune=commune,
            cartographie=cartographie,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.numero is not None:
            result["numero"] = self.numero
        if self.libelle is not None:
            result["libelle"] = self.libelle
        if self.libelle2 is not None:
            result["libelle2"] = self.libelle2
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.adresse_complement is not None:
            result["adresseComplement"] = self.adresse_complement
        if self.commune is not None:
            result["commune"] = self.commune.to_dict()
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie.to_dict()
        return result
