FROM ghcr.io/withlogicco/poetry:1.8.3
WORKDIR /bot
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . ./
CMD ["./run.sh"]
