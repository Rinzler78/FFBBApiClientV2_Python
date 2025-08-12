from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_bool,
    from_datetime,
    from_list,
    from_none,
    from_str,
    from_union,
    from_uuid,
    is_type,
)


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
    organisme_id_pere: str | None = None
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
    offres_pratiques: list[Any] | None = None
    engagements: list[Any] | None = None
    labellisation: list[Any] | None = None

    def __init__(
        self,
        adresse: str | None,
        adresse_club_pro: str | None,
        cartographie: str | None,
        code: str | None,
        commune: int | None,
        commune_club_pro: str | None,
        date_created: datetime | None,
        date_updated: datetime | None,
        id: int | None,
        mail: str | None,
        nom: str | None,
        nom_club_pro: str | None,
        organisme_id_pere: str | None,
        salle: str | None,
        telephone: str | None,
        type: str | None,
        type_association: str | None,
        url_site_web: str | None,
        logo: UUID | None,
        nom_simple: str | None,
        date_affiliation: datetime | None,
        saison_en_cours: bool | None,
        entreprise: bool | None,
        handibasket: bool | None,
        omnisport: bool | None,
        hors_association: bool | None,
        offres_pratiques: list[Any] | None,
        engagements: list[Any] | None,
        labellisation: list[Any] | None,
    ) -> None:
        self.adresse = adresse
        self.adresse_club_pro = adresse_club_pro
        self.cartographie = cartographie
        self.code = code
        self.commune = commune
        self.commune_club_pro = commune_club_pro
        self.date_created = date_created
        self.date_updated = date_updated
        self.id = id
        self.mail = mail
        self.nom = nom
        self.nom_club_pro = nom_club_pro
        self.organisme_id_pere = organisme_id_pere
        self.salle = salle
        self.telephone = telephone
        self.type = type
        self.type_association = type_association
        self.url_site_web = url_site_web
        self.logo = logo
        self.nom_simple = nom_simple
        self.date_affiliation = date_affiliation
        self.saison_en_cours = saison_en_cours
        self.entreprise = entreprise
        self.handibasket = handibasket
        self.omnisport = omnisport
        self.hors_association = hors_association
        self.offres_pratiques = offres_pratiques
        self.engagements = engagements
        self.labellisation = labellisation

    @staticmethod
    def from_dict(obj: Any) -> OrganismeIDPere:
        assert isinstance(obj, dict)
        adresse = from_union([from_str, from_none], obj.get("adresse"))
        adresse_club_pro = from_none(obj.get("adresseClubPro"))
        cartographie = from_union([from_str, from_none], obj.get("cartographie"))
        code = from_union([from_str, from_none], obj.get("code"))
        commune = from_union(
            [lambda x: int(from_str(x)), from_none], obj.get("commune")
        )
        commune_club_pro = from_none(obj.get("communeClubPro"))
        date_created = from_union([from_datetime, from_none], obj.get("date_created"))
        date_updated = from_union([from_datetime, from_none], obj.get("date_updated"))
        id = from_union([lambda x: int(from_str(x)), from_none], obj.get("id"))
        mail = from_union([from_str, from_none], obj.get("mail"))
        nom = from_union([from_str, from_none], obj.get("nom"))
        nom_club_pro = from_union([from_str, from_none], obj.get("nomClubPro"))
        organisme_id_pere = from_union(
            [OrganismeIDPere.from_dict, from_none], obj.get("organisme_id_pere")
        )
        salle = from_none(obj.get("salle"))
        telephone = from_union([from_str, from_none], obj.get("telephone"))
        type = from_union([from_str, from_none], obj.get("type"))
        type_association = from_none(obj.get("type_association"))
        url_site_web = from_union([from_str, from_none], obj.get("urlSiteWeb"))
        logo = from_union([from_uuid, from_none], obj.get("logo"))
        nom_simple = from_union([from_str, from_none], obj.get("nom_simple"))
        date_affiliation = from_none(obj.get("dateAffiliation"))
        saison_en_cours = from_union([from_bool, from_none], obj.get("saison_en_cours"))
        entreprise = from_union([from_bool, from_none], obj.get("entreprise"))
        handibasket = from_union([from_bool, from_none], obj.get("handibasket"))
        omnisport = from_union([from_bool, from_none], obj.get("omnisport"))
        hors_association = from_union(
            [from_bool, from_none], obj.get("horsAssociation")
        )
        offres_pratiques = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("offresPratiques")
        )
        engagements = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("engagements")
        )
        labellisation = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("labellisation")
        )
        return OrganismeIDPere(
            adresse,
            adresse_club_pro,
            cartographie,
            code,
            commune,
            commune_club_pro,
            date_created,
            date_updated,
            id,
            mail,
            nom,
            nom_club_pro,
            organisme_id_pere,
            salle,
            telephone,
            type,
            type_association,
            url_site_web,
            logo,
            nom_simple,
            date_affiliation,
            saison_en_cours,
            entreprise,
            handibasket,
            omnisport,
            hors_association,
            offres_pratiques,
            engagements,
            labellisation,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.adresse is not None:
            result["adresse"] = from_union([from_str, from_none], self.adresse)
        if self.adresse_club_pro is not None:
            result["adresseClubPro"] = from_none(self.adresse_club_pro)
        if self.cartographie is not None:
            result["cartographie"] = from_union(
                [from_str, from_none], self.cartographie
            )
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.commune is not None:
            result["commune"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.commune,
            )
        if self.commune_club_pro is not None:
            result["communeClubPro"] = from_none(self.commune_club_pro)
        if self.date_created is not None:
            result["date_created"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_created
            )
        if self.date_updated is not None:
            result["date_updated"] = from_union(
                [lambda x: x.isoformat(), from_none], self.date_updated
            )
        if self.id is not None:
            result["id"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.id,
            )
        if self.mail is not None:
            result["mail"] = from_union([from_str, from_none], self.mail)
        if self.nom is not None:
            result["nom"] = from_union([from_str, from_none], self.nom)
        if self.nom_club_pro is not None:
            result["nomClubPro"] = from_union([from_str, from_none], self.nom_club_pro)
        if self.organisme_id_pere is not None:
            result["organisme_id_pere"] = from_union(
                [from_str, from_none], self.organisme_id_pere
            )
        if self.salle is not None:
            result["salle"] = from_none(self.salle)
        if self.telephone is not None:
            result["telephone"] = from_union([from_str, from_none], self.telephone)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.type_association is not None:
            result["type_association"] = from_none(self.type_association)
        if self.url_site_web is not None:
            result["urlSiteWeb"] = from_union([from_str, from_none], self.url_site_web)
        if self.logo is not None:
            result["logo"] = from_union([from_none, lambda x: str(x)], self.logo)
        if self.nom_simple is not None:
            result["nom_simple"] = from_union([from_str, from_none], self.nom_simple)
        if self.date_affiliation is not None:
            result["dateAffiliation"] = from_none(self.date_affiliation)
        if self.saison_en_cours is not None:
            result["saison_en_cours"] = from_union(
                [from_bool, from_none], self.saison_en_cours
            )
        if self.entreprise is not None:
            result["entreprise"] = from_union([from_bool, from_none], self.entreprise)
        if self.handibasket is not None:
            result["handibasket"] = from_union([from_bool, from_none], self.handibasket)
        if self.omnisport is not None:
            result["omnisport"] = from_union([from_bool, from_none], self.omnisport)
        if self.hors_association is not None:
            result["horsAssociation"] = from_union(
                [from_bool, from_none], self.hors_association
            )
        if self.offres_pratiques is not None:
            result["offresPratiques"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.offres_pratiques
            )
        if self.engagements is not None:
            result["engagements"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.engagements
            )
        if self.labellisation is not None:
            result["labellisation"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.labellisation
            )
        return result
