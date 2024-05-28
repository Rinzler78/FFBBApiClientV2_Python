from dataclasses import dataclass
from typing import Any, Optional

from .competition import Competition
from .converters import from_none, from_str, from_union, is_type, to_class
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .salle import Salle


@dataclass
class ExternalID:
    nom_equipe1: Optional[str] = None
    nom_equipe2: Optional[str] = None
    numero_journee: Optional[int] = None
    competition_id: Optional[Competition] = None
    id_organisme_equipe1: Optional[IDOrganismeEquipe] = None
    id_organisme_equipe2: Optional[IDOrganismeEquipe] = None
    salle: Optional[Salle] = None
    id_poule: Optional[IDPoule] = None

    @staticmethod
    def from_dict(obj: Any) -> "ExternalID":
        """
        Construct a new ExternalID object from a dictionary.

        Args:
            obj (Any): The input dictionary.

        Returns:
            ExternalID: The constructed ExternalID object.
        """
        assert isinstance(obj, dict)
        nom_equipe1 = from_union([from_str, from_none], obj.get("nomEquipe1"))
        nom_equipe2 = from_union([from_str, from_none], obj.get("nomEquipe2"))
        numero_journee = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("numeroJournee")
        )
        competition_id = from_union(
            [Competition.from_dict, from_none], obj.get("competitionId")
        )
        id_organisme_equipe1 = from_union(
            [IDOrganismeEquipe.from_dict, from_none], obj.get("idOrganismeEquipe1")
        )
        id_organisme_equipe2 = from_union(
            [IDOrganismeEquipe.from_dict, from_none], obj.get("idOrganismeEquipe2")
        )
        salle = from_union([Salle.from_dict, from_none], obj.get("salle"))
        id_poule = from_union([IDPoule.from_dict, from_none], obj.get("idPoule"))
        return ExternalID(
            nom_equipe1,
            nom_equipe2,
            numero_journee,
            competition_id,
            id_organisme_equipe1,
            id_organisme_equipe2,
            salle,
            id_poule,
        )

    def to_dict(self) -> dict:
        """
        Convert the ExternalID object to a dictionary.

        Returns:
            dict: The converted dictionary.
        """
        result: dict = {}
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = from_union([from_str, from_none], self.nom_equipe1)
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = from_union([from_str, from_none], self.nom_equipe2)
        if self.numero_journee is not None:
            result["numeroJournee"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.numero_journee,
            )
        if self.competition_id is not None:
            result["competitionId"] = from_union(
                [lambda x: to_class(Competition, x), from_none], self.competition_id
            )
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe, x), from_none],
                self.id_organisme_equipe1,
            )
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = from_union(
                [lambda x: to_class(IDOrganismeEquipe, x), from_none],
                self.id_organisme_equipe2,
            )
        if self.salle is not None:
            result["salle"] = from_union(
                [lambda x: to_class(Salle, x), from_none], self.salle
            )
        if self.id_poule is not None:
            result["idPoule"] = from_union(
                [lambda x: to_class(IDPoule, x), from_none], self.id_poule
            )
        return result
