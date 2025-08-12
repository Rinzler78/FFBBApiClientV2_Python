from __future__ import annotations

from typing import Any

from ..utils.converter_utils import from_none, from_str, from_union, is_type, to_class
from .IDOrganismeEquipe import IDOrganismeEquipe
from .IDPoule import IDPoule
from .salle import Salle


class CompetitionID:
    code: str | None = None
    nom: str | None = None
    sexe: str | None = None
    type_competition: str | None = None

    def __init__(
        self,
        code: str | None,
        nom: str | None,
        sexe: str | None,
        type_competition: str | None,
    ) -> None:
        self.code = code
        self.nom = nom
        self.sexe = sexe
        self.type_competition = type_competition

    @staticmethod
    def from_dict(obj: Any) -> CompetitionID:
        assert isinstance(obj, dict)
        code = from_union([from_str, from_none], obj.get("code"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        sexe = from_union([from_str, from_none], obj.get("sexe"))
        type_competition = from_union([from_str, from_none], obj.get("typeCompetition"))
        return CompetitionID(code, nom, sexe, type_competition)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.sexe is not None:
            result["sexe"] = from_union([from_str, from_none], self.sexe)
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [from_str, from_none], self.type_competition
            )
        return result


class ExternalID:
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    competition_id: CompetitionID | None = None
    id_organisme_equipe1: IDOrganismeEquipe | None = None
    id_organisme_equipe2: IDOrganismeEquipe | None = None
    salle: Salle | None = None
    id_poule: IDPoule | None = None

    def __init__(
        self,
        nom_equipe1: str | None,
        nom_equipe2: str | None,
        numero_journee: int | None,
        competition_id: CompetitionID | None,
        id_organisme_equipe1: IDOrganismeEquipe | None,
        id_organisme_equipe2: IDOrganismeEquipe | None,
        salle: Salle | None,
        id_poule: IDPoule | None,
    ) -> None:
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.numero_journee = numero_journee
        self.competition_id = competition_id
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.salle = salle
        self.id_poule = id_poule

    @staticmethod
    def from_dict(obj: Any) -> ExternalID:
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
            [lambda x: int(from_str(x)), from_none], obj.get("numeroJournee")
        )
        competition_id = from_union(
            [CompetitionID.from_dict, from_none], obj.get("competitionId")
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
                [lambda x: to_class(CompetitionID, x), from_none], self.competition_id
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
