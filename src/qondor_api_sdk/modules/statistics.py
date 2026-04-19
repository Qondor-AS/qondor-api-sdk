from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.statistics import OfferSalesStatistics


class StatisticsModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get_offer_sales(
        self, office_id: int | None = None, project_id: int | None = None, last_modified_date: str | None = None,
    ) -> list[OfferSalesStatistics]:
        url = self._url("/Statistics/GetOfferSales")
        params = {"officeId": office_id, "projectId": project_id, "lastModifiedDate": last_modified_date}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [OfferSalesStatistics.model_validate(item) for item in resp.json()]
