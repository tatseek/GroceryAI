from typing import Any

from google import genai
from google.genai import types

from app.ai.base import AIProvider
from app.core.config import settings


class GeminiProvider(AIProvider):

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

        self.model = "gemini-3.6-flash"

    async def generate_structured(
        self,
        prompt: str,
        response_schema: dict[str, Any],
    ) -> dict[str, Any]:

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        import json

        return json.loads(response.text)

    async def generate_text(
        self,
        prompt: str,
    ) -> str:

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        return response.text