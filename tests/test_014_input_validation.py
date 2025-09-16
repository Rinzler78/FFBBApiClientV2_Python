"""
Tests for input validation functionality.
"""

import unittest

from ffbb_api_client_v2.utils.input_validation import (
    ValidationError,
    validate_boolean,
    validate_deep_limit,
    validate_filter_criteria,
    validate_positive_integer,
    validate_search_query,
    validate_string_list,
    validate_token,
    validate_url,
)


class Test014InputValidation(unittest.TestCase):
    """Test cases for input validation functions."""

    def test_validate_token_valid(self):
        """Test validation of valid tokens."""
        # Valid token
        result = validate_token("valid_token_123456789")
        self.assertEqual(result, "valid_token_123456789")

        # Token with whitespace (should be stripped)
        result = validate_token("  token_with_spaces  ")
        self.assertEqual(result, "token_with_spaces")

    def test_validate_token_invalid(self):
        """Test validation of invalid tokens."""
        # None token
        with self.assertRaises(ValidationError) as context:
            validate_token(None)
        self.assertIn("cannot be None", str(context.exception))

        # Empty token
        with self.assertRaises(ValidationError) as context:
            validate_token("")
        self.assertIn("cannot be empty", str(context.exception))

        # Whitespace-only token
        with self.assertRaises(ValidationError) as context:
            validate_token("   ")
        self.assertIn("cannot be empty", str(context.exception))

        # Token too short
        with self.assertRaises(ValidationError) as context:
            validate_token("short")
        self.assertIn("must be at least 10 characters", str(context.exception))

        # Token too long
        long_token = "a" * 1001
        with self.assertRaises(ValidationError) as context:
            validate_token(long_token)
        self.assertIn("cannot be longer than 1000", str(context.exception))

        # Token with invalid characters
        with self.assertRaises(ValidationError) as context:
            validate_token("token<with>invalid&chars")
        self.assertIn("contains invalid characters", str(context.exception))

        # Non-string token
        with self.assertRaises(ValidationError) as context:
            validate_token(123)
        self.assertIn("must be a string", str(context.exception))

    def test_validate_url_valid(self):
        """Test validation of valid URLs."""
        valid_urls = [
            "https://api.example.com",
            "http://localhost:8080",
            "https://api.ffbb.app/items/test",
        ]

        for url in valid_urls:
            with self.subTest(url=url):
                result = validate_url(url)
                self.assertEqual(result, url)

    def test_validate_url_invalid(self):
        """Test validation of invalid URLs."""
        # Test None input
        with self.assertRaises(ValidationError) as context:
            validate_url(None)
        self.assertIn("cannot be None", str(context.exception))

        # Test empty input
        with self.assertRaises(ValidationError) as context:
            validate_url("")
        self.assertIn("cannot be empty", str(context.exception))

        # Test invalid URL
        with self.assertRaises(ValidationError) as context:
            validate_url("not-a-url")
        self.assertIn("is not a valid URL", str(context.exception))

        # Test wrong protocol
        with self.assertRaises(ValidationError) as context:
            validate_url("ftp://example.com")
        self.assertIn("must use HTTP or HTTPS", str(context.exception))

        # Test non-string input
        with self.assertRaises(ValidationError) as context:
            validate_url(123)
        self.assertIn("must be a string", str(context.exception))

    def test_validate_positive_integer_valid(self):
        """Test validation of valid positive integers."""
        valid_cases = [
            (1, 1),
            ("42", 42),
            (1000, 1000),
            ("  123  ", 123),  # With whitespace
        ]

        for input_value, expected in valid_cases:
            with self.subTest(input=input_value):
                result = validate_positive_integer(input_value)
                self.assertEqual(result, expected)

    def test_validate_positive_integer_invalid(self):
        """Test validation of invalid positive integers."""
        invalid_cases = [
            (None, "cannot be None"),
            (0, "must be a positive integer"),
            (-1, "must be a positive integer"),
            ("not-a-number", "must be a valid integer"),
            ("", "must be a valid integer"),
            (2**31, "is too large"),
        ]

        for invalid_value, expected_error in invalid_cases:
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValidationError) as context:
                    validate_positive_integer(invalid_value)
                self.assertIn(expected_error, str(context.exception))

    def test_validate_string_list_valid(self):
        """Test validation of valid string lists."""
        # Valid list
        result = validate_string_list(["field1", "field2", "field3"])
        self.assertEqual(result, ["field1", "field2", "field3"])

        # List with whitespace (should be stripped)
        result = validate_string_list(["  field1  ", " field2 "])
        self.assertEqual(result, ["field1", "field2"])

        # None input
        result = validate_string_list(None)
        self.assertIsNone(result)

        # Empty list
        result = validate_string_list([])
        self.assertEqual(result, [])

    def test_validate_string_list_invalid(self):
        """Test validation of invalid string lists."""
        # Non-list input
        with self.assertRaises(ValidationError) as context:
            validate_string_list("not-a-list")
        self.assertIn("must be a list", str(context.exception))

        # List with None element
        with self.assertRaises(ValidationError) as context:
            validate_string_list(["field1", None, "field3"])
        self.assertIn("cannot be None", str(context.exception))

        # List with non-string element
        with self.assertRaises(ValidationError) as context:
            validate_string_list(["field1", 123, "field3"])
        self.assertIn("must be a string", str(context.exception))

        # List with empty string
        with self.assertRaises(ValidationError) as context:
            validate_string_list(["field1", "", "field3"])
        self.assertIn("cannot be empty", str(context.exception))

        # List with too long string
        long_string = "a" * 101
        with self.assertRaises(ValidationError) as context:
            validate_string_list([long_string])
        self.assertIn("is too long", str(context.exception))

    def test_validate_boolean_valid(self):
        """Test validation of valid boolean values."""
        valid_cases = [
            (True, True),
            (False, False),
            ("true", True),
            ("false", False),
            ("True", True),
            ("False", False),
            ("1", True),
            ("0", False),
            ("yes", True),
            ("no", False),
            (1, True),
            (0, False),
        ]

        for input_value, expected in valid_cases:
            with self.subTest(input=input_value):
                result = validate_boolean(input_value)
                self.assertEqual(result, expected)

    def test_validate_boolean_invalid(self):
        """Test validation of invalid boolean values."""
        invalid_values = ["maybe", "invalid", 2, -1, None, {}]

        for invalid_value in invalid_values:
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValidationError) as context:
                    validate_boolean(invalid_value)
                self.assertIn("must be a boolean", str(context.exception))

    def test_validate_deep_limit_valid(self):
        """Test validation of valid deep limits."""
        valid_cases = [
            (None, None),
            (1, "1"),
            ("100", "100"),
            (1000, "1000"),
            ("  500  ", "500"),  # With whitespace
        ]

        for input_value, expected in valid_cases:
            with self.subTest(input=input_value):
                result = validate_deep_limit(input_value)
                self.assertEqual(result, expected)

    def test_validate_deep_limit_invalid(self):
        """Test validation of invalid deep limits."""
        invalid_cases = [
            (0, "must be at least 1"),
            (-1, "must be at least 1"),
            (10001, "cannot be greater than 10000"),
            ("not-a-number", "must be a valid integer"),
            ("", "must be a valid integer"),
        ]

        for invalid_value, expected_error in invalid_cases:
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValidationError) as context:
                    validate_deep_limit(invalid_value)
                self.assertIn(expected_error, str(context.exception))

    def test_validate_filter_criteria_valid(self):
        """Test validation of valid filter criteria."""
        valid_cases = [
            (None, None),
            ('{"actif":{"_eq":true}}', '{"actif":{"_eq":true}}'),
            ('  {"test": "value"}  ', '{"test": "value"}'),  # With whitespace
        ]

        for input_value, expected in valid_cases:
            with self.subTest(input=input_value):
                result = validate_filter_criteria(input_value)
                self.assertEqual(result, expected)

    def test_validate_filter_criteria_invalid(self):
        """Test validation of invalid filter criteria."""
        invalid_cases = [
            ("not-json-object", "must be a valid JSON object"),
            ('["not", "object"]', "must be a valid JSON object"),
            ("not-json", "must be a valid JSON object"),
            (123, "must be a string"),
            ("a" * 1001, "is too long"),
        ]

        for invalid_value, expected_error in invalid_cases:
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValidationError) as context:
                    validate_filter_criteria(invalid_value)
                self.assertIn(expected_error, str(context.exception))

    def test_validate_search_query_valid(self):
        """Test validation of valid search queries."""
        valid_cases = [
            (None, None),
            ("valid search", "valid search"),
            ("  search with spaces  ", "search with spaces"),  # With whitespace
            ("café", "café"),  # Unicode characters
        ]

        for input_value, expected in valid_cases:
            with self.subTest(input=input_value):
                result = validate_search_query(input_value)
                self.assertEqual(result, expected)

    def test_validate_search_query_invalid(self):
        """Test validation of invalid search queries."""
        # Test non-string input
        with self.assertRaises(ValidationError) as context:
            validate_search_query(123)
        self.assertIn("must be a string", str(context.exception))

        # Test too long query
        with self.assertRaises(ValidationError) as context:
            validate_search_query("a" * 201)
        self.assertIn("is too long", str(context.exception))

        # Test query with invalid characters
        with self.assertRaises(ValidationError) as context:
            validate_search_query("search<with>tags")
        self.assertIn("contains invalid characters", str(context.exception))


if __name__ == "__main__":
    unittest.main()
