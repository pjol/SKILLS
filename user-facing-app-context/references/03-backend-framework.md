# Backend Framework

## Stack

- Go API server with `net/http`.
- `go-chi/chi` router, chi middleware, and `go-chi/cors`.
- PostgreSQL via `pgxpool`.
- Embedded `db/schema.sql` for idempotent local schema initialization.
- `godotenv` for local env loading.
- `slog` JSON logs to stdout plus an in-memory admin log service.
- Mailgun email service with local logging fallback.
- S3-compatible object storage service.
- Payment provider abstraction with Stripe-first subscriptions/checkout and optional alternative providers.

## Runtime Assembly

Keep startup centralized:

```text
cmd/server/main.go
  -> bootstrap.NewRuntime(ctx)
      -> config.LoadEnv + config.FromEnv
      -> db.Open + InitSchema
      -> construct email, alerts, storage, uploads, payments, logs
      -> run boot-time reconciliation jobs where needed
      -> handlers.NewApp(...)
      -> router.New(...)
```

This makes tests and future apps easier because the server is assembled from explicit services rather than globals.

## Config Pattern

- `config.Config` contains typed env values and defaults.
- Support `ENV_FILE=/path/to/.env`.
- Keep backend secrets out of frontend env.
- Use `NEXT_PUBLIC_*` only for browser-safe config.
- Accept local stub flags for development-only provider bypasses.
- Validate required config, especially database URL and production payment/email/storage values.
- Include explicit TTLs for sessions, email verification, password reset, and guest access.

## Database Pattern

- The application runtime must open PostgreSQL from `DATABASE_URL` using `pgxpool`; do not ship JSON, file, SQLite, or in-memory persistence as the default backend store.
- `db.DB` wraps `*pgxpool.Pool`.
- `db/schema.sql` uses `CREATE TABLE IF NOT EXISTS`, `ALTER TABLE ADD COLUMN IF NOT EXISTS`, and indexes for repeatable local startup.
- Keep query methods in focused files by domain.
- Return typed model structs from DB methods.
- Use UUID primary keys for users/sessions/records; use text IDs only for small public config tables.
- Prefer soft redaction for records with payment/audit value; hard delete only when safe.
- Keep indexes for lookup paths used by auth, owner history, public share IDs, and admin filters.

## HTTP Router

- Apply middleware globally: request ID, real IP, logger, recoverer, CORS, auth, CSRF.
- Keep `/health` lightweight and unauthenticated.
- Group routes by concern: auth, me/settings, billing, config/public resources, uploads, feedback/support, requests/orders, shares/downloads, admin, payments, machine-readable manifests.
- Provide `/api/...` aliases only when needed for compatibility.
- Admin routes sit under `/admin` and use `RequireAdmin`.
- Payment webhooks must be CSRF-exempt and verify provider signatures in handlers/services.

## Auth and CSRF

- Sessions are random tokens stored as hashes in the DB.
- Session cookies are HTTP-only, SameSite=Lax, secure in production.
- Frontend prehashes passwords; backend hashes the client hash with pepper and bcrypt.
- Email verification and password resets use token hashes and expirations.
- Auth middleware accepts cookie or bearer token and attaches user to context.
- Cookie-auth unsafe methods require matching CSRF cookie and `X-CSRF-Token`.
- CSRF is skipped for auth bootstrap endpoints and webhook-style endpoints that authenticate differently.
- Admin can be granted by DB flag and/or configured admin email allowlist.

## Handler Style

- Decode JSON with `DisallowUnknownFields`.
- Return JSON for success and `{ "error": "friendly message" }` for errors.
- Use `writeErrorWithLogging` for internal failures: user sees friendly source, logs capture detail.
- Keep form-data handlers for uploads/attachments and JSON handlers for structured actions.
- Normalize email and IDs at boundaries.
- Enforce ownership in every handler that reads or mutates user data.
- Never trust frontend price, discount, credit, role, or entitlement claims.

## Guest Access

- Guest-owned records use normalized email plus a signed/opaque guest access token.
- Backend returns/refreshes guest access tokens in headers or payloads.
- Frontend stores guest access as a convenience; backend remains source of truth.
- Guest history and downloads should require both email and token unless the link is intentionally public.

## Billing and Entitlements

- Put provider-specific API calls behind a payment service.
- Store payment records, subscription records, invoice/renewal credit grants, and provider references.
- Enforce rates and entitlements server-side at intent/session creation and final capture/webhook handling.
- Stripe subscription checkout should be reconciled by webhook and boot-time sync to cover webhook gaps.
- Billing portal creation should be backend-mediated.
- Refund policy copy can be frontend text, but reimbursement/credit logic must be backend-enforced.

## Uploads and Media

- Validate file count, content type, and size on backend.
- Store metadata: original filename, content type, size, hash, owner, storage key/url, created time.
- Support object storage but allow DB byte fallback if useful for local/dev.
- Serve private media with owner/admin checks and private cache headers.
- Serve public/share media with longer cache headers when revocation is not expected.
- Convert or normalize device-specific image formats before sending to downstream services when applicable.

## Email, Alerts, and Support

- Email service should send verification, reset, fulfillment/order updates, billing/support notifications, and admin responses.
- If email provider config is missing in local dev, log intended sends instead of failing core flows.
- Admin alerts fan out to configured emails for support tickets, internal errors, safety events, and feedback.
- Feedback/support records should support attachments, status, admin response, responder, and responded timestamp.
- Admin replies should email account/guest submitters when possible.

## Observability

- Use structured logs with method, path, status, message, and error.
- Keep an admin-visible bounded log buffer for recent server issues.
- Avoid logging secrets, raw tokens, payment secrets, private prompts, or unredacted sensitive uploads.
- Expose health and optionally OpenAPI/agent manifests.

## Tests

- Backend tests should cover auth/security, payment accounting, support/email behavior, upload/image handling, and priority/business rules for the new app.
- Use `go test ./...` as the default backend verification.
- Keep provider live tests behind explicit env flags.
