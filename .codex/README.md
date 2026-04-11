# Project Codex Directory

This `.codex` directory is the project-level home for Codex collaboration assets that are safe and useful to version in the repository.

It is intentionally different from a user-level `~/.codex`:

- This folder stores project guidance, reusable workflows, templates, and automation definitions.
- This folder should not store local runtime databases, chat history, auth tokens, or machine-specific caches.

## Structure

- `.agents/skills/`: canonical repo-local skills, one folder per skill
- `agents/`: role definitions for specialized agents used in this repository
- `skills/`: compatibility alias pointing to `../.agents/skills`
- `registry/`: capability registration, route policy, and legacy mapping truth
- `runbooks/`: task lifecycle and operational procedures
- `state/`: task-level status and evidence carriers
- `evals/`: bootstrap and regression evaluation entrypoints
- `schemas/`: shared schema truth once templates stabilize
- `plugins/`: local plugin skeletons and plugin-related notes
- `rules/`: durable repo rules and operating conventions
- `automations/`: project automation specs and scheduling notes
- `prompts/`: reusable prompts for recurring tasks
- `templates/`: starter templates for skills, plugins, and agent docs
- `scripts/`: helper scripts that support local Codex workflows
- `docs/`: extra documentation for the Codex setup in this repo

## Quick Start

1. Put high-level repo instructions in the root `AGENTS.md`.
2. Put shared operational rules in `rules/project.rules`.
3. Add project-specific workflows in `.agents/skills/<name>/SKILL.md`.
4. Add specialized role docs in `agents/`.
5. Register repo-local capabilities in `registry/` before expanding workflows.
6. Use `templates/` and `runbooks/` when creating a new skill, plugin, or agent role.

## Suggested Conventions

- Prefer small, focused skills over one very large skill.
- Keep agent role docs short and outcome-oriented.
- Never store secrets in prompts, repo docs, or automation files.
- Treat `.agents/skills` as canonical and `.codex/skills` as a compatibility alias only.
- Treat `registry/`, `runbooks/`, `state/`, and `templates/harness/` as the bootstrap harness truth.
