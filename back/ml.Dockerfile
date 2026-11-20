FROM modelw/base:2026.10

COPY --chown=user back/pyproject.toml back/poetry.lock ./
COPY --chown=user chat_rag /chat_rag

RUN modelw-docker install
RUN poetry install --with ml \
    && poetry run pip check

COPY --chown=user back .

RUN modelw-docker build

CMD ["modelw-docker", "serve"]
