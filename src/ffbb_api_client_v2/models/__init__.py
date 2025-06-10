"""
Models package for ffbb_api_client_v2
"""

from .cartographie import Cartographie
from .commune import Commune
from .competition_id import CompetitionID
from .competition_id_type_competition import CompetitionIDTypeCompetition
from .competition_id_type_competition_generique import (
    CompetitionIDTypeCompetitionGenerique,
)
from .competition_origine import CompetitionOrigine
from .competition_origine_categorie import CompetitionOrigineCategorie
from .competition_origine_type_competition_generique import (
    CompetitionOrigineTypeCompetitionGenerique,
)
from .competitions_multi_search_result import (
    CompetitionsFacetDistribution,
    CompetitionsFacetStats,
    CompetitionsHit,
    CompetitionsMultiSearchResult,
)
from .coordonnees import Coordonnees
from .document_flyer import DocumentFlyer
from .geo import Geo
from .get_ffbbserver_competitions_request_args import (
    GetFfbbserverCompetitionsRequestArgs,
    get_ffbbserver_competitions_request_args_from_dict,
    get_ffbbserver_competitions_request_args_to_dict,
)
from .get_ffbbserver_organismes_request_args import (
    GetFfbbserverOrganismesRequestArgs,
    get_ffbbserver_organismes_request_args_from_dict,
    get_ffbbserver_organismes_request_args_to_dict,
)
from .get_ffbbserver_poules_request_args import (
    GetFfbbserverPoulesRequestArgs,
    get_ffbbserver_poules_request_args_from_dict,
    get_ffbbserver_poules_request_args_to_dict,
)
from .get_ffbbserver_poules_response import Classement
from .get_lives_json_response import Element
from .id_engagement_equipe import IDEngagementEquipe
from .id_organisme_equipe import IDOrganismeEquipe
from .id_organisme_equipe1_logo import IDOrganismeEquipe1Logo
from .id_poule import IDPoule
from .labellisation import Labellisation
from .lives import Clock, Live
from .logo import Logo
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
from .multi_search_result_terrains import Sexe
from .multi_search_result_tournois import Sexe as TournoisSexe
from .niveau_data import NiveauData
from .organismes_multi_search_result import (
    OrganismesFacetDistribution,
    OrganismesFacetStats,
    OrganismesHit,
    OrganismesMultiSearchResult,
)
from .post_multi_search_response import (
    CompetitionIDSexe,
)
from .post_multi_search_response import Niveau as PostNiveau
from .poule import Poule
from .pratiques_multi_search_result import (
    PratiquesFacetDistribution,
    PratiquesFacetStats,
    PratiquesHit,
    PratiquesMultiSearchResult,
)
from .purple_logo import PurpleLogo
from .rencontres_multi_search_result import (
    RencontresFacetDistribution,
    RencontresFacetStats,
    RencontresHit,
    RencontresMultiSearchResult,
)
from .salles_multi_search_result import (
    SallesFacetDistribution,
    SallesFacetStats,
    SallesHit,
    SallesMultiSearchResult,
)
from .team_engagement import TeamEngagement
from .terrains_multi_search_result import (
    TerrainsFacetDistribution,
    TerrainsFacetStats,
    TerrainsHit,
    TerrainsMultiSearchResult,
)
from .tournoi_type import TournoiType
from .tournois_multi_search_result import (
    TournoisFacetDistribution,
    TournoisFacetStats,
    TournoisHit,
    TournoisMultiSearchResult,
)
from .type_association import TypeAssociation
from .type_association_libelle import TypeAssociationLibelle
from .type_competition_generique import TypeCompetitionGenerique

__all__ = [
    "CompetitionsFacetDistribution",
    "CompetitionsFacetStats",
    "CompetitionsHit",
    "CompetitionsMultiSearchResult",
    "MultiSearchQuery",
    "CompetitionsMultiSearchQuery",
    "OrganismesMultiSearchQuery",
    "PratiquesMultiSearchQuery",
    "RencontresMultiSearchQuery",
    "SallesMultiSearchQuery",
    "TerrainsMultiSearchQuery",
    "TournoisMultiSearchQuery",
    "OrganismesFacetDistribution",
    "OrganismesFacetStats",
    "OrganismesHit",
    "OrganismesMultiSearchResult",
    "PratiquesFacetDistribution",
    "PratiquesFacetStats",
    "PratiquesHit",
    "PratiquesMultiSearchResult",
    "RencontresFacetDistribution",
    "RencontresFacetStats",
    "RencontresHit",
    "RencontresMultiSearchResult",
    "SallesFacetDistribution",
    "SallesFacetStats",
    "SallesHit",
    "SallesMultiSearchResult",
    "TerrainsFacetDistribution",
    "TerrainsFacetStats",
    "TerrainsHit",
    "TerrainsMultiSearchResult",
    "TournoisFacetDistribution",
    "TournoisFacetStats",
    "TournoisHit",
    "TournoisMultiSearchResult",
    "Cartographie",
    "Commune",
    "CompetitionID",
    "Labellisation",
    "CompetitionIDTypeCompetition",
    "CompetitionIDTypeCompetitionGenerique",
    "CompetitionOrigine",
    "CompetitionOrigineCategorie",
    "CompetitionOrigineTypeCompetitionGenerique",
    "Coordonnees",
    "DocumentFlyer",
    "Geo",
    "GetFfbbserverCompetitionsRequestArgs",
    "get_ffbbserver_competitions_request_args_from_dict",
    "get_ffbbserver_competitions_request_args_to_dict",
    "GetFfbbserverOrganismesRequestArgs",
    "get_ffbbserver_organismes_request_args_from_dict",
    "get_ffbbserver_organismes_request_args_to_dict",
    "GetFfbbserverPoulesRequestArgs",
    "get_ffbbserver_poules_request_args_from_dict",
    "get_ffbbserver_poules_request_args_to_dict",
    "Classement",
    "Element",
    "IDEngagementEquipe",
    "IDOrganismeEquipe",
    "IDOrganismeEquipe1Logo",
    "IDPoule",
    "NiveauData",
    "Clock",
    "Live",
    "Logo",
    "Sexe",
    "TournoisSexe",
    "PostNiveau",
    "CompetitionIDSexe",
    "TournoiType",
    "Poule",
    "PurpleLogo",
    "TeamEngagement",
    "TypeAssociation",
    "TypeAssociationLibelle",
    "TypeCompetitionGenerique",
]
