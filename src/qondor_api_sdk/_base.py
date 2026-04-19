"""Base model with camelCase alias generation for Qondor API serialization."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


def to_camel(s: str) -> str:
    """Convert snake_case to camelCase."""
    parts = s.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class ApiModel(BaseModel):
    """Base model for all Qondor API contracts.

    Uses camelCase aliases for JSON serialization (API expects camelCase)
    and populate_by_name=True for snake_case Python usage.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
