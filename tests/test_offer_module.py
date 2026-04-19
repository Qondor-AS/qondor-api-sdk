"""Tests for OfferModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
import pytest
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.offer import (
    AddCurrencyToOffer,
    CreateOffer,
    OfferCurrencyDetails,
    OfferDetails,
    OfferSummary,
    UpdateOffer,
    UpdateOfferCurrency,
)
from qondor_api_sdk.modules.offer import OfferModule

OFFER_JSON = {
    "id": 789,
    "heading": "Test Offer",
    "status": 1,
    "projectId": 42,
    "defaultMargin": 15.0,
    "displayPricesExclVat": True,
    "displayPricesInclVat": False,
    "displayTotalOfferPrice": False,
    "displayTotalPriceColumn": False,
    "displayTotalPriceInclVat": False,
    "displayVatAmount": False,
    "hideVatTextFromPrices": False,
    "includeOfficeTermsAndConditions": False,
    "disableUnsureAnswerOnProductsAndGroups": False,
    "isPublished": False,
    "isMainOffer": False,
    "accommodationOfferPriceType": 1,
    "lastEditedDate": "2026-04-01T00:00:00Z",
    "lastEditedDateUtc": "2026-04-01T00:00:00Z",
    "offerLocation": {"displayText": "Oslo", "location": None},
}


class TestOfferModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url="https://mock.example.com/Offer/v1/Offer/789", json=OFFER_JSON)
        module = OfferModule(http_client, "/Offer/v1")
        result = await module.get(789)
        assert isinstance(result, OfferDetails)
        assert result.id == 789
        assert result.heading == "Test Offer"

    async def test_get_all_for_project(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL("https://mock.example.com/Offer/v1/Offer/GetAllForProject", params={"projectId": "42"}),
            json=[
                {
                    **OFFER_JSON,
                    "id": 1,
                    "heading": "Option A",
                    "defaultMargin": 10.0,
                    "isMainOffer": True,
                    "offerLocation": None,
                }
            ],
        )
        module = OfferModule(http_client, "/Offer/v1")
        result = await module.get_all_for_project(project_id=42)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OfferSummary)

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer",
            method="POST",
            json={**OFFER_JSON, "id": 100, "heading": "New Offer", "offerLocation": None},
        )
        module = OfferModule(http_client, "/Offer/v1")
        request = CreateOffer(project_id=42, heading="New Offer", default_margin=15.0)
        result = await module.create(request)
        assert isinstance(result, OfferDetails)
        assert result.id == 100

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["projectId"] == 42
        assert body["heading"] == "New Offer"
        assert body["defaultMargin"] == 15.0

    async def test_delete(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer/789",
            method="DELETE",
            status_code=200,
        )
        module = OfferModule(http_client, "/Offer/v1")
        await module.delete(789)

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Offer/v1/Offer/GetByExternalReference",
                params={"externalReference": "off-1"},
            ),
            json={**OFFER_JSON, "externalReference": "off-1"},
        )
        module = OfferModule(http_client, "/Offer/v1")
        result = await module.get_by_external_reference(external_reference="off-1")
        assert isinstance(result, OfferDetails)
        assert result.external_reference == "off-1"

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer",
            method="PUT",
            status_code=200,
        )
        module = OfferModule(http_client, "/Offer/v1")
        request = UpdateOffer(id=789, heading="Updated Offer")
        result = await module.update(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 789
        assert body["heading"] == "Updated Offer"

    async def test_delete_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Offer/v1/Offer/DeleteByExternalReference",
                params={"externalReference": "off-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = OfferModule(http_client, "/Offer/v1")
        await module.delete_by_external_reference(external_reference="off-1")

    async def test_add_currency_to_offer(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer/AddCurrencyToOffer",
            method="POST",
            json={"id": 5, "offerId": 789, "currencyCode": 124, "exchangeRate": 1.0},
        )
        module = OfferModule(http_client, "/Offer/v1")
        request = AddCurrencyToOffer(offer_id=789, currency_code="USD", exchange_rate=1.0)
        result = await module.add_currency_to_offer(request)
        assert isinstance(result, OfferCurrencyDetails)
        assert result.id == 5
        assert result.offer_id == 789

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["offerId"] == 789
        assert body["currencyCode"] == "USD"

    async def test_update_offer_currency(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer/UpdateOfferCurrency",
            method="PUT",
            status_code=200,
        )
        module = OfferModule(http_client, "/Offer/v1")
        request = UpdateOfferCurrency(id=5, offer_id=789, exchange_rate=1.1)
        result = await module.update_offer_currency(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 5
        assert body["exchangeRate"] == 1.1

    async def test_delete_offer_currency(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Offer/v1/Offer/DeleteOfferCurrency",
                params={"offerId": "42", "offerCurrencyId": "5"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = OfferModule(http_client, "/Offer/v1")
        await module.delete_offer_currency(offer_id=42, offer_currency_id=5)

    async def test_direct_mode_no_prefix(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        """Direct mode uses empty prefix -- controller paths as-is."""
        httpx_mock.add_response(url="https://mock.example.com/Offer/789", json={**OFFER_JSON, "offerLocation": None})
        module = OfferModule(http_client, "")  # empty prefix = direct mode
        result = await module.get(789)
        assert result.id == 789

    async def test_400_raises_validation_error(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer",
            method="POST",
            status_code=400,
            json={
                "errors": {"ProjectId": ["Project not found."]},
                "title": "Validation error",
                "status": 400,
            },
        )
        module = OfferModule(http_client, "/Offer/v1")
        from qondor_api_sdk.errors import QondorValidationError

        with pytest.raises(QondorValidationError) as exc_info:
            await module.create(CreateOffer(project_id=999))
        assert "ProjectId" in exc_info.value.errors

    async def test_500_raises_server_error(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer/789",
            status_code=500,
            text="Internal Server Error",
        )
        module = OfferModule(http_client, "/Offer/v1")
        from qondor_api_sdk.errors import QondorServerError

        with pytest.raises(QondorServerError):
            await module.get(789)

    async def test_429_raises_rate_limit_error(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Offer/v1/Offer/789",
            status_code=429,
            headers={"Retry-After": "10"},
        )
        module = OfferModule(http_client, "/Offer/v1")
        from qondor_api_sdk.errors import QondorRateLimitError

        with pytest.raises(QondorRateLimitError) as exc_info:
            await module.get.__wrapped__(module, 789)  # bypass retry decorator
        assert exc_info.value.retry_after == 10.0
