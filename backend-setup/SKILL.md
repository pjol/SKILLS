---
name: backend-setup
description: "Reusable backend setup specifications for Go API services: runtime layout, env/config loading, PostgreSQL via pgxpool, embedded schema setup, router and middleware shape, auth/CSRF/admin gates, payments/uploads/email/support boundaries, and GAEA-derived structured logging. Use when scaffolding, reviewing, or modifying a backend for a user-facing app or similar Go/Postgres API."
---

# Backend Setup

## Purpose

Use this skill as the backend source of truth for reusable Go/Postgres API services. It captures the preferred service layout, package choices, persistence, routing, security, observability, and validation patterns that frontend or app-shell skills can reference without duplicating backend details.

Rename domain nouns, env prefixes, cookie names, products, providers, and service-specific route names for each app. Keep the operational patterns unless the target repo already has a stronger local convention.

## No Stubs Or Mock Data

Never use stubbed backend behavior, mock data, fake records, hard-coded demo responses, placeholder provider output, or in-memory fake success paths in runtime app code. They obscure what is actually implemented and make testing unreliable.

If a backend capability is not implemented, return an honest error, leave the route unregistered, gate it behind an explicit unavailable status, or fail configuration validation. Automated tests may use test fixtures, fakes, or mock providers only inside test code or clearly test-only helpers; those must never be wired into development, staging, or production runtime paths.

## Stack Defaults

- Go 1.25+ API server on `net/http`.
- Use `http.Server` with explicit timeouts, at least `ReadHeaderTimeout`.
- Prefer the standard `http.ServeMux` method-pattern router for compact services. Use `go-chi/chi`, chi middleware, and `go-chi/cors` when the app needs route groups, mountable subrouters, or existing chi-compatible app-shell patterns.
- PostgreSQL is the default runtime store, opened with `github.com/jackc/pgx/v5/pgxpool`.
- Embed local schema SQL with `//go:embed` and run idempotent DDL on startup.
- Keep JSON, file, SQLite, or in-memory stores out of runtime app paths unless the user explicitly requests one as the actual product persistence layer. Do not use them as mock replacements for Postgres-backed functionality.
- Use app-specific service packages for payments, email, object storage, uploads, alerts, logs, support, and domain workflows.
- Keep third-party providers behind interfaces for real implementations and isolated tests. Do not return fabricated provider success from runtime code when credentials or provider setup are missing.

## Directory Shape

Use `internal/` by default for app-owned packages:

```text
backend/
|-- cmd/server/main.go          startup, signal context, http.Server
|-- internal/api/               routes, handlers, middleware, OpenAPI
|-- internal/config/            env loading, typed config, defaults
|-- internal/db/                pgxpool open/close and embedded schema.sql
|-- internal/store/             storage interface and Postgres implementation
|-- internal/logging/           activity/error logger
|-- internal/models/            JSON/data structs
`-- internal/services/          payments, email, storage, uploads, alerts, support
```

If an existing app already uses top-level `config/`, `db/`, `handlers/`, `router/`, and `services/`, keep that layout and apply the same contracts.

## Runtime Assembly

Keep startup centralized and explicit:

```text
cmd/server/main.go
  -> config.Load()
  -> logging.Open(cfg.Logging)
  -> db.Open(ctx, cfg.DatabaseURL) + InitSchema(ctx)
  -> construct store and app services
  -> run boot-time reconciliation jobs where needed
  -> api.New(cfg, store, services, logger)
  -> http.Server{Addr, Handler, ReadHeaderTimeout}
