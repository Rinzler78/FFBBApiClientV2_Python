from .query_fields_manager import QueryFieldsManager


class EngagementsFields(QueryFieldsManager):
    """Fields for engagements queries."""

    ID = "id"
    NOM = "nom"
    NOM_EQUIPE = "nomEquipe"
    NOM_USUEL = "nomUsuel"
    NOM_OFFICIEL = "nomOfficiel"
    NUMERO_EQUIPE = "numeroEquipe"
    CODE_ABREGE = "codeAbrege"
    CLUB_PRO = "clubPro"
    POSITION = "position"
    POSITION_VARIATION = "positionVariation"
    POSITION_N1 = "position_n1"
    LOGO = "logo"
    LOGO_GENIUS = "logo_genius"
    PHOTO = "photo"
    POULE_ID = "pouleId"
    # FK-only fields
    ID_COMPETITION = "idCompetition"
    ID_ORGANISME = "idOrganisme"
    ID_ORGANISME_CTC = "idOrganismeCtc"
    ID_POULE = "idPoule"
    ENTRAINEUR = "entraineur"
    ENTRAINEUR_ADJOINT = "entraineurAdjoint"
    RENCONTRES_DOMICILES = "rencontres_domiciles"
    RENCONTRES_EXTERIEUR = "rencontres_exterieur"
    # Correspondant fields
    ADRESSE_CORRESPONDANT_EQUIPE = "adresseCorrespondantEquipe"
    COMPLEMENT_ADRESSE_CORRESPONDANT_EQUIPE = "complementAdresseCorrespondantEquipe"
    COMMUNE_CORRESPONDANT_EQUIPE = "communeCorrespondantEquipe"
    EMAIL_CORRESPONDANT_EQUIPE = "emailCorrespondantEquipe"
    NOM_CORRESPONDANT_EQUIPE = "nomCorrespondantEquipe"
    TELEPHONE_FIXE_CORRESPONDANT_EQUIPE = "telephoneFixeCorrespondantEquipe"
    TELEPHONE_PORTABLE_CORRESPONDANT_EQUIPE = "telephonePortableCorrespondantEquipe"
    TELEPHONE_TRAVAIL_CORRESPONDANT_EQUIPE = "telephoneTravailCorrespondantEquipe"
    # CTC fields
    NOM_CTC = "nomCtc"
    TYPE_ENTENTE_CTC = "typeEntenteCtc"
    # Other
    TO_UPDATE = "toUpdate"
    URL_COMPETITION = "url_competition"
    # Embedded: niveau
    NIVEAU_ID = "niveau.id"
    NIVEAU_CODE = "niveau.code"
    NIVEAU_LIBELLE = "niveau.libelle"
    NIVEAU_SEXE = "niveau.sexe"
    NIVEAU_ORDRE = "niveau.ordre"
    NIVEAU_POINT = "niveau.point"
    NIVEAU_CCG = "niveau.ccg"
    NIVEAU_CATEGORIE_CHAMPIONNAT = "niveau.categorieChampionnat"
    # Embedded: classement (scalaires + FK-only nested)
    CLASSEMENT_ID = "classement.id"
    CLASSEMENT_POSITION = "classement.position"
    CLASSEMENT_POINTS = "classement.points"
    CLASSEMENT_MATCH_JOUES = "classement.matchJoues"
    CLASSEMENT_GAGNES = "classement.gagnes"
    CLASSEMENT_PERDUS = "classement.perdus"
    CLASSEMENT_NULS = "classement.nuls"
    CLASSEMENT_NOMBRE_FORFAITS = "classement.nombreForfaits"
    CLASSEMENT_NOMBRE_DEFAUTS = "classement.nombreDefauts"
    CLASSEMENT_PANIERS_MARQUES = "classement.paniersMarques"
    CLASSEMENT_PANIERS_ENCAISSES = "classement.paniersEncaisses"
    CLASSEMENT_DIFFERENCE = "classement.difference"
    CLASSEMENT_QUOTIENT = "classement.quotient"
    CLASSEMENT_POINT_INITIAUX = "classement.pointInitiaux"
    CLASSEMENT_POINTS_INITIAUX = "classement.pointsInitiaux"
    CLASSEMENT_PENALITES = "classement.penalites"
    CLASSEMENT_PENALITES_ARBITRAGE = "classement.penalitesArbitrage"
    CLASSEMENT_PENALITES_ENTRAINEUR = "classement.penalitesEntraineur"
    CLASSEMENT_PENALITES_DIVERSES = "classement.penalitesDiverses"
    CLASSEMENT_HORS_CLASSEMENT = "classement.horsClassement"
    CLASSEMENT_ORGANISME_NOM = "classement.organisme_nom"
    # FK-only nested in classement
    CLASSEMENT_ID_COMPETITION = "classement.idCompetition"
    CLASSEMENT_ID_POULE = "classement.idPoule"
    CLASSEMENT_ID_ENGAGEMENT = "classement.idEngagement"
    CLASSEMENT_ORGANISME = "classement.organisme"
    # Embedded: positions
    POSITIONS = "positions"
    DATE_CREATED = "date_created"
    DATE_UPDATED = "date_updated"

    @classmethod
    def get_fields(cls) -> list[str]:
        """Return the complete list of fields for engagements."""
        return [
            cls.ID,
            cls.NOM,
            cls.NOM_EQUIPE,
            cls.NOM_USUEL,
            cls.NOM_OFFICIEL,
            cls.NUMERO_EQUIPE,
            cls.CODE_ABREGE,
            cls.CLUB_PRO,
            cls.POSITION,
            cls.POSITION_VARIATION,
            cls.POSITION_N1,
            cls.LOGO,
            cls.LOGO_GENIUS,
            cls.PHOTO,
            cls.POULE_ID,
            cls.ID_COMPETITION,
            cls.ID_ORGANISME,
            cls.ID_ORGANISME_CTC,
            cls.ID_POULE,
            cls.ENTRAINEUR,
            cls.ENTRAINEUR_ADJOINT,
            cls.RENCONTRES_DOMICILES,
            cls.RENCONTRES_EXTERIEUR,
            cls.ADRESSE_CORRESPONDANT_EQUIPE,
            cls.COMPLEMENT_ADRESSE_CORRESPONDANT_EQUIPE,
            cls.COMMUNE_CORRESPONDANT_EQUIPE,
            cls.EMAIL_CORRESPONDANT_EQUIPE,
            cls.NOM_CORRESPONDANT_EQUIPE,
            cls.TELEPHONE_FIXE_CORRESPONDANT_EQUIPE,
            cls.TELEPHONE_PORTABLE_CORRESPONDANT_EQUIPE,
            cls.TELEPHONE_TRAVAIL_CORRESPONDANT_EQUIPE,
            cls.NOM_CTC,
            cls.TYPE_ENTENTE_CTC,
            cls.TO_UPDATE,
            cls.URL_COMPETITION,
            cls.NIVEAU_ID,
            cls.NIVEAU_CODE,
            cls.NIVEAU_LIBELLE,
            cls.NIVEAU_SEXE,
            cls.NIVEAU_ORDRE,
            cls.NIVEAU_POINT,
            cls.NIVEAU_CCG,
            cls.NIVEAU_CATEGORIE_CHAMPIONNAT,
            cls.CLASSEMENT_ID,
            cls.CLASSEMENT_POSITION,
            cls.CLASSEMENT_POINTS,
            cls.CLASSEMENT_MATCH_JOUES,
            cls.CLASSEMENT_GAGNES,
            cls.CLASSEMENT_PERDUS,
            cls.CLASSEMENT_NULS,
            cls.CLASSEMENT_NOMBRE_FORFAITS,
            cls.CLASSEMENT_NOMBRE_DEFAUTS,
            cls.CLASSEMENT_PANIERS_MARQUES,
            cls.CLASSEMENT_PANIERS_ENCAISSES,
            cls.CLASSEMENT_DIFFERENCE,
            cls.CLASSEMENT_QUOTIENT,
            cls.CLASSEMENT_POINT_INITIAUX,
            cls.CLASSEMENT_POINTS_INITIAUX,
            cls.CLASSEMENT_PENALITES,
            cls.CLASSEMENT_PENALITES_ARBITRAGE,
            cls.CLASSEMENT_PENALITES_ENTRAINEUR,
            cls.CLASSEMENT_PENALITES_DIVERSES,
            cls.CLASSEMENT_HORS_CLASSEMENT,
            cls.CLASSEMENT_ORGANISME_NOM,
            cls.CLASSEMENT_ID_COMPETITION,
            cls.CLASSEMENT_ID_POULE,
            cls.CLASSEMENT_ID_ENGAGEMENT,
            cls.CLASSEMENT_ORGANISME,
            cls.POSITIONS,
            cls.DATE_CREATED,
            cls.DATE_UPDATED,
        ]
