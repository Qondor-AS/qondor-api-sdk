from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.contact_person import (
    CreateContactPerson,
    CustomerContactPersonsDetails,
    UpdateContactPerson,
    UpdateContactPersonCustomer,
    UpdateContactPersonSupplier,
)


class ContactPersonModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> CustomerContactPersonsDetails:
        url = self._url(f"/ContactPerson/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return CustomerContactPersonsDetails.model_validate(resp.json())

    @_with_retry
    async def delete(self, id: int) -> None:
        url = self._url(f"/ContactPerson/{id}")
        resp = await self._http.delete(url)
        _raise_for_status(resp)

    @_with_retry
    async def get_by_email(self, email: str | None = None) -> CustomerContactPersonsDetails:
        url = self._url("/ContactPerson/GetByEmail")
        params = {"email": email}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return CustomerContactPersonsDetails.model_validate(resp.json())

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> CustomerContactPersonsDetails:
        url = self._url("/ContactPerson/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return CustomerContactPersonsDetails.model_validate(resp.json())

    @_with_retry
    async def create(self, request: CreateContactPerson) -> CustomerContactPersonsDetails:
        url = self._url("/ContactPerson")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return CustomerContactPersonsDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateContactPerson) -> None:
        url = self._url("/ContactPerson")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_email(self, email: str | None = None) -> None:
        url = self._url("/ContactPerson/DeleteByEmail")
        params = {"email": email}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_external_reference(self, external_reference: str | None = None) -> None:
        url = self._url("/ContactPerson/DeleteByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def update_customer_relation(self, request: UpdateContactPersonCustomer) -> None:
        url = self._url("/ContactPerson/UpdateCustomerRelation")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def update_supplier_relation(self, request: UpdateContactPersonSupplier) -> None:
        url = self._url("/ContactPerson/UpdateSupplierRelation")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
