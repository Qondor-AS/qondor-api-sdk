"""Shared fixtures for SDK module tests."""

from __future__ import annotations

import httpx
import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture
def http_client(httpx_mock: HTTPXMock) -> httpx.AsyncClient:
    return httpx.AsyncClient(base_url="https://mock.example.com")
