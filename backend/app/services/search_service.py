import asyncio

from app.providers import (
    BlinkitProvider,
    GroceryProvider,
    InstamartProvider,
    ProviderProduct,
    ZeptoProvider,
)
from app.services.normalization_service import normalize_product


class SearchService:

    def __init__(self) -> None:
        self.providers: list[GroceryProvider] = [
            BlinkitProvider(),
            ZeptoProvider(),
            InstamartProvider(),
        ]

    async def search(
        self,
        query: str,
    ) -> list[ProviderProduct]:

        query = query.strip()

        if not query:
            return []

        async def search_provider(
            provider: GroceryProvider,
        ) -> list[ProviderProduct]:

            try:
                products = await provider.search_products(query)

                return [
                    normalize_product(product)
                    for product in products
                ]

            except Exception:
                # One provider failing must not
                # bring down the complete search.
                return []

        results = await asyncio.gather(
            *[
                search_provider(provider)
                for provider in self.providers
            ]
        )

        return [
            product
            for provider_results in results
            for product in provider_results
        ]