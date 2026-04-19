"""Integration tests for contact-person operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.contact_person import (
    CreateContactPerson,
    CustomerContactPersonsDetails,
    UpdateContactPerson,
    UpdateContactPersonCustomer,
    UpdateContactPersonSupplier,
)
from qondor_api_sdk.models.supplier import SupplierDetails

from .conftest import EnvConfig
from .helpers import unique_email, unique_ref

pytestmark = pytest.mark.integration


class TestContactPerson:
    """Contact-person lifecycle tests."""

    async def test_create(self, created_contact_person: CustomerContactPersonsDetails):
        assert created_contact_person.id is not None

    async def test_get(
        self, created_contact_person: CustomerContactPersonsDetails, qondor_client: QondorClient
    ):
        result = await qondor_client.contact_person.get(created_contact_person.id)
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == created_contact_person.id

    async def test_get_by_email(
        self, created_contact_person: CustomerContactPersonsDetails, qondor_client: QondorClient
    ):
        assert created_contact_person.email is not None
        result = await qondor_client.contact_person.get_by_email(email=created_contact_person.email)
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == created_contact_person.id

    async def test_get_by_ref(
        self, created_contact_person: CustomerContactPersonsDetails, qondor_client: QondorClient
    ):
        assert created_contact_person.external_reference is not None
        result = await qondor_client.contact_person.get_by_external_reference(
            external_reference=created_contact_person.external_reference,
        )
        assert isinstance(result, CustomerContactPersonsDetails)
        assert result.id == created_contact_person.id

    async def test_update(
        self, created_contact_person: CustomerContactPersonsDetails, qondor_client: QondorClient
    ):
        await qondor_client.contact_person.update(UpdateContactPerson(
            id=created_contact_person.id,
            first_name="IntUpdated",
            last_name="TestUpdated",
            email=unique_email("cp-upd"),
            phone_number="91122334",
            external_reference=unique_ref("cp-upd"),
            phone_country_code="+47",
            phone_country_code2="+46",
            phone_number2="703334444",
        ))

    async def test_update_customer_relation(
        self,
        created_contact_person: CustomerContactPersonsDetails,
        env_config: EnvConfig,
        qondor_client: QondorClient,
    ):
        await qondor_client.contact_person.update_customer_relation(
            UpdateContactPersonCustomer(
                contact_person_id=created_contact_person.id,
                customer_id=env_config.customer_id,
                is_active=True,
            )
        )

    async def test_update_supplier_relation(
        self,
        created_contact_person: CustomerContactPersonsDetails,
        created_supplier: SupplierDetails,
        qondor_client: QondorClient,
    ):
        await qondor_client.contact_person.update_supplier_relation(
            UpdateContactPersonSupplier(
                contact_person_id=created_contact_person.id,
                supplier_id=created_supplier.id,
                is_active=True,
            )
        )

    async def test_update_customer_relation_by_email(
        self,
        created_contact_person_for_relation: CustomerContactPersonsDetails,
        env_config: EnvConfig,
        qondor_client: QondorClient,
    ):
        """Link a contact person via email + customer external-reference."""
        email = created_contact_person_for_relation.email
        assert email is not None

        # Fetch the seed customer to get its external reference
        cust = await qondor_client.customer.get(env_config.customer_id)

        if cust.external_reference:
            await qondor_client.contact_person.update_customer_relation(
                UpdateContactPersonCustomer(
                    contact_person_email=email,
                    customer_external_reference=cust.external_reference,
                    is_active=True,
                )
            )
        else:
            await qondor_client.contact_person.update_customer_relation(
                UpdateContactPersonCustomer(
                    contact_person_email=email,
                    customer_id=env_config.customer_id,
                    is_active=True,
                )
            )

    async def test_delete(self, qondor_client: QondorClient):
        """Create a throwaway contact person and delete by ID."""
        email = unique_email("cp-del")
        cp = await qondor_client.contact_person.create(CreateContactPerson(
            first_name="Del",
            last_name="ById",
            email=email,
        ))
        await qondor_client.contact_person.delete(cp.id)

    async def test_delete_by_email(self, qondor_client: QondorClient):
        """Create a throwaway contact person and delete by email."""
        email = unique_email("cp-del-email")
        await qondor_client.contact_person.create(CreateContactPerson(
            first_name="Del",
            last_name="ByEmail",
            email=email,
        ))
        await qondor_client.contact_person.delete_by_email(email=email)

    async def test_delete_by_ref(self, qondor_client: QondorClient):
        """Create a throwaway contact person and delete by external reference."""
        ref = unique_ref("cp-del-ref")
        await qondor_client.contact_person.create(CreateContactPerson(
            first_name="Del",
            last_name="ByRef",
            email=unique_email("cp-del-ref"),
            external_reference=ref,
        ))
        await qondor_client.contact_person.delete_by_external_reference(external_reference=ref)