```

Log startup mode and selected providers after config loads and before serving. Log whether secrets are configured as booleans, never their values.

## Config And Env

- Load env files before typed config is created.
- Find the project root from either repo root or `backend/` working directories.
- Load root `.env`, then `backend/.env`, then optional `ENV_FILE=/path/to/file`.
- Preserve precedence: real process environment variables override env-file values; later env files may override earlier env-file values only when the key was not set by the real shell environment.
- Keep backend secrets out of frontend env. Only `NEXT_PUBLIC_*` may cross into browser config.
- Use typed config structs with defaults and validation for required production values.
- Include explicit TTLs for sessions, CSRF, email verification, password reset, guest access, jobs, and provider polling.
- Anchor relative backend-local paths to the `backend/` directory. If an override starts with `backend/`, anchor it to the repo root instead of producing `backend/backend/...`.
- Use app-specific env prefixes when helpful, for example `APP_LOG_ACTIVITY_PATH`; do not carry old product prefixes into new apps.

## PostgreSQL Setup

- `DATABASE_URL` is required for the default runtime store.
- `db.Open(ctx, databaseURL)` should parse a pgxpool config, set bounded pool defaults, open the pool, and `Ping` before returning.
- Use conservative starter pool defaults: `MaxConns=10`, `MinConns=1`, `MaxConnLifetime=time.Hour`, then tune per deployment.
- `db.DB` wraps `*pgxpool.Pool` and exposes `Close()` plus `InitSchema(ctx)`.
- `InitSchema` reads embedded `schema.sql` and executes it on startup.
- Schema SQL should be repeatable: `CREATE TABLE IF NOT EXISTS`, `ALTER TABLE ADD COLUMN IF NOT EXISTS`, and indexed lookup paths.
- Use UUID/text IDs consistently for users, sessions, records, and public links. Text IDs are fine for small config tables.
- Keep relational columns for ownership, status, timestamps, auth lookups, provider references, public IDs, and admin filters. JSON payload columns can mirror flexible domain models, but should not hide indexed lookup fields.
- Keep query methods focused by domain and return typed model structs.
- Map `pgx.ErrNoRows` and common Postgres constraint errors into store-level sentinel errors such as `ErrNotFound`, `ErrAlreadyExists`, `ErrInvalidRequest`, `ErrUnauthorized`, and `ErrForbidden`.
- Prefer soft redaction for records with payment, audit, or support value; hard delete only when safe and policy-backed.

## Routing And Middleware

- Keep `/health` lightweight and unauthenticated.
- Expose OpenAPI or machine-readable manifests from `/openapi.json` or a clear equivalent.
- Group routes by concern: auth, me/settings, billing, uploads, feedback/support, request/order history, shares/downloads, admin, payments/webhooks, and app domain workflows.
- Use `/api/...` aliases only for compatibility.
- Put admin routes under `/admin` and gate them centrally.
- Payment webhooks must bypass CSRF and authenticate with provider signatures.
- For stdlib routing, use `mux.HandleFunc("GET /path", handler)` and `r.PathValue("id")`.
- For chi routing, keep the same concern grouping and mount middleware at route groups rather than scattering auth checks across handlers.

Preferred middleware order:

```text
log and recover
  -> CORS and OPTIONS handling
  -> auth
  -> CSRF for unsafe cookie-auth requests
  -> admin gate
  -> mux/routes
