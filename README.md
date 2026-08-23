# GroceryAI 

GroceryAI is an AI-powered grocery shopping assistant that understands natural-language shopping requirements and helps users build an optimized grocery basket.

## Core Idea

Instead of manually searching multiple grocery stores, a user can describe what they need naturally:

> "I need vegetarian groceries for 4 people for 5 days under ₹2000."

GroceryAI extracts the requirements, searches available products, compares prices and availability, and builds an optimized basket.

---

## Architecture

```text
Frontend
   |
   v
FastAPI Backend
   |
   +---- AI Requirement Parser
   |
   +---- Agent / Tool Calling
   |
   +---- Product Search
   |
   +---- Price Comparison
   |
   +---- Availability
   |
   +---- Basket Optimizer
   |
   v
PostgreSQL / Supabase
```

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Supabase

### AI

- Groq
- `openai/gpt-oss-120b`
- Structured Outputs
- Tool Calling

### Frontend

- React / Next.js

---

## Current Features

- Natural-language grocery requirement parsing
- Structured LLM output
- Pydantic validation
- PostgreSQL database
- Supabase-hosted database
- AI provider abstraction

---

## Planned Features

- Product search
- Multi-store comparison
- Availability checking
- Delivery calculation
- Basket optimization
- AI shopping agent
- Final basket recommendations

---

## Project Structure

```text
GroceryAI/
├── backend/
├── frontend/
├── docs/
├── .gitignore
└── README.md
```

---

## Documentation

Detailed documentation is available in:

- [Architecture](docs/architecture.md)
- [AI Agent](docs/ai-agent.md)
- [Database](docs/database.md)
- [Setup](docs/setup.md)
- [Development Log](docs/development-log.md)

---

## Running the Backend

```bash
cd backend
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Environment Variables

Create a `.env` file inside `backend/`.

Required variables include:

```env
DATABASE_URL=
SUPABASE_URL=
SUPABASE_PUBLISHABLE_KEY=
GROQ_API_KEY=
```

Never commit `.env` or API credentials.

---

## Status

Currently under active development.

Day 1 foundation and Day 2 AI requirement parsing are complete.