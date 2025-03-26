from typing import List

from requests_cache import CachedSession

from .http_requests_helper import catch_result, default_cached_session
from .http_requests_utils import http_get_json
from .lives import Live, lives_from_dict


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

    def get_lives(self, cached_session: CachedSession = None) -> List[Live]:
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
