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

async def compare_prices(query: str) -> dict:
    """
    Search products across providers and compare their prices.

    Price comparison is performed deterministically by the backend.
    """

    products = await search_products(query)

    available_products = [
        product
        for product in products
        if product["available"]
    ]

    if not available_products:
        return {
            "query": query,
            "found": False,
            "message": "No available products found.",
            "products": [],
        }

    sorted_products = sorted(
        available_products,
        key=lambda product: product["price"],
    )

    cheapest = sorted_products[0]
    most_expensive = sorted_products[-1]

    savings = (
        most_expensive["price"]
        - cheapest["price"]
    )

    return {
        "query": query,
        "found": True,
        "cheapest": cheapest,
        "most_expensive": most_expensive,
        "savings": round(savings, 2),
        "products": sorted_products,
    }