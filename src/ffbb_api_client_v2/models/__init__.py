"""Data models for FFBB API client."""

# Import existing model files (only those that actually exist)
# Snake case model files
from .affiche import Affiche
from .Cartographie import Cartographie
from .categorie import Categorie
from .code import Code
from .commune import Commune
from .competition_type import CompetitionType
from .CompetitionID import CompetitionID
from .CompetitionIDCategorie import CompetitionIDCategorie
from .CompetitionIDSexe import CompetitionIDSexe
from .CompetitionIDTypeCompetition import CompetitionIDTypeCompetition
from .CompetitionIDTypeCompetitionGenerique import CompetitionIDTypeCompetitionGenerique
from .CompetitionOrigine import CompetitionOrigine
from .CompetitionOrigineCategorie import CompetitionOrigineCategorie
from .CompetitionOrigineTypeCompetition import CompetitionOrigineTypeCompetition
from .CompetitionOrigineTypeCompetitionGenerique import (
    CompetitionOrigineTypeCompetitionGenerique,
)
from .competitions_models import CompetitionsQuery
from .coordonnees import Coordonnees
from .CoordonneesType import CoordonneesType
from .DocumentFlyer import DocumentFlyer
from .DocumentFlyerType import DocumentFlyerType
from .etat import Etat
from .external_id import ExternalID
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .folder import Folder
from .geo import Geo
from .GradientColor import GradientColor
from .hit import Hit
from .IDEngagementEquipe import IDEngagementEquipe
from .IDOrganismeEquipe import IDOrganismeEquipe
from .IDOrganismeEquipe1Logo import IDOrganismeEquipe1Logo
from .IDPoule import IDPoule
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
from .multi_search_results import MultiSearchResult, multi_search_results_from_dict
from .MultiSearchResultCompetitions import MultiSearchResultCompetitions
from .MultiSearchResultOrganismes import MultiSearchResultOrganismes
from .MultiSearchResultPratiques import MultiSearchResultPratiques
from .MultiSearchResultRencontres import MultiSearchResultRencontres
from .MultiSearchResults import MultiSearchResults
from .MultiSearchResultSalles import MultiSearchResultSalles
from .MultiSearchResultTerrains import MultiSearchResultTerrains
from .MultiSearchResultTournois import MultiSearchResultTournois
from .NatureSol import NatureSol
from .niveau import Niveau
from .NiveauClass import NiveauClass
from .objectif import Objectif
from .Organisateur import Organisateur
from .OrganisateurType import OrganisateurType
from .OrganismeIDPere import OrganismeIDPere
from .organismes_models import GetOrganismeResponse, OrganismesQuery
from .PhaseCode import PhaseCode
from .poule import Poule
from .poules_models import GetPouleResponse, PoulesQuery
from .pratique import Pratique
from .PublicationInternet import PublicationInternet
from .PurpleLogo import PurpleLogo
from .query_fields import QueryFields
from .saison import Saison
from .saisons_models import GetSaisonsResponse, SaisonsQuery
from .salle import Salle
from .sexe import Sexe
from .source import Source
from .status import Status
from .TeamEngagement import TeamEngagement
from .TournoiTypeClass import TournoiTypeClass
from .TournoiTypeEnum import TournoiTypeEnum
from .TypeAssociation import TypeAssociation
from .TypeAssociationLibelle import TypeAssociationLibelle
from .TypeClass import TypeClass
from .TypeCompetition import TypeCompetition
from .TypeCompetitionGenerique import TypeCompetitionGenerique
from .TypeEnum import TypeEnum
from .TypeLeague import TypeLeague

__all__ = [
    # PascalCase classes
    "Cartographie",
    "CompetitionID",
    "CompetitionIDCategorie",
    "CompetitionIDSexe",
    "CompetitionIDTypeCompetition",
    "CompetitionIDTypeCompetitionGenerique",
    "CompetitionOrigine",
    "CompetitionOrigineCategorie",
    "CompetitionOrigineTypeCompetition",
    "CompetitionOrigineTypeCompetitionGenerique",
    "CoordonneesType",
    "DocumentFlyer",
    "DocumentFlyerType",
    "FacetDistribution",
    "FacetStats",
    "GradientColor",
    "IDEngagementEquipe",
    "IDOrganismeEquipe",
    "IDOrganismeEquipe1Logo",
    "IDPoule",
    "MultiSearchResultCompetitions",
    "MultiSearchResultOrganismes",
    "MultiSearchResultPratiques",
    "MultiSearchResultRencontres",
    "MultiSearchResultSalles",
    "MultiSearchResultTerrains",
    "MultiSearchResultTournois",
    "MultiSearchResults",
    "NatureSol",
    "NiveauClass",
    "Organisateur",
    "OrganisateurType",
    "OrganismeIDPere",
    "PhaseCode",
    "PublicationInternet",
    "PurpleLogo",
    "TeamEngagement",
    "TournoiTypeClass",
    "TournoiTypeEnum",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeClass",
    "TypeCompetition",
    "TypeCompetitionGenerique",
    "TypeEnum",
    "TypeLeague",
    # Snake case classes
    "Affiche",
    "Categorie",
    "Clock",
    "Code",
    "Commune",
    "CompetitionType",
    "CompetitionsMultiSearchQuery",
    "CompetitionsMultiSearchResult",
    "CompetitionsQuery",
    "Coordonnees",
    "Etat",
    "ExternalID",
    "Folder",
    "Geo",
    "GetCompetitionsResponse",
    "GetOrganismeResponse",
    "GetPouleResponse",
    "GetSaisonsResponse",
    "Hit",
    "Jour",
    "Label",
    "Labellisation",
    "Live",
    "Logo",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResult",
    "Niveau",
    "Objectif",
    "OrganismesMultiSearchQuery",
    "OrganismesMultiSearchResult",
    "OrganismesQuery",
    "Poule",
    "PoulesQuery",
    "Pratique",
    "PratiquesMultiSearchQuery",
    "PratiquesMultiSearchResult",
    "QueryFields",
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
    "TerrainsMultiSearchQuery",
    "TerrainsMultiSearchResult",
    "TournoisMultiSearchQuery",
    "TournoisMultiSearchResult",
    # Functions
    "lives_from_dict",
    "lives_to_dict",
    "multi_search_results_from_dict",
]
