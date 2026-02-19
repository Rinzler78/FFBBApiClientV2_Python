from .query_fields_manager import QueryFieldsManager


class OrganismeFields(QueryFieldsManager):
    """Fields for organisme queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    CODE = "code"
    TELEPHONE = "telephone"
    ADRESSE = "adresse"
    MAIL = "mail"
    TYPE = "type"
    NOM_SIMPLE = "nom_simple"
    URL_SITE_WEB = "urlSiteWeb"

    # Club Pro fields
    NOM_CLUB_PRO = "nomClubPro"
    ADRESSE_CLUB_PRO = "adresseClubPro"
    COMMUNE_CLUB_PRO = "communeClubPro"

    # FK-only fields (int IDs)
    COMMUNE = "commune"
    SALLE = "salle"
    SAISON = "saison"
    ORGANISME_ID_PERE = "organisme_id_pere"

    # FK-only: logo (Directus file UUID)
    LOGO = "logo"

    # FK-only: lists
    ENGAGEMENTS = "engagements"
    COMPETITIONS = "competitions"

    # Organismes fils (list of int IDs)
    ORGANISMES_FILS = "organismes_fils"

    # Embedded: cartographie
    CARTOGRAPHIE_ID = "cartographie.id"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    CARTOGRAPHIE_ADRESSE = "cartographie.adresse"
    CARTOGRAPHIE_CODE_POSTAL = "cartographie.codePostal"
    CARTOGRAPHIE_COORDONNEES = "cartographie.coordonnees"
    CARTOGRAPHIE_COORDONNEES_COORDINATES = "cartographie.coordonnees.coordinates"
    CARTOGRAPHIE_COORDONNEES_TYPE = "cartographie.coordonnees.type"
    CARTOGRAPHIE_STATUS = "cartographie.status"
    CARTOGRAPHIE_TITLE = "cartographie.title"
    CARTOGRAPHIE_VILLE = "cartographie.ville"

    # Embedded: offresPratiques (junction table)
    OFFRES_PRATIQUES_ID = "offresPratiques.ffbbserver_offres_pratiques_id.id"
    OFFRES_PRATIQUES_TITLE = "offresPratiques.ffbbserver_offres_pratiques_id.title"
    OFFRES_PRATIQUES_CATEGORIE = (
        "offresPratiques.ffbbserver_offres_pratiques_id.categoriePratique"
    )
    OFFRES_PRATIQUES_TYPE = (
        "offresPratiques.ffbbserver_offres_pratiques_id.typePratique"
    )

    # Embedded: labellisation
    LABELLISATION_ID = "labellisation.id"
    LABELLISATION_DEBUT = "labellisation.debut"
    LABELLISATION_FIN = "labellisation.fin"
    LABELLISATION_PROGRAMME_ID = "labellisation.idLabellisationProgramme.id"
    LABELLISATION_PROGRAMME_LIBELLE = "labellisation.idLabellisationProgramme.libelle"
    LABELLISATION_PROGRAMME_LABEL = (
        "labellisation.idLabellisationProgramme.labellisationLabel"
    )
    LABELLISATION_PROGRAMME_LOGO_VERTICAL = (
        "labellisation.idLabellisationProgramme.logo_vertical"
    )

    # Embedded: membres
    MEMBRES_ID = "membres.id"
    MEMBRES_NOM = "membres.nom"
    MEMBRES_PRENOM = "membres.prenom"
    MEMBRES_MAIL = "membres.mail"
    MEMBRES_TELEPHONE_PORTABLE = "membres.telephonePortable"
    MEMBRES_ADRESSE1 = "membres.adresse1"
    MEMBRES_ADRESSE2 = "membres.adresse2"
    MEMBRES_CODE_POSTAL = "membres.codePostal"
    MEMBRES_VILLE = "membres.ville"
    MEMBRES_TELEPHONE_FIXE = "membres.telephoneFixe"
    MEMBRES_CODE_FONCTION = "membres.codeFonction"

    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for organisme queries."""
        return [
            # Basic fields
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.MAIL,
            cls.TYPE,
            cls.NOM_SIMPLE,
            cls.URL_SITE_WEB,
            # Club Pro
            cls.NOM_CLUB_PRO,
            cls.ADRESSE_CLUB_PRO,
            cls.COMMUNE_CLUB_PRO,
            # FK-only
            cls.COMMUNE,
            cls.SALLE,
            cls.SAISON,
            cls.ORGANISME_ID_PERE,
            cls.LOGO,
            cls.ENGAGEMENTS,
            cls.COMPETITIONS,
            # Organismes fils
            cls.ORGANISMES_FILS,
            # Cartographie
            cls.CARTOGRAPHIE_ID,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
            cls.CARTOGRAPHIE_ADRESSE,
            cls.CARTOGRAPHIE_CODE_POSTAL,
            cls.CARTOGRAPHIE_COORDONNEES,
            cls.CARTOGRAPHIE_COORDONNEES_COORDINATES,
            cls.CARTOGRAPHIE_COORDONNEES_TYPE,
            cls.CARTOGRAPHIE_STATUS,
            cls.CARTOGRAPHIE_TITLE,
            cls.CARTOGRAPHIE_VILLE,
            # Offres Pratiques
            cls.OFFRES_PRATIQUES_ID,
            cls.OFFRES_PRATIQUES_TITLE,
            cls.OFFRES_PRATIQUES_CATEGORIE,
            cls.OFFRES_PRATIQUES_TYPE,
            # Labellisation
            cls.LABELLISATION_ID,
            cls.LABELLISATION_DEBUT,
            cls.LABELLISATION_FIN,
            cls.LABELLISATION_PROGRAMME_ID,
            cls.LABELLISATION_PROGRAMME_LIBELLE,
            cls.LABELLISATION_PROGRAMME_LABEL,
            cls.LABELLISATION_PROGRAMME_LOGO_VERTICAL,
            # Membres
            cls.MEMBRES_ID,
            cls.MEMBRES_NOM,
            cls.MEMBRES_PRENOM,
            cls.MEMBRES_MAIL,
            cls.MEMBRES_TELEPHONE_PORTABLE,
            cls.MEMBRES_ADRESSE1,
            cls.MEMBRES_ADRESSE2,
            cls.MEMBRES_CODE_POSTAL,
            cls.MEMBRES_VILLE,
            cls.MEMBRES_TELEPHONE_FIXE,
            cls.MEMBRES_CODE_FONCTION,
            # Timestamps
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
