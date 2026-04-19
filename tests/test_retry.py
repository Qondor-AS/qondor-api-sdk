"""Tests for retry logic and response handler."""

from __future__ import annotations

import httpx
import pytest

from qondor_api_sdk._retry import _raise_for_status
from qondor_api_sdk.errors import (
    QondorApiError,
    QondorRateLimitError,
    QondorServerError,
    QondorValidationError,
)


def _make_response(status_code: int, json_body: dict | None = None, headers: dict | None = None) -> httpx.Response:
    """Build a fake httpx.Response."""
    h = {"content-type": "application/json"} if json_body is not None else {}
    if headers:
        h.update(headers)
    resp = httpx.Response(
        status_code=status_code,
        json=json_body,
        headers=h,
        request=httpx.Request("GET", "https://example.com"),
    )
    return resp


class TestRaiseForStatus:
    def test_200_does_not_raise(self):
        resp = _make_response(200)
        _raise_for_status(resp)  # should not raise

    def test_201_does_not_raise(self):
        resp = _make_response(201)
        _raise_for_status(resp)

    def test_400_raises_validation_error(self):
        body = {
            "errors": {"Name": ["Name is required."]},
            "title": "Validation error",
            "status": 400,
        }
        resp = _make_response(400, json_body=body)
        with pytest.raises(QondorValidationError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 400
        assert "Name" in exc_info.value.errors

    def test_422_raises_validation_error(self):
        body = {"errors": {"Field": ["Invalid"]}, "status": 422}
        resp = _make_response(422, json_body=body)
        with pytest.raises(QondorValidationError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 422

    def test_429_raises_rate_limit_error(self):
        resp = _make_response(429, headers={"Retry-After": "5"})
        with pytest.raises(QondorRateLimitError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.retry_after == 5.0

    def test_429_without_retry_after_header(self):
        resp = _make_response(429)
        with pytest.raises(QondorRateLimitError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.retry_after is None

    def test_503_raises_rate_limit_error(self):
        resp = _make_response(503)
        with pytest.raises(QondorRateLimitError):
            _raise_for_status(resp)

    def test_500_raises_server_error(self):
        resp = _make_response(500)
        with pytest.raises(QondorServerError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 500

    def test_502_raises_server_error(self):
        resp = _make_response(502)
        with pytest.raises(QondorServerError):
            _raise_for_status(resp)

    def test_404_raises_generic_api_error(self):
        resp = _make_response(404)
        with pytest.raises(QondorApiError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 404
        assert not isinstance(exc_info.value, QondorValidationError)

    def test_400_non_json_raises_validation_error_with_text(self):
        resp = httpx.Response(
            status_code=400,
            text="Bad Request",
            headers={"content-type": "text/plain"},
            request=httpx.Request("GET", "https://example.com"),
        )
        with pytest.raises(QondorValidationError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.raw_response is None
        assert "Bad Request" in exc_info.value.detail

    def test_retry_after_non_numeric_ignored(self):
        resp = _make_response(429, headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"})
        with pytest.raises(QondorRateLimitError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.retry_after is None


class TestRetryDecorator:
    async def test_retry_on_rate_limit(self):
        """Verify _with_retry retries on QondorRateLimitError."""
        from qondor_api_sdk._retry import _with_retry

        call_count = 0

        @_with_retry
        async def flaky_call():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise QondorRateLimitError(429, "Rate limited", retry_after=0.01)
            return "success"

        result = await flaky_call()
        assert result == "success"
        assert call_count == 3

    async def test_no_retry_on_validation_error(self):
        """Verify _with_retry does NOT retry on QondorValidationError."""
        from qondor_api_sdk._retry import _with_retry

        call_count = 0

        @_with_retry
        async def bad_call():
            nonlocal call_count
            call_count += 1
            raise QondorValidationError(400, "Bad request")

        with pytest.raises(QondorValidationError):
            await bad_call()
        assert call_count == 1

    async def test_no_retry_on_server_error(self):
        """Verify _with_retry does NOT retry on QondorServerError."""
        from qondor_api_sdk._retry import _with_retry

        call_count = 0

        @_with_retry
        async def failing_call():
            nonlocal call_count
            call_count += 1
            raise QondorServerError(500, "Server error")

        with pytest.raises(QondorServerError):
            await failing_call()
        assert call_count == 1
