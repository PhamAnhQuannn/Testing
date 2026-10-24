# Prep App: API (+ the built web app, if apps/web builds). One uvicorn worker (one SQLite writer).
FROM node:22-slim AS web
WORKDIR /web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci
COPY apps/web/ ./
RUN npm run build

FROM python:3.12-slim AS app
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/opt/venv UV_COMPILE_BYTECODE=1 PATH="/opt/venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
RUN uv sync --locked --no-dev --package prep-api --no-install-workspace
COPY apps/api apps/api
COPY content content
COPY --from=web /web/dist /app/web-dist

# DB lives in the named volume mounted on /app/data; backups go to /app/backups (host bind mount).
ENV DATA_DIR=/app/data BACKUP_DIR=/app/backups CONTENT_DIR=/app/content WEB_DIST=/app/web-dist
WORKDIR /app/apps/api
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
