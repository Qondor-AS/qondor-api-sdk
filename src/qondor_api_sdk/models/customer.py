from __future__ import annotations

from .._base import ApiModel
from .contact_person import CustomerContactPersonsDetails
from .enums import CustomFieldDataType, ISO4217CurrencyCode

__all__ = [
    "CustomerCategory",
    "CustomerCustomFieldAnswerIn",
    "CustomerInvoiceFieldAlternativeForCustomerIn",
    "CustomerInvoiceFieldForCustomerIn",
    "CustomerOwner",
    "CreateCustomer",
    "UpdateCustomer",
    "CustomerCustomFieldAnswerDetails",
    "CustomerDetails",
    "CustomerInvoiceFieldAlternativeDetails",
    "CustomerInvoiceFieldDetails",
    "CustomerSummary",
]


class CustomerCategory(ApiModel):
    id: int | None = None
    name: str | None = None


class CustomerCustomFieldAnswerIn(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    answer: str | None = None


class CustomerInvoiceFieldAlternativeForCustomerIn(ApiModel):
    value: str | None = None


class CustomerInvoiceFieldForCustomerIn(ApiModel):
    description: str | None = None
    heading: str | None = None
    external_reference: str | None = None
    allowed_values: list[CustomerInvoiceFieldAlternativeForCustomerIn] | None = None
    id: int | None = None
    is_required: bool | None = None


class CustomerOwner(ApiModel):
    full_name: str | None = None
    email: str | None = None


class CreateCustomer(ApiModel):
    office_id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    legal_name: str | None = None
    address: str | None = None
    address2: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country_code: str | None = None
    organisation_number: str | None = None
    vat_number: str | None = None
    phone_number: str | None = None
    fax_number: str | None = None
    customer_number: str | None = None
    is_invoiceable: bool | None = None
    invoice_currency: str | None = None
    invoice_currency_code: ISO4217CurrencyCode | None = None
    invoice_address_enabled: bool | None = None
    invoice_address: str | None = None
    invoice_address2: str | None = None
    invoice_zip_code: str | None = None
    invoice_city: str | None = None
    invoice_country_code: str | None = None
    invoice_additional_information: str | None = None
    customer_fields: list[CustomerInvoiceFieldForCustomerIn] | None = None
    customer_invoice_fields: list[CustomerInvoiceFieldForCustomerIn] | None = None
    customer_category_id: int | None = None
    is_active: bool | None = None
    customer_custom_field_answers: list[CustomerCustomFieldAnswerIn] | None = None
    invoice_email: str | None = None
    remarks: str | None = None


class UpdateCustomer(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    legal_name: str | None = None
    address: str | None = None
    address2: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country_code: str | None = None
    organisation_number: str | None = None
    vat_number: str | None = None
    phone_number: str | None = None
    fax_number: str | None = None
    customer_number: str | None = None
    is_invoiceable: bool | None = None
    invoice_currency: str | None = None
    invoice_currency_code: ISO4217CurrencyCode | None = None
    invoice_address_enabled: bool | None = None
    invoice_address: str | None = None
    invoice_address2: str | None = None
    invoice_zip_code: str | None = None
    invoice_city: str | None = None
    invoice_country_code: str | None = None
    invoice_additional_information: str | None = None
    customer_fields: list[CustomerInvoiceFieldForCustomerIn] | None = None
    customer_invoice_fields: list[CustomerInvoiceFieldForCustomerIn] | None = None
    customer_category_id: int | None = None
    is_active: bool | None = None
    customer_custom_field_answers: list[CustomerCustomFieldAnswerIn] | None = None
    invoice_email: str | None = None
    remarks: str | None = None


class CustomerCustomFieldAnswerDetails(ApiModel):
    heading: str | None = None
    answer: str | None = None
    external_reference: str | None = None
    data_type: CustomFieldDataType | None = None
    data_type_text: str | None = None


class CustomerDetails(ApiModel):
    id: int | None = None
    office_id: int | None = None
    name: str | None = None
    legal_name: str | None = None
    external_reference: str | None = None
    address: str | None = None
    address2: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country: str | None = None
    country_code: str | None = None
    organisation_number: str | None = None
    vat_number: str | None = None
    phone_number: str | None = None
    fax_number: str | None = None
    customer_number: str | None = None
    is_invoiceable: bool | None = None
    invoice_currency: str | None = None
    invoice_currency_code: ISO4217CurrencyCode | None = None
    invoice_address_enabled: bool | None = None
    invoice_address: str | None = None
    invoice_address2: str | None = None
    invoice_zip_code: str | None = None
    invoice_city: str | None = None
    invoice_country: str | None = None
    invoice_country_code: str | None = None
    invoice_additional_information: str | None = None
    customer_invoice_fields_deprecated: list[CustomerInvoiceFieldDetails] | None = None
    customer_invoice_fields: list[CustomerInvoiceFieldDetails] | None = None
    customer_category_id: int | None = None
    customer_category_name: str | None = None
    customer_owner: CustomerOwner | None = None
    contact_persons: list[CustomerContactPersonsDetails] | None = None
    is_active: bool | None = None
    customer_custom_field_answers: list[CustomerCustomFieldAnswerDetails] | None = None
    invoice_email: str | None = None
    remarks: str | None = None


class CustomerInvoiceFieldAlternativeDetails(ApiModel):
    id: int | None = None
    value: str | None = None


class CustomerInvoiceFieldDetails(ApiModel):
    id: int | None = None
    heading: str | None = None
    description: str | None = None
    external_reference: str | None = None
    is_required: bool | None = None
    allowed_values: list[CustomerInvoiceFieldAlternativeDetails] | None = None


class CustomerSummary(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    organisation_number: str | None = None
    city: str | None = None
    customer_number: str | None = None
    office_id: int | None = None
    category_id: int | None = None
    category_name: str | None = None
    is_active: bool | None = None
    custom_field_customer_answers: list[CustomerCustomFieldAnswerDetails] | None = None
    invoice_email: str | None = None
