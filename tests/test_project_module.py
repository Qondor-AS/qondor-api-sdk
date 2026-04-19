"""Tests for ProjectModule: correct HTTP method, path, params, and response parsing."""

from __future__ import annotations

import json

import httpx
from pytest_httpx import HTTPXMock

from qondor_api_sdk.models.enums import ProjectStatus
from qondor_api_sdk.models.project import CreateProject, ProjectDetails, ProjectSummary, SetAsFinished
from qondor_api_sdk.modules.project import ProjectModule

PROJECT_JSON = {"id": 1, "name": "Test Project", "projectNo": "P001", "status": 1, "officeId": 1}


class TestProjectModule:
    async def test_get(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(url="https://mock.example.com/Project/v1/Project/1", json=PROJECT_JSON)
        module = ProjectModule(http_client, "/Project/v1")
        result = await module.get(1)
        assert isinstance(result, ProjectDetails)
        assert result.id == 1
        assert result.name == "Test Project"

    async def test_get_all(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Project/v1/Project/GetAll",
                params=[("status", "1"), ("status", "2"), ("officeId", "1")],
            ),
            json=[PROJECT_JSON],
        )
        module = ProjectModule(http_client, "/Project/v1")
        result = await module.get_all(
            status=[ProjectStatus.PENDING, ProjectStatus.CONFIRMED],
            office_id=1,
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ProjectSummary)

    async def test_get_by_project_no(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url=httpx.URL(
                "https://mock.example.com/Project/v1/Project/GetByProjectNo",
                params={"projectNo": "P001", "officeId": "1"},
            ),
            json=PROJECT_JSON,
        )
        module = ProjectModule(http_client, "/Project/v1")
        result = await module.get_by_project_no(project_no="P001", office_id=1)
        assert isinstance(result, ProjectDetails)
        assert result.project_no == "P001"

    async def test_create(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Project/v1/Project",
            method="POST",
            json=PROJECT_JSON,
        )
        module = ProjectModule(http_client, "/Project/v1")
        request = CreateProject(office_id=1, name="Test Project")
        result = await module.create(request)
        assert isinstance(result, ProjectDetails)
        assert result.id == 1

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["officeId"] == 1
        assert body["name"] == "Test Project"

    async def test_set_as_finished(self, http_client: httpx.AsyncClient, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://mock.example.com/Project/v1/Project/SetAsFinished",
            method="PUT",
            status_code=200,
        )
        module = ProjectModule(http_client, "/Project/v1")
        request = SetAsFinished(project_id=1, real_sales=10000.0, real_revenue=3000.0)
        result = await module.set_as_finished(request)
        assert result is None

        sent = httpx_mock.get_requests()[-1]
        body = json.loads(sent.content)
        assert body["projectId"] == 1
        assert body["realSales"] == 10000.0
