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

async def check_availability(query: str) -> dict:
    """
    Search products and return their availability
    across grocery providers.
    """

    products = await search_products(query)

    if not products:
        return {
            "query": query,
            "found": False,
            "products": [],
        }

    available = [
        product
        for product in products
        if product["available"]
    ]

    unavailable = [
        product
        for product in products
        if not product["available"]
    ]

    return {
        "query": query,
        "found": True,
        "available_count": len(available),
        "unavailable_count": len(unavailable),
        "available": available,
        "unavailable": unavailable,
    }

async def calculate_delivery(
    provider: str,
    subtotal: float,
) -> dict:
    """
    Calculate delivery cost for a provider based on
    the current basket subtotal.
    """

    # Temporary deterministic delivery rules.
    # These can later be replaced by real provider data.
    delivery_rules = {
        "blinkit": {
            "free_delivery_threshold": 299.0,
            "delivery_fee": 25.0,
        },
        "zepto": {
            "free_delivery_threshold": 299.0,
            "delivery_fee": 25.0,
        },
        "instamart": {
            "free_delivery_threshold": 299.0,
            "delivery_fee": 30.0,
        },
    }

    provider_code = provider.lower().strip()

    rule = delivery_rules.get(provider_code)

    if rule is None:
        return {
            "provider": provider,
            "subtotal": round(subtotal, 2),
            "delivery_fee": None,
            "total": None,
            "error": "Unknown provider",
        }

    if subtotal >= rule["free_delivery_threshold"]:
        delivery_fee = 0.0
    else:
        delivery_fee = rule["delivery_fee"]

    total = subtotal + delivery_fee

    return {
        "provider": provider_code,
        "subtotal": round(subtotal, 2),
        "delivery_fee": round(delivery_fee, 2),
        "total": round(total, 2),
        "free_delivery": delivery_fee == 0.0,
    }

async def optimize_basket(
    queries: list[str],
    budget: float | None = None,
) -> dict:
    """
    Find the cheapest single-provider basket for the
    requested grocery items, including delivery charges.
    """

    provider_products: dict[str, list[dict]] = {}

    for query in queries:
        products = await search_products(query)

        for product in products:
            if not product["available"]:
                continue

            provider = product["provider"]

            if provider not in provider_products:
                provider_products[provider] = []

            provider_products[provider].append(
                {
                    "query": query,
                    **product,
                }
            )

    if not provider_products:
        return {
            "found": False,
            "message": "No available products found.",
            "baskets": [],
        }

    baskets = []

    for provider, products in provider_products.items():

        selected_items = []
        subtotal = 0.0
        missing_items = []

        for query in queries:
            matches = [
                product
                for product in products
                if product["query"] == query
            ]

            if not matches:
                missing_items.append(query)
                continue

            cheapest = min(
                matches,
                key=lambda product: product["price"],
            )

            selected_items.append(cheapest)
            subtotal += cheapest["price"]

        delivery = await calculate_delivery(
            provider,
            subtotal,
        )

        total = delivery["total"]

        baskets.append(
            {
                "provider": provider,
                "items": selected_items,
                "subtotal": round(subtotal, 2),
                "delivery_fee": delivery["delivery_fee"],
                "total": total,
                "missing_items": missing_items,
                "complete": len(missing_items) == 0,
            }
        )

    complete_baskets = [
        basket
        for basket in baskets
        if basket["complete"]
    ]

    if complete_baskets:
        baskets_to_compare = complete_baskets
    else:
        baskets_to_compare = baskets

    baskets_to_compare.sort(
        key=lambda basket: (
            basket["total"] is None,
            basket["total"] or float("inf"),
        )
    )

    best_basket = (
        baskets_to_compare[0]
        if baskets_to_compare
        else None
    )

    within_budget = (
        best_basket is not None
        and best_basket["total"] is not None
        and (
            budget is None
            or best_basket["total"] <= budget
        )
    )

    return {
        "found": best_basket is not None,
        "budget": budget,
        "within_budget": within_budget,
        "best_basket": best_basket,
        "alternatives": baskets_to_compare[1:],
    }

