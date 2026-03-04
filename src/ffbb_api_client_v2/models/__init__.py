"""Data models for FFBB API client."""

# Meilisearch generic models
from ..meilisearch.models.facet_distribution import FacetDistribution
from ..meilisearch.models.facet_stats import FacetStats
from ..meilisearch.models.multi_search_queries import MultiSearchQueries
from ..meilisearch.models.multi_search_query import MultiSearchQuery
from ..meilisearch.models.multi_search_results import MultiSearchResult
from ..meilisearch.models.multi_search_results_class import (
    multi_search_results_from_dict,
)

# Shared domain models
from .affiche import Affiche
from .age_group_enum import AgeGroupEnum
from .cartographie import Cartographie
from .categorie import Categorie
from .categorie_code import CategorieCode
from .categorie_type_enum import CategorieTypeEnum
from .clock import Clock
from .club_contacts import ClubContacts
from .code_enum import CodeEnum
from .code_fonction_enum import CODE_FONCTION_TO_CONTACT_ROLE, CodeFonctionEnum
from .commune import Commune
from .competition import Competition
from .competition_base import CompetitionBase
from .competition_detail import CompetitionDetail
from .competition_origine import CompetitionOrigine
from .competition_origine_categorie import CompetitionOrigineCategorie
from .competition_origine_type_competition_enum import (
    CompetitionOrigineTypeCompetitionEnum,
)
from .competition_phase import CompetitionPhase
from .competition_poule import CompetitionPoule
from .competition_rencontre import CompetitionRencontre
from .competition_type_enum import CompetitionTypeEnum
from .competition_type_facet import CompetitionTypeFacet
from .contact_info import ContactInfo
from .contact_role_enum import ContactRoleEnum
from .coordonnees import Coordonnees
from .coordonnees_type_enum import CoordonneesTypeEnum
from .document_flyer import DocumentFlyer
from .document_flyer_type_enum import DocumentFlyerTypeEnum
from .echelon_enum import EchelonEnum
from .engagement_contacts import EngagementContacts
from .engagement_equipe import EngagementEquipe
from .engagement_position import EngagementPosition
from .etat_enum import EtatEnum
from .external_competition import ExternalCompetition
from .external_rencontre import ExternalRencontre
from .folder import Folder
from .fonction import Fonction
from .game_stats_model import GameStatsModel
from .gender_enum import GenderEnum
from .geo import Geo
from .jour_enum import JourEnum
from .label_enum import LabelEnum
from .labellisation import Labellisation
from .labellisation_item import LabellisationItem
from .labellisation_programme import LabellisationProgramme
from .logo import Logo
from .membre import Membre
from .nature_sol import NatureSol
from .niveau_enum import NiveauEnum
from .niveau_extractor import NiveauExtractor
from .niveau_facet import NiveauFacet
from .niveau_info import NiveauInfo
from .niveau_type_enum import NiveauTypeEnum
from .objectif_enum import ObjectifEnum
from .officiel import Officiel
from .officiel_personne import OfficielPersonne
from .offre_pratique import OffrePratique, OffrePratiqueDetail
from .organisateur import Organisateur
from .organisateur_type_enum import OrganisateurTypeEnum
from .organisme_engagement import OrganismeEngagement
from .organisme_equipe import OrganismeEquipe
from .phase_code_enum import PhaseCodeEnum
from .phase_engagement import PhaseEngagement
from .phone_number import PhoneNumber
from .poule import Poule
from .pratique_enum import PratiqueEnum
from .pratiques_hit_type_enum import PratiquesHitTypeEnum
from .publication_internet_enum import PublicationInternetEnum
from .ranking_engagement import RankingEngagement
from .rencontres_engagement import Engagement
from .saison import Saison
from .salle import Salle
from .sexe_enum import SexeEnum
from .sexe_facet import SexeFacet
from .source_enum import SourceEnum
from .status_enum import StatusEnum
from .team_ranking import TeamRanking
from .terrains_categorie_championnat_3x3_libelle_enum import (
    CategorieChampionnat3X3LibelleEnum,
)
from .tournoi_type_enum import TournoiTypeEnum
from .tournoi_type_facet import TournoiTypeFacet
from .tournoi_types_3x3 import TournoiTypes3X3
from .tournoi_types_3x3_libelle import TournoiTypes3X3Libelle
from .tournoi_types_3x3_libelle_enum import TournoiTypes3x3LibelleEnum
from .tournois_hit_type_enum import TournoisHitTypeEnum
from .type_association import TypeAssociation
from .type_association_libelle import TypeAssociationLibelle
from .type_competition_enum import TypeCompetitionEnum
from .type_competition_generique import TypeCompetitionGenerique
from .type_enum import TypeEnum
from .type_facet import TypeFacet
from .type_league_enum import TypeLeagueEnum

__all__ = [
    # Meilisearch generic
    "FacetDistribution",
    "FacetStats",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResult",
    "multi_search_results_from_dict",
    # Shared domain models
    "Affiche",
    "AgeGroupEnum",
    "Cartographie",
    "Categorie",
    "CategorieChampionnat3X3LibelleEnum",
    "CategorieCode",
    "CategorieTypeEnum",
    "Clock",
    "ClubContacts",
    "CODE_FONCTION_TO_CONTACT_ROLE",
    "CodeEnum",
    "CodeFonctionEnum",
    "Commune",
    "Competition",
    "CompetitionBase",
    "CompetitionDetail",
    "CompetitionOrigine",
    "CompetitionOrigineCategorie",
    "CompetitionOrigineTypeCompetitionEnum",
    "CompetitionPhase",
    "CompetitionPoule",
    "CompetitionRencontre",
    "CompetitionTypeEnum",
    "CompetitionTypeFacet",
    "ContactInfo",
    "ContactRoleEnum",
    "Coordonnees",
    "CoordonneesTypeEnum",
    "DocumentFlyer",
    "DocumentFlyerTypeEnum",
    "EchelonEnum",
    "Engagement",
    "EngagementContacts",
    "EngagementEquipe",
    "EngagementPosition",
    "EtatEnum",
    "ExternalCompetition",
    "ExternalRencontre",
    "Folder",
    "Fonction",
    "GameStatsModel",
    "GenderEnum",
    "Geo",
    "JourEnum",
    "LabelEnum",
    "Labellisation",
    "LabellisationItem",
    "LabellisationProgramme",
    "Logo",
    "Membre",
    "NatureSol",
    "NiveauEnum",
    "NiveauExtractor",
    "NiveauFacet",
    "NiveauInfo",
    "NiveauTypeEnum",
    "ObjectifEnum",
    "Officiel",
    "OfficielPersonne",
    "OffrePratique",
    "OffrePratiqueDetail",
    "Organisateur",
    "OrganisateurTypeEnum",
    "OrganismeEngagement",
    "OrganismeEquipe",
    "PhaseCodeEnum",
    "PhaseEngagement",
    "PhoneNumber",
    "Poule",
    "PratiqueEnum",
    "PratiquesHitTypeEnum",
    "PublicationInternetEnum",
    "RankingEngagement",
    "Saison",
    "Salle",
    "SexeEnum",
    "SexeFacet",
    "SourceEnum",
    "StatusEnum",
    "TeamRanking",
    "TournoiTypeEnum",
    "TournoiTypeFacet",
    "TournoiTypes3X3",
    "TournoiTypes3X3Libelle",
    "TournoiTypes3x3LibelleEnum",
    "TournoisHitTypeEnum",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeCompetitionEnum",
    "TypeCompetitionGenerique",
    "TypeEnum",
    "TypeFacet",
    "TypeLeagueEnum",
]
