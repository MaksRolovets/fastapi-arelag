FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY src alembic alembic.ini /app/

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]