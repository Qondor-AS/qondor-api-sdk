"""Shared helpers for integration tests."""

from __future__ import annotations

import uuid


def unique_ref(prefix: str = "sdk-inttest") -> str:
    """Return a collision-free external reference."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def unique_email(prefix: str = "sdk-inttest") -> str:
    """Return a unique email address for contact-person tests."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}@test.example.com"
