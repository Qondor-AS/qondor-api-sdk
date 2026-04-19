from __future__ import annotations

from .._base import ApiModel
from .enums import DesignTemplate

__all__ = [
    "CreateProductGroup",
    "UpdateProductGroup",
    "ProductGroupDetails",
    "ProductGroupSummary",
]


class CreateProductGroup(ApiModel):
    offer_id: int | None = None
    offer_external_reference: str | None = None
    external_reference: str | None = None
    position: int | None = None
    name: str | None = None
    introduction: str | None = None
    description: str | None = None
    offer_design_template: DesignTemplate | None = None
    hide_all_products: bool | None = None
    must_select_all_products: bool | None = None
    hide_product_prices: bool | None = None
    show_total_price_for_group: bool | None = None
    show_total_price_per_person: bool | None = None
    number_of_persons_in_total_price: int | None = None
    hide_price_table: bool | None = None
    custom_total_row_text: str | None = None
    name_on_invoice: str | None = None
    hide_feedback_on_offer: bool | None = None


class UpdateProductGroup(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    position: int | None = None
    name: str | None = None
    introduction: str | None = None
    description: str | None = None
    offer_design_template: DesignTemplate | None = None
    hide_all_products: bool | None = None
    must_select_all_products: bool | None = None
    hide_product_prices: bool | None = None
    show_total_price_for_group: bool | None = None
    show_total_price_per_person: bool | None = None
    number_of_persons_in_total_price: int | None = None
    hide_price_table: bool | None = None
    custom_total_row_text: str | None = None
    name_on_invoice: str | None = None
    hide_feedback_on_offer: bool | None = None


class ProductGroupDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    offer_project_id: int | None = None
    offer_id: int | None = None
    position: int | None = None
    heading: str | None = None
    intro: str | None = None
    description: str | None = None
    offer_design_template: DesignTemplate | None = None
    offer_design_template_text: str | None = None
    hide_all_products: bool | None = None
    all_products_are_required: bool | None = None
    hide_product_prices: bool | None = None
    show_package_price: bool | None = None
    show_total_price_per_person: bool | None = None
    number_of_persons_in_total_price: int | None = None
    hide_price_table_on_offer: bool | None = None
    custom_total_row_text: str | None = None
    invoice_text: str | None = None
    hide_feedback_on_offer: bool | None = None


class ProductGroupSummary(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    offer_project_id: int | None = None
    offer_id: int | None = None
    position: int | None = None
    heading: str | None = None
    intro: str | None = None
    description: str | None = None
    offer_design_template: DesignTemplate | None = None
    offer_design_template_text: str | None = None
    hide_all_products: bool | None = None
    all_products_are_required: bool | None = None
    hide_product_prices: bool | None = None
    show_package_price: bool | None = None
    show_total_price_per_person: bool | None = None
    number_of_persons_in_total_price: int | None = None
    hide_price_table_on_offer: bool | None = None
    custom_total_row_text: str | None = None
    invoice_text: str | None = None
    hide_feedback_on_offer: bool | None = None
