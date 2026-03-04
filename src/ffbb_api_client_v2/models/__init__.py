"""Data models for FFBB API client."""

# Shared domain models (used by both Directus and Meilisearch layers)
# Meilisearch generic models (will move to meilisearch/ in Phase 4)
from ..meilisearch.models.facet_distribution import FacetDistribution
from ..meilisearch.models.facet_stats import FacetStats
from ..meilisearch.models.multi_search_queries import MultiSearchQueries
from ..meilisearch.models.multi_search_query import MultiSearchQuery
from ..meilisearch.models.multi_search_results import MultiSearchResult
from ..meilisearch.models.multi_search_results_class import (
    multi_search_results_from_dict,
)
from .affiche import Affiche
from .age_group_enum import AgeGroupEnum
from .cartographie import Cartographie
from .categorie import Categorie
from .categorie_code import CategorieCode
from .clock import Clock
from .club_contacts import ClubContacts
from .code_enum import CodeEnum
from .code_fonction_enum import CODE_FONCTION_TO_CONTACT_ROLE, CodeFonctionEnum
from .commune import Commune
from .competition import Competition
from .competition_base import CompetitionBase
from .competition_detail import CompetitionDetail
from .competition_origine import CompetitionOrigine
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
from .echelon_enum import EchelonEnum
from .engagement_contacts import (
    EngagementContacts,
)
from .engagement_equipe import EngagementEquipe
from .etat_enum import EtatEnum
from .external_competition_id import ExternalCompetitionID
from .external_id import ExternalID
from .folder import Folder
from .fonction import Fonction
from .gender_enum import GenderEnum
from .geo import Geo
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .jour_enum import JourEnum
from .label_enum import LabelEnum
from .labellisation import Labellisation
from .labellisation_item import LabellisationItem
from .labellisation_programme import LabellisationProgramme
from .logo import Logo
from .membre import Membre
from .nature_sol import NatureSol
from .niveau_enum import NiveauEnum
from .objectif_enum import ObjectifEnum
from .officiel import Officiel
from .officiel_personne import OfficielPersonne
from .offre_pratique import OffrePratique, OffrePratiqueDetail
from .organisateur import Organisateur
from .organisateur_type_enum import OrganisateurTypeEnum
from .organisme_engagement import OrganismeEngagement
from .phase_code_enum import PhaseCodeEnum
from .phase_engagement import PhaseEngagement
from .poule import Poule
from .pratique_enum import PratiqueEnum
from .publication_internet_enum import PublicationInternetEnum
from .ranking_engagement import RankingEngagement
from .saison import Saison
from .salle import Salle
from .sexe_class import SexeClass
from .sexe_enum import SexeEnum
from .source_enum import SourceEnum
from .status_enum import StatusEnum
from .team_ranking import TeamRanking
from .tournoi_type_class import TournoiTypeClass
from .tournoi_type_enum import TournoiTypeEnum
from .type_association import TypeAssociation
from .type_association_libelle import TypeAssociationLibelle
from .type_class import TypeClass
from .type_competition_enum import TypeCompetitionEnum
from .type_competition_generique import (
    TypeCompetitionGenerique,
)
from .type_enum import TypeEnum
from .type_league_enum import TypeLeagueEnum

__all__ = [
    # Shared domain models
    "AgeGroupEnum",
    "Affiche",
    "Cartographie",
    "Categorie",
    "CategorieCode",
    "ClubContacts",
    "Clock",
    "CODE_FONCTION_TO_CONTACT_ROLE",
    "CodeFonctionEnum",
    "ContactInfo",
    "ContactRoleEnum",
    "CodeEnum",
    "Commune",
    "Competition",
    "CompetitionBase",
    "Categorie",
    "CompetitionTypeFacet",
    "TypeCompetitionGenerique",
    "CompetitionOrigine",
    "CompetitionOrigineTypeCompetitionEnum",
    "TypeCompetitionGenerique",
    "CompetitionPhase",
    "CompetitionPoule",
    "CompetitionDetail",
    "CompetitionRencontre",
    "CompetitionTypeEnum",
    "Coordonnees",
    "CoordonneesTypeEnum",
    "DocumentFlyer",
    "EngagementContacts",
    "EngagementEquipe",
    "EchelonEnum",
    "EtatEnum",
    "ExternalCompetitionID",
    "ExternalID",
    "Folder",
    "Fonction",
    "GenderEnum",
    "Geo",
    "EngagementEquipe",
    "IDOrganismeEquipe",
    "IDPoule",
    "JourEnum",
    "LabelEnum",
    "Labellisation",
    "LabellisationItem",
    "LabellisationProgramme",
    "Logo",
    "Membre",
    "NatureSol",
    "NiveauEnum",
    "ObjectifEnum",
    "Officiel",
    "OfficielPersonne",
    "OffrePratique",
    "OffrePratiqueDetail",
    "Organisateur",
    "OrganisateurTypeEnum",
    "OrganismeEngagement",
    "IDOrganismeEquipe",
    "Organisateur",
    "PhaseCodeEnum",
    "PhaseEngagement",
    "Poule",
    "PratiqueEnum",
    "PublicationInternetEnum",
    "Logo",
    "RankingEngagement",
    "Saison",
    "Salle",
    "SexeEnum",
    "SexeClass",
    "SourceEnum",
    "StatusEnum",
    "EngagementEquipe",
    "TeamRanking",
    "TournoiTypeClass",
    "TournoiTypeEnum",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeClass",
    "TypeCompetitionEnum",
    "TypeCompetitionGenerique",
    "TypeEnum",
    "TypeLeagueEnum",
    # Meilisearch generic
    "FacetDistribution",
    "FacetStats",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResult",
    "multi_search_results_from_dict",
]
