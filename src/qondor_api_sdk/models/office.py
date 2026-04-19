from __future__ import annotations

from .._base import ApiModel

__all__ = ["OfficeSummary"]


class OfficeSummary(ApiModel):
    id: int | None = None
    name: str | None = None
    internal_name: str | None = None
    public_name: str | None = None
    address: str | None = None
    zip_code: str | None = None
    city: str | None = None
    country: str | None = None
    country_code: str | None = None
    external_reference: str | None = None
    custom_value1: str | None = None
    custom_value2: str | None = None
    custom_value3: str | None = None
    custom_value4: str | None = None
