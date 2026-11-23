FROM modelw/base:2026.10 AS dependencies

COPY --chown=user back/model-w.toml back/pyproject.toml back/poetry.lock back/README.md ./
COPY --chown=user chat_rag /chat_rag

# For PDF parsing
# RUN apt-get install -y tesseract-ocr tesseract-ocr-spa tesseract-ocr-fra


RUN modelw-docker install \
    && modelw-docker run poetry run playwright install firefox

# Install the locked embedding stack, then replace its CPU-only Torch wheel
# with the pinned CUDA build without mutating the project manifests.
RUN poetry install --with ml
ARG TORCH_GPU_URL=https://download.pytorch.org/whl/cu128/torch-2.10.0%2Bcu128-cp314-cp314-manylinux_2_28_x86_64.whl
RUN poetry run pip install --no-cache-dir "${TORCH_GPU_URL}"
RUN poetry install --only main --no-root \
    && poetry run pip check

FROM modelw/base:2026.10

COPY --from=dependencies --chown=user /code/.venv /code/.venv
COPY --from=dependencies --chown=user /code/.cache/ms-playwright /code/.cache/ms-playwright
COPY --chown=user chat_rag /chat_rag
COPY --chown=user back .

RUN sudo rm -f /etc/sudoers.d/model-w
RUN modelw-docker build

CMD ["bash", "-c", "modelw-docker run python -m daphne -b 0.0.0.0 -p 8000 back.config.asgi:application"]
