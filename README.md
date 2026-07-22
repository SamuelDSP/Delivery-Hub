# Delivery Hub

A full-stack delivery marketplace built with **FastAPI**, **Next.js** and **PostgreSQL**.

Delivery Hub is a modern web application where customers can browse products and place orders while sellers manage their own storefronts through a secure role-based platform.

Designed as a production-ready solution, it focuses on clean architecture, authentication, authorization, scalable backend design and production-ready deployment.

---

## Preview

### Home Page

![Home Page](docs/images/home.png)

---

### Customer Catalog

![Customer Catalog](docs/images/customer-catalog.png)

---

### User Registration

![User Registration](docs/images/register.png)

---

### Seller Dashboard

![Seller Dashboard](docs/images/dashboard.png)

---

### API Documentation

![Swagger](docs/images/swagger.png)

---

## Live Demo

Application:

https://delivery-hub-spot.vercel.app

API Documentation:

https://productmanagementsystem-81hs.onrender.com/docs

---

# Features

### Authentication

- User registration
- Secure login
- JWT authentication
- Password hashing with bcrypt
- Protected routes

### Authorization

Role-Based Access Control (RBAC)

- Customer
- Seller
- Admin

Business rules are enforced through reusable FastAPI dependencies and service-layer validation.

### Marketplace

- Browse products
- Product details
- Seller storefronts
- Customer order workflow
- Seller product management

### Product Management

- Create products
- Update products
- Delete products
- Product ownership validation
- Inventory management

### Backend Engineering

- Layered architecture
- RESTful API
- Database migrations with Alembic
- SQLAlchemy ORM
- Input validation with Pydantic
- Automated tests
- CI/CD with GitHub Actions

---

# Technology Stack

| Backend | Frontend | Infrastructure |
|----------|-----------|----------------|
| FastAPI | Next.js | Render |
| SQLAlchemy | React | Vercel |
| PostgreSQL | TypeScript | Supabase |
| Alembic | App Router | GitHub Actions |
| Pydantic | Fetch API | Poetry |
| JWT | | Pytest |

---

# Architecture

```text
                    Next.js Frontend
                           │
                           ▼
                    FastAPI REST API
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
 Authentication & Authorization       Business Services
         │                                   │
         └─────────────────┬─────────────────┘
                           ▼
                    PostgreSQL Database
                         (Supabase)
```

---

# Repository Structure

```text
Delivery-Hub
│
├── Backend
│   ├── app
│   ├── alembic
│   ├── tests
│   └── README.md
│
├── Frontend
│   ├── app
│   ├── components
│   ├── services
│   └── README.md
│
├── docs
│   └── images
│
└── README.md
```

---

# Documentation

Detailed documentation for each part of the project is available in:

- **Backend/README.md**
- **Frontend/README.md**

---

# Roadmap

The project continues to evolve with new marketplace features.

Planned improvements include:

- Payment gateway integration
- Product search and filtering
- Seller profile pages
- Order tracking
- Email notifications
- Docker support
- Redis caching

---

# License

This project is licensed under the MIT License.