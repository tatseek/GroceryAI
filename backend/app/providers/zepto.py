from decimal import Decimal

from app.providers.base import GroceryProvider, ProviderProduct


class ZeptoProvider(GroceryProvider):
    """Deterministic mock implementation of Zepto."""

    def __init__(self) -> None:
        self.products = [
            ProviderProduct(
                provider="zepto",
                product_id="ZP-MILK-001",
                name="Amul Taaza 1000ml",
                brand="Amul",
                quantity=Decimal("1000"),
                unit="ml",
                price=Decimal("65"),
                available=True,
            ),
            ProviderProduct(
                provider="zepto",
                product_id="ZP-RICE-001",
                name="India Gate Basmati Rice 5 kg",
                brand="India Gate",
                quantity=Decimal("5"),
                unit="kg",
                price=Decimal("499"),
                available=True,
            ),
            ProviderProduct(
                provider="zepto",
                product_id="ZP-POTATO-001",
                name="Potatoes 1 kg",
                brand=None,
                quantity=Decimal("1"),
                unit="kg",
                price=Decimal("35"),
                available=True,
            ),
            ProviderProduct(
                provider="zepto",
                product_id="ZP-TOMATO-001",
                name="Fresh Tomato 1kg",
                brand=None,
                quantity=Decimal("1"),
                unit="kg",
                price=Decimal("42"),
                available=True,
            ),
            ProviderProduct(
                provider="zepto",
                product_id="ZP-BREAD-001",
                name="Harvest Gold Bread 400 g",
                brand="Harvest Gold",
                quantity=Decimal("400"),
                unit="g",
                price=Decimal("42"),
                available=True,
            ),
        ]

    async def search_products(
        self,
        query: str,
    ) -> list[ProviderProduct]:

        query = query.strip().lower()

        if not query:
            return []

        return [
            product
            for product in self.products
            if query in product.name.lower()
        ]

    async def get_product(
        self,
        product_id: str,
    ) -> ProviderProduct | None:

        return next(
            (
                product
                for product in self.products
                if product.product_id == product_id
            ),
            None,
        )