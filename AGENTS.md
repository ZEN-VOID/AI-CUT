# Repository Guidelines

## Project Structure & Module Organization

This repository is a Codex workflow and skill workspace, not a single application. Repo-local skills live in `.agents/skills/`; each durable skill should keep its contract in `SKILL.md`, notes in `CONTEXT.md`, helpers in `scripts/`, tests in `tests/`, and examples in `test-prompts.json`. Codex governance and routing live in `.codex/`, especially `registry/`, `rules/`, `templates/`, and `runbooks/`. Local media and generated work belong in `projects/`, while planning and audit artifacts belong in `PRPs/` and `reports/`; these working directories are ignored by Git.

## Build, Test, and Development Commands

There is no root build command. Run checks from the skill or tool you change.

- `cd .agents/skills/video-editing-skill && python3 scripts/utils.py`: check local video-editing dependencies.
- `cd .agents/skills/video-editing-skill && pytest tests/`: run the Python regression suite.
- `cd .agents/skills/video-use && uv sync`: install `video-use` dependencies; use `pip install -e .` if `uv` is unavailable.
- `python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --help`: inspect workflow validation options before changing dialogue timing behavior.
- `npx hyperframes lint && npx hyperframes validate`: run HyperFrames checks inside generated HyperFrames project roots.

## Coding Style & Naming Conventions

Use Markdown for workflow contracts and Python for executable helpers. Python code uses 4-space indentation, `snake_case` functions/files, and focused scripts with `--help` output when practical. Skill directories use kebab-case, for example `.agents/skills/hyperframes/motion-graphics/`. Keep `SKILL.md` concise and directive-driven; move long references into `references/` or skill-local docs. Do not commit generated video, audio, or large local assets unless they are intentional fixtures.

## Testing Guidelines

Use `pytest` for Python helpers, with tests named `tests/test_*.py` beside the skill they cover. Add narrow tests for script behavior and update `test-prompts.json` for prompt-only workflow changes. For video workflow changes, include the relevant validator output, render check, or sample artifact path in your notes.

## Commit & Pull Request Guidelines

Recent history uses concise Chinese sync messages such as `项目同步更新 - YYYY-MM-DD HH:MM`. For feature work, prefer an imperative summary with a scope, such as `feat(workflow): add visual contract validator`. Pull requests should describe the workflow impact, list validation performed, link related tasks, and include screenshots or output paths for visual/video changes.

## Security & Configuration Tips

Never commit `.env` files or API keys; `.gitignore` excludes `.env*` except `.env.example`. Treat `projects/素材/` and `projects/示例/` as source pools, not canonical code. Before editing a skill, read its `SKILL.md` completely and preserve unrelated user changes in the working tree.

## Agent-Specific Instructions

默认以中文进行交流，除非用户明确要求使用其他语言，或任务本身需要英文输出。
