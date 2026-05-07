# App Map

This reference captures the reusable app structure. It intentionally avoids the domain-specific generation pipeline and private product mechanics.

## Root Layout

```text
repo/
├── frontend/          Next.js App Router app
├── backend/           Go API server
├── docs/              Operational notes and smoke-test docs
├── scripts/           Repo utilities
├── context-tree/      Product-specific notes; do not treat as reusable wholesale
├── .env.example       Combined local env starter
└── README.md          Human project overview
```

## Frontend Layout

```text
frontend/
├── app/
│   ├── layout.tsx                  Global metadata, preconnects, footer mount
│   ├── globals.css                 Base CSS, focus ring, animation utilities
│   ├── page.tsx                    Public home
│   ├── auth/                       Sign in/up, forgot/reset flows
│   ├── verify-email/               Email verification gate
│   ├── settings/                   Account, billing, preferences, deletion
│   ├── buy-credits/                Purchase/subscription management screen
│   ├── request-history/            Searchable/paginated order history and sharing
│   ├── feedback/                   Feedback and support-ticket intake
│   ├── device-order-history/       Browser-local recovery page
│   ├── legal/                      Terms, privacy, refund/subscription terms
│   ├── share/                      Public shared resources
│   ├── download/                   Public/download fulfillment routes
│   ├── admin/                      Admin configuration, feedback, logs, detail
│   └── .well-known/ + manifests    Agent/OpenAPI/MCP/static discovery routes
├── components/                     Shared shell, nav, brand, media, forms
├── lib/                            API client, browser storage helpers, payments
├── public/                         Brand marks and static images
├── package.json                    Next/React/Tailwind/lint scripts
├── tailwind.config.ts              Design tokens
├── next.config.ts                  image optimization and remote API host
└── eslint.config.mjs               Next core-web-vitals + TS linting
```

## Backend Layout

```text
backend/
├── cmd/server/main.go              HTTP entrypoint and graceful signal context
├── bootstrap/runtime.go            Runtime assembly and startup jobs
├── config/config.go                Env parsing and defaults
├── router/router.go                chi routes, CORS, middleware, aliases
├── handlers/                       HTTP handlers, middleware, OpenAPI, tests
├── db/                             pgxpool accessors and embedded schema.sql
├── models/                         JSON/data structs
├── services/
│   ├── alerts/                     Admin alert fan-out
│   ├── email/                      Mail service with local fallback
│   ├── logs/                       In-memory admin-visible log buffer
│   ├── payments/                   Provider abstractions, webhooks, billing sync
│   ├── security/                   Tokens, password hashing, digests
│   ├── storage/                    S3-compatible object storage
│   └── upload/                     Upload validation and normalization
└── go.mod                          Go 1.25, chi, pgx, godotenv, Mailgun
```

## Route Families

- **Public marketing**: home page with public nav, primary CTA, visual examples, feature tiles.
- **Authentication**: sign-up, sign-in, email verification, forgot/reset password, return-to redirects.
- **Authenticated app**: `AppShell` wraps protected pages, checks `me()`, redirects unverified users, and exposes account nav.
- **Billing and settings**: account preferences, subscription/billing portal, purchases, legal/refund links.
- **History/recovery**: server-backed request/order history plus browser-local device order IDs.
- **Feedback/support**: user-facing feedback form doubles as support ticket intake; admin can triage and reply.
- **Admin console**: admin-gated configuration/settings/feedback/logs/detail routes using the same shell.
- **Public share/download**: routes for public viewing or recovery links without entering the full app.
- **Machine-readable discovery**: OpenAPI, robots, sitemap, agent/MCP manifests.

## Component Roles

- `Brand`: reusable logo link with responsive mark and wordmark.
- `PublicNav`: public header that adapts for signed-in users with credit/balance and profile dropdown.
- `AppShell`: authenticated header, admin-aware nav, compact mobile menu, "more" overflow menu.
- `SiteFooter`: compact global footer with support, legal, history, and relevant app links.
- `LoadableImage`: Next image wrapper with fixed dimensions, skeleton, quality selection, error state.
- `GuestAccessPanel`: reusable guest recovery form with email + access token.
- Domain visual components should be isolated so they can be dropped for a new app.

## Reusable Data Surfaces

- Users, sessions, email verification, password reset.
- Payment/subscription records and credit or entitlement ledger.
- Uploaded media metadata with owner or guest email.
- Feedback/support tickets and attachments.
- Site settings/admin-managed configuration.
- Share links/groups/download records.
- Admin-visible log entries.

Do not carry over product-specific catalog tables, generation job tables, prompt tables, or model accounting unless the new app needs its own domain-specific equivalents.
