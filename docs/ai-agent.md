# AI Agent

## Overview

GroceryAI uses an LLM to understand natural-language grocery requirements and later coordinate application tools to build an optimized grocery basket.

The AI layer is intentionally separated from the rest of the application.

---

## Current LLM Provider

The current provider is:

```text
Groq
```

Current model:

```text
openai/gpt-oss-120b
```

The integration is implemented in:

```text
backend/app/ai/groq.py
```

---

## AI Provider Interface

The provider abstraction is implemented in:

```text
backend/app/ai/base.py
```

The interface exposes:

```python
generate_structured()
generate_text()
```

This means application services don't need to know whether the underlying provider is:

- Groq
- Gemini
- OpenAI
- another provider

---

## Structured Requirement Extraction

The first AI task is converting natural language into structured requirements.

Example input:

```text
I need vegetarian groceries for 4 people
for 5 days under ₹2000.
```

The LLM produces structured data:

```json
{
  "people": 4,
  "days": 5,
  "diet": "vegetarian",
  "budget": 2000,
  "items": []
}
```

The result is validated using Pydantic.

---

## GroceryRequirements

The schema is defined in:

```text
backend/app/schemas/agent.py
```

Current structure:

```text
GroceryRequirements
├── people
├── days
├── diet
├── budget
└── items
      └── GroceryItem
            ├── name
            ├── quantity
            └── unit
```

---

## Validation

Pydantic validates the LLM response before the application uses it.

Validation includes:

- positive number of people
- positive number of days
- positive grocery quantity
- non-negative budget
- non-empty grocery item names
- non-empty units
- rejection of unexpected fields

This prevents malformed LLM output from directly entering business logic.

---

## Agent Tools

The planned agent will have access to application tools.

Planned tools:

```text
search_products()
check_availability()
compare_prices()
calculate_delivery()
optimize_basket()
```

These functions will be implemented by our backend.

The LLM should not directly access the database.

Instead:

```text
LLM
 |
 | tool call
 v
Backend Tool
 |
 v
Database / Application Logic
 |
 v
Tool Result
 |
 v
LLM
```

---

## Tool Calling

The agent will use function/tool calling to decide when application capabilities are required.

For example:

```text
User:
Find rice and dal under ₹500.
```

The agent may decide to call:

```text
search_products()
```

The backend executes the function and returns product data.

The LLM can then reason over those results.

---

## Deterministic Logic

The LLM will not be responsible for critical calculations.

For example:

```text
product price
+
delivery fee
-
discount
=
final cost
```

will be calculated by backend code.

Similarly, basket optimization will be implemented as deterministic application logic.

The LLM's responsibility is primarily:

1. Understand user intent.
2. Decide which tools are required.
3. Interpret tool results.
4. Explain the final recommendation.

---

## Current AI Flow

```text
User Request
     |
     v
Requirement Parser
     |
     v
GroceryRequirements
     |
     v
Agent
     |
     +----> search_products()
     |
     +----> check_availability()
     |
     +----> compare_prices()
     |
     +----> optimize_basket()
     |
     v
Final Basket
```

---

## Provider Replacement

Because the system uses:

```text
AIProvider
```

the LLM provider can be changed without rewriting the services.

For example:

```text
GroqProvider
      ↓
OpenAIProvider
```

would only require a new provider implementation and configuration changes.