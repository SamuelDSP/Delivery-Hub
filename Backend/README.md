# Product Management System

This is the backend service for the Product Management System, built using Python and FastAPI. It provides RESTful APIs to manage products, including creating, reading, updating, and deleting product information.

## Technologies Used

- Python 3.11.9
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (for database migrations)
- Pydantic (for data validation)
- Uvicorn (ASGI server)
- Poetry (for dependency management)
- Pytest (for testing)
- Github Actions (for CI/CD)
- Swagger UI (for API documentation)

## Functionalities

- Create new products
- Read product information
- Update existing products
- Delete products

## Architecture

The application follows a layered architecture:
- Presentation Layer (FastAPI)
- Business Logic Layer (Pydantic models and service logic)
- Data Access Layer (SQLAlchemy ORM)
- Database Layer (PostgreSQL)

## Setup Instructions

### 1. Clone the repository

Use git clone in the following [Repository](https://github.com/SamuelDSP/ProductManagementSystem/tree/main)
then navigate to the Backend directory by running:
```bash
cd Backend
```


### 2. Install dependencies using Poetry

Make sure you have Poetry installed. Then run:
```bash
poetry install
```


### 3. Set up the PostgreSQL database

Create a PostgreSQL database for the application. You can use the following commands to create a new database:
```sql
CREATE DATABASE YourDatabaseName;
CREATE DATABASE YourTestDatabaseName;
```


Then,
Create a environment file `.env` in the Backend directory with the following content (note: replace placeholders with actual values):
```plaintext
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/YourDatabaseName
```
```plaintext
TEST_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/YourTestDatabaseName
```


### 4. Run database migrations

Run the following command to apply database migrations:
```bash
poetry run alembic upgrade head
```


### 5. Start the FastAPI server

Run the following command to start the server:
```bash
poetry run uvicorn app.main:app --reload
```
The server will be accessible at [http://localhost:8000](http://localhost:8000).


## Testing

To run the tests, use the following command:
```bash
poetry run pytest
```

## API Documentation

Swagger UI is available at [https://productmanagementsystem-81hs.onrender.com/docs](https://productmanagementsystem-81hs.onrender.com/docs) for interactive API documentation.

![Swagger UI](docs/images/swagger.png)


## Future improvements

The project is still under development. Here are some planned improvements:

- Implement user authentication and authorization (e.g., JWT)
- Add product categories and filtering capabilities
- Integrate with a caching layer (e.g., Redis)
- Add more comprehensive API tests
- Implement logging for better monitoring
- Dockerize the application for easier deployment


## License
This project is licensed under the MIT License.