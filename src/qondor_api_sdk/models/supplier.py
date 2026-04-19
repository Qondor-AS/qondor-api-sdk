from __future__ import annotations

from .._base import ApiModel
from .contact_person import SupplierContactPerson
from .enums import SupplierStatus

__all__ = [
    "CreateSupplier",
    "UpdateSupplier",
    "SupplierDetails",
    "SupplierSummary",
]


class CreateSupplier(ApiModel):
    office_id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    email: str | None = None
    address: str | None = None
    address2: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country_code: str | None = None
    organisation_number: str | None = None
    vat_number: str | None = None
    phone_number: str | None = None
    fax_number: str | None = None
    status: SupplierStatus | None = None
    chain: str | None = None
    brand: str | None = None
    supplier_number: str | None = None
    is_internal_supplier: bool | None = None
    invoice_address_enabled: bool | None = None
    invoice_address: str | None = None
    invoice_address2: str | None = None
    invoice_zip_code: str | None = None
    invoice_city: str | None = None
    invoice_country_code: str | None = None
    invoice_additional_information: str | None = None
    supplier_category_id: int | None = None
    remarks: str | None = None


class UpdateSupplier(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    email: str | None = None
    address: str | None = None
    address2: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country_code: str | None = None
    organisation_number: str | None = None
    vat_number: str | None = None
    phone_number: str | None = None
    fax_number: str | None = None
    status: SupplierStatus | None = None
    chain: str | None = None
    brand: str | None = None
    supplier_number: str | None = None
    is_internal_supplier: bool | None = None
    invoice_address_enabled: bool | None = None
    invoice_address: str | None = None
    invoice_address2: str | None = None
    invoice_zip_code: str | None = None
    invoice_city: str | None = None
    invoice_country_code: str | None = None
    invoice_additional_information: str | None = None
    supplier_category_id: int | None = None
    remarks: str | None = None


class SupplierDetails(ApiModel):
    id: int | None = None
    office_id: int | None = None
    name: str | None = None
    external_reference: str | None = None
    status: int | None = None
    status_text: str | None = None
    chain: str | None = None
    brand: str | None = None
    email: str | None = None
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
    supplier_number: str | None = None
    is_internal_supplier: bool | None = None
    invoice_address_enabled: bool | None = None
    invoice_address: str | None = None
    invoice_address2: str | None = None
    invoice_zip_code: str | None = None
    invoice_city: str | None = None
    invoice_country: str | None = None
    invoice_country_code: str | None = None
    invoice_additional_information: str | None = None
    remarks: str | None = None
    supplier_category_id: int | None = None
    supplier_category_name: str | None = None
    contact_persons: list[SupplierContactPerson] | None = None
    last_modified_date_utc: str | None = None


class SupplierSummary(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    name: str | None = None
    email: str | None = None
    organisation_number: str | None = None
    city: str | None = None
    country: str | None = None
    country_code: str | None = None
    supplier_number: str | None = None
    office_id: int | None = None
    category_id: int | None = None
    category_name: str | None = None
    chain: str | None = None
    brand: str | None = None
    last_modified_date_utc: str | None = None
