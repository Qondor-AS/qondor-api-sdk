"""Retry decorator and response handler for Qondor API calls."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx
from tenacity import RetryCallState, retry, retry_if_exception_type, stop_after_attempt

from .errors import QondorApiError, QondorRateLimitError, QondorServerError, QondorValidationError


def _wait_with_retry_after(retry_state: RetryCallState) -> float:
    """Use Retry-After header if available, otherwise exponential backoff."""
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    if isinstance(exc, QondorRateLimitError) and exc.retry_after is not None:
        return exc.retry_after
    attempt = retry_state.attempt_number
    return min(2 ** (attempt - 1), 30)


def _with_retry[F: Callable[..., Any]](func: F) -> F:
    """Decorator: retry on 429/503 with backoff, respecting Retry-After."""
    return retry(  # type: ignore[return-value]
        retry=retry_if_exception_type(QondorRateLimitError),
        wait=_wait_with_retry_after,
        stop=stop_after_attempt(5),
        reraise=True,
    )(func)


def _raise_for_status(resp: httpx.Response) -> None:
    """Classify HTTP errors into SDK error types."""
    if resp.status_code in (429, 503):
        retry_after: float | None = None
        retry_after_raw = resp.headers.get("Retry-After")
        if retry_after_raw:
            try:
                retry_after = float(retry_after_raw)
            except ValueError:
                pass
        raise QondorRateLimitError(
            resp.status_code,
            "Rate limited or unavailable",
            retry_after=retry_after,
        )
    if resp.status_code in (400, 422):
        raw: dict | None = None
        detail = resp.text
        content_type = resp.headers.get("content-type", "")
        if content_type.startswith("application/json") or content_type.startswith("application/problem+json"):
            raw = resp.json()
            detail = str(raw)
        raise QondorValidationError(resp.status_code, detail, raw_response=raw)
    if resp.status_code >= 500:
        raise QondorServerError(resp.status_code, resp.text)
    if resp.status_code >= 400:
        raise QondorApiError(resp.status_code, resp.text)
