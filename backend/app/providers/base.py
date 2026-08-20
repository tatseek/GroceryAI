from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProviderProduct:
    provider: str
    product_id: str
    name: str
    brand: str | None
    quantity: Decimal
    unit: str
    price: Decimal
    available: bool
    product_url: str | None = None


class GroceryProvider(ABC):
    """Base interface for all grocery providers."""

    @abstractmethod
    async def search_products(
        self,
        query: str,
    ) -> list[ProviderProduct]:
        """Search products from the provider."""
        raise NotImplementedError

    @abstractmethod
    async def get_product(
        self,
        product_id: str,
    ) -> ProviderProduct | None:
        """Get a single product by provider-specific ID."""
        raise NotImplementedError