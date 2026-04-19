"""Tests for SupplierModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.supplier import CreateSupplier, SupplierDetails, SupplierSummary, UpdateSupplier
from qondor_api_sdk.modules.supplier import SupplierModule

SUPPLIER_JSON = {"id": 1, "name": "Hotel Grand", "officeId": 1, "externalReference": "sup-1"}


class TestSupplierModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url="https://mock.example.com/Supplier/v1/Supplier/1", json=SUPPLIER_JSON)
        module = SupplierModule(http_client, "/Supplier/v1")
        result = await module.get(1)
        assert isinstance(result, SupplierDetails)
        assert result.id == 1
        assert result.name == "Hotel Grand"

    async def test_delete(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Supplier/v1/Supplier/1",
            method="DELETE",
            status_code=200,
        )
        module = SupplierModule(http_client, "/Supplier/v1")
        await module.delete(1)

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Supplier/v1/Supplier/GetByExternalReference",
                params={"externalReference": "sup-1"},
            ),
            json=SUPPLIER_JSON,
        )
        module = SupplierModule(http_client, "/Supplier/v1")
        result = await module.get_by_external_reference(external_reference="sup-1")
        assert isinstance(result, SupplierDetails)
        assert result.external_reference == "sup-1"

    async def test_get_all(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Supplier/v1/Supplier/GetAll",
                params={"officeId": "1"},
            ),
            json=[{"id": 1, "name": "Hotel Grand"}],
        )
        module = SupplierModule(http_client, "/Supplier/v1")
        result = await module.get_all(office_id=1)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], SupplierSummary)

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Supplier/v1/Supplier",
            method="POST",
            json=SUPPLIER_JSON,
        )
        module = SupplierModule(http_client, "/Supplier/v1")
        request = CreateSupplier(office_id=1, name="Hotel Grand")
        result = await module.create(request)
        assert isinstance(result, SupplierDetails)
        assert result.id == 1

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["officeId"] == 1
        assert body["name"] == "Hotel Grand"

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Supplier/v1/Supplier",
            method="PUT",
            status_code=200,
        )
        module = SupplierModule(http_client, "/Supplier/v1")
        request = UpdateSupplier(id=1, name="Hotel Grand Updated")
        result = await module.update(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 1
        assert body["name"] == "Hotel Grand Updated"

    async def test_delete_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Supplier/v1/Supplier/DeleteByExternalReference",
                params={"externalReference": "sup-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = SupplierModule(http_client, "/Supplier/v1")
        await module.delete_by_external_reference(external_reference="sup-1")
