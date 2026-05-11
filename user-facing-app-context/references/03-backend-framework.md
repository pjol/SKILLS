# Backend Framework

Backend setup specifications now live in `$backend-setup`.

Use that skill for:

- Go runtime layout and preferred packages.
- Postgres and `pgxpool` setup.
- Env/config loading and backend-local path anchoring.
- Router and middleware setup.
- Auth, CSRF, admin gates, guest access, billing, uploads, email, and support service boundaries.
- GAEA-derived activity/error logging and request logging behavior.
- Backend tests and validation.

Keep this file only as a compatibility pointer for older workflows that still look for `references/03-backend-framework.md`.
