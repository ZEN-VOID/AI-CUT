# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design/3-面板设计` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/3-面板设计/SKILL.md` 时，应在 `aigc -> 2-主体设计` 根链之后加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| panel 阶段绕过 `2-主体设计` 直接从 detail 或 list 发明 layout | 输入 carrier 层 | 回退到对应 domain 的 design carrier | 父层固定“只能从 `2-主体设计` 起步”的规则 | 不再从上游低层真源直接造 panel |
| 模板缺失时脚本临时拼结构 | 模板真源层 | 阻塞对应域并报告 template 缺口 | 在父层把 template readiness 写成硬门槛 | 没有第二套隐式模板 |
| manifest 或 aggregate 开始承载设计事实 | 输出治理层 | 恢复 packet 为唯一展示事实载体 | 在父层与 leaf 共同固定 packet / aggregate / manifest 分层 | aggregate 只做汇总，manifest 只做审计 |
| full-build 时四域被无意义串行 | 调度拓扑层 | 回到多域并行候选 + selective dispatch | 在父层显式声明“并行候选，不靠名称序号推断” | 多域构建时长下降 |
| `5-Image` 仍需重猜 packet 路径或 prompt 来源 | handoff 层 | 回查各域 packet 命名与输出根 | 在父层验收里强制检查 handoff readiness | 下游直接定位 packet 与 manifest |
| 自动生图时每个 leaf 都私有一套 prompt/ref 规则 | 真源治理层 | 收回到 `_shared/smart-image-handoff-contract.md` + 共享桥接脚本 | 统一 request sidecar、SMART 判型和 continuity ref 扫描 | 四域自动生图合同不再漂移 |
| 用户单独点某个 JSON 生图，却被隐式塞进 continuity refs | SMART 模式层 | 将 resolved mode 切到 `single-doc-t2i` | 在共享合同固化“单文档默认 T2I” | 单文件请求不再误走 I2I |

## Repair Playbook

1. 先确认本轮命中的 panel 域，避免把 domain-local 模板问题误修成父层问题。
2. 再检查该域是否从对应 `2-主体设计` carrier 起步。
3. 再检查模板是否存在，以及 leaf 是否已显式声明 packet 输出根。
4. 若是多域构建，优先检查 selective dispatch 与并行策略，而不是默认全串行。
5. 若开启自动生图，再检查 request sidecar 是否来自 packet 真源字段，且 `SMART` resolved mode 是否正确。
6. 最后汇总到 `projects/aigc/<项目名>/4-Design/validation-report.md`，记录 blocked templates、handoff 状态和自动生图桥结果。

## Reusable Heuristics

- `3-面板设计` 的核心不是“再写一版设计”，而是把已有 design carrier 稳定投影为展示 packet。
- 面板阶段最容易坏的是真源层级：一旦回头读取 detail 或 list，当轮 packet 就会带入错误的事实来源。
- 多域 panel build 通常没有强依赖，默认应视为并行候选；真正需要串行的是人工审阅或共享汇报，而不是 packet 生成本身。
- template readiness 比 prompt 细节更优先，因为没有模板就不存在稳定的 layout contract。
- stage-level 验收只需要回答三个问题：命中了哪些域、哪些域 blocked、哪些 packet 已可交给 `5-Image / review`。
- 若要在 `3-面板` 直接自动生图，最稳的做法不是在四个 leaf 里各造 prompt，而是从 packet 写统一 request sidecar 再调用 `nano-banana/general`。
- `SMART` 的关键不是“总带参考图”，而是“连续批量任务自动继承 `2-设计` 图像；单文档请求默认 T2I”。
