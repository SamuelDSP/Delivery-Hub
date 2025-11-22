FROM python:3.11-slim

WORKDIR /app

COPY Backend/pyproject.toml Backend/poetry.lock ./

RUN pip install poetry && poetry install --no-interaction --no-ansi

COPY Backend ./

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
