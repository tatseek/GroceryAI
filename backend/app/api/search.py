from fastapi import APIRouter

from app.schemas.search import (
    SearchProductResponse,
    SearchRequest,
    SearchResponse,
)
from app.services.search_service import SearchService


router = APIRouter(
    prefix="/api/search",
    tags=["Search"],
)


search_service = SearchService()


@router.post(
    "",
    response_model=SearchResponse,
)
async def search_products(
    request: SearchRequest,
) -> SearchResponse:

    products = await search_service.search(
        request.query
    )

    return SearchResponse(
        query=request.query,
        count=len(products),
        products=[
            SearchProductResponse(
                provider=product.provider,
                product_id=product.product_id,
                name=product.name,
                brand=product.brand,
                quantity=product.quantity,
                unit=product.unit,
                price=product.price,
                available=product.available,
                product_url=product.product_url,
            )
            for product in products
        ],
    )