from requests_cache import CachedSession

from ffbb_api_client_v2.Multi_search_results import MultiSearchResults

from .ffbb_api_client_helper import default_cached_session


class MeilisearchProdFFBBAPPClient:
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://meilisearch-prod.ffbb.app/",
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
        self.bearer_token = bearer_token
        self.url = url
        self.debug = debug
        self.cached_session = cached_session
        self.headers = {"Authorization": f"Bearer {self.bearer_token}"}

    def multi_search(
        self, searched_name: str, cached_session: CachedSession = None
    ) -> MultiSearchResults:
        f"{self.url}multi-search"
