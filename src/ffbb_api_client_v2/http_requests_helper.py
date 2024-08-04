import json

from requests import ReadTimeout
from requests_cache import CachedSession


def catch_result(callback, is_retrieving: bool = False):
    """
    Catch the result of a callback function.

    Args:
        callback: The callback function.

    Returns:
        The result of the callback function or None if an exception occurs.
    """

    try:
        return callback()
    except json.decoder.JSONDecodeError as e:
        if e.msg == "Expecting value":
            return None
        raise e
    except ReadTimeout as e:
        if not is_retrieving:
            return catch_result(callback, True)
        raise e
    except ConnectionError as e:
        if not is_retrieving:
            return catch_result(callback, True)
        raise e
    except Exception as e:
        raise e


# Default cached session sqlite backend with 30 minutes expiration
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
