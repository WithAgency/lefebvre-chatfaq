# Agent guidance

## Testing

- Backend: build `docker build -f back/Dockerfile -t chatfaq-back:modelw-2026.10-check .`, then run the Django suite in that image with disposable test environment variables including `BASE_URL=http://localhost` (`poetry run python manage.py test -v 0`); ~7s after build, timeout 180000ms.
- `chat_rag`: from `chat_rag/`, `PYENV_VERSION=3.14.2 poetry run python -m unittest discover -s tests -p 'test_*.py' -q`; ~3s, timeout 60000ms.
- SDK static: `cd sdk && poetry check --lock && poetry run black --check --quiet . && poetry run isort --check-only --quiet chatfaq_sdk examples tests` (timeout 120s).
- SDK tests: `cd sdk && poetry run python -m unittest discover -s tests -p 'test_*.py' -q` (6 tests, ~1s; timeout 60s).
- SDK package: `cd sdk && poetry build` (~1s; timeout 120s); validate the wheel from an isolated Python 3.14 environment.
- Widget static: `cd widget && pnpm exec nuxt prepare && pnpm exec vue-tsc --noEmit --pretty false` (~5s; timeout 180s).
- Widget package: `cd widget && pnpm run package` (~17s; timeout 300s), then validate package entry points and `npm pack --dry-run --json`.
- Widget app build: `cd widget && pnpm run build` (~10s; timeout 300s).
- Admin: from `admin/`, run `pnpm run build` with local disposable Nuxt URLs; ~38s, timeout 300000ms. To validate an unpublished widget, install its tarball in an isolated `/tmp/opencode` copy of the admin; ~30s.
- Always redirect output to a temporary file; stay quiet on success and show only relevant failure excerpts.
- Last measured: 2026-11-23.
