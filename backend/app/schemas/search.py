from decimal import Decimal

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=100,
    )


class SearchProductResponse(BaseModel):
    provider: str
    product_id: str
    name: str
    brand: str | None
    quantity: Decimal
    unit: str
    price: Decimal
    available: bool
    product_url: str | None = None


class SearchResponse(BaseModel):
    query: str
    count: int
    products: list[SearchProductResponse]