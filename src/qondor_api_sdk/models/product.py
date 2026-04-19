from __future__ import annotations

from .._base import ApiModel
from .enums import (
    BillingModel,
    DesignTemplate,
    FlightClass,
    ISO4217CurrencyCode,
    OfferProductAnswer,
    ProductApiProductType,
    TripMode,
)
from .offer import OfferImageOut

__all__ = [
    "AddPrice",
    "AttachTicketToTransportProduct",
    "ConfirmProduct",
    "ProductPriceOut",
    "CreateProduct",
    "UpdatePrice",
    "UpdateProduct",
    "ProductDetails",
    "ProductTicketDetails",
    "ProductSummary",
    "ProductTicketSummary",
]


class AddPrice(ApiModel):
    external_reference: str | None = None
    product_id: int | None = None
    product_external_reference: str | None = None
    art_no: str | None = None
    in_price_excl_vat: float | None = None
    in_price_incl_vat: float | None = None
    out_price_excl_vat: float | None = None
    out_price_incl_vat: float | None = None
    foreign_in_price: float | None = None
    foreign_in_price_offer_currency_id: int | None = None
    foreign_in_price_offer_currency_external_reference: str | None = None


class AttachTicketToTransportProduct(ApiModel):
    transport_product_id: int | None = None
    transport_product_external_reference: str | None = None
    ticket_id: int | None = None
    ticket_external_reference: str | None = None


class ConfirmProduct(ApiModel):
    product_id: int | None = None
    product_external_reference: str | None = None


class ProductPriceOut(ApiModel):
    id: int | None = None
    art_no: str | None = None
    is_valid_from: str | None = None
    in_price_excl_vat: float | None = None
    in_price_incl_vat: float | None = None
    out_price_excl_vat: float | None = None
    out_price_incl_vat: float | None = None
    foreign_in_price: float | None = None
    vat_percentage: float | None = None
    vat_percentage_fee: float | None = None


class CreateProduct(ApiModel):
    product_type: ProductApiProductType | None = None
    name: str | None = None
    external_reference: str | None = None
    offer_id: int | None = None
    offer_external_reference: str | None = None
    product_group_id: int | None = None
    product_group_external_reference: str | None = None
    offer_intro_text: str | None = None
    offer_description: str | None = None
    offer_quantity: float | None = None
    offer_terms_and_conditions_text: str | None = None
    name_on_invoice: str | None = None
    name_on_offer: str | None = None
    supplier_id: int | None = None
    supplier_external_reference: str | None = None
    supplier_specified: bool | None = None
    supplier_invoice_reference: str | None = None
    product_category_id: int | None = None
    product_category_external_reference: str | None = None
    product_category_specified: bool | None = None
    is_published_on_offer: bool | None = None
    is_mandatory_on_offer: bool | None = None
    hide_feedback_on_offer: bool | None = None
    commission_percent: float | None = None
    billing_model: BillingModel | None = None
    initial_rate: float | None = None
    is_initial_rate_incl_vat: bool | None = None


