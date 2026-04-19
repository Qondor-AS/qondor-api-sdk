from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.product import (
    AddPrice,
    AttachTicketToTransportProduct,
    ConfirmProduct,
    CreateProduct,
    ProductDetails,
    ProductPriceOut,
    ProductSummary,
    ProductTicketDetails,
    ProductTicketSummary,
    UpdatePrice,
    UpdateProduct,
)


class ProductModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get(self, id: int) -> ProductDetails:
        url = self._url(f"/Product/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return ProductDetails.model_validate(resp.json())

    @_with_retry
    async def delete(self, id: int) -> None:
        url = self._url(f"/Product/{id}")
        resp = await self._http.delete(url)
        _raise_for_status(resp)

    @_with_retry
    async def get_by_external_reference(self, external_reference: str | None = None) -> ProductDetails:
        url = self._url("/Product/GetByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return ProductDetails.model_validate(resp.json())

    @_with_retry
    async def get_all_for_project(
        self, project_id: int | None = None, project_no: str | None = None,
    ) -> list[ProductSummary]:
        url = self._url("/Product/GetAllForProject")
        params = {"projectId": project_id, "projectNo": project_no}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [ProductSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def create(self, request: CreateProduct) -> ProductDetails:
        url = self._url("/Product")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return ProductDetails.model_validate(resp.json())

    @_with_retry
    async def update(self, request: UpdateProduct) -> None:
        url = self._url("/Product")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_by_external_reference(self, external_reference: str | None = None) -> None:
        url = self._url("/Product/DeleteByExternalReference")
        params = {"externalReference": external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def confirm_product(self, request: ConfirmProduct) -> None:
        url = self._url("/Product/ConfirmProduct")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def add_price(self, request: AddPrice) -> ProductPriceOut:
        url = self._url("/Product/AddPrice")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return ProductPriceOut.model_validate(resp.json())

    @_with_retry
    async def update_price(self, request: UpdatePrice) -> None:
        url = self._url("/Product/UpdatePrice")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def delete_price(
        self,
        id: int | None = None,
        external_reference: str | None = None,
        product_id: int | None = None,
        product_external_reference: str | None = None,
    ) -> None:
        url = self._url("/Product/DeletePrice")
        params = {
            "id": id,
            "externalReference": external_reference,
            "productId": product_id,
            "productExternalReference": product_external_reference,
        }
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)

    @_with_retry
    async def get_tickets_for_transport_product(
        self, transport_product_id: int | None = None,
    ) -> list[ProductTicketSummary]:
        url = self._url("/Product/GetTicketsForTransportProduct")
        params = {"transportProductId": transport_product_id}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [ProductTicketSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def get_tickets_for_transport_product_by_external_reference(
        self, transport_product_external_reference: str | None = None,
    ) -> list[ProductTicketSummary]:
        url = self._url("/Product/GetTicketsForTransportProductByExternalReference")
        params = {"transportProductExternalReference": transport_product_external_reference}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [ProductTicketSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def attach_ticket_to_transport_product(self, request: AttachTicketToTransportProduct) -> ProductTicketDetails:
        url = self._url("/Product/AttachTicketToTransportProduct")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return ProductTicketDetails.model_validate(resp.json())

    @_with_retry
    async def delete_detach_ticket_from_transport_product(
        self,
        transport_product_id: int | None = None,
        transport_product_external_reference: str | None = None,
        ticket_id: int | None = None,
        ticket_external_reference: str | None = None,
    ) -> None:
        url = self._url("/Product/DetachTicketFromTransportProduct")
        params = {
            "transportProductId": transport_product_id,
            "transportProductExternalReference": transport_product_external_reference,
            "ticketId": ticket_id,
            "ticketExternalReference": ticket_external_reference,
        }
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.delete(url, params=params)
        _raise_for_status(resp)
