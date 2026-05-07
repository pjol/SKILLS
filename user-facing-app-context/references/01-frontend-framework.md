# Frontend Framework

## Stack

- Next.js App Router with React 18 and TypeScript.
- Tailwind CSS for all styling; no component framework.
- `lucide-react` for icons.
- `next/image` for optimized media, with remote API host configured from `NEXT_PUBLIC_API_BASE_URL`.
- ESLint uses `next/core-web-vitals` and `next/typescript`.

## Scripts

```json
{
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "eslint ."
}
```

Use `npm run lint` and `npm run build` as the frontend acceptance checks.

## App Router Conventions

- Put public, auth, app, admin, legal, share, and support pages under `frontend/app`.
- Use `layout.tsx` for global metadata, API preconnects, CSS import, and persistent footer.
- Use route-level client components for forms, auth checks, localStorage, dropdowns, and modals.
- Use `Suspense` around pages that read `useSearchParams`.
- Keep public pages self-contained with `PublicNav`; wrap protected account/admin pages in `AppShell`.
- Keep machine-readable routes under `app/.well-known`, `app/openapi.json`, `app/robots.txt`, `app/sitemap.xml`, or backend proxy routes as needed.

## API Client Pattern

Centralize backend calls in `frontend/lib/api.ts`:

- `API_BASE_URL` and `APP_BASE_URL` come from `NEXT_PUBLIC_*`.
- Export typed response shapes alongside request helpers.
- Use a single `apiFetch<T>()` wrapper for JSON, FormData, credentials, CSRF, guest tokens, and error parsing.
- Set `Content-Type: application/json` unless body is `FormData`.
- Send `credentials: "include"` for cookie sessions.
- For unsafe cookie-auth requests, read CSRF from cookie/memory/localStorage and send `X-CSRF-Token`.
- Send `X-Guest-Access-Token` when local guest access exists.
- Parse backend `{ error }` JSON into an `ApiError(status)`.
- Remember guest tokens and CSRF tokens from response headers/payloads.

## Auth Flow

- Backend exposes `/auth/password-config`; frontend uses Web Crypto SHA-256 prehashing before sending password material.
- Sign-up accepts first name, last name, email, password, terms acceptance, and marketing preference.
- Sign-in and sign-up support `email` and safe relative `return_to` query params.
- Existing account conflicts during sign-up can redirect to sign-in with a friendly message.
- Email verification is a first-class gate; protected shell redirects unverified users to `/verify-email`.
- Auth pages use split layouts on desktop, single-column on mobile, strong form labels, and password visibility toggles.

## Guest and Device Recovery

- Guest access stores email and access token in localStorage, guarded with try/catch for privacy browsers.
- Recovery links can seed guest access via URL params.
- Browser-local order/request IDs are stored separately from server records and are treated as convenience only.
- Device history pages should allow copy, clear, remove, open status, and support-ticket links.

## Navigation Shells

- `PublicNav` checks `me()` once and changes anonymous vs signed-in CTAs.
- Public desktop nav keeps primary links visible and moves extras into a "More" dropdown.
- Public mobile nav collapses into a menu with the main CTA at the top.
- Signed-in public nav shows balance/entitlement and a profile icon dropdown.
- `AppShell` performs protected auth checks, mounts sticky nav, includes admin links when `user.is_admin`, and uses a mobile menu below large breakpoints.
- Menus close on route change, outside pointer, and Escape.

## Images and Loading

- Use `LoadableImage` when rendering remote/user/admin images.
- Always reserve dimensions with `aspect-ratio`, fixed height/width, or grid constraints.
- Show skeletons until `next/image` fires `onLoad`.
- Use `sizes` and quality heuristics to avoid overserving small images.
- Prefer `priority` only for first-viewport brand/hero images.
- Give unavailable images a clear inline fallback.

## Browser Storage

- Wrap localStorage access in helpers that check `typeof window !== "undefined"`.
- Catch storage failures; never make core checkout/auth flows depend on storage availability.
- Deduplicate records and cap lists.
- Store only recovery metadata that is safe on a shared device.

## Payments Frontend

- Keep provider-specific checkout setup in a separate module, for example `lib/stripe-checkout.ts`.
- Preload checkout widgets when the flow makes an imminent payment likely.
- Redirect logged-out users through account creation/sign-in when subscriptions or account-tied purchases require identity.
- Enforce all price and entitlement decisions on the backend; frontend is only a display/control surface.

## Page Composition

- Public home: nav, first-viewport product signal, clear CTA, visual proof, compact feature tiles.
- Settings/billing: quiet operational layout with status, management action, subtext legal/refund links.
- History pages: searchable/paginated list, modal/detail view, share/copy actions, clear empty states.
- Feedback/support: mode switch, category/issue buttons, email, subject, message, attachments, friendly notices.
- Admin pages: dense but readable lists, filters, detail pane, response forms, and admin-only media access.
