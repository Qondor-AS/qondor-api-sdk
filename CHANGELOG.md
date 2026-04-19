# Changelog

All notable changes to `qondor-api-sdk` are documented in this file. The format
is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-19

Initial public release.

### Added

- Async `QondorClient` with subscription-key auth and optional delegated JWT
  (`X-OnBehalfOf-Token`).
- Nine resource modules on the client: `customer`, `project`, `offer`,
  `product_group`, `product`, `supplier`, `office`, `contact_person`,
  `statistics`.
- Pydantic v2 models with alias-based (camelCase ↔ snake_case) (de)serialization
  for request and response payloads.
- Typed error hierarchy rooted at `QondorApiError` — `QondorValidationError`
  (400/422, parsed ProblemDetails), `QondorServerError` (500),
  `QondorRateLimitError` (429/503).
- Automatic retry with exponential backoff via `tenacity` for 429/503,
  honouring `Retry-After`.
- Configurable resource-group URL prefixes and auth header for non-standard
  deployments.
- `py.typed` marker — type information ships with the wheel.
