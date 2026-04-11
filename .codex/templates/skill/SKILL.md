---
name: "example-skill"
description: "Describe when this skill should be used and what it helps accomplish."
---

# Example Skill

## Use When

- The request matches a repeatable workflow
- Project-specific knowledge or steps are required

## Inputs

- User goal
- Relevant files or directories
- Constraints or output format

## Workflow

1. Gather the minimum context required.
2. Inspect the relevant files before changing anything.
3. Apply the project conventions from `AGENTS.md` and `.codex/rules/`.
4. Make the change or produce the requested output.
5. Verify the result and summarize what changed.

## Output

- A concrete result in the repo or a concise answer to the user

## Notes

- Add scripts under `scripts/` when the workflow benefits from automation.
- Add examples or reference material under `references/` if they materially help.
