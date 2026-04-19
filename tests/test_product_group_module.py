"""Tests for ProductGroupModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.enums import DesignTemplate
from qondor_api_sdk.models.product_group import (
    CreateProductGroup,
    ProductGroupDetails,
    ProductGroupSummary,
    UpdateProductGroup,
)
from qondor_api_sdk.modules.product_group import ProductGroupModule

PRODUCT_GROUP_JSON = {
    "id": 20,
    "offerId": 789,
    "position": 1,
    "heading": "Accommodation",
    "offerDesignTemplate": 1,
    "hideAllProducts": False,
    "allProductsAreRequired": False,
    "hideProductPrices": False,
    "showPackagePrice": False,
    "showTotalPricePerPerson": False,
    "hidePriceTableOnOffer": False,
    "hideFeedbackOnOffer": False,
    "offerProjectId": 42,
}


class TestProductGroupModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ProductGroup/v1/ProductGroup/20",
            json=PRODUCT_GROUP_JSON,
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        result = await module.get(20)
        assert isinstance(result, ProductGroupDetails)
        assert result.id == 20
        assert result.heading == "Accommodation"

    async def test_delete(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ProductGroup/v1/ProductGroup/20",
            method="DELETE",
            status_code=200,
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        await module.delete(20)

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ProductGroup/v1/ProductGroup/GetByExternalReference",
                params={"externalReference": "pg-1"},
            ),
            json={**PRODUCT_GROUP_JSON, "externalReference": "pg-1"},
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        result = await module.get_by_external_reference(external_reference="pg-1")
        assert isinstance(result, ProductGroupDetails)
        assert result.external_reference == "pg-1"

    async def test_get_all_for_offer(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ProductGroup/v1/ProductGroup/GetAllForOffer",
                params={"offerId": "789"},
            ),
            json=[PRODUCT_GROUP_JSON],
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        result = await module.get_all_for_offer(offer_id=789)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProductGroupSummary)

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ProductGroup/v1/ProductGroup",
            method="POST",
            json=PRODUCT_GROUP_JSON,
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        request = CreateProductGroup(
            offer_id=789,
            name="Accommodation",
            position=1,
            offer_design_template=DesignTemplate.IMAGE_LEFT_TEXT_RIGHT,
        )
        result = await module.create(request)
        assert isinstance(result, ProductGroupDetails)
        assert result.id == 20

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ProductGroup/v1/ProductGroup",
            method="PUT",
            status_code=200,
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        request = UpdateProductGroup(id=20, name="Updated Name")
        result = await module.update(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 20
        assert body["name"] == "Updated Name"

    async def test_delete_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ProductGroup/v1/ProductGroup/DeleteByExternalReference",
                params={"externalReference": "pg-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = ProductGroupModule(http_client, "/ProductGroup/v1")
        await module.delete_by_external_reference(external_reference="pg-1")
