"""SDK error hierarchy for Qondor API responses."""

from __future__ import annotations


class QondorApiError(Exception):
    """Base error for all SDK errors."""

    def __init__(self, status_code: int, detail: str, raw_response: dict | None = None) -> None:
        self.status_code = status_code
        self.detail = detail
        self.raw_response = raw_response
        super().__init__(f"[{status_code}] {detail}")


class QondorValidationError(QondorApiError):
    """400/422 -- agent can self-correct and retry.

    Parses ASP.NET ProblemDetails JSON. The ``errors`` dict maps
    field names to lists of error messages.
    """

    def __init__(self, status_code: int, detail: str, raw_response: dict | None = None) -> None:
        super().__init__(status_code, detail, raw_response)
        self.errors: dict[str, list[str]] = {}
        if isinstance(raw_response, dict):
            self.errors = raw_response.get("errors", {})


class QondorServerError(QondorApiError):
    """500 -- surface to human, don't retry."""


class QondorRateLimitError(QondorApiError):
    """429/503 -- handled transparently by retry logic.

    Azure APIM returns Retry-After header on 429 responses.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        retry_after: float | None = None,
        raw_response: dict | None = None,
    ) -> None:
        super().__init__(status_code, detail, raw_response)
        self.retry_after = retry_after
