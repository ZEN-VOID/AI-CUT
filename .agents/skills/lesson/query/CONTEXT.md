# CONTEXT.md

本文件是 `lesson/query` 的经验层知识库，不是第二份执行合同。它保存课程项目事实查询、truth-role 判定、存在/完成/验收区分、三端交付路径和路由漂移诊断中的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-06-05
recommended_action: keep-query-heuristics-focused
```

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 把 `.agents/skills/lesson/` 当成课程项目结果目录 | project-root guard | 先定位 `projects/lesson/<项目名>/` | 在 `SKILL.md#Thinking-Action Node Map` 固定 root lock | 证据路径落在真实项目根 |
| 把 DOC/PPT/HTML 导出物存在说成课程阶段完成 | delivery/status distinction | 补读 owning stage 产物和既有执行报告 | `N6-DISTINCTION` 强制分开文件存在、阶段完成、验收通过 | 答复显式列三种状态 |
| 把 `content-model/` 当成第二份阶段主稿 | content-model truth split | 查 owning stage canonical file，再把 `content-model/` 标为索引或投影证据 | Field Mapping 固定 content-model 边界 | 答复说明 stage owner 与 content-model role |
| 问下一入口时只看目录结构 | route carrier gap | 读取 lesson 根路由、阶段合同和状态载体 | `state_route` 固定 route evidence | 下一入口附合同或状态证据 |
| 多个课程项目候选时混答 | candidate ambiguity | 最多扫描一轮候选后阻断澄清 | `N2-ROOT` 固定 candidate_count gate | 不输出混合结论 |
| 查询结论像路径扫描模板 | scripted conclusion | 废弃模板化结论，回到 carrier 证据和 LLM status distinction | Review Gate Binding 固定 authorship gate | 答复说明证据如何支撑结论 |
| 把未见验收报告说成未通过 | validation overclaim | 改成“未见验收证据”，不推断失败 | Output Contract 固定无证不判 PASS/FAIL | 答复保留 evidence gap |

## Repair Playbook

1. 任何课程项目查询先锁 `PROJECT_ROOT`，再判 truth role。
2. 用户问“有没有 / 在哪”时回答文件存在；用户问“完成了吗”时补查 owning stage 完成证据；用户问“通过了吗”时补查既有验收 PASS 证据。
3. 用户问 DOC/PPT/HTML 时，先说明交付路径，再追溯上游 `content-model/` 或 owning stage；不要把末端导出物当课程质量证据。
4. 用户问路由、下一入口或为什么进入某阶段时，先读 lesson 根合同和相关阶段/卫星合同，再看项目目录。
5. carrier 缺失时报告已检查路径和缺口，不自行创建、不修复、不验收。
6. 若发现可复用失败模式，先写入本 `CONTEXT.md`；稳定后再晋升到 `SKILL.md`。
7. 查询报告如果被用户要求保存，只能是辅助证据，不得成为阶段状态、项目进度或验收真源。

## Reusable Heuristics

- `lesson-query` 的价值不是全仓搜索，而是先判断“哪个 carrier 有资格回答这个课程问题”。
- 课程项目事实以 `projects/lesson/<项目名>/` 为 runtime 真源；技能目录只能回答制度合同，不回答业务完成状态。
- `content-model/` 是 DOC/PPT/HTML 的共享上游和投影索引，不是第二套课程主稿。
- 文件存在、阶段完成、验收通过是三个不同结论：存在看路径，完成看 owning stage 完成证据，验收通过看既有 PASS 证据。
- 没有执行报告或验收报告时，只能说“未见完成/验收证据”，不能说“已完成”“已通过”或“失败”。
- 对三端交付查询，先区分 DOC、PPT、HTML 叶子，再检查是否共享同一上游内容模型。
- 对路由漂移查询，目录结构是现象，lesson 根合同、阶段合同和状态载体才是制度证据。
