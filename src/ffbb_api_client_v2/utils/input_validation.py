"""
Input validation utilities for FFBB API Client V2.

This module provides comprehensive validation functions for all input parameters
to ensure data integrity and prevent common errors.
"""

import re
from typing import Any, Optional, Union
from urllib.parse import urlparse


class ValidationError(ValueError):
    """Exception raised when input validation fails."""


def validate_token(token: str, field_name: str = "token") -> str:
    """
    Validate a bearer token.

    Args:
        token (str): The token to validate
        field_name (str): Name of the field for error messages

    Returns:
        str: The validated token

    Raises:
        ValidationError: If token is invalid
    """
    if token is None:
        raise ValidationError(f"{field_name} cannot be None")

    if not isinstance(token, str):
        raise ValidationError(
            f"{field_name} must be a string, got {type(token).__name__}"
        )

    token_stripped = token.strip()
    if not token_stripped:
        raise ValidationError(f"{field_name} cannot be empty or whitespace-only")

    if len(token_stripped) < 10:
        raise ValidationError(f"{field_name} must be at least 10 characters long")

    if len(token_stripped) > 1000:
        raise ValidationError(f"{field_name} cannot be longer than 1000 characters")

    # Check for potentially dangerous characters
    if re.search(r'[<>"\';&]', token_stripped):
        raise ValidationError(f"{field_name} contains invalid characters")

    return token_stripped


def validate_url(url: str, field_name: str = "url") -> str:
    """
    Validate a URL.

    Args:
        url (str): The URL to validate
        field_name (str): Name of the field for error messages

    Returns:
        str: The validated URL

    Raises:
        ValidationError: If URL is invalid
    """
    if url is None:
        raise ValidationError(f"{field_name} cannot be None")

    if not isinstance(url, str):
        raise ValidationError(
            f"{field_name} must be a string, got {type(url).__name__}"
        )

    url_stripped = url.strip()
    if not url_stripped:
        raise ValidationError(f"{field_name} cannot be empty")

    # Parse URL
    try:
        parsed = urlparse(url_stripped)
        if not parsed.scheme or not parsed.netloc:
            raise ValidationError(f"{field_name} must be a valid URL")
    except Exception as e:
        raise ValidationError(f"{field_name} is not a valid URL: {e}")

    # Check scheme
    if parsed.scheme not in ["http", "https"]:
        raise ValidationError(f"{field_name} must use HTTP or HTTPS protocol")

    return url_stripped


def validate_positive_integer(value: Union[int, str], field_name: str = "value") -> int:
    """
    Validate a positive integer.

    Args:
        value: The value to validate (int or string representation)
        field_name (str): Name of the field for error messages

    Returns:
        int: The validated integer

    Raises:
        ValidationError: If value is invalid
    """
    if value is None:
        raise ValidationError(f"{field_name} cannot be None")

    try:
        if isinstance(value, str):
            int_value = int(value.strip())
        else:
            int_value = int(value)
    except (ValueError, AttributeError) as e:
        raise ValidationError(f"{field_name} must be a valid integer: {e}")

    if int_value <= 0:
        raise ValidationError(
            f"{field_name} must be a positive integer, got {int_value}"
        )

    if int_value > 2**31 - 1:  # Max 32-bit signed integer
        raise ValidationError(f"{field_name} is too large (max: {2**31 - 1})")

    return int_value


def validate_string_list(
    values: Optional[list[str]], field_name: str = "values"
) -> Optional[list[str]]:
    """
    Validate a list of strings.

    Args:
        values: The list to validate
        field_name (str): Name of the field for error messages

    Returns:
        Optional[List[str]]: The validated list or None

    Raises:
        ValidationError: If list is invalid
    """
    if values is None:
        return None

    if not isinstance(values, list):
        raise ValidationError(
            f"{field_name} must be a list, got {type(values).__name__}"
        )

    if len(values) == 0:
        return values

    validated_values = []
    for i, value in enumerate(values):
        if value is None:
            raise ValidationError(f"{field_name}[{i}] cannot be None")

        if not isinstance(value, str):
            raise ValidationError(
                f"{field_name}[{i}] must be a string, got {type(value).__name__}"
            )

        value_stripped = value.strip()
        if not value_stripped:
            raise ValidationError(f"{field_name}[{i}] cannot be empty")

        if len(value_stripped) > 100:
            raise ValidationError(f"{field_name}[{i}] is too long (max 100 characters)")

        validated_values.append(value_stripped)

    return validated_values


