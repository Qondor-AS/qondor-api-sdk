from __future__ import annotations

from pydantic import Field

from .._base import ApiModel
from .enums import BillingModel, DesignTemplate, ISO4217CurrencyCode, OfferProductAnswer
from .offer import OfferImageOut
from .product import ProductPriceOut

__all__ = [
    "AccommodationProductDetails",
    "AccommodationProductSummary",
    "AccommodationRoomDetails",
    "AccommodationRoomNightDetails",
    "AccommodationRoomNightPrice",
    "CreateAccommodationProduct",
    "CreateAccommodationRoom",
    "CreateAccommodationRoomNight",
    "UpdateAccommodationProduct",
    "UpdateAccommodationRoom",
    "UpdateAccommodationRoomNight",
]


class CreateAccommodationProduct(ApiModel):
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
    supplier_invoice_reference: str | None = None
    product_category_id: int | None = None
    product_category_external_reference: str | None = None
    is_published_on_offer: bool | None = None
    is_mandatory_on_offer: bool | None = None
    hide_feedback_on_offer: bool | None = None
    foreign_in_price_offer_currency_id: int | None = None
    foreign_in_price_offer_currency_external_reference: str | None = None


class UpdateAccommodationProduct(ApiModel):
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
    supplier_invoice_reference: str | None = None
    product_category_id: int | None = None
    product_category_external_reference: str | None = None
    is_published_on_offer: bool | None = None
    is_mandatory_on_offer: bool | None = None
    hide_feedback_on_offer: bool | None = None
    foreign_in_price_offer_currency_id: int | None = None
    foreign_in_price_offer_currency_external_reference: str | None = None


class CreateAccommodationRoom(ApiModel):
    external_reference: str | None = None
    accommodation_product_id: int | None = None
    accommodation_product_external_reference: str | None = None
    name: str | None = None
    guests_per_room: int | None = None
    billing_model: BillingModel | None = None
    referral: bool | None = None
    commission_percent: float | None = None
    is_initial_rate_incl_vat: bool | None = None


class UpdateAccommodationRoom(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    accommodation_product_id: int | None = None
    accommodation_product_external_reference: str | None = None
    name: str | None = None
    guests_per_room: int | None = None
    billing_model: BillingModel | None = None
    referral: bool | None = None
    commission_percent: float | None = None
    is_initial_rate_incl_vat: bool | None = None


class AccommodationRoomNightPrice(ApiModel):
    art_no: str | None = None
    in_price_excl_vat: float | None = None
    in_price_incl_vat: float | None = None
    out_price_excl_vat: float | None = None
    out_price_incl_vat: float | None = None
    foreign_in_price: float | None = None


class CreateAccommodationRoomNight(ApiModel):
    external_reference: str | None = None
    room_id: int | None = None
    room_external_reference: str | None = None
    accommodation_product_id: int | None = None
    accommodation_product_external_reference: str | None = None
    check_in_date: str | None = None
    allotment: int | None = Field(default=None, alias="numberOfRooms")
    initial_rate: float | None = None
    prices: list[AccommodationRoomNightPrice] | None = None


class UpdateAccommodationRoomNight(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    room_id: int | None = None
    room_external_reference: str | None = None
    accommodation_product_id: int | None = None
    accommodation_product_external_reference: str | None = None
    check_in_date: str | None = None
    allotment: int | None = Field(default=None, alias="numberOfRooms")
    initial_rate: float | None = None
    prices: list[AccommodationRoomNightPrice] | None = None


class AccommodationRoomNightDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    allotment: int | None = Field(default=None, alias="numberOfRooms")
    initial_rate: float | None = None
    date: str | None = None
    prices: list[ProductPriceOut] | None = None


class AccommodationRoomDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    position: int | None = None
    guests_per_room: int | None = None
    billing_model: BillingModel | None = None
    billing_model_text: str | None = None
    referral: bool | None = None
    commission_percent: float | None = None
    is_initial_rate_incl_vat: bool | None = None
    nights: list[AccommodationRoomNightDetails] | None = None


class AccommodationProductDetails(ApiModel):
    id: int | None = None
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
    offer_currency_id: int | None = None
    offer_currency_external_reference: str | None = None
    foreign_in_price_currency: ISO4217CurrencyCode | None = None
    foreign_in_price_currency_code: str | None = None
    rooms: list[AccommodationRoomDetails] | None = None


class AccommodationProductSummary(AccommodationProductDetails):
    pass
