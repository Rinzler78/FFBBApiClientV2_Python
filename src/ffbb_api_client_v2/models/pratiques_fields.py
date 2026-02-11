class PratiquesFields:
    """Default fields for pratiques queries."""

    ID = "id"
    TITRE = "titre"
    TYPE = "type"
    LABEL = "label"
    DESCRIPTION = "description"
    CODE = "code"
    ADRESSE = "adresse"
    EMAIL = "email"
    TELEPHONE = "telephone"
    DATE_DEBUT = "date_debut"
    DATE_FIN = "date_fin"
    HORAIRES_SEANCES = "horaires_seances"
    JOURS = "jours"
    NOM_STRUCTURE = "nom_structure"
    ADRESSE_STRUCTURE = "adresse_structure"
    MAIL_STRUCTURE = "mail_structure"
    NOM_SALLE = "nom_salle"
    ADRESSE_SALLE = "adresse_salle"
    CP_SALLE = "cp_salle"
    VILLE_SALLE = "ville_salle"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    CARTOGRAPHIE_CODE_POSTAL = "cartographie.codePostal"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for pratiques queries."""
        return [
            cls.ID,
            cls.TITRE,
            cls.TYPE,
            cls.LABEL,
            cls.DESCRIPTION,
            cls.CODE,
            cls.ADRESSE,
            cls.EMAIL,
            cls.TELEPHONE,
            cls.DATE_DEBUT,
            cls.DATE_FIN,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for pratiques queries."""
        return cls.get_default_fields() + [
            cls.HORAIRES_SEANCES,
            cls.JOURS,
            cls.NOM_STRUCTURE,
            cls.ADRESSE_STRUCTURE,
            cls.MAIL_STRUCTURE,
            cls.NOM_SALLE,
            cls.ADRESSE_SALLE,
            cls.CP_SALLE,
            cls.VILLE_SALLE,
            cls.CARTOGRAPHIE_CODE_POSTAL,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    @staticmethod
    def get_wildcard(depth: int = 2) -> list[str]:
        """Get wildcard fields at the specified depth."""
        return [".".join(["*"] * min(depth, 5))]
