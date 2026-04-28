# Changelog

## 2026-04-28

- Added book-level timeline system via shared `../_shared/timeline-design-contract.md`.
- Added `故事编年史` to `SKILL.md`, output contract, templates, workflow nodes, review gate, and validator-facing template fields.
- Fixed book-level handoff so volume planning inherits world chronology, causal milestones, hidden events, and end-state changes before rhythm and task expansion.

## 2026-04-26

- Upgraded `story-plan-book-level` to the Skill 2.0 workshop layout.
- Added canonical sections: `steps/`, `review/`, `types/`, `knowledge-base/`, `scripts/`, `agents/`, `README.md`, and `CHANGELOG.md`.
- Rewrote `SKILL.md` as an input/output anchored dynamic reference entry.
- Preserved existing `references/book-rhythm-save-the-cat.md` and `templates/overall-planning.template.md`.
- Added `templates/output-template.md` with Output Contract Alignment for validator compatibility.
- Added `references/legacy-upgrade-migration-matrix.md` to preserve old-section traceability.
- Validation passed with `validate_skill_2_0.py` and target-scoped `skill_context_audit.py --strict`.
