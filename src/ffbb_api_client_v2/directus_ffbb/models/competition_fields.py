from .query_fields_manager import QueryFieldsManager


class CompetitionFields(QueryFieldsManager):
    """Fields for competition queries."""

    # Basic fields
    ID = "id"
    NOM = "nom"
    SEXE = "sexe"
    CODE = "code"
    TYPE_COMPETITION = "typeCompetition"
    LIVE_STAT = "liveStat"
    PUBLICATION_INTERNET = "publicationInternet"
    ETAT = "etat"
    CREATION_EN_COURS = "creationEnCours"
    COMPARE_OLD_SITE = "compare_old_site"
    EMARQUE_V2 = "emarqueV2"
    ORDRE = "ordre"
    PRO = "pro"
    SLUG = "slug"
    TO_UPDATE = "toUpdate"
    PHASE_CODE = "phase_code"
    COMPETITION_ORIGINE_NOM = "competition_origine_nom"
    COMPETITION_ORIGINE_NIVEAU = "competition_origine_niveau"

    # FK-only fields (int IDs)
    SAISON = "saison"
    COMPETITION_ORIGINE = "competition_origine"
    ID_COMPETITION_PERE = "idCompetitionPere"
    ORGANISATEUR = "organisateur"
    LOGO = "logo"

    # FK-only: poules (list of int IDs)
    POULES = "poules"

    # Embedded: categorie
    CATEGORIE_ID = "categorie.id"
    CATEGORIE_CODE = "categorie.code"
    CATEGORIE_LIBELLE = "categorie.libelle"
    CATEGORIE_ORDRE = "categorie.ordre"

    # Embedded: typeCompetitionGenerique
    TYPE_COMPETITION_GENERIQUE_ID = "typeCompetitionGenerique.id"
    TYPE_COMPETITION_GENERIQUE_LOGO = "typeCompetitionGenerique.logo"

    # Embedded: phases (child competitions)
    PHASES_ID = "phases.id"
    PHASES_NOM = "phases.nom"
    PHASES_LIVE_STAT = "phases.liveStat"
    PHASES_PHASE_CODE = "phases.phase_code"
    PHASES_POULES = "phases.poules"
    PHASES_SAISON = "phases.saison"

    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for competition queries."""
        return [
            # Basic fields
            cls.ID,
            cls.NOM,
            cls.SEXE,
            cls.CODE,
            cls.TYPE_COMPETITION,
            cls.LIVE_STAT,
            cls.PUBLICATION_INTERNET,
            cls.ETAT,
            cls.CREATION_EN_COURS,
            cls.COMPARE_OLD_SITE,
            cls.EMARQUE_V2,
            cls.ORDRE,
            cls.PRO,
            cls.SLUG,
            cls.TO_UPDATE,
            cls.PHASE_CODE,
            cls.COMPETITION_ORIGINE_NOM,
            cls.COMPETITION_ORIGINE_NIVEAU,
            # FK-only
            cls.SAISON,
            cls.COMPETITION_ORIGINE,
            cls.ID_COMPETITION_PERE,
            cls.ORGANISATEUR,
            cls.LOGO,
            cls.POULES,
            # Categorie
            cls.CATEGORIE_ID,
            cls.CATEGORIE_CODE,
            cls.CATEGORIE_LIBELLE,
            cls.CATEGORIE_ORDRE,
            # typeCompetitionGenerique
            cls.TYPE_COMPETITION_GENERIQUE_ID,
            cls.TYPE_COMPETITION_GENERIQUE_LOGO,
            # Phases
            cls.PHASES_ID,
            cls.PHASES_NOM,
            cls.PHASES_LIVE_STAT,
            cls.PHASES_PHASE_CODE,
            cls.PHASES_POULES,
            cls.PHASES_SAISON,
            # Timestamps
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
