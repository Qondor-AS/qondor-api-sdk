# API6 coverage

How much of the .NET `Qondor.API6` surface this Python SDK exposes, what is
missing, and where to put new modules. Generated from a controller-by-controller
audit of `Qondor.API6/Services/*` versus the modules in this package.

## Summary

| Status | Service area | SDK module |
|---|---|---|
| Done | AccommodationProducts | `accommodation_product` |
| Done | ContactPerson | `contact_person` |
| Done | Offers | `offer` |
| Done | Offices | `office` |
| Done | Products | `product` |
| Done | ProductGroups | `product_group` |
| Done | Projects | `project` |
| Done | Statistics | `statistics` |
| Done | Suppliers | `supplier` |
| Partial | Customers | `customer` (main controller only; sub-controllers missing) |
| Missing | Bookings | — |
| Missing | CheckIns | — |
| Missing | Costs | — |
| Missing | Forms | — |
| Missing | Invoicing | — |
| Missing | Participants | — |
| Missing | Reporting | — |
| Missing | Sales | — |
| Missing | Teams | — |
| Missing | Tickets | — |
| Missing | TimeTracking | — |
| Missing | ViewOffers | — |
| Missing | ProductCommonFiles | — |
| N/A | Monitoring, Tests, Shared | intentionally not bound |

## Service areas entirely missing from the SDK

| Service area | Controllers | Endpoints | Notes |
|---|---|---|---|
| Bookings | Booking, BookingRawData | 4 | GetAll, Get(reference), GetBookingsForAccommodationProduct, POST raw data |
| CheckIns | CheckIn, CheckInClerk, CheckInPoint | 11 | GetCheckIns, CRUD on clerks and points, AssignToProject |
| Costs | Cost | 6 | Get, GetByExternalReference, GetAllForProject, CRUD |
| Forms | Form | 1 | Get by projectId |
| Invoicing | Invoice | 2 | Get(id), GetInvoice/{id} |
| Participants | Participant, ParticipantBadgeSettings, ParticipantCustomField, ParticipantStatistics | 13 | CRUD participants, badge settings, custom fields, statistics |
| Reporting | Reporting | 3 | GetProjectList, GetBookerSales, GetProgramFeedbackResults |
| Sales | Sale | 6 | Get, GetByExternalReference, GetAllForProject, CRUD |
| Teams | Team | 3 | Get(id), GetByExternalReference, GetAll |
| Tickets | Ticket | 5 | Get(id), GetForProjectNumber, CRUD |
| TimeTracking | TimeTrackingLogEntry, TimeTrackingProjectBudget | 4 | GetAll + Get per resource |
| ViewOffers | ViewOffer | 1 | Get(id) |
| ProductCommonFiles | (not verified in detail) | ? | Folder exists in API6, no SDK module |

Intentional omissions (not gaps):

- **Monitoring** (`/Ping`, `/TestException`) — health-check / diagnostic
- **Tests** (`/Test/NullableMapping`) — internal mapping test
- **Shared** — shared utilities, not its own endpoint surface

## Within-module gaps

### `customer` — missing the entire sub-resource surface

The SDK exposes only the 6 endpoints on `CustomerController` itself, but API6
has three more controllers in `Services/Customers/`:

- **CustomerActivityController** (`/CustomerActivity`)
  - `GET /CustomerActivity/GetForCustomer` — paged customer activity feed
  - `GET /CustomerActivity/{id}`
- **CustomerFieldController** (`/CustomerField`) — 6 endpoints, full CRUD
- **CustomerInvoiceFieldController** (`/CustomerInvoiceField`) — 6 endpoints, full CRUD

Total: **14 endpoints** that belong logically to "customer" but have no SDK
binding. Add them as sub-namespaces on the existing `customer` module
(mirroring how `offer` bundles its offer-currency methods).

### Endpoints inside completed modules

Based on the verification pass against the controllers, these SDK modules
cover the corresponding API6 controller fully:

- `accommodation_product` (13/13, across the three controllers)
- `contact_person` (10/10)
- `office` (2/2)
- `offer` (10/10, incl. AddCurrencyToOffer / UpdateOfferCurrency / DeleteOfferCurrency)
- `product` (15/15, incl. ConfirmProduct, Add/Update/DeletePrice, transport ticket attach/detach)
- `product_group` (7/7)
- `project` (5/5)
- `statistics` (1/1)
- `supplier` (7/7)

## Adding a new module

Each new module follows the same shape as the existing ones — thin async
methods that call `self._http.{get,post,put,delete}` with the API6 route,
plus matching Pydantic models.

Reference implementations:

- Module template — `src/qondor_api_sdk/modules/offer.py`
- Model template — `src/qondor_api_sdk/models/offer.py`
- Module with multiple controllers under one resource group —
  `src/qondor_api_sdk/modules/accommodation_product.py`

Wiring checklist for a new module:

1. Add the API6 endpoints as methods in `src/qondor_api_sdk/modules/<name>.py`.
2. Add request/response models in `src/qondor_api_sdk/models/<name>.py` and
   re-export them from `src/qondor_api_sdk/models/__init__.py`.
3. Register the resource-group prefix in `src/qondor_api_sdk/client.py`
   (`_RESOURCE_GROUPS`) and instantiate the module in `QondorClient.__init__`.
4. Add unit tests under `tests/test_<name>_module.py` (mocked with
   `pytest_httpx`) and an integration test under
   `tests/integration/test_<name>.py` (gated on `QONDOR_SUBSCRIPTION_KEY`).
5. Update the table at the top of this file.

## Sources

- API6 controllers — `Qondor/Qondor.API6/Services/<Area>/*Controller.cs`
- SDK modules — `src/qondor_api_sdk/modules/`
- Resource-group registry — `src/qondor_api_sdk/client.py`
