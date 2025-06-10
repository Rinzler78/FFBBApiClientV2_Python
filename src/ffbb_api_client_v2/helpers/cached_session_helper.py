from requests_cache import CachedSession


def create_cache_key(request, **kwargs):
    url = request.url
    method = request.method
    data_hash = request.body or "empty"
    return f"{method} {url} {data_hash}"


default_cached_session = CachedSession(
    "http_cache",
    backend="sqlite",
    expire_after=1800,
    allowable_methods=("GET", "POST"),
    key_fn=create_cache_key,
)
