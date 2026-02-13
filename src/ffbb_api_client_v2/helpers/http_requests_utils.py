from __future__ import annotations

import json
import time
from typing import Any, cast
from urllib.parse import urlencode

import requests
from requests import Response
from requests_cache import CachedSession

from ..directus_exceptions import DirectusError
from ..exceptions import (
    FFBBAuthError,
    FFBBNotFoundError,
    FFBBRateLimitError,
    FFBBServerError,
)
from ..meilisearch_exceptions import MeilisearchError
from ..utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    make_http_request_with_retry,
)
from ..utils.secure_logging import get_secure_logger

logger = get_secure_logger(__name__)


def to_json_from_response(response: Response) -> dict[str, Any]:
    """
    Converts the HTTP response to a JSON dictionary.

    Args:
        response (Response): The HTTP response.

    Returns:
        Dict[str, Any]: The JSON dictionary extracted from the response.
    """
    data_str = response.text.strip()

    try:
        return cast(dict[str, Any], json.loads(data_str))
    except json.JSONDecodeError as e:
        logger.warning(f"Error in to_json_from_response: {e}")

    if data_str.endswith(","):
        data_str = data_str[:-1]

    data_str = data_str.replace("][", ",")
    data_str = data_str.replace("KO", "")

    if data_str.startswith('""'):
        data_str = data_str[2:]

    return cast(dict[str, Any], json.loads(data_str))


def _check_response_errors(response: Response) -> None:
    """Check HTTP response for errors and raise appropriate exceptions.

    This function inspects the HTTP response status code and body to raise
    structured exceptions instead of silently returning error data.

    Args:
        response: The HTTP response to check.

    Raises:
        DirectusError: For Directus API errors (detected by 'errors' key in body).
        MeilisearchError: For Meilisearch API errors (detected by 'code'+'type' in body).
        FFBBAuthError: For 401/403 responses without recognizable error format.
        FFBBNotFoundError: For 404 responses.
        FFBBRateLimitError: For 429 responses.
        FFBBServerError: For 5xx responses.
    """
    status = response.status_code

    # 2xx is success, no error to raise
    if 200 <= status < 300:
        return

    # Try to parse the response body for structured error info
    body: dict[str, Any] | None = None
    try:
        body = response.json()
    except (json.JSONDecodeError, ValueError):
        pass

    # Detect Meilisearch error format: {"message": ..., "code": ..., "type": ..., "link": ...}
    if body and "code" in body and "type" in body:
        raise MeilisearchError.from_response(body, status_code=status)

    # Detect Directus error format: {"errors": [...]}
    if body and "errors" in body:
        raise DirectusError.from_response(body, status_code=status)

    # Generic HTTP error mapping
    message = f"HTTP {status}"
    if body and isinstance(body, dict):
        message = body.get("message", message)

    if status in (401, 403):
        raise FFBBAuthError(message=message, status_code=status, response_body=body)
    if status == 404:
        raise FFBBNotFoundError(message=message, status_code=status, response_body=body)
    if status == 429:
        retry_after_header = response.headers.get("Retry-After")
        retry_after = float(retry_after_header) if retry_after_header else None
        raise FFBBRateLimitError(
            message=message,
            status_code=status,
            response_body=body,
            retry_after=retry_after,
        )
    if status >= 500:
        raise FFBBServerError(message=message, status_code=status, response_body=body)

    # For other 4xx errors, raise a generic validation-like error
    from ..exceptions import FFBBValidationError

    raise FFBBValidationError(message=message, status_code=status, response_body=body)


def http_get(
    url: str,
    headers: dict[str, str],
    debug: bool = False,
    cached_session: CachedSession | None = None,
    timeout: int = 20,
    retry_config: RetryConfig | None = None,
    timeout_config: TimeoutConfig | None = None,
) -> Response:
    """
    Performs an HTTP GET request with retry logic.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        cached_session (CachedSession): Cached session to use. Default is None.
        timeout (int): The timeout value in seconds. Default is 20.
        retry_config (RetryConfig): Retry configuration. Default is None.
        timeout_config (TimeoutConfig): Timeout configuration. Default is None.

    Returns:
        Response: The HTTP response.
    """
    start_time: float = 0.0
    if debug:
        logger.debug(f"Making GET request to {url}")
        start_time = time.time()

    # Use retry logic if configured
    if retry_config and timeout_config:
        response = make_http_request_with_retry(
            "GET",
            url,
            headers,
            cached_session=cached_session,
            retry_config=retry_config,
            timeout_config=timeout_config,
            debug=debug,
        )
    else:
        # Fallback to original behavior
        if cached_session:
            response = cached_session.get(url, headers=headers, timeout=timeout)
        else:
            response = requests.get(url, headers=headers, timeout=timeout)

    if debug:
        end_time = time.time()
        logger.debug(f"GET request to {url} took {end_time - start_time} seconds.")
        logger.debug(f"GET response: {response.text}")

    return response


