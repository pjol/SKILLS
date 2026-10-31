---
name: skills-repo-index
description: Index and governance map for this skills repository. Use when orienting in or maintaining the repo, choosing which local skill to invoke, adding or updating skills, or routing app-building work to the scaffold skill tree.
---

# Skills Repo Index

## Purpose

Use this skill as the top-level map for the repository. It should help an agent choose the right local skill quickly, understand how skills relate to each other, and keep the catalog current without loading every skill body or reference file.

Keep this skill concise. Do not duplicate detailed instructions from child skills; point to them and summarize their triggers.

## Current Catalog

### `scaffold/`

A pointer to the app-building skill tree and toolset. The skill lives in its own private repo, `github.com/pjol/scaffold`, cloned at `~/scaffold`.

Use it for:

- Starting a new app on the shared stack: a Go API (chi, pgxpool, Postgres, S3, Clerk), a Next.js web app and an Expo mobile app.
- Adding feature modules to an existing scaffold project, or reviewing a project against the foundation.
- Design system and process, env naming, dev-up, project docs and store compliance.

Load order: `scaffold/SKILL.md` here → `~/scaffold/SKILL.md` → `~/scaffold/concrete/SKILL.md` or `~/scaffold/feature-belt/SKILL.md`, depending on the task.

Replaced `backend-setup` and `user-facing-app-context`, which were removed on 2026-10-31 and are still in git history.

### `time-accounting/`

Measuring how long work actually took, and writing the figure down honestly.

Use it for:

- Any output that carries hours: branch scopes, work logs, status notes, estimates, invoices.
- Auditing an hours figure that looks wrong, or one written before this skill existed.
- Installing the `UserPromptSubmit` timestamp hook that makes elapsed time visible live.

Carries `scripts/measure_sittings.py`, which clusters session-transcript timestamps into sittings on a 30-minute gap and prints the measured total.

Independent of the app-building family: it applies to any work in any repo.

## Skill Families

`time-accounting` stands alone: it is about reporting work, not building it, and has no hub.

`scaffold` is the hub for building apps. Its sub-skills (`concrete`, `feature-belt`) and its feature modules live in the scaffold repo, not here. New app-building work goes into that repo: a foundation rule into `concrete/`, a reusable feature into `feature-belt/`. Add a satellite skill here only when it is narrower than scaffold and doesn't belong in an app: for example deployment runbooks or provider-account setup.

When adding a satellite skill:

- Make the satellite's trigger narrower than the hub.
- Reference the hub when the satellite assumes the same stack and design posture.
- Avoid copying hub content into the satellite.

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
