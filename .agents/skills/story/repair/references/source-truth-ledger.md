# Source Truth Ledger

本文件定义 repair 时各层真源和禁止越权边界。

## Truth Owners

| layer | owns | repair rule |
| --- | --- | --- |
| `MEMORY.md` | 项目长期偏好、稳定禁区、持续口径 | 只有用户明确要求记住或改动将长期生效时写回 |
| `0-初始化` | 项目立项、north_star、global/style/genre direction | 题材方向或总风格错误先修此层 |
| `1-设定` | 角色、场景、物品、技能对象真源 | 对象身份、状态、关系、能力和物件机制先修此层 |
| `2-卷章` | 整书、卷、章规划，线索/伏笔/任务链 | 结构、线索、伏笔、卷章义务先修此层 |
| `3-初稿` | 章节正文初稿业务真源 | 只拥有正文执行，不拥有上游设定和 review 判定 |
| `4-润色` | 基于初稿的最小局部修补稿 | 不覆盖初稿、planning、cards 或 review 判定 |
| `review` | 质量判定、aggregate gate、repair finding | 不直接改写正文或 actualization |
| `return` | PASS 后的 accepted actualization 和投影刷新 | 不改规划正文，不替代审查 |
| `STATE.json` | workflow runtime 状态和 completion records | 只记录状态，不制造创作事实 |

## Writeback Order

默认顺序：

1. 用户授权的新长期记忆或禁区。
2. 最早 canonical source。
3. 同层 planning/card projection。
4. 已产出正文或润色稿。
5. review aggregate、return actualization 和 `STATE.json`。
6. 后续 provider prompt/handoff guardrail。

## Authorship Boundary

- repair diagnosis、impact map、repair plan、finding 汇总和验收由 `story-repair` 持有。
- 创作性正文改写由 owning stage 和原 provider lane 持有。
- 当用户指定的目标文档头部含 `写作模型` 字段时，该字段是本次内容调整的默认 provider lane 证据；除非用户显式要求切换写作模型，否则必须按该模型执行正文调整。
- B/C provider lane 的修复需要 provider messages/report；缺失时不得声称保持原 lane。
- 若用户显式切换写作模型，必须同步更新目标文档 `写作模型`、provider sidecar/evidence 与最终报告，禁止保留旧模型标记来承载新模型正文。
- 脚本可读取、diff、统计、校验和落盘，不得生成 canonical creative truth。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 本次修复是否锁定最早 canonical owner，并按 source -> projection -> draft/polish -> review/return/state -> future guardrail 的顺序处理？ | `source_priority` | `FAIL-REPAIR-OWNER` | `steps/repair-workflow.md#N3-OWNER-ROUTE`、`steps/repair-workflow.md#N4-SOURCE-WRITEBACK` | `canonical_owner`、`writeback_order`、changed files 顺序 |
| 是否避免让 `3-初稿`、`4-润色`、review、return 或 STATE 越权拥有上游设定、规划或验收事实？ | `cards_planning_alignment` | `FAIL-REPAIR-OWNER` | `references/source-truth-ledger.md#Truth Owners`、`steps/repair-workflow.md#N6-DOWNSTREAM-SYNC` | owner ledger 判定、未改文件理由、同步/失效动作 |
| 创作性正文修复是否回到 owning stage 和原 provider lane；目标文档含 `写作模型` 时是否默认遵循该字段？ | `authorship` | `FAIL-REPAIR-AUTHORSHIP` | `steps/repair-workflow.md#N5-LANE-REPAIR-BRIEF` | `creative_engine`、provider evidence、repair brief 或 sidecar |
| 用户显式切换写作模型时，是否同步更新 `写作模型`、provider sidecar/evidence 与最终报告？ | `authorship` | `FAIL-REPAIR-AUTHORSHIP` | `steps/repair-workflow.md#N5-LANE-REPAIR-BRIEF`、`SKILL.md#Execution Contract` | 切换授权、头部字段变更、sidecar/report 证据 |
| 脚本是否只做读取、diff、统计、校验和落盘，没有生成 canonical creative truth？ | `runtime_behavior` | `FAIL-REPAIR-RUNTIME` | `guardrails/guardrails-contract.md`、`scripts/README.md` | 脚本调用清单、人工/LLM 创作判定、final report 降级说明 |
