"""Data models for FFBB API client."""

# Import all model classes for easy access
from .Affiche import Affiche
from .Cartographie import Cartographie
from .Categorie import Categorie
from .Code import Code
from .Commune import Commune
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
from .Coordonnees import Coordonnees
from .CoordonneesType import CoordonneesType
from .DocumentFlyer import DocumentFlyer
from .DocumentFlyerType import DocumentFlyerType
from .Etat import Etat
from .external_id import ExternalID
from .FacetDistribution import FacetDistribution
from .FacetStats import FacetStats
from .Folder import Folder
from .Geo import Geo
from .GradientColor import GradientColor
from .Hit import Hit
from .IDEngagementEquipe import IDEngagementEquipe
from .IDOrganismeEquipe import IDOrganismeEquipe
from .IDOrganismeEquipe1Logo import IDOrganismeEquipe1Logo
from .IDPoule import IDPoule
from .Jour import Jour
from .Label import Label
from .Labellisation import Labellisation
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

# Fixed import for multi search results
from .multi_search_results import MultiSearchResult as MSR
from .MultiSearchResults import MultiSearchResults, multi_search_results_from_dict
from .NatureSol import NatureSol
from .Niveau import Niveau
from .NiveauClass import NiveauClass
from .Objectif import Objectif
from .Organisateur import Organisateur
from .OrganisateurType import OrganisateurType
from .OrganismeIDPere import OrganismeIDPere
from .PhaseCode import PhaseCode
from .Poule import Poule
from .Pratique import Pratique
from .PublicationInternet import PublicationInternet
from .PurpleLogo import PurpleLogo
from .Saison import Saison
from .salle import Salle
from .Sexe import Sexe
from .Source import Source
from .Status import Status
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
    "Coordonnees",
    "CoordonneesType",
    "DocumentFlyer",
    "DocumentFlyerType",
    "Etat",
    "ExternalID",
    "FacetDistribution",
    "FacetStats",
    "Folder",
    "Geo",
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
    "MSR",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResultCompetitions",
    "MultiSearchResultOrganismes",
    "MultiSearchResultPratiques",
    "MultiSearchResultRencontres",
    "MultiSearchResultSalles",
    "MultiSearchResultTerrains",
    "MultiSearchResultTournois",
    "MultiSearchResults",
    "NatureSol",
    "Niveau",
    "NiveauClass",
    "Objectif",
    "Organisateur",
    "OrganisateurType",
    "OrganismesMultiSearchQuery",
    "OrganismeIDPere",
    "PhaseCode",
    "Poule",
    "Pratique",
    "PratiquesMultiSearchQuery",
    "PublicationInternet",
    "PurpleLogo",
    "RencontresMultiSearchQuery",
    "Saison",
    "Salle",
    "SallesMultiSearchQuery",
    "Sexe",
    "Source",
    "Status",
    "TeamEngagement",
    "TerrainsMultiSearchQuery",
    "TournoiTypeClass",
    "TournoiTypeEnum",
    "TournoisMultiSearchQuery",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeClass",
    "TypeCompetition",
    "TypeCompetitionGenerique",
    "TypeEnum",
    "TypeLeague",
    "lives_from_dict",
    "lives_to_dict",
    "multi_search_results_from_dict",
]
