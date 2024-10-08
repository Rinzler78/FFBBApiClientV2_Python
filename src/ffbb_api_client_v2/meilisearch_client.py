from typing import List

from requests_cache import CachedSession

from .http_requests_helper import catch_result, default_cached_session
from .http_requests_utils import http_post_json
from .multi_search_query import MultiSearchQuery
from .MultiSearchResults import MultiSearchResults, multi_search_results_from_dict


class MeilisearchClient:
    def __init__(
        self,
        bearer_token: str,
        url: str,
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        """
        Initializes an instance of the ApiFFBBAppClient class.

        Args:
            bearer_token (str): The bearer token used for authentication.
            url (str, optional): The base URL.
            debug (bool, optional): Whether to enable debug mode. Defaults to False.
            cached_session (CachedSession, optional): The cached session to use.
        """
        if not bearer_token:
            raise ValueError("Bearer token cannot be None or empty.")

        self.bearer_token = bearer_token

        if not url:
            raise ValueError("URL cannot be None or empty.")

        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }

    def multi_search(
        self,
        queries: List[MultiSearchQuery] = None,
        cached_session: CachedSession = None,
    ) -> MultiSearchResults:
        url = f"{self.url}multi-search"
        params = {"queries": [query.to_dict() for query in queries] if queries else []}
        return catch_result(
            lambda: multi_search_results_from_dict(
                http_post_json(
                    url,
                    self.headers,
                    params,
                    debug=self.debug,
                    cached_session=cached_session or self.cached_session,
                )
            )
        )
