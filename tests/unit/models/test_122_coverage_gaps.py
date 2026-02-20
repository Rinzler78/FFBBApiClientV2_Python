"""Tests to bring model modules to >=90% coverage.

Targets model files identified as <90% after the converter refactoring:
- Models: to_dict branches for non-None fields
- multi_search_queries, multi_search_query, multi_search_results
- FacetDistribution / FacetStats assert False branch

Non-model tests (SecureLogging, RetryUtils, CacheManager, __init__, FFBBAPIClientV2)
have been extracted to:
- tests/unit/utils/test_307_coverage_gaps_utils.py
- tests/unit/clients/test_206_coverage_gaps_clients.py
"""

from __future__ import annotations

import unittest
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

# ---------------------------------------------------------------------------
# Model to_dict coverage
# ---------------------------------------------------------------------------


class TestCategorieToDictCoverage(unittest.TestCase):
    """categorie.py -- cover to_dict branches for all fields."""

    def test_025_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.models.categorie import Categorie

        now = datetime(2024, 6, 15, 12, 0, 0)
        c = Categorie(
            code="U13",
            date_created=now,
            date_updated=now,
            categorie_id="cat-1",
            libelle="Under 13",
            ordre=3,
        )
        d = c.to_dict()
        self.assertEqual(d["code"], "U13")
        self.assertEqual(d["date_created"], now.isoformat())
        self.assertEqual(d["date_updated"], now.isoformat())
        self.assertEqual(d["id"], "cat-1")
        self.assertEqual(d["libelle"], "Under 13")
        self.assertEqual(d["ordre"], 3)


class TestCartographieToDictCoverage(unittest.TestCase):
    """cartographie.py -- cover to_dict branches."""

    def test_025_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.models.cartographie import Cartographie
        from ffbb_api_client_v2.models.coordonnees import Coordonnees

        coords = Coordonnees(coordinates=[2.35, 48.85], type="Point")
        c = Cartographie(
            adresse="1 rue du Panier",
            code_postal="75001",
            coordonnees=coords,
            date_created=None,
            date_updated=None,
            cartographie_id="carto-1",
            latitude=48.85,
            longitude=2.35,
            title="Salle A",
            ville="Paris",
            status="published",
        )
        d = c.to_dict()
        self.assertEqual(d["adresse"], "1 rue du Panier")
        self.assertEqual(d["codePostal"], "75001")
        self.assertEqual(d["coordonnees"], coords.to_dict())
        self.assertEqual(d["id"], "carto-1")
        self.assertEqual(d["latitude"], 48.85)
        self.assertEqual(d["longitude"], 2.35)
        self.assertEqual(d["title"], "Salle A")
        self.assertEqual(d["ville"], "Paris")
        self.assertEqual(d["status"], "published")


class TestFolderToDictCoverage(unittest.TestCase):
    """folder.py -- cover to_dict branches for id and name."""

    def test_025_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.models.folder import Folder

        uid = UUID("12345678-1234-1234-1234-123456789abc")
        f = Folder(id=uid, name="images", parent=None)
        d = f.to_dict()
        self.assertEqual(d["id"], str(uid))
        self.assertEqual(d["name"], "images")
        self.assertNotIn("parent", d)  # parent is None


class TestIDPouleToDictCoverage(unittest.TestCase):
    """id_poule.py -- cover to_dict nom branch."""

    def test_003_to_dict_with_nom(self) -> None:
        from ffbb_api_client_v2.models.id_poule import IDPoule

        p = IDPoule(id="poule-1", nom="Poule A")
        d = p.to_dict()
        self.assertEqual(d["id"], "poule-1")
        self.assertEqual(d["nom"], "Poule A")


