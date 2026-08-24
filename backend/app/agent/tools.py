from app.services.search_service import SearchService


search_service = SearchService()


async def search_products(query: str) -> list[dict]:
    """
    Search grocery products across all configured providers.

    This is the tool exposed to the AI agent.
    The agent does not interact with provider implementations directly.
    """

    products = await search_service.search(query)

    return [
        {
            "provider": product.provider,
            "product_id": product.product_id,
            "name": product.name,
            "brand": product.brand,
            "quantity": product.quantity,
            "unit": product.unit,
            "price": float(product.price),
            "available": product.available,
            "product_url": product.product_url,
        }
        for product in products
    ]