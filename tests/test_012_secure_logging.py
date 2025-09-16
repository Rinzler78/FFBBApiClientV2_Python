"""
Tests for secure logging functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

from ffbb_api_client_v2.utils.secure_logging import (
    SecureLogger,
    get_secure_logger,
    mask_token,
)


class Test012SecureLogging(unittest.TestCase):
    """Test cases for secure logging functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.logger = SecureLogger("test_logger")

    def test_mask_token_basic(self):
        """Test basic token masking functionality."""
        token = "abcdefghijklmnop"
        masked = mask_token(token, visible_chars=4)
        self.assertEqual(masked, "abcd***MASKED***")

    def test_mask_token_short(self):
        """Test masking of short tokens."""
        token = "abc"
        masked = mask_token(token, visible_chars=4)
        self.assertEqual(masked, "***MASKED***")

    def test_mask_token_empty(self):
        """Test masking of empty tokens."""
        token = ""
        masked = mask_token(token)
        self.assertEqual(masked, "***MASKED***")

    def test_mask_token_none(self):
        """Test masking of None tokens."""
        token = None
        masked = mask_token(token)
        self.assertEqual(masked, "***MASKED***")

    def test_mask_sensitive_data_bearer_token(self):
        """Test masking of Bearer tokens in messages."""
        message = "Authorization: Bearer abcdefghijklmnop"
        masked = self.logger._mask_sensitive_data(message)
        self.assertEqual(masked, "Authorization: Bearer ***MASKED***")

    def test_mask_sensitive_data_api_token(self):
        """Test masking of API tokens in various formats."""
        test_cases = [
            ('token: "abcdefghijklmnop"', 'token: "***MASKED***"'),
            ("token='abcdefghijklmnop'", "token='***MASKED***'"),
            ("password: mypassword123", 'password: "***MASKED***"'),
            ("Bearer abcdefghijklmnop", "Bearer ***MASKED***"),
        ]

        for original, expected in test_cases:
            with self.subTest(original=original):
                masked = self.logger._mask_sensitive_data(original)
                # Check that sensitive data is masked (not the exact format)
                self.assertIn("***MASKED***", masked)
                self.assertNotIn("abcdefghijklmnop", masked)
                self.assertNotIn("mypassword123", masked)

    def test_mask_sensitive_data_long_token(self):
        """Test masking of long tokens (32+ characters)."""
        long_token = "a" * 40  # 40 character token
        message = f"Authorization: Bearer {long_token}"
        masked = self.logger._mask_sensitive_data(message)
        # Check that the long token is masked
        self.assertIn("***MASKED***", masked)
        self.assertNotIn(long_token, masked)

    def test_get_secure_logger(self):
        """Test getting a secure logger instance."""
        logger = get_secure_logger("test_component")
        self.assertIsInstance(logger, SecureLogger)
        self.assertEqual(logger.logger.name, "test_component")

    @patch("ffbb_api_client_v2.utils.secure_logging.logging")
    def test_secure_logger_debug(self, mock_logging):
        """Test debug logging with sensitive data masking."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        logger = SecureLogger("test")
        logger.debug("Bearer token123 in message")

        # Verify that the message was masked before logging
        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0]
        self.assertIn("***MASKED***", call_args[0])
        self.assertNotIn("token123", call_args[0])

    @patch("ffbb_api_client_v2.utils.secure_logging.logging")
    def test_secure_logger_info(self, mock_logging):
        """Test info logging with sensitive data masking."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        logger = SecureLogger("test")
        logger.info("API call with token: abcdef123456")

        # Verify that the message was masked before logging
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0]
        self.assertIn("***MASKED***", call_args[0])
        self.assertNotIn("abcdef123456", call_args[0])

    def test_no_sensitive_data_unchanged(self):
        """Test that messages without sensitive data remain unchanged."""
        message = "This is a normal log message without sensitive data"
        masked = self.logger._mask_sensitive_data(message)
        self.assertEqual(masked, message)

    def test_case_insensitive_masking(self):
        """Test that masking is case insensitive."""
        message = "AUTHORIZATION: bearer token123"
        masked = self.logger._mask_sensitive_data(message)
        # Check that sensitive data is masked (case insensitive)
        self.assertIn("***MASKED***", masked)
        self.assertNotIn("token123", masked)


if __name__ == "__main__":
    unittest.main()
