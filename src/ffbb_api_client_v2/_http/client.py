"""HTTP client utilities for FFBB API Client."""

from __future__ import annotations

import json
import time
from typing import Any, cast
from urllib.parse import urlencode

import requests
from requests import Response
from requests_cache import CachedSession

from ..exceptions import (
    FFBBAuthError,
    FFBBNotFoundError,
    FFBBRateLimitError,
    FFBBServerError,
    FFBBValidationError,
)
from ..utils.retry_utils import (
    RetryConfig,
    TimeoutConfig,
    make_http_request_with_retry,
)
from ..utils.secure_logging import get_secure_logger

logger = get_secure_logger(__name__)


class HttpClient:
    """HTTP client with error checking, retry logic, and URL encoding."""

    @staticmethod
    def to_json_from_response(response: Response) -> dict[str, Any]:
        """
        Converts the HTTP response to a JSON dictionary.

        Args:
            response: The HTTP response.

        Returns:
            The JSON dictionary extracted from the response.
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

    @staticmethod
    def check_response_errors(response: Response) -> None:
        """Check HTTP response for errors and raise appropriate exceptions.

        Raises only generic FFBB exceptions with the response_body attached.
        Callers that need Directus- or Meilisearch-specific exceptions should
        catch these and re-raise as appropriate.

        Args:
            response: The HTTP response to check.

        Raises:
            FFBBAuthError: For 401/403 responses.
            FFBBNotFoundError: For 404 responses.
            FFBBRateLimitError: For 429 responses.
            FFBBServerError: For 5xx responses.
            FFBBValidationError: For other 4xx responses.
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

        # Extract message from known error formats
        message = f"HTTP {status}"
        if body and isinstance(body, dict):
            # Meilisearch format: {"message": ..., "code": ..., "type": ...}
            if "message" in body:
                message = body["message"]
            # Directus format: {"errors": [{"message": "..."}]}
            elif "errors" in body and isinstance(body.get("errors"), list):
                errors = body["errors"]
                if errors:
                    message = errors[0].get("message", message)

        if status in (401, 403):
            raise FFBBAuthError(message=message, status_code=status, response_body=body)
        if status == 404:
            raise FFBBNotFoundError(
                message=message, status_code=status, response_body=body
            )
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
            raise FFBBServerError(
                message=message, status_code=status, response_body=body
            )

        # For other 4xx errors
        raise FFBBValidationError(
            message=message, status_code=status, response_body=body
        )

    @staticmethod
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
            url: The URL of the request.
            headers: The headers of the request.
            debug: Whether to enable debug mode. Default is False.
            cached_session: Cached session to use. Default is None.
            timeout: The timeout value in seconds. Default is 20.
            retry_config: Retry configuration. Default is None.
            timeout_config: Timeout configuration. Default is None.

        Returns:
            The HTTP response.
        """
        start_time: float = 0.0
        if debug:
            logger.debug(f"Making GET request to {url}")
            start_time = time.time()

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
            if cached_session:
                response = cached_session.get(url, headers=headers, timeout=timeout)
            else:
                response = requests.get(url, headers=headers, timeout=timeout)

        if debug:
            end_time = time.time()
            logger.debug(f"GET request to {url} took {end_time - start_time} seconds.")
            logger.debug(f"GET response: {response.text}")

        return response

    @staticmethod
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
            url: The URL of the request.
            headers: The headers of the request.
            data: The data of the request.
            debug: Whether to enable debug mode. Default is False.
            cached_session: Cached session to use. Default is None.
            timeout: The timeout value in seconds. Default is 20.
            retry_config: Retry configuration. Default is None.
            timeout_config: Timeout configuration. Default is None.

        Returns:
            The HTTP response.
        """
        start_time: float = 0.0
        data_str: str = ""
        if debug:
            data_str = ", ".join([f"{k}:{v}" for k, v in data.items()]) if data else ""
            logger.debug(f"Making POST request to {url} {data_str}")
            start_time = time.time()

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
            if cached_session:
                response = cached_session.post(
                    url, headers=headers, json=data, timeout=timeout
                )
            else:
                response = requests.post(
                    url, headers=headers, json=data, timeout=timeout
                )

        if debug:
            end_time = time.time()
            logger.debug(
                f"POST request to {url} {data_str} "
                f"took {end_time - start_time} seconds."
            )
            logger.debug(f"POST response: {response.text}")

        return response

    @staticmethod
    def http_get_json(
        url: str,
        headers: dict[str, str],
        debug: bool = False,
        cached_session: CachedSession | None = None,
        timeout: int = 20,
        retry_config: RetryConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
    ) -> dict[str, Any]:
        """Performs an HTTP GET request and returns JSON."""
        response = HttpClient.http_get(
            url,
            headers,
            debug=debug,
            cached_session=cached_session,
            timeout=timeout,
            retry_config=retry_config,
            timeout_config=timeout_config,
        )
        HttpClient.check_response_errors(response)
        return HttpClient.to_json_from_response(response)

    @staticmethod
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
        """Performs an HTTP POST request and returns JSON."""
        filtered_data = (
            {k: v for k, v in data.items() if v is not None} if data else None
        )

        response = HttpClient.http_post(
            url,
            headers,
            filtered_data,
            debug=debug,
            cached_session=cached_session,
            timeout=timeout,
            retry_config=retry_config,
            timeout_config=timeout_config,
        )
        HttpClient.check_response_errors(response)
        return HttpClient.to_json_from_response(response)

    @staticmethod
    def encode_params(params: dict[str, Any]) -> str:
        """Encodes request parameters into a query string."""
        encoded_pairs = []
        for k, v in params.items():
            if v is None:
                continue
            if isinstance(v, list):
                for item in v:
                    encoded_pairs.append(urlencode({k: item}))
            else:
                encoded_pairs.append(urlencode({k: v}))

        return "&".join(encoded_pairs)

    @staticmethod
    def url_with_params(url: str, params: dict[str, Any]) -> str:
        """Adds request parameters to the URL."""
        if encoded_params := HttpClient.encode_params(params):
            return f"{url}?{encoded_params}"
        return url


# Module-level aliases for backward compatibility
to_json_from_response = HttpClient.to_json_from_response
_check_response_errors = HttpClient.check_response_errors
http_get = HttpClient.http_get
http_post = HttpClient.http_post
http_get_json = HttpClient.http_get_json
http_post_json = HttpClient.http_post_json
encode_params = HttpClient.encode_params
url_with_params = HttpClient.url_with_params
