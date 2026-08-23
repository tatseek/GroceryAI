# Database

## Database Provider

GroceryAI uses:

```text
PostgreSQL
```

The hosted PostgreSQL database is provided through:

```text
Supabase
```

Supabase provides the managed PostgreSQL infrastructure while the backend connects to PostgreSQL using its database connection string.

---

## Database Migrations

Database schema changes are managed using:

```text
Alembic
```

The migration files are located under:

```text
backend/alembic/
```

Typical commands:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

---

## Current Database Model

The database is designed around grocery products and shopping.

The planned core entities are:

```text
Product
   |
   +---- Store
   |
   +---- Product Availability
   |
   +---- Price

Basket
   |
   +---- Basket Items
```

The exact final schema will be documented here as the agent/product layer is implemented.

---

## Planned Product Data

A product should contain information such as:

```text
Product
├── id
├── name
├── category
├── brand
├── quantity
└── unit
```

---

## Planned Store Data

```text
Store
├── id
├── name
└── delivery information
```

---

## Planned Price Data

Price information will allow the application to compare the same or equivalent products across stores.

Conceptually:

```text
Product
   |
   +---- Store A → ₹120
   |
   +---- Store B → ₹110
   |
   +---- Store C → ₹125
```

The optimizer can then select the appropriate option based on:

- price
- availability
- delivery cost
- user budget
- other constraints

---

## Database Responsibilities

PostgreSQL is responsible for persistent application data.

The database should store:

- products
- stores
- prices
- availability
- shopping baskets
- basket items
- other application state

The LLM itself does not store application data.

---

## Security

Secrets such as database connection strings must never be committed to Git.

They belong in:

```text
.env
```

The `.env` file must remain in `.gitignore`.

A safe template should be provided through:

```text
.env.example
```

without actual credentials.