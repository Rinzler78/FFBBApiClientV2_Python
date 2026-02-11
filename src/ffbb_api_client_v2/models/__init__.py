"""Data models for FFBB API client."""

# Import existing model files (all now in snake_case)
from .affiche import Affiche
from .cartographie import Cartographie
from .categorie import Categorie
from .categorie_code import CategorieCode
from .clock import Clock
from .code import Code
from .commune import Commune
from .communes_fields import CommunesFields
from .competition_fields import CompetitionFields
from .competition_id import CompetitionID
from .competition_id_categorie import CompetitionIDCategorie
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
from .competition_phase import CompetitionPhase
from .competition_poule import CompetitionPoule
from .competition_ref import CompetitionRef
from .competition_rencontre import CompetitionRencontre
from .competition_type import CompetitionType
from .competitions_facet_distribution import CompetitionsFacetDistribution
from .competitions_multi_search_query import CompetitionsMultiSearchQuery
from .competitions_query import CompetitionsQuery
from .coordonnees import Coordonnees
from .coordonnees_type import CoordonneesType
from .document_flyer import DocumentFlyer
from .document_flyer_type import DocumentFlyerType
from .engagement_equipe import EngagementEquipe
from .engagements_fields import EngagementsFields
from .entraineurs_fields import EntraineursFields
from .etat import Etat
from .external_competition_id import ExternalCompetitionID
from .external_id import ExternalID
from .facet_distribution import FacetDistribution
from .facet_stats import FacetStats
from .field_set import FieldSet
from .folder import Folder
from .fonction import Fonction
from .formations_fields import FormationsFields
from .game_stats_model import GameStatsModel
from .geo import Geo
from .get_communes_response import GetCommunesResponse
from .get_competition_response import GetCompetitionResponse
from .get_configuration_response import GetConfigurationResponse
from .get_engagements_response import GetEngagementsResponse
from .get_entraineurs_response import GetEntraineursResponse
from .get_formations_response import GetFormationsResponse
from .get_officiels_response import GetOfficielsResponse
from .get_organisme_response import GetOrganismeResponse
from .get_poule_response import GetPouleResponse
from .get_pratiques_response import GetPratiquesResponse
from .get_rencontres_response import GetRencontresResponse
from .get_salles_response import GetSallesResponse
from .get_terrains_response import GetTerrainsResponse
from .get_tournois_response import GetTournoisResponse
from .id_engagement_equipe import IDEngagementEquipe
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .jour import Jour
from .label import Label
from .labellisation import Labellisation
from .labellisation_item import LabellisationItem
from .labellisation_programme import LabellisationProgramme
from .live import Live, lives_from_dict
from .logo import Logo
from .membre import Membre
from .multi_search_queries import MultiSearchQueries
from .multi_search_query import MultiSearchQuery
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
from .officiel import Officiel
from .officiel_personne import OfficielPersonne
from .officiels_fields import OfficielsFields
from .offre_pratique import OffrePratique, OffrePratiqueDetail
from .organisateur import Organisateur
from .organisateur_type import OrganisateurType
from .organisme_engagement import OrganismeEngagement
from .organisme_equipe import OrganismeEquipe
from .organisme_fields import OrganismeFields
from .organisme_id import OrganismeId
from .organisme_id_pere import OrganismeIDPere
from .organismes_multi_search_query import OrganismesMultiSearchQuery
from .organismes_query import OrganismesQuery
from .phase_code import PhaseCode
from .phase_engagement import PhaseEngagement
from .poule import Poule
from .poule_fields import PouleFields
from .poules_query import PoulesQuery
from .pratique import Pratique
from .pratiques_fields import PratiquesFields
from .pratiques_multi_search_query import PratiquesMultiSearchQuery
from .pratiques_type_class import PratiquesTypeClass
from .publication_internet import PublicationInternet
from .purple_logo import PurpleLogo
from .query_fields_manager import QueryFieldsManager
from .ranking_engagement import RankingEngagement
from .rencontres_fields import RencontresFields
from .rencontres_multi_search_query import RencontresMultiSearchQuery
from .saison import Saison
from .saison_fields import SaisonFields
from .saisons_query import SaisonsQuery
from .salle import Salle
from .salles_fields import SallesFields
from .salles_multi_search_query import SallesMultiSearchQuery
from .sexe import Sexe
from .sexe_class import SexeClass
from .source import Source
from .status import Status
from .team_engagement import TeamEngagement
from .team_ranking import TeamRanking
from .terrains_facet_distribution import TerrainsFacetDistribution
from .terrains_fields import TerrainsFields
from .terrains_multi_search_query import TerrainsMultiSearchQuery
from .tournoi_type_class import TournoiTypeClass
from .tournoi_type_enum import TournoiTypeEnum
from .tournois_fields import TournoisFields
from .tournois_multi_search_query import TournoisMultiSearchQuery
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
    "CategorieCode",
    "Clock",
    "Code",
    "Commune",
    "CommunesFields",
    "CompetitionFields",
    "CompetitionID",
    "CompetitionIDCategorie",
    "CompetitionIDTypeCompetition",
    "CompetitionIDTypeCompetitionGenerique",
    "CompetitionOrigine",
    "CompetitionOrigineCategorie",
    "CompetitionOrigineTypeCompetition",
    "CompetitionOrigineTypeCompetitionGenerique",
    "CompetitionPhase",
    "CompetitionPoule",
    "CompetitionRef",
    "CompetitionRencontre",
    "CompetitionType",
    "CompetitionsFacetDistribution",
    "CompetitionsMultiSearchQuery",
    "CompetitionsMultiSearchResult",
    "CompetitionsQuery",
    "Coordonnees",
    "CoordonneesType",
    "DocumentFlyer",
    "DocumentFlyerType",
    "EngagementEquipe",
    "EngagementsFields",
    "EntraineursFields",
    "Etat",
    "ExternalCompetitionID",
    "ExternalID",
    "FacetDistribution",
    "FacetStats",
    "FieldSet",
    "Folder",
    "Fonction",
    "FormationsFields",
    "GameStatsModel",
    "Geo",
    "GetCommunesResponse",
    "GetCompetitionResponse",
    "GetConfigurationResponse",
    "GetEngagementsResponse",
    "GetEntraineursResponse",
    "GetFormationsResponse",
    "GetOfficielsResponse",
    "GetOrganismeResponse",
    "GetPouleResponse",
    "GetPratiquesResponse",
    "GetRencontresResponse",
    "GetSallesResponse",
    "GetTerrainsResponse",
    "GetTournoisResponse",
    "IDEngagementEquipe",
    "IDOrganismeEquipe",
    "IDPoule",
    "Jour",
    "Label",
    "Labellisation",
    "LabellisationItem",
    "LabellisationProgramme",
    "Live",
    "Logo",
    "Membre",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResult",
    "NatureSol",
    "Niveau",
    "NiveauClass",
    "Objectif",
    "Officiel",
    "OfficielPersonne",
    "OfficielsFields",
    "OffrePratique",
    "OffrePratiqueDetail",
    "Organisateur",
    "OrganisateurType",
    "OrganismeEngagement",
    "OrganismeEquipe",
    "OrganismeFields",
    "OrganismeId",
    "OrganismeIDPere",
    "OrganismesMultiSearchQuery",
    "OrganismesMultiSearchResult",
    "OrganismesQuery",
    "PhaseCode",
    "PhaseEngagement",
    "Poule",
    "PouleFields",
    "PoulesQuery",
    "Pratique",
    "PratiquesFields",
    "PratiquesMultiSearchQuery",
    "PratiquesMultiSearchResult",
    "PratiquesTypeClass",
    "PublicationInternet",
    "PurpleLogo",
    "QueryFieldsManager",
    "RankingEngagement",
    "RencontresFields",
    "RencontresMultiSearchQuery",
    "RencontresMultiSearchResult",
    "Saison",
    "SaisonFields",
    "SaisonsQuery",
    "Salle",
    "SallesFields",
    "SallesMultiSearchQuery",
    "SallesMultiSearchResult",
    "Sexe",
    "SexeClass",
    "Source",
    "Status",
    "TeamEngagement",
    "TeamRanking",
    "TerrainsFacetDistribution",
    "TerrainsFields",
    "TerrainsMultiSearchQuery",
    "TerrainsMultiSearchResult",
    "TournoisFields",
    "TournoisMultiSearchQuery",
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
    "multi_search_results_from_dict",
]
