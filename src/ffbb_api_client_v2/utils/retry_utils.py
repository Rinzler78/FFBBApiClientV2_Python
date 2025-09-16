"""
Retry utilities for FFBB API Client V2.

This module provides retry logic with exponential backoff for HTTP requests,
along with configurable timeout management.
"""

import random
import time
from typing import Any, Callable, Optional

import requests
from requests import Response
from requests_cache import CachedSession


class RetryConfig:
    """
    Configuration for retry behavior.

    Attributes:
        max_attempts (int): Maximum number of retry attempts
        base_delay (float): Base delay in seconds between retries
        max_delay (float): Maximum delay between retries
        backoff_factor (float): Exponential backoff multiplier
        jitter (bool): Whether to add random jitter to delays
        retry_on_status_codes (list[int]): HTTP status codes to retry on
        retry_on_exceptions (tuple[Type[Exception]]): Exception types to retry on
    """

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
        retry_on_status_codes: Optional[list[int]] = None,
        retry_on_exceptions: Optional[tuple[type[Exception], ...]] = None,
    ):
        """
        Initialize retry configuration.

        Args:
            max_attempts: Maximum number of retry attempts
            base_delay: Base delay in seconds between retries
            max_delay: Maximum delay between retries
            backoff_factor: Exponential backoff multiplier
            jitter: Whether to add random jitter to delays
            retry_on_status_codes: HTTP status codes to retry on
            retry_on_exceptions: Exception types to retry on
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.retry_on_status_codes = retry_on_status_codes or [429, 500, 502, 503, 504]
        self.retry_on_exceptions = retry_on_exceptions or (
            Exception,
            ConnectionError,
            TimeoutError,
        )


class TimeoutConfig:
    """
    Configuration for timeout behavior.

    Attributes:
        connect_timeout (float): Connection timeout in seconds
        read_timeout (float): Read timeout in seconds
        total_timeout (float): Total request timeout in seconds
    """

    def __init__(
        self,
        connect_timeout: float = 10.0,
        read_timeout: float = 30.0,
        total_timeout: Optional[float] = None,
    ):
        """
        Initialize timeout configuration.

        Args:
            connect_timeout: Connection timeout in seconds
            read_timeout: Read timeout in seconds
            total_timeout: Total request timeout in seconds (overrides connect+read if set)
        """
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.total_timeout = total_timeout or (connect_timeout + read_timeout)


# Default configurations
DEFAULT_RETRY_CONFIG = RetryConfig()
DEFAULT_TIMEOUT_CONFIG = TimeoutConfig()


def calculate_delay(attempt: int, config: RetryConfig) -> float:
    """
    Calculate delay for the given retry attempt.

    Args:
        attempt: Current attempt number (0-based)
        config: Retry configuration

    Returns:
        float: Delay in seconds
    """
    delay = config.base_delay * (config.backoff_factor**attempt)
    delay = min(delay, config.max_delay)

    if config.jitter:
        # Add random jitter (±25% of delay)
        jitter_range = delay * 0.25
        delay += random.uniform(-jitter_range, jitter_range)
        delay = max(0.1, delay)  # Minimum 100ms delay

    return delay


def should_retry(
    attempt: int,
    response: Optional[Response],
    exception: Optional[Exception],
    config: RetryConfig,
) -> bool:
    """
    Determine if a request should be retried.

    Args:
        attempt: Current attempt number (0-based)
        response: HTTP response (if any)
        exception: Exception that occurred (if any)
        config: Retry configuration

    Returns:
        bool: True if request should be retried
    """
    # Retry on exceptions
    if exception and isinstance(exception, config.retry_on_exceptions):
        return True

    # Retry on specific status codes
    if (
        response
        and hasattr(response, "status_code")
        and response.status_code in config.retry_on_status_codes
    ):
        return True

    return False


def execute_with_retry(
    func: Callable[..., Response],
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
    timeout_config: TimeoutConfig = DEFAULT_TIMEOUT_CONFIG,
    *args,
    **kwargs,
) -> Response:
    """
    Execute a function with retry logic.

    Args:
        func: Function to execute (should return a Response object)
        config: Retry configuration
        timeout_config: Timeout configuration
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Response: The HTTP response

    Raises:
        Exception: The last exception if all retries are exhausted
    """
    last_exception = None

    # Update timeout in kwargs if not already set
    if "timeout" not in kwargs:
        kwargs["timeout"] = timeout_config.total_timeout

    for attempt in range(config.max_attempts + 1):
        try:
            response = func(*args, **kwargs)

            # Check if we should retry based on response
            if should_retry(attempt, response, None, config):
                if attempt < config.max_attempts:
                    delay = calculate_delay(attempt, config)
                    time.sleep(delay)
                    continue

            return response

        except Exception as e:
            last_exception = e

            # Check if we should retry based on exception
            if should_retry(attempt, None, e, config):
                if attempt < config.max_attempts:
                    delay = calculate_delay(attempt, config)
                    time.sleep(delay)
                    continue
            else:
                # Don't retry this type of exception
                raise

    # All retries exhausted
    if last_exception:
        raise last_exception

    # This should never happen, but just in case
    raise RuntimeError("Retry logic failed unexpectedly")


def make_http_request_with_retry(
    method: str,
    url: str,
    headers: dict[str, str],
    data: Optional[dict[str, Any]] = None,
    cached_session: Optional[CachedSession] = None,
    retry_config: RetryConfig = DEFAULT_RETRY_CONFIG,
    timeout_config: TimeoutConfig = DEFAULT_TIMEOUT_CONFIG,
    debug: bool = False,
) -> Response:
    """
    Make an HTTP request with retry logic.

    Args:
        method: HTTP method ('GET', 'POST', etc.)
        url: Request URL
        headers: Request headers
        data: Request data (for POST requests)
        cached_session: Cached session to use
        retry_config: Retry configuration
        timeout_config: Timeout configuration
        debug: Whether to enable debug logging

    Returns:
        Response: HTTP response
    """

    def _make_request(**unused_kwargs) -> Response:
        if debug:
            print(f"Making {method} request to {url}")

        if cached_session:
            session = cached_session
        else:
            session = requests.Session()

        if method.upper() == "GET":
            return session.get(
                url, headers=headers, timeout=timeout_config.total_timeout
            )
        elif method.upper() == "POST":
            return session.post(
                url, headers=headers, json=data, timeout=timeout_config.total_timeout
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    return execute_with_retry(
        _make_request, config=retry_config, timeout_config=timeout_config
    )


# Convenience functions for backward compatibility
def get_default_retry_config() -> RetryConfig:
    """Get default retry configuration."""
    return DEFAULT_RETRY_CONFIG


def get_default_timeout_config() -> TimeoutConfig:
    """Get default timeout configuration."""
    return DEFAULT_TIMEOUT_CONFIG


def create_custom_retry_config(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
) -> RetryConfig:
    """
    Create a custom retry configuration.

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds

    Returns:
        RetryConfig: Custom retry configuration
    """
    return RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
    )


def create_custom_timeout_config(
    connect_timeout: float = 10.0,
    read_timeout: float = 30.0,
) -> TimeoutConfig:
    """
    Create a custom timeout configuration.

    Args:
        connect_timeout: Connection timeout in seconds
        read_timeout: Read timeout in seconds

    Returns:
        TimeoutConfig: Custom timeout configuration
    """
    return TimeoutConfig(
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
    )
