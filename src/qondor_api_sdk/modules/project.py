from __future__ import annotations

import httpx

from .._retry import _raise_for_status, _with_retry
from ..models.enums import ProjectStatus
from ..models.project import CreateProject, ProjectDetails, ProjectSummary, SetAsFinished


class ProjectModule:
    def __init__(self, http: httpx.AsyncClient, prefix: str = "") -> None:
        self._http = http
        self._prefix = prefix

    def _url(self, path: str) -> str:
        return f"{self._prefix}{path}"

    @_with_retry
    async def get_all(
        self,
        status: list[ProjectStatus] | None = None,
        office_id: int | None = None,
        changed_after: str | None = None,
        changed_after_includes_offer_changes: bool | None = None,
        include_project_leaders: bool | None = None,
        include_project_managers: bool | None = None,
        include_project_custom_field_answers: bool | None = None,
    ) -> list[ProjectSummary]:
        url = self._url("/Project/GetAll")
        params = {
            "status": status,
            "officeId": office_id,
            "changedAfter": changed_after,
            "changedAfterIncludesOfferChanges": changed_after_includes_offer_changes,
            "includeProjectLeaders": include_project_leaders,
            "includeProjectManagers": include_project_managers,
            "includeProjectCustomFieldAnswers": include_project_custom_field_answers,
        }
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return [ProjectSummary.model_validate(item) for item in resp.json()]

    @_with_retry
    async def get(self, id: int) -> ProjectDetails:
        url = self._url(f"/Project/{id}")
        resp = await self._http.get(url)
        _raise_for_status(resp)
        return ProjectDetails.model_validate(resp.json())

    @_with_retry
    async def get_by_project_no(self, project_no: str | None = None, office_id: int | None = None) -> ProjectDetails:
        url = self._url("/Project/GetByProjectNo")
        params = {"projectNo": project_no, "officeId": office_id}
        params = {k: v for k, v in params.items() if v is not None}
        resp = await self._http.get(url, params=params)
        _raise_for_status(resp)
        return ProjectDetails.model_validate(resp.json())

    @_with_retry
    async def set_as_finished(self, request: SetAsFinished) -> None:
        url = self._url("/Project/SetAsFinished")
        resp = await self._http.put(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)

    @_with_retry
    async def create(self, request: CreateProject) -> ProjectDetails:
        url = self._url("/Project")
        resp = await self._http.post(url, json=request.model_dump(by_alias=True, exclude_none=True))
        _raise_for_status(resp)
        return ProjectDetails.model_validate(resp.json())
