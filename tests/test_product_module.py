"""Tests for ProductModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.product import (
    AddPrice,
    AttachTicketToTransportProduct,
    ConfirmProduct,
    CreateProduct,
    ProductDetails,
    ProductPriceOut,
    ProductSummary,
    ProductTicketDetails,
    ProductTicketSummary,
    UpdatePrice,
    UpdateProduct,
)
from qondor_api_sdk.modules.product import ProductModule

PRODUCT_JSON = {
    "id": 50,
    "name": "Grand Hotel Room",
    "productType": 1,
    "offerId": 789,
    "offerQuantity": 200.0,
    "isPublishedOnOffer": True,
    "billingModel": 1,
    "commissionPercent": 10.0,
    "enableOfferConfiguration": False,
    "isOptionalOnOffer": False,
    "offerDesignTemplate": 1,
    "offerAnswer": 0,
    "referral": False,
    "isInitialRateInclVat": False,
}

TICKET_JSON = {
    "id": 1,
    "transportProductId": 50,
    "ticketNumber": "TK001",
    "travellerName": "Jane Doe",
}


class TestProductModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url="https://mock.example.com/Product/v1/Product/50", json=PRODUCT_JSON)
        module = ProductModule(http_client, "/Product/v1")
        result = await module.get(50)
        assert isinstance(result, ProductDetails)
        assert result.id == 50
        assert result.name == "Grand Hotel Room"

    async def test_delete(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product/50",
            method="DELETE",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        await module.delete(50)

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/GetByExternalReference",
                params={"externalReference": "prod-1"},
            ),
            json={**PRODUCT_JSON, "externalReference": "prod-1"},
        )
        module = ProductModule(http_client, "/Product/v1")
        result = await module.get_by_external_reference(external_reference="prod-1")
        assert isinstance(result, ProductDetails)
        assert result.external_reference == "prod-1"

    async def test_get_all_for_project(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/GetAllForProject",
                params={"projectId": "42"},
            ),
            json=[PRODUCT_JSON],
        )
        module = ProductModule(http_client, "/Product/v1")
        result = await module.get_all_for_project(project_id=42)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProductSummary)

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product",
            method="POST",
            json=PRODUCT_JSON,
        )
        module = ProductModule(http_client, "/Product/v1")
        request = CreateProduct(name="Grand Hotel Room", offer_id=789)
        result = await module.create(request)
        assert isinstance(result, ProductDetails)
        assert result.id == 50

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product",
            method="PUT",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        request = UpdateProduct(id=50, name="Updated Room")
        result = await module.update(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 50
        assert body["name"] == "Updated Room"

    async def test_delete_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/DeleteByExternalReference",
                params={"externalReference": "prod-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        await module.delete_by_external_reference(external_reference="prod-1")

    async def test_confirm_product(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product/ConfirmProduct",
            method="PUT",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        request = ConfirmProduct(product_id=50)
        result = await module.confirm_product(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["productId"] == 50

    async def test_add_price(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product/AddPrice",
            method="POST",
            json={
                "id": 100,
                "outPriceExclVat": 1500.0,
                "outPriceInclVat": 1875.0,
                "inPriceExclVat": 1200.0,
                "inPriceInclVat": 1500.0,
                "vatPercentage": 25.0,
                "vatPercentageFee": 0.0,
                "isValidFrom": "2026-01-01T00:00:00Z",
            },
        )
        module = ProductModule(http_client, "/Product/v1")
        request = AddPrice(product_id=50, out_price_excl_vat=1500.0, out_price_incl_vat=1875.0)
        result = await module.add_price(request)
        assert isinstance(result, ProductPriceOut)
        assert result.id == 100

    async def test_update_price(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product/UpdatePrice",
            method="PUT",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        request = UpdatePrice(id=100, product_id=50, out_price_excl_vat=2000.0)
        result = await module.update_price(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 100
        assert body["outPriceExclVat"] == 2000.0

    async def test_delete_price_by_id(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL("https://mock.example.com/Product/v1/Product/DeletePrice", params={"id": "100"}),
            method="DELETE",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        await module.delete_price(id=100)

    async def test_delete_price_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/DeletePrice",
                params={"externalReference": "pr-1", "productExternalReference": "prod-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        await module.delete_price(external_reference="pr-1", product_external_reference="prod-1")

    async def test_get_tickets_for_transport_product(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/GetTicketsForTransportProduct",
                params={"transportProductId": "50"},
            ),
            json=[TICKET_JSON],
        )
        module = ProductModule(http_client, "/Product/v1")
        result = await module.get_tickets_for_transport_product(transport_product_id=50)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProductTicketSummary)
        assert result[0].ticket_number == "TK001"

    async def test_get_tickets_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/GetTicketsForTransportProductByExternalReference",
                params={"transportProductExternalReference": "tp-1"},
            ),
            json=[TICKET_JSON],
        )
        module = ProductModule(http_client, "/Product/v1")
        result = await module.get_tickets_for_transport_product_by_external_reference(
            transport_product_external_reference="tp-1",
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProductTicketSummary)

    async def test_attach_ticket(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Product/v1/Product/AttachTicketToTransportProduct",
            method="POST",
            json=TICKET_JSON,
        )
        module = ProductModule(http_client, "/Product/v1")
        request = AttachTicketToTransportProduct(transport_product_id=50, ticket_id=1)
        result = await module.attach_ticket_to_transport_product(request)
        assert isinstance(result, ProductTicketDetails)
        assert result.id == 1
        assert result.transport_product_id == 50

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["transportProductId"] == 50
        assert body["ticketId"] == 1

    async def test_detach_ticket(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Product/v1/Product/DetachTicketFromTransportProduct",
                params={"transportProductId": "50", "ticketId": "1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = ProductModule(http_client, "/Product/v1")
        await module.delete_detach_ticket_from_transport_product(
            transport_product_id=50, ticket_id=1,
        )
