# qondor-api-sdk

Typed async Python SDK for the [Qondor API](https://qondor.com).

## Installation

```bash
pip install qondor-api-sdk
```

## Quick start

```python
from qondor_api_sdk import QondorClient

client = QondorClient(
    base_url="https://api.example.com/Prod",
    subscription_key="your-subscription-key",
    on_behalf_of_jwt="delegated-jwt",
)

customers = await client.customer.get_all()
await client.close()
```

### Custom configuration

For non-standard deployments you can override the auth header and disable
resource-group path prefixes:

```python
client = QondorClient(
    base_url="https://api.example.com",
    subscription_key="your-key",
    auth_header="X-Custom-Auth",
    use_resource_group_prefixes=False,
)
```

## Modules

| Module              | Description                  |
|---------------------|------------------------------|
| `client.customer`   | Customer CRUD                |
| `client.project`    | Project CRUD                 |
| `client.offer`      | Offer CRUD and currencies    |
| `client.product_group` | Product group CRUD        |
| `client.product`    | Product CRUD and pricing     |
| `client.supplier`   | Supplier CRUD                |
| `client.office`     | Office lookup                |
| `client.contact_person` | Contact person CRUD      |
| `client.statistics` | Offer/sales statistics       |

## Error handling

All errors derive from `QondorApiError`:

- **`QondorValidationError`** (400/422) — includes parsed field errors from ASP.NET ProblemDetails.
- **`QondorServerError`** (500) — surface to human, do not retry.
- **`QondorRateLimitError`** (429/503) — retried automatically with exponential backoff, respecting the `Retry-After` header.

## Retry behaviour

Calls that receive 429 or 503 are retried up to 5 times with exponential backoff (1 s, 2 s, 4 s, …, capped at 30 s). If the response includes a `Retry-After` header, that value is used instead.

## Integration tests

Integration tests live in `tests/integration/` and hit the real Qondor API.
Set `QONDOR_SUBSCRIPTION_KEY` (and optionally `QONDOR_ENV`, defaults to `dev`)
and run `uv run pytest -m integration`. They also run automatically on merges
to `main` via the `Integration Tests` GitHub Actions workflow.

## License

MIT — see [LICENSE](LICENSE).
