---
name: user-facing-app-context
description: Reusable STIQQ-derived context tree for building polished user-facing web apps with a Next.js App Router frontend, backend integration through the backend-setup skill, auth/billing/admin/support/legal surfaces, responsive navigation, image loading, and design-system patterns. Use when spinning up or adapting a similar app shell while excluding app-specific generation or business pipelines.
---

# User-Facing App Context

## Purpose

Use this skill to recreate the reusable app shell: a polished consumer-facing Next.js frontend, backend-facing product surfaces, authentication flows, payments/subscriptions UI, admin/support surfaces, legal pages, responsive shells, and the visual system. Use `$backend-setup` for backend architecture and implementation details. Do not copy product-specific generation logic, private prompts, or domain-specific pipeline concepts.

## Context Tree

- `references/00-app-map.md`: Full reusable app tree, route taxonomy, component roles, and backend boundary.
- `references/01-frontend-framework.md`: Next.js setup, routing conventions, API client pattern, auth flow, localStorage conventions, and image loading.
- `references/02-design-system.md`: Tailwind theme, layout rules, navigation behavior, responsive choices, forms, cards, buttons, loading states, and accessibility.
- `$backend-setup`: Go service architecture, config/env, database pattern, auth/CSRF, handlers, admin gates, payments, uploads, email, support, logging, and observability.
- `references/03-backend-framework.md`: Compatibility pointer to `$backend-setup`; do not duplicate backend setup there.
- `references/04-implementation-playbook.md`: How to spin up a new app from these patterns, what to rename, what to validate, and what to deliberately leave behind.

## Reuse Rules

1. Keep the frontend/backend split: `frontend/` is a Next.js App Router app; backend implementation follows `$backend-setup`.
2. Keep the user-facing surfaces: public home, auth, authenticated app shell, settings/billing, request/order history, support/feedback, legal pages, admin console, public share/download surfaces, and lightweight footer.
3. Keep the design posture: bright, tactile, compact, mobile-first, icon-forward, rounded controls, restrained cards, strong loading states, and real image handling.
4. Never use stubbed content, mock data, fake rows, hard-coded demo records, placeholder product output, stubbed checkout/support/admin responses, or UI states that imply unfinished functionality works. This creates confusion about what is actually implemented and makes testing harder. If functionality is not wired to real app behavior, leave it unimplemented, disabled, or explicitly blocked in development code paths rather than faking it.
5. Replace all domain nouns, products, prices, copy, and route labels with the new app's vocabulary.
6. Exclude domain-specific generation pipelines, prompt catalog logic, queue mechanics, model calls, and private product internals unless the new app explicitly needs its own equivalent.
7. Preserve frontend/backend safety boundaries from `$backend-setup`: server-enforced pricing and permissions, cookie-auth CSRF, validated uploads, admin gates, friendly JSON errors, and non-secret `NEXT_PUBLIC_*` browser config.

## Default Workflow

1. Read `00-app-map.md` to choose the surfaces the new app needs.
2. Read `01-frontend-framework.md` before building routes, components, or API clients.
3. Read `02-design-system.md` before designing or modifying user-facing UI.
4. Use `$backend-setup` before adding API, auth, billing, storage, email, admin, support, logging, or backend persistence behavior.
5. Read `04-implementation-playbook.md` before scaffolding a new repo or porting these patterns into an existing one.

## Validation

For a Next.js + Go implementation using these patterns, run:

```sh
cd frontend && npm run lint && npm run build
cd ../backend && go test ./...
```

If the app has a dev server workflow, run the frontend locally and check mobile and desktop layouts for navigation overflow, form sizing, image skeletons, modal fit, footer placement, and auth redirects.
