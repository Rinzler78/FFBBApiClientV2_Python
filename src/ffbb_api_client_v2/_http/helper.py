"""HTTP request helper utilities for FFBB API Client."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import TypeVar

from requests import ReadTimeout

from ..exceptions import FFBBApiError, FFBBNetworkError

__all__ = ["HttpHelper", "catch_result"]

T = TypeVar("T")

logger = logging.getLogger(__name__)


class HttpHelper:
    """Helper class for HTTP request error handling and retries."""

    @staticmethod
    def catch_result(callback: Callable[[], T]) -> T | None:
        """
        Catch the result of a callback function.

        FFBBApiError subclasses are allowed to propagate (they carry structured
        error information). Network errors are wrapped into FFBBNetworkError.
        Only empty-body JSON responses (Expecting value) still return None.

        Args:
            callback: The callback function.

        Returns:
            The result of the callback function or None if the response body is empty.

        Raises:
            FFBBApiError: Any structured API error (auth, not found, rate limit, etc.).
            FFBBNetworkError: Wraps network-level failures.
        """
        try:
            return callback()
        except FFBBApiError:
            raise
        except json.decoder.JSONDecodeError as e:
            if e.msg == "Expecting value":
                return None
            raise
        except (ReadTimeout, ConnectionError) as e:
            raise FFBBNetworkError(
                message=f"Network error: {e}",
                original_exception=e,
            ) from e


# Module-level alias for backward compatibility
catch_result = HttpHelper.catch_result
