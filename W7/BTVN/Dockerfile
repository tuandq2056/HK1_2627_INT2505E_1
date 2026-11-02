# ─── stage 1: builder ───
FROM python:3.12-slim AS builder
WORKDIR /build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
COPY pyproject.toml ./
COPY src ./src
RUN pip install .

# ─── stage 2: runtime ───
FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r app && useradd -r -g app -d /app app && chown app:app /app

# Chỉ copy venv đã cài package — không mang theo pip cache / build tool
COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app wsgi.py gunicorn.conf.py docker-entrypoint.sh ./
COPY --chown=app:app migrations ./migrations

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=wsgi:app \
    APP_CONFIG=product_api.config.ProductionConfig

USER app
EXPOSE 5000
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
