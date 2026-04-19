"""Integration tests for statistics operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.project import ProjectDetails
from qondor_api_sdk.models.statistics import OfferSalesStatistics

from .conftest import EnvConfig

pytestmark = pytest.mark.integration


class TestStatistics:
    """Statistics read-only operations."""

    async def test_offer_sales(
        self,
        env_config: EnvConfig,
        created_project: ProjectDetails,
        qondor_client: QondorClient,
    ):
        results = await qondor_client.statistics.get_offer_sales(
            office_id=env_config.office_id,
            project_id=created_project.id,
        )
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], OfferSalesStatistics)
