"""Tests for GetFormationsResponse model."""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta
from typing import Any

from ffbb_api_client_v2.directus_ffbb.models.get_formations_response import (
    GetFormationsResponse,
)

SAMPLE_DATA: dict[str, Any] = {
    "id": "5faa8064-93a7-4817-9187-dc87c567dc1c",
    "title": "Diplome de Preparateur Physique en Basketball",
    "description": "Formation avancee pour les preparateurs physiques specialises basketball.",
    "mode": "in_person",
    "level": "avance",
    "reference": "FEDE",
    "duration_hours": 40.0,
    "certification": "Certification FFBB Preparateur Physique",
    "status": "published",
    "sort": 10,
    "domain": {"id": "550e8400-e29b-41d4-a716-446655440001", "name": "Transversales"},
    "theme": {
        "id": "550e8400-e29b-41d4-a716-446655440005",
        "name": "Diplome de Preparateur Physique en Basketball",
    },
    "sessions": [
        {
            "id": "sess-001",
            "date_debut": "2025-09-15",
            "date_fin": "2025-09-19",
            "lieu": "INSEP Paris",
        },
        {
            "id": "sess-002",
            "date_debut": "2025-10-13",
            "date_fin": "2025-10-17",
            "lieu": "CREPS Montpellier",
        },
    ],
    "public": "Entraineurs et preparateurs physiques titulaires du BPJEPS Basketball",
    "goals": "Maitriser les fondamentaux de la preparation physique appliquee au basketball",
    "content": "Module 1: Physiologie de l'effort / Module 2: Planification / Module 3: Prevention",
    "pedagogy": "Cours theoriques et ateliers pratiques sur le terrain",
    "prerequisites": "BPJEPS Basketball ou equivalent",
    "results": "Attestation de reussite delivree par la FFBB",
    "modalities": "Presentielle - 2 sessions de 5 jours",
    "image": {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "filename_download": "formation_prep_physique.jpg",
        "type": "image/jpeg",
    },
    "files": [
        {"id": "file-001", "filename": "programme_detaille.pdf"},
        {"id": "file-002", "filename": "bulletin_inscription.pdf"},
    ],
    "idOrigin": "ORIGIN-123",
    "idOriginHash": "aTeHNOrTPV8jXC9appqLTQ%3D%3D",
    "programIdFbi": "FBI-PROG-456",
    "date_created": "2025-01-10T08:00:00.000Z",
    "date_updated": "2025-06-01T14:30:00.000Z",
}


class TestGetFormationsResponse(unittest.TestCase):
    def test_000_from_dict_valid(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)

    def test_001_from_dict_none(self) -> None:
        result = GetFormationsResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_002_from_dict_empty(self) -> None:
        result = GetFormationsResponse.from_dict({})
        self.assertIsNone(result)

    def test_003_from_dict_errors(self) -> None:
        result = GetFormationsResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_004_from_dict_not_dict(self) -> None:
        result = GetFormationsResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_005_from_list_valid(self) -> None:
        result = GetFormationsResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)

    def test_006_from_list_empty(self) -> None:
        result = GetFormationsResponse.from_list([])
        self.assertEqual(result, [])

    def test_007_field_id(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.id, "5faa8064-93a7-4817-9187-dc87c567dc1c")

    def test_008_field_title(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.title, "Diplome de Preparateur Physique en Basketball")

    def test_009_field_description(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("preparateurs physiques", result.description)  # type: ignore[operator]

    def test_010_field_mode(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.mode, "in_person")

    def test_011_field_level(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.level, "avance")

    def test_012_field_reference(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.reference, "FEDE")

    def test_013_field_duration_hours(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.duration_hours, timedelta(hours=40))

    def test_014_field_certification(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(
            result.certification, "Certification FFBB Preparateur Physique"
        )

    def test_015_field_status(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.status, "published")

    def test_016_field_sort(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.sort, 10)

    def test_017_field_domain(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        from ffbb_api_client_v2.models.folder import Folder

        self.assertIsInstance(result.domain, Folder)
        assert isinstance(result.domain, Folder)
        self.assertEqual(result.domain.name, "Transversales")

    def test_018_field_theme(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        from ffbb_api_client_v2.models.folder import Folder

        self.assertIsInstance(result.theme, Folder)
        assert isinstance(result.theme, Folder)
        self.assertIn("Preparateur Physique", result.theme.name)  # type: ignore[operator]

    def test_019_field_sessions(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.sessions, list)
        self.assertEqual(len(result.sessions), 2)
        self.assertEqual(result.sessions[0]["lieu"], "INSEP Paris")

    def test_020_field_public(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("BPJEPS", result.public)  # type: ignore[operator]

    def test_021_field_goals(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("preparation physique", result.goals)  # type: ignore[operator]

    def test_022_field_content(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Module 1", result.content)  # type: ignore[operator]

    def test_023_field_pedagogy(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("ateliers pratiques", result.pedagogy)  # type: ignore[operator]

    def test_024_field_prerequisites(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.prerequisites, "BPJEPS Basketball ou equivalent")

    def test_025_field_results(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("FFBB", result.results)  # type: ignore[operator]

    def test_026_field_modalities(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Presentielle", result.modalities)  # type: ignore[operator]

    def test_027_field_image(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        from ffbb_api_client_v2.models.document_flyer import DocumentFlyer

        self.assertIsInstance(result.image, DocumentFlyer)
        assert isinstance(result.image, DocumentFlyer)
        self.assertEqual(result.image.filename_download, "formation_prep_physique.jpg")

    def test_028_field_files(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.files, list)
        self.assertEqual(len(result.files), 2)

    def test_029_field_date_created(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.date_created, datetime)

    def test_030_field_date_updated(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.date_updated, datetime)

    def test_031_nullable_float_none(self) -> None:
        data = {**SAMPLE_DATA, "duration_hours": None}
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.duration_hours)

    def test_032_nullable_int_none(self) -> None:
        data = {**SAMPLE_DATA, "sort": None}
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.sort)

    def test_033_nullable_dicts_none(self) -> None:
        data = {
            **SAMPLE_DATA,
            "domain": None,
            "theme": None,
            "image": None,
        }
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.domain)
        self.assertIsNone(result.theme)
        self.assertIsNone(result.image)

    def test_034_lists_default_to_empty(self) -> None:
        data = {**SAMPLE_DATA, "sessions": None, "files": None}
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertEqual(result.sessions, [])
        self.assertEqual(result.files, [])

    def test_035_from_list_filters_none_items(self) -> None:
        result = GetFormationsResponse.from_list([SAMPLE_DATA, {}, SAMPLE_DATA])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
