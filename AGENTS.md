## Testing

- Backend: build `docker build -f back/Dockerfile -t chatfaq-back:modelw-2026.10-check .`, then run the Django suite in that image with disposable test environment variables (`python manage.py test -v 0`); ~11s, timeout 120000ms.
- `chat_rag`: from `chat_rag/`, `PYENV_VERSION=3.14.2 poetry run python -m unittest discover -s tests -p 'test_*.py' -q`; ~3s, timeout 60000ms.
- SDK: from `sdk/`, `PYENV_VERSION=3.14.2 poetry run python -m unittest discover -s tests -p 'test_*.py' -q`; ~1s, timeout 30000ms.
- Admin: from `admin/`, run `pnpm run build` with local disposable Nuxt URLs; ~42s, timeout 300000ms.
- Widget: from `widget/`, `pnpm exec vue-tsc --noEmit && pnpm run build`; ~32s, timeout 300000ms.
- Always redirect output to `/tmp/opencode`; stay silent on success and print failures only.
- Last measured: 2026-11-20.
