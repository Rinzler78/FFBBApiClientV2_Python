"""FFBB-specific Meilisearch configuration: index UIDs, facets."""

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
