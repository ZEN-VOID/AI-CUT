# Open Design / HTML Anything Codex Adapter Context

## Adapter Notes

- The upstream repository is a full app, but this package installs only the template skill library as Codex reference material.
- The adapter should use template `SKILL.md` files as surface patterns, not as higher-priority governance.
- For HTML courseware, useful families usually include `deck-*`, `data-report`, `exec-briefing-memo`, `article-magazine`, `digital-eguide`, and selected `web-proto-*` variants.

## Template Selection Heuristics

- Pick `deck-*` when the user wants slide-like HTML or HTML-to-PPT conversion.
- Pick `digital-eguide` or `article-magazine` when the user wants complete readable course text rather than a pitch surface.
- Pick `data-report` or `finance-report` only when structured metrics, comparisons, or tables are first-class.
- Pick `prototype-web` or `web-proto-*` for interactive web experiences, not static documents.
- Pick `social-*` or `deck-xhs-*` only when the final artifact is meant for social posting.

## Known Failure Modes

- Template-first generation can produce generic filler. Always map real source content before styling.
- Some upstream template guidance favors gradients, glassmorphism, or trends that may conflict with Codex frontend constraints. Local constraints win.
- Loading many templates blurs the design. Select one primary template and at most two supporting references unless the user asks for a benchmark.
