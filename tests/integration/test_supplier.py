"""Integration tests for supplier operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.supplier import CreateSupplier, SupplierDetails, SupplierSummary, UpdateSupplier

from .conftest import EnvConfig
from .helpers import unique_email, unique_ref

pytestmark = pytest.mark.integration


class TestSupplier:
    """Supplier lifecycle tests."""

    async def test_create(self, created_supplier: SupplierDetails):
        assert created_supplier.id is not None
        assert created_supplier.name == "IntTest Supplier"

    async def test_get(self, created_supplier: SupplierDetails, qondor_client: QondorClient):
        result = await qondor_client.supplier.get(created_supplier.id)
        assert isinstance(result, SupplierDetails)
        assert result.id == created_supplier.id

    async def test_list(self, env_config: EnvConfig, qondor_client: QondorClient):
        results = await qondor_client.supplier.get_all(office_id=env_config.office_id)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], SupplierSummary)

    async def test_get_by_ref(self, created_supplier: SupplierDetails, qondor_client: QondorClient):
        assert created_supplier.external_reference is not None
        result = await qondor_client.supplier.get_by_external_reference(
            external_reference=created_supplier.external_reference,
        )
        assert isinstance(result, SupplierDetails)
        assert result.id == created_supplier.id

    async def test_update(self, created_supplier: SupplierDetails, qondor_client: QondorClient):
        await qondor_client.supplier.update(UpdateSupplier(
            id=created_supplier.id,
            name="IntTest Supplier Updated",
            external_reference=created_supplier.external_reference or "",
            email=unique_email("sup-upd"),
            city="Stavanger",
            country_code="NO",
            address="Updated Supplier St",
            address2="Updated Unit D",
            zip_code="4005",
            organisation_number="987654321",
            vat_number="NO987654321MVA",
            phone_number="+4798765430",
            fax_number="+4798765431",
            status=2,
            chain="UpdatedChain",
            brand="UpdatedBrand",
            supplier_number="SUP-UPD",
            is_internal_supplier=False,
            invoice_address_enabled=True,
            invoice_address="Upd Inv St",
            invoice_address2="Upd Inv Unit",
            invoice_zip_code="4006",
            invoice_city="Stavanger",
            invoice_country_code="NO",
            invoice_additional_information="Updated inv info",
            remarks="Updated supplier",
        ))

    async def test_delete(self, env_config: EnvConfig, qondor_client: QondorClient):
        """Create a throwaway supplier and delete by ID."""
        ref = unique_ref()
        result = await qondor_client.supplier.create(CreateSupplier(
            name="IntTest Delete Me",
            office_id=env_config.office_id,
            external_reference=ref,
            city="Bergen",
            country_code="NO",
            zip_code="5003",
            status=1,
        ))
        await qondor_client.supplier.delete(result.id)

    async def test_delete_by_ref(self, env_config: EnvConfig, qondor_client: QondorClient):
        """Create a throwaway supplier and delete by external reference."""
        ref = unique_ref()
        await qondor_client.supplier.create(CreateSupplier(
            name="IntTest Delete By Ref",
            office_id=env_config.office_id,
            external_reference=ref,
            city="Bergen",
            country_code="NO",
            zip_code="5003",
            status=1,
        ))
        await qondor_client.supplier.delete_by_external_reference(external_reference=ref)
