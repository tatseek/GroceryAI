import json

from app.agent.tools import (
    calculate_delivery,
    check_availability,
    optimize_basket,
    compare_prices,
    search_products,
    )
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

COMPARE_PRICES_TOOL = {
    "type": "function",
    "function": {
        "name": "compare_prices",
        "description": (
            "Search available grocery products across providers "
            "and compare their prices. Use this when the user "
            "asks which provider has the cheapest option."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The grocery product to compare, "
                        "such as milk, rice, or bread."
                    ),
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}

CHECK_AVAILABILITY_TOOL = {
    "type": "function",
    "function": {
        "name": "check_availability",
        "description": (
            "Check whether a grocery product is currently "
            "available across grocery providers."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The grocery product to check, "
                        "such as milk, rice, bread, or eggs."
                    ),
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}

CALCULATE_DELIVERY_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_delivery",
        "description": (
            "Calculate the final grocery basket cost for a provider "
            "including delivery charges."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "provider": {
                    "type": "string",
                    "description": "The grocery provider.",
                },
                "subtotal": {
                    "type": "number",
                    "description": "The basket subtotal before delivery.",
                },
            },
            "required": [
                "provider",
                "subtotal",
            ],
            "additionalProperties": False,
        },
    },
}

OPTIMIZE_BASKET_TOOL = {
    "type": "function",
    "function": {
        "name": "optimize_basket",
        "description": (
            "Find the cheapest grocery basket for a list of requested "
            "items. The calculation includes product prices and "
            "delivery charges. Use this when the user asks for the "
            "best, cheapest, or most affordable grocery basket."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "queries": {
                    "type": "array",
                    "description": "The grocery items requested by the user.",
                    "items": {
                        "type": "string",
                    },
                },
                "budget": {
                    "type": ["number", "null"],
                    "description": "Optional maximum budget. Use null if no budget was specified.",
                },
            },
            "required": [
                "queries",
                "budget",
            ],
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
        tools=[
            SEARCH_PRODUCTS_TOOL,
            COMPARE_PRICES_TOOL,
            CHECK_AVAILABILITY_TOOL,
            CALCULATE_DELIVERY_TOOL,
            OPTIMIZE_BASKET_TOOL,
            ],
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
        elif tool_call.function.name == "compare_prices":
            arguments = json.loads(
                tool_call.function.arguments
            )

            result = await compare_prices(
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
        elif tool_call.function.name == "check_availability":
            arguments = json.loads(
                tool_call.function.arguments
            )

            result = await check_availability(
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
        elif tool_call.function.name == "calculate_delivery":
            arguments = json.loads(
                tool_call.function.arguments
            )

            result = await calculate_delivery(
                arguments["provider"],
                arguments["subtotal"],
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
        elif tool_call.function.name == "optimize_basket":
            arguments = json.loads(
                tool_call.function.arguments
            )

            result = await optimize_basket(
                arguments["queries"],
                arguments.get("budget"),
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