def validate_boolean(value: Any, field_name: str = "value") -> bool:
    """
    Validate a boolean value.

    Args:
        value: The value to validate
        field_name (str): Name of the field for error messages

    Returns:
        bool: The validated boolean

    Raises:
        ValidationError: If value is invalid
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        lower_value = value.lower().strip()
        if lower_value in ["true", "1", "yes", "on"]:
            return True
        elif lower_value in ["false", "0", "no", "off"]:
            return False

    if isinstance(value, int):
        if value == 0:
            return False
        elif value == 1:
            return True

    raise ValidationError(
        f"{field_name} must be a boolean (True/False), got {value} ({type(value).__name__})"
    )


def validate_deep_limit(
    deep_limit: Optional[Union[str, int]], field_name: str = "deep_limit"
) -> Optional[str]:
    """
    Validate a deep limit parameter.

    Args:
        deep_limit: The deep limit to validate
        field_name (str): Name of the field for error messages

    Returns:
        Optional[str]: The validated deep limit or None

    Raises:
        ValidationError: If deep limit is invalid
    """
    if deep_limit is None:
        return None

    try:
        if isinstance(deep_limit, str):
            int_value = int(deep_limit.strip())
        else:
            int_value = int(deep_limit)
    except (ValueError, AttributeError) as e:
        raise ValidationError(f"{field_name} must be a valid integer: {e}")

    if int_value < 1:
        raise ValidationError(f"{field_name} must be at least 1, got {int_value}")

    if int_value > 10000:
        raise ValidationError(
            f"{field_name} cannot be greater than 10000, got {int_value}"
        )

    return str(int_value)


def validate_filter_criteria(
    filter_criteria: Optional[str], field_name: str = "filter_criteria"
) -> Optional[str]:
    """
    Validate filter criteria (JSON string).

    Args:
        filter_criteria: The filter criteria to validate
        field_name (str): Name of the field for error messages

    Returns:
        Optional[str]: The validated filter criteria or None

    Raises:
        ValidationError: If filter criteria is invalid
    """
    if filter_criteria is None:
        return None

    if not isinstance(filter_criteria, str):
        raise ValidationError(
            f"{field_name} must be a string, got {type(filter_criteria).__name__}"
        )

    filter_stripped = filter_criteria.strip()
    if not filter_stripped:
        return None

    if len(filter_stripped) > 1000:
        raise ValidationError(f"{field_name} is too long (max 1000 characters)")

    # Basic JSON structure validation
    if not (filter_stripped.startswith("{") and filter_stripped.endswith("}")):
        raise ValidationError(
            f"{field_name} must be a valid JSON object (start with {{ and end with }})"
        )

    return filter_stripped


def validate_search_query(
    query: Optional[str], field_name: str = "query"
) -> Optional[str]:
    """
    Validate a search query.

    Args:
        query: The search query to validate
        field_name (str): Name of the field for error messages

    Returns:
        Optional[str]: The validated query or None

    Raises:
        ValidationError: If query is invalid
    """
    if query is None:
        return None

    if not isinstance(query, str):
        raise ValidationError(
            f"{field_name} must be a string, got {type(query).__name__}"
        )

    query_stripped = query.strip()
    if not query_stripped:
        return None

    if len(query_stripped) > 200:
        raise ValidationError(f"{field_name} is too long (max 200 characters)")

    # Check for potentially dangerous characters in search queries
    if re.search(r"[<>]", query_stripped):
        raise ValidationError(f"{field_name} contains invalid characters")

    return query_stripped
