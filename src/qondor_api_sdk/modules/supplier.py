from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.supplier import CreateSupplier, SupplierDetails, SupplierSummary, UpdateSupplier


class SupplierModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> SupplierDetails:
        url = self._url(f"/Supplier/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return SupplierDetails.model_validate(resp.json())

    @_with_retry
    async def delete(self, id: int) -> None:
        url = self._url(f"/Supplier/{id}")
        resp = await self._http.delete(url)
        _raise_for_status(resp)

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> SupplierDetails:
        url = self._url("/Supplier/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return SupplierDetails.model_validate(resp.json())

    @_with_retry
    async def get_all(
        self, office_id: int | None = None, last_modified_date: str | None = None,
    ) -> list[SupplierSummary]:
        url = self._url("/Supplier/GetAll")
        params = {"officeId": office_id, "lastModifiedDate": last_modified_date}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [SupplierSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def create(self, request: CreateSupplier) -> SupplierDetails:
        url = self._url("/Supplier")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return SupplierDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateSupplier) -> None:
        url = self._url("/Supplier")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_external_reference(self, external_reference: str | None = None) -> None:
        url = self._url("/Supplier/DeleteByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)
