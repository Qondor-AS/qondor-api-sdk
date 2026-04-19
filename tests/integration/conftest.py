"""Integration-test configuration: env config, seed data, session fixtures."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import pytest
import pytest_asyncio

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.contact_person import CreateContactPerson
from qondor_api_sdk.models.customer import CreateCustomer
from qondor_api_sdk.models.offer import CreateOffer
from qondor_api_sdk.models.product import CreateProduct
from qondor_api_sdk.models.product_group import CreateProductGroup
from qondor_api_sdk.models.project import CreateProject
from qondor_api_sdk.models.supplier import CreateSupplier

from .helpers import unique_email, unique_ref

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment URL mapping
# ---------------------------------------------------------------------------

_ENV_URLS = {
    "prod": "https://qondor.azure-api.net/Prod",
    "test": "https://qondor.azure-api.net/Test",
    "dev": "https://qondor.azure-api.net/Dev",
}


# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EnvConfig:
    """Pre-existing entity IDs for a target environment."""

    subscription_key: str
    env_name: str
    office_id: int
    customer_id: int
    project_manager_id: int
    team_id: int
    contact_person_id: int
    ticket_ids: list[int] | None = None


SEED: dict[str, dict] = {
    "dev": dict(office_id=2, customer_id=1, project_manager_id=5, team_id=1, contact_person_id=6),
    "test": dict(office_id=102, customer_id=15409, project_manager_id=264636, team_id=19, contact_person_id=264718),
}


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def env_config() -> EnvConfig:
    """Read QONDOR_ENV + QONDOR_SUBSCRIPTION_KEY and return config; skip if missing."""
    key = os.environ.get("QONDOR_SUBSCRIPTION_KEY")
    env_name = os.environ.get("QONDOR_ENV", "dev")
    if not key:
        pytest.skip("QONDOR_SUBSCRIPTION_KEY not set")
    if env_name not in SEED:
        pytest.skip(f"No seed data for QONDOR_ENV={env_name}")
    ticket_ids_raw = os.environ.get("QONDOR_TICKET_IDS")
    ticket_ids = [int(x) for x in ticket_ids_raw.split(",")] if ticket_ids_raw else None
    return EnvConfig(subscription_key=key, env_name=env_name, ticket_ids=ticket_ids, **SEED[env_name])


@pytest_asyncio.fixture(scope="session")
async def qondor_client(env_config: EnvConfig) -> QondorClient:
    """Create a real QondorClient for the session; close on teardown."""
    client = QondorClient(
        base_url=_ENV_URLS[env_config.env_name],
        subscription_key=env_config.subscription_key,
    )
    yield client
    await client.close()


# ---------------------------------------------------------------------------
# Entity creation fixtures (session-scoped, yield + best-effort cleanup)
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture(scope="session")
async def created_customer(env_config: EnvConfig, qondor_client: QondorClient):
    """Create a customer (not deletable via API)."""
    ref = unique_ref()
    result = await qondor_client.customer.create(CreateCustomer(
        name="IntTest Customer",
        office_id=env_config.office_id,
        external_reference=ref,
        city="Oslo",
        country_code="NO",
        organisation_number="123456789",
        legal_name="IntTest Legal",
        address="Test St 1",
        address2="Floor 2",
        zip_code="0150",
        vat_number="NO123456789MVA",
        phone_number="+4712345678",
        fax_number="+4712345679",
        is_invoiceable=True,
        invoice_currency="NOK",
        invoice_address_enabled=True,
        invoice_address="Invoice St 1",
        invoice_address2="Invoice Floor 2",
        invoice_zip_code="0151",
        invoice_city="Oslo",
        invoice_country_code="NO",
        invoice_additional_information="IntTest invoice info",
        is_active=True,
        invoice_email=unique_email(),
        remarks="Integration test customer",
    ))
    return result


@pytest_asyncio.fixture(scope="session")
async def created_supplier(env_config: EnvConfig, qondor_client: QondorClient):
    """Create a supplier; delete on teardown."""
    ref = unique_ref()
    result = await qondor_client.supplier.create(CreateSupplier(
        name="IntTest Supplier",
        office_id=env_config.office_id,
        email=unique_email("supplier"),
        external_reference=ref,
        city="Bergen",
        country_code="NO",
        address="Supplier St 1",
        address2="Unit B",
        zip_code="5003",
        organisation_number="987654321",
        vat_number="NO987654321MVA",
        phone_number="+4798765432",
        fax_number="+4798765433",
        status=1,
        chain="TestChain",
        brand="TestBrand",
        supplier_number=f"SUP-{ref[-8:]}",
        is_internal_supplier=False,
        invoice_address_enabled=True,
        invoice_address="Inv Supplier St 1",
        invoice_address2="Inv Unit C",
        invoice_zip_code="5004",
        invoice_city="Bergen",
        invoice_country_code="NO",
        invoice_additional_information="Supplier inv info",
        remarks="Integration test supplier",
    ))
    yield result
    # best-effort cleanup
    try:
        await qondor_client.supplier.delete(result.id)
    except Exception:
        # Cleanup is best-effort; log but don't fail the test session
        logger.warning("teardown cleanup failed", exc_info=True)


@pytest_asyncio.fixture(scope="session")
async def created_contact_person(qondor_client: QondorClient):
    """Create a contact person; delete on teardown."""
    ref = unique_ref()
    email = unique_email("cp")
    result = await qondor_client.contact_person.create(CreateContactPerson(
        first_name="Int",
        last_name="Test",
        email=email,
        phone_number="98765432",
        external_reference=ref,
        phone_country_code="+47",
        phone_country_code2="+46",
        phone_number2="701234567",
    ))
    yield result
    try:
        await qondor_client.contact_person.delete(result.id)
    except Exception:
        # Cleanup is best-effort; log but don't fail the test session
        logger.warning("teardown cleanup failed", exc_info=True)


@pytest_asyncio.fixture(scope="session")
async def created_contact_person_for_relation(qondor_client: QondorClient):
    """Create a second contact person for relation tests; delete on teardown."""
    email = unique_email("cp-rel")
    ref = unique_ref("cp-rel")
    result = await qondor_client.contact_person.create(CreateContactPerson(
        first_name="Rel",
        last_name="Test",
        email=email,
        external_reference=ref,
    ))
    yield result
    try:
        await qondor_client.contact_person.delete(result.id)
    except Exception:
        # Cleanup is best-effort; log but don't fail the test session
        logger.warning("teardown cleanup failed", exc_info=True)


@pytest_asyncio.fixture(scope="session")
async def created_project(env_config: EnvConfig, qondor_client: QondorClient):
    """Create a project (not deletable via API)."""
    result = await qondor_client.project.create(CreateProject(
        name="IntTest Project",
        project_no=unique_ref("proj"),
        office_id=env_config.office_id,
        customer_id=env_config.customer_id,
        pax=10,
        start_date="2026-06-01",
        end_date="2026-06-10",
        location="Oslo",
        main_project_manager_id=env_config.project_manager_id,
        team_id=env_config.team_id,
        main_contact_person_id=env_config.contact_person_id,
        location_code="OSL",
        budgeted_sales=100000,
        budgeted_revenue=20000,
        currency="NOK",
    ))
    return result


@pytest_asyncio.fixture(scope="session")
async def created_offer(created_project, qondor_client: QondorClient):
    """Create an offer on the project; delete on teardown."""
    ref = unique_ref()
    result = await qondor_client.offer.create(CreateOffer(
        project_id=created_project.id,
        heading="IntTest Offer",
        default_margin=15.0,
        description="Integration test offer",
        external_reference=ref,
        is_main_offer=False,
        disable_unsure_answer_on_products_and_groups=False,
        display_total_offer_price=True,
        accommodation_offer_price_type=1,
        confirmation_page_content="Thank you",
        include_office_terms_and_conditions=True,
        confirmation_page_header="Confirmed",
        terms_and_conditions_text="Standard T&C",
        status=1,
        email_confirmation_template_body="Booking confirmed",
        email_confirmation_template_subject="Confirmation",
        use_office_settings=True,
        display_prices_excl_vat=True,
        display_prices_incl_vat=False,
        display_vat_amount=False,
        hide_vat_text_from_prices=False,
        display_total_price_column=True,
        display_total_price_incl_vat=False,
    ))
    yield result
    try:
        await qondor_client.offer.delete(result.id)
    except Exception:
        # Cleanup is best-effort; log but don't fail the test session
        logger.warning("teardown cleanup failed", exc_info=True)


@pytest_asyncio.fixture(scope="session")
async def created_product_group(created_offer, qondor_client: QondorClient):
    """Create a product group on the offer; delete on teardown."""
    ref = unique_ref()
    result = await qondor_client.product_group.create(CreateProductGroup(
        offer_id=created_offer.id,
        name="IntTest Group",
        position=1,
        introduction="Group intro",
        description="Group description",
        external_reference=ref,
        offer_design_template=1,
        hide_all_products=False,
        must_select_all_products=False,
        hide_product_prices=False,
        show_total_price_for_group=True,
        show_total_price_per_person=False,
        number_of_persons_in_total_price=10,
        hide_price_table=False,
        custom_total_row_text="Total",
        name_on_invoice="IntTest Group Invoice",
        hide_feedback_on_offer=False,
    ))
    yield result
    try:
        await qondor_client.product_group.delete(result.id)
    except Exception:
        # Cleanup is best-effort; log but don't fail the test session
        logger.warning("teardown cleanup failed", exc_info=True)


@pytest_asyncio.fixture(scope="session")
async def created_product(
    created_offer,
    created_product_group,
    created_supplier,
    qondor_client: QondorClient,
):
    """Create a product; delete on teardown."""
    ref = unique_ref()
    result = await qondor_client.product.create(CreateProduct(
        name="IntTest Product",
        offer_id=created_offer.id,
        product_group_id=created_product_group.id,
        supplier_id=created_supplier.id,
        offer_quantity=5,
        external_reference=ref,
        product_type=1,
        offer_intro_text="Product intro",
        offer_description="Product description",
        offer_terms_and_conditions_text="Product T&C",
        name_on_invoice="IntTest Product Inv",
        name_on_offer="IntTest Product Offer",
        supplier_specified=True,
        supplier_invoice_reference="SUP-INV-001",
        is_published_on_offer=True,
        is_mandatory_on_offer=False,
        hide_feedback_on_offer=False,
        commission_percent=10.0,
        billing_model=0,
        initial_rate=500.0,
        is_initial_rate_incl_vat=False,
    ))
    yield result
    try:
        await qondor_client.product.delete(result.id)
    except Exception:
        # Cleanup is best-effort; log but don't fail the test session
        logger.warning("teardown cleanup failed", exc_info=True)
