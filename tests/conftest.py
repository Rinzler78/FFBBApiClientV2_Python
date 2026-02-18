"""
Pytest configuration with parallel execution support.

This file is automatically executed by pytest before running tests.
It loads environment variables from .env file and configures cache
isolation for parallel test execution with pytest-xdist.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING, Any

import pytest
from dotenv import load_dotenv

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest

# Load environment variables for all tests
load_dotenv()


@pytest.fixture(scope="session")
def worker_id(request: FixtureRequest) -> str:
    """Get xdist worker ID or 'master'.

    Args:
        request: Pytest fixture request.

    Returns:
        Worker ID string ('gw0', 'gw1', etc.) or 'master' for non-parallel runs.
    """
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]  # type: ignore[no-any-return]
    return "master"


@pytest.fixture(scope="session", autouse=True)
def configure_cache_for_worker(
    worker_id: str,
) -> Generator[None]:
    """Configure CacheManager with memory backend for test isolation.

    Each pytest-xdist worker runs in its own process, so using the memory
    backend ensures complete cache isolation without file collisions.

    Args:
        worker_id: The xdist worker ID (used to establish fixture dependency).

    Yields:
        None - fixture runs setup, yields control, then runs teardown.
    """
    _ = worker_id  # Used by pytest for fixture dependency ordering
    from ffbb_api_client_v2.utils.cache_manager import CacheConfig, CacheManager

    CacheManager.reset_instance()

    # Use memory backend for tests - each worker has its own Python process
    # so its own memory space, no collision possible
    config = CacheConfig(
        enabled=True,
        backend="memory",  # Memory cache isolated per worker process
        expire_after=1800,
        max_size=1000,
    )
    CacheManager(config)

    yield

    CacheManager.reset_instance()


@pytest.fixture
def isolated_env() -> Generator[dict[str, str]]:
    """Fixture providing isolated environment variables.

    Saves the current environment, yields it for modification,
    then restores the original environment on teardown.

    Yields:
        The current environment dictionary for modification.
    """
    original = os.environ.copy()
    yield dict(os.environ)
    os.environ.clear()
    os.environ.update(original)


# --- Fixture loading helpers ---

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def load_fixture(name: str) -> Any:
    """Load a JSON fixture file from tests/fixtures/.

    Args:
        name: Fixture filename without .json extension.

    Returns:
        Parsed JSON data (dict or list).

    Raises:
        FileNotFoundError: If the fixture file does not exist.
    """
    filepath = os.path.join(FIXTURES_DIR, f"{name}.json")
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fixture_loader() -> Callable[[str], Any]:
    """Pytest fixture providing the load_fixture helper.

    Returns:
        A callable that loads a named JSON fixture.
    """
    return load_fixture
