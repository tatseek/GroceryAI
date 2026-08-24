# Development Log

This document tracks the development of GroceryAI across the four-day implementation period.

---

# Day 1 — Foundation

## Completed

### Project Structure

Created separate application areas for:

```text
backend/
frontend/
```

### Backend

Configured:

- FastAPI
- Python virtual environment
- application configuration
- API structure

### Database

Configured:

- PostgreSQL
- Supabase
- SQLAlchemy
- Alembic

### Migrations

Created the initial database migration for the core grocery tables.

Verified migration state using:

```bash
alembic current
```

and:

```bash
alembic history
```

### Environment

Configured environment variables through:

```text
.env
.env.example
```

Secrets are excluded from Git.

---

# Day 2 — AI Requirement Parsing

## AI Provider Abstraction

Created:

```text
app/ai/base.py
```

The application uses an `AIProvider` abstraction so the LLM provider can be replaced without changing business logic.

---

## Initial Gemini Integration

Gemini was initially selected as the LLM provider.

The implementation used structured JSON output.

However, the Google Cloud project associated with the Gemini API key had restricted API access and required billing.

Therefore, Gemini was not used for the final implementation.

---

## Gemini Schema Compatibility Issue

The initial Pydantic schema generated JSON Schema constraints such as:

```text
exclusiveMinimum
```

For example:

```json
{
  "exclusiveMinimum": 1
}
```

These constraints caused validation errors when the schema was passed to the Gemini API.

### Resolution

The LLM-facing schema was simplified by removing unsupported constraints.

Business-level validation remained in Pydantic rather than being enforced through the LLM JSON schema.

The resulting schema contained simpler types such as:

```json
{
  "people": {
    "type": "integer"
  },
  "days": {
    "type": "integer"
  },
  "quantity": {
    "type": "number"
  }
}
```

---

## Gemini Model Availability Issue

After resolving the schema issue, the configured Gemini model:

```text
models/gemini-2.5-flash
```

returned:

```text
404 NOT_FOUND
```

The API indicated that the configured model was no longer available to new users and recommended using a newer model.

The project subsequently encountered an access restriction.

---

## Gemini Permission Issue

The Gemini API then returned:

```text
403 PERMISSION_DENIED
```

indicating that the project had been denied access.

Because Gemini could not be reliably used for the project, an alternative provider was selected.

---

## Groq Integration

Switched the active AI provider to:

```text
Groq
```

Model:

```text
openai/gpt-oss-120b
```

Created:

```text
app/ai/groq.py
```

The existing AI provider abstraction allowed the provider to be replaced without changing the rest of the application architecture.

---

## Structured Output

Implemented structured requirement extraction.

User input:

```text
I need vegetarian groceries for 4 people for 5 days under ₹2000.
```

is converted into:

```json
{
  "people": 4,
  "days": 5,
  "diet": "vegetarian",
  "budget": 2000,
  "items": []
}
```

---

## Pydantic Validation

Created the `GroceryRequirements` schema.

Validation ensures:

- valid people count
- valid day count
- valid quantities
- valid budget
- valid item names
- valid units
- no unexpected fields

---

## Groq Schema Compatibility

Several JSON Schema compatibility issues were resolved while integrating structured output with Groq.

### Issue 1 — Unsupported Constraints

Constraints such as:

```text
exclusiveMinimum
```

were removed from the LLM-facing schema.

Business validation remains in Pydantic.

---

### Issue 2 — Additional Properties

Groq strict structured outputs requires:

```json
"additionalProperties": false
```

for object schemas.

Pydantic models were configured with:

```python
ConfigDict(extra="forbid")
```

This ensured that both the root model and nested objects generated compatible schemas.

---

### Issue 3 — Required Fields

Groq strict structured outputs requires every property to be included in the `required` array.

Therefore:

```python
diet: str | None
budget: float | None
```

are required fields that may still contain:

```json
null
```

This allowed the schema to remain strict while supporting requests where the user does not specify a diet or budget.

---

## Current Working Endpoint

The following endpoint is working:

