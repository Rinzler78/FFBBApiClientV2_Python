"""Tests to bring remaining model modules to >= 90% coverage.

Targets:
- Enums at 0% (terrains_name, terrains_storage, tournois_libelle)
- FacetStats / FacetDistribution subclasses (78-91%)
- Models with uncovered to_dict branches

converter_utils edge cases have been extracted to:
- tests/unit/utils/test_307_coverage_gaps_utils.py
"""

from __future__ import annotations

import unittest

# ===========================================================================
# Groupe 1 : Enums at 0%
# ===========================================================================


class TestTerrainsNameEnum(unittest.TestCase):
    def test_000_tournois_value(self) -> None:
        from ffbb_api_client_v2.models.terrains_name import Name

        self.assertEqual(Name.TOURNOIS.value, "Tournois")

    def test_003_from_value(self) -> None:
        from ffbb_api_client_v2.models.terrains_name import Name

        self.assertIs(Name("Tournois"), Name.TOURNOIS)


class TestTerrainsStorageEnum(unittest.TestCase):
    def test_002_minio_value(self) -> None:
        from ffbb_api_client_v2.models.terrains_storage import Storage

        self.assertEqual(Storage.MINIO.value, "minio")

    def test_003_from_value(self) -> None:
        from ffbb_api_client_v2.models.terrains_storage import Storage

        self.assertIs(Storage("minio"), Storage.MINIO)


class TestTournoisLibelleEnum(unittest.TestCase):
    def test_004_bitume_value(self) -> None:
        from ffbb_api_client_v2.models.tournois_libelle import Libelle

        self.assertEqual(Libelle.BITUME.value, "BITUME")

    def test_005_beton_value(self) -> None:
        from ffbb_api_client_v2.models.tournois_libelle import Libelle

        self.assertEqual(Libelle.BÉTON.value, "Béton")

    def test_006_sol_synthetique_value(self) -> None:
        from ffbb_api_client_v2.models.tournois_libelle import Libelle

        self.assertEqual(Libelle.SOL_SYNTHÉTIQUE.value, "Sol synthétique")


# ===========================================================================
# Groupe 2 : FacetStats / FacetDistribution subclasses
# ===========================================================================


class TestCompetitionsFacetStats(unittest.TestCase):
    def test_021_from_dict_returns_instance(self) -> None:
        from ffbb_api_client_v2.models.competitions_facet_stats import (
            CompetitionsFacetStats,
        )

        obj = CompetitionsFacetStats.from_dict({})
        self.assertIsInstance(obj, CompetitionsFacetStats)

    def test_022_to_dict_returns_empty(self) -> None:
        from ffbb_api_client_v2.models.competitions_facet_stats import (
            CompetitionsFacetStats,
        )

        obj = CompetitionsFacetStats()
        self.assertEqual(obj.to_dict(), {})


