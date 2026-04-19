"""Integration tests for product-group operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.offer import OfferDetails
from qondor_api_sdk.models.product_group import (
    CreateProductGroup,
    ProductGroupDetails,
    ProductGroupSummary,
    UpdateProductGroup,
)

from .helpers import unique_ref

pytestmark = pytest.mark.integration


class TestProductGroup:
    """Product-group lifecycle tests."""

    async def test_create(self, created_product_group: ProductGroupDetails):
        assert created_product_group.id is not None

    async def test_get(self, created_product_group: ProductGroupDetails, qondor_client: QondorClient):
        result = await qondor_client.product_group.get(created_product_group.id)
        assert isinstance(result, ProductGroupDetails)
        assert result.id == created_product_group.id

    async def test_list(self, created_offer: OfferDetails, qondor_client: QondorClient):
        results = await qondor_client.product_group.get_all_for_offer(offer_id=created_offer.id)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], ProductGroupSummary)

    async def test_get_by_ref(self, created_product_group: ProductGroupDetails, qondor_client: QondorClient):
        assert created_product_group.external_reference is not None
        result = await qondor_client.product_group.get_by_external_reference(
            external_reference=created_product_group.external_reference,
        )
        assert isinstance(result, ProductGroupDetails)
        assert result.id == created_product_group.id

    async def test_update(self, created_product_group: ProductGroupDetails, qondor_client: QondorClient):
        await qondor_client.product_group.update(UpdateProductGroup(
            id=created_product_group.id,
            name="IntTest Group Updated",
            position=2,
            external_reference=unique_ref("pg-upd"),
            introduction="Updated intro",
            description="Updated description",
            offer_design_template=2,
            hide_all_products=False,
            must_select_all_products=False,
            hide_product_prices=False,
            show_total_price_for_group=True,
            show_total_price_per_person=False,
            number_of_persons_in_total_price=15,
            hide_price_table=False,
            custom_total_row_text="Updated Total",
            name_on_invoice="Updated Group Invoice",
            hide_feedback_on_offer=False,
        ))

    async def test_delete(self, created_offer: OfferDetails, qondor_client: QondorClient):
        """Create a throwaway product group and delete by ID."""
        ref = unique_ref()
        result = await qondor_client.product_group.create(CreateProductGroup(
            offer_id=created_offer.id,
            name="IntTest Delete Me",
            external_reference=ref,
        ))
        await qondor_client.product_group.delete(result.id)

    async def test_delete_by_ref(self, created_offer: OfferDetails, qondor_client: QondorClient):
        """Create a throwaway product group and delete by external reference."""
        ref = unique_ref()
        await qondor_client.product_group.create(CreateProductGroup(
            offer_id=created_offer.id,
            name="IntTest Delete By Ref",
            external_reference=ref,
        ))
        await qondor_client.product_group.delete_by_external_reference(external_reference=ref)