class UpdatePrice(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    product_id: int | None = None
    product_external_reference: str | None = None
    art_no: str | None = None
    in_price_excl_vat: float | None = None
    in_price_incl_vat: float | None = None
    out_price_excl_vat: float | None = None
    out_price_incl_vat: float | None = None
    foreign_in_price: float | None = None
    foreign_in_price_offer_currency_id: int | None = None
    foreign_in_price_offer_currency_external_reference: str | None = None


class UpdateProduct(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    product_group_id: int | None = None
    product_group_external_reference: str | None = None
    offer_intro_text: str | None = None
    offer_description: str | None = None
    offer_quantity: float | None = None
    offer_terms_and_conditions_text: str | None = None
    name_on_invoice: str | None = None
    name_on_offer: str | None = None
    supplier_id: int | None = None
    supplier_external_reference: str | None = None
    supplier_specified: bool | None = None
    supplier_invoice_reference: str | None = None
    product_category_id: int | None = None
    product_category_external_reference: str | None = None
    product_category_specified: bool | None = None
    is_published_on_offer: bool | None = None
    is_mandatory_on_offer: bool | None = None
    hide_feedback_on_offer: bool | None = None
    commission_percent: float | None = None
    billing_model: BillingModel | None = None
    initial_rate: float | None = None
    is_initial_rate_incl_vat: bool | None = None


class ProductDetails(ApiModel):
    id: int | None = None
    product_type: ProductApiProductType | None = None
    product_type_text: str | None = None
    external_reference: str | None = None
    name: str | None = None
    offer_id: int | None = None
    offer_external_reference: str | None = None
    product_group_id: int | None = None
    product_group_external_reference: str | None = None
    name_on_offer: str | None = None
    name_on_invoice: str | None = None
    enable_offer_configuration: bool | None = None
    is_published_on_offer: bool | None = None
    offer_intro_text: str | None = None
    offer_description: str | None = None
    offer_quantity: float | None = None
    is_optional_on_offer: bool | None = None
    offer_terms_and_conditions_text: str | None = None
    offer_terms_and_conditions_file_id: str | None = None
    offer_design_template: DesignTemplate | None = None
    offer_design_template_text: str | None = None
    offer_answer: OfferProductAnswer | None = None
    offer_answer_text: str | None = None
    offer_images: list[OfferImageOut] | None = None
    product_category_id: int | None = None
    product_category_name: str | None = None
    product_category_external_reference: str | None = None
    supplier_id: int | None = None
    supplier_name: str | None = None
    supplier_external_reference: str | None = None
    billing_model: BillingModel | None = None
    billing_model_text: str | None = None
    referral: bool | None = None
    offer_currency_id: int | None = None
    offer_currency_external_reference: str | None = None
    foreign_in_price_currency: ISO4217CurrencyCode | None = None
    foreign_in_price_currency_code: str | None = None
    prices: list[ProductPriceOut] | None = None
    commission_percent: float | None = None
    initial_rate: float | None = None
    is_initial_rate_incl_vat: bool | None = None


class ProductTicketDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    transport_product_id: int | None = None
    transport_product_external_reference: str | None = None
    ticket_inbox_entry_id: int | None = None
    ticket_inbox_entry_external_reference: str | None = None
    project_id: int | None = None
    project_project_no: str | None = None
    pnr: str | None = None
    ticket_number: str | None = None
    traveller_name: str | None = None
    trip_mode: TripMode | None = None
    trip_mode_text: str | None = None
    flight_class: FlightClass | None = None
    flight_class_text: str | None = None
    fare_basis: str | None = None
    purchase_price_excl_vat: float | None = None
    purchase_price_incl_vat: float | None = None
    sales_price_excl_vat: float | None = None
    sales_price_incl_vat: float | None = None
    tax_amount: float | None = None
    vat_rate: float | None = None
    supplier_code: str | None = None
    supplier_name: str | None = None


class ProductSummary(ApiModel):
    id: int | None = None
    product_type: ProductApiProductType | None = None
    product_type_text: str | None = None
    external_reference: str | None = None
    name: str | None = None
    offer_id: int | None = None
    offer_external_reference: str | None = None
    product_group_id: int | None = None
    product_group_external_reference: str | None = None
    name_on_offer: str | None = None
    name_on_invoice: str | None = None
    enable_offer_configuration: bool | None = None
    is_published_on_offer: bool | None = None
    offer_intro_text: str | None = None
    offer_description: str | None = None
    offer_quantity: float | None = None
    is_optional_on_offer: bool | None = None
    offer_terms_and_conditions_text: str | None = None
    offer_terms_and_conditions_file_id: str | None = None
    offer_design_template: DesignTemplate | None = None
    offer_design_template_text: str | None = None
    offer_answer: OfferProductAnswer | None = None
    offer_answer_text: str | None = None
    offer_images: list[OfferImageOut] | None = None
    product_category_id: int | None = None
    product_category_name: str | None = None
    product_category_external_reference: str | None = None
    supplier_id: int | None = None
    supplier_name: str | None = None
    supplier_external_reference: str | None = None
    billing_model: BillingModel | None = None
    billing_model_text: str | None = None
    referral: bool | None = None
    offer_currency_id: int | None = None
    offer_currency_external_reference: str | None = None
    foreign_in_price_currency: ISO4217CurrencyCode | None = None
    foreign_in_price_currency_code: str | None = None
    prices: list[ProductPriceOut] | None = None
    commission_percent: float | None = None
    initial_rate: float | None = None
    is_initial_rate_incl_vat: bool | None = None


class ProductTicketSummary(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    transport_product_id: int | None = None
    transport_product_external_reference: str | None = None
    ticket_inbox_entry_id: int | None = None
    ticket_inbox_entry_external_reference: str | None = None
    project_id: int | None = None
    project_project_no: str | None = None
    pnr: str | None = None
    ticket_number: str | None = None
    traveller_name: str | None = None
    trip_mode: TripMode | None = None
    trip_mode_text: str | None = None
    flight_class: FlightClass | None = None
    flight_class_text: str | None = None
    fare_basis: str | None = None
    purchase_price_excl_vat: float | None = None
    purchase_price_incl_vat: float | None = None
    sales_price_excl_vat: float | None = None
    sales_price_incl_vat: float | None = None
    tax_amount: float | None = None
    vat_rate: float | None = None
    supplier_code: str | None = None
    supplier_name: str | None = None