class TestPouleToDictCoverage(unittest.TestCase):
    """poule.py -- cover to_dict engagements branch."""

    def test_004_to_dict_with_engagements(self) -> None:
        from ffbb_api_client_v2.models.poule import Poule
        from ffbb_api_client_v2.models.rencontres_engagement import Engagement

        eng = Engagement.from_dict({"nomEquipe": "Team A"})
        p = Poule(nom="Poule A", id="p-1", engagements=[eng])
        d = p.to_dict()
        self.assertEqual(d["nom"], "Poule A")
        self.assertEqual(d["id"], "p-1")
        self.assertIsInstance(d["engagements"], list)
        self.assertEqual(len(d["engagements"]), 1)


class TestSaisonToDictCoverage(unittest.TestCase):
    """saison.py -- cover to_dict code branch."""

    def test_005_to_dict_with_code(self) -> None:
        from ffbb_api_client_v2.models.saison import Saison

        s = Saison(code="2024")
        d = s.to_dict()
        self.assertEqual(d["code"], "2024")


class TestTypeClassToDictCoverage(unittest.TestCase):
    """type_class.py -- cover to_dict groupement branch."""

    def test_006_to_dict_with_groupement(self) -> None:
        from ffbb_api_client_v2.models.type_class import TypeClass

        t = TypeClass(groupement=5)
        d = t.to_dict()
        self.assertEqual(d["Groupement"], 5)


class TestExternalIDToDictCoverage(unittest.TestCase):
    """external_id.py -- cover to_dict branches for CompetitionID and ExternalID."""

    def test_007_competition_id_to_dict(self) -> None:
        from ffbb_api_client_v2.models.external_id import ExternalCompetitionID
        from ffbb_api_client_v2.models.type_competition import TypeCompetition

        c = ExternalCompetitionID(
            code="NM1",
            nom="Nationale 1",
            sexe="Masculin",
            type_competition=TypeCompetition.CHAMPIONNAT,
        )
        d = c.to_dict()
        self.assertEqual(d["code"], "NM1")
        self.assertEqual(d["nom"], "Nationale 1")
        self.assertEqual(d["sexe"], "Masculin")
        self.assertEqual(d["typeCompetition"], "Championnat")

    def test_008_external_id_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.models.external_id import (
            ExternalCompetitionID,
            ExternalID,
        )
        from ffbb_api_client_v2.models.id_organisme_equipe import IDOrganismeEquipe
        from ffbb_api_client_v2.models.id_poule import IDPoule
        from ffbb_api_client_v2.models.salle import Salle

        comp = ExternalCompetitionID(
            code="NM1", nom="Nationale 1", sexe="M", type_competition=None
        )
        org1 = IDOrganismeEquipe(
            id="o1",
            nom="Club A",
            nom_simple=None,
            code="CA",
            nom_club_pro=None,
            logo=None,
        )
        org2 = IDOrganismeEquipe(
            id="o2",
            nom="Club B",
            nom_simple=None,
            code="CB",
            nom_club_pro=None,
            logo=None,
        )
        salle = Salle.from_dict({"libelle": "Salle X", "adresse": "1 rue"})
        poule = IDPoule(id="p1", nom="Poule A")
        ext = ExternalID(
            nom_equipe1="Eq1",
            nom_equipe2="Eq2",
            numero_journee=5,
            competition_id=comp,
            id_organisme_equipe1=org1,
            id_organisme_equipe2=org2,
            salle=salle,
            id_poule=poule,
        )
        d = ext.to_dict()
        self.assertEqual(d["nomEquipe1"], "Eq1")
        self.assertEqual(d["nomEquipe2"], "Eq2")
        self.assertEqual(d["numeroJournee"], "5")
        self.assertEqual(d["competitionId"]["code"], "NM1")
        self.assertIn("idOrganismeEquipe1", d)
        self.assertIn("idOrganismeEquipe2", d)
        self.assertEqual(d["salle"]["libelle"], "Salle X")
        self.assertEqual(d["idPoule"]["id"], "p1")


