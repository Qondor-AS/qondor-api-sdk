from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.offer import (
    AddCurrencyToOffer,
    CreateOffer,
    OfferCurrencyDetails,
    OfferDetails,
    OfferSummary,
    UpdateOffer,
    UpdateOfferCurrency,
)


class OfferModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> OfferDetails:
        url = self._url(f"/Offer/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return OfferDetails.model_validate(resp.json())

    @_with_retry
    async def delete(self, id: int) -> None:
        url = self._url(f"/Offer/{id}")
        resp = await self._http.delete(url)
        _raise_for_status(resp)

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> OfferDetails:
        url = self._url("/Offer/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return OfferDetails.model_validate(resp.json())

    @_with_retry
    async def get_all_for_project(self, project_id: int | None = None) -> list[OfferSummary]:
        url = self._url("/Offer/GetAllForProject")
        params = {"projectId": project_id}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [OfferSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def create(self, request: CreateOffer) -> OfferDetails:
        url = self._url("/Offer")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return OfferDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateOffer) -> None:
        url = self._url("/Offer")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_external_reference(self, external_reference: str | None = None) -> None:
        url = self._url("/Offer/DeleteByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def add_currency_to_offer(self, request: AddCurrencyToOffer) -> OfferCurrencyDetails:
        url = self._url("/Offer/AddCurrencyToOffer")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return OfferCurrencyDetails.model_validate(resp.json())

    @_with_retry
    async def update_offer_currency(self, request: UpdateOfferCurrency) -> None:
        url = self._url("/Offer/UpdateOfferCurrency")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_offer_currency(
        self,
        offer_id: int | None = None,
        offer_external_reference: str | None = None,
        offer_currency_id: int | None = None,
        offer_currency_external_reference: str | None = None,
    ) -> None:
        url = self._url("/Offer/DeleteOfferCurrency")
        params = {
            "offerId": offer_id,
            "offerExternalReference": offer_external_reference,
            "offerCurrencyId": offer_currency_id,
            "offerCurrencyExternalReference": offer_currency_external_reference,
        }
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)
