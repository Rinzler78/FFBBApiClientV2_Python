from __future__ import annotations

from datetime import datetime
from typing import Any

from ..utils.converter_utils import (
    from_comma_separated_list,
    from_datetime,
    from_dict,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
)
from .CompetitionID import CompetitionID
from .CompetitionIDSexe import CompetitionIDSexe
from .CompetitionIDTypeCompetition import CompetitionIDTypeCompetition
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Geo import Geo
from .Hit import Hit
from .IDEngagementEquipe import IDEngagementEquipe
from .IDOrganismeEquipe import IDOrganismeEquipe
from .IDPoule import IDPoule
from .Niveau import Niveau
from .NiveauClass import NiveauClass
from .Organisateur import Organisateur
from .Pratique import Pratique
from .Saison import Saison
from .salle import Salle


class RencontresFacetDistribution(FacetDistribution):
    competition_id_categorie_code: dict[str, int] | None = None
    competition_id_nom_extended: dict[str, int] | None = None
    competition_id_sexe: CompetitionIDSexe | None = None
    competition_id_type_competition: CompetitionIDTypeCompetition | None = None
    niveau: Niveau | None = None
    organisateur_id: dict[str, int] | None = None
    organisateur_nom: dict[str, int] | None = None

    def __init__(
        self,
        competition_id_categorie_code: dict[str, int] | None,
        competition_id_nom_extended: dict[str, int] | None,
        competition_id_sexe: CompetitionIDSexe | None,
        competition_id_type_competition: CompetitionIDTypeCompetition | None,
        niveau: Niveau | None,
        organisateur_id: dict[str, int] | None,
        organisateur_nom: dict[str, int] | None,
    ):
        self.competition_id_categorie_code = competition_id_categorie_code
        self.competition_id_nom_extended = competition_id_nom_extended
        self.competition_id_sexe = competition_id_sexe
        self.competition_id_type_competition = competition_id_type_competition
        self.niveau = niveau
        self.organisateur_id = organisateur_id
        self.organisateur_nom = organisateur_nom

    @staticmethod
    def from_dict(obj: Any) -> RencontresFacetDistribution:
        assert isinstance(obj, dict)
        competition_id_categorie_code = from_union(
            [lambda x: from_dict(from_int, x), from_none],
            obj.get("competitionId.categorie.code"),
        )
        competition_id_nom_extended = from_union(
            [lambda x: from_dict(from_int, x), from_none],
            obj.get("competitionId.nomExtended"),
        )
        competition_id_sexe = from_union(
            [CompetitionIDSexe.from_dict, from_none], obj.get("competitionId.sexe")
        )
        competition_id_type_competition = from_union(
            [CompetitionIDTypeCompetition.from_dict, from_none],
            obj.get("competitionId.typeCompetition"),
        )
        niveau = from_union([NiveauClass.from_dict, from_none], obj.get("niveau"))
        organisateur_id = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("organisateur.id")
        )
        organisateur_nom = from_union(
            [lambda x: from_dict(from_int, x), from_none], obj.get("organisateur.nom")
        )
        return RencontresFacetDistribution(
            competition_id_categorie_code,
            competition_id_nom_extended,
            competition_id_sexe,
            competition_id_type_competition,
            niveau,
            organisateur_id,
            organisateur_nom,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.competition_id_categorie_code is not None:
            result["competitionId.categorie.code"] = from_union(
                [lambda x: from_dict(from_int, x), from_none],
                self.competition_id_categorie_code,
            )
        if self.competition_id_nom_extended is not None:
            result["competitionId.nomExtended"] = from_union(
                [lambda x: from_dict(from_int, x), from_none],
                self.competition_id_nom_extended,
            )
        if self.competition_id_sexe is not None:
            result["competitionId.sexe"] = from_union(
                [lambda x: to_class(CompetitionIDSexe, x), from_none],
                self.competition_id_sexe,
            )
        if self.competition_id_type_competition is not None:
            result["competitionId.typeCompetition"] = from_union(
                [lambda x: to_class(CompetitionIDTypeCompetition, x), from_none],
                self.competition_id_type_competition,
            )
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_enum(Niveau, x), from_none], self.niveau
            )
        if self.organisateur_id is not None:
            result["organisateur.id"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.organisateur_id
            )
        if self.organisateur_nom is not None:
            result["organisateur.nom"] = from_union(
                [lambda x: from_dict(from_int, x), from_none], self.organisateur_nom
            )
        return result


# class LibelleEnum(Enum):
#     SE = "SE"
#     SENIORS = "Seniors"
#     U11 = "U11"
#     U13 = "U13"
#     U15 = "U15"
#     U17 = "U17"
#     U18 = "U18"
#     U20 = "U20"
#     U7 = "U7"
#     U9 = "U9"
#     VE = "VE"
#     VÉTÉRANS = "Vétérans"


