import json
from typing import Any

from groq import AsyncGroq

from app.ai.base import AIProvider
from app.core.config import settings


class GroqProvider(AIProvider):

    def __init__(self) -> None:
        self.client = AsyncGroq(
            api_key=settings.groq_api_key
        )

        self.model = "openai/gpt-oss-120b"

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Any,
    ) -> dict[str, Any]:

        schema = response_schema.model_json_schema()

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a structured data extraction "
                        "assistant. Follow the requested JSON "
                        "schema exactly."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "grocery_requirements",
                    "strict": True,
                    "schema": schema,
                },
            },
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "Groq returned an empty response."
            )

        return json.loads(content)

    async def generate_text(
        self,
        prompt: str,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "Groq returned an empty response."
            )

        return content