class TestDocumentFlyerToDictCoverage(unittest.TestCase):
    """document_flyer.py -- cover to_dict branches."""

    def test_009_to_dict_populated_fields(self) -> None:
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer
        from ffbb_api_client_v2.models.document_flyer_type import DocumentFlyerType
        from ffbb_api_client_v2.models.folder import Folder
        from ffbb_api_client_v2.models.source import Source

        uid = UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        now = datetime(2024, 1, 15, 10, 30, 0)
        folder = Folder(id=uid, name="docs", parent=None)
        doc = DocumentFlyer(
            id=uid,
            storage="local",
            filename_disk="file.pdf",
            filename_download="file.pdf",
            title="Flyer",
            type=DocumentFlyerType.IMAGE_JPEG,
            uploaded_on=now,
            modified_on=now,
            filesize=1024,
            width=800,
            height=600,
            source=Source.FFBB_SERVEUR,
            gradient_color="#fff",
            md5="abc123def456",
            newsbridge_labels=["label1"],
            newsbridge_persons=["person1"],
            folder=folder,
        )
        d = doc.to_dict()
        self.assertEqual(d["id"], str(uid))
        self.assertEqual(d["storage"], "local")
        self.assertEqual(d["filename_disk"], "file.pdf")
        self.assertEqual(d["filename_download"], "file.pdf")
        self.assertEqual(d["title"], "Flyer")
        self.assertEqual(d["type"], DocumentFlyerType.IMAGE_JPEG.value)
        self.assertEqual(d["uploaded_on"], now.isoformat())
        self.assertEqual(d["modified_on"], now.isoformat())
        self.assertEqual(d["filesize"], "1024")
        self.assertEqual(d["width"], 800)
        self.assertEqual(d["height"], 600)
        self.assertEqual(d["source"], Source.FFBB_SERVEUR.value)
        self.assertEqual(d["gradient_color"], "#fff")
        self.assertIn("md5", d)
        self.assertEqual(d["newsbridge_labels"], ["label1"])
        self.assertIn("newsbridge_persons", d)
        self.assertEqual(d["folder"]["name"], "docs")


class TestTournoisToDictCoverage(unittest.TestCase):
    """multi_search_result_tournois.py -- cover SexeClass and TerrainsFacetDistribution to_dict."""

    def test_010_sexe_class_to_dict(self) -> None:
        from ffbb_api_client_v2.models.sexe_class import SexeClass

        s = SexeClass(feminine=3, masculine=5, mixed=2)
        d = s.to_dict()
        self.assertEqual(d["Féminin"], 3)
        self.assertEqual(d["Masculin"], 5)
        self.assertEqual(d["Mixte"], 2)

    def test_011_terrains_facet_distribution_to_dict(self) -> None:
        from ffbb_api_client_v2.meilisearch_ffbb.models.terrains_facet_distribution import (
            TerrainsFacetDistribution,
        )
        from ffbb_api_client_v2.models.sexe_class import SexeClass
        from ffbb_api_client_v2.models.tournoi_type_class import TournoiTypeClass

        sexe = SexeClass(feminine=1, masculine=2, mixed=0)
        tt = TournoiTypeClass.from_dict({"Terrain": 3})
        fd = TerrainsFacetDistribution(
            sexe=sexe, tournoi_type=tt, tournoi_types3_x3_libelle=None
        )
        d = fd.to_dict()
        self.assertEqual(d["sexe"]["Féminin"], 1)
        self.assertIn("tournoiType", d)

    def test_012_tournois_hit_to_dict(self) -> None:
        from ffbb_api_client_v2.meilisearch_ffbb.models.terrains_sexe_enum import (
            SexeEnum,
        )
        from ffbb_api_client_v2.meilisearch_ffbb.models.tournois_hit import TournoisHit
        from ffbb_api_client_v2.models.commune import Commune
        from ffbb_api_client_v2.models.geo import Geo
        from ffbb_api_client_v2.models.tournoi_type_enum import TournoiTypeEnum

        now = datetime(2024, 6, 1, 12, 0, 0)
        commune = Commune.from_dict({"libelle": "Paris", "departement": "75"})
        geo = Geo.from_dict({"lat": 48.85, "lng": 2.35})
        hit = TournoisHit(
            nom="Tournoi A",
            sexe=SexeEnum.MIXTE,
            adresse="Parc de Bercy",
            nom_organisateur="FFBB",
            description="Tournoi outdoor",
            id=42,
            code="T-001",
            date_created=now,
            date_updated=now,
            age_max=99,
            age_min=10,
            commune=commune,
            tournoi_type=TournoiTypeEnum.OPEN_PLUS,
            geo=geo,
            thumbnail=None,
        )
        d = hit.to_dict()
        self.assertEqual(d["nom"], "Tournoi A")
        self.assertEqual(d["sexe"], "Mixte")
        self.assertEqual(d["adresse"], "Parc de Bercy")
        self.assertEqual(d["nomOrganisateur"], "FFBB")
        self.assertIn("id", d)
        self.assertIn("date_created", d)
        self.assertIn("date_updated", d)
        self.assertEqual(d["ageMax"], 99)
        self.assertEqual(d["ageMin"], 10)
        self.assertIn("commune", d)
        self.assertIn("_geo", d)
        self.assertEqual(d["tournoiType"], "Open Plus")


