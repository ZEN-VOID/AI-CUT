# Changelog

## 2026-06-10

- 新增 `_shared/upstream-context-application-contract.md`，把主链 `2-编剧` 到 `9-光影` 的上游 context 从“读取证明”升级为“应用证明”。
- 根 `SKILL.md` 新增 `PASS-AIGC-06` / `FAIL-AIGC-UPSTREAM-CONTEXT`，要求阶段执行报告包含 `Upstream Context Application Map`，证明 `source_anchor -> local_decision -> preservation_check`。
- 根 `CONTEXT.md` 新增 `AIGC-TM-09`，用于识别“下游读了上游但各说各话”的源层失败模式。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。
