from __future__ import annotations

from .._base import ApiModel
from .enums import (
    AccommodationOfferPriceType,
    ISO4217CurrencyCode,
    LocationCodeScheme,
    LocationCodeType,
    LocationTypeDEPRECATED,
    OfferStatus,
)

__all__ = [
    "AddCurrencyToOffer",
    "Country",
    "Location",
    "OfferImageOut",
    "OfferLocation",
    "CreateOffer",
    "UpdateOffer",
    "UpdateOfferCurrency",
    "OfferCurrencyDetails",
    "OfferDetails",
    "OfferSummary",
]


class AddCurrencyToOffer(ApiModel):
    offer_id: int | None = None
    offer_external_reference: str | None = None
    external_reference: str | None = None
    currency_code: str | None = None
    exchange_rate: float | None = None
    date: str | None = None


class Country(ApiModel):
    name: str | None = None
    two_letter_iso_name: str | None = None


class Location(ApiModel):
    name: str | None = None
    code: str | None = None
    type: LocationTypeDEPRECATED | None = None
    type_text: str | None = None
    code_scheme: LocationCodeScheme | None = None
    code_scheme_text: str | None = None
    code_type: LocationCodeType | None = None
    code_type_text: str | None = None
    country: Country | None = None


class OfferImageOut(ApiModel):
    file_id: str | None = None


class OfferLocation(ApiModel):
    display_text: str | None = None
    location: Location | None = None


class CreateOffer(ApiModel):
    project_id: int | None = None
    project_no: str | None = None
    heading: str | None = None
    external_reference: str | None = None
    is_main_offer: bool | None = None
    default_margin: float | None = None
    disable_unsure_answer_on_products_and_groups: bool | None = None
    display_total_offer_price: bool | None = None
    accommodation_offer_price_type: AccommodationOfferPriceType | None = None
    confirmation_page_content: str | None = None
    include_office_terms_and_conditions: bool | None = None
    confirmation_page_header: str | None = None
    terms_and_conditions_text: str | None = None
    status: OfferStatus | None = None
    email_confirmation_template_body: str | None = None
    email_confirmation_template_subject: str | None = None
    use_office_settings: bool | None = None
    display_prices_excl_vat: bool | None = None
    display_prices_incl_vat: bool | None = None
    display_vat_amount: bool | None = None
    hide_vat_text_from_prices: bool | None = None
    display_total_price_column: bool | None = None
    display_total_price_incl_vat: bool | None = None
    description: str | None = None
    offer_valid_until_utc: str | None = None
    location_code: str | None = None
    location_display_text: str | None = None


class UpdateOffer(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    heading: str | None = None
    is_main_offer: bool | None = None
    default_margin: float | None = None
    disable_unsure_answer_on_products_and_groups: bool | None = None
    display_total_offer_price: bool | None = None
    accommodation_offer_price_type: AccommodationOfferPriceType | None = None
    confirmation_page_content: str | None = None
    include_office_terms_and_conditions: bool | None = None
    confirmation_page_header: str | None = None
    terms_and_conditions_text: str | None = None
    status: OfferStatus | None = None
    email_confirmation_template_body: str | None = None
    email_confirmation_template_subject: str | None = None
    use_office_settings: bool | None = None
    display_prices_excl_vat: bool | None = None
    display_prices_incl_vat: bool | None = None
    display_vat_amount: bool | None = None
    hide_vat_text_from_prices: bool | None = None
    display_total_price_column: bool | None = None
    display_total_price_incl_vat: bool | None = None
    description: str | None = None
    offer_valid_until_utc: str | None = None
    location_code: str | None = None
    location_display_text: str | None = None


class UpdateOfferCurrency(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    offer_id: int | None = None
    offer_external_reference: str | None = None
    exchange_rate: float | None = None
    date_utc: str | None = None
    recalculate_out_prices: bool | None = None


class OfferCurrencyDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    offer_id: int | None = None
    currency_code: ISO4217CurrencyCode | None = None
    currency_code_text: str | None = None
    exchange_rate: float | None = None
    date: str | None = None


class OfferDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    description: str | None = None
    disable_unsure_answer_on_products_and_groups: bool | None = None
    accommodation_offer_price_type: AccommodationOfferPriceType | None = None
    accommodation_offer_price_type_text: str | None = None
    display_prices_excl_vat: bool | None = None
    display_prices_incl_vat: bool | None = None
    display_total_offer_price: bool | None = None
    display_total_price_column: bool | None = None
    display_total_price_incl_vat: bool | None = None
    display_vat_amount: bool | None = None
    hide_vat_text_from_prices: bool | None = None
    email_confirmation_template_subject: str | None = None
    email_confirmation_template_body: str | None = None
    confirmation_page_content: str | None = None
    heading: str | None = None
    include_office_terms_and_conditions: bool | None = None
    is_published: bool | None = None
    is_main_offer: bool | None = None
    last_sent_utc: str | None = None
    last_viewed_utc: str | None = None
    offer_valid_until_utc: str | None = None
    last_edited_date: str | None = None
    last_edited_date_utc: str | None = None
    status: OfferStatus | None = None
    status_text: str | None = None
    use_office_settings: bool | None = None
    terms_and_conditions_text: str | None = None
    terms_and_conditions_file_id: str | None = None
    project_id: int | None = None
    project_name: str | None = None
    project_project_no: str | None = None
    project_main_offer_id: int | None = None
    default_margin: float | None = None
    offer_location: OfferLocation | None = None
    offer_currencies: list[OfferCurrencyDetails] | None = None


class OfferSummary(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    description: str | None = None
    disable_unsure_answer_on_products_and_groups: bool | None = None
    accommodation_offer_price_type: AccommodationOfferPriceType | None = None
    accommodation_offer_price_type_text: str | None = None
    display_prices_excl_vat: bool | None = None
    display_prices_incl_vat: bool | None = None
    display_total_offer_price: bool | None = None
    display_total_price_column: bool | None = None
    display_total_price_incl_vat: bool | None = None
    display_vat_amount: bool | None = None
    hide_vat_text_from_prices: bool | None = None
    email_confirmation_template_subject: str | None = None
    email_confirmation_template_body: str | None = None
    confirmation_page_content: str | None = None
    heading: str | None = None
    include_office_terms_and_conditions: bool | None = None
    is_published: bool | None = None
    is_main_offer: bool | None = None
    last_sent_utc: str | None = None
    last_viewed_utc: str | None = None
    offer_valid_until_utc: str | None = None
    last_edited_date: str | None = None
    last_edited_date_utc: str | None = None
    status: OfferStatus | None = None
    status_text: str | None = None
    use_office_settings: bool | None = None
    terms_and_conditions_text: str | None = None
    terms_and_conditions_file_id: str | None = None
    project_id: int | None = None
    project_name: str | None = None
    project_project_no: str | None = None
    project_main_offer_id: int | None = None
    default_margin: float | None = None
    offer_location: OfferLocation | None = None
