# MCP Server Spec — python-kraken-sdk (v2)

**Goal:** expose Kraken Spot (incl. xStocks) and Futures REST access to MCP
clients via two generic `request` tools — no per-endpoint tooling, matching
this SDK's existing philosophy (README "Considerations": only `request()` is
maintained long-term).

## File layout

- `src/kraken/mcp.py` — single file, no package. One file doesn't need a
  directory.
- Console script: `kraken-mcp = "kraken.mcp:main"` (stdio transport)
- Optional dependency group: `mcp = ["mcp>=2.0.0"]` (verified current on
  PyPI — the SDK renamed `FastMCP` to `MCPServer` in the 2.x line)

## Tools exposed

Two tools, kept separate. The two client `.request()` signatures genuinely
differ (`params` vs. `post_params`/`query_params`), and the CLI already
splits `spot`/`futures`. Collapsing to one tool with an `exchange` switch
would produce a schema where half the fields are silently ignored per
branch — a model-facing lie, not simplicity.

### `spot_request` — wraps `SpotClient.request()`

```
method: str
uri: str
params: dict | None = None
auth: bool = False
do_json: bool = False
```

`do_json` is kept, not dropped — it gates JSON-bodied Spot endpoints, and
cutting it would contradict "the request function should be enough."
`query_str`, `extra_params`, `return_raw` stay cut as genuinely marginal.
`timeout` is also cut: `base_api`'s `request()` resets any non-default value
back to `TIMEOUT` (inconsistently between Spot and Futures), so exposing it
as a tool argument would offer a knob that doesn't work.

`auth` defaults to `False`, not `True` — credentials aren't guaranteed to be
configured (see Client construction below), and a tool schema shouldn't
default to the branch that fails without them.

Covers xStocks too — same client, same endpoints. Caller passes
`"asset_class": "tokenized_asset"` inside `params` where the Kraken API docs
require it. This is not a special case worth code or a dedicated spec
section — it's `SpotClient` used normally. One README sentence covers it.

### `futures_request` — wraps `FuturesClient.request()`

```
method: str
uri: str
post_params: dict | None = None
query_params: dict | None = None
auth: bool = False
```

Both tools serialize their result to JSON text on success. Exceptions
(including the SDK's existing `KrakenException.*`) propagate as MCP tool
errors (`isError` + `str(exc)`) rather than being left undefined across the
stdio boundary. Concretely: `mcp`'s `MCPServer` only surfaces `str(exc)` to
the model for exceptions that are (or subclass) its own `ToolError` —
anything else is masked to a generic "Error executing tool `<name>`" and
only logged server-side. Each tool therefore catches the SDK's exceptions
and re-raises `ToolError(str(exc))`, rather than relying on the library's
default behavior.

## Auth model

Credentials are **never** tool arguments — they'd otherwise flow through the
LLM's context. Read once, server-side, from env vars, matching the naming
the CLI already uses via `auto_envvar_prefix="KRAKEN"` — add nothing new
except the one sandbox toggle:

| Var                                                    | Purpose                                                                                                      |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `KRAKEN_SPOT_API_KEY` / `KRAKEN_SPOT_SECRET_KEY`       | Spot/xStocks auth (existing)                                                                                 |
| `KRAKEN_FUTURES_API_KEY` / `KRAKEN_FUTURES_SECRET_KEY` | Futures auth (existing)                                                                                      |
| `KRAKEN_FUTURES_SANDBOX`                               | `1`/`true` → demo-futures.kraken.com (new — justified as a safety rail on a tool that can place real orders) |

No `KRAKEN_SPOT_URL` / `KRAKEN_FUTURES_URL`. Inventing env vars nothing else
reads is scope creep and a permanent compatibility promise for a need
nobody stated.

## Client construction

Two module-level instances, built at import time:

```python
_spot = SpotClient(
    key=os.getenv("KRAKEN_SPOT_API_KEY", ""),
    secret=os.getenv("KRAKEN_SPOT_SECRET_KEY", ""),
)
_futures = FuturesClient(
    key=os.getenv("KRAKEN_FUTURES_API_KEY", ""),
    secret=os.getenv("KRAKEN_FUTURES_SECRET_KEY", ""),
    sandbox=os.getenv("KRAKEN_FUTURES_SANDBOX", "").lower() in ("1", "true"),
)
```

Not a cached factory function (`lru_cache`-wrapped singleton getter) — that's
a global with extra ceremony and an invisible lifetime. Module-level
construction is explicit, and `key`/`secret` default to `""`, which is
already valid for public endpoints, so import never fails on missing env
vars.

**Fixed — concurrent tool calls race on nonce generation and session
renewal.** The `mcp` SDK dispatches every request other than `initialize`
via `task_group.start_soon` without awaiting it, and each synchronous tool
body runs on its own worker thread (`anyio.to_thread.run_sync`) — two
`tools/call` requests the client sends without waiting for a reply (e.g.
parallel tool calling) genuinely run concurrently, not just hypothetically.
Against that, `get_nonce()` (`time.time() * 1e8`, no locked counter) can
produce colliding or out-of-order nonces, which Kraken rejects, and
`__check_renew_session()` can close the shared `requests.Session` out from
under a request another thread is mid-flight on. A `threading.Lock` per
client, held around the call to `.request()`, serializes calls against the
same client (Spot and Futures calls still run independently of each other)
and removes both races.

## Non-goals

- No per-endpoint tools (Trade/Market/User/Funding wrappers).
- No secrets as tool parameters.
- No websocket exposure (REST only).
- No Sphinx doc page / toctree entry — `doc/03_examples` is for SDK usage
  samples, not a server binary; the README section is enough.
- No rate limiting, no read-only/write-guard mode. Kraken already enforces
  rate limits server-side and raises exceptions that this spec already
  propagates as tool errors. The actual safety rail against unwanted
  trading is scoping the Spot/Futures API key's permissions at Kraken (a
  no-trade key), not code in this server.

## Touch points (minimum viable set)

1. `src/kraken/mcp.py` — server + two tools + `main()`
2. `pyproject.toml` — `[project.optional-dependencies] mcp = ["mcp>=2.0.0"]`
   (verify the floor against current PyPI before shipping), plus the
   `kraken-mcp` console script entry. This is the project's first optional-
   dependency group — there's no existing convention to follow, but it's
   plain PEP 621.
3. `README.md` — ~10 lines: env vars, one example client config, the
   xStocks sentence
4. One test file, two tests, mocking `.request()` to verify tool wiring —
   not a dedicated multi-file test suite
