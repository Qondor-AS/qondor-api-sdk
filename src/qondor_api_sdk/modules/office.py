from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.customer import CustomerCategory
from ..models.office import OfficeSummary


class OfficeModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get_all(self) -> list[OfficeSummary]:
        url = self._url("/Office/GetAll")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return [OfficeSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def get_all_customer_categories(self, office_id: int | None = None) -> list[CustomerCategory]:
        url = self._url("/Office/GetAllCustomerCategories")
        params = {"officeId": office_id}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [CustomerCategory.model_validate(item) for item in resp.json()]
