"""
Integration tests for input validation in API clients.
"""

import unittest
from unittest.mock import patch

from ffbb_api_client_v2 import FFBBAPIClientV2
from ffbb_api_client_v2.utils.input_validation import ValidationError


class Test015InputValidationIntegration(unittest.TestCase):
    """Integration tests for input validation in API clients."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_token = "valid_test_token_123456789"
        self.valid_meilisearch_token = "valid_meilisearch_token_123456789"

    def test_create_client_valid_inputs(self):
        """Test creating client with valid inputs."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ), patch("ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"):
            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=self.valid_token,
                debug=True,
            )
            self.assertIsInstance(client, FFBBAPIClientV2)

    def test_create_client_invalid_tokens(self):
        """Test creating client with invalid tokens."""
        invalid_token_cases = [
            (None, self.valid_token, "meilisearch_bearer_token cannot be None"),
            (self.valid_meilisearch_token, None, "api_bearer_token cannot be None"),
            ("", self.valid_token, "meilisearch_bearer_token cannot be empty"),
            (self.valid_meilisearch_token, "", "api_bearer_token cannot be empty"),
            ("   ", self.valid_token, "meilisearch_bearer_token cannot be empty"),
            (self.valid_meilisearch_token, "   ", "api_bearer_token cannot be empty"),
            ("short", self.valid_token, "meilisearch_bearer_token must be at least 10"),
            (
                self.valid_meilisearch_token,
                "short",
                "api_bearer_token must be at least 10",
            ),
            (
                "token<with>invalid",
                self.valid_token,
                "meilisearch_bearer_token contains invalid",
            ),
            (
                self.valid_meilisearch_token,
                "token<with>invalid",
                "api_bearer_token contains invalid",
            ),
        ]

        for meilisearch_token, api_token, expected_error in invalid_token_cases:
            with self.subTest(meilisearch=meilisearch_token, api=api_token):
                with self.assertRaises(ValidationError) as context:
                    FFBBAPIClientV2.create(
                        meilisearch_bearer_token=meilisearch_token,
                        api_bearer_token=api_token,
                    )
                self.assertIn(expected_error, str(context.exception))

    def test_create_client_invalid_debug(self):
        """Test creating client with invalid debug parameter."""
        with self.assertRaises(ValidationError) as context:
            FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=self.valid_token,
                debug="invalid",
            )
        self.assertIn("debug must be a boolean", str(context.exception))

    def test_get_saisons_valid_inputs(self):
        """Test get_saisons with valid inputs."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ) as mock_api_client_class, patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"
        ):  # noqa: F841

            mock_api_client_instance = mock_api_client_class.return_value
            mock_api_client_instance.get_saisons.return_value = []

            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=self.valid_token,
            )

            # Verify client was created successfully
            self.assertIsNotNone(client)
            self.assertIsNotNone(client.api_ffbb_client)

            # Test with valid inputs
            result = client.get_saisons(
                fields=["id", "nom"], filter_criteria='{"actif":{"_eq":true}}'
            )

            # Verify the result is what we expect
            self.assertEqual(result, [])

            # Verify the API was called
            mock_api_client_instance.get_saisons.assert_called_once()
            call_args = mock_api_client_instance.get_saisons.call_args
            self.assertEqual(call_args[1]["fields"], ["id", "nom"])
            self.assertEqual(call_args[1]["filter_criteria"], '{"actif":{"_eq":true}}')

    def test_get_saisons_invalid_inputs(self):
        """Test get_saisons with invalid inputs."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ), patch("ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"):
            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=self.valid_token,
            )

            # Test invalid fields
            with self.assertRaises(ValidationError) as context:
                client.get_saisons(fields=[""])
            self.assertIn("cannot be empty", str(context.exception))

            # Test invalid filter criteria
            with self.assertRaises(ValidationError) as context:
                client.get_saisons(filter_criteria="not-json")
            self.assertIn("must be a valid JSON object", str(context.exception))

    def test_multi_search_valid_inputs(self):
        """Test multi_search with valid inputs."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ), patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"
        ) as mock_meilisearch_class:

            mock_meilisearch_instance = mock_meilisearch_class.return_value
            mock_meilisearch_instance.recursive_smart_multi_search.return_value = None

            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=self.valid_token,
            )

            # Test with valid search query
            result = client.multi_search("valid search query")
            # Result should be either None or empty list
            self.assertTrue(result is None or result == [])

            # Verify the search was called
            mock_meilisearch_instance.recursive_smart_multi_search.assert_called_once()

    def test_multi_search_invalid_inputs(self):
        """Test multi_search with invalid inputs."""
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ), patch("ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"):
            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=self.valid_token,
            )

            # Test with query containing invalid characters
            with self.assertRaises(ValidationError) as context:
                client.multi_search("search<with>invalid")
            self.assertIn("contains invalid characters", str(context.exception))

            # Test with too long query
            long_query = "a" * 201
            with self.assertRaises(ValidationError) as context:
                client.multi_search(long_query)
            self.assertIn("is too long", str(context.exception))

    def test_token_validation_edge_cases(self):
        """Test token validation edge cases."""
        # Test token exactly at minimum length
        min_length_token = "a" * 10
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ), patch("ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"):
            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=min_length_token,
                api_bearer_token=self.valid_token,
            )
            self.assertIsInstance(client, FFBBAPIClientV2)

        # Test token exactly at maximum length
        max_length_token = "a" * 1000
        with patch(
            "ffbb_api_client_v2.clients.ffbb_api_client_v2.ApiFFBBAppClient"
        ), patch("ffbb_api_client_v2.clients.ffbb_api_client_v2.MeilisearchFFBBClient"):
            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=max_length_token,
            )
            self.assertIsInstance(client, FFBBAPIClientV2)

        # Test token over maximum length
        over_length_token = "a" * 1001
        with self.assertRaises(ValidationError) as context:
            FFBBAPIClientV2.create(
                meilisearch_bearer_token=self.valid_meilisearch_token,
                api_bearer_token=over_length_token,
            )
        self.assertIn("cannot be longer than 1000", str(context.exception))


if __name__ == "__main__":
    unittest.main()
