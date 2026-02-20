from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ...meilisearch.models.hit import Hit
from ...models.competition_id import CompetitionID
from ...models.geo import Geo
from ...models.id_engagement_equipe import IDEngagementEquipe
from ...models.id_organisme_equipe import IDOrganismeEquipe
from ...models.id_poule import IDPoule
from ...models.niveau import Niveau
from ...models.organisateur import Organisateur
from ...models.pratique import Pratique
from ...models.saison import Saison
from ...models.salle import Salle
from ...utils.converter_utils import (
    from_bool,
    from_datetime,
    from_enum,
    from_int,
    from_obj,
    from_officiels_list,
    from_str,
)


@dataclass
class RencontresHit(Hit):
    niveau: Niveau | None = None
    id: str | None = None
    date: datetime | None = None
    date_rencontre: datetime | None = None
    nom_equipe1: str | None = None
    nom_equipe2: str | None = None
    numero_journee: int | None = None
    pratique: Pratique | None = None
    gs_id: str | None = None
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
    date_saisie_resultat_timestamp: int | None = None
    modification_timestamp: int | None = None
    thumbnail: str | None = None
    organisateur: Organisateur | None = None
    niveau_nb: int | None = None
    competition_orgine: str | None = None
    competition_origine: str | None = None
    handicap1: int | None = None
    handicap2: int | None = None
    horaire: str | None = None
    joue: bool | None = None
    logo: str | None = None
    nom_extended: str | None = None
    officiels_string: str | None = None
    pro: bool | None = None
    resultat_equipe1: str | None = None
    resultat_equipe2: str | None = None
    sexe: str | None = None
    type_competition_generique: str | None = None
    unique_key: str | None = None
    url_competition: str | None = None
    lower_id: str | None = field(init=False, default=None, repr=False)
    lower_nom_equipe1: str | None = field(init=False, default=None, repr=False)
    lower_nom_equipe2: str | None = field(init=False, default=None, repr=False)
    lower_gs_id: str | None = field(init=False, default=None, repr=False)
    lower_officiels: list[str] | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_id = self.id.lower() if self.id else None
        self.lower_nom_equipe1 = self.nom_equipe1.lower() if self.nom_equipe1 else None
        self.lower_nom_equipe2 = self.nom_equipe2.lower() if self.nom_equipe2 else None
        self.lower_gs_id = self.gs_id.lower() if self.gs_id else None
        # Handle both old format (list of strings) and new format (list of dicts)
        if self.officiels:
            lower_officiels = []
            for o in self.officiels:
                if isinstance(o, str):
                    lower_officiels.append(o.lower())
                elif isinstance(o, dict):
                    off = o.get("officiel", {})
                    name = f"{off.get('nom', '')} {off.get('prenom', '')}".strip()
                    lower_officiels.append(name.lower() if name else "")
            self.lower_officiels = lower_officiels if lower_officiels else None
        else:
            self.lower_officiels = None

    @staticmethod
    def from_dict(obj: Any) -> RencontresHit:
        try:
            assert isinstance(obj, dict)
            niveau = from_enum(Niveau, obj, "niveau")
            id = from_str(obj, "id")
            date = from_datetime(obj, "date")
            date_rencontre = from_datetime(obj, "date_rencontre")
            nom_equipe1 = from_str(obj, "nomEquipe1")
            nom_equipe2 = from_str(obj, "nomEquipe2")

            numero_journee = from_int(obj, "numeroJournee")
            pratique = from_enum(Pratique, obj, "pratique")
            gs_id = from_str(obj, "gsId")
            officiels = from_officiels_list(obj.get("officiels"))
            competition_id = from_obj(CompetitionID.from_dict, obj, "competitionId")
            id_organisme_equipe1 = from_obj(
                IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe1"
            )
            id_organisme_equipe2 = from_obj(
                IDOrganismeEquipe.from_dict, obj, "idOrganismeEquipe2"
            )
            id_poule = from_obj(IDPoule.from_dict, obj, "idPoule")
            saison = from_obj(Saison.from_dict, obj, "saison")
            salle = from_obj(Salle.from_dict, obj, "salle")
            id_engagement_equipe1 = from_obj(
                IDEngagementEquipe.from_dict, obj, "idEngagementEquipe1"
            )
            id_engagement_equipe2 = from_obj(
                IDEngagementEquipe.from_dict, obj, "idEngagementEquipe2"
            )
            geo = from_obj(Geo.from_dict, obj, "_geo")
            date_timestamp = from_int(obj, "date_timestamp")
            date_rencontre_timestamp = from_int(obj, "date_rencontre_timestamp")
            creation_timestamp = from_int(obj, "creation_timestamp")
            date_saisie_resultat_timestamp = from_int(
                obj, "dateSaisieResultat_timestamp"
            )
            modification_timestamp = from_int(obj, "modification_timestamp")
            thumbnail = from_str(obj, "thumbnail")
            organisateur = from_obj(Organisateur.from_dict, obj, "organisateur")
            niveau_nb = from_int(obj, "niveau_nb")
            competition_orgine = from_str(obj, "competition_orgine")
            competition_origine = from_str(obj, "competition_origine")
            handicap1 = from_int(obj, "handicap1")
            handicap2 = from_int(obj, "handicap2")
            horaire = from_str(obj, "horaire")
            joue = from_bool(obj, "joue")
            logo = from_str(obj, "logo")
            nom_extended = from_str(obj, "nomExtended")
            officiels_string = from_str(obj, "officiels_string")
            pro = from_bool(obj, "pro")
            resultat_equipe1 = from_str(obj, "resultatEquipe1")
            resultat_equipe2 = from_str(obj, "resultatEquipe2")
            sexe = from_str(obj, "sexe")
            type_competition_generique = from_str(obj, "typeCompetitionGenerique")
            unique_key = from_str(obj, "uniqueKey")
            url_competition = from_str(obj, "url_competition")
            return RencontresHit(
                niveau=niveau,
                id=id,
                date=date,
                date_rencontre=date_rencontre,
                nom_equipe1=nom_equipe1,
                nom_equipe2=nom_equipe2,
                numero_journee=numero_journee,
                pratique=pratique,
                gs_id=gs_id,
                officiels=officiels,
                competition_id=competition_id,
                id_organisme_equipe1=id_organisme_equipe1,
                id_organisme_equipe2=id_organisme_equipe2,
                id_poule=id_poule,
                saison=saison,
                salle=salle,
                id_engagement_equipe1=id_engagement_equipe1,
                id_engagement_equipe2=id_engagement_equipe2,
                geo=geo,
                date_timestamp=date_timestamp,
                date_rencontre_timestamp=date_rencontre_timestamp,
                creation_timestamp=creation_timestamp,
                date_saisie_resultat_timestamp=date_saisie_resultat_timestamp,
                modification_timestamp=modification_timestamp,
                thumbnail=thumbnail,
                organisateur=organisateur,
                niveau_nb=niveau_nb,
                competition_orgine=competition_orgine,
                competition_origine=competition_origine,
                handicap1=handicap1,
                handicap2=handicap2,
                horaire=horaire,
                joue=joue,
                logo=logo,
                nom_extended=nom_extended,
                officiels_string=officiels_string,
                pro=pro,
                resultat_equipe1=resultat_equipe1,
                resultat_equipe2=resultat_equipe2,
                sexe=sexe,
                type_competition_generique=type_competition_generique,
                unique_key=unique_key,
                url_competition=url_competition,
            )
        except Exception as e:
            raise ValueError(f"Invalid `Hit` object: {e}") from e

    def to_dict(self) -> dict:
        result: dict = {}
        if self.niveau is not None:
            result["niveau"] = self.niveau.value
        if self.id is not None:
            result["id"] = self.id
        if self.date is not None:
            result["date"] = self.date.isoformat()
        if self.date_rencontre is not None:
            result["date_rencontre"] = self.date_rencontre.isoformat()
        if self.nom_equipe1 is not None:
            result["nomEquipe1"] = self.nom_equipe1
        if self.nom_equipe2 is not None:
            result["nomEquipe2"] = self.nom_equipe2
        if self.numero_journee is not None:
            result["numeroJournee"] = str(self.numero_journee)
        if self.pratique is not None:
            result["pratique"] = self.pratique.value
        if self.gs_id is not None:
            result["gsId"] = self.gs_id
        if self.officiels is not None:
            result["officiels"] = self.officiels
        if self.competition_id is not None:
            result["competitionId"] = self.competition_id.to_dict()
        if self.id_organisme_equipe1 is not None:
            result["idOrganismeEquipe1"] = self.id_organisme_equipe1.to_dict()
        if self.id_organisme_equipe2 is not None:
            result["idOrganismeEquipe2"] = self.id_organisme_equipe2.to_dict()
        if self.id_poule is not None:
            result["idPoule"] = self.id_poule.to_dict()
        if self.saison is not None:
            result["saison"] = self.saison.to_dict()
        if self.salle is not None:
            result["salle"] = self.salle.to_dict()
        if self.id_engagement_equipe1 is not None:
            result["idEngagementEquipe1"] = self.id_engagement_equipe1.to_dict()
        if self.id_engagement_equipe2 is not None:
            result["idEngagementEquipe2"] = self.id_engagement_equipe2.to_dict()
        if self.geo is not None:
            result["_geo"] = self.geo.to_dict()
        if self.date_timestamp is not None:
            result["date_timestamp"] = self.date_timestamp
        if self.date_rencontre_timestamp is not None:
            result["date_rencontre_timestamp"] = self.date_rencontre_timestamp
        if self.creation_timestamp is not None:
            result["creation_timestamp"] = self.creation_timestamp
        if self.date_saisie_resultat_timestamp is not None:
            result["dateSaisieResultat_timestamp"] = self.date_saisie_resultat_timestamp
        if self.modification_timestamp is not None:
            result["modification_timestamp"] = self.modification_timestamp
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.organisateur is not None:
            result["organisateur"] = self.organisateur.to_dict()
        if self.niveau_nb is not None:
            result["niveau_nb"] = str(self.niveau_nb)
        if self.competition_orgine is not None:
            result["competition_orgine"] = self.competition_orgine
        if self.competition_origine is not None:
            result["competition_origine"] = self.competition_origine
        if self.handicap1 is not None:
            result["handicap1"] = self.handicap1
        if self.handicap2 is not None:
            result["handicap2"] = self.handicap2
        if self.horaire is not None:
            result["horaire"] = self.horaire
        if self.joue is not None:
            result["joue"] = self.joue
        if self.logo is not None:
            result["logo"] = self.logo
        if self.nom_extended is not None:
            result["nomExtended"] = self.nom_extended
        if self.officiels_string is not None:
            result["officiels_string"] = self.officiels_string
        if self.pro is not None:
            result["pro"] = self.pro
        if self.resultat_equipe1 is not None:
            result["resultatEquipe1"] = self.resultat_equipe1
        if self.resultat_equipe2 is not None:
            result["resultatEquipe2"] = self.resultat_equipe2
        if self.sexe is not None:
            result["sexe"] = self.sexe
        if self.type_competition_generique is not None:
            result["typeCompetitionGenerique"] = self.type_competition_generique
        if self.unique_key is not None:
            result["uniqueKey"] = self.unique_key
        if self.url_competition is not None:
            result["url_competition"] = self.url_competition
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_gs_id and query in self.lower_gs_id)
            or (self.lower_id and query in self.lower_id)
            or (
                self.lower_officiels
                and any(query in off for off in self.lower_officiels)
            )
            or (
                self.salle
                and (
                    (self.salle.lower_adresse and query in self.salle.lower_adresse)
                    or (
                        self.salle.lower_adresse_complement
                        and query in self.salle.lower_adresse_complement
                    )
                    or (self.salle.lower_libelle and query in self.salle.lower_libelle)
                )
            )
        )
