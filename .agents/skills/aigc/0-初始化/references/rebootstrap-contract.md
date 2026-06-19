# Rebootstrap Contract

For current `$aigc-init`, rebootstrap means returning an existing AIGC project to the scaffold baseline by creating missing current `1-10` directories and creating or merging `MEMORY.md`.

It does not delete, archive, purge, or rewrite existing business artifacts.

## Allowed Rebootstrap Actions

- Create missing active runtime stage directories from `1-分集/` through `10-画布/`; do not create project-level `0-初始化/`.
- Create `MEMORY.md` if missing.
- Merge initialization-time user requirements or long-term inclinations into existing `MEMORY.md`.
- Report legacy paths or former initialization artifacts as existing compatibility material without modifying them.

## Blocked Actions Without Explicit Separate Scope

- Deleting or archiving stage outputs.
- Purging source material or original assets.
- Rewriting `north_star.yaml`, `init_handoff.yaml`, `story-source-manifest.yaml`, `team.yaml`, `STATE.json`, governance sidecars, or downstream stage outputs.
- Creating `CHANGELOG.md` or `源/` merely for structural completeness. Project `CONTEXT/` is part of the current scaffold baseline and is not a removed artifact.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does rebootstrap preserve existing files and only repair scaffold plus memory? | `FIELD-INIT-05` / `FIELD-INIT-09` | `FAIL-INIT-05` / `FAIL-INIT-09` | `SKILL.md` `N2-scaffold` and `N3-memory` | Readback lists created directories, memory updates, and skipped existing artifacts. |
