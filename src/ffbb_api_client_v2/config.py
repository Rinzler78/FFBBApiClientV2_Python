"""Centralized configuration for FFBB API client."""

# API URLs
API_FFBB_BASE_URL = "https://api.ffbb.app/"
MEILISEARCH_BASE_URL = "https://meilisearch-prod.ffbb.app/"

# HTTP Headers
DEFAULT_USER_AGENT = "okhttp/4.12.0"

# Environment variable names for tokens
ENV_API_TOKEN = "API_FFBB_APP_BEARER_TOKEN"
ENV_MEILISEARCH_TOKEN = "MEILISEARCH_BEARER_TOKEN"

# API Endpoint Paths (relative to base URL)
ENDPOINT_CONFIGURATION = "items/configuration"
ENDPOINT_LIVES = "json/lives.json"
ENDPOINT_COMPETITIONS = "items/ffbbserver_competitions"
ENDPOINT_POULES = "items/ffbbserver_poules"
ENDPOINT_SAISONS = "items/ffbbserver_saisons"
ENDPOINT_ORGANISMES = "items/ffbbserver_organismes"
ENDPOINT_COMMUNES = "items/ffbbserver_communes"
ENDPOINT_OFFICIELS = "items/ffbbserver_officiels"
ENDPOINT_ENTRAINEURS = "items/ffbbserver_entraineurs"
ENDPOINT_RENCONTRES = "items/ffbbserver_rencontres"
ENDPOINT_SALLES = "items/ffbbserver_salles"
ENDPOINT_TERRAINS = "items/ffbbserver_terrains"
ENDPOINT_TOURNOIS = "items/ffbbserver_tournois"
ENDPOINT_ENGAGEMENTS = "items/ffbbserver_engagements"
ENDPOINT_FORMATIONS = "items/ffbbserver_formations"
ENDPOINT_PRATIQUES = "items/ffbbnational_pratiques"

# Meilisearch Endpoint Paths
MEILISEARCH_ENDPOINT_MULTI_SEARCH = "multi-search"

# Meilisearch Index UIDs
MEILISEARCH_INDEX_ORGANISMES = "ffbbserver_organismes"
MEILISEARCH_INDEX_RENCONTRES = "ffbbserver_rencontres"
MEILISEARCH_INDEX_TERRAINS = "ffbbserver_terrains"
MEILISEARCH_INDEX_SALLES = "ffbbserver_salles"
MEILISEARCH_INDEX_TOURNOIS = "ffbbserver_tournois"
MEILISEARCH_INDEX_COMPETITIONS = "ffbbserver_competitions"
MEILISEARCH_INDEX_ENGAGEMENTS = "ffbbserver_engagements"
MEILISEARCH_INDEX_FORMATIONS = "ffbbserver_formations"
MEILISEARCH_INDEX_PRATIQUES = "ffbbnational_pratiques"

MEILISEARCH_INDEX_UIDS = [
    MEILISEARCH_INDEX_ORGANISMES,
    MEILISEARCH_INDEX_RENCONTRES,
    MEILISEARCH_INDEX_TERRAINS,
    MEILISEARCH_INDEX_SALLES,
    MEILISEARCH_INDEX_TOURNOIS,
    MEILISEARCH_INDEX_COMPETITIONS,
    MEILISEARCH_INDEX_ENGAGEMENTS,
    MEILISEARCH_INDEX_FORMATIONS,
    MEILISEARCH_INDEX_PRATIQUES,
]

# Meilisearch Default Facets per Index
MEILISEARCH_FACETS_ORGANISMES = [
    "type_association.libelle",
    "type_association.code",
    "type",
    "labellisation",
    "offresPratiques",
    "saison_en_cours",
    "commune.codePostal",
    "commune.departement",
    "commune.libelle",
    "communeClubPro.codePostal",
    "communeClubPro.departement",
    "communeClubPro.libelle",
    "organisme_id_pere.code",
    "organisme_id_pere.nom",
    "organisme_id_pere.type",
    "salle.libelle",
    "_geo",
    "_geo.lat",
    "_geo.lng",
]
MEILISEARCH_FACETS_RENCONTRES = [
    "competitionId.categorie.code",
    "competitionId.categorie.ordre",
    "competitionId.code",
    "competitionId.competition_origine.id",
    "competitionId.id",
    "competitionId.nom",
    "competitionId.nomExtended",
    "competitionId.sexe",
    "competitionId.typeCompetition",
    "creation_timestamp",
    "dateSaisieResultat_timestamp",
    "date_rencontre_timestamp",
    "date_timestamp",
    "gsId.currentStatus",
    "gsId.matchStatus",
    "gsId.matchType",
    "gsId.periodStatus",
    "idOrganismeEquipe1.code",
    "idOrganismeEquipe1.nom",
    "idOrganismeEquipe2.code",
    "idOrganismeEquipe2.nom",
    "idPoule.nom",
    "joue",
    "modification_timestamp",
    "niveau",
    "niveau_nb",
    "organisateur.id",
    "organisateur.nom",
    "pratique",
    "saison.code",
    "salle.libelle",
    "_geo",
]
MEILISEARCH_FACETS_TOURNOIS = [
    "sexe",
    "tournoiTypes3x3.libelle",
    "tournoiTypes3x3.type_league",
    "tournoiType",
    "debut_timestamp",
    "fin_timestamp",
    "commune.codePostal",
    "commune.departement",
    "commune.libelle",
    "_geo",
]
MEILISEARCH_FACETS_PRATIQUES = [
    "label",
    "type",
    "cp_salle",
    "ville_salle",
    "date_debut_timestamp",
    "date_fin_timestamp",
    "cartographie.codePostal",
    "_geo",
    "_geo.lat",
    "_geo.lng",
]
MEILISEARCH_FACETS_COMPETITIONS = [
    "categorie.code",
    "categorie.libelle",
    "categorie.ordre",
    "code",
    "compare_old_site",
    "creationEnCours",
    "emarqueV2",
    "etat",
    "liveStat",
    "niveau",
    "niveau_nb",
    "organisateur.code",
    "organisateur.id",
    "organisateur.nom",
    "organisateur.type",
    "phase_code",
    "pro",
    "saison.code",
    "sexe",
    "toUpdate",
    "typeCompetition",
]
MEILISEARCH_FACETS_SALLES = [
    "type",
    "commune.codePostal",
    "commune.departement",
    "commune.libelle",
    "_geo",
    "_geo.lat",
    "_geo.lng",
]
MEILISEARCH_FACETS_TERRAINS = [
    "accesLibre",
    "commune.codePostal",
    "commune.departement",
    "commune.libelle",
    "natureSol.code",
    "natureSol.libelle",
    "_geo",
    "_geo.lat",
    "_geo.lng",
]
MEILISEARCH_FACETS_ENGAGEMENTS = [
    "clubPro",
    "idCompetition.categorie.code",
    "idCompetition.categorie.libelle",
    "idCompetition.code",
    "idCompetition.nom",
    "idCompetition.sexe",
    "idPoule.nom",
    "niveau.code",
    "niveau.libelle",
    "_geo",
    "_geo.lat",
    "_geo.lng",
]
MEILISEARCH_FACETS_FORMATIONS = [
    "date_end_formatted",
    "date_start_formatted",
    "domain",
    "mode",
    "place",
    "places",
    "postal_code",
    "postal_codes",
    "theme",
    "type",
]
