from fastapi import APIRouter
from pydantic import BaseModel

from app.services.requirement_service import RequirementService


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"],
)


class RequirementRequest(BaseModel):
    request: str


requirement_service = RequirementService()


@router.post("/parse")
async def parse_requirements(
    body: RequirementRequest,
):
    requirements = await requirement_service.parse(
        body.request
    )

    return requirements