class TestSallesFacetStats(unittest.TestCase):
    def test_021_from_dict_returns_instance(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_stats import SallesFacetStats

        obj = SallesFacetStats.from_dict({})
        self.assertIsInstance(obj, SallesFacetStats)

    def test_022_to_dict_returns_empty(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_stats import SallesFacetStats

        self.assertEqual(SallesFacetStats().to_dict(), {})


class TestSallesFacetDistribution(unittest.TestCase):
    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        obj = SallesFacetDistribution.from_dict({})
        self.assertIsInstance(obj, SallesFacetDistribution)
        self.assertIsNone(obj.type)
        self.assertIsNone(obj.commune_code_postal)
        self.assertIsNone(obj.commune_departement)
        self.assertIsNone(obj.commune_libelle)

    def test_026_to_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        self.assertEqual(SallesFacetDistribution().to_dict(), {})

    def test_027_from_dict_with_data(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        data = {
            "type": {"salle": 100, "annexe": 20},
            "commune.codePostal": {"75000": 5, "69000": 3},
            "commune.departement": {"75": 5, "69": 3},
            "commune.libelle": {"Paris": 5, "Lyon": 3},
        }
        obj = SallesFacetDistribution.from_dict(data)
        self.assertEqual(obj.type, {"salle": 100, "annexe": 20})
        self.assertEqual(obj.commune_code_postal, {"75000": 5, "69000": 3})
        self.assertEqual(obj.commune_departement, {"75": 5, "69": 3})
        self.assertEqual(obj.commune_libelle, {"Paris": 5, "Lyon": 3})

    def test_028_to_dict_with_data(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        obj = SallesFacetDistribution(
            type={"salle": 100},
            commune_code_postal={"75000": 5},
            commune_departement={"75": 5},
            commune_libelle={"Paris": 5},
        )
        d = obj.to_dict()
        self.assertEqual(d["type"], {"salle": 100})
        self.assertEqual(d["commune.codePostal"], {"75000": 5})
        self.assertEqual(d["commune.departement"], {"75": 5})
        self.assertEqual(d["commune.libelle"], {"Paris": 5})

    def test_040_roundtrip(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        data = {
            "type": {"salle": 100},
            "commune.codePostal": {"75000": 5},
            "commune.departement": {"75": 5},
            "commune.libelle": {"Paris": 5},
        }
        obj = SallesFacetDistribution.from_dict(data)
        self.assertEqual(obj.to_dict(), data)

    def test_016_partial_data(self) -> None:
        from ffbb_api_client_v2.models.salles_facet_distribution import (
            SallesFacetDistribution,
        )

        obj = SallesFacetDistribution.from_dict({"type": {"salle": 50}})
        self.assertEqual(obj.type, {"salle": 50})
        self.assertIsNone(obj.commune_code_postal)
        d = obj.to_dict()
        self.assertEqual(d, {"type": {"salle": 50}})


class TestTerrainsFacetStats(unittest.TestCase):
    def test_021_from_dict_returns_instance(self) -> None:
        from ffbb_api_client_v2.models.terrains_facet_stats import TerrainsFacetStats

        obj = TerrainsFacetStats.from_dict({})
        self.assertIsInstance(obj, TerrainsFacetStats)

    def test_022_to_dict_returns_empty(self) -> None:
        from ffbb_api_client_v2.models.terrains_facet_stats import TerrainsFacetStats

        self.assertEqual(TerrainsFacetStats().to_dict(), {})


class TestRencontresFacetStats(unittest.TestCase):
    def test_021_from_dict_returns_instance(self) -> None:
        from ffbb_api_client_v2.models.rencontres_facet_stats import (
            RencontresFacetStats,
        )

        obj = RencontresFacetStats.from_dict({})
        self.assertIsInstance(obj, RencontresFacetStats)

    def test_022_to_dict_returns_empty(self) -> None:
        from ffbb_api_client_v2.models.rencontres_facet_stats import (
            RencontresFacetStats,
        )

        self.assertEqual(RencontresFacetStats().to_dict(), {})


class TestTournoisFacetStats(unittest.TestCase):
    def test_021_from_dict_returns_instance(self) -> None:
        from ffbb_api_client_v2.models.tournois_facet_stats import TournoisFacetStats

        obj = TournoisFacetStats.from_dict({})
        self.assertIsInstance(obj, TournoisFacetStats)

    def test_022_to_dict_returns_empty(self) -> None:
        from ffbb_api_client_v2.models.tournois_facet_stats import TournoisFacetStats

        self.assertEqual(TournoisFacetStats().to_dict(), {})


class TestCompetitionsFacetDistribution(unittest.TestCase):
    """Cover from_dict({}) and to_dict() empty-branch paths."""

    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.competitions_facet_distribution import (
            CompetitionsFacetDistribution,
        )

        obj = CompetitionsFacetDistribution.from_dict({})
        self.assertIsInstance(obj, CompetitionsFacetDistribution)
        self.assertIsNone(obj.competition_id_categorie_code)

    def test_026_to_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.competitions_facet_distribution import (
            CompetitionsFacetDistribution,
        )

        self.assertEqual(CompetitionsFacetDistribution().to_dict(), {})


class TestTerrainsFacetDistribution(unittest.TestCase):
    """Cover from_dict({}) and to_dict() empty-branch paths."""

    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )

        obj = TerrainsFacetDistribution.from_dict({})
        self.assertIsInstance(obj, TerrainsFacetDistribution)
        self.assertIsNone(obj.sexe)
        self.assertIsNone(obj.tournoi_type)
        self.assertIsNone(obj.tournoi_types3_x3_libelle)

    def test_026_to_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )

        self.assertEqual(TerrainsFacetDistribution().to_dict(), {})


class TestTerrainsFacetDistributionWithData(unittest.TestCase):
    """Cover from_dict with data (True branch) and to_dict (formerly TestTournoisFacetDistribution)."""

    def test_027_from_dict_with_data(self) -> None:
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )

        data = {
            "sexe": {"Féminin": 5, "Masculin": 10, "Mixte": 3},
            "tournoiType": {"Open Plus": 2, "Open Plus Access": 1, "Open Start": 4},
            "tournoiTypes3x3.libelle": {
                "Open Plus - Junior league 3x3": 1,
                "Open Plus - Super league 3x3": 2,
            },
        }
        obj = TerrainsFacetDistribution.from_dict(data)
        self.assertIsNotNone(obj.sexe)
        self.assertEqual(obj.sexe.feminine, 5)
        self.assertIsNotNone(obj.tournoi_type)
        self.assertEqual(obj.tournoi_type.open_plus, 2)
        self.assertIsNotNone(obj.tournoi_types3_x3_libelle)

    def test_028_to_dict_with_data(self) -> None:
        from ffbb_api_client_v2.models.sexe_class import SexeClass
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )
        from ffbb_api_client_v2.models.tournoi_type_class import TournoiTypeClass

        obj = TerrainsFacetDistribution(
            sexe=SexeClass(feminine=5, masculine=10, mixed=3),
            tournoi_type=TournoiTypeClass(open_plus=2),
        )
        d = obj.to_dict()
        self.assertIn("sexe", d)
        self.assertIn("tournoiType", d)

    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )

        obj = TerrainsFacetDistribution.from_dict({})
        self.assertEqual(obj.to_dict(), {})


