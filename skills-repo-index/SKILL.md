---
name: skills-repo-index
description: Index and governance map for this skills repository. Use when orienting in or maintaining the repo, choosing which local skill to invoke, adding or updating skills, or routing app-building work through the user-facing-app-context and backend-setup hubs.
---

# Skills Repo Index

## Purpose

Use this skill as the top-level map for the repository. It should help an agent choose the right local skill quickly, understand how skills relate to each other, and keep the catalog current without loading every skill body or reference file.

Keep this skill concise. Do not duplicate detailed instructions from child skills; point to them and summarize their triggers.

## Current Catalog

### `backend-setup/`

Backend foundation skill for reusable Go/Postgres API services.

Use it for:

- Go service layout, preferred packages, and runtime assembly.
- Env/config loading, backend-local path anchoring, and Postgres via pgxpool.
- Router/middleware shape, auth/CSRF/admin gates, billing, uploads, email, support, and service boundaries.
- GAEA-derived activity/error JSONL logging, request logging, and backend validation.

This skill is the backend source of truth for `user-facing-app-context`.

### `user-facing-app-context/`

Hub skill for spinning up polished consumer-facing web apps quickly.

Use it for:

- B2C or prosumer app shells.
- Next.js App Router frontends with Tailwind and lucide icons.
- Backend-facing app surfaces that delegate backend implementation details to `backend-setup`.
- Shared app surfaces: public home, auth, settings/billing, history/recovery, support, legal, admin, share/download, and machine-readable routes.
- Reusable design-system and implementation preferences for compact, tactile, responsive apps.

Load order inside the skill:

1. `references/00-app-map.md` for the reusable route and app-boundary map.
2. `references/01-frontend-framework.md` before frontend routes, components, auth flow, API clients, navigation, or browser storage.
3. `references/02-design-system.md` before user-facing UI decisions.
4. `backend-setup/` before API, auth, billing, storage, support, observability, or backend behavior.
5. `references/04-implementation-playbook.md` before scaffolding or porting the pattern into a new app.

Do not use it to copy product-specific generation pipelines, private prompts, model queues, old product nouns, prices, screenshots, live IDs, or user data.

### `time-accounting/`

Measuring how long work actually took, and writing the figure down honestly.

Use it for:

- Any output that carries hours: branch scopes, work logs, status notes, estimates, invoices.
- Auditing an hours figure that looks wrong, or one written before this skill existed.
- Installing the `UserPromptSubmit` timestamp hook that makes elapsed time visible live.

Carries `scripts/measure_sittings.py`, which clusters session-transcript timestamps into sittings on a 30-minute gap and prints the measured total.

Independent of the app-building family below — it applies to any work in any repo.

## Skill Families

`time-accounting` stands alone: it is about reporting work, not building it, and has no hub.

`user-facing-app-context` is the root hub for B2C app-building skills. `backend-setup` is the backend foundation it delegates to. Future skills in that family should be more focused satellites, such as provider-specific payments, deployment, analytics, image/media workflows, admin tooling, or frontend component patterns.

When adding a satellite skill:

- Make the satellite's trigger narrower than the hub.
- Reference the hub when the satellite assumes the same frontend/backend/design posture.
- Keep framework-wide defaults in the hub unless the satellite needs task-specific detail.
- Avoid copying hub reference content into the satellite.

## Routing Workflow

1. Match the user's request against the current catalog.
2. Load the matching skill's `SKILL.md`.
3. Load only the referenced files needed for the task.
4. If the task is about creating or editing skills, also use the system `skill-creator` guidance.
5. If no skill matches, work normally and consider whether the repository should gain a new skill.

## Maintenance Rules

- Update `Current Catalog` whenever a skill is added, removed, renamed, or meaningfully repurposed.
- Keep each catalog entry to its trigger, scope, and load order; detailed workflows belong in the child skill.
- Keep frontmatter descriptions specific enough that the right skill triggers without requiring this index first.
- Keep `agents/openai.yaml` aligned with each skill's current purpose.
- Leave unrelated or user-owned worktree changes untouched while maintaining the repo.

## Validation

After editing this skill or any indexed skill, run the skill validator when available:

```sh
python3 /Users/coding/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills-repo-index
```
