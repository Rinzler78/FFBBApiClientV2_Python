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
    NATURE_SOL_ID = "natureSol.id"
    NATURE_SOL_CODE = "natureSol.code"
    NATURE_SOL_LIBELLE = "natureSol.libelle"
    NATURE_SOL_TERRAIN = "natureSol.terrain"
    COMMUNE = "commune"
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
            cls.NATURE_SOL_ID,
            cls.NATURE_SOL_CODE,
            cls.NATURE_SOL_LIBELLE,
            cls.NATURE_SOL_TERRAIN,
            cls.COMMUNE,
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
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
