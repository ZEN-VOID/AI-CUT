# Story2026 Genre Templates

`templates/genres/` is the canonical root for story2026 genre knowledge.

## Layout

- Entry templates stay at `templates/genres/{中文题材}.md`.
- Deep-dive packs live at `templates/genres/details/{genre_slug}/`.
- Do not create or revive a parallel root such as `story2026/genres/`.

## Current detail-pack mapping

| detail slug | canonical entry template |
|---|---|
| `xuanhuan` | `修仙.md` |
| `rules-mystery` | `规则怪谈.md` |
| `zhihu-short` | `知乎短篇.md` |
| `dog-blood-romance` | `狗血言情.md` |
| `period-drama` | `古言.md` |
| `realistic` | `现实题材.md` |

## Usage rule

- Initialization and scaffold flows should keep using the entry templates.
- When a task needs finer-grained genre craft guidance, load the matching detail pack from `details/`.
- Planning modules may read the same shared genre assets, but must not create skill-private trope mirrors under `references/`.
- If a genre needs new craft knowledge, add it to `templates/genres/{中文题材}.md` or `templates/genres/details/{genre_slug}/`, not to a single stage's private folder.

## Shared Heuristics

- Use roughly `70%` expected genre satisfaction plus `30%` surprise so the book feels legible without becoming assembly-line.
- Do not repeat the exact same trope beat more than 3 times in a row without a variant, reversal, or cost escalation.
- Villains, face-slapping beats, and power reveals should change texture with setting and status; do not let every scene speak in the same stock voice.
