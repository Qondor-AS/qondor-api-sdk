"""Tests for QondorClient auth header injection and module initialization."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import _RESOURCE_GROUPS, QondorClient
from qondor_api_sdk.modules.customer import CustomerModule
from qondor_api_sdk.modules.offer import OfferModule
from qondor_api_sdk.modules.product import ProductModule
from qondor_api_sdk.modules.product_group import ProductGroupModule
from qondor_api_sdk.modules.project import ProjectModule
from qondor_api_sdk.modules.supplier import SupplierModule


class TestClientDefaults:
    @pytest.fixture
    def client(self):
        c = QondorClient(
            base_url="https://mock.example.com/Prod",
            subscription_key="test-sub-key",
            on_behalf_of_jwt="test-jwt-token",
        )
        yield c

    def test_default_auth_headers(self, client: QondorClient):
        headers = client._http.headers
        assert headers["Ocp-Apim-Subscription-Key"] == "test-sub-key"
        assert headers["X-OnBehalfOf-Token"] == "test-jwt-token"

    def test_default_module_prefixes(self, client: QondorClient):
        assert client.customer._prefix == "/Customer/v1"
        assert client.project._prefix == "/Project/v1"
        assert client.offer._prefix == "/Offer/v1"
        assert client.product._prefix == "/Product/v1"
        assert client.product_group._prefix == "/ProductGroup/v1"
        assert client.supplier._prefix == "/Supplier/v1"
        assert client.office._prefix == "/Office/v1"
        assert client.contact_person._prefix == "/ContactPerson/v1"
        assert client.statistics._prefix == "/Statistics/v1"

    def test_module_types(self, client: QondorClient):
        assert isinstance(client.customer, CustomerModule)
        assert isinstance(client.project, ProjectModule)
        assert isinstance(client.offer, OfferModule)
        assert isinstance(client.product, ProductModule)
        assert isinstance(client.product_group, ProductGroupModule)
        assert isinstance(client.supplier, SupplierModule)


class TestClientCustomAuth:
    @pytest.fixture
    def client(self):
        c = QondorClient(
            base_url="https://mock.example.com",
            subscription_key="test-user-id",
            on_behalf_of_jwt="test-jwt-token",
            auth_header="X-Custom-Auth",
            use_resource_group_prefixes=False,
        )
        yield c

    def test_custom_auth_headers(self, client: QondorClient):
        headers = client._http.headers
        assert headers["X-Custom-Auth"] == "test-user-id"
        assert headers["X-OnBehalfOf-Token"] == "test-jwt-token"
        assert "Ocp-Apim-Subscription-Key" not in headers

    def test_no_module_prefixes(self, client: QondorClient):
        """With use_resource_group_prefixes=False, prefixes are empty."""
        assert client.customer._prefix == ""
        assert client.project._prefix == ""
        assert client.offer._prefix == ""
        assert client.product._prefix == ""


class TestResourceGroups:
    def test_all_nine_groups_defined(self):
        expected = {
            "Customer", "Project", "Offer", "Product", "ProductGroup",
            "Supplier", "Office", "ContactPerson", "Statistics",
        }
        assert set(_RESOURCE_GROUPS.keys()) == expected

    def test_versioned_paths(self):
        for key, value in _RESOURCE_GROUPS.items():
            assert value.endswith("/v1"), f"{key} should have /v1 suffix"


class TestClientClose:
    async def test_close(self):
        client = QondorClient(
            base_url="https://example.com",
            subscription_key="key",
            on_behalf_of_jwt="jwt",
        )
        await client.close()
        assert client._http.is_closed
