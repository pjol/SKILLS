---
name: scaffold
description: "Root of the app-building skill tree and toolset: concrete (the Go/Next.js/Expo/Postgres/Clerk/S3 foundation, design system and process, env, dev-up, docs, compliance) plus feature-belt (copyable modules: chat, feed, places/maps, events, payments, wallets, AI assistant, notifications, moderation, orgs, support, identity, MCP access), driven by the scaffold CLI (also available over MCP and HTTP). Use when starting a new app, adding a feature to an existing scaffold project, reviewing a project against the foundation, or improving the scaffold itself."
---

# Scaffold

This entry only points to the skill. The specs, the running template, the feature modules and the CLI live in their own private repo, `github.com/pjol/scaffold`, cloned at `~/scaffold`.

1. Open `~/scaffold/SKILL.md`. If the folder is missing, run `gh repo clone pjol/scaffold ~/scaffold`; this needs read access to the repo. Projects built from it refer to `~/scaffold/...`, so clone it at that path.
2. Follow that file. It sends you to `concrete/` for the foundation rules, `feature-belt/` for the feature modules, and `bin/scaffold` for the CLI (`new`, `add`, `env`, `doctor`, also available over MCP and HTTP).

Scaffold replaced `backend-setup` and `user-facing-app-context`. Both were removed from this repo on 2026-10-31 and are still in its git history.
