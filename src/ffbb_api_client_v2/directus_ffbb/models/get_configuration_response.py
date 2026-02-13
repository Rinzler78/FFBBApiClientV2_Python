"""Configuration models for FFBB API."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GetConfigurationResponse:
    """Response model for /items/configuration endpoint."""

    id: int
    key_dh: str
    key_ms: str
    key_directus_website: str | None = None
    key_directus_competitions: str | None = None
    ios_version: str | None = None
    android_version: str | None = None
    date_created: str | None = None
    date_updated: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> GetConfigurationResponse:
        """Create a GetConfigurationResponse from a dictionary."""
        return cls(
            id=data.get("id", 0),
            key_dh=data.get("key_dh", ""),
            key_ms=data.get("key_ms", ""),
            key_directus_website=data.get("key_directus_website"),
            key_directus_competitions=data.get("key_directus_competitions"),
            ios_version=data.get("ios_version"),
            android_version=data.get("android_version"),
            date_created=data.get("date_created"),
            date_updated=data.get("date_updated"),
        )

    @property
    def api_bearer_token(self) -> str:
        """Alias for key_dh - the API bearer token."""
        return self.key_dh

    @property
    def meilisearch_token(self) -> str:
        """Alias for key_ms - the Meilisearch token."""
        return self.key_ms
