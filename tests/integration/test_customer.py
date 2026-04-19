"""Integration tests for customer operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.customer import CustomerDetails, CustomerSummary, UpdateCustomer

from .conftest import EnvConfig
from .helpers import unique_email

pytestmark = pytest.mark.integration


class TestCustomer:
    """Customer lifecycle tests."""

    async def test_create(self, created_customer: CustomerDetails):
        assert created_customer.id is not None
        assert created_customer.name == "IntTest Customer"

    async def test_get(self, created_customer: CustomerDetails, qondor_client: QondorClient):
        result = await qondor_client.customer.get(created_customer.id)
        assert isinstance(result, CustomerDetails)
        assert result.id == created_customer.id

    async def test_list(self, env_config: EnvConfig, qondor_client: QondorClient):
        results = await qondor_client.customer.get_all(office_id=env_config.office_id)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], CustomerSummary)

    async def test_get_by_ref(self, created_customer: CustomerDetails, qondor_client: QondorClient):
        assert created_customer.external_reference is not None
        result = await qondor_client.customer.get_by_external_reference(
            external_reference=created_customer.external_reference,
        )
        assert isinstance(result, CustomerDetails)
        assert result.id == created_customer.id

    async def test_search(
        self, created_customer: CustomerDetails, env_config: EnvConfig, qondor_client: QondorClient
    ):
        if created_customer.customer_number is None:
            pytest.skip("customer_number not in create response")
        results = await qondor_client.customer.get_all_by_customer_number(
            customer_number=str(created_customer.customer_number),
            office_id=env_config.office_id,
        )
        assert isinstance(results, list)

    async def test_update(self, created_customer: CustomerDetails, qondor_client: QondorClient):
        await qondor_client.customer.update(UpdateCustomer(
            id=created_customer.id,
            name="IntTest Customer Updated",
            external_reference=created_customer.external_reference or "",
            legal_name="IntTest Legal Updated",
            address="Updated St 1",
            address2="Updated Floor 3",
            zip_code="0160",
            city="Trondheim",
            country_code="NO",
            organisation_number="123456789",
            vat_number="NO123456789MVA",
            phone_number="+4712345670",
            fax_number="+4712345671",
            is_invoiceable=True,
            invoice_currency="NOK",
            invoice_address_enabled=True,
            invoice_address="Updated Inv St",
            invoice_address2="Updated Inv Floor",
            invoice_zip_code="0161",
            invoice_city="Trondheim",
            invoice_country_code="NO",
            invoice_additional_information="Updated inv info",
            is_active=True,
            invoice_email=unique_email("cust-upd"),
            remarks="Updated customer",
        ))
