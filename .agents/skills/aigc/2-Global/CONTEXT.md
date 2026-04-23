# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-23

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-Global` 仍把四份 Markdown 当默认真源 | 输出治理层 | 收回到 `episode_root.json` 直写 | 在 `SKILL.md + IO_CONTRACT + branch-output-contract` 同步固化单一 JSON 输出 | `2-Global` 的 canonical 输出只剩 `episode_root.json + validation-report.md` |
| `episode_root.json` 不是围绕模板填，而是边写边发明结构 | 模板治理层 | 回到 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 对齐字段 | 在 shared contract 中把模板声明为唯一填写真源 | 所有字段都能直接对应模板槽位 |
| 组级字段仍通过 Markdown 中转 | handoff 层 | 直接在 JSON 中定稿 `global.*` | 在 `group_design_seed_contract` 固化“直接写 JSON，不经 Markdown 中转” | `3-Detail` 不再依赖 `2-Global/*.md` 才能消费上游 seed |
| `groups[].global.剧本正文` 写成摘要 | 组壳写回层 | 强制把命中组全文完整入壳 | 在 `Writeback Policy` 与验收清单中固化全文入壳规则 | 下游可直接继承原组文本 |
| 项目级字段和组级字段混写 | 结构分层层 | 项目级写入 `project_global`，组级写入 `groups[].global` | 在模板与 I/O 合同中固定分层 | `project_global.全集类型元素` 不再漂到组级，组级类型/导演意图不再污染项目总则 |
| 旧下游仍依赖 Markdown，导致切换卡住 | 兼容层 | 明确 Markdown 只做 derived projection | 在合同中写明 compat projection 不拥有真源地位 | JSON-first 切换后仍可渐进兼容旧消费者 |

## Repair Playbook

1. 先看 `2-Global/SKILL.md` 是否明确围绕 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 填写。
2. 再看 `_shared/IO_CONTRACT.md` 与 `_shared/branch-output-contract.md` 是否仍把 `episode_root.json` 定义为唯一业务真源。
3. 再看 `_shared/group_design_seed_contract.md` 是否仍要求 `3-Detail` 从 JSON 直接继承，而不是从 Markdown 抽取。
4. 最后才看是否需要保留兼容 Markdown 投影。

## Reusable Heuristics

- `2-Global` 最稳的形态不是“四份长文定稿后再抽 JSON”，而是“围绕 `episode_root.json` 模板直接填好字段”。
- 若要和 `3-Detail` 对齐，真正要对齐的是“模板中心 + 单一 JSON 真源 + 直接 patch-in-place”，而不是只对齐文件后缀。
- `project_global` 负责项目级稳定项，`groups[].global` 负责当前集组级 seed；这层分工一旦混掉，`3-Detail` 就会失焦。
- `groups[].global.剧本正文` 必须保留原组全文；任何“为了更结构化所以顺手摘要一下”的做法都会伤到下游。
- 兼容 Markdown 可以保留，但只能是 derived projection，不能再被当作 canonical creative truth。
