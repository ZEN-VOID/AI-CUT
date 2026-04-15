---
name: "example-skill"
description: "Describe when this skill should be used and what it helps accomplish."
---

# Example Skill

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

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
