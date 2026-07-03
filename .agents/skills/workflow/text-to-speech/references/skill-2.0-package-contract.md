# Package Contract

本文件展开 `text-to-speech` 的包维护细则。运行时真源仍是 `SKILL.md`；本文件只用于检查 Skill 2.0 包结构是否和运行合同保持同步。

## Scope

- Applies to package maintenance, review, and future edits under `.agents/skills/workflow/text-to-speech`.
- Does not define new TTS behavior beyond what `SKILL.md` already authorizes.
- Any change to default paths, voice pool, overwrite behavior, title filtering, CLI path, manifest format, or completion criteria must update `SKILL.md` and the affected script in the same change.

## Rules

1. `SKILL.md` owns the runtime spine: input, type routing, node map, gates, module triggers, guardrails, and output contract.
2. `scripts/generate_missing_audio.py` owns mechanical execution only: scan, plan, local MiniMax CLI call, retry, manifest, and nonempty output check.
3. `review/review-contract.md` owns expanded review questions and fail-code coverage.
4. `templates/` owns report shape only and must not introduce new pass/fail rules.
5. `CONTEXT/` files store examples and learnings only; stable rules must be promoted back to `SKILL.md`.
6. Real API keys must never be copied into this package. Examples must use environment references such as `$MINIMAX_API_KEY`.

## Review Gate Mapping

Every mandatory rule, anti-pattern, and review question in this reference must have an executable review landing point. Do not leave review questions as soft prompts.

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does `SKILL.md` remain the only runtime truth for default paths, voice pool, title filtering, overwrite behavior, and output naming? | `C1-SPINE-READY` / `C2-MODULES-BOUND` | `FAIL-PACKAGE-CONTRACT` | `SKILL.md` Core Task Contract and Module Loading Matrix | package diff and module audit |
| Does the script implement only the rules authorized by `SKILL.md`? | `C4-VALIDATION-PASS` | `FAIL-PACKAGE-SCRIPT-DRIFT` | `scripts/generate_missing_audio.py` | script argument audit and dry-run output |
| Are secrets excluded from package docs, scripts, manifests, and examples? | `Review Gate Binding` secret check | `FAIL-SECRET-LEAK` | `N5-CLOSE` / package docs | secret scan summary |

## SKILL.md Boundary

- Keep input and output decisions in `SKILL.md`.
- Keep `Multi-Subskill Continuous Workflow` in `SKILL.md` so whole-package calls have a stable default dispatch contract.
- Output decisions include required output, output format, output path, naming convention, and completion gate.
- Keep output content templates aligned with those Output Contract decisions.
- Move process details, long rules, examples, and edge-case handling into modules only when `SKILL.md` authorizes those modules in `Module Loading Matrix` and maps actual loading through `Module Trigger Matrix`.

## Multi-Subskill Continuous Workflow

Every long-lived skill must standardize whole-package dispatch:

- Unnumbered sibling subskill packages default to all-selected parallel execution.
- Number-prefixed subskill packages or nodes default to ascending serial execution.
- Letter-prefixed subskill packages or routes default to intent-based single-route branching unless the user explicitly asks for comparison, parallel routes, or batch multi-route execution.
- Satellite skills and query/resume/review side channels do not join the main chain by default.
- Blocking gates still apply when required input is missing, destructive action is not authorized, a subskill is missing, or ambiguous routing would cause an incorrect canonical writeback.

## Agent Metadata

- `agents/openai.yaml` stores product-specific interface metadata.
- `interface.default_prompt` must explicitly mention `$text-to-speech`.

## Source Ownership

- Consumed by `SKILL.md` `Directory Structure & Detail Routing Contract`, `Module Loading Matrix`, and `Review Gate Binding`.
- If this file changes route, gate, or output behavior, update `SKILL.md` and `review/review-contract.md` in the same change.
