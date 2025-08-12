"""
conftest.py for ffbb_api_client_v2 tests.

This file is automatically executed by pytest before running tests.
It loads environment variables from .env file for all test modules.
"""

from dotenv import load_dotenv

# Load environment variables for all tests
load_dotenv()
