from decimal import Decimal

from app.providers.base import GroceryProvider, ProviderProduct


class InstamartProvider(GroceryProvider):
    """Deterministic mock implementation of Instamart."""

    def __init__(self) -> None:
        self.products = [
            ProviderProduct(
                provider="instamart",
                product_id="IS-MILK-001",
                name="Amul Taaza Milk 1 L",
                brand="Amul",
                quantity=Decimal("1"),
                unit="L",
                price=Decimal("70"),
                available=True,
            ),
            ProviderProduct(
                provider="instamart",
                product_id="IS-RICE-001",
                name="India Gate Basmati Rice 5kg",
                brand="India Gate",
                quantity=Decimal("5"),
                unit="kg",
                price=Decimal("510"),
                available=True,
            ),
            ProviderProduct(
                provider="instamart",
                product_id="IS-POTATO-001",
                name="Potato 1 KG",
                brand=None,
                quantity=Decimal("1"),
                unit="kg",
                price=Decimal("40"),
                available=True,
            ),
            ProviderProduct(
                provider="instamart",
                product_id="IS-TOMATO-001",
                name="Tomatoes 1 kg",
                brand=None,
                quantity=Decimal("1"),
                unit="kg",
                price=Decimal("48"),
                available=True,
            ),
            ProviderProduct(
                provider="instamart",
                product_id="IS-BREAD-001",
                name="Harvest Gold White Bread 400g",
                brand="Harvest Gold",
                quantity=Decimal("400"),
                unit="g",
                price=Decimal("44"),
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