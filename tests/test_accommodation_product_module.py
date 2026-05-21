"""Tests for AccommodationProductModule: HTTP method, path, params, and response parsing.

Covers all three controllers under the AccommodationProduct resource group:
  - /AccommodationProduct        (product CRUD)
  - /AccommodationRoomProduct    (room CRUD)
  - /AccommodationRoomNightProduct (night CRUD)
"""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.accommodation_product import (
    AccommodationProductDetails,
    AccommodationProductSummary,
    AccommodationRoomDetails,
    AccommodationRoomNightDetails,
    AccommodationRoomNightPrice,
    CreateAccommodationProduct,
    CreateAccommodationRoom,
    CreateAccommodationRoomNight,
    UpdateAccommodationProduct,
    UpdateAccommodationRoom,
    UpdateAccommodationRoomNight,
)
from qondor_api_sdk.modules.accommodation_product import AccommodationProductModule

PREFIX = "/AccommodationProduct/v1"
BASE = "https://mock.example.com" + PREFIX

PRODUCT_JSON = {
    "id": 10,
    "name": "Grand Hotel",
    "offerId": 789,
    "isPublishedOnOffer": True,
    "enableOfferConfiguration": False,
    "isOptionalOnOffer": False,
    "offerQuantity": 1.0,
    "offerDesignTemplate": 1,
    "rooms": [],
}

ROOM_JSON = {
    "id": 100,
    "name": "Double Room",
    "position": 1,
    "guestsPerRoom": 2,
    "billingModel": 1,
    "referral": False,
    "commissionPercent": 0.0,
    "isInitialRateInclVat": False,
    "nights": [],
}

NIGHT_JSON = {
    "id": 1000,
    "numberOfRooms": 5,
    "initialRate": 1500.0,
    "date": "2026-06-01T00:00:00",
    "prices": [],
}