# ===========================================================================
# Groupe 3 : Models with uncovered to_dict branches
# ===========================================================================


class TestDocumentFlyer(unittest.TestCase):
    """Cover to_dict branches for fields not exercised in other tests."""

    def test_030_from_dict_with_extra_fields(self) -> None:
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer

        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "storage": "minio",
            "filename_disk": "file.jpg",
            "filename_download": "download.jpg",
            "title": "Test",
            "type": "image/jpeg",
            "uploaded_on": "2024-01-01T00:00:00",
            "modified_on": "2024-06-15T12:00:00",
            "charset": "utf-8",
            "filesize": 1024,
            "width": 800,
            "height": 600,
            "duration": 120,
            "embed": "<iframe></iframe>",
            "description": "A test image",
            "location": "Paris",
            "tags": "test,image",
            "source": "FFBB Serveur",
            "credits": "FFBB",
            "gradient_color": "#ffffff",
            "md5": "abc123",
            "newsbridge_media_id": "nb-123",
            "newsbridge_metadatas": "{}",
            "newsbridge_name": "news",
            "newsbridge_recorded_at": "2024-03-01T10:00:00",
            "focal_point_x": 0.5,
            "focal_point_y": 0.3,
            "newsbridge_labels": ["label1"],
            "newsbridge_persons": ["person1"],
            "uploaded_by": "660e8400-e29b-41d4-a716-446655440000",
            "modified_by": "770e8400-e29b-41d4-a716-446655440000",
            "newsbridge_mission": "mission-1",
        }
        obj = DocumentFlyer.from_dict(data)
        d = obj.to_dict()

        self.assertEqual(d["charset"], "utf-8")
        self.assertEqual(d["duration"], 120)
        self.assertEqual(d["embed"], "<iframe></iframe>")
        self.assertEqual(d["description"], "A test image")
        self.assertEqual(d["location"], "Paris")
        self.assertEqual(d["tags"], "test,image")
        self.assertEqual(d["credits"], "FFBB")
        self.assertEqual(d["newsbridge_media_id"], "nb-123")
        self.assertEqual(d["newsbridge_metadatas"], "{}")
        self.assertEqual(d["newsbridge_name"], "news")
        self.assertIn("newsbridge_recorded_at", d)
        self.assertEqual(d["focal_point_x"], 0.5)
        self.assertEqual(d["focal_point_y"], 0.3)
        self.assertEqual(d["uploaded_by"], "660e8400-e29b-41d4-a716-446655440000")
        self.assertEqual(d["modified_by"], "770e8400-e29b-41d4-a716-446655440000")
        self.assertEqual(d["newsbridge_mission"], "mission-1")


