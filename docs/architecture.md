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
    ├── ai/
    │   ├── base.py
    │   ├── groq.py
    │   └── gemini.py
    │
    ├── api/
    │   └── agent.py
    │
    ├── core/
    │   └── config.py
    │
    ├── schemas/
    │   └── agent.py
    │
    ├── services/
    │   └── requirement_service.py
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

### In Progress

- Product search tools
- Availability tools
- Price comparison
- Basket optimization
- Agent tool calling

### Planned

- Frontend
- Complete shopping workflow
- Error handling
- Testing
- Deployment