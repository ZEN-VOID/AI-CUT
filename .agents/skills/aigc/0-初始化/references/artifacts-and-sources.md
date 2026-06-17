# Artifacts And Sources Legacy Note

This reference is inactive for current `$aigc-init` execution.

Current initialization is scaffold plus centralized memory and writes only:

- current `0-初始化/` through `10-画布/` project directories
- project root `MEMORY.md`, including initialization user requirements, team configuration, supplied-reference absorption summaries, and downstream context guidance
- project root `CONTEXT/README.md`

It does not create or synthesize:

- `north_star.yaml`
- `init_handoff.yaml`
- `story-source-manifest.yaml`
- `team.yaml`
- `STATE.json`
- `CHANGELOG.md`
- `源/`
- governance sidecars

Source intake, story-source manifests, handoff seeds, state routing, and governance carriers must be created later only by an owning workflow that explicitly reintroduces them in its own `SKILL.md`. Downstream aesthetic context is not owned by initialization; it must come from `2-美学/类型风格.md`, `2-美学/画面基调/全局风格协议.md`, and current-episode or baseline style protocol outputs. Initialization-time supplied materials should first be summarized into `MEMORY.md`; large raw files or indexes may be placed under project `CONTEXT/` by an owning workflow, with `MEMORY.md` retaining the usable absorbed summary.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does current initialization avoid former artifact and source generation while consolidating supplied user context into memory? | `FIELD-INIT-05` / `FIELD-INIT-09` | `FAIL-INIT-05` / `FAIL-INIT-09` | `SKILL.md` `Output Contract`; `review/init-review-gate.md`; `templates/project-memory.template.md` | Readback confirms only scaffold directories, `MEMORY.md`, and `CONTEXT/README.md` were written, and supplied context was captured or explicitly deferred. |
