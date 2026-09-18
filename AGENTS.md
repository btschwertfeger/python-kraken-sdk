# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Unofficial Python SDK and CLI for the Kraken Crypto Asset Exchange, covering
Spot (incl. xStocks), and Futures over both REST and websocket APIs. Synchronous
and asynchronous clients are provided. Python >=3.11.

The upstream repository is located at: https://github.com/btschwertfeger/python-kraken-sdk

## Commands

Use `uv` exclusively (never bare `python`/`pip`).

- Install dev env: `make dev` (= `uv pip install -e . -r requirements-dev.txt`)
- Quality gate (black, ruff, mypy, codespell, etc.): `prek run -a` — a change is
  not done until this passes.
- Full test suite: `make test` (runs `tests/cli/basic.sh` then pytest).
- Rerun only last failures: `make retest`.
- Coverage: `make coverage`.
- Single test: `uv run pytest tests/spot/test_spot_trade.py::<test_name> -vv`
- By marker (see full list in `pyproject.toml`): `uv run pytest -m spot_trade`.
  Markers mirror the layout: `spot`, `futures`, `*_auth` (private), plus
  per-domain markers like `spot_market`, `futures_user`, `spot_websocket`,
  `xstocks`. `wip` marks a single hand-run test (`make wip`).
- Build / docs: `make build`, `make doc`.

### Testing notes

Tests run against the **live Kraken API**, so they are flaky by design — pytest
is configured with retries and a 60s timeout (`pyproject.toml`). Authenticated
tests read credentials from environment variables (`SPOT_API_KEY`,
`SPOT_SECRET_KEY`, `XSTOCKS_API_KEY`/`XSTOCKS_SECRET_KEY`/`XSTOCKS_API_URL`,
and the Futures equivalents) via the `conftest.py` fixtures; they are skipped /
fail without valid keys. `asyncio_mode = auto`.

## Architecture

### Base clients are the core (`src/kraken/base_api/__init__.py`)

Four base classes carry all transport, auth signing, session management, and
error handling:

- `SpotClient` / `SpotAsyncClient` (requests / aiohttp)
- `FuturesClient` / `FuturesAsyncClient` (requests / aiohttp)

The primary public interface is each client's generic `request(...)` method —
callers pass the raw `method` + `uri` (+ params) and get parsed, exception-
checked responses. The README "Considerations" section is the design intent:
**concentrate on `request`**; the higher-level domain clients are maintained but
no longer extended.

Key shared behaviors:

- **Signing differs between Spot and Futures.** Spot uses `API-Key`/`API-Sign`
  HMAC over `uri + query` and the SHA256 of `nonce + postdata`; Futures uses
  `APIKey`/`Authent`/`Nonce` and strips the `/derivatives` prefix before signing.
  Don't unify these.
- **Session auto-renewal**: a new HTTP session is created every
  `MAX_SESSION_AGE` (300s) because Kraken rejects stale sessions.
- **Error handling**: `ErrorHandler` raises typed exceptions from
  `kraken.exceptions`. Spot checks the `error` field; Futures additionally
  checks `sendStatus` and `batchStatus`. `use_custom_exceptions=False` returns
  the raw response object instead.
- `extra_params` (str|dict) is merged into params; `ensure_string` decorator
  normalizes list args into comma-joined strings (and json-dumps `extra_params`).

### Domain clients (`src/kraken/{spot,futures}/`)

`market.py`, `trade.py`, `user.py`, `funding.py`, `earn.py` (Spot only) each
subclass the corresponding base client and add named convenience methods that
ultimately call `request`. These are thin wrappers; argument/method names
intentionally mirror Kraken's API docs rather than PEP8 (see the
`ignore-names` list in `pyproject.toml`).

### Websocket clients

- Spot: `SpotWSClient` (`spot/ws_client.py`) → base `SpotWSClientBase`
  (`spot/websocket/__init__.py`) → connection handling in
  `spot/websocket/connectors.py`. **Websocket API v2 only.** An authenticated
  client holds up to two connections (public + private); `no_public=True`
  disables the public one. Subclass and override `on_message`.
- Futures: `FuturesWSClient` (`futures/ws_client.py`, `futures/websocket/`).
- `SpotOrderBookClient` (`spot/orderbook.py`) builds on `SpotWSClient`,
  maintaining a local order book with crc32 checksum validation.

### CLI (`src/kraken/cli.py`, entry point `kraken`)

`kraken {spot,futures} [OPTIONS] URL` is a thin passthrough: it builds the
appropriate base client and calls `request` against the given URL, handling
auth in the background. It is not a wrapper around the domain clients.

## Conventions

- Type hints on all signatures; ruff + mypy run in `strict` mode (config in
  `pyproject.toml`). `line-length = 130`.
- Public interfaces get sphinx-style docstrings; skip them on internal helpers.
- When adding/adjusting an endpoint, add or update the matching test under
  `tests/` (mirroring `src/` layout) with the correct marker.
- Versioning is SemVer; version is derived from git tags via setuptools_scm
  (`src/kraken/_version.py` is generated — do not edit).

## Git & pull requests

Derived from the repository's own history — match it.

### Branch names

- kebab-case, short and descriptive (`split-dependencies`, `regroup-tests`,
  `update-citation-file`).
- For issue-driven work, GitHub's auto-format `<issue#>-<slugified-title>` is
  also fine (`403-spottradetruncate-not-working-for-xstocks`).
- Branch off `master`; never commit directly to it.

### Commit & PR titles (they match)

- **Everything else** (housekeeping, CI, config, refactors): a short imperative
  phrase, no trailing period (`Update tests`, `Improve test suite`,
  `Extract dev-dependencies`, `Fix CI build and update pre-commit hooks`).
- Do **not** use Conventional Commits prefixes (`feat:`, `fix:`, `chore:`) — the
  owner's own commits don't.
- Commit messages must read like titles without body.

### PR bodies

- For larger changes, use `# Summary` or `## <topic>` headers with bullet lists
  of the notable changes.
- End issue-linked PRs with `Closes #<n>` on its own line.

### Assignees

Always set the repository owner (`btschwertfeger`) as the assignee on every PR
created on their behalf. `gh pr edit --add-assignee` may abort on the
projects-classic GraphQL warning — if so, apply via REST:
`gh api -X POST repos/<owner>/<repo>/issues/<pr#>/assignees -f "assignees[]=btschwertfeger"`.

### Labels

Label every PR. When it closes an issue, carry over that issue's labels, and add
any others that fit the change. `gh pr edit --add-label` may abort on the
projects-classic GraphQL warning — if so, apply via REST:
`gh api -X POST repos/<owner>/<repo>/issues/<pr#>/labels -f "labels[]=<Label>"`.

Pick from the repo's existing labels (exact names, case-sensitive) — don't
invent new ones:

- `Spot` / `Futures` — changes to the respective trading API.
- `Documentation` — docs, docstrings, examples.
- `Bug` — fixes for something that isn't working.
- `enhancement` — new feature or request.
- `Testing` — test-only changes.
- `CI/CD` — workflows and package publishing.
- `Project setup` — QA, tooling, and repo setup.
- `dependencies` — dependency updates.
- `Breaking` — backward-incompatible changes.
