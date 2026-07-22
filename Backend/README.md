# Delivery Hub Backend

Backend service for **Delivery Hub**, a full-stack delivery marketplace built with FastAPI.

The backend provides authentication, authorization, product management and order management through a RESTful API following a layered architecture and modern backend development practices.

---

# Overview

The backend is responsible for:

- User authentication
- Role-based authorization
- Product management
- Order management
- Business rules
- Database persistence
- API documentation

---

# Architecture

The project follows a layered architecture to separate responsibilities.

```
                 FastAPI Routers
                        │
                        ▼
                 Dependencies
                        │
                        ▼
                   Services
                        │
                        ▼
                SQLAlchemy Models
                        │
                        ▼
                  PostgreSQL
```

Each layer has a single responsibility:

| Layer | Responsibility |
|-------|----------------|
| Routers | HTTP endpoints |
| Dependencies | Authentication & Authorization |
| Services | Business logic |
| Models | Database entities |
| Schemas | Request & Response validation |
| Database | Persistence |

---

## Design Decisions

Some architectural decisions adopted in this project:

- Layered architecture
- Service layer for business rules
- SQLAlchemy ORM
- JWT authentication
- Dependency-based authorization
- Database migrations with Alembic
- Separation between Models and Schemas
- Role-based access control

# Technologies

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT
- Passlib
- Poetry
- Pytest
- GitHub Actions

---

# Authentication

Authentication is implemented using JWT.

Implemented features:

- User registration
- Login
- Password hashing with bcrypt
- JWT token generation
- Protected endpoints
- Current user dependency

---

# Authorization

Role-Based Access Control (RBAC)

Available roles:

- Customer
- Seller
- Admin

Authorization is implemented using reusable FastAPI dependencies.

Examples:

- Customers cannot create products.
- Sellers manage only their own products.
- Admins have unrestricted access.

---

# Product Management

Implemented features:

- Create products
- Update products
- Delete products
- Product ownership validation
- Product listing
- Product details

---

# Order Management

Current features include:

- Customer orders
- Seller order management
- Order status tracking

Payment integration will be added in a future release.

---

# Database

The application uses PostgreSQL together with SQLAlchemy ORM.

Database schema changes are managed through Alembic migrations.

---

# Project Structure

```
Backend
│
├── alembic
│
├── app
│   ├── api
│   ├── core
│   ├── database
│   ├── enums
│   ├── models
│   ├── schemas
│   ├── services
│   └── tests
│
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# Local Development

## Install dependencies

```bash
poetry install
```

---

## Environment Variables

Create a `.env` file inside the Backend folder.

```env
DATABASE_URL=
DATABASE_TEST_URL=
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run Migrations

```bash
poetry run alembic upgrade head
```

---

## Start the Server

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at

```
http://localhost:8000
```

---

# Testing

Run all tests:

```bash
poetry run pytest
```

---

# API Documentation

Swagger UI

```
/docs
```

ReDoc

```
/redoc
```

---

# Deployment

| Service | Platform |
|----------|----------|
| Backend | Render |
| Database | Supabase |

---

# Future Improvements

- Payment gateway integration
- Docker Compose
- Redis caching
- Email notifications
- Monitoring and logging

---

# Related Documentation

Return to the project overview:

➡️ **[Delivery Hub](../README.md)**

Frontend documentation:

➡️ **[Frontend README](../Frontend/README.md)**

---

# License

MIT License