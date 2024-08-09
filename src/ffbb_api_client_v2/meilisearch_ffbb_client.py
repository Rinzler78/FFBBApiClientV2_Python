from requests_cache import CachedSession

from .http_requests_helper import default_cached_session
from .meilisearch_client_extension import MeilisearchClientExtension


class MeilisearchFFBBClient(MeilisearchClientExtension):
    def __init__(
        self,
        bearer_token: str,
        url: str = "https://meilisearch-prod.ffbb.app/",
        debug: bool = False,
        cached_session: CachedSession = default_cached_session,
    ):
        super().__init__(bearer_token, url, debug, cached_session)
