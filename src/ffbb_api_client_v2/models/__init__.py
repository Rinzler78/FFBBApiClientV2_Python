"""Data models for FFBB API client."""

# Import existing model files (all now in snake_case)
from .affiche import Affiche
from .cartographie import Cartographie
from .categorie import Categorie
from .code import Code
from .commune import Commune
from .competition_id import CompetitionID
from .competition_id_categorie import CompetitionIDCategorie
from .competition_id_sexe import CompetitionIDSexe
from .competition_id_type_competition import CompetitionIDTypeCompetition
from .competition_id_type_competition_generique import (
    CompetitionIDTypeCompetitionGenerique,
)
from .competition_origine import CompetitionOrigine
from .competition_origine_categorie import CompetitionOrigineCategorie
from .competition_origine_type_competition import CompetitionOrigineTypeCompetition
from .competition_origine_type_competition_generique import (
    CompetitionOrigineTypeCompetitionGenerique,
)
from .competition_type import CompetitionType
from .competitions_models import CompetitionsQuery, GetCompetitionResponse
from .coordonnees import Coordonnees
from .coordonnees_type import CoordonneesType
from .document_flyer import DocumentFlyer
from .document_flyer_type import DocumentFlyerType
from .etat import Etat
from .external_id import ExternalID
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .folder import Folder
from .game_stats_models import GameStatsModel
from .geo import Geo
from .gradient_color import GradientColor
from .hit import Hit
from .id_engagement_equipe import IDEngagementEquipe
from .id_organisme_equipe import IDOrganismeEquipe
from .id_organisme_equipe1_logo import IDOrganismeEquipe1Logo
from .id_poule import IDPoule
from .jour import Jour
from .label import Label
from .labellisation import Labellisation
from .lives import Clock, Live, lives_from_dict, lives_to_dict
from .logo import Logo
from .multi_search_queries import MultiSearchQueries
from .multi_search_query import (
    CompetitionsMultiSearchQuery,
    MultiSearchQuery,
    OrganismesMultiSearchQuery,
    PratiquesMultiSearchQuery,
    RencontresMultiSearchQuery,
    SallesMultiSearchQuery,
    TerrainsMultiSearchQuery,
    TournoisMultiSearchQuery,
)
from .multi_search_result_competitions import CompetitionsMultiSearchResult
from .multi_search_result_organismes import OrganismesMultiSearchResult
from .multi_search_result_pratiques import PratiquesMultiSearchResult
from .multi_search_result_rencontres import RencontresMultiSearchResult
from .multi_search_result_salles import SallesMultiSearchResult
from .multi_search_result_terrains import TerrainsMultiSearchResult
from .multi_search_result_tournois import TournoisMultiSearchResult
from .multi_search_results import MultiSearchResult
from .multi_search_results_class import multi_search_results_from_dict
from .nature_sol import NatureSol
from .niveau import Niveau
from .niveau_class import NiveauClass
from .objectif import Objectif
from .organisateur import Organisateur
from .organisateur_type import OrganisateurType
from .organisme_id_pere import OrganismeIDPere
from .organismes_models import GetOrganismeResponse, OrganismesQuery
from .phase_code import PhaseCode
from .poule import Poule
from .poules_models import GetPouleResponse, PoulesQuery
from .pratique import Pratique
from .publication_internet import PublicationInternet
from .purple_logo import PurpleLogo
from .query_fields import (
    CompetitionFields,
    FieldSet,
    OrganismeFields,
    PouleFields,
    QueryFieldsManager,
    SaisonFields,
)
from .rankings_models import RankingEngagement, TeamRanking
from .saison import Saison
from .saisons_models import GetSaisonsResponse, SaisonsQuery
from .salle import Salle
from .sexe import Sexe
from .source import Source
from .status import Status
from .team_engagement import TeamEngagement
from .tournoi_type_class import TournoiTypeClass
from .tournoi_type_enum import TournoiTypeEnum
from .type_association import TypeAssociation
from .type_association_libelle import TypeAssociationLibelle
from .type_class import TypeClass
from .type_competition import TypeCompetition
from .type_competition_generique import TypeCompetitionGenerique
from .type_enum import TypeEnum
from .type_league import TypeLeague

__all__ = [
    # Classes from snake_case files
    "Affiche",
    "Cartographie",
    "Categorie",
    "Clock",
    "Code",
    "Commune",
    "CompetitionID",
    "CompetitionIDCategorie",
    "CompetitionIDSexe",
    "CompetitionIDTypeCompetition",
    "CompetitionIDTypeCompetitionGenerique",
    "CompetitionOrigine",
    "CompetitionOrigineCategorie",
    "CompetitionOrigineTypeCompetition",
    "CompetitionOrigineTypeCompetitionGenerique",
    "CompetitionType",
    "CompetitionsMultiSearchQuery",
    "CompetitionsMultiSearchResult",
    "CompetitionsQuery",
    "Coordonnees",
    "CoordonneesType",
    "DocumentFlyer",
    "DocumentFlyerType",
    "Etat",
    "ExternalID",
    "FacetDistribution",
    "FacetStats",
    "Folder",
    "GameStatsModel",
    "Geo",
    "GetCompetitionResponse",
    "GetOrganismeResponse",
    "GetPouleResponse",
    "GetSaisonsResponse",
    "GradientColor",
    "Hit",
    "IDEngagementEquipe",
    "IDOrganismeEquipe",
    "IDOrganismeEquipe1Logo",
    "IDPoule",
    "Jour",
    "Label",
    "Labellisation",
    "Live",
    "Logo",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResult",
    "NatureSol",
    "Niveau",
    "NiveauClass",
    "Objectif",
    "Organisateur",
    "OrganisateurType",
    "OrganismeIDPere",
    "OrganismesMultiSearchQuery",
    "OrganismesMultiSearchResult",
    "OrganismesQuery",
    "PhaseCode",
    "Poule",
    "PoulesQuery",
    "Pratique",
    "RankingEngagement",
    "PratiquesMultiSearchQuery",
    "PratiquesMultiSearchResult",
    "PublicationInternet",
    "PurpleLogo",
    "QueryFieldsManager",
    "OrganismeFields",
    "CompetitionFields",
    "PouleFields",
    "SaisonFields",
    "FieldSet",
    "RencontresMultiSearchQuery",
    "RencontresMultiSearchResult",
    "Saison",
    "SaisonsQuery",
    "Salle",
    "SallesMultiSearchQuery",
    "SallesMultiSearchResult",
    "Sexe",
    "Source",
    "Status",
    "TeamEngagement",
    "TerrainsMultiSearchQuery",
    "TerrainsMultiSearchResult",
    "TournoisMultiSearchQuery",
    "TeamRanking",
    "TournoisMultiSearchResult",
    "TournoiTypeClass",
    "TournoiTypeEnum",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeClass",
    "TypeCompetition",
    "TypeCompetitionGenerique",
    "TypeEnum",
    "TypeLeague",
    # Functions
    "lives_from_dict",
    "lives_to_dict",
    "multi_search_results_from_dict",
]
