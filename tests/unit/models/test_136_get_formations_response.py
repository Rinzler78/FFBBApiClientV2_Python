"""Tests for GetFormationsResponse model."""

from __future__ import annotations

import unittest
from typing import Any

from ffbb_api_client_v2.models.get_formations_response import (
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
    "domain": {"id": "1", "libelle": "Transversales"},
    "theme": {
        "id": "5",
        "libelle": "Diplome de Preparateur Physique en Basketball",
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
        "id": "img-001",
        "filename": "formation_prep_physique.jpg",
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
    def test_from_dict_valid(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        self.assertIsNotNone(result)

    def test_from_dict_none(self) -> None:
        result = GetFormationsResponse.from_dict(None)  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_from_dict_empty(self) -> None:
        result = GetFormationsResponse.from_dict({})
        self.assertIsNone(result)

    def test_from_dict_errors(self) -> None:
        result = GetFormationsResponse.from_dict({"errors": [{"message": "err"}]})
        self.assertIsNone(result)

    def test_from_dict_not_dict(self) -> None:
        result = GetFormationsResponse.from_dict("not a dict")  # type: ignore[arg-type]
        self.assertIsNone(result)

    def test_from_list_valid(self) -> None:
        result = GetFormationsResponse.from_list([SAMPLE_DATA, SAMPLE_DATA])
        self.assertEqual(len(result), 2)

    def test_from_list_empty(self) -> None:
        result = GetFormationsResponse.from_list([])
        self.assertEqual(result, [])

    def test_field_id(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.id, "5faa8064-93a7-4817-9187-dc87c567dc1c")

    def test_field_title(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.title, "Diplome de Preparateur Physique en Basketball")

    def test_field_description(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("preparateurs physiques", result.description)  # type: ignore[operator]

    def test_field_mode(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.mode, "in_person")

    def test_field_level(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.level, "avance")

    def test_field_reference(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.reference, "FEDE")

    def test_field_duration_hours(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.duration_hours, 40.0)

    def test_field_certification(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(
            result.certification, "Certification FFBB Preparateur Physique"
        )

    def test_field_status(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.status, "published")

    def test_field_sort(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.sort, 10)

    def test_field_domain(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.domain, dict)
        self.assertEqual(result.domain["libelle"], "Transversales")  # type: ignore[index]

    def test_field_theme(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.theme, dict)
        self.assertIn("Preparateur Physique", result.theme["libelle"])  # type: ignore[index]

    def test_field_sessions(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.sessions, list)
        self.assertEqual(len(result.sessions), 2)
        self.assertEqual(result.sessions[0]["lieu"], "INSEP Paris")

    def test_field_public(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("BPJEPS", result.public)  # type: ignore[operator]

    def test_field_goals(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("preparation physique", result.goals)  # type: ignore[operator]

    def test_field_content(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Module 1", result.content)  # type: ignore[operator]

    def test_field_pedagogy(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("ateliers pratiques", result.pedagogy)  # type: ignore[operator]

    def test_field_prerequisites(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.prerequisites, "BPJEPS Basketball ou equivalent")

    def test_field_results(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("FFBB", result.results)  # type: ignore[operator]

    def test_field_modalities(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIn("Presentielle", result.modalities)  # type: ignore[operator]

    def test_field_image(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.image, dict)
        self.assertEqual(
            result.image["filename"], "formation_prep_physique.jpg"  # type: ignore[index]
        )

    def test_field_files(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertIsInstance(result.files, list)
        self.assertEqual(len(result.files), 2)

    def test_field_date_created(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_created, "2025-01-10T08:00:00.000Z")

    def test_field_date_updated(self) -> None:
        result = GetFormationsResponse.from_dict(SAMPLE_DATA)
        assert result is not None
        self.assertEqual(result.date_updated, "2025-06-01T14:30:00.000Z")

    def test_nullable_float_none(self) -> None:
        data = {**SAMPLE_DATA, "duration_hours": None}
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.duration_hours)

    def test_nullable_int_none(self) -> None:
        data = {**SAMPLE_DATA, "sort": None}
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertIsNone(result.sort)

    def test_nullable_dicts_none(self) -> None:
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

    def test_lists_default_to_empty(self) -> None:
        data = {**SAMPLE_DATA, "sessions": None, "files": None}
        result = GetFormationsResponse.from_dict(data)
        assert result is not None
        self.assertEqual(result.sessions, [])
        self.assertEqual(result.files, [])

    def test_from_list_filters_none_items(self) -> None:
        result = GetFormationsResponse.from_list([SAMPLE_DATA, {}, SAMPLE_DATA])
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