```

The GAEA implementation expresses this as `logRequests(cors(authenticate(mux)))`, with CSRF/admin checks inside auth middleware.

## Handler Style

- Decode JSON with `json.Decoder.DisallowUnknownFields`.
- Return JSON for success and typed friendly errors, for example `{ "error": { "code": "invalid_request", "message": "..." } }`.
- Normalize email, IDs, public tokens, and storage keys at boundaries.
- Enforce ownership in every handler that reads or mutates user data.
- Never trust frontend price, discount, credit, role, ownership, or entitlement claims.
- Log internal failures with enough structured fields to debug; keep client-facing errors friendly.
- Keep upload/attachment endpoints as form-data handlers and structured commands as JSON handlers.

## Auth And Security

- Store random session tokens only as hashes in the DB.
- Session cookies are HTTP-only, SameSite=Lax, and secure in production.
- CSRF tokens can be readable cookies plus `X-CSRF-Token` response/header values; unsafe cookie-auth methods must match the stored session token.
- Skip CSRF only for auth bootstrap endpoints and webhook endpoints that authenticate differently.
- Support bearer tokens only when the app has a clear non-browser client need.
- Admin access can come from a DB role/flag and a configured admin email allowlist.
- Local auth bypass may exist only outside production and must be obvious in config.
- Frontend password prehashing is allowed, but backend must still hash with a pepper and a real password KDF. Prefer established KDF libraries; PBKDF2-SHA256 is acceptable when staying stdlib-only.
- Guest access should use normalized email plus signed or opaque guest tokens; browser storage is convenience only, not authority.
- Validate object paths against traversal and absolute-path escapes before serving private or public media.

## Billing, Uploads, Email, And Support

- Put provider-specific payment calls behind a payment service interface.
- Enforce prices, entitlements, subscription state, and refund/credit rules on the backend.
- Reconcile subscriptions and one-time payments through webhooks plus boot-time sync where needed.
- Validate upload count, content type, size, hash, owner, and storage location on the backend.
- Support S3-compatible object storage for durable media, with local or DB-byte storage adapters only when explicitly scoped as real persistence.
- Serve private media with owner/admin checks and private cache headers; serve intentionally public media with longer cache headers.
- Email service should send verification, reset, fulfillment/order updates, billing/support notifications, and admin responses.
- If email config is missing in local dev, log intended sends instead of breaking core flows.
- Feedback/support records should include status, optional attachments, admin response, responder, and responded timestamp.

## Logging Specification

Use the GAEA logging pattern as the default.

- Logging is enabled by default.
- Write append-only JSONL activity entries to `backend/logs/activity.log`.
- Write append-only JSONL server-error entries to `backend/logs/errors.log`.
- Also write readable console output to stdout/stderr by default for local and hosted runtimes.
- Use config fields equivalent to `Enabled`, `ToStdout`, `ActivityPath`, and `ErrorsPath`.
- Expose env controls equivalent to `LOGGING_ENABLED`, `LOG_TO_STDOUT`, `LOG_ACTIVITY_PATH`, and `LOG_ERRORS_PATH`, optionally with an app-specific prefix.
- Resolve relative log paths to the backend directory and create parent dirs with `0700`.
- Open log files with create/write/append and `0600` permissions.
- Serialize writes with a mutex and close file handles on shutdown.
- Provide a `Nop()` logger so tests and partial assemblies do not need nil checks.

Logger API:

```go
logger.Activity("request completed", logging.F("path", r.URL.Path))
logger.Error("handler error", err, logging.F("status", 500))
```

Structured JSONL entries should include:

- `time` in UTC RFC3339Nano.
- `level`, usually `info` or `error`.
- `message`.
- `error` when an error is present.
- Normalized structured fields, with errors converted to strings.

Error logs should go to the error targets and also to activity-log error targets so the activity stream shows the full operational timeline.

Console entries should be human-readable, color-coded by level, and field-aligned. Sanitize newlines and carriage returns so a single event remains visually bounded.

Request logging middleware should:

- Wrap the response writer to capture status and byte count.
- Log duration in milliseconds.
- Include method, path, status, bytes, remote address, user agent, and user ID/role when authenticated.
- Recover panics, log the panic and stack, and return a friendly JSON 500 if headers are not already written.
- Send 5xx completions to `Error`; send non-5xx completions to `Activity`.

Startup logging should include app environment, store backend, selected log paths, and provider mode. Log secret presence as booleans and derived provider availability or live-call status, never raw secrets or tokens.

Do not log passwords, raw sessions, CSRF tokens, guest tokens, payment secrets, private prompts, raw provider keys, unredacted uploads, or full sensitive request bodies.

## Validation

Default backend verification:

```sh
cd backend && go test ./...
```

Add focused tests when touching backend setup:

- Config tests for env-file precedence and backend-anchored paths.
- DB tests for required `DATABASE_URL`, schema initialization, and store error mapping.
- Logger tests for activity writes, error duplication, console formatting, path creation, and close behavior.
- Handler tests for request logging, panic recovery, auth/CSRF gates, admin gates, and friendly error JSON.
- Provider tests behind explicit live-env flags; test fakes must stay test-only and must not masquerade as runtime provider implementations.