```text
POST /api/agent/parse
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Day 3 — Agent Layer

## Agent Architecture

Day 3 focused on converting the requirement-parsing AI layer into an actual grocery shopping agent.

The agent uses Groq tool/function calling to decide which backend functionality should be executed.

The implemented tools are:

```text
search_products()
check_availability()
compare_prices()
calculate_delivery()
optimize_basket()
```

The architecture separates AI decision-making from deterministic business logic.

---

## Agent Controller

Implemented the agent controller responsible for:

1. receiving the user's request
2. sending the request to Groq
3. allowing Groq to select an appropriate tool
4. executing the selected backend tool
5. returning the tool result to Groq
6. generating the final user-facing response

The agent endpoint is:

```text
POST /api/agent/chat
```

---

## Product Search Tool

Implemented:

```text
search_products()
```

The tool uses the existing provider search infrastructure.

It searches across:

```text
Blinkit
Zepto
Instamart
```

and returns normalized product results.

The search functionality was already tested independently and was then exposed to the agent.

---

## Price Comparison Tool

Implemented:

```text
compare_prices()
```

The tool compares product prices across available providers.

The comparison considers:

- provider
- product
- price
- availability

This allows the agent to determine which provider offers a lower price for a requested product.

---

## Availability Tool

Implemented:

```text
check_availability()
```

The tool determines whether a requested product is available from a provider.

Unavailable products are excluded when building optimized baskets.

The tool was tested successfully.

---

## Delivery Calculation Tool

Implemented:

```text
calculate_delivery()
```

The tool calculates the estimated delivery cost for a provider based on the basket subtotal.

This is important because comparing only product prices can produce an incorrect result.

The actual basket cost must consider:

```text
product subtotal
+
delivery fee
=
final cost
```

The delivery calculation was tested successfully.

---

# Basket Optimization

Implemented:

```text
optimize_basket()
```

The optimizer is responsible for finding the cheapest valid grocery basket.

It considers:

- product prices
- product availability
- providers
- delivery charges
- user budget

The calculation is performed by backend code rather than the LLM.

The LLM is responsible for deciding when the optimization tool should be used.

---

## Initial Basket Optimization

The first implementation compared complete baskets from individual providers.

For example:

```text
Blinkit
├── Milk
├── Rice
└── Bread
```

could be compared against:

```text
Zepto
├── Milk
├── Rice
└── Bread
```

The final cost was calculated using:

```text
subtotal + delivery fee
```

---

## Multi-Provider Basket Optimization

The optimizer was then extended to evaluate baskets split across multiple providers.

For example:

```text
Blinkit
├── Milk
└── Bread

Zepto
└── Rice
```

The optimizer calculates:

```text
Blinkit subtotal
+ Blinkit delivery
+
Zepto subtotal
+ Zepto delivery
```

and compares this against single-provider baskets.

This prevents the system from assuming that selecting the cheapest individual product automatically produces the cheapest overall basket.

---

## Basket Combination Strategy

The optimizer evaluates possible provider assignments for the requested products.

For example, with:

```text
3 items
3 providers
```

there can be up to:

```text
3³ = 27
```

provider combinations.

This is small enough for exhaustive evaluation.

Each candidate basket is evaluated using:

```text
Product prices
+
Provider delivery charges
=
Final basket cost
```

The cheapest valid basket is selected.

---

# Budget-Aware Optimization

The optimizer supports an optional budget.

Example:

```text
I need milk, rice and bread under ₹250.
```

The optimizer evaluates candidate baskets against:

```text
budget = 250
```

If a basket is available within the budget, the cheapest valid basket is selected.

If no basket satisfies the budget, the cheapest available basket is returned with:

```json
{
  "within_budget": false
}
```

This allows the agent to communicate that the cheapest available basket exceeds the user's requested budget.

---

# Groq Tool Calling Issue — Nullable Budget

After connecting `optimize_basket()` to the Groq agent, Groq returned:

```text
Tool call validation failed:

