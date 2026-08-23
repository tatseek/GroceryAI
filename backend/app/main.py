from fastapi import FastAPI

from app.api.search import router as search_router
from app.api.agent import router as agent_router

app = FastAPI(
    title="GroceryAI API",
    description="AI-powered multi-provider grocery optimization API",
    version="0.1.0",
)


app.include_router(search_router)
app.include_router(agent_router)

@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
    }