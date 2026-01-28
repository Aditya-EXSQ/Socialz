# Social Media Backend — Architecture & Flow Guide

> **Goal of this document**
> This README explains **how the system thinks**, not just what the code does.
> Use it for **revision, learning, and architectural recall**, not onboarding users.

---

## 1. High-Level Philosophy

This backend follows three non-negotiable principles:

1. **One-directional dependency flow**
2. **Database is the source of truth**
3. **Business logic lives in services, not controllers**

Everything else is a consequence of these.

---

## 2. Request Lifecycle (End-to-End Flow)

Every HTTP request follows **this exact path**:

```
Client
  ↓
Middleware (JWT auth)
  ↓
Middleware (DB session)
  ↓
Router
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
  ↑
Service (commit / raise)
  ↑
Controller (format response)
  ↑
Global Error Handler (if exception)
  ↑
Client
```

**Key idea:**

> Each layer solves *one* problem and then gets out of the way.

---

## 3. Dependency Rules (Read This Twice)

Allowed direction:

```
router → controller → service → repository → model
```

Forbidden:

* Controller accessing database directly
* Service importing HTTP / FastAPI objects
* Repository containing business logic
* Models knowing about anything else

If you break this, the architecture collapses.

---

## 4. Folder-by-Folder Mental Model

### `app/main.py`

**Purpose**

* Application bootstrap
* System wiring

**Responsibilities**

* Create FastAPI app
* Register routers
* Attach middleware
* Register global error handler

**Never**

* Business logic
* Database queries

Think of this as **main() in C**.

---

### `config/`

**Purpose**

* Environment & infrastructure configuration

**Contains**

* `settings.py`: env vars, DB URLs, JWT secrets
* `logging.py`: logging format & levels

**Mental model**

> Configuration should change between environments without touching code.

---

### `db/`

**Purpose**

* Database lifecycle management

**Files**

* `engine.py`: creates SQLAlchemy engine
* `session.py`: session factory
* `base.py`: declarative base
* `migrations/`: Alembic migrations

**Key rule**

> A DB session is created **per request**, not per query.

---

### `models/`

**Purpose**

* Database schema definition

**Contains**

* ORM models only
* Constraints
* Relationships

**Allowed**

* Columns
* Indexes
* Foreign keys
* Check constraints

**Forbidden**

* Business logic
* Validation logic
* HTTP concerns

Mental model:

> These files describe **what is allowed to exist** in the database.

---

### `repositories/`

**Purpose**

* Data access layer

**Responsibilities**

* Read/write data
* Express queries
* Return ORM objects

**Characteristics**

* Accept a `Session`
* No commits
* No authorization
* No business rules

Example:

> “Fetch post by ID”
> “Insert a like row”

Repositories answer:
**“How do I talk to the database?”**

---

### `services/`

**Purpose**

* Business logic & invariants

**This is the brain of the system.**

**Responsibilities**

* Enforce rules
* Handle transactions
* Authorization checks
* Decide what *should* happen

**Allowed**

* Calling multiple repositories
* Raising domain errors
* Committing transactions

**Forbidden**

* HTTP request/response objects
* JWT parsing

Mental model:

> Services answer **“Is this allowed, and what does it mean?”**

---

### `api/routers/`

**Purpose**

* HTTP routing only

**Responsibilities**

* URL mapping
* HTTP methods
* Dependency injection

**Characteristics**

* Extremely thin
* No logic

Mental model:

> Routers are a **table of contents** for the API.

---

### `api/controllers/`

**Purpose**

* Translate HTTP → business call

**Responsibilities**

* Parse request data
* Call service
* Format response

**Rules**

* No try/except
* No DB access
* No business logic

Controllers answer:

> “Given an HTTP request, which service do I call and how do I shape the response?”

---

### `api/schemas/`

**Purpose**

* Input/output validation

**Contains**

* Request DTOs
* Response DTOs

**Mental model**

> Schemas protect the system from malformed input.

---

### `middlewares/`

#### `jwt_auth.py`

**Purpose**

* Authentication

**Responsibilities**

* Extract JWT
* Validate signature & expiry
* Attach `request.user_id`

**Key idea**

> JWT proves *who* you are, not *what* you can do.

---

#### `db_session.py`

**Purpose**

* Transaction boundary

**Responsibilities**

* Open DB session
* Attach to request
* Rollback on error
* Close session

This enables:

* Atomic requests
* Clean error handling

---

### `core/errors.py`

**Purpose**

* Domain-level error taxonomy

**Examples**

* `AuthError`
* `NotFoundError`
* `PermissionError`
* `DomainError`

These are **not HTTP errors**.
They are mapped later.

Mental model:

> Errors describe **what went wrong**, not how to respond.

---

### `core/responses.py`

**Purpose**

* Enforce response consistency

**Success**

```json
{
  "success": true,
  "data": {...},
  "meta": {}
}
```

**Error**

```json
{
  "success": false,
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

One format → easier clients → easier debugging.

---

### `utils/`

**Purpose**

* Pure helpers

**Rules**

* No imports from app layers
* No side effects

---

### `tests/`

**Structure**

* `unit/`: services, repositories
* `integration/`: full HTTP flows

**Philosophy**

> Test behavior, not implementation.

---

## 5. Error Handling Flow

1. Service raises a domain exception
2. Controller does nothing
3. Global handler maps exception → HTTP response
4. DB session middleware rolls back

**Result**

* Clean controllers
* Predictable errors
* No partial writes

---

## 6. Why This Architecture Scales

| Problem           | Where it’s solved |
| ----------------- | ----------------- |
| Auth              | Middleware        |
| Business rules    | Services          |
| Data integrity    | Database          |
| Error consistency | Global handler    |
| Testability       | Layer isolation   |

This structure survives:

* More endpoints
* More developers
* More rules
* More complexity

---

## 7. How to Study This Codebase

When revising:

1. Read **this README first**
2. Pick one endpoint
3. Trace it layer by layer
4. Ask: *why is this logic here and not elsewhere?*

If the answer is unclear, the design is wrong.

---

## 8. Final Mental Model

> **HTTP is a delivery mechanism.
> The service layer is the product.
> The database is the law.**

Everything else exists to keep those three clean.