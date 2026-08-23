# Development Setup

## Prerequisites

Install:

- Python 3.x
- Git
- PostgreSQL/Supabase account
- Node.js
- npm
- VS Code or another IDE

---

# Backend Setup

Move into the backend directory:

```bash
cd backend
```

---

## Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```powershell
pip install -r requirements.txt
```

If adding a new dependency:

```powershell
pip install <package>
```

Then update:

```powershell
pip freeze > requirements.txt
```

---

# Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=your_database_url

SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_publishable_key

GROQ_API_KEY=your_groq_api_key
```

Never commit the real `.env` file.

---

# Database

The project uses PostgreSQL hosted through Supabase.

After configuring the database connection:

```powershell
alembic upgrade head
```

Check migration state:

```powershell
alembic current
```

---

# Run Backend

From:

```text
backend/
```

run:

```powershell
uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically provides Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Test Requirement Parsing

Endpoint:

```text
POST /api/agent/parse
```

Example request:

```json
{
  "request": "I need vegetarian groceries for 4 people for 5 days under ₹2000."
}
```

Expected response structure:

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

# Common Development Commands

Start backend:

```powershell
uvicorn app.main:app --reload
```

Run migrations:

```powershell
alembic upgrade head
```

Create migration:

```powershell
alembic revision --autogenerate -m "description"
```

Check migration:

```powershell
alembic current
```

Migration history:

```powershell
alembic history
```

---

# Environment Security

Never commit:

```text
.env
API keys
database passwords
service account credentials
private keys
```

Use:

```text
.env.example
```

for documenting required variables.