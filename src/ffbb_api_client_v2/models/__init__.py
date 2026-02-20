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
from .age_group import AgeGroup
from .cartographie import Cartographie
from .categorie import Categorie
from .categorie_code import CategorieCode
from .clock import Clock
from .club_contacts import ClubContacts
from .code import Code
from .code_fonction import CODE_FONCTION_TO_CONTACT_ROLE, CodeFonction
from .commune import Commune
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
from .contact_info import ContactInfo
from .contact_role import ContactRole
from .coordonnees import Coordonnees
from .coordonnees_type import CoordonneesType
from .document_flyer import DocumentFlyer
from .document_flyer_type import DocumentFlyerType
from .echelon import Echelon
from .engagement_contacts import (
    EngagementContacts,
)
from .engagement_equipe import EngagementEquipe
from .etat import Etat
from .external_competition_id import ExternalCompetitionID
from .external_id import ExternalID
from .folder import Folder
from .fonction import Fonction
from .gender import Gender
from .geo import Geo
from .id_engagement_equipe import IDEngagementEquipe
from .id_organisme_equipe import IDOrganismeEquipe
from .id_poule import IDPoule
from .jour import Jour
from .label import Label
from .labellisation import Labellisation
from .labellisation_item import LabellisationItem
from .labellisation_programme import LabellisationProgramme
from .logo import Logo
from .membre import Membre
from .nature_sol import NatureSol
from .niveau import Niveau
from .objectif import Objectif
from .officiel import Officiel
from .officiel_personne import OfficielPersonne
from .offre_pratique import OffrePratique, OffrePratiqueDetail
from .organisateur import Organisateur
from .organisateur_type import OrganisateurType
from .organisme_engagement import OrganismeEngagement
from .organisme_equipe import OrganismeEquipe
from .organisme_id import OrganismeId
from .organisme_id_pere import OrganismeIDPere
from .phase_code import PhaseCode
from .phase_engagement import PhaseEngagement
from .poule import Poule
from .pratique import Pratique
from .publication_internet import PublicationInternet
from .purple_logo import PurpleLogo
from .ranking_engagement import RankingEngagement
from .saison import Saison
from .salle import Salle
from .sexe import Sexe
from .sexe_class import SexeClass
from .source import Source
from .status import Status
from .team_engagement import TeamEngagement
from .team_ranking import TeamRanking
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
    # Shared domain models
    "AgeGroup",
    "Affiche",
    "Cartographie",
    "Categorie",
    "CategorieCode",
    "ClubContacts",
    "Clock",
    "CODE_FONCTION_TO_CONTACT_ROLE",
    "CodeFonction",
    "ContactInfo",
    "ContactRole",
    "Code",
    "Commune",
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
    "Coordonnees",
    "CoordonneesType",
    "DocumentFlyer",
    "DocumentFlyerType",
    "EngagementContacts",
    "EngagementEquipe",
    "Echelon",
    "Etat",
    "ExternalCompetitionID",
    "ExternalID",
    "Folder",
    "Fonction",
    "Gender",
    "Geo",
    "IDEngagementEquipe",
    "IDOrganismeEquipe",
    "IDPoule",
    "Jour",
    "Label",
    "Labellisation",
    "LabellisationItem",
    "LabellisationProgramme",
    "Logo",
    "Membre",
    "NatureSol",
    "Niveau",
    "Objectif",
    "Officiel",
    "OfficielPersonne",
    "OffrePratique",
    "OffrePratiqueDetail",
    "Organisateur",
    "OrganisateurType",
    "OrganismeEngagement",
    "OrganismeEquipe",
    "OrganismeId",
    "OrganismeIDPere",
    "PhaseCode",
    "PhaseEngagement",
    "Poule",
    "Pratique",
    "PublicationInternet",
    "PurpleLogo",
    "RankingEngagement",
    "Saison",
    "Salle",
    "Sexe",
    "SexeClass",
    "Source",
    "Status",
    "TeamEngagement",
    "TeamRanking",
    "TournoiTypeClass",
    "TournoiTypeEnum",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeClass",
    "TypeCompetition",
    "TypeCompetitionGenerique",
    "TypeEnum",
    "TypeLeague",
    # Meilisearch generic
    "FacetDistribution",
    "FacetStats",
    "MultiSearchQueries",
    "MultiSearchQuery",
    "MultiSearchResult",
    "multi_search_results_from_dict",
]
