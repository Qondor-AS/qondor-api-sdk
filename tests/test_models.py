"""Tests for Pydantic model serialization, deserialization, and spec quirks."""

from __future__ import annotations

from qondor_api_sdk.models.customer import CustomerDetails, CustomerSummary
from qondor_api_sdk.models.enums import (
    AccommodationOfferPriceType,
    DesignTemplate,
    ISO4217CurrencyCode,
    OfferStatus,
    ProjectStatus,
)
from qondor_api_sdk.models.offer import CreateOffer, OfferDetails
from qondor_api_sdk.models.product import AddPrice, ProductDetails
from qondor_api_sdk.models.product_group import CreateProductGroup, ProductGroupDetails
from qondor_api_sdk.models.project import CreateProject


class TestCamelCaseSerialization:
    def test_create_project_serializes_to_camel_case(self):
        project = CreateProject(office_id=1, name="Annual Conference", pax=200)
        data = project.model_dump(by_alias=True, exclude_none=True)
        assert data == {"officeId": 1, "name": "Annual Conference", "pax": 200}

    def test_create_offer_serializes_to_camel_case(self):
        offer = CreateOffer(
            project_id=42,
            heading="Conference Offer",
            default_margin=15.0,
            status=OfferStatus.NOT_SENT,
        )
        data = offer.model_dump(by_alias=True, exclude_none=True)
        assert data["projectId"] == 42
        assert data["heading"] == "Conference Offer"
        assert data["defaultMargin"] == 15.0
        assert data["status"] == 1

    def test_create_product_group_serializes_to_camel_case(self):
        pg = CreateProductGroup(
            offer_id=10,
            name="Accommodation",
            position=1,
            offer_design_template=DesignTemplate.IMAGE_LEFT_TEXT_RIGHT,
        )
        data = pg.model_dump(by_alias=True, exclude_none=True)
        assert data["offerId"] == 10
        assert data["name"] == "Accommodation"
        assert data["position"] == 1
        assert data["offerDesignTemplate"] == 1

    def test_add_price_serializes_defaults(self):
        price = AddPrice(product_id=5, out_price_excl_vat=1500.0, out_price_incl_vat=1875.0)
        data = price.model_dump(by_alias=True, exclude_none=True)
        assert data["productId"] == 5
        assert data["outPriceExclVat"] == 1500.0
        assert data["outPriceInclVat"] == 1875.0


