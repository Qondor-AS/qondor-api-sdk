"""Tests for CustomerModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.customer import CreateCustomer, CustomerDetails, CustomerSummary, UpdateCustomer
from qondor_api_sdk.modules.customer import CustomerModule


class TestCustomerModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Customer/v1/Customer/123",
            json={"id": 123, "name": "ACME Corp", "officeId": 1, "city": "Oslo"},
        )
        module = CustomerModule(http_client, "/Customer/v1")
        result = await module.get(123)
        assert isinstance(result, CustomerDetails)
        assert result.id == 123
        assert result.name == "ACME Corp"

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Customer/v1/Customer/GetByExternalReference",
                params={"externalReference": "ext-1"},
            ),
            json={"id": 123, "name": "ACME Corp", "externalReference": "ext-1"},
        )
        module = CustomerModule(http_client, "/Customer/v1")
        result = await module.get_by_external_reference(external_reference="ext-1")
        assert isinstance(result, CustomerDetails)
        assert result.external_reference == "ext-1"

    async def test_get_all(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL("https://mock.example.com/Customer/v1/Customer/GetAll", params={"officeId": "1"}),
            json=[{"id": 123, "name": "ACME Corp", "officeId": 1}],
        )
        module = CustomerModule(http_client, "/Customer/v1")
        result = await module.get_all(office_id=1)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CustomerSummary)

    async def test_get_all_by_customer_number(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Customer/v1/Customer/GetAllByCustomerNumber",
                params={"customerNumber": "C001", "officeId": "1"},
            ),
            json=[{"id": 123, "name": "ACME Corp", "customerNumber": "C001"}],
        )
        module = CustomerModule(http_client, "/Customer/v1")
        result = await module.get_all_by_customer_number(customer_number="C001", office_id=1)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CustomerDetails)

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Customer/v1/Customer",
            method="POST",
            json={"id": 200, "name": "New Customer", "officeId": 1},
        )
        module = CustomerModule(http_client, "/Customer/v1")
        request = CreateCustomer(name="New Customer", office_id=1)
        result = await module.create(request)
        assert isinstance(result, CustomerDetails)
        assert result.id == 200

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["name"] == "New Customer"
        assert body["officeId"] == 1

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Customer/v1/Customer",
            method="PUT",
            status_code=200,
        )
        module = CustomerModule(http_client, "/Customer/v1")
        request = UpdateCustomer(id=123, name="Updated")
        result = await module.update(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 123
        assert body["name"] == "Updated"
