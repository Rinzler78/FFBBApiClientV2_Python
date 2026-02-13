class SallesFields:
    """Default fields for salles queries."""

    ID = "id"
    LIBELLE = "libelle"
    LIBELLE2 = "libelle2"
    ADRESSE = "adresse"
    ADRESSE_COMPLEMENT = "adresseComplement"
    NUMERO = "numero"
    TELEPHONE = "telephone"
    MAIL = "mail"
    CAPACITE_SPECTATEUR = "capaciteSpectateur"
    COMMUNE_ID = "commune.id"
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"
    COMMUNE_DEPARTEMENT = "commune.departement"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_default_fields(cls) -> list[str]:
        """Get default fields for salles queries."""
        return [
            cls.ID,
            cls.LIBELLE,
            cls.LIBELLE2,
            cls.ADRESSE,
            cls.ADRESSE_COMPLEMENT,
            cls.NUMERO,
            cls.TELEPHONE,
            cls.MAIL,
            cls.CAPACITE_SPECTATEUR,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
        ]

    @classmethod
    def get_detailed_fields(cls) -> list[str]:
        """Get detailed fields for salles queries."""
        return cls.get_default_fields() + [
            cls.COMMUNE_ID,
            cls.COMMUNE_DEPARTEMENT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]

    @staticmethod
    def get_wildcard(depth: int = 2) -> list[str]:
        """Get wildcard fields at the specified depth."""
        return [".".join(["*"] * min(depth, 5))]
