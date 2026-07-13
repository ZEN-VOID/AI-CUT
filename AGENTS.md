# Repository Guidelines

## 三体治理入口

- 仓库根 `AGENTS.md` 是项目级治理的唯一权威真源。
- 根 `CLAUDE.md` 与 `CODEBUDDY.md` 都必须精确为 `@AGENTS.md` 加一个结尾换行；不得复制治理正文或独立维护规则。
- 项目级规则变更只编辑 `AGENTS.md`；单一工具规则仍写入真源并显式标注适用范围。
- 完成前必须校验两个入口的精确内容，并确认相对路径可解析到根 `AGENTS.md`。

## Project Structure & Module Organization

This repository is a local AI video workflow and skill workspace, not a single application package. Repo-local skills live under `.agents/skills/`; each durable skill should keep its contract in `SKILL.md`, notes in `CONTEXT.md` or `CONTEXT/`, helpers in `scripts/`, examples in `test-prompts.json`, and tests in `tests/` when available. Codex configuration and hooks live in `.codex/`. Source media and generated outputs belong under `projects/`, especially `projects/素材/`, `projects/示例/`, and `projects/output/`. Planning and audit artifacts belong in `PRPs/` and `reports/`; these working directories are ignored.

## Build, Test, and Development Commands

There is no root build command. Run checks from the skill or tool you changed.

- `python3 -m pytest .agents/skills/version-sync/tests`: run version-sync regression tests.
- `python3 -m pytest .agents/skills/video-editing-skill/tests`: run video-editing helper tests.
- `cd .agents/skills/cli/mmx-cli && npm install`: install the local `mmx-cli` dependency wrapper.
- `python3 .codex/hooks/update_version_for_github_push.py --help`: inspect release-sync hook options.

For HyperFrames or Remotion outputs, run the relevant tool commands inside the generated project root rather than at repository root.

## Coding Style & Naming Conventions

Use Markdown for skill contracts and Python for executable helpers unless a skill already uses Node tooling. Python uses 4-space indentation, `snake_case` names, and focused command-line scripts. Skill directories use kebab-case, for example `.agents/skills/hyperframes/motion-graphics/`. Keep `SKILL.md` concise; move long references into `references/`, `review/`, `types/`, or `templates/`.

## Testing Guidelines

Prefer narrow, skill-local tests. Python tests use `pytest` and `tests/test_*.py` naming. Prompt-only workflow changes should update `test-prompts.json` or a nearby example file. Video workflow changes should include validator output, render QA notes, or an artifact path under `projects/output/[task-name]/`.

## Commit & Pull Request Guidelines

Recent history uses timestamped project-sync commits and occasional conventional commits such as `docs:` and `chore:`. For feature work, prefer an imperative scoped summary, for example `feat(workflow): add subtitle QA gate`. Pull requests should describe workflow impact, validation, related tasks, and screenshots or output paths for visual/video changes.

## Security & Configuration Tips

Never commit `.env`, API keys, access tokens, or private media. `.gitignore` excludes `.env*` except `.env.example`, plus local media/output folders. Preserve unrelated working-tree changes.

## Agent-Specific Instructions

Before editing a skill, read its `SKILL.md` completely and treat it as the runtime source of truth. This repository inherits the user-level governance baseline; repo-specific rules here should narrow or operationalize that baseline, not replace it.
