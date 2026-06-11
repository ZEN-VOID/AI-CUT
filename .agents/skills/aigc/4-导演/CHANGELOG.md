# CHANGELOG

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求导演批注证明 `2-编剧` 画面点与 `3-美学` 画面基调如何投影为导演意图、信息差、节奏和表演交接。
- 新增 `FAIL-DIR-UPSTREAM-CONTEXT`、`GATE-DIR-20-UPSTREAM-CONTEXT` 和报告 `Upstream Context Application Map`，并将完成门扩展到 `GATE-DIR-01..20`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-04

- Created `4-导演` as a Skill 2.0 runtime-spine package.
- Added inline director annotation contract, review gates, output template, script boundary notes, local director style index, agent metadata, and regression prompts.
- Imported five `2-编导` director references into `4-导演/references/` with local adaptation notices: anticlimax strategy, directorial authorship, episode visual spine, information asymmetry, and scene rhythm.
- Updated the main runtime spine to require episode-level director intent planning before per-visual-point inline annotations.
- Added performance handoff requirements so director annotations can be passed with the screenplay to downstream performance skills and actors as concrete, visible performance seeds.