/budget: expected number, but got null
```

The agent was correctly generating:

```json
{
  "queries": [
    "milk",
    "rice",
    "bread"
  ],
  "budget": null
}
```

However, the tool schema defined `budget` only as:

```json
{
  "type": "number"
}
```

Therefore Groq rejected the `null` value.

---

## Resolution

The tool schema was updated to allow both numbers and null:

```json
{
  "type": ["number", "null"]
}
```

The tool can therefore receive:

```json
{
  "budget": null
}
```

when no budget is specified.

It can also receive:

```json
{
  "budget": 250
}
```

when a budget is provided.

---

# Python Naming Collision During Optimization

While implementing multi-provider optimization, the following error occurred:

```text
TypeError: 'dict' object is not callable
```

The error occurred at:

```python
product(*choices_per_item)
```

The cause was a naming collision.

The module imported:

```python
from itertools import product
```

but the code also used:

```text
product
```

as a variable name.

This shadowed the imported `itertools.product` function.

---

## Resolution

The import was changed to:

```python
from itertools import product as cartesian_product
```

and the combination generation was changed to:

```python
for combination in cartesian_product(*choices_per_item):
```

After this change, the optimizer executed successfully.

---

# Agent Verification

The agent tools were individually tested:

```text
search_products()
compare_prices()
check_availability()
calculate_delivery()
optimize_basket()
```

The basket optimizer was also tested directly from the backend using:

```powershell
python -c "import asyncio; from app.agent.tools import optimize_basket; import pprint; pprint.pp(asyncio.run(optimize_basket(['milk', 'rice', 'bread'])))"
```

The optimizer returned successfully.

---

# Swagger Verification

The complete agent workflow was tested through FastAPI Swagger UI.

Verified endpoint:

```text
POST /api/agent/chat
```

The endpoint successfully:

1. receives a natural-language grocery request
2. allows Groq to select an appropriate tool
3. executes the selected backend tool
4. returns the tool result to Groq
5. generates the final response

---

# Current Agent Flow

```text
                         User
                           │
                           ▼
                         FastAPI
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
        Requirement Parser       Groq Agent
                 │                   │
                 │             ┌─────┴─────┐
                 │             │   Agent   │
                 │             │   Tools   │
                 │             └─────┬─────┘
                 │                   │
                 │       ┌───────────┼────────────┐
                 │       ▼           ▼            ▼
                 │   Search      Compare      Availability
                 │   Products     Prices         Check
                 │       │           │            │
                 │       └───────────┼────────────┘
                 │                   ▼
                 │           Basket Optimizer
                 │                   │
                 │           Delivery Calculator
                 │                   │
                 └───────────┬───────┘
                             ▼
                       SearchService
                             │
                    ┌────────┼────────┐
                    ▼        ▼        ▼
                 Blinkit   Zepto   Instamart
```

---

# Day 3 — Completed

The following functionality has been implemented and verified:

- Groq tool calling
- Product search
- Price comparison
- Availability checking
- Delivery calculation
- Budget-aware basket optimization
- Multi-provider basket optimization
- Agent integration
- Swagger verification

**Status: COMPLETE**

---

# Day 4 — Frontend & End-to-End Integration

Day 4 will focus on converting the working backend into the complete user-facing GroceryAI application.

## Planned

### Frontend

- Frontend application setup
- Grocery requirement input
- Natural-language shopping request
- API integration
- Loading states
- Error states
- Basket result UI
- Provider comparison
- Price breakdown
- Delivery charges
- Total basket cost
- Budget status

### End-to-End Integration

The intended final flow is:

```text
User
  ↓
Frontend
  ↓
Natural-language grocery request
  ↓
FastAPI
  ↓
Requirement Parsing
  ↓
Groq Agent
  ↓
Agent Tools
  ↓
Provider Search
  ↓
Basket Optimization
  ↓
Delivery Calculation
  ↓
Best Basket
  ↓
Frontend Result
```

### Testing

The final testing phase will cover:

- requirement parsing
- agent tool selection
- provider failures
- unavailable products
- missing products
- budget constraints
- single-provider baskets
- multi-provider baskets
- delivery calculations
- API errors
- frontend loading states
- frontend error states
- complete end-to-end shopping flow

### Deployment

The final application will be prepared for deployment.

Deployment areas:

```text
Frontend
Backend
PostgreSQL / Supabase
Environment variables
```

Production secrets will remain outside the repository.

### Final Documentation

The following documentation will be finalized:

```text
README.md
docs/setup.md
docs/architecture.md
docs/ai-agent.md
docs/database.md
docs/development-log.md
```

### Demo Preparation

The final stage will include:

- project cleanup
- README completion
- architecture review
- API verification
- end-to-end demo
- deployment verification

---

# Current Status

## Day 1

- Provider abstraction
- Blinkit, Zepto and Instamart adapters
- Product normalization
- Search API
- PostgreSQL/Supabase setup
- SQLAlchemy
- Alembic

**COMPLETE**

## Day 2

- Natural-language requirement parsing
- AI provider abstraction
- Groq LLM integration
- Structured requirement extraction
- Pydantic validation
- Groq schema compatibility fixes

**COMPLETE**

## Day 3

- Groq tool calling
- Product search tool
- Price comparison
- Availability checking
- Delivery calculation
- Budget-aware basket optimization
- Multi-provider basket optimization
- Agent integration
- Swagger verification

**COMPLETE**

## Day 4

- Frontend
- End-to-end integration
- UI/UX
- Testing
- Deployment
- Final documentation
- Demo preparation

**NEXT**