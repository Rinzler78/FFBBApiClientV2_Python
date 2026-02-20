from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.categorie import Categorie
from ...models.etat import Etat
from ...models.logo import Logo
from ...models.niveau import Niveau
from ...models.organisateur import Organisateur
from ...models.phase_code import PhaseCode
from ...models.poule import Poule
from ...models.publication_internet import PublicationInternet
from ...models.saison import Saison
from ...models.sexe import Sexe
from ...models.type_competition import TypeCompetition
from ...models.type_competition_generique import TypeCompetitionGenerique
from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_int,
    from_list,
    from_obj,
    from_str,
)


@dataclass
class CompetitionsHit(Hit):
    nom: str | None = None
    code: str | None = None
    niveau: Niveau | None = None
    type_competition: TypeCompetition | None = None
    sexe: Sexe | None = None
    id: str | None = None
    creation_en_cours: bool | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    emarque_v2: bool | None = None
    live_stat: bool | None = None
    publication_internet: PublicationInternet | None = None
    pro: bool | None = None
    competition_origine: str | None = None
    competition_origine_niveau: int | None = None
    phase_code: PhaseCode | None = None
    competition_origine_nom: str | None = None
    etat: Etat | None = None
    poules: list[Poule] | None = None
    phases: list[str] | None = None
    categorie: Categorie | None = None
    id_competition_pere: str | None = None
    organisateur: Organisateur | None = None
    saison: Saison | None = None
    logo: Logo | None = None
    type_competition_generique: TypeCompetitionGenerique | None = None
    thumbnail: str | None = None
    niveau_nb: int | None = None
    age: str | None = None
    code_comite: str | None = None
    code_ligue: str | None = None
    compare_old_site: bool | None = None
    ordre: int | None = None
    participants: str | None = None
    slug: str | None = None
    to_update: bool | None = None
    lower_nom: str | None = field(init=False, default=None, repr=False)
    lower_code: str | None = field(init=False, default=None, repr=False)
    lower_id: str | None = field(init=False, default=None, repr=False)
    lower_competition_origine: str | None = field(init=False, default=None, repr=False)
    lower_competition_origine_nom: str | None = field(
        init=False, default=None, repr=False
    )

    def __post_init__(self) -> None:
        self.lower_nom = self.nom.lower() if self.nom else None
        self.lower_code = self.code.lower() if self.code else None
        self.lower_id = self.id.lower() if self.id else None
        self.lower_competition_origine = (
            self.competition_origine.lower() if self.competition_origine else None
        )
        self.lower_competition_origine_nom = (
            self.competition_origine_nom.lower()
            if self.competition_origine_nom
            else None
        )

    @staticmethod
    def from_dict(obj: Any) -> CompetitionsHit:
        try:
            assert isinstance(obj, dict)
            nom = from_str(obj, "nom")
            code = from_str(obj, "code")
            niveau = from_enum(Niveau, obj, "niveau")
            type_competition = from_enum(TypeCompetition, obj, "typeCompetition")
            sexe = from_enum(Sexe, obj, "sexe")
            id = from_str(obj, "id")
            creation_en_cours = from_bool(obj, "creationEnCours")
            date_created = from_datetime(obj, "date_created")
            date_updated = from_datetime(obj, "date_updated")
            emarque_v2 = from_bool(obj, "emarqueV2")
            live_stat = from_bool(obj, "liveStat")
            publication_internet = from_enum(
                PublicationInternet, obj, "publicationInternet"
            )
            pro = from_bool(obj, "pro")
            competition_origine = from_str(obj, "competition_origine")
            competition_origine_niveau = from_int(obj, "competition_origine_niveau")
            phase_code = from_enum(PhaseCode, obj, "phase_code")
            competition_origine_nom = from_str(obj, "competition_origine_nom")
            etat = from_enum(Etat, obj, "etat")
            poules = from_list(Poule.from_dict, obj, "poules")
            phases = from_list(str, obj, "phases")
            categorie = from_obj(Categorie.from_dict, obj, "categorie")
            id_competition_pere = from_str(obj, "idCompetitionPere")
            organisateur = from_obj(Organisateur.from_dict, obj, "organisateur")
            saison = from_obj(Saison.from_dict, obj, "saison")
            logo = from_obj(Logo.from_dict, obj, "logo")
            type_competition_generique = from_obj(
                TypeCompetitionGenerique.from_dict, obj, "typeCompetitionGenerique"
            )
            thumbnail = from_str(obj, "thumbnail")
            niveau_nb = from_int(obj, "niveau_nb")
            age = from_str(obj, "age")
            code_comite = from_str(obj, "codeComite")
            code_ligue = from_str(obj, "codeLigue")
            compare_old_site = from_bool(obj, "compare_old_site")
            ordre = from_int(obj, "ordre")
            participants = from_str(obj, "participants")
            slug = from_str(obj, "slug")
            to_update = from_bool(obj, "toUpdate")
            return CompetitionsHit(
                nom=nom,
                code=code,
                niveau=niveau,
                type_competition=type_competition,
                sexe=sexe,
                id=id,
                creation_en_cours=creation_en_cours,
                date_created=date_created,
                date_updated=date_updated,
                emarque_v2=emarque_v2,
                live_stat=live_stat,
                publication_internet=publication_internet,
                pro=pro,
                competition_origine=competition_origine,
                competition_origine_niveau=competition_origine_niveau,
                phase_code=phase_code,
                competition_origine_nom=competition_origine_nom,
                etat=etat,
                poules=poules,
                phases=phases,
                categorie=categorie,
                id_competition_pere=id_competition_pere,
                organisateur=organisateur,
                saison=saison,
                logo=logo,
                type_competition_generique=type_competition_generique,
                thumbnail=thumbnail,
                niveau_nb=niveau_nb,
                age=age,
                code_comite=code_comite,
                code_ligue=code_ligue,
                compare_old_site=compare_old_site,
                ordre=ordre,
                participants=participants,
                slug=slug,
                to_update=to_update,
            )
        except Exception as e:
            raise ValueError(f"Invalid `Hit.from_dict` input: {e}") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.nom is not None:
            result["nom"] = self.nom
        if self.code is not None:
            result["code"] = self.code
        if self.niveau is not None:
            result["niveau"] = self.niveau.value
        if self.type_competition is not None:
            result["typeCompetition"] = self.type_competition.value
        if self.sexe is not None:
            result["sexe"] = self.sexe.value
        if self.id is not None:
            result["id"] = self.id
        if self.creation_en_cours is not None:
            result["creationEnCours"] = self.creation_en_cours
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.emarque_v2 is not None:
            result["emarqueV2"] = self.emarque_v2
        if self.live_stat is not None:
            result["liveStat"] = self.live_stat
        if self.publication_internet is not None:
            result["publicationInternet"] = self.publication_internet.value
        if self.pro is not None:
            result["pro"] = self.pro
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine
        if self.competition_origine_niveau is not None:
            result["competition_origine_niveau"] = self.competition_origine_niveau
        if self.phase_code is not None:
            result["phase_code"] = self.phase_code.value
        if self.competition_origine_nom is not None:
            result["competition_origine_nom"] = self.competition_origine_nom
        if self.etat is not None:
            result["etat"] = self.etat.value
        if self.poules is not None:
            result["poules"] = [p.to_dict() for p in self.poules]
        if self.phases is not None:
            result["phases"] = self.phases
        if self.categorie is not None:
            result["categorie"] = self.categorie.to_dict()
        if self.id_competition_pere is not None:
            result["idCompetitionPere"] = self.id_competition_pere
        if self.organisateur is not None:
            result["organisateur"] = self.organisateur.to_dict()
        if self.saison is not None:
            result["saison"] = self.saison.to_dict()
        if self.logo is not None:
            result["logo"] = self.logo.to_dict()
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = (
                self.type_competition_generique.to_dict()
            )
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.niveau_nb is not None:
            result["niveau_nb"] = str(self.niveau_nb)
        if self.age is not None:
            result["age"] = self.age
        if self.code_comite is not None:
            result["codeComite"] = self.code_comite
        if self.code_ligue is not None:
            result["codeLigue"] = self.code_ligue
        if self.compare_old_site is not None:
            result["compare_old_site"] = self.compare_old_site
        if self.ordre is not None:
            result["ordre"] = self.ordre
        if self.participants is not None:
            result["participants"] = self.participants
        if self.slug is not None:
            result["slug"] = self.slug
        if self.to_update is not None:
            result["toUpdate"] = self.to_update
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
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
