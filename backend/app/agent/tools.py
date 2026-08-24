from app.services.search_service import SearchService
from itertools import product as cartesian_product

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
    Find the cheapest grocery basket, including the possibility
    of splitting items across multiple providers.
    """

    # 1. Search for every requested item

    item_results: dict[str, list[dict]] = {}

    for query in queries:
        products = await search_products(query)

        available_products = [
            product
            for product in products
            if product["available"]
        ]

        item_results[query] = available_products

    # 2. Check whether every requested item was found

    missing_items = [
        query
        for query in queries
        if not item_results.get(query)
    ]

    if missing_items:
        return {
            "found": False,
            "budget": budget,
            "missing_items": missing_items,
            "message": (
                "Some requested items are unavailable."
            ),
            "best_basket": None,
            "alternatives": [],
        }

    # 3. Build provider choices for every item

    choices_per_item = []

    for query in queries:
        choices = []

        for product in item_results[query]:
            choices.append(
                {
                    "query": query,
                    **product,
                }
            )

        choices_per_item.append(choices)

    # 4. Generate every possible provider assignment

    candidate_baskets = []

    for combination in cartesian_product(*choices_per_item):

        provider_groups: dict[str, list[dict]] = {}

        for item in combination:
            provider = item["provider"]

            if provider not in provider_groups:
                provider_groups[provider] = []

            provider_groups[provider].append(item)

        # 5. Calculate subtotal + delivery for every provider

        provider_breakdown = []

        final_total = 0.0
        total_subtotal = 0.0
        total_delivery = 0.0

        for provider, items in provider_groups.items():

            subtotal = sum(
                float(item["price"])
                for item in items
            )

            delivery = await calculate_delivery(
                provider,
                subtotal,
            )

            delivery_fee = float(
                delivery["delivery_fee"]
            )

            provider_total = subtotal + delivery_fee

            total_subtotal += subtotal
            total_delivery += delivery_fee
            final_total += provider_total

            provider_breakdown.append(
                {
                    "provider": provider,
                    "items": items,
                    "subtotal": round(subtotal, 2),
                    "delivery_fee": round(
                        delivery_fee,
                        2,
                    ),
                    "total": round(
                        provider_total,
                        2,
                    ),
                }
            )

        # 6. Check budget

        within_budget = (
            budget is None
            or final_total <= budget
        )

        candidate_baskets.append(
            {
                "providers": provider_breakdown,
                "subtotal": round(
                    total_subtotal,
                    2,
                ),
                "delivery_fee": round(
                    total_delivery,
                    2,
                ),
                "total": round(
                    final_total,
                    2,
                ),
                "provider_count": len(
                    provider_groups
                ),
                "within_budget": within_budget,
            }
        )

    # 7. Prefer baskets within budget

    affordable_baskets = [
        basket
        for basket in candidate_baskets
        if basket["within_budget"]
    ]

    baskets_to_compare = (
        affordable_baskets
        if affordable_baskets
        else candidate_baskets
    )

    # 8. Cheapest basket wins

    baskets_to_compare.sort(
        key=lambda basket: basket["total"]
    )

    best_basket = baskets_to_compare[0]

    return {
        "found": True,
        "budget": budget,
        "within_budget": best_basket["within_budget"],
        "best_basket": best_basket,
        "alternatives": baskets_to_compare[1:5],
        "missing_items": [],
    }

