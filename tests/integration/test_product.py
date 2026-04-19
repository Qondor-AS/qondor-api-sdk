"""Integration tests for product operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.offer import OfferDetails
from qondor_api_sdk.models.product import (
    AddPrice,
    AttachTicketToTransportProduct,
    ConfirmProduct,
    CreateProduct,
    ProductDetails,
    ProductPriceOut,
    ProductSummary,
    ProductTicketSummary,
    UpdatePrice,
    UpdateProduct,
)
from qondor_api_sdk.models.product_group import ProductGroupDetails
from qondor_api_sdk.models.supplier import SupplierDetails

from .conftest import EnvConfig
from .helpers import unique_ref

pytestmark = pytest.mark.integration


class TestProduct:
    """Product lifecycle tests (including prices, confirm, transport/tickets)."""

    async def test_create(self, created_product: ProductDetails):
        assert created_product.id is not None

    async def test_get(self, created_product: ProductDetails, qondor_client: QondorClient):
        result = await qondor_client.product.get(created_product.id)
        assert isinstance(result, ProductDetails)
        assert result.id == created_product.id

    async def test_list(self, created_project, qondor_client: QondorClient):
        results = await qondor_client.product.get_all_for_project(project_id=created_project.id)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], ProductSummary)

    async def test_get_by_ref(self, created_product: ProductDetails, qondor_client: QondorClient):
        assert created_product.external_reference is not None
        result = await qondor_client.product.get_by_external_reference(
            external_reference=created_product.external_reference,
        )
        assert isinstance(result, ProductDetails)
        assert result.id == created_product.id

    async def test_update(
        self,
        created_product: ProductDetails,
        created_product_group: ProductGroupDetails,
        qondor_client: QondorClient,
    ):
        await qondor_client.product.update(UpdateProduct(
            id=created_product.id,
            name="IntTest Product Updated",
            external_reference=unique_ref("prod-upd"),
            product_group_id=created_product_group.id,
            offer_intro_text="Updated intro",
            offer_description="Updated description",
            offer_quantity=8,
            offer_terms_and_conditions_text="Updated T&C",
            name_on_invoice="Updated Inv Name",
            name_on_offer="Updated Offer Name",
            supplier_specified=True,
            supplier_invoice_reference="SUP-INV-002",
            is_published_on_offer=True,
            is_mandatory_on_offer=False,
            hide_feedback_on_offer=False,
            commission_percent=12.0,
            billing_model=0,
            initial_rate=600.0,
            is_initial_rate_incl_vat=False,
        ))

    # --- Price sub-resource ---

    @pytest.mark.skip(
        reason=(
            "TODO: revisit when env access available — "
            "Qondor dev env rejects ART-001/ART-002; valid ArtNo format unknown"
        )
    )
    async def test_add_price(self, created_product: ProductDetails, qondor_client: QondorClient):
        ref = unique_ref("price")
        result = await qondor_client.product.add_price(AddPrice(
            product_id=created_product.id,
            out_price_excl_vat=1000.0,
            out_price_incl_vat=1250.0,
            in_price_excl_vat=800.0,
            in_price_incl_vat=1000.0,
            external_reference=ref,
            art_no="ART-001",
        ))
        assert isinstance(result, ProductPriceOut)
        assert result.id is not None
        TestProduct._price_id = result.id
        TestProduct._price_ref = ref

    @pytest.mark.skip(
        reason=(
            "TODO: revisit when env access available — "
            "Qondor dev env rejects ART-001/ART-002; valid ArtNo format unknown"
        )
    )
    async def test_update_price(self, created_product: ProductDetails, qondor_client: QondorClient):
        price_id = getattr(TestProduct, "_price_id", None)
        if price_id is None:
            pytest.skip("No price created")
        await qondor_client.product.update_price(UpdatePrice(
            id=price_id,
            product_id=created_product.id,
            out_price_excl_vat=1100.0,
            out_price_incl_vat=1375.0,
            in_price_excl_vat=850.0,
            in_price_incl_vat=1062.5,
            external_reference=TestProduct._price_ref,
            art_no="ART-002",
        ))

    @pytest.mark.skip(
        reason="TODO: revisit when env access available — depends on test_add_price which is skipped"
    )
    async def test_delete_price(self, created_product: ProductDetails, qondor_client: QondorClient):
        price_id = getattr(TestProduct, "_price_id", None)
        if price_id is None:
            pytest.skip("No price created")
        await qondor_client.product.delete_price(
            id=price_id,
            product_id=created_product.id,
        )

    # --- Confirm ---

    @pytest.mark.skip(
        reason=(
            "TODO: revisit when env access available — "
            "PUT /Product/ConfirmProduct returns 404, likely from "
            "GetProjectByIdOrNoWithGuardAsync (product.ProjectId null or permission guard)"
        )
    )
    async def test_confirm(self, created_product: ProductDetails, qondor_client: QondorClient):
        await qondor_client.product.confirm_product(ConfirmProduct(
            product_id=created_product.id,
        ))

    # --- Delete ---

    async def test_delete(
        self,
        created_offer: OfferDetails,
        created_product_group: ProductGroupDetails,
        created_supplier: SupplierDetails,
        qondor_client: QondorClient,
    ):
        """Create a throwaway product and delete by ID."""
        ref = unique_ref()
        result = await qondor_client.product.create(CreateProduct(
            name="IntTest Delete Me",
            offer_id=created_offer.id,
            product_group_id=created_product_group.id,
            product_type=1,
            external_reference=ref,
        ))
        await qondor_client.product.delete(result.id)

    async def test_delete_by_ref(
        self,
        created_offer: OfferDetails,
        created_product_group: ProductGroupDetails,
        qondor_client: QondorClient,
    ):
        """Create a throwaway product and delete by external reference."""
        ref = unique_ref()
        await qondor_client.product.create(CreateProduct(
            name="IntTest Delete By Ref",
            offer_id=created_offer.id,
            product_group_id=created_product_group.id,
            product_type=1,
            external_reference=ref,
        ))
        await qondor_client.product.delete_by_external_reference(external_reference=ref)

    # --- Transport product + tickets ---

    async def test_create_transport(
        self,
        created_offer: OfferDetails,
        created_product_group: ProductGroupDetails,
        qondor_client: QondorClient,
    ):
        """Create a transport product (product_type=2)."""
        ref = unique_ref("transport")
        result = await qondor_client.product.create(CreateProduct(
            name="IntTest Transport Product",
            offer_id=created_offer.id,
            product_group_id=created_product_group.id,
            product_type=2,
            external_reference=ref,
        ))
        assert result.id is not None
        TestProduct._transport_product_id = result.id
        TestProduct._transport_product_ref = ref

    async def test_get_tickets(self, qondor_client: QondorClient):
        transport_id = getattr(TestProduct, "_transport_product_id", None)
        if transport_id is None:
            pytest.skip("No transport product created")
        results = await qondor_client.product.get_tickets_for_transport_product(
            transport_product_id=transport_id,
        )
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], ProductTicketSummary)

    async def test_get_tickets_by_ref(self, qondor_client: QondorClient):
        transport_ref = getattr(TestProduct, "_transport_product_ref", None)
        if transport_ref is None:
            pytest.skip("No transport product created")
        results = await qondor_client.product.get_tickets_for_transport_product_by_external_reference(
            transport_product_external_reference=transport_ref,
        )
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], ProductTicketSummary)

    async def test_attach_detach_ticket(self, env_config: EnvConfig, qondor_client: QondorClient):
        transport_id = getattr(TestProduct, "_transport_product_id", None)
        if transport_id is None:
            pytest.skip("No transport product created")
        if not env_config.ticket_ids:
            pytest.skip("QONDOR_TICKET_IDS not configured")

        ticket_id = env_config.ticket_ids[0]

        # Attach
        await qondor_client.product.attach_ticket_to_transport_product(
            AttachTicketToTransportProduct(
                transport_product_id=transport_id,
                ticket_id=ticket_id,
            )
        )

        # Detach
        await qondor_client.product.delete_detach_ticket_from_transport_product(
            transport_product_id=transport_id,
            ticket_id=ticket_id,
        )
