from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.customer import CreateCustomer, CustomerDetails, CustomerSummary, UpdateCustomer


class CustomerModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> CustomerDetails:
        url = self._url(f"/Customer/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return CustomerDetails.model_validate(resp.json())

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> CustomerDetails:
        url = self._url("/Customer/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return CustomerDetails.model_validate(resp.json())

    @_with_retry
    async def get_all(self, office_id: int | None = None) -> list[CustomerSummary]:
        url = self._url("/Customer/GetAll")
        params = {"officeId": office_id}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [CustomerSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def get_all_by_customer_number(
        self, customer_number: str | None = None, office_id: int | None = None,
    ) -> list[CustomerDetails]:
        url = self._url("/Customer/GetAllByCustomerNumber")
        params = {"customerNumber": customer_number, "officeId": office_id}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [CustomerDetails.model_validate(item) for item in resp.json()]

    @_with_retry
    async def create(self, request: CreateCustomer) -> CustomerDetails:
        url = self._url("/Customer")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return CustomerDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateCustomer) -> None:
        url = self._url("/Customer")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
