"""Tests for ContactPersonModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.contact_person import (
    CreateContactPerson,
    CustomerContactPersonsDetails,
    UpdateContactPerson,
    UpdateContactPersonCustomer,
    UpdateContactPersonSupplier,
)
from qondor_api_sdk.modules.contact_person import ContactPersonModule

CONTACT_PERSON_JSON = {
    "id": 10,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "isActive": True,
}


class TestContactPersonModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ContactPerson/v1/ContactPerson/10",
            json=CONTACT_PERSON_JSON,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        result = await module.get(10)
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == 10
        assert result.first_name == "John"

    async def test_get_by_email(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ContactPerson/v1/ContactPerson/GetByEmail",
                params={"email": "a@example.com"},
            ),
            json={"id": 10, "firstName": "John", "email": "a@example.com"},
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        result = await module.get_by_email(email="a@example.com")
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == 10

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ContactPerson/v1/ContactPerson/GetByExternalReference",
                params={"externalReference": "cp-1"},
            ),
            json={"id": 10, "firstName": "John", "externalReference": "cp-1"},
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        result = await module.get_by_external_reference(external_reference="cp-1")
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == 10

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ContactPerson/v1/ContactPerson",
            method="POST",
            json=CONTACT_PERSON_JSON,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        request = CreateContactPerson(first_name="John", last_name="Doe", email="john@example.com")
        result = await module.create(request)
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == 10
        assert result.first_name == "John"

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["firstName"] == "John"
        assert body["lastName"] == "Doe"
        assert body["email"] == "john@example.com"

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ContactPerson/v1/ContactPerson",
            method="PUT",
            status_code=200,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        request = UpdateContactPerson(id=10, first_name="Jane")
        result = await module.update(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 10
        assert body["firstName"] == "Jane"

    async def test_delete(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ContactPerson/v1/ContactPerson/10",
            method="DELETE",
            status_code=200,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        await module.delete(10)

    async def test_delete_by_email(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ContactPerson/v1/ContactPerson/DeleteByEmail",
                params={"email": "john@example.com"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        await module.delete_by_email(email="john@example.com")

    async def test_delete_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/ContactPerson/v1/ContactPerson/DeleteByExternalReference",
                params={"externalReference": "cp-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        await module.delete_by_external_reference(external_reference="cp-1")

    async def test_update_customer_relation(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ContactPerson/v1/ContactPerson/UpdateCustomerRelation",
            method="PUT",
            status_code=200,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        request = UpdateContactPersonCustomer(contact_person_id=10, customer_id=123, is_active=True)
        result = await module.update_customer_relation(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["contactPersonId"] == 10
        assert body["customerId"] == 123
        assert body["isActive"] is True

    async def test_update_supplier_relation(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/ContactPerson/v1/ContactPerson/UpdateSupplierRelation",
            method="PUT",
            status_code=200,
        )
        module = ContactPersonModule(http_client, "/ContactPerson/v1")
        request = UpdateContactPersonSupplier(contact_person_id=10, supplier_id=456, is_active=True)
        result = await module.update_supplier_relation(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["contactPersonId"] == 10
        assert body["supplierId"] == 456
