from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..utils.converter_utils import from_enum, from_str
from .code_fonction import CodeFonction


@dataclass
class Membre:
    id: str | None = None
    nom: str | None = None
    prenom: str | None = None
    adresse1: str | None = None
    adresse2: str | None = None
    code_postal: str | None = None
    ville: str | None = None
    mail: str | None = None
    telephone_fixe: str | None = None
    telephone_portable: str | None = None
    code_fonction: CodeFonction | None = None

    @staticmethod
    def from_dict(obj: Any) -> Membre:
        assert isinstance(obj, dict)
        return Membre(
            id=from_str(obj, "id"),
            nom=from_str(obj, "nom"),
            prenom=from_str(obj, "prenom"),
            adresse1=from_str(obj, "adresse1"),
            adresse2=from_str(obj, "adresse2"),
            code_postal=from_str(obj, "codePostal"),
            ville=from_str(obj, "ville"),
            mail=from_str(obj, "mail"),
            telephone_fixe=from_str(obj, "telephoneFixe"),
            telephone_portable=from_str(obj, "telephonePortable"),
            code_fonction=from_enum(CodeFonction, obj, "codeFonction"),
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.prenom is not None:
            result["prenom"] = self.prenom
        if self.adresse1 is not None:
            result["adresse1"] = self.adresse1
        if self.adresse2 is not None:
            result["adresse2"] = self.adresse2
        if self.code_postal is not None:
            result["codePostal"] = self.code_postal
        if self.ville is not None:
            result["ville"] = self.ville
        if self.mail is not None:
            result["mail"] = self.mail
        if self.telephone_fixe is not None:
            result["telephoneFixe"] = self.telephone_fixe
        if self.telephone_portable is not None:
            result["telephonePortable"] = self.telephone_portable
        if self.code_fonction is not None:
            result["codeFonction"] = self.code_fonction.value
        return result
