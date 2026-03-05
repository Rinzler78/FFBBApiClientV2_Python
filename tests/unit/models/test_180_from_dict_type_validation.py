"""Test that all model from_dict() methods reject non-dict input."""

from __future__ import annotations

import importlib

import pytest

# (module_path, class_name) for all models with TypeError validation in from_dict
MODELS_WITH_TYPE_CHECK = [
    ("ffbb_api_client_v2.directus_ffbb.models.live", "Live"),
    (
        "ffbb_api_client_v2.directus_ffbb.models.poule_rencontre_item_model",
        "PouleRencontreItemModel",
    ),
    (
        "ffbb_api_client_v2.meilisearch.models.federated_search_result",
        "FederatedHit",
    ),
    (
        "ffbb_api_client_v2.meilisearch.models.federated_search_result",
        "FederatedSearchResult",
    ),
    (
        "ffbb_api_client_v2.meilisearch.models.federated_search_result",
        "FederationInfo",
    ),
    (
        "ffbb_api_client_v2.meilisearch.models.meilisearch_index_settings",
        "MeilisearchIndexSettings",
    ),
    (
        "ffbb_api_client_v2.meilisearch.models.multi_search_queries",
        "MultiSearchQueries",
    ),
    ("ffbb_api_client_v2.meilisearch.models.multi_search_query", "MultiSearchQuery"),
    (
        "ffbb_api_client_v2.meilisearch.models.multi_search_results",
        "MultiSearchResult",
    ),
    (
        "ffbb_api_client_v2.meilisearch.models.multi_search_results_class",
        "MultiSearchResults",
    ),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.competitions_facet_distribution",
        "CompetitionsFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.competitions_hit", "CompetitionsHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.engagements_facet_distribution",
        "EngagementsFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.engagements_hit", "EngagementsHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.formation_session",
        "FormationSession",
    ),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.formations_facet_distribution",
        "FormationsFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.formations_hit", "FormationsHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.organismes_facet_distribution",
        "OrganismesFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.organismes_hit", "OrganismesHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_facet_distribution",
        "PratiquesFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_hit", "PratiquesHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.pratiques_type_facet",
        "PratiquesTypeFacet",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.rencontres_hit", "RencontresHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.salles_facet_distribution",
        "SallesFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.salles_hit", "SallesHit"),
    (
        "ffbb_api_client_v2.meilisearch_ffbb.models.terrains_facet_distribution",
        "TerrainsFacetDistribution",
    ),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.terrains_hit", "TerrainsHit"),
    ("ffbb_api_client_v2.meilisearch_ffbb.models.tournois_hit", "TournoisHit"),
    ("ffbb_api_client_v2.models.affiche", "Affiche"),
    ("ffbb_api_client_v2.models.cartographie", "Cartographie"),
    ("ffbb_api_client_v2.models.categorie", "Categorie"),
    ("ffbb_api_client_v2.models.commune", "Commune"),
    ("ffbb_api_client_v2.models.competition", "Competition"),
    ("ffbb_api_client_v2.models.competition_detail", "CompetitionDetail"),
    ("ffbb_api_client_v2.models.competition_origine", "CompetitionOrigine"),
    (
        "ffbb_api_client_v2.models.competition_origine_categorie",
        "CompetitionOrigineCategorie",
    ),
    ("ffbb_api_client_v2.models.competition_phase", "CompetitionPhase"),
    ("ffbb_api_client_v2.models.competition_poule", "CompetitionPoule"),
    ("ffbb_api_client_v2.models.competition_rencontre", "CompetitionRencontre"),
    ("ffbb_api_client_v2.models.competition_type_facet", "CompetitionTypeFacet"),
    ("ffbb_api_client_v2.models.coordonnees", "Coordonnees"),
    ("ffbb_api_client_v2.models.document_flyer", "DocumentFlyer"),
    ("ffbb_api_client_v2.models.engagement_equipe", "EngagementEquipe"),
    ("ffbb_api_client_v2.models.engagement_position", "EngagementPosition"),
    ("ffbb_api_client_v2.models.external_competition", "ExternalCompetition"),
    ("ffbb_api_client_v2.models.external_rencontre", "ExternalRencontre"),
    ("ffbb_api_client_v2.models.folder", "Folder"),
    ("ffbb_api_client_v2.models.fonction", "Fonction"),
    ("ffbb_api_client_v2.models.geo", "Geo"),
    ("ffbb_api_client_v2.models.labellisation", "Labellisation"),
    ("ffbb_api_client_v2.models.labellisation_item", "LabellisationItem"),
    ("ffbb_api_client_v2.models.labellisation_programme", "LabellisationProgramme"),
    ("ffbb_api_client_v2.models.logo", "Logo"),
    ("ffbb_api_client_v2.models.membre", "Membre"),
    ("ffbb_api_client_v2.models.nature_sol", "NatureSol"),
    ("ffbb_api_client_v2.models.niveau_facet", "NiveauFacet"),
    ("ffbb_api_client_v2.models.officiel", "Officiel"),
    ("ffbb_api_client_v2.models.officiel_personne", "OfficielPersonne"),
    ("ffbb_api_client_v2.models.offre_pratique", "OffrePratique"),
    ("ffbb_api_client_v2.models.offre_pratique", "OffrePratiqueDetail"),
    ("ffbb_api_client_v2.models.organisateur", "Organisateur"),
    ("ffbb_api_client_v2.models.organisme_engagement", "OrganismeEngagement"),
    ("ffbb_api_client_v2.models.organisme_equipe", "OrganismeEquipe"),
    ("ffbb_api_client_v2.models.phase_engagement", "PhaseEngagement"),
    ("ffbb_api_client_v2.models.poule", "Poule"),
    ("ffbb_api_client_v2.models.rencontres_engagement", "Engagement"),
    ("ffbb_api_client_v2.models.saison", "Saison"),
    ("ffbb_api_client_v2.models.salle", "Salle"),
    ("ffbb_api_client_v2.models.sexe_facet", "SexeFacet"),
    ("ffbb_api_client_v2.models.tournoi_type_facet", "TournoiTypeFacet"),
    ("ffbb_api_client_v2.models.tournoi_types_3x3", "TournoiTypes3X3"),
    ("ffbb_api_client_v2.models.tournoi_types_3x3_libelle", "TournoiTypes3X3Libelle"),
    ("ffbb_api_client_v2.models.type_association", "TypeAssociation"),
    ("ffbb_api_client_v2.models.type_association_libelle", "TypeAssociationLibelle"),
    (
        "ffbb_api_client_v2.models.type_competition_generique",
        "TypeCompetitionGenerique",
    ),
    ("ffbb_api_client_v2.models.type_facet", "TypeFacet"),
]


@pytest.mark.parametrize("module_path,class_name", MODELS_WITH_TYPE_CHECK)
def test_from_dict_rejects_non_dict(module_path: str, class_name: str) -> None:
    """Verify from_dict raises TypeError/ValueError when called with non-dict."""
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    with pytest.raises((TypeError, ValueError)):
        cls.from_dict("not a dict")
