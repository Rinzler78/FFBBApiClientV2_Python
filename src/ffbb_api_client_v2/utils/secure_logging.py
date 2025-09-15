"""
Secure logging utilities for FFBB API Client V2.

This module provides logging utilities that automatically mask sensitive information
like API tokens and authentication credentials.
"""

import logging
import re
from typing import Any, Optional


class SecureLogger:
    """
    A logger that automatically masks sensitive information in log messages.

    This class provides methods to log messages while ensuring that sensitive
    information like API tokens, passwords, and authentication credentials
    are masked or redacted.
    """

    # Patterns for sensitive information that should be masked
    SENSITIVE_PATTERNS = [
        # Bearer tokens (case insensitive)
        (r"Bearer\s+[A-Za-z0-9\-_\.]+", "Bearer ***MASKED***"),
        # Authorization headers (case insensitive)
        (
            r"Authorization:\s*Bearer\s+[A-Za-z0-9\-_\.]+",
            "Authorization: Bearer ***MASKED***",
        ),
        # API tokens in various formats
        (
            r'token["\']?\s*[:=]\s*["\']?[A-Za-z0-9\-_\.]+["\']?',
            'token: "***MASKED***"',
        ),
        # Passwords
        (r'password["\']?\s*[:=]\s*["\']?.+?["\']?', 'password: "***MASKED***"'),
        # Generic token patterns (32+ chars)
        (r"\b[A-Za-z0-9]{32,}\b", "***MASKED_TOKEN***"),
    ]

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initialize the secure logger.

        Args:
            name (str): Logger name
            level (int): Logging level (default: INFO)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Add handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _mask_sensitive_data(self, message: str) -> str:
        """
        Mask sensitive information in a log message.

        Args:
            message (str): The original log message

        Returns:
            str: The message with sensitive data masked
        """
        if not isinstance(message, str):
            return str(message)

        masked_message = message
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            masked_message = re.sub(
                pattern, replacement, masked_message, flags=re.IGNORECASE
            )

        return masked_message

    def debug(self, message: str, *args, **kwargs):
        """Log a debug message with sensitive data masked."""
        masked_message = self._mask_sensitive_data(message)
        self.logger.debug(masked_message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log an info message with sensitive data masked."""
        masked_message = self._mask_sensitive_data(message)
        self.logger.info(masked_message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log a warning message with sensitive data masked."""
        masked_message = self._mask_sensitive_data(message)
        self.logger.warning(masked_message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log an error message with sensitive data masked."""
        masked_message = self._mask_sensitive_data(message)
        self.logger.error(masked_message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log a critical message with sensitive data masked."""
        masked_message = self._mask_sensitive_data(message)
        self.logger.critical(masked_message, *args, **kwargs)

    def log(self, level: int, message: str, *args, **kwargs):
        """Log a message at the specified level with sensitive data masked."""
        masked_message = self._mask_sensitive_data(message)
        self.logger.log(level, masked_message, *args, **kwargs)


# Global secure logger instance
secure_logger = SecureLogger("ffbb_api_client_v2")


def get_secure_logger(name: str) -> SecureLogger:
    """
    Get a secure logger instance for the specified name.

    Args:
        name (str): Logger name

    Returns:
        SecureLogger: A secure logger instance
    """
    return SecureLogger(name)


def mask_token(token: str, visible_chars: int = 4) -> str:
    """
    Mask a token, showing only the first few characters.

    Args:
        token (str): The token to mask
        visible_chars (int): Number of characters to show at the beginning

    Returns:
        str: The masked token

    Example:
        >>> mask_token("abcdefghijklmnop", 4)
        'abcd***MASKED***'
    """
    if not token or len(token) <= visible_chars:
        return "***MASKED***"

    visible_part = token[:visible_chars]
    return f"{visible_part}***MASKED***"


def log_api_call(
    logger: SecureLogger,
    method: str,
    url: str,
    headers: Optional[dict[str, Any]] = None,
):
    """
    Log an API call with sensitive data masked.

    Args:
        logger (SecureLogger): The logger to use
        method (str): HTTP method
        url (str): Request URL
        headers (dict, optional): Request headers
    """
    if headers:
        headers_str = ", ".join(f"{k}: {v}" for k, v in headers.items())
        logger.debug(f"API Call: {method} {url} - Headers: {headers_str}")
    else:
        logger.debug(f"API Call: {method} {url}")