class Engagement:
    id: str | None = None

    def __init__(self, id: str | None):
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> Engagement:
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        return Engagement(id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        return result


class RencontresHit(Hit):
    niveau: Niveau | None = None
    id: str | None = None
    date: datetime | None = None
    date_rencontre: datetime | None = None
    horaire: int | None = None
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    pratique: Pratique | None = None
    gs_id: str
    officiels: list[str] | None = None
    competition_id: CompetitionID | None = None
    id_organisme_equipe1: IDOrganismeEquipe | None = None
    id_organisme_equipe2: IDOrganismeEquipe | None = None
    id_poule: IDPoule | None = None
    saison: Saison | None = None
    salle: Salle | None = None
    id_engagement_equipe1: IDEngagementEquipe | None = None
    id_engagement_equipe2: IDEngagementEquipe | None = None
    geo: Geo | None = None
    date_timestamp: int | None = None
    date_rencontre_timestamp: int | None = None
    creation_timestamp: int | None = None
    date_saisie_resultat_timestamp: None
    modification_timestamp: int | None = None
    thumbnail: None
    organisateur: Organisateur | None = None
    niveau_nb: int | None = None

    def __init__(
        self,
        niveau: Niveau | None,
        id: str | None,
        date: datetime | None,
        date_rencontre: datetime | None,
        horaire: int | None,
        nom_equipe1: str | None,
        nom_equipe2: str | None,
        numero_journee: int | None,
        pratique: Pratique | None,
        gs_id: str,
        officiels: list[str] | None,
        competition_id: CompetitionID | None,
        id_organisme_equipe1: IDOrganismeEquipe | None,
        id_organisme_equipe2: IDOrganismeEquipe | None,
        id_poule: IDPoule | None,
        saison: Saison | None,
        salle: Salle | None,
        id_engagement_equipe1: IDEngagementEquipe | None,
        id_engagement_equipe2: IDEngagementEquipe | None,
        geo: Geo | None,
        date_timestamp: int | None,
        date_rencontre_timestamp: int | None,
        creation_timestamp: int | None,
        date_saisie_resultat_timestamp: None,
        modification_timestamp: int | None,
        thumbnail: None,
        organisateur: Organisateur | None,
        niveau_nb: int | None,
    ):
        self.niveau = niveau
        self.id = id
        self.lower_id = id.lower() if id else None

        self.date = date
        self.date_rencontre = date_rencontre
        self.horaire = horaire
        self.nom_equipe1 = nom_equipe1
        self.nom_equipe2 = nom_equipe2
        self.lower_nom_equipe1 = nom_equipe1.lower() if nom_equipe1 else None
        self.lower_nom_equipe2 = nom_equipe2.lower() if nom_equipe2 else None

        self.numero_journee = numero_journee
        self.pratique = pratique
        self.gs_id = gs_id
        self.lower_gs_id = gs_id.lower() if gs_id else None

        self.officiels = officiels
        self.lower_officiels = [o.lower() for o in officiels] if officiels else None

        self.competition_id = competition_id
        self.id_organisme_equipe1 = id_organisme_equipe1
        self.id_organisme_equipe2 = id_organisme_equipe2
        self.id_poule = id_poule
        self.saison = saison
        self.salle = salle
        self.id_engagement_equipe1 = id_engagement_equipe1
        self.id_engagement_equipe2 = id_engagement_equipe2
        self.geo = geo
        self.date_timestamp = date_timestamp
        self.date_rencontre_timestamp = date_rencontre_timestamp
        self.creation_timestamp = creation_timestamp
        self.date_saisie_resultat_timestamp = date_saisie_resultat_timestamp
        self.modification_timestamp = modification_timestamp
        self.thumbnail = thumbnail
        self.organisateur = organisateur
        self.niveau_nb = niveau_nb

    @staticmethod
    def from_dict(obj: Any) -> Hit:
        try:
            assert isinstance(obj, dict)
            niveau = from_union([Niveau, from_none], obj.get("niveau"))
            id = from_union([from_str, from_none], obj.get("id"))
            date = from_union([from_datetime, from_none], obj.get("date"))
            date_rencontre = from_union(
                [from_datetime, from_none], obj.get("date_rencontre")
            )
            horaire = from_union(
                [from_none, lambda x: int(from_str(x))], obj.get("horaire")
            )
            nom_equipe1 = from_union([from_str, from_none], obj.get("nomEquipe1"))
            nom_equipe2 = from_union([from_str, from_none], obj.get("nomEquipe2"))

            numero_journee_tmp = obj.get("numeroJournee")
            numero_journee_tmp = (
                numero_journee_tmp if len(numero_journee_tmp) > 0 else None
            )

            numero_journee = from_union(
                [from_none, lambda x: int(from_str(x))], numero_journee_tmp
            )
            pratique = from_union([from_none, Pratique], obj.get("pratique"))
            gs_id = from_union([from_str, from_none], obj.get("gsId"))
            officiels = from_union(
                [from_comma_separated_list, from_none], obj.get("officiels")
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
            id_poule = from_union([IDPoule.from_dict, from_none], obj.get("idPoule"))
            saison = from_union([Saison.from_dict, from_none], obj.get("saison"))
            salle = from_union([Salle.from_dict, from_none], obj.get("salle"))
            id_engagement_equipe1 = from_union(
                [IDEngagementEquipe.from_dict, from_none],
                obj.get("idEngagementEquipe1"),
            )
            id_engagement_equipe2 = from_union(
                [IDEngagementEquipe.from_dict, from_none],
                obj.get("idEngagementEquipe2"),
            )
            geo = from_union([Geo.from_dict, from_none], obj.get("_geo"))
            date_timestamp = from_union(
                [from_int, from_none], obj.get("date_timestamp")
            )
            date_rencontre_timestamp = from_union(
                [from_int, from_none], obj.get("date_rencontre_timestamp")
            )
            creation_timestamp = from_union(
                [from_int, from_none], obj.get("creation_timestamp")
            )
            date_saisie_resultat_timestamp = from_union(
                [from_int, from_none], obj.get("dateSaisieResultat_timestamp")
            )
            modification_timestamp = from_union(
                [from_int, from_none], obj.get("modification_timestamp")
            )
            thumbnail = from_none(obj.get("thumbnail"))
            organisateur = from_union(
                [Organisateur.from_dict, from_none], obj.get("organisateur")
            )
            niveau_nb = from_union(
                [from_none, lambda x: int(from_str(x))], obj.get("niveau_nb")
            )
            return RencontresHit(
                niveau,
                id,
                date,
                date_rencontre,
                horaire,
                nom_equipe1,
                nom_equipe2,
                numero_journee,
                pratique,
                gs_id,
                officiels,
                competition_id,
                id_organisme_equipe1,
                id_organisme_equipe2,
                id_poule,
                saison,
                salle,
                id_engagement_equipe1,
                id_engagement_equipe2,
                geo,
                date_timestamp,
                date_rencontre_timestamp,
                creation_timestamp,
                date_saisie_resultat_timestamp,
                modification_timestamp,
                thumbnail,
                organisateur,
                niveau_nb,
            )
        except Exception as e:
            raise ValueError(f"Invalid `Hit` object: {e}")

    def to_dict(self) -> dict:
        result: dict = {}
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_enum(Niveau, x), from_none], self.niveau
            )
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.date is not None:
            result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        if self.date_rencontre is not None:
            result["date_rencontre"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_rencontre
            )
        if self.horaire is not None:
            result["horaire"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.horaire,
            )
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
        if self.pratique is not None:
            result["pratique"] = from_union(
                [from_none, lambda x: to_enum(Pratique, x)], self.pratique
            )
        if self.gs_id is not None:
            result["gsId"] = from_union([from_str, from_none], self.gs_id)
        if self.officiels is not None:
            result["officiels"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.officiels
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
        if self.id_poule is not None:
            result["idPoule"] = from_union(
                [lambda x: to_class(IDPoule, x), from_none], self.id_poule
            )
        if self.saison is not None:
            result["saison"] = from_union(
                [lambda x: to_class(Saison, x), from_none], self.saison
            )
        if self.salle is not None:
            result["salle"] = from_union(
                [lambda x: to_class(Salle, x), from_none], self.salle
            )
        if self.id_engagement_equipe1 is not None:
            result["idEngagementEquipe1"] = from_union(
                [lambda x: to_class(IDEngagementEquipe, x), from_none],
                self.id_engagement_equipe1,
            )
        if self.id_engagement_equipe2 is not None:
            result["idEngagementEquipe2"] = from_union(
                [lambda x: to_class(IDEngagementEquipe, x), from_none],
                self.id_engagement_equipe2,
            )
        if self.geo is not None:
            result["_geo"] = from_union(
                [lambda x: to_class(Geo, x), from_none], self.geo
            )
        if self.date_timestamp is not None:
            result["date_timestamp"] = from_union(
                [from_int, from_none], self.date_timestamp
            )
        if self.date_rencontre_timestamp is not None:
            result["date_rencontre_timestamp"] = from_union(
                [from_int, from_none], self.date_rencontre_timestamp
            )
        if self.creation_timestamp is not None:
            result["creation_timestamp"] = from_union(
                [from_int, from_none], self.creation_timestamp
            )
        if self.date_saisie_resultat_timestamp is not None:
            result["dateSaisieResultat_timestamp"] = from_none(
                self.date_saisie_resultat_timestamp
            )
        if self.modification_timestamp is not None:
            result["modification_timestamp"] = from_union(
                [from_int, from_none], self.modification_timestamp
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_none(self.thumbnail)
        if self.organisateur is not None:
            result["organisateur"] = from_union(
                [lambda x: to_class(Organisateur, x), from_none], self.organisateur
            )
        if self.niveau_nb is not None:
            result["niveau_nb"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.niveau_nb,
            )
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return (
            not query
            or (self.lower_gs_id and query in self.lower_gs_id)
            or (self.lower_id and query in self.lower_id)
            or (self.lower_officiels and query in self.lower_officiels)
            or (
                self.salle
                and (
                    (self.salle.lower_adresse and query in self.salle.lower_adresse)
                    or (
                        self.salle.lower_adresse_complement
                        and query in self.salle.lower_adresse
                    )
                    or (self.salle.lower_libelle and query in self.salle.lower_libelle)
                )
            )
        )


class RencontresFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> RencontresFacetStats:
        return RencontresFacetStats()

    def to_dict(self) -> dict:
        super().to_dict()
