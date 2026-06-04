# Artifacts And Sources Legacy Note

This reference is inactive for current `$aigc-init` execution.

Current initialization is scaffold-only and writes only:

- current `0-初始化/` through `14-审片/` project directories
- project root `MEMORY.md`
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

Source intake, story-source manifests, north-star style contracts, handoff seeds, state routing, and governance carriers must be created later only by an owning workflow that explicitly reintroduces them in its own `SKILL.md`.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does current initialization avoid former artifact and source generation? | `FIELD-INIT-05` | `FAIL-INIT-05` | `SKILL.md` `Output Contract`; `review/init-review-gate.md` | Readback confirms only scaffold directories, `MEMORY.md`, and `CONTEXT/README.md` were written. |