class TestAccommodationProduct:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationProduct/10", json=PRODUCT_JSON)
        module = AccommodationProductModule(http_client, PREFIX)
        result = await module.get(10)
        assert isinstance(result, AccommodationProductDetails)
        assert result.id == 10
        assert result.name == "Grand Hotel"

    async def test_get_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationProduct/GetByExternalReference",
                params={"externalReference": "ap-1"},
            ),
            json={**PRODUCT_JSON, "externalReference": "ap-1"},
        )
        module = AccommodationProductModule(http_client, PREFIX)
        result = await module.get_by_external_reference(external_reference="ap-1")
        assert isinstance(result, AccommodationProductDetails)
        assert result.external_reference == "ap-1"

    async def test_get_all_for_project(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationProduct/GetAllForProject",
                params={"projectId": "42"},
            ),
            json=[PRODUCT_JSON],
        )
        module = AccommodationProductModule(http_client, PREFIX)
        result = await module.get_all_for_project(project_id=42)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], AccommodationProductSummary)
        assert result[0].id == 10

    async def test_get_all_for_project_by_no(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationProduct/GetAllForProject",
                params={"projectNo": "PRJ-2026"},
            ),
            json=[],
        )
        module = AccommodationProductModule(http_client, PREFIX)
        result = await module.get_all_for_project(project_no="PRJ-2026")
        assert result == []

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationProduct", method="POST", json=PRODUCT_JSON)
        module = AccommodationProductModule(http_client, PREFIX)
        request = CreateAccommodationProduct(name="Grand Hotel", offer_id=789)
        result = await module.create(request)
        assert isinstance(result, AccommodationProductDetails)
        assert result.id == 10

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["name"] == "Grand Hotel"
        assert body["offerId"] == 789

    async def test_update(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationProduct", method="PUT", status_code=200)
        module = AccommodationProductModule(http_client, PREFIX)
        result = await module.update(UpdateAccommodationProduct(id=10, name="Renamed"))
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 10
        assert body["name"] == "Renamed"

    async def test_delete(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationProduct/10", method="DELETE", status_code=200)
        module = AccommodationProductModule(http_client, PREFIX)
        await module.delete(10)

    async def test_delete_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationProduct/DeleteByExternalReference",
                params={"externalReference": "ap-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = AccommodationProductModule(http_client, PREFIX)
        await module.delete_by_external_reference(external_reference="ap-1")


class TestAccommodationRoom:
    async def test_create_room(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationRoomProduct", method="POST", json=ROOM_JSON)
        module = AccommodationProductModule(http_client, PREFIX)
        request = CreateAccommodationRoom(accommodation_product_id=10, name="Double Room", guests_per_room=2)
        result = await module.create_room(request)
        assert isinstance(result, AccommodationRoomDetails)
        assert result.id == 100
        assert result.name == "Double Room"

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["accommodationProductId"] == 10
        assert body["guestsPerRoom"] == 2

    async def test_update_room(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationRoomProduct", method="PUT", status_code=200)
        module = AccommodationProductModule(http_client, PREFIX)
        request = UpdateAccommodationRoom(id=100, accommodation_product_id=10, name="Twin Room")
        result = await module.update_room(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 100
        assert body["name"] == "Twin Room"

    async def test_delete_room_by_id(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationRoomProduct",
                params={"id": "100", "accommodationProductId": "10"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = AccommodationProductModule(http_client, PREFIX)
        await module.delete_room(id=100, accommodation_product_id=10)

    async def test_delete_room_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationRoomProduct",
                params={"externalReference": "rm-1", "accommodationExternalReference": "ap-1"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = AccommodationProductModule(http_client, PREFIX)
        await module.delete_room(external_reference="rm-1", accommodation_external_reference="ap-1")


class TestAccommodationRoomNight:
    async def test_create_room_night(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationRoomNightProduct", method="POST", json=NIGHT_JSON)
        module = AccommodationProductModule(http_client, PREFIX)
        request = CreateAccommodationRoomNight(
            accommodation_product_id=10,
            room_id=100,
            check_in_date="2026-06-01",
            allotment=5,
            prices=[AccommodationRoomNightPrice(art_no="A1", out_price_excl_vat=1200.0, out_price_incl_vat=1500.0)],
        )
        result = await module.create_room_night(request)
        assert isinstance(result, AccommodationRoomNightDetails)
        assert result.id == 1000

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["accommodationProductId"] == 10
        assert body["roomId"] == 100
        assert body["numberOfRooms"] == 5
        assert body["prices"][0]["artNo"] == "A1"
        assert body["prices"][0]["outPriceExclVat"] == 1200.0

    async def test_update_room_night(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url=f"{BASE}/AccommodationRoomNightProduct", method="PUT", status_code=200)
        module = AccommodationProductModule(http_client, PREFIX)
        request = UpdateAccommodationRoomNight(
            id=1000, room_id=100, accommodation_product_id=10, allotment=10,
        )
        result = await module.update_room_night(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["id"] == 1000
        assert body["numberOfRooms"] == 10

    async def test_delete_room_night_by_id(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationRoomNightProduct",
                params={"id": "1000", "roomId": "100", "accommodationProductId": "10"},
            ),
            method="DELETE",
            status_code=200,
        )
        module = AccommodationProductModule(http_client, PREFIX)
        await module.delete_room_night(id=1000, room_id=100, accommodation_product_id=10)

    async def test_delete_room_night_by_external_reference(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                f"{BASE}/AccommodationRoomNightProduct",
                params={
                    "externalReference": "nt-1",
                    "roomExternalReference": "rm-1",
                    "accommodationProductExternalReference": "ap-1",
                },
            ),
            method="DELETE",
            status_code=200,
        )
        module = AccommodationProductModule(http_client, PREFIX)
        await module.delete_room_night(
            external_reference="nt-1",
            room_external_reference="rm-1",
            accommodation_product_external_reference="ap-1",
        )
