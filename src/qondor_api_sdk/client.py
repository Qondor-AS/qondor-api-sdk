"""QondorClient -- HTTP client with auth injection for Qondor API.

Auth is injected via a configurable header (default ``Ocp-Apim-Subscription-Key``).
When ``use_resource_group_prefixes`` is enabled (the default), each module path is
prefixed with its resource group (e.g. ``/Customer/v1/…``).

``X-OnBehalfOf-Token`` is included when a delegated JWT is provided.
"""

from __future__ import annotations

import httpx

from .modules.contact_person import ContactPersonModule
from .modules.customer import CustomerModule
from .modules.offer import OfferModule
from .modules.office import OfficeModule
from .modules.product import ProductModule
from .modules.product_group import ProductGroupModule
from .modules.project import ProjectModule
from .modules.statistics import StatisticsModule
from .modules.supplier import SupplierModule

# Resource group -> versioned prefix mapping (used when use_resource_group_prefixes=True)
_RESOURCE_GROUPS: dict[str, str] = {
    "Customer": "Customer/v1",
    "Project": "Project/v1",
    "Offer": "Offer/v1",
    "Product": "Product/v1",
    "ProductGroup": "ProductGroup/v1",
    "Supplier": "Supplier/v1",
    "Office": "Office/v1",
    "ContactPerson": "ContactPerson/v1",
    "Statistics": "Statistics/v1",
}


class QondorClient:
    """HTTP client for Qondor API.

    Injects auth headers on every request. Not safe to serialize.

    The ``auth_header`` parameter controls which HTTP header carries the
    subscription key (default ``Ocp-Apim-Subscription-Key``).  Set
    ``use_resource_group_prefixes=False`` to disable resource-group path
    prefixes.
    """

    def __init__(
        self,
        base_url: str,
        subscription_key: str,
        on_behalf_of_jwt: str = "",
        *,
        auth_header: str = "Ocp-Apim-Subscription-Key",
        use_resource_group_prefixes: bool = True,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._use_resource_group_prefixes = use_resource_group_prefixes

        auth_headers: dict[str, str] = {}
        if on_behalf_of_jwt:
            auth_headers["X-OnBehalfOf-Token"] = on_behalf_of_jwt
        auth_headers[auth_header] = subscription_key

        self._http = httpx.AsyncClient(
            base_url=self._base_url,
            headers=auth_headers,
            timeout=30.0,
        )

        # Initialize modules with correct URL prefixes
        self.customer = CustomerModule(self._http, self._module_prefix("Customer"))
        self.project = ProjectModule(self._http, self._module_prefix("Project"))
        self.offer = OfferModule(self._http, self._module_prefix("Offer"))
        self.product_group = ProductGroupModule(self._http, self._module_prefix("ProductGroup"))
        self.product = ProductModule(self._http, self._module_prefix("Product"))
        self.supplier = SupplierModule(self._http, self._module_prefix("Supplier"))
        self.office = OfficeModule(self._http, self._module_prefix("Office"))
        self.contact_person = ContactPersonModule(self._http, self._module_prefix("ContactPerson"))
        self.statistics = StatisticsModule(self._http, self._module_prefix("Statistics"))

    def _module_prefix(self, resource_group: str) -> str:
        """Build per-module URL prefix.

        With prefixes:    ``/Customer/v1``  (prepended to controller paths)
        Without prefixes: ``""``            (controller paths used as-is)
        """
        if self._use_resource_group_prefixes:
            return f"/{_RESOURCE_GROUPS[resource_group]}"
        return ""

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()
