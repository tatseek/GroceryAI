from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.controller import run_agent


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"],
)


class AgentChatRequest(BaseModel):
    message: str


class AgentChatResponse(BaseModel):
    response: str


@router.post(
    "/chat",
    response_model=AgentChatResponse,
)
async def agent_chat(
    request: AgentChatRequest,
) -> AgentChatResponse:

    response = await run_agent(
        request.message
    )

    return AgentChatResponse(
        response=response
    )