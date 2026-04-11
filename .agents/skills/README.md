# Skills

Store project-specific Codex skills here.

Conventions:

- One folder per skill
- Each skill folder should include a `SKILL.md`
- Add helper scripts or reference files inside the same skill folder when needed

Recommended layout:

```text
.agents/skills/
  my-skill/
    SKILL.md
    scripts/
    references/
    assets/
```

This is the canonical skill root for the starter.

`.codex/skills` may exist as a compatibility alias, but new projects should treat `.agents/skills` as the source of truth.

Start from `../../.codex/templates/skill/SKILL.md`.
