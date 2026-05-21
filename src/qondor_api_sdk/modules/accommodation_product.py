from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.accommodation_product import (
    AccommodationProductDetails,
    AccommodationProductSummary,
    AccommodationRoomDetails,
    AccommodationRoomNightDetails,
    CreateAccommodationProduct,
    CreateAccommodationRoom,
    CreateAccommodationRoomNight,
    UpdateAccommodationProduct,
    UpdateAccommodationRoom,
    UpdateAccommodationRoomNight,
)


class AccommodationProductModule:
    """Accommodation products, rooms, and room nights.

    Wraps three API6 controllers that share the AccommodationProduct resource group:
      - /AccommodationProduct
      - /AccommodationRoomProduct
      - /AccommodationRoomNightProduct
    """

    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> AccommodationProductDetails:
        url = self._url(f"/AccommodationProduct/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return AccommodationProductDetails.model_validate(resp.json())

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> AccommodationProductDetails:
        url = self._url("/AccommodationProduct/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return AccommodationProductDetails.model_validate(resp.json())

    @_with_retry
    async def get_all_for_project(
        self, project_id: int | None = None, project_no: str | None = None,
    ) -> list[AccommodationProductSummary]:
        url = self._url("/AccommodationProduct/GetAllForProject")
        params = {"projectId": project_id, "projectNo": project_no}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [AccommodationProductSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def create(self, request: CreateAccommodationProduct) -> AccommodationProductDetails:
        url = self._url("/AccommodationProduct")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return AccommodationProductDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateAccommodationProduct) -> None:
        url = self._url("/AccommodationProduct")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete(self, id: int) -> None:
        url = self._url(f"/AccommodationProduct/{id}")
        resp = await self._http.delete(url)
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_external_reference(self, external_reference: str | None = None) -> None:
        url = self._url("/AccommodationProduct/DeleteByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def create_room(self, request: CreateAccommodationRoom) -> AccommodationRoomDetails:
        url = self._url("/AccommodationRoomProduct")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return AccommodationRoomDetails.model_validate(resp.json())

    @_with_retry
    async def update_room(self, request: UpdateAccommodationRoom) -> None:
        url = self._url("/AccommodationRoomProduct")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_room(
        self,
        id: int | None = None,
        external_reference: str | None = None,
        accommodation_product_id: int | None = None,
        accommodation_external_reference: str | None = None,
    ) -> None:
        url = self._url("/AccommodationRoomProduct")
        params = {
            "id": id,
            "externalReference": external_reference,
            "accommodationProductId": accommodation_product_id,
            "accommodationExternalReference": accommodation_external_reference,
        }
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def create_room_night(self, request: CreateAccommodationRoomNight) -> AccommodationRoomNightDetails:
        url = self._url("/AccommodationRoomNightProduct")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return AccommodationRoomNightDetails.model_validate(resp.json())

    @_with_retry
    async def update_room_night(self, request: UpdateAccommodationRoomNight) -> None:
        url = self._url("/AccommodationRoomNightProduct")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_room_night(
        self,
        id: int | None = None,
        external_reference: str | None = None,
        room_id: int | None = None,
        room_external_reference: str | None = None,
        accommodation_product_id: int | None = None,
        accommodation_product_external_reference: str | None = None,
    ) -> None:
        url = self._url("/AccommodationRoomNightProduct")
        params = {
            "id": id,
            "externalReference": external_reference,
            "roomId": room_id,
            "roomExternalReference": room_external_reference,
            "accommodationProductId": accommodation_product_id,
            "accommodationProductExternalReference": accommodation_product_external_reference,
        }
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)
