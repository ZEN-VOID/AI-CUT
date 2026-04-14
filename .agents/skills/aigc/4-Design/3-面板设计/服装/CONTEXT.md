# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-面板设计/服装` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-面板` 目录存在但没有可执行合同 | 叶子技能层 | 补齐 `SKILL.md + CONTEXT.md + template + runner` | 固化“空目录不算 active 技能”原则 | 目录可执行且有最小 runner |
| 面板阶段回头重扫 `角色清单 / 编导` | 输入真源层 | 锁定 `2-设计` 产物为唯一输入 | 在 `SKILL.md` 和 runner 同时固定输入根 | runner 只读取 `2-设计/第N集/` |
| prompt sidecar 缺失导致 panel prompt 变短 | 降级策略层 | 回退 `服装设计.json.prompt_anchor` 并标记 degraded mode | manifest 永远记录 sidecar 缺失 | `_manifest.json.degraded_costumes` 非空 |
| 每集被写成单一 panel 文件 | 输出契约层 | 按 `costumes[]` 逐服装输出 layout | 在命名合同中固定 `<costume_id>-<canonical_label>-CostumePanel-layout.json` | episode 输出文件数等于 costume 数 |
| 模板结构从 reference 漂移 | 模板真源层 | 回退当前目录 template，禁止脚本内再造第二套结构 | 把 layout contract 锁在 template 文件，不在脚本复制模块定义 | prompt 中能回链 mandatory rules |
| 叶子合同只说流程，不足以支撑 degraded mode 和 packet 级闭环 | 思行网络层 | 把输入门、sidecar 退化、模板锁定、逐服装 packet 组装和 manifest 汇流都收回主 `SKILL.md` | 固化 `Node Network + Capability Detail + Convergence` | `3-面板` 可直接按节点执行 |

## Reusable Heuristics

- 服装面板最稳定的输入不是角色清单，而是已经收束好的 `服装设计.json + costume_design_prompt.json`。
- 若当前仓库还没有稳定共享 panel engine，先固定 layout JSON 停点，比仓促接回自动生图更稳。
- 逐服装 layout 比整集单文件更适合后续审阅、回修和图像工具消费。
- 对 `3-面板` 做知行合一改造时，最重要的是把 degraded mode 也当成正式节点，而不是只在脚本里静默兜底。
