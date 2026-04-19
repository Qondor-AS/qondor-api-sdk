"""Tests for OfficeModule and StatisticsModule."""

from __future__ import annotations

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.customer import CustomerCategory
from qondor_api_sdk.models.office import OfficeSummary
from qondor_api_sdk.models.statistics import OfferSalesStatistics
from qondor_api_sdk.modules.office import OfficeModule
from qondor_api_sdk.modules.statistics import StatisticsModule


class TestOfficeModule:
    async def test_get_all(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Office/v1/Office/GetAll",
            json=[{"id": 1, "name": "Oslo Office", "city": "Oslo"}],
        )
        module = OfficeModule(http_client, "/Office/v1")
        result = await module.get_all()
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OfficeSummary)
        assert result[0].name == "Oslo Office"

    async def test_get_all_customer_categories(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Office/v1/Office/GetAllCustomerCategories",
                params={"officeId": "1"},
            ),
            json=[{"id": 10, "name": "VIP"}],
        )
        module = OfficeModule(http_client, "/Office/v1")
        result = await module.get_all_customer_categories(office_id=1)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CustomerCategory)
        assert result[0].name == "VIP"


class TestStatisticsModule:
    async def test_get_offer_sales(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Statistics/v1/Statistics/GetOfferSales",
                params={"officeId": "1", "projectId": "42"},
            ),
            json=[{"priceId": 100, "officeId": 1, "projectId": 42, "projectName": "Event"}],
        )
        module = StatisticsModule(http_client, "/Statistics/v1")
        result = await module.get_offer_sales(office_id=1, project_id=42)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OfferSalesStatistics)
        assert result[0].project_id == 42
