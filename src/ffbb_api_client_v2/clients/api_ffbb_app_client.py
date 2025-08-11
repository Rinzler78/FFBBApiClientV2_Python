from typing import Any, Optional

from requests_cache import CachedSession

from ..helpers.http_requests_helper import catch_result, default_cached_session
from ..helpers.http_requests_utils import http_get_json, url_with_params
from ..models.lives import Live, lives_from_dict


class ApiFFBBAppClient:
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://api.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        """
        Initializes an instance of the ApiFFBBAppClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL. Defaults to "https://api.ffbb.app/".
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (CachedSession, optional): The cached session to use.
        """
        if not bearer_token:
            raise ValueError("bearer_token cannot be None or empty")
        self.bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {"Authorization": f"Bearer {self.bearer_token}"}

    def get_lives(self, cached_session: CachedSession = None) -> list[Live]:
        """
        Retrieves a list of live events.

        Args:
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[Live]: A list of Live objects representing the live events.
        """
        url = f"{self.url}json/lives.json"
        return catch_result(
            lambda: lives_from_dict(
                http_get_json(
                    url,
                    self.headers,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                )
            )
        )

    def get_competition(
        self,
        competition_id: int,
        deep_limit: Optional[str] = "1000",
        fields: Optional[list[str]] = None,
        cached_session: CachedSession = None,
    ) -> dict[str, Any]:
        """
        Retrieves detailed information about a competition.

        Args:
            competition_id (int): The ID of the competition
            deep_limit (str, optional): Limit for nested rencontres. Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            Dict[str, Any]: Competition data with nested phases, poules, and rencontres
        """
        url = f"{self.url}items/ffbbserver_competitions/{competition_id}"

        params = {}
        if deep_limit:
            params["deep[phases][poules][rencontres][_limit]"] = deep_limit

        if fields:
            for field in fields:
                if "fields[]" not in params:
                    params["fields[]"] = []
                params["fields[]"].append(field)
        else:
            # Default fields from descriptor
            default_fields = [
                "id",
                "nom",
                "sexe",
                "categorie.code",
                "categorie.ordre",
                "saison",
                "code",
                "typeCompetition",
                "liveStat",
                "competition_origine",
                "competition_origine_nom",
                "phases.id",
                "phases.nom",
                "phases.poules.rencontres.id",
            ]
            params["fields[]"] = default_fields

        final_url = url_with_params(url, params)
        return catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

    def get_poule(
        self,
        poule_id: int,
        deep_limit: Optional[str] = "1000",
        fields: Optional[list[str]] = None,
        cached_session: CachedSession = None,
    ) -> dict[str, Any]:
        """
        Retrieves detailed information about a poule.

        Args:
            poule_id (int): The ID of the poule
            deep_limit (str, optional): Limit for nested rencontres. Defaults to "1000".
            fields (List[str], optional): List of fields to retrieve
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            Dict[str, Any]: Poule data with rencontres
        """
        url = f"{self.url}items/ffbbserver_poules/{poule_id}"

        params = {}
        if deep_limit:
            params["deep[rencontres][_limit]"] = deep_limit

        if fields:
            params["fields[]"] = fields
        else:
            # Default fields from descriptor
            default_fields = [
                "id",
                "rencontres.id",
                "rencontres.numero",
                "rencontres.numeroJournee",
                "rencontres.idPoule",
                "rencontres.competitionId",
                "rencontres.resultatEquipe1",
                "rencontres.resultatEquipe2",
                "rencontres.joue",
                "rencontres.nomEquipe1",
                "rencontres.nomEquipe2",
                "rencontres.date_rencontre",
            ]
            params["fields[]"] = default_fields

        final_url = url_with_params(url, params)
        return catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

    def get_saisons(
        self,
        fields: Optional[list[str]] = None,
        filter_criteria: Optional[str] = '{"actif":{"_eq":true}}',
        cached_session: CachedSession = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieves list of seasons.

        Args:
            fields (List[str], optional): List of fields to retrieve.
                Defaults to ["id"].
            filter_criteria (str, optional): JSON filter criteria.
                Defaults to active seasons.
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            List[Dict[str, Any]]: List of season data
        """
        url = f"{self.url}items/ffbbserver_saisons"

        params = {}
        if fields:
            params["fields[]"] = fields
        else:
            params["fields[]"] = ["id"]

        if filter_criteria:
            params["filter"] = filter_criteria

        final_url = url_with_params(url, params)
        return catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )

    def get_organisme(
        self,
        organisme_id: int,
        fields: Optional[list[str]] = None,
        cached_session: CachedSession = None,
    ) -> dict[str, Any]:
        """
        Retrieves detailed information about an organisme.

        Args:
            organisme_id (int): The ID of the organisme
            fields (List[str], optional): List of fields to retrieve
            cached_session (CachedSession, optional): The cached session to use

        Returns:
            Dict[str, Any]: Organisme data with members, competitions, etc.
        """
        url = f"{self.url}items/ffbbserver_organismes/{organisme_id}"

        params = {}
        if fields:
            params["fields[]"] = fields
        else:
            # Default fields from descriptor
            default_fields = [
                "id",
                "nom",
                "code",
                "telephone",
                "adresse",
                "commune.codePostal",
                "commune.libelle",
                "mail",
                "type",
                "nom_simple",
                "urlSiteWeb",
                "competitions.id",
                "competitions.nom",
                "engagements.id",
                "membres.id",
                "membres.nom",
                "membres.prenom",
            ]
            params["fields[]"] = default_fields

        final_url = url_with_params(url, params)
        return catch_result(
            lambda: http_get_json(
                final_url,
                self.headers,
                debug=self.debug,
                cached_session=cached_session or self.cached_session,
            )
        )
