import json

from app.agent.tools import search_products
from app.core.config import settings
from groq import AsyncGroq


client = AsyncGroq(
    api_key=settings.groq_api_key,
)


SEARCH_PRODUCTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": (
            "Search grocery products across available "
            "grocery providers. Use this when the user "
            "needs current product, price, or availability information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The grocery product or item to search for, "
                        "such as milk, rice, bread, or eggs."
                    ),
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}


async def run_agent(user_message: str) -> str:
    response = await client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are GroceryAI, a grocery shopping assistant. "
                    "Use the available tools whenever product information "
                    "is required. Do not invent product prices or availability."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        tools=[SEARCH_PRODUCTS_TOOL],
        tool_choice="auto",
    )

    message = response.choices[0].message

    # No tool call: return the model's normal response.
    if not message.tool_calls:
        return message.content or ""

    tool_messages = []

    for tool_call in message.tool_calls:
        if tool_call.function.name == "search_products":
            arguments = json.loads(
                tool_call.function.arguments
            )

            result = await search_products(
                arguments["query"]
            )

            tool_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        default=str,
                    ),
                }
            )

    # Send tool results back to Groq.
    final_response = await client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are GroceryAI, a grocery shopping assistant. "
                    "Use tool results to answer the user. "
                    "Never invent prices or availability."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
            message,
            *tool_messages,
        ],
    )

    return (
        final_response.choices[0].message.content
        or ""
    )