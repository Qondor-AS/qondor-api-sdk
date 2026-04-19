from __future__ import annotations

from .._base import ApiModel
from .enums import ISO4217CurrencyCode, OfferProductAnswer, ToBePaidBy

__all__ = ["OfferSalesStatistics"]


class OfferSalesStatistics(ApiModel):
    price_id: int | None = None
    office_id: int | None = None
    project_id: int | None = None
    project_no: str | None = None
    project_name: str | None = None
    project_status: int | None = None
    project_status_text: str | None = None
    project_confirmation_date: str | None = None
    project_finished_date: str | None = None
    project_departure_date: str | None = None
    project_return_date: str | None = None
    project_start_date: str | None = None
    project_end_date: str | None = None
    project_location_country_code: str | None = None
    offer_id: int | None = None
    offer_name: str | None = None
    is_main_offer: bool | None = None
    is_offer_published: bool | None = None
    offer_status: int | None = None
    offer_status_text: str | None = None
    product_name: str | None = None
    product_start_date: str | None = None
    product_end_date: str | None = None
    is_product_published: bool | None = None
    offer_answer: OfferProductAnswer | None = None
    offer_answer_text: str | None = None
    probability_percentage: int | None = None
    offer_quantity: float | None = None
    referral: bool | None = None
    in_price_excl_vat: float | None = None
    out_price_excl_vat: float | None = None
    vat_amount: float | None = None
    currency: str | None = None
    currency_code: ISO4217CurrencyCode | None = None
    article_number: str | None = None
    vat_percentage: float | None = None
    vat_percentage_fee: float | None = None
    supplier_id: int | None = None
    supplier_name: str | None = None
    supplier_number: str | None = None
    supplier_chain_or_brand_deprecated: str | None = None
    supplier_chain: str | None = None
    supplier_brand: str | None = None
    supplier_external_reference: str | None = None
    supplier_category_id: int | None = None
    supplier_category_name: str | None = None
    supplier_price: float | None = None
    supplier_currency: str | None = None
    supplier_currency_code: ISO4217CurrencyCode | None = None
    product_category_name: str | None = None
    product_category_external_reference: str | None = None
    last_modified_date: str | None = None
    is_deleted: bool | None = None
    to_be_paid_by: ToBePaidBy | None = None
    to_be_paid_by_text: str | None = None
    product_id: int | None = None
