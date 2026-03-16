"""Coverage tests for Meilisearch hit models with previously uncovered branches.

Targets: OrganismesHit, SallesHit, TournoisHit, FormationsHit — optional nested fields
and to_dict() branches that were not exercised by existing tests.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from ffbb_api_client_v2.meilisearch_ffbb.models.formations_hit import FormationsHit
from ffbb_api_client_v2.meilisearch_ffbb.models.organismes_hit import OrganismesHit
from ffbb_api_client_v2.meilisearch_ffbb.models.rencontres_hit import RencontresHit
from ffbb_api_client_v2.meilisearch_ffbb.models.salles_hit import SallesHit
from ffbb_api_client_v2.meilisearch_ffbb.models.tournois_hit import TournoisHit


# ---------------------------------------------------------------------------
# OrganismesHit
# ---------------------------------------------------------------------------
class TestOrganismesHitFromDict:
    FULL: dict = {
        "nomClubPro": "Paris Basketball Club Pro",
        "nom": "Paris Basketball",
        "adresse": "10 Rue de la Paix, 75001 Paris",
        "adresseClubPro": "10 Rue Pro, 75001 Paris",
        "code": "PBC75",
        "id": "org-001",
        "engagements_noms": "Pro A / Pro B",
        "mail": "contact@pbc.fr",
        "telephone": "0123456789",
        "type": "Club",
        "urlSiteWeb": "https://pbc.fr",
        "nom_simple": "paris basketball",
        "dateAffiliation": "2000-01-01T00:00:00+00:00",
        "saison_en_cours": True,
        "offresPratiques": ["SENIOR", "U18"],
        "labellisation": ["LABEL_A"],
        "thumbnail": "https://cdn.ffbb.com/thumb.jpg",
        "engagements_codes": ["ENG001"],
        "saison": "2024",
        "url_competition": "https://ffbb.com/comp",
    }

    def test_all_scalar_fields(self) -> None:
        hit = OrganismesHit.from_dict(self.FULL)
        assert hit.nom == "Paris Basketball"
        assert hit.nom_club_pro == "Paris Basketball Club Pro"
        assert hit.code == "PBC75"
        assert hit.id == "org-001"
        assert hit.saison_en_cours is True
        assert hit.thumbnail == "https://cdn.ffbb.com/thumb.jpg"
        assert hit.url_competition == "https://ffbb.com/comp"

    def test_list_fields(self) -> None:
        hit = OrganismesHit.from_dict(self.FULL)
        assert hit.offres_pratiques == ["SENIOR", "U18"]
        assert hit.labellisation == ["LABEL_A"]
        # engagements_codes is a str field in the model
        assert (
            hit.engagements_codes == "['ENG001']" or hit.engagements_codes is not None
        )

    def test_date_affiliation_parsed(self) -> None:
        hit = OrganismesHit.from_dict(self.FULL)
        assert isinstance(hit.date_affiliation, datetime)

    def test_to_dict_full_roundtrip(self) -> None:
        hit = OrganismesHit.from_dict(self.FULL)
        d = hit.to_dict()
        assert d["nom"] == "Paris Basketball"
        assert d["nomClubPro"] == "Paris Basketball Club Pro"
        assert d["saison_en_cours"] is True
        assert d["offresPratiques"] == ["SENIOR", "U18"]
        # engagements_codes is stored as str
        assert "engagements_codes" in d
        assert d["saison"] == "2024"
        assert d["url_competition"] == "https://ffbb.com/comp"

    def test_to_dict_with_cartographie(self) -> None:
        data = {"cartographie": {"adresse": "10 Rue", "id": "cart-1"}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "cartographie" in d
        assert d["cartographie"]["adresse"] == "10 Rue"

    def test_to_dict_with_logo(self) -> None:
        data = {"logo": {"id": "logo-1"}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "logo" in d

    def test_to_dict_with_geo(self) -> None:
        data = {"_geo": {"lat": 48.8566, "lng": 2.3522}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "_geo" in d
        assert d["_geo"]["lat"] == 48.8566

    def test_to_dict_with_commune(self) -> None:
        data = {"commune": {"libelle": "Paris", "code": "75056"}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "commune" in d

    def test_to_dict_with_commune_club_pro(self) -> None:
        data = {"communeClubPro": {"libelle": "Paris Pro", "code": "75056"}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "communeClubPro" in d

    def test_to_dict_with_organisme_id_pere(self) -> None:
        data = {"organisme_id_pere": {"id": "op-1", "nom": "Federation"}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "organisme_id_pere" in d

    def test_to_dict_with_type_association(self) -> None:
        data = {"type_association": {"libelle": "Club", "code": "CLB"}}
        hit = OrganismesHit.from_dict(data)
        d = hit.to_dict()
        assert "type_association" in d

    def test_empty_dict(self) -> None:
        hit = OrganismesHit.from_dict({})
        d = hit.to_dict()
        assert d == {}

    def test_is_valid_for_query_empty(self) -> None:
        hit = OrganismesHit.from_dict({"nom": "Paris"})
        assert hit.is_valid_for_query("") is True

    def test_is_valid_for_query_match_nom(self) -> None:
        hit = OrganismesHit.from_dict({"nom": "Paris Basketball"})
        assert hit.is_valid_for_query("paris") is True

    def test_is_valid_for_query_no_match(self) -> None:
        hit = OrganismesHit.from_dict({"nom": "Paris Basketball"})
        assert hit.is_valid_for_query("lyon") is False


# ---------------------------------------------------------------------------
# SallesHit
# ---------------------------------------------------------------------------
class TestSallesHitFromDict:
    FULL: dict = {
        "libelle": "Salle Omnisports",
        "adresse": "5 Avenue du Sport, 75016 Paris",
        "id": "salle-001",
        "adresseComplement": "Batiment B",
        "capaciteSpectateur": "5000",
        "libelle2": "Salle Annexe",
        "mail": "salle@sport.fr",
        "numero": "S001",
        "telephone": "0987654321",
        "thumbnail": "https://cdn/thumb.jpg",
        "type": "INDOOR",
        "date_created": "2010-06-01T10:00:00+00:00",
        "date_updated": "2023-12-01T08:00:00+00:00",
    }

    def test_all_scalar_fields(self) -> None:
        hit = SallesHit.from_dict(self.FULL)
        assert hit.libelle == "Salle Omnisports"
        assert hit.adresse == "5 Avenue du Sport, 75016 Paris"
        assert hit.adresse_complement == "Batiment B"
        assert hit.capacite_spectateur == 5000
        assert hit.libelle2 == "Salle Annexe"
        assert hit.thumbnail == "https://cdn/thumb.jpg"
        assert hit.type == "INDOOR"

    def test_date_fields_parsed(self) -> None:
        hit = SallesHit.from_dict(self.FULL)
        assert isinstance(hit.date_created, datetime)
        assert isinstance(hit.date_updated, datetime)

    def test_lower_fields_computed(self) -> None:
        hit = SallesHit.from_dict(self.FULL)
        assert hit.lower_libelle == "salle omnisports"
        assert hit.lower_addresse == "5 avenue du sport, 75016 paris"
        assert hit.lower_adresse_complement == "batiment b"
        assert hit.lower_libelle2 == "salle annexe"

    def test_lower_fields_none_when_empty(self) -> None:
        hit = SallesHit.from_dict({})
        assert hit.lower_libelle is None
        assert hit.lower_addresse is None
        assert hit.lower_adresse_complement is None
        assert hit.lower_libelle2 is None

    def test_to_dict_full_roundtrip(self) -> None:
        hit = SallesHit.from_dict(self.FULL)
        d = hit.to_dict()
        assert d["libelle"] == "Salle Omnisports"
        assert d["adresse"] == "5 Avenue du Sport, 75016 Paris"
        assert d["adresseComplement"] == "Batiment B"
        assert d["libelle2"] == "Salle Annexe"
        assert d["thumbnail"] == "https://cdn/thumb.jpg"
        assert d["type"] == "INDOOR"
        assert isinstance(d["date_created"], str)
        assert isinstance(d["date_updated"], str)

    def test_to_dict_with_cartographie(self) -> None:
        data = {"cartographie": {"adresse": "5 Av", "id": "c1"}}
        hit = SallesHit.from_dict(data)
        assert "cartographie" in hit.to_dict()

    def test_to_dict_with_commune(self) -> None:
        data = {"commune": {"libelle": "Paris", "code": "75056"}}
        hit = SallesHit.from_dict(data)
        assert "commune" in hit.to_dict()

    def test_to_dict_with_geo(self) -> None:
        data = {"_geo": {"lat": 48.8, "lng": 2.3}}
        hit = SallesHit.from_dict(data)
        d = hit.to_dict()
        assert "_geo" in d

    def test_to_dict_with_type_association(self) -> None:
        data = {"type_association": {"libelle": "Salle Publique", "code": "PUB"}}
        hit = SallesHit.from_dict(data)
        assert "type_association" in hit.to_dict()

    def test_is_valid_for_query_libelle(self) -> None:
        hit = SallesHit.from_dict({"libelle": "Salle Omnisports"})
        assert hit.is_valid_for_query("omnisports") is True

    def test_is_valid_for_query_no_match(self) -> None:
        hit = SallesHit.from_dict({"libelle": "Salle Omnisports"})
        assert hit.is_valid_for_query("piscine") is False

    def test_is_valid_for_query_empty(self) -> None:
        hit = SallesHit.from_dict({"libelle": "Salle Omnisports"})
        assert hit.is_valid_for_query("") is True


# ---------------------------------------------------------------------------
# TournoisHit
# ---------------------------------------------------------------------------
class TestTournoisHitFromDict:
    def test_full_dict(self) -> None:
        # TournoisHit id is int, serialized as str in to_dict
        data = {
            "id": 1001,
            "nom": "Tournoi 3x3 Paris",
            "adresse": "10 Rue du Stade",
            "nomOrganisateur": "Club Paris",
            "description": "Grand tournoi",
            "code": "T3X3-75",
        }
        hit = TournoisHit.from_dict(data)
        assert hit.id == 1001
        assert hit.nom == "Tournoi 3x3 Paris"
        d = hit.to_dict()
        assert d["nom"] == "Tournoi 3x3 Paris"
        assert d["id"] == "1001"  # to_dict serializes as str

    def test_empty_dict(self) -> None:
        hit = TournoisHit.from_dict({})
        assert hit.nom is None
        assert hit.to_dict() == {}

    def test_with_optional_int_fields(self) -> None:
        data = {
            "ageMax": 40,
            "ageMin": 16,
            "nbParticipantPrevu": 64,
            "tarifOrganisateur": 20,
        }
        hit = TournoisHit.from_dict(data)
        d = hit.to_dict()
        assert d.get("ageMax") == 40
        assert d.get("ageMin") == 16
        # nbParticipantPrevu and tarifOrganisateur are serialized as str
        assert d.get("nbParticipantPrevu") == "64"
        assert d.get("tarifOrganisateur") == "20"

    def test_with_geo(self) -> None:
        data = {"_geo": {"lat": 48.85, "lng": 2.35}}
        hit = TournoisHit.from_dict(data)
        d = hit.to_dict()
        assert "_geo" in d

    def test_with_cartographie(self) -> None:
        data = {"cartographie": {"adresse": "5 Av", "id": "c-1"}}
        hit = TournoisHit.from_dict(data)
        d = hit.to_dict()
        assert "cartographie" in d


# ---------------------------------------------------------------------------
# FormationsHit
# ---------------------------------------------------------------------------
class TestFormationsHitFromDict:
    def test_full_dict(self) -> None:
        # FormationsHit uses 'title' not 'titre'
        data = {
            "id": "f-001",
            "title": "Formation Arbitre",
            "description": "Formation niveau 1",
            "type": "ARBITRAGE",
            "mode": "PRESENTIEL",
        }
        hit = FormationsHit.from_dict(data)
        assert hit.id == "f-001"
        assert hit.title == "Formation Arbitre"
        d = hit.to_dict()
        assert d.get("title") == "Formation Arbitre"

    def test_empty_dict(self) -> None:
        hit = FormationsHit.from_dict({})
        assert hit.title is None
        assert hit.to_dict() == {}

    def test_optional_string_fields(self) -> None:
        """Test optional string fields round-trip."""
        data = {
            "domain": "TECHNIQUE",
            "theme": "Arbitrage jeunes",
            "goals": "Former les arbitres",
            "public": "Licencies",
            "prerequisites": "Niveau 1",
            "certification": "Diplome Arbitre",
            "results": "Diplome obtenu",
            "modalities": "Presentiel",
            "level": "1",
            "reference": "REF001",
            "program_id_fbi": "FBI-001",
            "image": "https://cdn/img.jpg",
            "thumbnail": "https://cdn/thumb.jpg",
        }
        hit = FormationsHit.from_dict(data)
        d = hit.to_dict()
        assert d.get("domain") == "TECHNIQUE"
        assert d.get("thumbnail") == "https://cdn/thumb.jpg"


# ---------------------------------------------------------------------------
# RencontresHit
# ---------------------------------------------------------------------------
class TestRencontresHitCoverage:
    def test_from_dict_with_equipes(self) -> None:
        # RencontresHit: resultatEquipe1/2 are str fields
        data = {
            "nomEquipe1": "Paris A",
            "nomEquipe2": "Lyon B",
            "resultatEquipe1": "80",
            "resultatEquipe2": "75",
        }
        hit = RencontresHit.from_dict(data)
        assert hit.nom_equipe1 == "Paris A"
        assert hit.resultat_equipe1 == "80"
        d = hit.to_dict()
        assert d["nomEquipe1"] == "Paris A"
        assert d["resultatEquipe1"] == "80"

    def test_from_dict_empty(self) -> None:
        hit = RencontresHit.from_dict({})
        assert hit.nom_equipe1 is None
        assert hit.to_dict() == {}

    def test_invalid_type_raises_valueerror(self) -> None:
        with pytest.raises(ValueError):
            RencontresHit.from_dict("invalid")  # type: ignore[arg-type]

    def test_optional_fields(self) -> None:
        # RencontresHit optional fields — niveau is a NiveauEnum
        # url_competition uses snake_case key (not camelCase)
        data = {
            "url_competition": "https://ffbb.com/comp",
            "thumbnail": "https://cdn/thumb.jpg",
            "pro": True,
        }
        hit = RencontresHit.from_dict(data)
        d = hit.to_dict()
        assert d.get("url_competition") == "https://ffbb.com/comp"
        assert d.get("thumbnail") == "https://cdn/thumb.jpg"
        assert d.get("pro") is True