class TestDeserialization:
    def test_customer_details_from_api_json(self):
        api_response = {
            "id": 123,
            "name": "Berg Hansen",
            "officeId": 1,
            "city": "Oslo",
            "isActive": True,
            "invoiceCurrencyCode": 578,
            "contactPersons": [
                {"id": 10, "firstName": "Maria", "lastName": "Hansen", "email": "maria@example.com"}
            ],
        }
        customer = CustomerDetails.model_validate(api_response)
        assert customer.id == 123
        assert customer.name == "Berg Hansen"
        assert customer.office_id == 1
        assert customer.is_active is True
        assert customer.invoice_currency_code == ISO4217CurrencyCode.NOK
        assert customer.contact_persons is not None
        assert len(customer.contact_persons) == 1

    def test_offer_details_from_api_json(self):
        api_response = {
            "id": 789,
            "heading": "Annual Conference 2026",
            "status": 1,
            "statusText": "Not Sent",
            "projectId": 42,
            "defaultMargin": 15.0,
            "displayPricesExclVat": True,
            "displayPricesInclVat": False,
            "displayTotalOfferPrice": True,
            "displayTotalPriceColumn": False,
            "displayTotalPriceInclVat": False,
            "displayVatAmount": False,
            "hideVatTextFromPrices": False,
            "includeOfficeTermsAndConditions": False,
            "disableUnsureAnswerOnProductsAndGroups": False,
            "isPublished": False,
            "isMainOffer": True,
            "accommodationOfferPriceType": 1,
            "lastEditedDate": "2026-04-01T10:00:00Z",
            "lastEditedDateUtc": "2026-04-01T10:00:00Z",
            "offerLocation": {"displayText": "Oslo", "location": None},
        }
        offer = OfferDetails.model_validate(api_response)
        assert offer.id == 789
        assert offer.heading == "Annual Conference 2026"
        assert offer.status == OfferStatus.NOT_SENT
        assert offer.project_id == 42
        assert offer.default_margin == 15.0
        assert offer.accommodation_offer_price_type == AccommodationOfferPriceType.DISPLAY_PRICE_PER_PERSON_PER_NIGHT

    def test_product_details_with_prices(self):
        api_response = {
            "id": 50,
            "name": "Grand Hotel Room",
            "productType": 1,
            "offerId": 789,
            "offerQuantity": 200.0,
            "isPublishedOnOffer": True,
            "billingModel": 1,
            "commissionPercent": 10.0,
            "prices": [
                {
                    "id": 100,
                    "outPriceExclVat": 1500.0,
                    "outPriceInclVat": 1875.0,
                    "inPriceExclVat": 1200.0,
                    "inPriceInclVat": 1500.0,
                    "vatPercentage": 25.0,
                    "vatPercentageFee": 0.0,
                    "isValidFrom": "2026-01-01T00:00:00Z",
                }
            ],
        }
        product = ProductDetails.model_validate(api_response)
        assert product.id == 50
        assert product.prices is not None
        assert len(product.prices) == 1
        assert product.prices[0].out_price_excl_vat == 1500.0

    def test_product_group_details_from_api(self):
        api_response = {
            "id": 20,
            "offerId": 789,
            "position": 1,
            "heading": "Accommodation",
            "offerDesignTemplate": 1,
            "hideAllProducts": False,
            "hideProductPrices": False,
            "allProductsAreRequired": False,
            "showPackagePrice": False,
            "showTotalPricePerPerson": False,
            "hidePriceTableOnOffer": False,
            "hideFeedbackOnOffer": False,
            "offerProjectId": 42,
        }
        pg = ProductGroupDetails.model_validate(api_response)
        assert pg.id == 20
        assert pg.heading == "Accommodation"
        assert pg.offer_design_template == DesignTemplate.IMAGE_LEFT_TEXT_RIGHT


class TestSpecQuirks:
    def test_customer_summary_office_id_is_int(self):
        """CustomerSummaryContract.officeId is typed as string in spec but should be int."""
        data = {"id": 1, "officeId": 5, "name": "Test", "isActive": True}
        summary = CustomerSummary.model_validate(data)
        assert summary.office_id == 5
        assert isinstance(summary.office_id, int)

    def test_customer_summary_office_id_none(self):
        data = {"id": 1, "name": "Test", "isActive": True}
        summary = CustomerSummary.model_validate(data)
        assert summary.office_id is None


class TestEnumValues:
    def test_offer_status_values(self):
        assert OfferStatus.NOT_SENT == 1
        assert OfferStatus.SENT == 2
        assert OfferStatus.CONFIRMED == 3
        assert OfferStatus.DECLINED == 4

    def test_project_status_values(self):
        assert ProjectStatus.PENDING == 1
        assert ProjectStatus.CONFIRMED == 2
        assert ProjectStatus.FINISHED == 3
        assert ProjectStatus.CANCELLED == 4

    def test_design_template_values(self):
        assert DesignTemplate.IMAGE_LEFT_TEXT_RIGHT == 1
        assert DesignTemplate.IMAGE_TOP_TEXT_BOTTOM == 2
        assert DesignTemplate.IMAGE_RIGHT_TEXT_LEFT == 6
        assert DesignTemplate.THREE_IMAGES_TOP_TEXT_BOTTOM == 7
        assert DesignTemplate.IMAGE_SLIDER_TOP_TEXT_BOTTOM == 8

    def test_iso4217_common_currencies(self):
        assert ISO4217CurrencyCode.NOK == 578
        assert ISO4217CurrencyCode.EUR == 978
        assert ISO4217CurrencyCode.USD == 840
        assert ISO4217CurrencyCode.GBP == 826
        assert ISO4217CurrencyCode.SEK == 752
        assert ISO4217CurrencyCode.DKK == 208
