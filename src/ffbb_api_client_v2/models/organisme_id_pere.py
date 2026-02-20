from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_int,
    from_list,
    from_obj,
    from_str,
    from_uuid,
)
from .id_poule import IDPoule
from .labellisation_item import LabellisationItem


@dataclass
class OrganismeIDPere:
    adresse: str | None = None
    adresse_club_pro: str | None = None
    cartographie: str | None = None
    code: str | None = None
    commune: int | None = None
    commune_club_pro: str | None = None
    date_created: datetime | None = None
    date_updated: datetime | None = None
    id: int | None = None
    mail: str | None = None
    nom: str | None = None
    nom_club_pro: str | None = None
    organisme_id_pere: OrganismeIDPere | None = None
    salle: str | None = None
    telephone: str | None = None
    type: str | None = None
    type_association: str | None = None
    url_site_web: str | None = None
    logo: UUID | None = None
    nom_simple: str | None = None
    date_affiliation: datetime | None = None
    saison_en_cours: bool | None = None
    entreprise: bool | None = None
    handibasket: bool | None = None
    omnisport: bool | None = None
    hors_association: bool | None = None
    offres_pratiques: list[int] | None = None
    engagements: list[IDPoule] | None = None
    labellisation: list[LabellisationItem] | None = None

    @staticmethod
    def from_dict(obj: Any) -> OrganismeIDPere:
        assert isinstance(obj, dict)
        adresse = from_str(obj, "adresse")
        adresse_club_pro = from_str(obj, "adresseClubPro")
        cartographie = from_str(obj, "cartographie")
        code = from_str(obj, "code")
        commune = from_int(obj, "commune")
        commune_club_pro = from_str(obj, "communeClubPro")
        date_created = from_datetime(obj, "date_created")
        date_updated = from_datetime(obj, "date_updated")
        id = from_int(obj, "id")
        mail = from_str(obj, "mail")
        nom = from_str(obj, "nom")
        nom_club_pro = from_str(obj, "nomClubPro")
        organisme_id_pere = from_obj(
            OrganismeIDPere.from_dict, obj, "organisme_id_pere"
        )
        salle = from_str(obj, "salle")
        telephone = from_str(obj, "telephone")
        type = from_str(obj, "type")
        type_association = from_str(obj, "type_association")
        url_site_web = from_str(obj, "urlSiteWeb")
        logo = from_uuid(obj, "logo")
        nom_simple = from_str(obj, "nom_simple")
        date_affiliation = from_datetime(obj, "dateAffiliation")
        saison_en_cours = from_bool(obj, "saison_en_cours")
        entreprise = from_bool(obj, "entreprise")
        handibasket = from_bool(obj, "handibasket")
        omnisport = from_bool(obj, "omnisport")
        hors_association = from_bool(obj, "horsAssociation")
        offres_pratiques = from_list(int, obj, "offresPratiques")
        engagements = from_list(IDPoule.from_dict, obj, "engagements")
        labellisation = from_list(LabellisationItem.from_dict, obj, "labellisation")
        return OrganismeIDPere(
            adresse=adresse,
            adresse_club_pro=adresse_club_pro,
            cartographie=cartographie,
            code=code,
            commune=commune,
            commune_club_pro=commune_club_pro,
            date_created=date_created,
            date_updated=date_updated,
            id=id,
            mail=mail,
            nom=nom,
            nom_club_pro=nom_club_pro,
            organisme_id_pere=organisme_id_pere,
            salle=salle,
            telephone=telephone,
            type=type,
            type_association=type_association,
            url_site_web=url_site_web,
            logo=logo,
            nom_simple=nom_simple,
            date_affiliation=date_affiliation,
            saison_en_cours=saison_en_cours,
            entreprise=entreprise,
            handibasket=handibasket,
            omnisport=omnisport,
            hors_association=hors_association,
            offres_pratiques=offres_pratiques,
            engagements=engagements,
            labellisation=labellisation,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = self.adresse
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = self.adresse_club_pro
        if self.cartographie is not None:
            result["cartographie"] = self.cartographie
        if self.code is not None:
            result["code"] = self.code
        if self.commune is not None:
            result["commune"] = str(self.commune)
        if self.commune_club_pro is not None:
            result["communeClubPro"] = self.commune_club_pro
        if self.date_created is not None:
            result["date_created"] = self.date_created.isoformat()
        if self.date_updated is not None:
            result["date_updated"] = self.date_updated.isoformat()
        if self.id is not None:
            result["id"] = str(self.id)
        if self.mail is not None:
            result["mail"] = self.mail
        if self.nom is not None:
            result["nom"] = self.nom
        if self.nom_club_pro is not None:
            result["nomClubPro"] = self.nom_club_pro
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = self.organisme_id_pere.to_dict()
        if self.salle is not None:
            result["salle"] = self.salle
        if self.telephone is not None:
            result["telephone"] = self.telephone
        if self.type is not None:
            result["type"] = self.type
        if self.type_association is not None:
            result["type_association"] = self.type_association
        if self.url_site_web is not None:
            result["urlSiteWeb"] = self.url_site_web
        if self.logo is not None:
            result["logo"] = str(self.logo)
        if self.nom_simple is not None:
            result["nom_simple"] = self.nom_simple
        if self.date_affiliation is not None:
            result["dateAffiliation"] = self.date_affiliation.isoformat()
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = self.saison_en_cours
        if self.entreprise is not None:
            result["entreprise"] = self.entreprise
        if self.handibasket is not None:
            result["handibasket"] = self.handibasket
        if self.omnisport is not None:
            result["omnisport"] = self.omnisport
        if self.hors_association is not None:
            result["horsAssociation"] = self.hors_association
        if self.offres_pratiques is not None:
            result["offresPratiques"] = self.offres_pratiques
        if self.engagements is not None:
            result["engagements"] = [e.to_dict() for e in self.engagements]
        if self.labellisation is not None:
            result["labellisation"] = [lb.to_dict() for lb in self.labellisation]
        return result
