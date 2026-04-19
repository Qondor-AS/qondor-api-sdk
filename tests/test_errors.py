"""Tests for SDK error hierarchy and ProblemDetails parsing."""

from __future__ import annotations

from qondor_api_sdk.errors import (
    QondorApiError,
    QondorRateLimitError,
    QondorServerError,
    QondorValidationError,
)


class TestErrorHierarchy:
    def test_validation_error_is_api_error(self):
        err = QondorValidationError(400, "Bad request")
        assert isinstance(err, QondorApiError)

    def test_server_error_is_api_error(self):
        err = QondorServerError(500, "Internal server error")
        assert isinstance(err, QondorApiError)

    def test_rate_limit_error_is_api_error(self):
        err = QondorRateLimitError(429, "Rate limited")
        assert isinstance(err, QondorApiError)

    def test_error_stores_status_code(self):
        err = QondorApiError(404, "Not found")
        assert err.status_code == 404
        assert err.detail == "Not found"


class TestValidationErrorParsing:
    def test_parses_model_binding_errors(self):
        """ASP.NET model binding error format."""
        raw = {
            "errors": {"ProjectId": ["Could not convert string to integer: abc"]},
            "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
            "title": "One or more validation errors occurred.",
            "status": 400,
            "traceId": "00-abc123",
        }
        err = QondorValidationError(400, str(raw), raw_response=raw)
        assert "ProjectId" in err.errors
        assert err.errors["ProjectId"] == ["Could not convert string to integer: abc"]

    def test_parses_fluent_validation_errors(self):
        """FluentValidation business rule error format."""
        raw = {
            "errors": {"LocationCode": ["'ASDASD' is not a valid location code."]},
            "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
            "title": "One or more validation errors occurred.",
            "status": 400,
        }
        err = QondorValidationError(400, str(raw), raw_response=raw)
        assert "LocationCode" in err.errors
        assert "'ASDASD' is not a valid location code." in err.errors["LocationCode"]

    def test_multiple_field_errors(self):
        raw = {
            "errors": {
                "Name": ["Name is required."],
                "OfficeId": ["Invalid office ID.", "Office not found."],
            },
            "title": "One or more validation errors occurred.",
            "status": 400,
        }
        err = QondorValidationError(400, str(raw), raw_response=raw)
        assert len(err.errors) == 2
        assert len(err.errors["OfficeId"]) == 2

    def test_no_raw_response_means_empty_errors(self):
        err = QondorValidationError(400, "Bad request")
        assert err.errors == {}

    def test_raw_response_without_errors_key(self):
        raw = {"title": "Error", "status": 400}
        err = QondorValidationError(400, str(raw), raw_response=raw)
        assert err.errors == {}


class TestRateLimitError:
    def test_stores_retry_after(self):
        err = QondorRateLimitError(429, "Rate limited", retry_after=5.0)
        assert err.retry_after == 5.0

    def test_retry_after_defaults_to_none(self):
        err = QondorRateLimitError(429, "Rate limited")
        assert err.retry_after is None
