from app.ai import GroqProvider
from app.ai.prompts import REQUIREMENT_PARSER_PROMPT
from app.schemas.agent import GroceryRequirements


class RequirementService:

    def __init__(self) -> None:
        self.ai_provider = GroqProvider()

    async def parse(
        self,
        user_request: str,
    ) -> GroceryRequirements:

        prompt = REQUIREMENT_PARSER_PROMPT.format(
            user_request=user_request
        )

        schema = GroceryRequirements.model_json_schema()

        result = await self.ai_provider.generate_structured(
            prompt=prompt,
            response_schema=GroceryRequirements,
        )

        return GroceryRequirements.model_validate(result)