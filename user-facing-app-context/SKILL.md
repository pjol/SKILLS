---
name: user-facing-app-context
description: Reusable STIQQ-derived context tree for building polished user-facing web apps with a Next.js App Router frontend, Go/chi/Postgres API backend, auth, billing, admin, support, legal pages, responsive navigation, image loading, and design-system patterns. Use when spinning up or adapting a similar app shell while excluding app-specific generation or business pipelines.
---

# User-Facing App Context

## Purpose

Use this skill to recreate the reusable parts of this app: a polished consumer-facing Next.js frontend, a Go API backend, authentication, payments/subscriptions, admin/support surfaces, legal pages, responsive shells, and the visual system. Do not copy product-specific generation logic, private prompts, or domain-specific pipeline concepts.

## Context Tree

- `references/00-app-map.md`: Full reusable app tree, route taxonomy, component roles, and backend package layout.
- `references/01-frontend-framework.md`: Next.js setup, routing conventions, API client pattern, auth flow, localStorage conventions, and image loading.
- `references/02-design-system.md`: Tailwind theme, layout rules, navigation behavior, responsive choices, forms, cards, buttons, loading states, and accessibility.
- `references/03-backend-framework.md`: Go service architecture, config/env, database pattern, auth/CSRF, handlers, admin gates, payments, uploads, email, support, and observability.
- `references/04-implementation-playbook.md`: How to spin up a new app from these patterns, what to rename, what to validate, and what to deliberately leave behind.

## Reuse Rules

1. Keep the frontend/backend split: `frontend/` is a Next.js App Router app; `backend/` is a Go API with chi, pgxpool, embedded schema SQL, and package-separated services. The running backend must use PostgreSQL via `pgxpool` by default; JSON, file, SQLite, or in-memory stores are only acceptable for tests or explicitly named local fallback modes.
2. Keep the user-facing surfaces: public home, auth, authenticated app shell, settings/billing, request/order history, support/feedback, legal pages, admin console, public share/download surfaces, and lightweight footer.
3. Keep the design posture: bright, tactile, compact, mobile-first, icon-forward, rounded controls, restrained cards, strong loading states, and real image handling.
4. Replace all domain nouns, products, prices, copy, and route labels with the new app's vocabulary.
5. Exclude domain-specific generation pipelines, prompt catalog logic, queue mechanics, model calls, and private product internals unless the new app explicitly needs its own equivalent.
6. Preserve safety patterns: server-enforced pricing and permissions, HTTP-only session cookies, CSRF for cookie-auth unsafe requests, guest access tokens, validated uploads, admin gates, friendly JSON errors, and non-secret `NEXT_PUBLIC_*` boundaries.

## Default Workflow

1. Read `00-app-map.md` to choose the surfaces the new app needs.
2. Read `01-frontend-framework.md` before building routes, components, or API clients.
3. Read `02-design-system.md` before designing or modifying user-facing UI.
4. Read `03-backend-framework.md` before adding API, auth, billing, storage, email, admin, or support behavior.
5. Read `04-implementation-playbook.md` before scaffolding a new repo or porting these patterns into an existing one.

## Validation

For a Next.js + Go implementation using these patterns, run:

```sh
cd frontend && npm run lint && npm run build
cd ../backend && go test ./...
```

If the app has a dev server workflow, run the frontend locally and check mobile and desktop layouts for navigation overflow, form sizing, image skeletons, modal fit, footer placement, and auth redirects.