def http_post(
    url: str,
    headers: dict[str, str],
    data: dict[str, Any] | None = None,
    debug: bool = False,
    cached_session: CachedSession | None = None,
    timeout: int = 20,
    retry_config: RetryConfig | None = None,
    timeout_config: TimeoutConfig | None = None,
) -> Response:
    """
    Performs an HTTP POST request with retry logic.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        data (Dict[str, Any]): The data of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        cached_session (CachedSession): Cached session to use. Default is None.
        timeout (int): The timeout value in seconds. Default is 20.
        retry_config (RetryConfig): Retry configuration. Default is None.
        timeout_config (TimeoutConfig): Timeout configuration. Default is None.

    Returns:
        Response: The HTTP response.
    """
    start_time: float = 0.0
    data_str: str = ""
    if debug:
        data_str = ", ".join([f"{k}:{v}" for k, v in data.items()]) if data else ""
        logger.debug(f"Making POST request to {url} {data_str}")
        start_time = time.time()

    # Use retry logic if configured
    if retry_config and timeout_config:
        response = make_http_request_with_retry(
            "POST",
            url,
            headers,
            data=data,
            cached_session=cached_session,
            retry_config=retry_config,
            timeout_config=timeout_config,
            debug=debug,
        )
    else:
        # Fallback to original behavior
        if cached_session:
            response = cached_session.post(
                url, headers=headers, json=data, timeout=timeout
            )
        else:
            response = requests.post(url, headers=headers, json=data, timeout=timeout)

    if debug:
        end_time = time.time()
        logger.debug(
            f"POST request to {url} {data_str} took {end_time - start_time} seconds."
        )
        logger.debug(f"POST response: {response.text}")

    return response


def http_get_json(
    url: str,
    headers: dict[str, str],
    debug: bool = False,
    cached_session: CachedSession | None = None,
    timeout: int = 20,
    retry_config: RetryConfig | None = None,
    timeout_config: TimeoutConfig | None = None,
) -> dict[str, Any]:
    """
    Performs an HTTP GET request and returns the result in JSON format.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        cached_session (CachedSession): Cached session to use. Default is None.
        timeout (int): The timeout value in seconds. Default is 20.
        retry_config (RetryConfig): Retry configuration. Default is None.
        timeout_config (TimeoutConfig): Timeout configuration. Default is None.

    Returns:
        Dict[str, Any]: The result of the request in JSON format.
    """
    response = http_get(
        url,
        headers,
        debug=debug,
        cached_session=cached_session,
        timeout=timeout,
        retry_config=retry_config,
        timeout_config=timeout_config,
    )
    _check_response_errors(response)
    return to_json_from_response(response)


def http_post_json(
    url: str,
    headers: dict[str, str],
    data: dict[str, Any] | None = None,
    debug: bool = False,
    cached_session: CachedSession | None = None,
    timeout: int = 20,
    retry_config: RetryConfig | None = None,
    timeout_config: TimeoutConfig | None = None,
) -> dict[str, Any]:
    """
    Performs an HTTP POST request and returns the result in JSON format.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        data (Dict[str, Any]): The data of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        cached_session (CachedSession): Cached session to use. Default is None.
        timeout (int): The timeout value in seconds. Default is 20.
        retry_config (RetryConfig): Retry configuration. Default is None.
        timeout_config (TimeoutConfig): Timeout configuration. Default is None.

    Returns:
        Dict[str, Any]: The result of the request in JSON format.
    """
    filtered_data = {k: v for k, v in data.items() if v is not None} if data else None

    response = http_post(
        url,
        headers,
        filtered_data,
        debug=debug,
        cached_session=cached_session,
        timeout=timeout,
        retry_config=retry_config,
        timeout_config=timeout_config,
    )
    _check_response_errors(response)
    return to_json_from_response(response)


def encode_params(params: dict[str, Any]) -> str:
    """
    Encodes the request parameters into a query string.
    Handles array parameters correctly (fields[], etc.)

    Args:
        params (Dict[str, Any]): The request parameters.

    Returns:
        str: The encoded query string.
    """
    encoded_pairs = []
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, list):
            # Handle array parameters like fields[]
            for item in v:
                encoded_pairs.append(urlencode({k: item}))
        else:
            encoded_pairs.append(urlencode({k: v}))

    return "&".join(encoded_pairs)


def url_with_params(url: str, params: dict[str, Any]) -> str:
    """
    Adds the request parameters to the URL.

    Args:
        url (str): The URL of the request.
        params (Dict[str, Any]): The request parameters.

    Returns:
        str: The URL with the request parameters.
    """
    if encoded_params := encode_params(params):
        return f"{url}?{encoded_params}"
    else:
        return url
