"""Coverage tests for Directus models with uncovered branches.

Targets:
- directus_ffbb.models.rankings_models: re-export shim (0% coverage)
- directus_ffbb.models.query_fields_manager: abstract base class
- directus_ffbb.models.get_competition_response: line 65
- directus_ffbb.models.get_organisme_response: line 71
"""

from __future__ import annotations

import pytest

from ffbb_api_client_v2.directus_ffbb.models.get_competition_response import (
    GetCompetitionResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.get_organisme_response import (
    GetOrganismeResponse,
)
from ffbb_api_client_v2.directus_ffbb.models.query_fields_manager import (
    QueryFieldsManager,
)
from ffbb_api_client_v2.directus_ffbb.models.rankings_models import (
    RankingEngagement,
    TeamRanking,
)


# ---------------------------------------------------------------------------
# rankings_models re-export shim
# ---------------------------------------------------------------------------
class TestRankingsModelsReexport:
    def test_ranking_engagement_importable(self) -> None:
        """RankingEngagement should be importable from rankings_models."""
        assert RankingEngagement is not None

    def test_team_ranking_importable(self) -> None:
        """TeamRanking should be importable from rankings_models."""
        assert TeamRanking is not None

    def test_ranking_engagement_from_dict(self) -> None:
        # RankingEngagement fields: id, nom, nom_usuel, etc.
        data = {"id": "team-1", "nom": "Paris A"}
        obj = RankingEngagement.from_dict(data)
        assert obj is not None
        assert obj.nom == "Paris A"

    def test_team_ranking_from_dict(self) -> None:
        obj = TeamRanking.from_dict({"id": 1})
        assert obj is not None


# ---------------------------------------------------------------------------
# QueryFieldsManager abstract class
# ---------------------------------------------------------------------------
class TestQueryFieldsManagerAbstract:
    def test_cannot_instantiate_directly(self) -> None:
        with pytest.raises(TypeError):
            QueryFieldsManager()  # type: ignore[abstract]

    def test_concrete_subclass_works(self) -> None:
        class ConcreteManager(QueryFieldsManager):
            @classmethod
            def get_fields(cls) -> list[str]:
                return ["field1", "field2", "field3"]

        fields = ConcreteManager.get_fields()
        assert fields == ["field1", "field2", "field3"]
        assert isinstance(ConcreteManager(), ConcreteManager)


# ---------------------------------------------------------------------------
# GetCompetitionResponse — line 65 (optional field)
# ---------------------------------------------------------------------------
class TestGetCompetitionResponseCoverage:
    def test_from_dict_basic_fields(self) -> None:
        """Test basic fields (id is str in this model)."""
        data = {"id": "100", "nom": "Pro A", "sexe": "M"}
        response = GetCompetitionResponse.from_dict(data)
        assert response.id == "100"
        assert response.nom == "Pro A"

    def test_from_dict_with_poules_list(self) -> None:
        """Test that 'poules' list is correctly parsed when present."""
        data = {
            "id": "100",
            "nom": "Pro A",
            "poules": [],  # empty list still exercises the branch
        }
        response = GetCompetitionResponse.from_dict(data)
        assert response.poules == []

    def test_from_dict_without_poules(self) -> None:
        data = {"id": "200", "nom": "National 1"}
        response = GetCompetitionResponse.from_dict(data)
        assert response.id == "200"
        assert response.poules == []  # defaults to empty list

    def test_from_dict_with_phases(self) -> None:
        """Test phases and competition fields."""
        data = {"id": "300", "nom": "Ligue A", "phases": [], "pro": True}
        response = GetCompetitionResponse.from_dict(data)
        assert response.id == "300"
        assert response.pro is True


# ---------------------------------------------------------------------------
# GetOrganismeResponse — line 71 (optional field)
# ---------------------------------------------------------------------------
class TestGetOrganismeResponseCoverage:
    def test_from_dict_with_engagements(self) -> None:
        """Test that 'engagements' field is parsed when present."""
        data = {
            "id": "99",  # id is str in this model
            "nom": "Club Paris",
            "engagements": [1, 2, 3],
        }
        response = GetOrganismeResponse.from_dict(data)
        assert response.id == "99"
        assert response.nom == "Club Paris"
        assert response.engagements is not None

    def test_from_dict_without_engagements(self) -> None:
        data = {"id": "88", "nom": "Club Lyon"}
        response = GetOrganismeResponse.from_dict(data)
        assert response.id == "88"
        assert response.engagements == []  # defaults to empty list

    def test_from_dict_basic_fields(self) -> None:
        data = {
            "id": "99",
            "nom": "Club Paris",
            "telephone": "0123456789",
            "mail": "info@club.fr",
            "code": "PBC75",
        }
        response = GetOrganismeResponse.from_dict(data)
        assert response.nom == "Club Paris"
        assert response.telephone == "0123456789"
        assert response.code == "PBC75"
