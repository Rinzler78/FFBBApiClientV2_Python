from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.categorie import Categorie
from ...models.competition_id_categorie import CompetitionIDCategorie
from ...models.competition_origine import CompetitionOrigine
from ...models.geo import Geo
from ...models.id_poule import IDPoule
from ...utils.converter_utils import (
    from_bool,
    from_int,
    from_obj,
    from_str,
)


@dataclass
class EngagementsHit(Hit):
    id: str | None = None
    nom: str | None = None
    age: str | None = None
    sexe: str | None = None
    club_pro: bool | None = None
    code_abrege: str | None = None
    code_club: str | None = None
    code_comite: str | None = None
    code_ligue: str | None = None
    competitions_url: str | None = None
    id_competition: CompetitionOrigine | None = None
    id_poule: IDPoule | None = None
    logo: str | None = None
    niveau: Categorie | None = None
    categorie: CompetitionIDCategorie | None = None
    nom_club: str | None = None
    nom_club_pro: str | None = None
    nom_comite: str | None = None
    nom_ctc: str | None = None
    nom_equipe: str | None = None
    nom_ligue: str | None = None
    nom_officiel: str | None = None
    nom_organisme: str | None = None
    nom_usuel: str | None = None
    numero_equipe: int | None = None
    thumbnail: str | None = None
    gradient_color: str | None = None
    geo: Geo | None = None
    lower_nom: str | None = field(init=False, default=None, repr=False)
    lower_nom_club: str | None = field(init=False, default=None, repr=False)
    lower_nom_equipe: str | None = field(init=False, default=None, repr=False)
    lower_nom_organisme: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_nom = self.nom.lower() if self.nom else None
        self.lower_nom_club = self.nom_club.lower() if self.nom_club else None
        self.lower_nom_equipe = self.nom_equipe.lower() if self.nom_equipe else None
        self.lower_nom_organisme = (
            self.nom_organisme.lower() if self.nom_organisme else None
        )

    @staticmethod
    def from_dict(obj: Any) -> EngagementsHit:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        nom = from_str(obj, "nom")
        age = from_str(obj, "age")
        sexe = from_str(obj, "sexe")
        club_pro = from_bool(obj, "clubPro")
        code_abrege = from_str(obj, "codeAbrege")
        code_club = from_str(obj, "codeClub")
        code_comite = from_str(obj, "codeComite")
        code_ligue = from_str(obj, "codeLigue")
        competitions_url = from_str(obj, "competitionsUrl")
        id_competition = from_obj(CompetitionOrigine.from_dict, obj, "idCompetition")
        id_poule = from_obj(IDPoule.from_dict, obj, "idPoule")
        logo = from_str(obj, "logo")
        niveau = from_obj(Categorie.from_dict, obj, "niveau")
        categorie = from_obj(CompetitionIDCategorie.from_dict, obj, "categorie")
        nom_club = from_str(obj, "nomClub")
        nom_club_pro = from_str(obj, "nomClubPro")
        nom_comite = from_str(obj, "nomComite")
        nom_ctc = from_str(obj, "nomCtc")
        nom_equipe = from_str(obj, "nomEquipe")
        nom_ligue = from_str(obj, "nomLigue")
        nom_officiel = from_str(obj, "nomOfficiel")
        nom_organisme = from_str(obj, "nomOrganisme")
        nom_usuel = from_str(obj, "nomUsuel")
        numero_equipe = from_int(obj, "numeroEquipe")
        thumbnail = from_str(obj, "thumbnail")
        gradient_color = from_str(obj, "gradient_color")
        geo = from_obj(Geo.from_dict, obj, "_geo")
        return EngagementsHit(
            id=id,
            nom=nom,
            age=age,
            sexe=sexe,
            club_pro=club_pro,
            code_abrege=code_abrege,
            code_club=code_club,
            code_comite=code_comite,
            code_ligue=code_ligue,
            competitions_url=competitions_url,
            id_competition=id_competition,
            id_poule=id_poule,
            logo=logo,
            niveau=niveau,
            categorie=categorie,
            nom_club=nom_club,
            nom_club_pro=nom_club_pro,
            nom_comite=nom_comite,
            nom_ctc=nom_ctc,
            nom_equipe=nom_equipe,
            nom_ligue=nom_ligue,
            nom_officiel=nom_officiel,
            nom_organisme=nom_organisme,
            nom_usuel=nom_usuel,
            numero_equipe=numero_equipe,
            thumbnail=thumbnail,
            gradient_color=gradient_color,
            geo=geo,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.nom is not None:
            result["nom"] = self.nom
        if self.age is not None:
            result["age"] = self.age
        if self.sexe is not None:
            result["sexe"] = self.sexe
        if self.club_pro is not None:
            result["clubPro"] = self.club_pro
        if self.code_abrege is not None:
            result["codeAbrege"] = self.code_abrege
        if self.code_club is not None:
            result["codeClub"] = self.code_club
        if self.code_comite is not None:
            result["codeComite"] = self.code_comite
        if self.code_ligue is not None:
            result["codeLigue"] = self.code_ligue
        if self.competitions_url is not None:
            result["competitionsUrl"] = self.competitions_url
        if self.id_competition is not None:
            result["idCompetition"] = self.id_competition.to_dict()
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule.to_dict()
        if self.logo is not None:
            result["logo"] = self.logo
        if self.niveau is not None:
            result["niveau"] = self.niveau.to_dict()
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.nom_club is not None:
            result["nomClub"] = self.nom_club
        if self.nom_club_pro is not None:
            result["nomClubPro"] = self.nom_club_pro
        if self.nom_comite is not None:
            result["nomComite"] = self.nom_comite
        if self.nom_ctc is not None:
            result["nomCtc"] = self.nom_ctc
        if self.nom_equipe is not None:
            result["nomEquipe"] = self.nom_equipe
        if self.nom_ligue is not None:
            result["nomLigue"] = self.nom_ligue
        if self.nom_officiel is not None:
            result["nomOfficiel"] = self.nom_officiel
        if self.nom_organisme is not None:
            result["nomOrganisme"] = self.nom_organisme
        if self.nom_usuel is not None:
            result["nomUsuel"] = self.nom_usuel
        if self.numero_equipe is not None:
            result["numeroEquipe"] = str(self.numero_equipe)
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.gradient_color is not None:
            result["gradient_color"] = self.gradient_color
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_nom and query in self.lower_nom)
            or (self.lower_nom_club and query in self.lower_nom_club)
            or (self.lower_nom_equipe and query in self.lower_nom_equipe)
            or (self.lower_nom_organisme and query in self.lower_nom_organisme)
        )
