# Source Truth Ledger

本文件定义 repair 时各层真源和禁止越权边界。

## Truth Owners

| layer | owns | repair rule |
| --- | --- | --- |
| `MEMORY.md` | 项目长期偏好、稳定禁区、持续口径 | 只有用户明确要求记住或改动将长期生效时写回 |
| `0-初始化` | 项目立项、north_star、global/style/genre direction | 题材方向或总风格错误先修此层 |
| `1-设定` | 角色、场景、物品、技能对象真源 | 对象身份、状态、关系、能力和物件机制先修此层 |
| `2-卷章` | 整书、卷、章规划，线索/伏笔/任务链 | 结构、线索、伏笔、卷章义务先修此层 |
| `3-初稿` | 章节正文初稿业务真源与初稿内置验收包 | 只拥有初稿执行与 handoff 到 `4-润色`，不拥有上游设定或 return actualization |
| `4-润色` | 基于初稿的最小局部修补稿与终稿内置验收包 | 不覆盖初稿、planning、cards 或 actualization 写回 |
| `return` | PASS 后的 accepted actualization 和投影刷新 | 不改规划正文，不替代阶段验收 |
| `STATE.json` | workflow runtime 状态和 completion records | 只记录状态，不制造创作事实 |

## Writeback Order

默认顺序：

1. 用户授权的新长期记忆或禁区。
2. 最早 canonical source。
3. 同层 planning/card projection。
4. 已产出正文或润色稿。
5. stage acceptance packet、return actualization 和 `STATE.json`。
6. 后续 provider prompt/handoff guardrail。

## Authorship Boundary

- repair diagnosis、impact map、repair plan、finding 汇总和验收由 `story-repair` 持有。
- 创作性正文改写由 owning stage 根技能持有：`3-初稿` 或 `4-润色`。
- 当用户指定的目标文档头部含 legacy `写作模型` / `润色模型` 字段时，该字段只作为历史执行环境线索，不得作为默认路由或返工归属。
- 模型/API/provider 的使用只记录为 `creative_engine_note`；不得恢复旧模型分流或用模型字段覆盖阶段真源。
- 若用户显式切换执行环境，只需在报告中说明；新产物 frontmatter 仍使用阶段字段。
- 脚本可读取、diff、统计、校验和落盘，不得生成 canonical creative truth。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 本次修复是否锁定最早 canonical owner，并按 source -> projection -> draft/polish -> acceptance/return/state -> future guardrail 的顺序处理？ | `source_priority` | `FAIL-REPAIR-OWNER` | `steps/repair-workflow.md#N3-OWNER-ROUTE`、`steps/repair-workflow.md#N4-SOURCE-WRITEBACK` | `canonical_owner`、`writeback_order`、changed files 顺序 |
| 是否避免让 `3-初稿`、`4-润色`、return 或 STATE 越权拥有上游设定、规划或非本阶段验收事实？ | `cards_planning_alignment` | `FAIL-REPAIR-OWNER` | `references/source-truth-ledger.md#Truth Owners`、`steps/repair-workflow.md#N6-DOWNSTREAM-SYNC` | owner ledger 判定、未改文件理由、同步/失效动作 |
| 创作性正文修复是否回到 owning stage 根技能，而不是由 repair brief、脚本或验收 finding 直接改写？ | `authorship` | `FAIL-REPAIR-AUTHORSHIP` | `steps/repair-workflow.md#N5-STAGE-REPAIR-BRIEF` | `owning_stage`、repair brief、creative authorship note |
| 用户显式切换执行环境时，是否只记录 `creative_engine_note`，并保持阶段 frontmatter 合同？ | `authorship` | `FAIL-REPAIR-AUTHORSHIP` | `steps/repair-workflow.md#N5-STAGE-REPAIR-BRIEF`、`SKILL.md#Execution Contract` | 切换授权、阶段字段、final report 说明 |
| 脚本是否只做读取、diff、统计、校验和落盘，没有生成 canonical creative truth？ | `runtime_behavior` | `FAIL-REPAIR-RUNTIME` | `guardrails/guardrails-contract.md`、`scripts/README.md` | 脚本调用清单、人工/LLM 创作判定、final report 降级说明 |
