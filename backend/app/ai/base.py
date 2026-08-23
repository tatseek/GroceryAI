from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_schema: Any,
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError