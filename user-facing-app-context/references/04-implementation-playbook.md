# Implementation Playbook

## Starting a New App

1. Copy the architectural shape, not the product logic.
2. Choose new domain nouns for:
   - primary user action
   - unit of purchase or entitlement
   - order/request/history object
   - admin-managed configuration
   - support categories
3. Scaffold `frontend/` and `backend/` as sibling folders.
4. Keep `.env.example`, `frontend/.env.example`, and `backend/.env.example` aligned.
5. Build the public home, auth, app shell, settings/billing, history, feedback/support, legal, and admin shell before deep domain workflows.
6. Add domain-specific flows only after the reusable shell is stable.

## What To Rename

- Brand assets and metadata in `frontend/app/layout.tsx`.
- Tailwind color names if they are too tied to the old brand.
- Cookie names, password prehash domain/salt/version, localStorage keys.
- Payment product/tier names and legal copy.
- Email sender display name and templates.
- Admin nav labels and support categories.
- Route labels, CTA copy, empty states, and footer links.

## What To Keep

- Next.js App Router with route folders.
- Tailwind-only component styling.
- `PublicNav` + `AppShell` split.
- API wrapper with CSRF, credentials, guest-token handling, typed responses, and friendly errors.
- Auth pages with return-to and email prefill.
- Settings/billing page with portal/subscription management.
- Feedback/support page with attachments and admin response path.
- Device-local recovery IDs when guest checkout or no-login flows exist.
- Global footer with support, history/recovery, legal, and informational links.
- Go runtime assembly, typed config, chi router, PostgreSQL via pgxpool as the default runtime store, embedded schema initialization, service packages.
- Server-side enforcement for pricing, roles, ownership, and entitlements.

## What To Leave Behind

- Product-specific generation pipelines.
- Prompt/catalog concepts that only exist for the old product.
- Model-specific rate limit queues and image-generation accounting.
- Domain-specific tables unless the new product needs direct analogs.
- Old product copy, examples, prices, and screenshots.
- Any private keys, provider-specific live IDs, or real user data.

## Suggested MVP Surface Checklist

- Public home with real product proof and primary CTA.
- Sign up, sign in, verify email, forgot/reset password.
- Authenticated app shell with mobile menu and desktop overflow menu.
- Settings page with account preferences, billing, support/legal links, and deletion flow.
- Purchase or subscription page, if monetized.
- User history page with search/pagination/detail/share where relevant.
- Feedback/support intake with attachments.
- Admin inbox for support/feedback.
- Admin logs and minimal admin settings.
- Terms, privacy, refund/subscription pages.
- Device-local recovery page if anonymous checkout exists.

## Environment Checklist

Backend:

```env
APP_ENV=development
APP_BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8080
SERVER_ADDR=:8080
CORS_ALLOWED_ORIGINS=http://localhost:3000
DATABASE_URL=postgres://user:pass@localhost:5432/app?sslmode=disable
SESSION_COOKIE_NAME=app_session
CSRF_TOKEN_COOKIE_NAME=app_csrf
PASSWORD_PEPPER=change-me
PASSWORD_PREHASH_SALT=app:password-prehash:v1
PASSWORD_PREHASH_VERSION=app-pwhash-v1
GUEST_ACCESS_TOKEN_SECRET=change-me
MAILGUN_DOMAIN=
MAILGUN_API_KEY=
MAILGUN_FROM_EMAIL=App <no-reply@example.com>
ADMIN_ALERT_EMAILS=ops@example.com
ADMIN_USER_EMAILS=admin@example.com
STORAGE_BUCKET=
STORAGE_REGION=us-east-1
STORAGE_ENDPOINT=
STORAGE_ACCESS_KEY_ID=
STORAGE_SECRET_ACCESS_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
ALLOW_STUB_PAYMENTS=true
```

Frontend:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
NEXT_PUBLIC_APP_BASE_URL=http://localhost:3000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
```

## Build Order

1. Create shared tokens, globals, `Brand`, `PublicNav`, `AppShell`, `SiteFooter`, and `LoadableImage`.
2. Implement backend config, DB open/init, auth/session/CSRF, `/me`, and health.
3. Build auth pages and verification flow.
4. Build settings/account page.
5. Add billing/entitlement service and frontend payment surfaces.
6. Add history/recovery surfaces.
7. Add feedback/support and admin feedback.
8. Add admin logs/settings.
9. Add domain-specific primary workflow.
10. Add share/download/public-detail routes if the product has shareable artifacts.

## Validation Checklist

- `frontend`: `npm run lint`, `npm run build`.
- `backend`: `go test ./...`.
- Mobile viewport:
  - nav menus open, close, and fit.
  - no button text overflows.
  - cards and skeletons keep dimensions.
  - footer wraps without horizontal scroll.
- Desktop viewport:
  - primary nav and overflow nav are aligned.
  - sticky authenticated nav does not cover content.
  - modals and sidebars are scroll-safe.
- Auth:
  - anonymous protected route redirects to sign-in.
  - unverified account redirects to verify email.
  - return-to survives sign-in/sign-up/verification.
- Payments:
  - frontend cannot set discounted rates.
  - webhook and boot-time sync grant entitlements once.
  - portal/cancel/change tier paths exist.
- Support:
  - user can submit a ticket.
  - admin receives alert.
  - admin response emails the user.
- Privacy:
  - localStorage failure does not break core flows.
  - delete/redact paths match legal policy.
  - secrets never appear in `NEXT_PUBLIC_*`.
