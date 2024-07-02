FROM ghcr.io/withlogicco/poetry:1.8.3

COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY ./ ./
RUN python -m bot
