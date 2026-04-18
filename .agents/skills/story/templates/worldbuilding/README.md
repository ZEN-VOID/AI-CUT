# Story2026 Worldbuilding Templates

`templates/worldbuilding/` is the shared root for cross-stage worldbuilding craft.

## Scope

- These files hold reusable worldbuilding methods that may be consumed by `0-Init`, `1-Cards`, and later planning or validation passes.
- They are not stage-private `references/` and should not be copied into a single skill's local folder.
- Genre-specific world craft still belongs in `templates/genres/{中文题材}.md` or `templates/genres/details/{genre_slug}/`.

## Layout

- `character-design.md`
  - Shared character construction heuristics for early init intake and downstream card construction.
- `faction-systems.md`
  - Shared faction hierarchy and relationship design.
- `power-systems.md`
  - Shared power-system and progression design.
- `setting-consistency.md`
  - Shared consistency and contradiction-check workflow.
- `world-rules.md`
  - Shared world-rule, taboo, and setting-stage design.

## Usage Rule

- `0-Init` may read these files when collecting or normalizing object seeds, but must not treat them as canonical object truth.
- `1-Cards` may read these files as craft support when building character, scene, and item cards, but canonical truth still lands in `Cards/**/*.json`.
- If a new file is useful across more than one stage, add it here instead of stage-private `references/`.
