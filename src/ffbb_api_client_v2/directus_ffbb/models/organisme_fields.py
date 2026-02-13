class OrganismeFields:
    """Default fields for organisme queries."""

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

    # Commune fields
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"

    # Competitions fields
    COMPETITIONS_ID = "competitions.id"
    COMPETITIONS_NOM = "competitions.nom"

    # Engagements fields
    ENGAGEMENTS_ID = "engagements.id"
    ENGAGEMENTS_ID_COMPETITION_ID = "engagements.idCompetition.id"
    ENGAGEMENTS_ID_COMPETITION_NOM = "engagements.idCompetition.nom"
    ENGAGEMENTS_ID_COMPETITION_CODE = "engagements.idCompetition.code"
    ENGAGEMENTS_ID_COMPETITION_SEXE = "engagements.idCompetition.sexe"
    ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE = (
        "engagements.idCompetition.competition_origine"
    )
    ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NOM = (
        "engagements.idCompetition.competition_origine_nom"
    )
    ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NIVEAU = (
        "engagements.idCompetition.competition_origine_niveau"
    )
    ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION = (
        "engagements.idCompetition.typeCompetition"
    )
    ENGAGEMENTS_ID_COMPETITION_LOGO_ID = "engagements.idCompetition.logo.id"
    ENGAGEMENTS_ID_COMPETITION_LOGO_GRADIENT_COLOR = (
        "engagements.idCompetition.logo.gradient_color"
    )
    ENGAGEMENTS_ID_COMPETITION_SAISON_ID = "engagements.idCompetition.saison.id"
    ENGAGEMENTS_ID_COMPETITION_SAISON_LIBELLE = (
        "engagements.idCompetition.saison.libelle"
    )
    ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE = (
        "engagements.idCompetition.idCompetitionPere"
    )
    ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_ID = (
        "engagements.idCompetition.idCompetitionPere.id"
    )
    ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_NOM = (
        "engagements.idCompetition.idCompetitionPere.nom"
    )
    ENGAGEMENTS_ID_COMPETITION_ORGANISATEUR_TYPE = (
        "engagements.idCompetition.organisateur.type"
    )
    ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_ID = (
        "engagements.idCompetition.typeCompetitionGenerique.logo.id"
    )
    ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_GRADIENT_COLOR = (
        "engagements.idCompetition.typeCompetitionGenerique.logo.gradient_color"
    )
    ENGAGEMENTS_ID_COMPETITION_CATEGORIE_CODE = (
        "engagements.idCompetition.categorie.code"
    )
    ENGAGEMENTS_ID_COMPETITION_CATEGORIE_ORDRE = (
        "engagements.idCompetition.categorie.ordre"
    )
    ENGAGEMENTS_ID_POULE_ID = "engagements.idPoule.id"
    ENGAGEMENTS_ID_POULE_NOM = "engagements.idPoule.nom"

    # Cartographie fields (model: CartographieModel)
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"

    # Club Pro fields (model: direct attributes)
    NOM_CLUB_PRO = "nomClubPro"
    ADRESSE_CLUB_PRO = "adresseClubPro"
    COMMUNE_CLUB_PRO = "communeClubPro"

    # Logo fields (model: LogoModel)
    LOGO_ID = "logo.id"
    LOGO_GRADIENT_COLOR = "logo.gradient_color"

    # Salle fields (model: SalleModel)
    SALLE_ID = "salle.id"
    SALLE_NUMERO = "salle.numero"
    SALLE_LIBELLE = "salle.libelle"
    SALLE_LIBELLE2 = "salle.libelle2"
    SALLE_ADRESSE = "salle.adresse"
    SALLE_ADRESSE_COMPLEMENT = "salle.adresseComplement"
    SALLE_COMMUNE_CODE_POSTAL = "salle.commune.codePostal"
    SALLE_COMMUNE_LIBELLE = "salle.commune.libelle"
    SALLE_CARTOGRAPHIE_LATITUDE = "salle.cartographie.latitude"
    SALLE_CARTOGRAPHIE_LONGITUDE = "salle.cartographie.longitude"

    # Organismes fils (model: list[Any])
    ORGANISMES_FILS = "organismes_fils"

    # Offres Pratiques fields (model: OffrespratiquesitemModel)
    OFFRES_PRATIQUES_ID = "offresPratiques.ffbbserver_offres_pratiques_id.id"
    OFFRES_PRATIQUES_TITLE = "offresPratiques.ffbbserver_offres_pratiques_id.title"
    OFFRES_PRATIQUES_CATEGORIE = (
        "offresPratiques.ffbbserver_offres_pratiques_id.categoriePratique"
    )
    OFFRES_PRATIQUES_TYPE = (
        "offresPratiques.ffbbserver_offres_pratiques_id.typePratique"
    )

    # Labellisation fields (model: LabellisationitemModel)
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

    # Membres fields
    MEMBRES_ID = "membres.id"
    MEMBRES_NOM = "membres.nom"
    MEMBRES_PRENOM = "membres.prenom"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for organisme queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.MAIL,
            cls.TYPE,
            cls.NOM_SIMPLE,
            cls.URL_SITE_WEB,
            # Cartographie
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
            # Club Pro
            cls.NOM_CLUB_PRO,
            cls.ADRESSE_CLUB_PRO,
            cls.COMMUNE_CLUB_PRO,
            # Logo
            cls.LOGO_ID,
            cls.LOGO_GRADIENT_COLOR,
            # Salle
            cls.SALLE_ID,
            cls.SALLE_NUMERO,
            cls.SALLE_LIBELLE,
            cls.SALLE_LIBELLE2,
            cls.SALLE_ADRESSE,
            cls.SALLE_ADRESSE_COMPLEMENT,
            cls.SALLE_COMMUNE_CODE_POSTAL,
            cls.SALLE_COMMUNE_LIBELLE,
            cls.SALLE_CARTOGRAPHIE_LATITUDE,
            cls.SALLE_CARTOGRAPHIE_LONGITUDE,
            # Organismes fils
            cls.ORGANISMES_FILS,
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
            # Competitions
            cls.COMPETITIONS_ID,
            cls.COMPETITIONS_NOM,
            # Engagements
            cls.ENGAGEMENTS_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_NOM,
            cls.ENGAGEMENTS_ID_COMPETITION_CODE,
            cls.ENGAGEMENTS_ID_COMPETITION_SEXE,
            cls.ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE,
            cls.ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NOM,
            cls.ENGAGEMENTS_ID_COMPETITION_COMPETITION_ORIGINE_NIVEAU,
            cls.ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION,
            cls.ENGAGEMENTS_ID_COMPETITION_LOGO_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_LOGO_GRADIENT_COLOR,
            cls.ENGAGEMENTS_ID_COMPETITION_SAISON_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_SAISON_LIBELLE,
            cls.ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE,
            cls.ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_ID_COMPETITION_PERE_NOM,
            cls.ENGAGEMENTS_ID_COMPETITION_ORGANISATEUR_TYPE,
            cls.ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_ID,
            cls.ENGAGEMENTS_ID_COMPETITION_TYPE_COMPETITION_GENERIQUE_LOGO_GRADIENT_COLOR,
            cls.ENGAGEMENTS_ID_COMPETITION_CATEGORIE_CODE,
            cls.ENGAGEMENTS_ID_COMPETITION_CATEGORIE_ORDRE,
            cls.ENGAGEMENTS_ID_POULE_ID,
            cls.ENGAGEMENTS_ID_POULE_NOM,
            # Membres (basic info)
            cls.MEMBRES_ID,
            cls.MEMBRES_NOM,
            cls.MEMBRES_PRENOM,
        ]

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        """Get basic fields for simple organisme queries."""
        return [
            cls.ID,
            cls.NOM,
            cls.CODE,
            cls.TELEPHONE,
            cls.ADRESSE,
            cls.MAIL,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields including personal member data."""
        return cls.get_default_fields() + [
            # Additional member personal data (not in default)
            "membres.mail",
            "membres.telephonePortable",
            "membres.adresse1",
            "membres.adresse2",
            "membres.codePostal",
            "membres.ville",
            "membres.telephoneFixe",
            "membres.codeFonction",
        ]

    @staticmethod
    def get_wildcard(depth: int = 4) -> list[str]:
        """Get wildcard fields at the specified depth.

        Max useful depth for organismes is 4 (2657 fields at *.*.*.*).
        """
        return [".".join(["*"] * min(depth, 5))]
