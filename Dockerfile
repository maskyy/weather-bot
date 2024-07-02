FROM python:alpine as base
ARG POETRY_VERSION=1.8.3
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app
RUN pip install poetry==$POETRY_VERSION
COPY pyproject.toml poetry.lock ./
RUN ls /app
RUN python -m poetry install --no-dev

FROM python:alpine
WORKDIR /app
COPY --from=base /app ./
RUN ./run.sh
