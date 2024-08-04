from typing import Any, Optional

from .CompetitionIDCategorie import CompetitionIDCategorie
from .CompetitionIDTypeCompetitionGenerique import CompetitionIDTypeCompetitionGenerique
from .CompetitionOrigine import CompetitionOrigine
from .converters import from_bool, from_none, from_str, from_union, to_class
from .logo import Logo


class CompetitionID:
    id: Optional[str] = None
    nom: Optional[str] = None
    competition_origine_nom: Optional[str] = None
    code: Optional[str] = None
    creation_en_cours: Optional[bool] = None
    live_stat: Optional[bool] = None
    publication_internet: Optional[str] = None
    sexe: Optional[str] = None
    type_competition: Optional[str] = None
    pro: Optional[bool] = None
    logo: Logo
    categorie: Optional[str] = None
    type_competition_generique: Optional[CompetitionIDTypeCompetitionGenerique] = None
    competition_origine: Optional[CompetitionOrigine] = None
    nom_extended: Optional[str] = None

    def __init__(
        self,
        id: Optional[str],
        nom: Optional[str],
        competition_origine_nom: Optional[str],
        code: Optional[str],
        creation_en_cours: Optional[bool],
        live_stat: Optional[bool],
        publication_internet: Optional[str],
        sexe: Optional[str],
        type_competition: Optional[str],
        pro: Optional[bool],
        logo: Logo,
        categorie: Optional[str],
        type_competition_generique: Optional[CompetitionIDTypeCompetitionGenerique],
        competition_origine: Optional[CompetitionOrigine],
        nom_extended: Optional[str],
    ) -> None:
        self.id = id
        self.nom = nom
        self.competition_origine_nom = competition_origine_nom
        self.code = code
        self.creation_en_cours = creation_en_cours
        self.live_stat = live_stat
        self.publication_internet = publication_internet
        self.sexe = sexe
        self.type_competition = type_competition
        self.pro = pro
        self.logo = logo
        self.categorie = categorie
        self.type_competition_generique = type_competition_generique
        self.competition_origine = competition_origine
        self.nom_extended = nom_extended

    @staticmethod
    def from_dict(obj: Any) -> "CompetitionID":
        try:
            assert isinstance(obj, dict)
            id = from_union([from_str, from_none], obj.get("id"))
            nom = from_union([from_str, from_none], obj.get("nom"))
            competition_origine_nom = from_union(
                [from_str, from_none], obj.get("competition_origine_nom")
            )
            code = from_union([from_str, from_none], obj.get("code"))
            creation_en_cours = from_union(
                [from_bool, from_none], obj.get("creationEnCours")
            )
            live_stat = from_union([from_bool, from_none], obj.get("liveStat"))
            publication_internet = from_union(
                [from_str, from_none], obj.get("publicationInternet")
            )
            sexe = from_union([from_str, from_none], obj.get("sexe"))
            type_competition = from_union(
                [from_str, from_none], obj.get("typeCompetition")
            )
            pro = from_union([from_bool, from_none], obj.get("pro"))
            logo = from_union([Logo.from_dict, from_none], obj.get("logo"))
            categorie = from_union(
                [CompetitionIDCategorie.from_dict, from_none], obj.get("categorie")
            )
            type_competition_generique = from_union(
                [CompetitionIDTypeCompetitionGenerique.from_dict, from_none],
                obj.get("typeCompetitionGenerique"),
            )
            competition_origine = from_union(
                [CompetitionOrigine.from_dict, from_none],
                obj.get("competition_origine"),
            )
            nom_extended = from_union([from_str, from_none], obj.get("nomExtended"))
            return CompetitionID(
                id,
                nom,
                competition_origine_nom,
                code,
                creation_en_cours,
                live_stat,
                publication_internet,
                sexe,
                type_competition,
                pro,
                logo,
                categorie,
                type_competition_generique,
                competition_origine,
                nom_extended,
            )
        except Exception as e:
            raise ValueError("Invalid CompetitionID object") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([from_str, from_none], self.id)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = from_union(
                [from_str, from_none], self.competition_origine_nom
            )
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.creation_en_cours is not None:
            result["creationEnCours"] = from_union(
                [from_bool, from_none], self.creation_en_cours
            )
        if self.live_stat is not None:
            result["liveStat"] = from_union([from_bool, from_none], self.live_stat)
        if self.publication_internet is not None:
            result["publicationInternet"] = from_union(
                [from_str, from_none],
                self.publication_internet,
            )
        if self.sexe is not None:
            result["sexe"] = from_union([from_str, from_none], self.sexe)
        if self.type_competition is not None:
            result["typeCompetition"] = from_union(
                [from_str, from_none],
                self.type_competition,
            )
        if self.pro is not None:
            result["pro"] = from_union([from_bool, from_none], self.pro)
        if self.logo is not None:
            result["logo"] = from_none(self.logo)
        if self.categorie is not None:
            result["categorie"] = from_union(
                [lambda x: to_class(CompetitionIDCategorie, x), from_none],
                self.categorie,
            )
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = from_union(
                [
                    lambda x: to_class(CompetitionIDTypeCompetitionGenerique, x),
                    from_none,
                ],
                self.type_competition_generique,
            )
        if self.competition_origine is not None:
            result["competition_origine"] = from_union(
                [lambda x: to_class(CompetitionOrigine, x), from_none],
                self.competition_origine,
            )
        if self.nom_extended is not None:
            result["nomExtended"] = from_union([from_str, from_none], self.nom_extended)
        return result
