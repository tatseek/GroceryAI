# GroceryAI Architecture

## Overview

GroceryAI is an AI-powered grocery shopping assistant.

The application accepts a natural-language grocery request, extracts structured requirements using an LLM, and uses those requirements to drive product search, price comparison, availability checks, and basket optimization.

The system is designed around a provider-independent AI abstraction so that the underlying LLM provider can be replaced without changing the business logic.

---

## High-Level Architecture

```
                    User
                     |
                     v
              Frontend Application
                     |
                     | HTTP/JSON
                     v
              FastAPI Backend
                     |
          +----------+----------+
          |                     |
          v                     v
   Requirement Service       Agent Layer
          |                     |
          v                     |
      AI Provider               |
          |                     |
          v                     |
     Groq / LLM                 |
                                |
                    +-----------+-----------+
                    |           |           |
                    v           v           v
              Product Search  Price      Availability
                              Compare       Check
                    |           |           |
                    +-----------+-----------+
                                |
                                v
                       Basket Optimizer
                                |
                                v
                         Final Basket
```

---

## Backend Structure

```text
backend/
└── app/
    ├── agent/
    │   ├── __init__.py
    │   ├── controller.py
    │   └── tools.py
    │
    ├── ai/
    │   ├── base.py
    │   ├── groq.py
    |   ├── prompts.py
    │   └── gemini.py
    │
    ├── api/
    │   └── agent.py
    |   ├── agent_chat.py
    │   └── search.py
    │
    ├── core/
    │   └── config.py
    │
    ├── models/
    │   ├── product.py
    │   ├── provider.py
    │   └── provider_product.py
    |
    ├── providers/
    │   ├── blinkit.py
    │   ├── zepto.py
    │   └── instamart.py
    │
    ├── schemas/
    │   └── agent.py
    │
    ├── services/
    │   └── requirement_service.py
    │   ├── search_service.py
    │   └── normalization_service.py
    │
    └── main.py
```

---

## AI Provider Abstraction

The provider interface is defined in:

```text
app/ai/base.py
```

Current implementation:

```text
AIProvider
    |
    └── GroqProvider
```

A Gemini provider was also initially implemented but is currently not active.

This allows the application to switch providers without changing the requirement parsing service.

---

## Requirement Parsing Flow

A user might enter:

```text
I need vegetarian groceries for 4 people
for 5 days under ₹2000.
```

The request flows through:

```text
HTTP Request
     |
     v
POST /api/agent/parse
     |
     v
RequirementService
     |
     v
GroqProvider
     |
     v
LLM Structured Output
     |
     v
GroceryRequirements
     |
     v
Pydantic Validation
```

The result is a validated structured object.

Example:

```json
{
  "people": 4,
  "days": 5,
  "diet": "vegetarian",
  "budget": 2000,
  "items": [
    {
      "name": "rice",
      "quantity": 5,
      "unit": "kg"
    }
  ]
}
```

---

## Design Principles

### Separation of Concerns

The system separates:

- API handling
- AI interaction
- requirement parsing
- database access
- agent tools
- basket optimization

### Provider Independence

The application uses an `AIProvider` abstraction instead of coupling services directly to Groq.

### Deterministic Business Logic

The LLM is responsible for language understanding and agent decisions.

Important calculations such as:

- total price
- delivery cost
- savings
- basket cost

should be handled deterministically by application code.

The LLM should not be trusted to perform critical numerical calculations.

---

## Current Status

### Completed

- FastAPI backend
- PostgreSQL/Supabase database
- SQLAlchemy/Alembic setup
- AI provider abstraction
- Groq integration
- Structured requirement extraction
- Pydantic validation
- Product search
- Availability checking
- Price comparison
- Delivery calculation
- Agent tool calling
- Budget-aware basket optimization
- Multi-provider basket optimization

### In Progress

- Frontend
- End-to-end shopping workflow

### Planned

- UI/UX improvements
- Error handling
- Testing
- Deployment