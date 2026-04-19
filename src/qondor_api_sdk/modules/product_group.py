from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.product_group import CreateProductGroup, ProductGroupDetails, ProductGroupSummary, UpdateProductGroup


class ProductGroupModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> ProductGroupDetails:
        url = self._url(f"/ProductGroup/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return ProductGroupDetails.model_validate(resp.json())

    @_with_retry
    async def delete(self, id: int) -> None:
        url = self._url(f"/ProductGroup/{id}")
        resp = await self._http.delete(url)
        _raise_for_status(resp)

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> ProductGroupDetails:
        url = self._url("/ProductGroup/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return ProductGroupDetails.model_validate(resp.json())

    @_with_retry
    async def get_all_for_offer(
        self, offer_id: int | None = None, offer_external_reference: str | None = None,
    ) -> list[ProductGroupSummary]:
        url = self._url("/ProductGroup/GetAllForOffer")
        params = {"offerId": offer_id, "offerExternalReference": offer_external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [ProductGroupSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def create(self, request: CreateProductGroup) -> ProductGroupDetails:
        url = self._url("/ProductGroup")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return ProductGroupDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateProductGroup) -> None:
        url = self._url("/ProductGroup")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_external_reference(self, external_reference: str | None = None) -> None:
        url = self._url("/ProductGroup/DeleteByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)