# ---------------------------------------------------------------------------
# MultiSearchQueries coverage (50% -> 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchQueriesCoverage(unittest.TestCase):
    """multi_search_queries.py -- cover from_dict and to_dict."""

    def test_013_from_dict_with_queries(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_queries import (
            MultiSearchQueries,
        )

        data = {
            "queries": [
                {
                    "indexUid": "ffbbserver_organismes",
                    "q": "test",
                    "limit": 10,
                    "offset": 0,
                }
            ]
        }
        result = MultiSearchQueries.from_dict(data)
        self.assertIsNotNone(result.queries)
        self.assertEqual(len(result.queries), 1)

    def test_014_from_dict_none_queries(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_queries import (
            MultiSearchQueries,
        )

        result = MultiSearchQueries.from_dict({"queries": None})
        self.assertIsNone(result.queries)

    def test_015_to_dict_with_queries(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_queries import (
            MultiSearchQueries,
        )
        from ffbb_api_client_v2.meilisearch.models.multi_search_query import (
            MultiSearchQuery,
        )

        q = MultiSearchQuery(index_uid="ffbbserver_organismes", q="test")
        msq = MultiSearchQueries(queries=[q])
        d = msq.to_dict()
        self.assertIn("queries", d)
        self.assertEqual(len(d["queries"]), 1)

    def test_016_to_dict_empty(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_queries import (
            MultiSearchQueries,
        )

        msq = MultiSearchQueries(queries=None)
        d = msq.to_dict()
        self.assertEqual(d, {})


# ---------------------------------------------------------------------------
# MultiSearchQuery coverage (85% -> 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchQueryCoverage(unittest.TestCase):
    """multi_search_query.py -- cover from_dict, to_dict, is_valid_result, filter_result."""

    def test_017_from_dict(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_query import (
            MultiSearchQuery,
        )

        data = {
            "indexUid": "ffbbserver_organismes",
            "q": "paris",
            "facets": ["type"],
            "limit": 20,
            "offset": 5,
            "filter": ["type = Club"],
            "sort": ["nom:asc"],
        }
        q = MultiSearchQuery.from_dict(data)
        self.assertEqual(q.index_uid, "ffbbserver_organismes")
        self.assertEqual(q.q, "paris")
        self.assertEqual(q.facets, ["type"])
        self.assertEqual(q.limit, 20)
        self.assertEqual(q.offset, 5)
        self.assertEqual(q.filter, ["type = Club"])
        self.assertEqual(q.sort, ["nom:asc"])

    def test_025_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_query import (
            MultiSearchQuery,
        )

        q = MultiSearchQuery(
            index_uid="ffbbserver_organismes",
            q="paris",
            facets=["type"],
            limit=20,
            offset=5,
            filter=["type = Club"],
            sort=["nom:asc"],
        )
        d = q.to_dict()
        self.assertEqual(d["indexUid"], "ffbbserver_organismes")
        self.assertEqual(d["q"], "paris")
        self.assertEqual(d["facets"], ["type"])
        self.assertEqual(d["limit"], 20)
        self.assertEqual(d["offset"], 5)
        self.assertEqual(d["filter"], ["type = Club"])
        self.assertEqual(d["sort"], ["nom:asc"])

    def test_019_is_valid_hit(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_query import (
            MultiSearchQuery,
        )

        q = MultiSearchQuery(index_uid="test", q="test")
        self.assertIs(q.is_valid_hit(MagicMock()), True)

    def test_020_filter_result_removes_invalid_hits(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_query import (
            MultiSearchQuery,
        )

        q = MultiSearchQuery(index_uid="test", q="paris")

        # Create mock hits
        valid_hit = MagicMock()
        valid_hit.is_valid_for_query.return_value = True
        invalid_hit = MagicMock()
        invalid_hit.is_valid_for_query.return_value = False

        result = MagicMock()
        result.hits = [valid_hit, invalid_hit]
        result.estimated_total_hits = 2

        filtered = q.filter_result(result)
        self.assertEqual(filtered.estimated_total_hits, 1)
        self.assertNotIn(invalid_hit, filtered.hits)

    def test_021_filter_result_no_query(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.multi_search_query import (
            MultiSearchQuery,
        )

        q = MultiSearchQuery(index_uid="test", q=None)
        result = MagicMock()
        result.hits = [MagicMock()]
        filtered = q.filter_result(result)
        self.assertIs(filtered, result)  # Unchanged


# ---------------------------------------------------------------------------
# MultiSearchResults to_dict coverage (89% -> 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchResultsToDictCoverage(unittest.TestCase):
    """multi_search_results.py -- cover to_dict branches."""

    def test_022_multi_search_result_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_organismes import (
            OrganismesMultiSearchResult,
        )
        from ffbb_api_client_v2.meilisearch_ffbb.models.organismes_facet_distribution import (
            OrganismesFacetDistribution,
        )
        from ffbb_api_client_v2.meilisearch_ffbb.models.organismes_facet_stats import (
            OrganismesFacetStats,
        )
        from ffbb_api_client_v2.meilisearch_ffbb.models.organismes_hit import (
            OrganismesHit,
        )

        hit = OrganismesHit.from_dict({"nom": "Club A", "code": "CL01"})
        fd = OrganismesFacetDistribution.from_dict({})
        fs = OrganismesFacetStats.from_dict({})
        result = OrganismesMultiSearchResult(
            index_uid="ffbbserver_organismes",
            hits=[hit],
            query="test",
            processing_time_ms=5,
            limit=10,
            offset=0,
            estimated_total_hits=1,
            facet_distribution=fd,
            facet_stats=fs,
        )
        d = result.to_dict()
        self.assertEqual(d["indexUid"], "ffbbserver_organismes")
        self.assertEqual(len(d["hits"]), 1)
        self.assertEqual(d["query"], "test")
        self.assertEqual(d["processingTimeMs"], 5)
        self.assertEqual(d["limit"], 10)
        self.assertEqual(d["offset"], 0)
        self.assertEqual(d["estimatedTotalHits"], 1)
        self.assertIn("facetDistribution", d)
        self.assertIn("facetStats", d)


# ---------------------------------------------------------------------------
# FacetDistribution / FacetStats (89% -- assert False branch)
# ---------------------------------------------------------------------------


class TestFacetDistributionAssertFalse(unittest.TestCase):
    """facet_distribution.py / facet_stats.py -- cover the assert False line."""

    def test_023_facet_distribution_from_dict_non_dict_fails(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.facet_distribution import (
            FacetDistribution,
        )

        with self.assertRaises(AssertionError):
            FacetDistribution.from_dict("not a dict")

    def test_024_facet_stats_from_dict_non_dict_fails(self) -> None:
        from ffbb_api_client_v2.meilisearch.models.facet_stats import FacetStats

        with self.assertRaises(AssertionError):
            FacetStats.from_dict("not a dict")


# ---------------------------------------------------------------------------
# OrganismeIdPere to_dict coverage (83% -> 90%+)
# ---------------------------------------------------------------------------


class TestOrganismeIdPereToDictCoverage(unittest.TestCase):
    """organisme_id_pere.py -- cover to_dict branches."""

    def test_025_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere

        data = {
            "adresse": "1 rue de Paris",
            "adresseClubPro": None,
            "cartographie": "some",
            "code": "CL01",
            "commune": "75001",
            "communeClubPro": None,
            "date_created": "2024-01-01T00:00:00",
            "date_updated": "2024-06-01T00:00:00",
            "id": "12345",
            "mail": "club@example.com",
            "nom": "Club Paris",
            "nomClubPro": "Pro Paris",
            "organisme_id_pere": None,
            "salle": None,
            "telephone": "0600000000",
            "type": "Association",
            "type_association": None,
            "urlSiteWeb": "https://club.fr",
            "logo": "550e8400-e29b-41d4-a716-446655440000",
            "nom_simple": "club paris",
            "dateAffiliation": None,
            "saison_en_cours": "true",
            "entreprise": "false",
            "handibasket": "true",
            "omnisport": "false",
            "horsAssociation": "false",
            "offresPratiques": [10821935],
            "engagements": [{"id": "eng1", "nom": "Equipe 1"}],
            "labellisation": [
                {
                    "id": "lab1",
                    "debut": "2024-01-01T00:00:00",
                    "fin": "2024-12-31T00:00:00",
                }
            ],
        }
        obj = OrganismeIDPere.from_dict(data)
        d = obj.to_dict()
        self.assertEqual(d["adresse"], "1 rue de Paris")
        self.assertEqual(d["code"], "CL01")
        self.assertEqual(d["commune"], "75001")
        self.assertIn("date_created", d)
        self.assertIn("date_updated", d)
        self.assertEqual(d["id"], "12345")
        self.assertEqual(d["mail"], "club@example.com")
        self.assertEqual(d["nom"], "Club Paris")
        self.assertEqual(d["nomClubPro"], "Pro Paris")
        self.assertEqual(d["telephone"], "0600000000")
        self.assertEqual(d["type"], "Association")
        self.assertEqual(d["urlSiteWeb"], "https://club.fr")
        self.assertEqual(d["nom_simple"], "club paris")
        self.assertIs(d["saison_en_cours"], True)
        self.assertIs(d["entreprise"], False)
        self.assertIs(d["handibasket"], True)
        self.assertIs(d["omnisport"], False)
        self.assertIs(d["horsAssociation"], False)
        self.assertEqual(d["offresPratiques"], [10821935])
        self.assertEqual(d["engagements"], [{"id": "eng1", "nom": "Equipe 1"}])
        self.assertEqual(
            d["labellisation"],
            [
                {
                    "id": "lab1",
                    "debut": "2024-01-01T00:00:00",
                    "fin": "2024-12-31T00:00:00",
                }
            ],
        )
        self.assertIn("logo", d)


# ---------------------------------------------------------------------------
# MultiSearchResultRencontres to_dict coverage (87% -> 90%+)
# ---------------------------------------------------------------------------


class TestMultiSearchResultRencontresToDictCoverage(unittest.TestCase):
    """multi_search_result_rencontres.py -- cover to_dict branches."""

    def test_026_rencontres_hit_to_dict_all_fields(self) -> None:
        from ffbb_api_client_v2.meilisearch_ffbb.models.rencontres_hit import (
            RencontresHit,
        )

        data = {
            "niveau": "Départemental",
            "id": "r-1",
            "date": "2024-06-15T20:00:00",
            "date_rencontre": "2024-06-15T20:00:00",
            "nomEquipe1": "Team A",
            "nomEquipe2": "Team B",
            "numeroJournee": "5",
            "pratique": "5x5",
            "gsId": "gs-123",
            "officiels": ["Ref1"],
            "competitionId": {"code": "NM1"},
            "idOrganismeEquipe1": {"id": "o1", "nom": "Club A"},
            "idOrganismeEquipe2": {"id": "o2", "nom": "Club B"},
            "idPoule": {"id": "p1"},
            "saison": {"code": "2024"},
            "salle": {"libelle": "Salle X", "adresse": "1 rue"},
            "idEngagementEquipe1": {"id": "e1"},
            "idEngagementEquipe2": {"id": "e2"},
            "_geo": {"lat": 48.85, "lng": 2.35},
            "date_timestamp": "1718485200",
            "date_rencontre_timestamp": "1718485200",
            "creation_timestamp": "1718485200",
            "dateSaisieResultat_timestamp": "1718485200",
            "modification_timestamp": "1718485200",
            "thumbnail": None,
            "organisateur": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nom": "Org1",
            },
            "niveau_nb": "3",
        }
        hit = RencontresHit.from_dict(data)
        d = hit.to_dict()
        self.assertEqual(d["nomEquipe1"], "Team A")
        self.assertEqual(d["nomEquipe2"], "Team B")
        self.assertEqual(d["id"], "r-1")
        self.assertIn("date", d)
        self.assertIn("date_rencontre", d)
        self.assertEqual(d["numeroJournee"], "5")
        self.assertIn("competitionId", d)
        self.assertIn("idOrganismeEquipe1", d)
        self.assertIn("idOrganismeEquipe2", d)
        self.assertIn("idPoule", d)
        self.assertIn("saison", d)
        self.assertIn("salle", d)
        self.assertIn("idEngagementEquipe1", d)
        self.assertIn("idEngagementEquipe2", d)
        self.assertIn("_geo", d)
        self.assertIn("date_timestamp", d)
        self.assertIn("date_rencontre_timestamp", d)
        self.assertIn("creation_timestamp", d)
        self.assertIn("dateSaisieResultat_timestamp", d)
        self.assertIn("modification_timestamp", d)
        self.assertIn("organisateur", d)
        self.assertEqual(d["niveau_nb"], "3")


# ---------------------------------------------------------------------------
# Additional tests for "False branch" coverage (empty/minimal data)
# These cover the `if self.field is not None:` False paths
# ---------------------------------------------------------------------------


class TestEmptyToDictBranches(unittest.TestCase):
    """Cover the False branches of to_dict (field IS None -> skip)."""

    def test_027_cartographie_empty_to_dict(self) -> None:
        from ffbb_api_client_v2.models.cartographie import Cartographie

        c = Cartographie.from_dict(
            {
                "date_created": None,
                "date_updated": None,
            }
        )
        d = c.to_dict()
        self.assertEqual(d, {})

    def test_028_folder_empty_to_dict(self) -> None:
        from ffbb_api_client_v2.models.folder import Folder

        f = Folder.from_dict({"parent": None})
        d = f.to_dict()
        self.assertEqual(d, {})

    def test_029_document_flyer_minimal_to_dict(self) -> None:
        """Test DocumentFlyer to_dict with only None-typed fields skipped."""
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer

        doc = DocumentFlyer.from_dict(
            {
                "charset": None,
                "duration": None,
                "embed": None,
                "description": None,
                "location": None,
                "tags": None,
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
            }
        )
        d = doc.to_dict()
        # All None-typed fields -> empty dict
        self.assertEqual(d, {})

    def test_030_organisme_id_pere_with_nested_organisme(self) -> None:
        """Cover the organisme_id_pere nested field + more to_dict branches."""
        from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere

        data = {
            "adresse": None,
            "adresseClubPro": None,
            "cartographie": None,
            "code": None,
            "commune": None,
            "communeClubPro": None,
            "date_created": None,
            "date_updated": None,
            "id": None,
            "mail": None,
            "nom": None,
            "nomClubPro": None,
            "organisme_id_pere": {
                "adresse": "nested addr",
                "adresseClubPro": None,
                "cartographie": None,
                "code": "N01",
                "commune": None,
                "communeClubPro": None,
                "date_created": None,
                "date_updated": None,
                "id": "99",
                "mail": None,
                "nom": "Nested Org",
                "nomClubPro": None,
                "organisme_id_pere": None,
                "salle": None,
                "telephone": None,
                "type": None,
                "type_association": None,
                "urlSiteWeb": None,
                "logo": None,
                "nom_simple": None,
                "dateAffiliation": None,
                "saison_en_cours": None,
                "entreprise": None,
                "handibasket": None,
                "omnisport": None,
                "horsAssociation": None,
                "offresPratiques": None,
                "engagements": None,
                "labellisation": None,
            },
            "salle": None,
            "telephone": None,
            "type": None,
            "type_association": None,
            "urlSiteWeb": None,
            "logo": None,
            "nom_simple": None,
            "dateAffiliation": None,
            "saison_en_cours": None,
            "entreprise": None,
            "handibasket": None,
            "omnisport": None,
            "horsAssociation": None,
            "offresPratiques": None,
            "engagements": None,
            "labellisation": None,
        }
        obj = OrganismeIDPere.from_dict(data)
        self.assertIsNotNone(obj.organisme_id_pere)
        self.assertEqual(obj.organisme_id_pere.nom, "Nested Org")
        d = obj.to_dict()
        self.assertIn("organisme_id_pere", d)
        self.assertEqual(d["organisme_id_pere"]["code"], "N01")

    def test_031_organisme_id_pere_empty_to_dict(self) -> None:
        """Cover all False branches in OrganismeIDPere.to_dict."""
        from ffbb_api_client_v2.models.organisme_id_pere import OrganismeIDPere

        data = {
            "adresse": None,
            "adresseClubPro": None,
            "cartographie": None,
            "code": None,
            "commune": None,
            "communeClubPro": None,
            "date_created": None,
            "date_updated": None,
            "id": None,
            "mail": None,
            "nom": None,
            "nomClubPro": None,
            "organisme_id_pere": None,
            "salle": None,
            "telephone": None,
            "type": None,
            "type_association": None,
            "urlSiteWeb": None,
            "logo": None,
            "nom_simple": None,
            "dateAffiliation": None,
            "saison_en_cours": None,
            "entreprise": None,
            "handibasket": None,
            "omnisport": None,
            "horsAssociation": None,
            "offresPratiques": None,
            "engagements": None,
            "labellisation": None,
        }
        obj = OrganismeIDPere.from_dict(data)
        d = obj.to_dict()
        self.assertEqual(d, {})

    def test_032_multi_search_results_to_dict_empty(self) -> None:
        """Cover the False branches of MultiSearchResult.to_dict."""
        from ffbb_api_client_v2.meilisearch_ffbb.models.multi_search_result_organismes import (
            OrganismesMultiSearchResult,
        )

        result = OrganismesMultiSearchResult(
            index_uid=None,
            hits=None,
            query=None,
            processing_time_ms=None,
            limit=None,
            offset=None,
            estimated_total_hits=None,
            facet_distribution=None,
            facet_stats=None,
        )
        d = result.to_dict()
        self.assertEqual(d, {})

    def test_033_multi_search_results_type_error(self) -> None:
        """Cover the TypeError branch in MultiSearchResult.from_dict."""
        from ffbb_api_client_v2.meilisearch.models.multi_search_results import (
            MultiSearchResult,
        )

        # MultiSearchResult itself is the generic base -- calling from_dict
        # on it directly raises (TypeError or AttributeError)
        with self.assertRaises(Exception):
            MultiSearchResult.from_dict({"indexUid": "test"})


if __name__ == "__main__":
    unittest.main()
