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

Several JSON Schema compatibility issues were resolved.

### Issue 1 — Unsupported Constraints

Constraints such as:

```text
exclusiveMinimum
```

were removed from the LLM-facing schema.

Business validation remains in Pydantic.

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

### Issue 3 — Required Fields

Groq strict structured outputs requires every property to be included in `required`.

Therefore:

```python
diet: str | None
budget: float | None
```

are required fields that may still contain:

```json
null
```

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

# Day 2 — Next

The next implementation phase is the actual agent layer.

Planned:

```text
search_products()
check_availability()
compare_prices()
calculate_delivery()
optimize_basket()
```

Then integrate these tools with the LLM.

---

# Day 3

Planned:

- complete agent workflow
- basket optimization
- database integration
- frontend integration
- end-to-end shopping flow

---

# Day 4

Planned:

- testing
- error handling
- UI polish
- deployment
- README completion
- final documentation
- demo preparation