# Changelog

## 2026-06-16

- 收紧根路由对 `backup/5-表演`、`backup/6-氛围`、`backup/9-光影` 的语义：显式点名只进入只读历史回读、迁移对照或退役状态说明，不再允许试用式写回 canonical。
- 根 `CONTEXT.md` 新增 `AIGC-TM-15`，识别“退役 backup 被重新执行”的路由漂移，并将表演/氛围/光影能力分别重定向到 story 人物/场景质感模块与 `7-摄影` 光影观看纪律。

## 2026-06-10

- 新增 `_shared/upstream-context-application-contract.md`，把主链 `2-美学` 到 `8-分组` 的上游 context 从“读取证明”升级为“应用证明”。
- 根 `SKILL.md` 新增 `PASS-AIGC-06` / `FAIL-AIGC-UPSTREAM-CONTEXT`，要求阶段执行报告包含 `Upstream Context Application Map`，证明 `source_anchor -> local_decision -> preservation_check`。
- 根 `CONTEXT.md` 新增 `AIGC-TM-09`，用于识别“下游读了上游但各说各话”的源层失败模式。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。
