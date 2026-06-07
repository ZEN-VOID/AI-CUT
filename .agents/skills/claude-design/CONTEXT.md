# Claude Design Codex Adapter Context

## Adapter Notes

- The upstream package is intentionally preserved under `references/upstream/`. Local Codex execution should use this adapter's `SKILL.md` as the runtime contract.
- Claude-specific actions such as `/browse` are translated to Codex-available browser verification when available.
- Design authorship remains LLM-first. Scripts may copy assets, run build commands, convert files, or check output, but they should not generate creative design decisions.

## Practical Heuristics

- For a messy HTML/PPT/courseware artifact, first separate content completeness from layout craft. Stabilize source text or document order, then redesign the HTML surface.
- If content is already title-like and thin, expand it using local project resources before visual polish. Do not pad with generic filler.
- For courseware HTML, favor professional learning-product interfaces: dense but breathable sections, clear progression, examples, checklists, and practical artifacts. Avoid landing-page theatrics unless the user asks for a marketing page.
- Browser verification is part of the design pass whenever HTML is produced or substantially changed.

## Known Failure Modes

- Loading every upstream reference creates noise. Load only the references triggered by the matrix.
- "Beautiful" often hides a format problem. Decide whether the artifact is a report, deck, prototype, class handout, landing page, or visual canvas before styling.
- Missing media should remain a labeled placeholder or be sourced/generated under explicit constraints; fake product screenshots reduce trust.