class TestExternalCompetitionID(unittest.TestCase):
    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.external_competition_id import (
            ExternalCompetitionID,
        )

        obj = ExternalCompetitionID.from_dict({})
        self.assertEqual(obj.to_dict(), {})

    def test_040_roundtrip(self) -> None:
        from ffbb_api_client_v2.models.external_competition_id import (
            ExternalCompetitionID,
        )

        data = {
            "code": "C01",
            "nom": "National",
            "sexe": "Masculin",
            "typeCompetition": "Championnat",
        }
        obj = ExternalCompetitionID.from_dict(data)
        d = obj.to_dict()
        self.assertEqual(d, data)


class TestTeamEngagement(unittest.TestCase):
    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.team_engagement import TeamEngagement

        obj = TeamEngagement.from_dict({})
        self.assertEqual(obj.to_dict(), {})

    def test_040_roundtrip(self) -> None:
        from ffbb_api_client_v2.models.team_engagement import TeamEngagement

        data = {
            "nomOfficiel": "Team A",
            "nomUsuel": "TA",
            "codeAbrege": "TA",
        }
        obj = TeamEngagement.from_dict(data)
        d = obj.to_dict()
        self.assertEqual(d["nomOfficiel"], "Team A")
        self.assertEqual(d["nomUsuel"], "TA")
        self.assertEqual(d["codeAbrege"], "TA")


class TestRencontresEngagement(unittest.TestCase):
    def test_035_to_dict_with_id(self) -> None:
        from ffbb_api_client_v2.models.rencontres_engagement import Engagement

        obj = Engagement(id="test")
        self.assertEqual(obj.to_dict(), {"id": "test"})

    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.rencontres_engagement import Engagement

        obj = Engagement.from_dict({})
        self.assertEqual(obj.to_dict(), {})


class TestSexeClass(unittest.TestCase):
    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        obj = SexeClass.from_dict({})
        self.assertEqual(obj.to_dict(), {})

    def test_040_roundtrip(self) -> None:
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        data = {"Féminin": 5, "Masculin": 10, "Mixte": 3}
        obj = SexeClass.from_dict(data)
        self.assertEqual(obj.to_dict(), data)


class TestTournoiTypes3X3(unittest.TestCase):
    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.tournoi_types_3x3 import TournoiTypes3X3

        obj = TournoiTypes3X3.from_dict({})
        self.assertEqual(obj.to_dict(), {})

    def test_040_roundtrip(self) -> None:
        from ffbb_api_client_v2.models.tournoi_types_3x3 import TournoiTypes3X3

        data = {
            "libelle": "Open Plus - Junior league 3x3",
            "logo": "550e8400-e29b-41d4-a716-446655440000",
            "type_league": "junior",
            "type_tournois": 5,
        }
        obj = TournoiTypes3X3.from_dict(data)
        d = obj.to_dict()
        self.assertEqual(d["libelle"], "Open Plus - Junior league 3x3")
        self.assertEqual(d["logo"], "550e8400-e29b-41d4-a716-446655440000")
        self.assertEqual(d["type_league"], "junior")
        self.assertEqual(d["type_tournois"], "5")


