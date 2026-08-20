from decimal import Decimal

from app.providers.base import GroceryProvider, ProviderProduct


class BlinkitProvider(GroceryProvider):
    """Deterministic mock implementation of Blinkit."""

    def __init__(self) -> None:
        self.products = [
            ProviderProduct(
                provider="blinkit",
                product_id="BL-MILK-001",
                name="Amul Taaza Milk 1L",
                brand="Amul",
                quantity=Decimal("1"),
                unit="L",
                price=Decimal("68"),
                available=True,
            ),
            ProviderProduct(
                provider="blinkit",
                product_id="BL-RICE-001",
                name="India Gate Basmati Rice 5kg",
                brand="India Gate",
                quantity=Decimal("5"),
                unit="kg",
                price=Decimal("520"),
                available=True,
            ),
            ProviderProduct(
                provider="blinkit",
                product_id="BL-POTATO-001",
                name="Potato 1kg",
                brand=None,
                quantity=Decimal("1"),
                unit="kg",
                price=Decimal("38"),
                available=True,
            ),
            ProviderProduct(
                provider="blinkit",
                product_id="BL-TOMATO-001",
                name="Tomato 1kg",
                brand=None,
                quantity=Decimal("1"),
                unit="kg",
                price=Decimal("45"),
                available=True,
            ),
            ProviderProduct(
                provider="blinkit",
                product_id="BL-BREAD-001",
                name="Harvest Gold White Bread 400g",
                brand="Harvest Gold",
                quantity=Decimal("400"),
                unit="g",
                price=Decimal("45"),
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