from datetime import datetime
from typing import Any, Dict, List, Optional

from .Categorie import Categorie
from .CompetitionIDSexe import CompetitionIDSexe
from .CompetitionIDTypeCompetition import CompetitionIDTypeCompetition
from .converters import (
    from_bool,
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
from .Etat import Etat
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Hit import Hit
from .logo import Logo
from .Niveau import Niveau
from .NiveauClass import NiveauClass
from .Organisateur import Organisateur
from .PhaseCode import PhaseCode
from .Poule import Poule
from .PublicationInternet import PublicationInternet
from .Saison import Saison
from .Sexe import Sexe
from .TypeCompetition import TypeCompetition
from .TypeCompetitionGenerique import TypeCompetitionGenerique


class CompetitionsFacetDistribution(FacetDistribution):
    competition_id_categorie_code: Optional[Dict[str, int]] = None
    competition_id_nom_extended: Optional[Dict[str, int]] = None
    competition_id_sexe: Optional[CompetitionIDSexe] = None
    competition_id_type_competition: Optional[CompetitionIDTypeCompetition] = None
    niveau: Optional[NiveauClass] = None
    organisateur_id: Optional[Dict[str, int]] = None
    organisateur_nom: Optional[Dict[str, int]] = None

    def __init__(
        self,
        competition_id_categorie_code: Optional[Dict[str, int]],
        competition_id_nom_extended: Optional[Dict[str, int]],
        competition_id_sexe: Optional[CompetitionIDSexe],
        competition_id_type_competition: Optional[CompetitionIDTypeCompetition],
        niveau: Optional[NiveauClass],
        organisateur_id: Optional[Dict[str, int]],
        organisateur_nom: Optional[Dict[str, int]],
    ) -> None:
        self.competition_id_categorie_code = competition_id_categorie_code
        self.competition_id_nom_extended = competition_id_nom_extended
        self.competition_id_sexe = competition_id_sexe
        self.competition_id_type_competition = competition_id_type_competition
        self.niveau = niveau
        self.organisateur_id = organisateur_id
        self.organisateur_nom = organisateur_nom

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionsFacetDistribution":
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
        return CompetitionsFacetDistribution(
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
                [lambda x: to_class(NiveauClass, x), from_none], self.niveau
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


class CompetitionsHit(Hit):
    nom: Optional[str] = None
    code: Optional[str] = None
    niveau: Optional[Niveau] = None
    type_competition: Optional[TypeCompetition] = None
    sexe: Optional[Sexe] = None
    id: Optional[str] = None
    creation_en_cours: Optional[bool] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    emarque_v2: Optional[bool] = None
    live_stat: Optional[bool] = None
    publication_internet: Optional[PublicationInternet] = None
    pro: Optional[bool] = None
    competition_origine: Optional[str] = None
    competition_origine_niveau: Optional[int] = None
    phase_code: Optional[PhaseCode] = None
    competition_origine_nom: Optional[str] = None
    etat: Optional[Etat] = None
    poules: Optional[List[Poule]] = None
    phases: Optional[List[str]] = None
    categorie: Optional[Categorie] = None
    id_competition_pere: None
    organisateur: Optional[Organisateur] = None
    saison: Optional[Saison] = None
    logo: Optional[Logo] = None
    type_competition_generique: Optional[TypeCompetitionGenerique] = None
    thumbnail: Optional[str] = None
    niveau_nb: Optional[int] = None

    def __init__(
        self,
        nom: Optional[str],
        code: Optional[str],
        niveau: Optional[Niveau],
        type_competition: Optional[TypeCompetition],
        sexe: Optional[Sexe],
        id: Optional[str],
        creation_en_cours: Optional[bool],
        date_created: Optional[datetime],
        date_updated: Optional[datetime],
        emarque_v2: Optional[bool],
        live_stat: Optional[bool],
        publication_internet: Optional[PublicationInternet],
        pro: Optional[bool],
        competition_origine: Optional[str],
        competition_origine_niveau: Optional[int],
        phase_code: Optional[PhaseCode],
        competition_origine_nom: Optional[str],
        etat: Optional[Etat],
        poules: Optional[List[Poule]],
        phases: Optional[List[str]],
        categorie: Optional[Categorie],
        id_competition_pere: None,
        organisateur: Optional[Organisateur],
        saison: Optional[Saison],
        logo: Optional[Logo],
        type_competition_generique: Optional[TypeCompetitionGenerique],
        thumbnail: Optional[str],
        niveau_nb: Optional[int],
    ) -> None:
        self.nom = nom
        self.lower_nom = nom.lower() if nom else None

        self.code = code
        self.lower_code = code.lower() if code else None

        self.niveau = niveau
        self.type_competition = type_competition
        self.sexe = sexe
        self.id = id
        self.lower_id = id.lower() if id else None

        self.creation_en_cours = creation_en_cours
        self.date_created = date_created
        self.date_updated = date_updated
        self.emarque_v2 = emarque_v2
        self.live_stat = live_stat
        self.publication_internet = publication_internet
        self.pro = pro
        self.competition_origine = competition_origine
        self.lower_competition_origine = (
            competition_origine.lower() if competition_origine else None
        )

        self.competition_origine_niveau = competition_origine_niveau
        self.competition_origine_nom = competition_origine_nom
        self.lower_competition_origine_nom = (
            competition_origine_nom.lower() if competition_origine_nom else None
        )

        self.phase_code = phase_code
        self.etat = etat
        self.poules = poules
        self.phases = phases
        self.categorie = categorie
        self.id_competition_pere = id_competition_pere
        self.organisateur = organisateur
        self.saison = saison
        self.logo = logo
        self.type_competition_generique = type_competition_generique
        self.thumbnail = thumbnail
        self.niveau_nb = niveau_nb

    @staticmethod
    def from_dict(obj: Any) -> "Hit":
        try:
            assert isinstance(obj, dict)
            nom = from_union([from_str, from_none], obj.get("nom"))
            code = from_union([from_str, from_none], obj.get("code"))
            niveau = from_union([Niveau, from_none], obj.get("niveau"))
            type_competition = from_union(
                [TypeCompetition, from_none], obj.get("typeCompetition")
            )
            sexe = from_union([Sexe, from_none], obj.get("sexe"))
            id = from_union([from_str, from_none], obj.get("id"))
            creation_en_cours = from_union(
                [from_bool, from_none], obj.get("creationEnCours")
            )
            date_created = from_union(
                [from_datetime, from_none], obj.get("date_created")
            )
            date_updated = from_union(
                [from_datetime, from_none], obj.get("date_updated")
            )
            emarque_v2 = from_union([from_bool, from_none], obj.get("emarqueV2"))
            live_stat = from_union([from_bool, from_none], obj.get("liveStat"))
            publication_internet = from_union(
                [PublicationInternet, from_none], obj.get("publicationInternet")
            )
            pro = from_union([from_bool, from_none], obj.get("pro"))
            competition_origine = from_union(
                [from_str, from_none], obj.get("competition_origine")
            )
            competition_origine_niveau = from_union(
                [from_int, from_none], obj.get("competition_origine_niveau")
            )
            phase_code = from_union([PhaseCode, from_none], obj.get("phase_code"))
            competition_origine_nom = from_union(
                [from_str, from_none], obj.get("competition_origine_nom")
            )
            etat = from_union([Etat, from_none], obj.get("etat"))
            poules = from_union(
                [lambda x: from_list(Poule.from_dict, x), from_none], obj.get("poules")
            )
            phases = from_union(
                [lambda x: from_list(from_str, x), from_none], obj.get("phases")
            )
            categorie = from_union(
                [Categorie.from_dict, from_none], obj.get("categorie")
            )
            id_competition_pere = from_none(obj.get("idCompetitionPere"))
            organisateur = from_union(
                [Organisateur.from_dict, from_none], obj.get("organisateur")
            )
            saison = from_union([Saison.from_dict, from_none], obj.get("saison"))
            logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
            type_competition_generique = from_union(
                [TypeCompetitionGenerique.from_dict, from_none],
                obj.get("typeCompetitionGenerique"),
            )
            thumbnail = from_union([from_none, from_str], obj.get("thumbnail"))
            niveau_nb = from_union(
                [from_none, lambda x: int(from_str(x))], obj.get("niveau_nb")
            )
            return CompetitionsHit(
                nom,
                code,
                niveau,
                type_competition,
                sexe,
                id,
                creation_en_cours,
                date_created,
                date_updated,
                emarque_v2,
                live_stat,
                publication_internet,
                pro,
                competition_origine,
                competition_origine_niveau,
                phase_code,
                competition_origine_nom,
                etat,
                poules,
                phases,
                categorie,
                id_competition_pere,
                organisateur,
                saison,
                logo,
                type_competition_generique,
                thumbnail,
                niveau_nb,
            )
        except Exception as e:
            raise ValueError(f"Invalid `Hit.from_dict` input: {e}")

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.niveau is not None:
            result["niveau"] = from_union(
                [lambda x: to_enum(Niveau, x), from_none], self.niveau
            )
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [lambda x: to_enum(TypeCompetition, x), from_none],
                self.type_competition,
            )
        if self.sexe is not None:
            result["sexe"] = from_union(
                [lambda x: to_enum(Sexe, x), from_none], self.sexe
            )
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.creation_en_cours is not None:
            result["creationEnCours"] = from_union(
                [from_bool, from_none], self.creation_en_cours
            )
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.emarque_v2 is not None:
            result["emarqueV2"] = from_union([from_bool, from_none], self.emarque_v2)
        if self.live_stat is not None:
            result["liveStat"] = from_union([from_bool, from_none], self.live_stat)
        if self.publication_internet is not None:
            result["publicationInternet"] = from_union(
                [lambda x: to_enum(PublicationInternet, x), from_none],
                self.publication_internet,
            )
        if self.pro is not None:
            result["pro"] = from_union([from_bool, from_none], self.pro)
        if self.competition_origine is not None:
            result["competition_origine"] = from_union(
                [from_str, from_none], self.competition_origine
            )
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = from_union(
                [from_int, from_none], self.competition_origine_niveau
            )
        if self.phase_code is not None:
            result["phase_code"] = from_union(
                [lambda x: to_enum(PhaseCode, x), from_none], self.phase_code
            )
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = from_union(
                [from_str, from_none], self.competition_origine_nom
            )
        if self.etat is not None:
            result["etat"] = from_union(
                [lambda x: to_enum(Etat, x), from_none], self.etat
            )
        if self.poules is not None:
            result["poules"] = from_union(
                [lambda x: from_list(lambda x: to_class(Poule, x), x), from_none],
                self.poules,
            )
        if self.phases is not None:
            result["phases"] = from_union(
                [lambda x: from_list(from_str, x), from_none], self.phases
            )
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(Categorie, x), from_none], self.categorie
            )
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = from_none(self.id_competition_pere)
        if self.organisateur is not None:
            result["organisateur"] = from_union(
                [lambda x: to_class(Organisateur, x), from_none], self.organisateur
            )
        if self.saison is not None:
            result["saison"] = from_union(
                [lambda x: to_class(Saison, x), from_none], self.saison
            )
        if self.logo is not None:
            result["logo"] = from_union(
                [lambda x: to_class(Logo, x), from_none], self.logo
            )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [lambda x: to_class(TypeCompetitionGenerique, x), from_none],
                self.type_competition_generique,
            )
        if self.thumbnail is not None:
            result["thumbnail"] = from_union([from_none, from_str], self.thumbnail)
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
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_code and query in self.lower_code)
            or (self.lower_id and query in self.lower_id)
            or (
                self.lower_competition_origine
                and query in self.lower_competition_origine
            )
            or (
                self.lower_competition_origine_nom
                and query in self.lower_competition_origine_nom
            )
        )


class CompetitionsFacetStats(FacetStats):
    @staticmethod
    def from_dict(obj: Any) -> "CompetitionsFacetStats":
        return CompetitionsFacetStats()

    def to_dict(self) -> dict:
        super().to_dict()
