"""Integration tests for project operations."""

from __future__ import annotations

import pytest

from qondor_api_sdk.client import QondorClient
from qondor_api_sdk.models.project import ProjectDetails, ProjectSummary, SetAsFinished

from .conftest import EnvConfig

pytestmark = pytest.mark.integration


class TestProject:
    """Project lifecycle tests (create is handled by the session fixture)."""

    async def test_create(self, created_project: ProjectDetails):
        assert created_project.id is not None
        assert created_project.name == "IntTest Project"

    async def test_get(self, created_project: ProjectDetails, qondor_client: QondorClient):
        result = await qondor_client.project.get(created_project.id)
        assert isinstance(result, ProjectDetails)
        assert result.id == created_project.id

    async def test_list(self, env_config: EnvConfig, qondor_client: QondorClient):
        results = await qondor_client.project.get_all(office_id=env_config.office_id)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], ProjectSummary)

    async def test_get_by_project_no(
        self, created_project: ProjectDetails, env_config: EnvConfig, qondor_client: QondorClient
    ):
        # Fetch the project to get its project_no
        full = await qondor_client.project.get(created_project.id)
        assert full.project_no is not None, "project_no not found in response"

        result = await qondor_client.project.get_by_project_no(
            project_no=str(full.project_no),
            office_id=env_config.office_id,
        )
        assert isinstance(result, ProjectDetails)
        assert result.id == created_project.id

    async def test_set_as_finished(
        self, created_project: ProjectDetails, env_config: EnvConfig, qondor_client: QondorClient
    ):
        await qondor_client.project.set_as_finished(SetAsFinished(
            project_id=created_project.id,
            office_id=env_config.office_id,
            real_sales=95000,
            real_revenue=18000,
        ))
