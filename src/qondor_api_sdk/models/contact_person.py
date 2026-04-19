from __future__ import annotations

from .._base import ApiModel

__all__ = [
    "SupplierContactPerson",
    "CreateContactPerson",
    "UpdateContactPerson",
    "UpdateContactPersonCustomer",
    "UpdateContactPersonSupplier",
    "CustomerContactPersonsDetails",
]


class SupplierContactPerson(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    phone2_number: str | None = None
    is_active: bool | None = None


class CreateContactPerson(ApiModel):
    phone_country_code: str | None = None
    phone_number: str | None = None
    phone_country_code2: str | None = None
    phone_number2: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    external_reference: str | None = None


class UpdateContactPerson(ApiModel):
    phone_country_code: str | None = None
    phone_number: str | None = None
    phone_country_code2: str | None = None
    phone_number2: str | None = None
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    external_reference: str | None = None


class UpdateContactPersonCustomer(ApiModel):
    contact_person_id: int | None = None
    contact_person_email: str | None = None
    contact_person_external_reference: str | None = None
    customer_id: int | None = None
    customer_external_reference: str | None = None
    is_active: bool | None = None
    delete_relation: bool | None = None


class UpdateContactPersonSupplier(ApiModel):
    contact_person_id: int | None = None
    contact_person_email: str | None = None
    contact_person_external_reference: str | None = None
    supplier_id: int | None = None
    supplier_external_reference: str | None = None
    is_active: bool | None = None
    delete_relation: bool | None = None


class CustomerContactPersonsDetails(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    phone2_number: str | None = None
    is_active: bool | None = None
