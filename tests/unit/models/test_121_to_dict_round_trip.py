"""Tests round-trip from_dict -> to_dict pour les modeles FFBB API.

Strategie: double round-trip pour valider la stabilite de la serialisation.
  obj1 = Model.from_dict(input_data)
  dict1 = obj1.to_dict()
  obj2 = Model.from_dict(dict1)
  dict2 = obj2.to_dict()
  assert dict1 == dict2  # stable apres normalisation

Section A: Small models (~12 tests)
Section B: Live models (~6 tests)
Section C: Multi-search Hit models (~12 tests)
Section D: Multi-search Result wrappers (~8 tests)
"""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.affiche import Affiche
from ffbb_api_client_v2.models.cartographie import Cartographie
from ffbb_api_client_v2.models.commune import Commune
from ffbb_api_client_v2.models.competitions_facet_distribution import (
    CompetitionsFacetDistribution,
)
from ffbb_api_client_v2.models.competitions_hit import CompetitionsHit
from ffbb_api_client_v2.models.document_flyer import DocumentFlyer
from ffbb_api_client_v2.models.external_id import ExternalCompetitionID, ExternalID
from ffbb_api_client_v2.models.folder import Folder
from ffbb_api_client_v2.models.geo import Geo
from ffbb_api_client_v2.models.lives import Clock, Live
from ffbb_api_client_v2.models.logo import Logo
from ffbb_api_client_v2.models.multi_search_result_competitions import (
    CompetitionsMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_organismes import (
    OrganismesMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_pratiques import (
    PratiquesMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_rencontres import (
    RencontresMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_salles import (
    SallesMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_terrains import (
    TerrainsMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_result_tournois import (
    TournoisMultiSearchResult,
)
from ffbb_api_client_v2.models.multi_search_results_class import MultiSearchResults
from ffbb_api_client_v2.models.nature_sol import NatureSol
from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere
from ffbb_api_client_v2.models.organismes_facet_distribution import (
    OrganismesFacetDistribution,
)
from ffbb_api_client_v2.models.organismes_hit import OrganismesHit
from ffbb_api_client_v2.models.pratiques_hit import PratiquesHit
from ffbb_api_client_v2.models.rencontres_hit import RencontresHit
from ffbb_api_client_v2.models.salles_hit import SallesHit
from ffbb_api_client_v2.models.team_engagement import TeamEngagement
from ffbb_api_client_v2.models.terrains_hit import TerrainsHit
from ffbb_api_client_v2.models.tournois_hit import TournoisHit
from ffbb_api_client_v2.models.type_association import TypeAssociation


class Test022ToDictRoundTrip(unittest.TestCase):
    """Double round-trip tests: from_dict(to_dict(from_dict(data))) is stable."""

    def _assert_stable(self, model_class: type, input_data: dict[str, Any]) -> None:
        """Assert that double round-trip produces identical dicts."""
        obj1 = model_class.from_dict(input_data)
        dict1 = obj1.to_dict()
        obj2 = model_class.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2, f"{model_class.__name__} round-trip not stable")

    # -----------------------------------------------------------------------
    # Section A: Small models
    # -----------------------------------------------------------------------

    def test_040_affiche_full(self) -> None:
        """Affiche with UUID id, gradient_color, width, height."""
        self._assert_stable(
            Affiche,
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "gradient_color": "#FF5733",
                "width": 800,
                "height": 600,
            },
        )

    def test_041_affiche_minimal(self) -> None:
        """Affiche with only id."""
        self._assert_stable(
            Affiche,
            {"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
        )

    def test_042_folder(self) -> None:
        """Folder with UUID id and name."""
        self._assert_stable(
            Folder,
            {
                "id": "f0e1d2c3-b4a5-6789-0123-456789abcdef",
                "name": "Photos Equipe",
                "parent": None,
            },
        )

    def test_043_nature_sol(self) -> None:
        """NatureSol with Code enum, datetime, terrain bool-string."""
        self._assert_stable(
            NatureSol,
            {
                "code": "BIT",
                "date_created": "2024-01-15T10:30:00",
                "date_updated": "2024-06-01T14:00:00",
                "id": "ns-001",
                "libelle": "Bitume",
                "terrain": "true",
            },
        )

    def test_044_logo(self) -> None:
        """Logo with UUID id and gradient_color."""
        self._assert_stable(
            Logo,
            {
                "id": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
                "gradient_color": "#0055AA",
            },
        )

    def test_045_geo(self) -> None:
        """Geo with lat/lng floats."""
        self._assert_stable(
            Geo,
            {"lat": 48.8566, "lng": 2.3522},
        )

    def test_046_cartographie(self) -> None:
        """Cartographie with nested Coordonnees, float lat/lng."""
        self._assert_stable(
            Cartographie,
            {
                "adresse": "12 rue du Sport",
                "codePostal": "75001",
                "coordonnees": {
                    "type": "Point",
                    "coordinates": [2.3522, 48.8566],
                },
                "date_created": None,
                "date_updated": None,
                "id": "carto-001",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "title": "Gymnase Central",
                "ville": "Paris",
            },
        )

    def test_047_commune(self) -> None:
        """Commune with int-as-string codePostal, datetime, libelle."""
        self._assert_stable(
            Commune,
            {
                "codeInsee": None,
                "codePostal": "75001",
                "date_created": "2024-01-01T00:00:00",
                "date_updated": "2024-06-15T12:00:00",
                "id": "12345",
                "libelle": "Paris 1er",
                "departement": "Paris",
            },
        )

    def test_048_document_flyer_full(self) -> None:
        """DocumentFlyer with many fields, nested Folder, datetime, enum."""
        self._assert_stable(
            DocumentFlyer,
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "storage": "local",
                "filename_disk": "photo.jpg",
                "filename_download": "photo.jpg",
                "title": "Photo Equipe",
                "type": "image/jpeg",
                "uploaded_on": "2024-01-15T10:30:00",
                "modified_on": "2024-06-01T14:00:00",
                "charset": None,
                "filesize": "204800",
                "width": 1920,
                "height": 1080,
                "duration": None,
                "embed": None,
                "description": None,
                "location": None,
                "tags": None,
                "metadata": None,
                "source": None,
                "credits": None,
                "gradient_color": "#FF5733",
                "md5": "d41d8cd98f00b204e9800998ecf8427e",
                "newsbridge_media_id": None,
                "newsbridge_metadatas": None,
                "newsbridge_name": None,
                "newsbridge_recorded_at": None,
                "focal_point_x": None,
                "focal_point_y": None,
                "newsbridge_labels": [],
                "newsbridge_persons": [],
                "folder": {
                    "id": "f0e1d2c3-b4a5-6789-0123-456789abcdef",
                    "name": "Photos",
                    "parent": None,
                },
                "uploaded_by": None,
                "modified_by": None,
                "newsbridge_mission": None,
            },
        )

    def test_049_document_flyer_minimal(self) -> None:
        """DocumentFlyer with only id and title."""
        self._assert_stable(
            DocumentFlyer,
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "title": "Photo",
                "charset": None,
                "duration": None,
                "embed": None,
                "description": None,
                "location": None,
                "tags": None,
                "metadata": None,
                "credits": None,
                "newsbridge_media_id": None,
                "newsbridge_metadatas": None,
                "newsbridge_name": None,
                "newsbridge_recorded_at": None,
                "focal_point_x": None,
                "focal_point_y": None,
                "uploaded_by": None,
                "modified_by": None,
                "newsbridge_mission": None,
            },
        )

    def test_050_type_association(self) -> None:
        """TypeAssociation with libelle."""
        self._assert_stable(
            TypeAssociation,
            {"libelle": "Association sportive"},
        )

    def test_051_organisme_id_pere(self) -> None:
        """OrganismeIDPere with nested fields."""
        self._assert_stable(
            OrganismeIDPere,
            {
                "adresse": "1 rue Federation",
                "adresseClubPro": None,
                "cartographie": "carto-123",
                "code": "0750001",
                "commune": "12345",
                "communeClubPro": None,
                "date_created": "2024-01-01T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "id": "9999",
                "mail": "contact@club.fr",
                "nom": "Club Paris",
                "nomClubPro": None,
                "organisme_id_pere": None,
                "salle": None,
                "telephone": "0100000000",
                "type": "ASS",
                "type_association": None,
                "urlSiteWeb": None,
                "logo": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
                "nom_simple": "Paris",
                "dateAffiliation": None,
                "saison_en_cours": True,
                "entreprise": False,
                "handibasket": False,
                "omnisport": False,
                "horsAssociation": False,
                "offresPratiques": [],
                "engagements": [],
                "labellisation": [],
            },
        )

    # -----------------------------------------------------------------------
    # Section B: Live models
    # -----------------------------------------------------------------------

    def test_060_clock_str(self) -> None:
        """Clock from_str/to_str round-trip."""
        clock1 = Clock.from_str("5:30:0")
        str1 = clock1.to_str()
        clock2 = Clock.from_str(str1)
        str2 = clock2.to_str()
        self.assertEqual(str1, str2)
        self.assertEqual(str1, "5:30:0")

    def test_061_live_full(self) -> None:
        """Live with matchId string->int->string, scores, clock, datetime."""
        self._assert_stable(
            Live,
            {
                "matchId": "99999",
                "matchTime": "2025-03-15T20:00:00",
                "competitionAbgName": "LNB Pro A",
                "score_q1_home": 22,
                "score_q2_home": 18,
                "score_q3_home": 20,
                "score_q4_home": 25,
                "score_q1_out": 19,
                "score_q2_out": 21,
                "score_q3_out": 17,
                "score_q4_out": 23,
                "score_ot1_home": None,
                "score_ot2_home": None,
                "score_ot1_out": None,
                "score_ot2_out": None,
                "score_home": 85,
                "score_out": 80,
                "clock": "5:30:0",
                "competitionName": "LNB Pro A 2024-2025",
                "currentStatus": "FINISHED",
                "currentPeriod": "Q4",
                "matchStatus": "COMPLETED",
                "teamName_home": "Paris Basketball",
                "teamName_out": "AS Monaco",
                "externalId": None,
                "teamEngagement_home": None,
                "teamEngagement_out": None,
            },
        )

    def test_062_live_minimal(self) -> None:
        """Live with matchId + clock only."""
        self._assert_stable(
            Live,
            {
                "matchId": "100",
                "clock": "0:0:0",
            },
        )

    def test_063_external_id(self) -> None:
        """ExternalID with nested CompetitionID, numeroJournee."""
        self._assert_stable(
            ExternalID,
            {
                "nomEquipe1": "Team A",
                "nomEquipe2": "Team B",
                "numeroJournee": "5",
                "competitionId": {
                    "code": "C001",
                    "nom": "Championnat",
                    "sexe": "M",
                    "typeCompetition": "CHAMP",
                },
                "idOrganismeEquipe1": None,
                "idOrganismeEquipe2": None,
                "salle": None,
                "idPoule": None,
            },
        )

    def test_064_team_engagement(self) -> None:
        """TeamEngagement with nested Logo."""
        self._assert_stable(
            TeamEngagement,
            {
                "nomOfficiel": "Paris BC Officiel",
                "nomUsuel": "Paris BC",
                "codeAbrege": "PBC",
                "logo": {
                    "id": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
                    "gradient_color": "#FF0000",
                },
            },
        )

    def test_065_competition_id(self) -> None:
        """CompetitionID (from external_id module) with 4 string fields."""
        self._assert_stable(
            ExternalCompetitionID,
            {
                "code": "PRO-A",
                "nom": "Pro A Masculine",
                "sexe": "Masculin",
                "typeCompetition": "CHAMPIONNAT",
            },
        )

    # -----------------------------------------------------------------------
    # Section C: Multi-search Hit models
    # -----------------------------------------------------------------------

    def test_070_organismes_hit_full(self) -> None:
        """OrganismesHit with 24 champs, nested Cartographie/Commune/Logo/Geo."""
        self._assert_stable(
            OrganismesHit,
            {
                "nomClubPro": None,
                "nom": "Paris Basketball Club",
                "adresse": "12 rue du Sport",
                "adresseClubPro": None,
                "code": "0750001",
                "id": "42",
                "engagements_noms": "EQ1, EQ2",
                "mail": "contact@parisbc.fr",
                "telephone": "0100000000",
                "type": "ASS",
                "urlSiteWeb": None,
                "nom_simple": None,
                "dateAffiliation": None,
                "saison_en_cours": True,
                "offresPratiques": ["Basket Santé", "Micro Basket"],
                "labellisation": ["Label Or"],
                "cartographie": {
                    "adresse": "12 rue du Sport",
                    "codePostal": "75001",
                    "coordonnees": None,
                    "date_created": None,
                    "date_updated": None,
                    "id": "carto-001",
                    "latitude": 48.8566,
                    "longitude": 2.3522,
                    "title": None,
                    "ville": "Paris",
                },
                "organisme_id_pere": None,
                "commune": {
                    "codeInsee": None,
                    "codePostal": "75001",
                    "date_created": None,
                    "date_updated": None,
                    "id": "12345",
                    "libelle": "Paris",
                    "departement": "Paris",
                },
                "communeClubPro": None,
                "type_association": {"libelle": "Association sportive"},
                "logo": {
                    "id": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
                    "gradient_color": "#0055AA",
                },
                "_geo": {"lat": 48.8566, "lng": 2.3522},
                "thumbnail": None,
            },
        )

    def test_071_organismes_hit_minimal(self) -> None:
        """OrganismesHit with id + nom only."""
        self._assert_stable(
            OrganismesHit,
            {
                "id": "1",
                "nom": "Club Minimal",
                "adresseClubPro": None,
                "nom_simple": None,
                "dateAffiliation": None,
                "communeClubPro": None,
                "thumbnail": None,
            },
        )

    def test_072_organismes_facet_distribution(self) -> None:
        """OrganismesFacetDistribution with nested TypeClass, dict[str,int]."""
        self._assert_stable(
            OrganismesFacetDistribution,
            {
                "labellisation": None,
                "offresPratiques": {"Basket Santé": 42, "Micro Basket": 15},
                "type": {
                    "Basket Inclusif": 3,
                    "Basket Santé": 10,
                    "Basket Tonik": 5,
                    "Centre Génération Basket": 2,
                    "Micro Basket": 8,
                },
                "type_association.libelle": None,
            },
        )

    def test_073_competitions_hit_full(self) -> None:
        """CompetitionsHit with Niveau/Sexe/Etat enums, nested Poule/Saison/Logo."""
        self._assert_stable(
            CompetitionsHit,
            {
                "nom": "Championnat D1 Masculine",
                "code": "D1M",
                "niveau": "Départemental",
                "typeCompetition": "Championnat",
                "sexe": "Masculin",
                "id": "comp-001",
                "creationEnCours": False,
                "date_created": "2024-09-01T00:00:00",
                "date_updated": "2024-12-15T00:00:00",
                "emarqueV2": True,
                "liveStat": False,
                "publicationInternet": "Affichée",
                "pro": False,
                "competition_origine": "comp-origin-001",
                "competition_origine_niveau": 1,
                "phase_code": None,
                "competition_origine_nom": "D1 Origine",
                "etat": None,
                "poules": [{"id": "poule-1", "nom": "Poule A"}],
                "phases": ["phase-1"],
                "categorie": {"code": "SE", "libelle": "Seniors"},
                "idCompetitionPere": None,
                "organisateur": {"id": "org-1", "nom": "Comite 75"},
                "saison": {"id": "saison-2024", "nom": "2024-2025"},
                "logo": {
                    "id": "d4e5f6a7-b8c9-0123-4567-89abcdef0123",
                    "gradient_color": "#003366",
                },
                "typeCompetitionGenerique": None,
                "thumbnail": None,
                "niveau_nb": None,
            },
        )

    def test_074_competitions_hit_minimal(self) -> None:
        """CompetitionsHit with id + nom + code."""
        self._assert_stable(
            CompetitionsHit,
            {
                "id": "comp-min",
                "nom": "Minimal",
                "code": "MIN",
                "idCompetitionPere": None,
                "thumbnail": None,
            },
        )

    def test_075_competitions_facet_distribution(self) -> None:
        """CompetitionsFacetDistribution with dict[str,int] fields."""
        self._assert_stable(
            CompetitionsFacetDistribution,
            {
                "competitionId.categorie.code": {"SE": 50, "U17": 30},
                "competitionId.nomExtended": None,
                "competitionId.sexe": None,
                "competitionId.typeCompetition": None,
                "niveau": None,
                "organisateur.id": {"org-1": 10, "org-2": 5},
                "organisateur.nom": {"Comite 75": 10, "Comite 93": 5},
            },
        )

    def test_076_salles_hit(self) -> None:
        """SallesHit with nested Commune, Geo."""
        self._assert_stable(
            SallesHit,
            {
                "libelle": "Gymnase Jean Moulin",
                "adresse": "5 avenue de la Republique",
                "id": "salle-001",
                "adresseComplement": None,
                "capaciteSpectateur": "500",
                "date_created": "2024-01-01T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "libelle2": None,
                "mail": "salle@mairie.fr",
                "numero": "S001",
                "telephone": "0100000001",
                "cartographie": None,
                "commune": {
                    "codeInsee": None,
                    "codePostal": "75011",
                    "date_created": None,
                    "date_updated": None,
                    "id": "11111",
                    "libelle": "Paris 11e",
                    "departement": "Paris",
                },
                "_geo": {"lat": 48.86, "lng": 2.38},
                "thumbnail": None,
                "type": "Salle",
                "type_association": None,
            },
        )

    def test_077_terrains_hit(self) -> None:
        """TerrainsHit with nested NatureSol, Commune, Geo."""
        self._assert_stable(
            TerrainsHit,
            {
                "nom": "Terrain Bercy",
                "rue": "Quai de Bercy",
                "id": "888",
                "accesLibre": True,
                "date_created": "2024-01-01T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "largeur": 15,
                "longueur": 28,
                "numero": 1,
                "cartographie": None,
                "commune": {
                    "codeInsee": None,
                    "codePostal": "75012",
                    "date_created": None,
                    "date_updated": None,
                    "id": "12012",
                    "libelle": "Paris 12e",
                    "departement": "Paris",
                },
                "natureSol": {
                    "code": "BIT",
                    "date_created": "2024-01-01T00:00:00",
                    "date_updated": None,
                    "id": "ns-1",
                    "libelle": "Bitume",
                    "terrain": "true",
                },
                "_geo": {"lat": 48.834, "lng": 2.386},
                "thumbnail": None,
                "type": "Terrain",
            },
        )

    def test_078_rencontres_hit(self) -> None:
        """RencontresHit with datetime, Niveau enum, nested CompetitionID."""
        self._assert_stable(
            RencontresHit,
            {
                "niveau": "Départemental",
                "id": "renc-001",
                "date": "2025-01-20T20:30:00",
                "date_rencontre": "2025-01-20T20:30:00",
                "nomEquipe1": "Paris BC 1",
                "nomEquipe2": "Lyon BC 1",
                "numeroJournee": "5",
                "pratique": None,
                "gsId": "GS-001",
                "officiels": ["Dupont Jean", "Martin Pierre"],
                "competitionId": {
                    "id": "comp-001",
                    "nom": "D1 Masculine",
                    "code": "D1M",
                    "sexe": "Masculin",
                    "typeCompetition": "Championnat",
                },
                "idOrganismeEquipe1": None,
                "idOrganismeEquipe2": None,
                "idPoule": {"id": "poule-1"},
                "saison": {"id": "saison-2024", "nom": "2024-2025"},
                "salle": None,
                "idEngagementEquipe1": None,
                "idEngagementEquipe2": None,
                "_geo": None,
                "date_timestamp": 1737405000,
                "date_rencontre_timestamp": 1737405000,
                "creation_timestamp": 1725148800,
                "dateSaisieResultat_timestamp": None,
                "modification_timestamp": 1737000000,
                "thumbnail": None,
                "organisateur": {"id": "org-1", "nom": "Comite 75"},
                "niveau_nb": None,
            },
        )

    def test_079_pratiques_hit(self) -> None:
        """PratiquesHit with nested TypeClass, labels."""
        self._assert_stable(
            PratiquesHit,
            {
                "titre": "Basket Sante Decouverte",
                "type": "Basket Santé",
                "adresse": "10 rue des Sports",
                "description": "Seances adaptees",
                "id": "777",
                "date_created": "2024-01-01T00:00:00",
                "date_debut": "2024-09-01T00:00:00",
                "date_demande": None,
                "date_fin": "2025-06-30T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "facebook": None,
                "site_web": None,
                "twitter": None,
                "action": "Decouverte",
                "adresse_salle": "Gymnase A",
                "adresse_structure": None,
                "assurance": None,
                "code": "BS-001",
                "cp_salle": "75015",
                "date_inscription": None,
                "email": "bs@club.fr",
                "engagement": None,
                "horaires_seances": "Mercredi 14h-16h",
                "inscriptions": None,
                "jours": ["mercredi"],
                "label": "Basket Santé Découverte",
                "latitude": None,
                "longitude": None,
                "mail_demandeur": None,
                "mail_structure": None,
                "nom_demandeur": None,
                "nom_salle": "Gymnase A",
                "nom_structure": "Club Sante",
                "nombre_personnes": "20",
                "nombre_seances": "30",
                "objectif": "Préventif",
                "prenom_demandeur": None,
                "public": "Adultes",
                "telephone": "0100000003",
                "ville_salle": "Paris",
                "cartographie": None,
                "affiche": None,
                "_geo": None,
                "date_debut_timestamp": 1725148800,
                "date_fin_timestamp": 1751241600,
                "thumbnail": None,
            },
        )

    def test_080_tournois_hit(self) -> None:
        """TournoisHit with nested DocumentFlyer, Commune, Geo."""
        self._assert_stable(
            TournoisHit,
            {
                "nom": "Tournoi Paris 3x3",
                "sexe": "Mixte",
                "adresse": "Parc de Bercy",
                "nomOrganisateur": "FFBB",
                "description": "Tournoi outdoor 3x3",
                "siteChoisi": None,
                "id": "555",
                "code": "T-001",
                "date_created": "2024-03-01T00:00:00",
                "date_updated": "2024-06-01T00:00:00",
                "ageMax": 99,
                "ageMin": 10,
                "categorieChampionnat3x3Id": None,
                "categorieChampionnat3x3Libelle": None,
                "debut": "2024-06-15T09:00:00",
                "fin": "2024-06-15T18:00:00",
                "mailOrganisateur": "tournoi@ffbb.fr",
                "nbParticipantPrevu": None,
                "tarifOrganisateur": None,
                "telephoneOrganisateur": "0100000002",
                "urlOrganisateur": None,
                "adresseComplement": None,
                "tournoiTypes3x3": None,
                "cartographie": None,
                "commune": {
                    "codeInsee": None,
                    "codePostal": "75012",
                    "date_created": None,
                    "date_updated": None,
                    "id": "12012",
                    "libelle": "Paris 12e",
                    "departement": "Paris",
                },
                "document_flyer": None,
                "tournoiType": None,
                "_geo": {"lat": 48.834, "lng": 2.386},
                "debut_timestamp": 1718438400,
                "fin_timestamp": 1718470800,
                "thumbnail": None,
            },
        )

    def test_081_rencontres_facet_distribution(self) -> None:
        """CompetitionsFacetDistribution with dict fields (formerly RencontresFacetDistribution)."""
        self._assert_stable(
            CompetitionsFacetDistribution,
            {
                "competitionId.categorie.code": {"SE": 100, "U17": 50},
                "competitionId.nomExtended": None,
                "competitionId.sexe": None,
                "competitionId.typeCompetition": None,
                "niveau": None,
                "organisateur.id": None,
                "organisateur.nom": None,
            },
        )

    # -----------------------------------------------------------------------
    # Section D: Multi-search Result wrappers
    # -----------------------------------------------------------------------

    def _result_wrapper(
        self, index_uid: str, hit_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Build a minimal MultiSearchResult dict."""
        return {
            "indexUid": index_uid,
            "hits": [hit_data],
            "query": "test",
            "processingTimeMs": 5,
            "limit": 20,
            "offset": 0,
            "estimatedTotalHits": 1,
        }

    def test_090_organismes_result(self) -> None:
        """OrganismesMultiSearchResult with hits and facetDistribution."""
        data = self._result_wrapper(
            "ffbbserver_organismes",
            {
                "id": "42",
                "nom": "Club Paris",
                "adresseClubPro": None,
                "nom_simple": None,
                "dateAffiliation": None,
                "communeClubPro": None,
                "thumbnail": None,
            },
        )
        data["facetDistribution"] = {
            "offresPratiques": {"Basket Santé": 10},
        }
        self._assert_stable(OrganismesMultiSearchResult, data)

    def test_091_competitions_result(self) -> None:
        """CompetitionsMultiSearchResult with hits and facets."""
        data = self._result_wrapper(
            "ffbbserver_competitions",
            {
                "id": "comp-1",
                "nom": "D1",
                "code": "D1M",
                "idCompetitionPere": None,
                "thumbnail": None,
            },
        )
        data["facetDistribution"] = {
            "competitionId.categorie.code": {"SE": 50},
        }
        self._assert_stable(CompetitionsMultiSearchResult, data)

    def test_092_salles_result(self) -> None:
        """SallesMultiSearchResult with hits."""
        data = self._result_wrapper(
            "ffbbserver_salles",
            {
                "id": "salle-1",
                "libelle": "Gymnase X",
                "thumbnail": None,
            },
        )
        self._assert_stable(SallesMultiSearchResult, data)

    def test_093_terrains_result(self) -> None:
        """TerrainsMultiSearchResult with hits."""
        data = self._result_wrapper(
            "ffbbserver_terrains",
            {
                "id": "111",
                "nom": "Terrain Y",
                "nbParticipantPrevu": None,
                "adresseComplement": None,
                "thumbnail": None,
            },
        )
        self._assert_stable(TerrainsMultiSearchResult, data)

    def test_094_rencontres_result(self) -> None:
        """RencontresMultiSearchResult with hits and facets."""
        data = self._result_wrapper(
            "ffbbserver_rencontres",
            {
                "id": "renc-1",
                "gsId": "GS-1",
                "dateSaisieResultat_timestamp": None,
                "thumbnail": None,
            },
        )
        data["facetDistribution"] = {
            "competitionId.categorie.code": {"SE": 20},
        }
        self._assert_stable(RencontresMultiSearchResult, data)

    def test_095_pratiques_result(self) -> None:
        """PratiquesMultiSearchResult with hits."""
        data = self._result_wrapper(
            "ffbbnational_pratiques",
            {
                "id": "999",
                "titre": "Basket Sante",
                "facebook": None,
                "twitter": None,
                "latitude": None,
                "longitude": None,
            },
        )
        self._assert_stable(PratiquesMultiSearchResult, data)

    def test_096_tournois_result(self) -> None:
        """TournoisMultiSearchResult with hits."""
        data = self._result_wrapper(
            "ffbbserver_tournois",
            {
                "id": "444",
                "nom": "Terrain Z",
                "thumbnail": None,
            },
        )
        self._assert_stable(TournoisMultiSearchResult, data)

    def test_097_multi_search_results_wrapper(self) -> None:
        """MultiSearchResults with results[] containing multiple types."""
        data: dict[str, Any] = {
            "results": [
                {
                    "indexUid": "ffbbserver_organismes",
                    "hits": [
                        {
                            "id": "1",
                            "nom": "Club A",
                            "adresseClubPro": None,
                            "nom_simple": None,
                            "dateAffiliation": None,
                            "communeClubPro": None,
                            "thumbnail": None,
                        }
                    ],
                    "query": "test",
                    "processingTimeMs": 2,
                    "limit": 20,
                    "offset": 0,
                    "estimatedTotalHits": 1,
                },
                {
                    "indexUid": "ffbbserver_competitions",
                    "hits": [
                        {
                            "id": "comp-1",
                            "nom": "D1",
                            "code": "D1M",
                            "idCompetitionPere": None,
                            "thumbnail": None,
                        }
                    ],
                    "query": "test",
                    "processingTimeMs": 3,
                    "limit": 20,
                    "offset": 0,
                    "estimatedTotalHits": 1,
                },
                {
                    "indexUid": "ffbbserver_salles",
                    "hits": [
                        {
                            "id": "salle-1",
                            "libelle": "Gymnase",
                            "thumbnail": None,
                        }
                    ],
                    "query": "test",
                    "processingTimeMs": 1,
                    "limit": 20,
                    "offset": 0,
                    "estimatedTotalHits": 1,
                },
            ]
        }
        obj1 = MultiSearchResults.from_dict(data)
        dict1 = obj1.to_dict()
        obj2 = MultiSearchResults.from_dict(dict1)
        dict2 = obj2.to_dict()
        self.assertEqual(dict1, dict2)


if __name__ == "__main__":
    unittest.main()
