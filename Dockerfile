FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .
EXPOSE 8000
CMD ["uvicorn", "movielibrary.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
