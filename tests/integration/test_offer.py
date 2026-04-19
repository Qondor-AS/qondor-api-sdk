"""Integration tests for offer operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.offer import (
    AddCurrencyToOffer,
    CreateOffer,
    OfferCurrencyDetails,
    OfferDetails,
    OfferSummary,
    UpdateOffer,
    UpdateOfferCurrency,
)
from qondor_api_sdk.models.project import ProjectDetails

from .helpers import unique_ref

pytestmark = pytest.mark.integration


class TestOffer:
    """Offer lifecycle tests (including currency sub-resource)."""

    async def test_create(self, created_offer: OfferDetails):
        assert created_offer.id is not None

    async def test_get(self, created_offer: OfferDetails, qondor_client: QondorClient):
        result = await qondor_client.offer.get(created_offer.id)
        assert isinstance(result, OfferDetails)
        assert result.id == created_offer.id

    async def test_list(self, created_project: ProjectDetails, qondor_client: QondorClient):
        results = await qondor_client.offer.get_all_for_project(project_id=created_project.id)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], OfferSummary)

    async def test_get_by_ref(self, created_offer: OfferDetails, qondor_client: QondorClient):
        assert created_offer.external_reference is not None
        result = await qondor_client.offer.get_by_external_reference(
            external_reference=created_offer.external_reference,
        )
        assert isinstance(result, OfferDetails)
        assert result.id == created_offer.id

    async def test_update(self, created_offer: OfferDetails, qondor_client: QondorClient):
        await qondor_client.offer.update(UpdateOffer(
            id=created_offer.id,
            heading="IntTest Offer Updated",
            default_margin=18.0,
            description="Updated description",
            is_main_offer=False,
            disable_unsure_answer_on_products_and_groups=False,
            display_total_offer_price=True,
            accommodation_offer_price_type=2,
            confirmation_page_content="Updated thank you",
            include_office_terms_and_conditions=True,
            confirmation_page_header="Updated Confirmed",
            terms_and_conditions_text="Updated T&C",
            status=1,
            email_confirmation_template_body="Updated body",
            email_confirmation_template_subject="Updated subject",
            use_office_settings=True,
            display_prices_excl_vat=True,
            display_prices_incl_vat=False,
            display_vat_amount=False,
            hide_vat_text_from_prices=False,
            display_total_price_column=True,
            display_total_price_incl_vat=False,
        ))

    async def test_add_currency(self, created_offer: OfferDetails, qondor_client: QondorClient):
        ref = unique_ref("cur")
        result = await qondor_client.offer.add_currency_to_offer(AddCurrencyToOffer(
            offer_id=created_offer.id,
            currency_code="840",
            exchange_rate=10.5,
            external_reference=ref,
            date="2026-06-01",
        ))
        assert isinstance(result, OfferCurrencyDetails)
        assert result.id is not None
        # Store for subsequent tests
        TestOffer._currency_id = result.id
        TestOffer._currency_ref = ref

    async def test_update_currency(self, created_offer: OfferDetails, qondor_client: QondorClient):
        currency_id = getattr(TestOffer, "_currency_id", None)
        if currency_id is None:
            pytest.skip("No currency created")
        await qondor_client.offer.update_offer_currency(UpdateOfferCurrency(
            id=currency_id,
            offer_id=created_offer.id,
            exchange_rate=11.0,
            external_reference=TestOffer._currency_ref,
            date_utc="2026-06-02",
            recalculate_out_prices=False,
        ))

    async def test_delete_currency(self, created_offer: OfferDetails, qondor_client: QondorClient):
        currency_id = getattr(TestOffer, "_currency_id", None)
        if currency_id is None:
            pytest.skip("No currency created")
        await qondor_client.offer.delete_offer_currency(
            offer_id=created_offer.id,
            offer_currency_id=currency_id,
        )

    async def test_delete(self, created_project: ProjectDetails, qondor_client: QondorClient):
        """Create a throwaway offer and delete by ID."""
        ref = unique_ref()
        result = await qondor_client.offer.create(CreateOffer(
            project_id=created_project.id,
            heading="IntTest Delete Me",
            external_reference=ref,
        ))
        await qondor_client.offer.delete(result.id)

    async def test_delete_by_ref(self, created_project: ProjectDetails, qondor_client: QondorClient):
        """Create a throwaway offer and delete by external reference."""
        ref = unique_ref()
        await qondor_client.offer.create(CreateOffer(
            project_id=created_project.id,
            heading="IntTest Delete By Ref",
            external_reference=ref,
        ))
        await qondor_client.offer.delete_by_external_reference(external_reference=ref)
