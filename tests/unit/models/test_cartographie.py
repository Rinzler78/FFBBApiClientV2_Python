"""Tests for Cartographie model — from_dict / to_dict round-trip and edge cases."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest

from ffbb_api_client_v2.models.cartographie import Cartographie
from ffbb_api_client_v2.models.coordonnees import Coordonnees

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FULL_DICT: dict[str, Any] = {
    "adresse": "1 Rue de la Paix",
    "codePostal": "75001",
    "coordonnees": {"type": "Point", "coordinates": [2.3311, 48.8699]},
    "date_created": "2023-01-15T10:00:00+00:00",
    "date_updated": "2024-06-01T08:30:00+00:00",
    "id": "carto-abc-123",
    "latitude": 48.8699,
    "longitude": 2.3311,
    "title": "Palais Royal",
    "ville": "Paris",
    "status": "published",
}


# ---------------------------------------------------------------------------
# from_dict
# ---------------------------------------------------------------------------


class TestCartographieFromDict:
    def test_all_fields_present(self) -> None:
        carto = Cartographie.from_dict(FULL_DICT)
        assert carto.adresse == "1 Rue de la Paix"
        assert carto.code_postal == "75001"
        assert carto.cartographie_id == "carto-abc-123"
        assert carto.latitude == 48.8699
        assert carto.longitude == 2.3311
        assert carto.title == "Palais Royal"
        assert carto.ville == "Paris"
        assert carto.status == "published"

    def test_date_fields_parsed(self) -> None:
        carto = Cartographie.from_dict(FULL_DICT)
        assert isinstance(carto.date_created, datetime)
        assert isinstance(carto.date_updated, datetime)
        assert carto.date_created.year == 2023
        assert carto.date_updated.year == 2024

    def test_coordonnees_nested(self) -> None:
        carto = Cartographie.from_dict(FULL_DICT)
        assert isinstance(carto.coordonnees, Coordonnees)
        assert carto.coordonnees.type == "Point"
        assert carto.coordonnees.coordinates == [2.3311, 48.8699]

    def test_empty_dict_returns_all_none(self) -> None:
        carto = Cartographie.from_dict({})
        assert carto.adresse is None
        assert carto.code_postal is None
        assert carto.coordonnees is None
        assert carto.date_created is None
        assert carto.date_updated is None
        assert carto.cartographie_id is None
        assert carto.latitude is None
        assert carto.longitude is None
        assert carto.title is None
        assert carto.ville is None
        assert carto.status is None

    def test_raises_on_non_dict(self) -> None:
        with pytest.raises(TypeError):
            Cartographie.from_dict("not a dict")  # type: ignore[arg-type]

    def test_raises_on_none(self) -> None:
        with pytest.raises(TypeError):
            Cartographie.from_dict(None)  # type: ignore[arg-type]

    def test_raises_on_list(self) -> None:
        with pytest.raises(TypeError):
            Cartographie.from_dict([])  # type: ignore[arg-type]

    def test_partial_dict(self) -> None:
        data = {"adresse": "10 Avenue Montaigne", "ville": "Paris"}
        carto = Cartographie.from_dict(data)
        assert carto.adresse == "10 Avenue Montaigne"
        assert carto.ville == "Paris"
        assert carto.code_postal is None
        assert carto.latitude is None

    def test_null_coordonnees_field(self) -> None:
        data = {**FULL_DICT, "coordonnees": None}
        carto = Cartographie.from_dict(data)
        assert carto.coordonnees is None

    def test_numeric_latitude_longitude(self) -> None:
        data = {**FULL_DICT, "latitude": "43.2965", "longitude": "5.3698"}
        # from_float coerces strings
        carto = Cartographie.from_dict(data)
        assert carto.latitude == pytest.approx(43.2965)
        assert carto.longitude == pytest.approx(5.3698)


# ---------------------------------------------------------------------------
# to_dict
# ---------------------------------------------------------------------------


class TestCartographieToDict:
    def test_full_roundtrip(self) -> None:
        carto = Cartographie.from_dict(FULL_DICT)
        result = carto.to_dict()
        assert result["adresse"] == "1 Rue de la Paix"
        assert result["codePostal"] == "75001"
        assert result["id"] == "carto-abc-123"
        assert result["latitude"] == 48.8699
        assert result["longitude"] == 2.3311
        assert result["title"] == "Palais Royal"
        assert result["ville"] == "Paris"
        assert result["status"] == "published"
        assert isinstance(result["coordonnees"], dict)
        assert result["coordonnees"]["type"] == "Point"

    def test_date_serialised_to_isoformat(self) -> None:
        carto = Cartographie.from_dict(FULL_DICT)
        result = carto.to_dict()
        assert isinstance(result["date_created"], str)
        assert isinstance(result["date_updated"], str)
        # Must be valid ISO format
        datetime.fromisoformat(result["date_created"])
        datetime.fromisoformat(result["date_updated"])

    def test_empty_object_produces_empty_dict(self) -> None:
        carto = Cartographie()
        result = carto.to_dict()
        assert result == {}

    def test_none_fields_excluded(self) -> None:
        carto = Cartographie(adresse="Rue Test", ville=None)
        result = carto.to_dict()
        assert "adresse" in result
        assert "ville" not in result

    def test_partial_fields_roundtrip(self) -> None:
        data = {"adresse": "Quai des Brumes", "latitude": 47.2184, "status": "draft"}
        carto = Cartographie.from_dict(data)
        result = carto.to_dict()
        assert result["adresse"] == "Quai des Brumes"
        assert result["latitude"] == 47.2184
        assert result["status"] == "draft"
        assert "ville" not in result
        assert "codePostal" not in result


# ---------------------------------------------------------------------------
# Dataclass constructor
# ---------------------------------------------------------------------------


class TestCartographieConstructor:
    def test_default_construction(self) -> None:
        carto = Cartographie()
        assert carto.adresse is None
        assert carto.latitude is None

    def test_keyword_construction(self) -> None:
        carto = Cartographie(adresse="Test", latitude=48.0, longitude=2.0)
        assert carto.adresse == "Test"
        assert carto.latitude == 48.0
        assert carto.longitude == 2.0

    def test_with_coordonnees(self) -> None:
        coords = Coordonnees(type="Point", coordinates=[1.0, 2.0])
        carto = Cartographie(coordonnees=coords)
        assert carto.coordonnees is coords
        result = carto.to_dict()
        assert result["coordonnees"] == {"type": "Point", "coordinates": [1.0, 2.0]}
