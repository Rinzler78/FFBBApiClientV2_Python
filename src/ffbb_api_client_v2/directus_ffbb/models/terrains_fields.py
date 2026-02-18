from .query_fields_manager import QueryFieldsManager


class TerrainsFields(QueryFieldsManager):
    """Fields for terrains queries."""

    ID = "id"
    NOM = "nom"
    RUE = "rue"
    NUMERO = "numero"
    LARGEUR = "largeur"
    LONGUEUR = "longueur"
    ACCES_LIBRE = "accesLibre"
    NATURE_SOL_CODE = "natureSol.code"
    NATURE_SOL_LIBELLE = "natureSol.libelle"
    COMMUNE_ID = "commune.id"
    COMMUNE_CODE_POSTAL = "commune.codePostal"
    COMMUNE_LIBELLE = "commune.libelle"
    COMMUNE_DEPARTEMENT = "commune.departement"
    CARTOGRAPHIE_LATITUDE = "cartographie.latitude"
    CARTOGRAPHIE_LONGITUDE = "cartographie.longitude"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for terrains."""
        return [
            cls.ID,
            cls.NOM,
            cls.RUE,
            cls.NUMERO,
            cls.LARGEUR,
            cls.LONGUEUR,
            cls.ACCES_LIBRE,
            cls.NATURE_SOL_CODE,
            cls.NATURE_SOL_LIBELLE,
            cls.COMMUNE_CODE_POSTAL,
            cls.COMMUNE_LIBELLE,
            cls.CARTOGRAPHIE_LATITUDE,
            cls.CARTOGRAPHIE_LONGITUDE,
            cls.COMMUNE_ID,
            cls.COMMUNE_DEPARTEMENT,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
