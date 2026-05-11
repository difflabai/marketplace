---
description: Browse, search, and edit DiffLab Business World Models — economic, AI, and value-stream simulations — via the BWM MCP server.
---

Use the Business World Models (BWM) MCP server to inspect and curate DiffLab's
catalogue of business simulation models: forecast harnesses (e.g. AI Futures
milestones), closed-form sector-economic models (e.g. layoff-trap dynamics),
and value-stream mapping models. The server exposes one composite registry per
DiffLab org with two views — a read-only `nexus` mirror of the upstream
[model-nexus](https://github.com/difflabai/model-nexus) checkout, and a
writable `local` registry forked from it.

## Connection

The plugin's `.mcp.json` launches `mcp-remote` against
`${BWM_MCP_URL}` (default `http://localhost:3000/admin/bwm/mcp/sse`).
Set two env vars before invoking:

- `BWM_MCP_URL` — base URL of the BWM MCP SSE endpoint. Local dev:
  `http://localhost:3000/admin/bwm/mcp/sse`. Production deployments use
  their own hostname, e.g. `https://bwm.difflab.ai/admin/bwm/mcp/sse`.
- `BWM_TOKEN` — opaque pipes capability token bound to your org. The
  server checks both org membership and per-mount file grants on every
  tool call (see Permissions below).

The synchronous JSON-RPC endpoint at `/admin/bwm/mcp/rpc` is also
available for headless CI/CD use; configure it via `BWM_MCP_URL` if
your client doesn't speak SSE.

## Tools

All six tools live under the `bwm.models.*` namespace.

### bwm.models.search

Relevance-ranked full-text search across registered models. Whitespace
separates terms; all terms must match (logical AND). Scoring weights
id (×6) > name (×4) > blurb (×2) > component/role (×1.5) > mechanism
(×1.0) > reference label/location (×0.8) > parameter key/value (×0.5),
with a 1.2× boost when a field starts with the term. Returns hits with
`score` and `matched_fields` (which logical fields contributed).

```json
{
  "name": "bwm.models.search",
  "arguments": {
    "q": "layoff trap nash",
    "kind": "sector_economic",
    "deep": true,
    "page_size": 20
  }
}
```

Optional `prefix` filters the dot-separated id namespace before scoring,
e.g. `"prefix": "global.10B.countries.india"` narrows the search to
that subtree. Optional `kind` narrows to a model class
(`forecast_harness` | `sector_economic`). Set `"deep": false` for a
cheap id/name/blurb-only scan.

### bwm.models.list

Paginated listing. Less expensive than search when ranking isn't
needed. Use the same `prefix` filter to walk the namespace.

```json
{
  "name": "bwm.models.list",
  "arguments": { "prefix": "global.economic", "page_size": 100 }
}
```

### bwm.models.get

Fetch full detail for one model. The `id` is the composite id returned
by list/search (e.g. `local:aifutures`, `nexus:layoff-trap`). The
detail payload includes `mechanism`, `components`, `inputs`, `outputs`,
`parameters`, `forecasts`, and `references` — enough context to summarise
or extend the model without further reads.

```json
{ "name": "bwm.models.get", "arguments": { "id": "local:aifutures" } }
```

### bwm.models.create

Create a new model in the writable registry. Requires Write permission
on the writable mount (see Permissions). Body is the model meta — id,
name, kind, blurb, mechanism, plus optional components/inputs/outputs/
parameters/references/depends_on arrays.

```json
{
  "name": "bwm.models.create",
  "arguments": {
    "id": "global.economic.new-model",
    "name": "New Sector Model",
    "kind": "sector_economic",
    "blurb": "One-line summary surfaced in lists and search.",
    "mechanism": "Multi-paragraph 'how it works' description.",
    "components": [],
    "inputs": [],
    "outputs": [],
    "parameters": [],
    "references": [],
    "depends_on": []
  }
}
```

The server enforces id hygiene: dot-separated segments, no path
traversal, no leading dots. Composite-id prefixes (`local:foo.bar`) are
stripped before validation.

### bwm.models.update

Replace the meta for an existing model. The `id` argument is the
composite id; the `meta.id` inside the body must match (composite
prefix is stripped before comparison).

```json
{
  "name": "bwm.models.update",
  "arguments": {
    "id": "local:demo.thing",
    "meta": { "id": "demo.thing", "name": "Renamed", ... }
  }
}
```

### bwm.models.delete

Remove a model from the writable registry. Returns `{ "deleted": true,
"id": "<composite id>" }`.

```json
{ "name": "bwm.models.delete", "arguments": { "id": "local:demo.thing" } }
```

## Permissions

The BWM MCP server runs on top of DiffLab's multi-tenant pipes
infrastructure. Every tool call is gated by the capability token in
`BWM_TOKEN`:

- The token's `org_id` must equal the BWM deployment's org. Cross-org
  tokens are rejected before any registry call.
- **Reads** (`search`, `list`, `get`) require `Read` or `List`
  permission on **any** of the configured registry mounts —
  typically `/org/{org}/nexus/` (read-only mirror) and
  `/org/{org}/local/` (writable fork).
- **Writes** (`create`, `update`, `delete`) require `Write`
  permission on the **writable** mount (`/org/{org}/local/`).
- File denies override grants — a deny on the writable mount blocks
  writes even if a broader Write grant covers it.

Permission errors return MCP error code 403 with a message indicating
which mount the token failed to cover. The error text never leaks
information about other orgs' mounts, matching pipes' V-2 invariant:
"the caller is told what they *can* see, not what they cannot."

## Typical Workflows

### Browse the catalogue

1. Call `bwm.models.list` with `page_size: 50` to see what's there.
2. For an interesting hit, call `bwm.models.get` for full detail.
3. To explore a subtree, re-list with `prefix: "global.10B"` etc.

### Find models by keyword

Always prefer `bwm.models.search` over `list` + manual filtering — the
server's scoring covers fields the summary doesn't expose (mechanism,
components, references) so a query like `"nash equilibrium"` will hit
models whose blurb doesn't mention the term.

### Fork a model into your local registry

The server pre-populates `local:` with a writable copy of every
upstream `nexus:` model on first boot. Edit the local copy via
`bwm.models.update`; the server dual-writes to disk and the VFS so the
change survives restarts and is git-committable.

### Author a new model

1. Pick a dot-separated id under an existing namespace
   (e.g. `global.economic.your-model`).
2. Call `bwm.models.create` with the full meta.
3. The server persists `<disk_root>/global/economic/your-model/model.meta.json`
   and re-upserts it into the VFS. The model immediately appears in
   subsequent list/search results.

## Notes

- The MCP surface intentionally exposes models only. Forecasts and
  value streams stay on the HTTP API for now — fetch the model detail
  with `bwm.models.get` and follow the linked forecast ids through the
  admin HTTP API if you need them.
- The server preserves authored cross-model dependencies (`depends_on`)
  but also computes derived edges (shared crates, shared references,
  matching input/output kinds). Those derived edges show up only on
  the `/admin/bwm/relationships` HTTP endpoint, not in the model
  detail returned via MCP.
- For local development without a real token, mint one with the
  `pipes-identity` CLI or grab a sponsor-token from the pipes admin
  UI. The token needs `Read+Write+List` on `/org/{your-org}/` to
  exercise the full surface.
