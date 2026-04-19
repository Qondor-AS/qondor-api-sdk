"""Integration tests for office operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.customer import CustomerCategory
from qondor_api_sdk.models.office import OfficeSummary

from .conftest import EnvConfig

pytestmark = pytest.mark.integration


class TestOffice:
    """Office read-only operations."""

    async def test_list(self, qondor_client: QondorClient):
        results = await qondor_client.office.get_all()
        assert isinstance(results, list)
        assert len(results) > 0
        assert isinstance(results[0], OfficeSummary)

    async def test_categories(self, env_config: EnvConfig, qondor_client: QondorClient):
        results = await qondor_client.office.get_all_customer_categories(
            office_id=env_config.office_id,
        )
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], CustomerCategory)
