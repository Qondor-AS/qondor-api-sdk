"""Integration tests for accommodation product, room, and room night operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.accommodation_product import (
    AccommodationProductDetails,
    AccommodationProductSummary,
    AccommodationRoomDetails,
    AccommodationRoomNightDetails,
    AccommodationRoomNightPrice,
    CreateAccommodationProduct,
    CreateAccommodationRoom,
    CreateAccommodationRoomNight,
    UpdateAccommodationProduct,
    UpdateAccommodationRoom,
    UpdateAccommodationRoomNight,
)
from qondor_api_sdk.models.offer import OfferDetails
from qondor_api_sdk.models.product_group import ProductGroupDetails
from qondor_api_sdk.models.supplier import SupplierDetails

from .helpers import unique_ref

pytestmark = pytest.mark.integration


class TestAccommodationProduct:
    """Accommodation product lifecycle (plus rooms and nights)."""

    async def test_create(
        self,
        created_offer: OfferDetails,
        created_product_group: ProductGroupDetails,
        created_supplier: SupplierDetails,
        qondor_client: QondorClient,
    ):
        ref = unique_ref("acc")
        result = await qondor_client.accommodation_product.create(CreateAccommodationProduct(
            name="IntTest Accommodation",
            offer_id=created_offer.id,
            product_group_id=created_product_group.id,
            supplier_id=created_supplier.id,
            external_reference=ref,
            offer_intro_text="Accommodation intro",
            offer_description="Accommodation description",
            offer_quantity=1,
            offer_terms_and_conditions_text="Accommodation T&C",
            name_on_invoice="IntTest Acc Inv",
            name_on_offer="IntTest Acc Offer",
            supplier_invoice_reference="ACC-INV-001",
            is_published_on_offer=True,
            is_mandatory_on_offer=False,
            hide_feedback_on_offer=False,
        ))
        assert isinstance(result, AccommodationProductDetails)
        assert result.id is not None
        TestAccommodationProduct._product_id = result.id
        TestAccommodationProduct._product_ref = ref

    async def test_get(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        if product_id is None:
            pytest.skip("No accommodation product created")
        result = await qondor_client.accommodation_product.get(product_id)
        assert isinstance(result, AccommodationProductDetails)
        assert result.id == product_id

    async def test_get_by_ref(self, qondor_client: QondorClient):
        product_ref = getattr(TestAccommodationProduct, "_product_ref", None)
        if product_ref is None:
            pytest.skip("No accommodation product created")
        result = await qondor_client.accommodation_product.get_by_external_reference(
            external_reference=product_ref,
        )
        assert isinstance(result, AccommodationProductDetails)
        assert result.external_reference == product_ref

    async def test_list(self, created_project, qondor_client: QondorClient):
        results = await qondor_client.accommodation_product.get_all_for_project(
            project_id=created_project.id,
        )
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], AccommodationProductSummary)

    async def test_update(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        if product_id is None:
            pytest.skip("No accommodation product created")
        # NOTE: do NOT pass product_group_id here. The API6 update validator has
        # a bug (UpdateAccommodationProductContract.cs:119) that compares
        # productGroup.OfferId against accommodationProduct.ProductGroup.Id
        # (should be .OfferId), which always fails.
        await qondor_client.accommodation_product.update(UpdateAccommodationProduct(
            id=product_id,
            name="IntTest Accommodation Updated",
            offer_intro_text="Updated accommodation intro",
            offer_description="Updated accommodation description",
            offer_quantity=2,
            name_on_invoice="Updated Acc Inv",
            name_on_offer="Updated Acc Offer",
            is_published_on_offer=True,
            is_mandatory_on_offer=False,
            hide_feedback_on_offer=False,
        ))

    # --- Room sub-resource ---

    async def test_create_room(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        if product_id is None:
            pytest.skip("No accommodation product created")
        ref = unique_ref("room")
        result = await qondor_client.accommodation_product.create_room(CreateAccommodationRoom(
            accommodation_product_id=product_id,
            name="Double Room",
            external_reference=ref,
            guests_per_room=2,
            commission_percent=0.0,
            is_initial_rate_incl_vat=False,
        ))
        assert isinstance(result, AccommodationRoomDetails)
        assert result.id is not None
        TestAccommodationProduct._room_id = result.id
        TestAccommodationProduct._room_ref = ref

    async def test_update_room(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        room_id = getattr(TestAccommodationProduct, "_room_id", None)
        if product_id is None or room_id is None:
            pytest.skip("No accommodation product or room created")
        await qondor_client.accommodation_product.update_room(UpdateAccommodationRoom(
            id=room_id,
            accommodation_product_id=product_id,
            name="Twin Room",
            guests_per_room=2,
        ))

    # --- Night sub-resource ---

    async def test_create_room_night(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        room_id = getattr(TestAccommodationProduct, "_room_id", None)
        if product_id is None or room_id is None:
            pytest.skip("No accommodation product or room created")
        ref = unique_ref("night")
        result = await qondor_client.accommodation_product.create_room_night(
            CreateAccommodationRoomNight(
                accommodation_product_id=product_id,
                room_id=room_id,
                external_reference=ref,
                check_in_date="2026-06-01",
                allotment=5,
                initial_rate=1200.0,
                prices=[AccommodationRoomNightPrice(
                    art_no="0",
                    out_price_excl_vat=1200.0,
                    out_price_incl_vat=1200.0,
                    in_price_excl_vat=1000.0,
                    in_price_incl_vat=1000.0,
                )],
            )
        )
        assert isinstance(result, AccommodationRoomNightDetails)
        assert result.id is not None
        TestAccommodationProduct._night_id = result.id

    async def test_update_room_night(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        room_id = getattr(TestAccommodationProduct, "_room_id", None)
        night_id = getattr(TestAccommodationProduct, "_night_id", None)
        if not all([product_id, room_id, night_id]):
            pytest.skip("Missing accommodation product, room, or night")
        await qondor_client.accommodation_product.update_room_night(
            UpdateAccommodationRoomNight(
                id=night_id,
                room_id=room_id,
                accommodation_product_id=product_id,
                allotment=10,
            )
        )

    async def test_delete_room_night(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        room_id = getattr(TestAccommodationProduct, "_room_id", None)
        night_id = getattr(TestAccommodationProduct, "_night_id", None)
        if not all([product_id, room_id, night_id]):
            pytest.skip("Missing accommodation product, room, or night")
        await qondor_client.accommodation_product.delete_room_night(
            id=night_id,
            room_id=room_id,
            accommodation_product_id=product_id,
        )

    # --- Teardown deletes (run last by suffix ordering) ---

    async def test_zz_delete_room(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        room_id = getattr(TestAccommodationProduct, "_room_id", None)
        if product_id is None or room_id is None:
            pytest.skip("No accommodation product or room created")
        await qondor_client.accommodation_product.delete_room(
            id=room_id,
            accommodation_product_id=product_id,
        )

    async def test_zz_delete(self, qondor_client: QondorClient):
        product_id = getattr(TestAccommodationProduct, "_product_id", None)
        if product_id is None:
            pytest.skip("No accommodation product created")
        await qondor_client.accommodation_product.delete(product_id)

    # --- Standalone: create + delete-by-ref on a throwaway product ---

    async def test_delete_by_ref(
        self,
        created_offer: OfferDetails,
        created_product_group: ProductGroupDetails,
        qondor_client: QondorClient,
    ):
        ref = unique_ref("acc-del")
        await qondor_client.accommodation_product.create(CreateAccommodationProduct(
            name="IntTest Delete By Ref",
            offer_id=created_offer.id,
            product_group_id=created_product_group.id,
            external_reference=ref,
        ))
        await qondor_client.accommodation_product.delete_by_external_reference(
            external_reference=ref,
        )
