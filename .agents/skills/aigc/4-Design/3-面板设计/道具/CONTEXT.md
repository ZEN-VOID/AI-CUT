# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-面板设计/道具` 的经验层知识库，不是过程日志。
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
| 面板阶段回头重扫 `3-Detail` | 输入真源层 | 锁定 `2-设计` 产物为唯一输入 | 在 `SKILL.md` 和 runner 同时固定输入根 | runner 只读取 `2-设计/第N集/` |
| prompt sidecar 缺失导致 panel prompt 变短 | 降级策略层 | 回退 `道具设计.json.prompt_anchor` 并标记 degraded mode | manifest 永远记录 sidecar 缺失 | `_manifest.json.degraded_episodes` 非空 |
| 每集被写成单一 panel 文件 | 输出契约层 | 按 `props[]` 逐道具输出 layout | 在命名合同中固定 `<prop_id>-<prop_name>-PropPanel-layout.json` | episode 输出文件数等于 prop 数 |
| 模板结构从 reference 漂移 | 模板真源层 | 回退当前目录 template，禁止脚本内再造第二套结构 | 把 layout contract 锁在 template 文件，不在脚本复制模块定义 | prompt 中能回链 mandatory rules |
| 面板技能要依赖历史说明或 references 才能看懂降级与 manifest 规则 | 合同真源层 | 将输入门禁、模板锁定、逐 prop dossier、manifest 汇流全部收回主 `SKILL.md` | 固化“展示型叶子技能也必须主文档单读可执行” | 只读主文档即可理解 panel 输出链 |
| 连续批量任务里道具设计图没有自动接到 panel 生图 | SMART bridge 层 | 以 `道具设计.json` 所在 episode 根做 continuity ref 扫描，再统一桥接 `nano-banana/general` | packet 写 `image_generation`，ref 扫描收口到共享 bridge 脚本 | request sidecar 中 continuity refs 指向 `2-设计/第N集/` |

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
- 对展示型叶子技能来说，最关键的不是 prose 解释，而是把“输入门禁 -> 模板锁定 -> prompt 组装 -> layout 写回 -> manifest 审计”写成主文档中的稳定节点。
- 道具面板启用自动生图时，不要把 continuity ref 扫描写进每个 leaf 的私有逻辑；直接复用 packet 的 `prompt` 和共享 SMART bridge 更稳。
