# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/4-道具/3-面板` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-面板` 目录存在但没有可执行合同 | 叶子技能层 | 补齐 `SKILL.md + CONTEXT.md + template + runner` | 固化“空目录不算 active 技能”原则 | 目录可执行且有最小 runner |
| 面板阶段回头重扫 `3-Detail` | 输入真源层 | 锁定 `2-设计` 产物为唯一输入 | 在 `SKILL.md` 和 runner 同时固定输入根 | runner 只读取 `2-设计/第N集/` |
| prompt sidecar 缺失导致 panel prompt 变短 | 降级策略层 | 回退 `道具设计.json.prompt_anchor` 并标记 degraded mode | manifest 永远记录 sidecar 缺失 | `_manifest.json.degraded_episodes` 非空 |
| 每集被写成单一 panel 文件 | 输出契约层 | 按 `props[]` 逐道具输出 layout | 在命名合同中固定 `<prop_id>-<prop_name>-PropPanel-layout.json` | episode 输出文件数等于 prop 数 |
| 模板结构从 reference 漂移 | 模板真源层 | 回退当前目录 template，禁止脚本内再造第二套结构 | 把 layout contract 锁在 template 文件，不在脚本复制模块定义 | prompt 中能回链 mandatory rules |

## Repair Playbook

1. 先检查 `2-设计/第N集/道具设计.json` 是否存在。
2. 再检查 `prop_design_prompt.json` 是否存在，并建立 `prop_id -> prompt` 索引。
3. 读取模板，确认 `layout_generation_prompt` 和 `mandatory_rules` 存在。
4. 对每个道具分别生成 layout；不要把整集压成一个泛化 handoff。
5. sidecar 缺失时允许降级，但必须把降级状态写进 manifest。

## Reusable Heuristics

- 道具面板最稳定的输入不是导演 JSON，而是已经收束好的 `道具设计.json + prop_design_prompt.json`。
- 若当前仓库还没有稳定共享 panel engine，先固定 layout JSON 停点，比仓促接回自动生图更稳。
- 逐道具 layout 比整集单文件更适合后续审阅、回修和图像工具消费。
- reference 仓的模板可以继承，但 runtime 路径、停点和输出 contract 必须服从当前仓库真源。

## Case Log

### Case-20260412-AIGC-PROP-PANEL-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/4-道具/3-面板` 建立了可执行 skill 包，并把参考仓的 prop panel contract 映射到当前 `projects/<项目名>/4-Design/...` runtime。
- root_cause_or_design_decision: 当前仓库 `4-道具` 已有 `1-清单` 与 `2-设计`，但 `3-面板` 仍是空目录；若直接照搬旧仓自动生图逻辑，会把旧 `output/影片/...` 路径与共享 panel engine 依赖一并带入，形成新的第二真源。
- final_fix_or_heuristic: 保留 reference 的 panel dossier 模板和门禁语义，但将输入锁定为 `2-设计` 产物，输出收口到 `projects/<项目名>/4-Design/4-道具/3-面板/第N集/`，并在本轮只生成 layout JSON + manifest。
- prevention_or_replication_checklist:
  - [x] 叶子 skill 合同已存在
  - [x] 模板与 runner 已落地
  - [x] 当前 runtime 路径已 canonicalized
  - [x] 降级路径已进入 manifest
- evidence_paths:
  - `.agents/skills/aigc/4-Design/4-道具/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/3-面板/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/4-道具/3-面板/templates/道具面板-提示词.json`
  - `.agents/skills/aigc/4-Design/4-道具/3-面板/scripts/generate_prop_panels.py`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/4-面板/道具面板/SKILL.md`
- user_feedback_or_constraint: 用户要求完善当前仓库的 `3-面板`，并以 AIGC-ZEN-VOID 的道具面板为参考，而不是直接复制旧链路。