# ===========================================================================
# Groupe 4 : Complex models
# ===========================================================================


class TestOrganismesHit(unittest.TestCase):
    def test_041_from_dict_invalid_raises_value_error(self) -> None:
        from ffbb_api_client_v2.models.organismes_hit import OrganismesHit

        with self.assertRaises(ValueError):
            OrganismesHit.from_dict("invalid")

    def test_042_from_dict_empty(self) -> None:
        from ffbb_api_client_v2.models.organismes_hit import OrganismesHit

        obj = OrganismesHit.from_dict({})
        self.assertIsInstance(obj, OrganismesHit)
        self.assertEqual(obj.to_dict(), {})


class TestLive(unittest.TestCase):
    """Cover to_dict branches for OT scores, external_id, team_engagements."""

    def test_043_to_dict_ot_scores_and_nested(self) -> None:
        from ffbb_api_client_v2.models.external_id import ExternalID
        from ffbb_api_client_v2.models.live import Live
        from ffbb_api_client_v2.models.team_engagement import TeamEngagement

        obj = Live(
            score_ot1_home=10,
            score_ot2_home=5,
            score_ot1_out=8,
            score_ot2_out=3,
            external_id=ExternalID(nom_equipe1="Team A", nom_equipe2="Team B"),
            team_engagement_home=TeamEngagement(nom_officiel="Home Team"),
            team_engagement_out=TeamEngagement(nom_officiel="Away Team"),
        )
        d = obj.to_dict()
        self.assertEqual(d["score_ot1_home"], 10)
        self.assertEqual(d["score_ot2_home"], 5)
        self.assertEqual(d["score_ot1_out"], 8)
        self.assertEqual(d["score_ot2_out"], 3)
        self.assertEqual(d["externalId"]["nomEquipe1"], "Team A")
        self.assertEqual(d["teamEngagement_home"]["nomOfficiel"], "Home Team")
        self.assertEqual(d["teamEngagement_out"]["nomOfficiel"], "Away Team")


# ===========================================================================
# Groupe 6 : Additional coverage for modules still < 90%
# ===========================================================================


class TestPratiquesFacetStats(unittest.TestCase):
    def test_044_from_dict_and_to_dict(self) -> None:
        from ffbb_api_client_v2.models.pratiques_facet_stats import PratiquesFacetStats

        obj = PratiquesFacetStats.from_dict({})
        self.assertIsInstance(obj, PratiquesFacetStats)
        self.assertEqual(obj.to_dict(), {})


class TestCompetitionsFacetDistributionWithData(unittest.TestCase):
    """Cover to_dict branches when nested objects are populated."""

    def test_045_to_dict_with_nested_objects(self) -> None:
        from ffbb_api_client_v2.models.competition_id_type_competition import (
            CompetitionIDTypeCompetition,
        )
        from ffbb_api_client_v2.models.competitions_facet_distribution import (
            CompetitionsFacetDistribution,
        )
        from ffbb_api_client_v2.models.niveau_class import NiveauClass
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        obj = CompetitionsFacetDistribution(
            competition_id_categorie_code={"U13": 5},
            competition_id_nom_extended={"National": 3},
            competition_id_sexe=SexeClass(feminine=2, masculine=8),
            competition_id_type_competition=CompetitionIDTypeCompetition(
                championnat=10
            ),
            niveau=NiveauClass(départemental=4),
            organisateur_id={"org1": 1},
            organisateur_nom={"FFBB": 2},
        )
        d = obj.to_dict()
        self.assertEqual(d["competitionId.categorie.code"], {"U13": 5})
        self.assertEqual(d["competitionId.nomExtended"], {"National": 3})
        self.assertIn("competitionId.sexe", d)
        self.assertIn("competitionId.typeCompetition", d)
        self.assertIn("niveau", d)
        self.assertEqual(d["organisateur.id"], {"org1": 1})
        self.assertEqual(d["organisateur.nom"], {"FFBB": 2})


if __name__ == "__main__":
    unittest.main()
