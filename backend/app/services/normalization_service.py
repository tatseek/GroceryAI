import re
from decimal import Decimal

from app.providers.base import ProviderProduct


def normalize_text(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


def normalize_unit(
    quantity: Decimal,
    unit: str,
) -> tuple[Decimal, str]:

    unit = unit.lower().strip()

    if unit == "ml":
        return quantity / Decimal("1000"), "L"

    if unit == "g":
        return quantity / Decimal("1000"), "kg"

    if unit in {"l", "litre", "liter", "litres", "liters"}:
        return quantity, "L"

    if unit in {"kg", "kilogram", "kilograms"}:
        return quantity, "kg"

    return quantity, unit


def normalize_product(product: ProviderProduct) -> ProviderProduct:
    quantity, unit = normalize_unit(
        product.quantity,
        product.unit,
    )

    return ProviderProduct(
        provider=product.provider,
        product_id=product.product_id,
        name=normalize_text(product.name),
        brand=(
            normalize_text(product.brand)
            if product.brand
            else None
        ),
        quantity=quantity,
        unit=unit,
        price=product.price,
        available=product.available,
        product_url=product.product_url,
    )