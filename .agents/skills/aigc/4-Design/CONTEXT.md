# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design` 的经验层知识库，不是过程日志。
- 调用本阶段父级合同时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `4-Design` 仍是空目录，根入口却把它当成已建阶段 | 阶段父级合同层 | 补齐父级 `SKILL.md + CONTEXT.md`，至少声明 active 子路径和边界 | 将“阶段已建”定义为必须存在本地合同，而不是只有目录 | 根入口与阶段真实状态一致 |
| design 阶段直接吞上游全部导演字段，不做对象池收敛 | 输出治理层 | 先进入清单子路径，把对象清单稳定落盘 | 固化“先清单、再设计、再面板”的阶段顺序 | 角色/场景/道具都有 design-source 层 |
| 道具链停在 `prop_design_bridge.json`，没有 design synthesis 真源 | 叶子治理层 | 补齐 `4-道具/2-设计` 父 skill、shared I/O、team 与 prompt sidecar | 把道具链固定为 `清单 -> bridge -> design master -> prompt sidecar` | 下游不再临时拼 prompt |
| 场景链只有对象池、没有 design synthesis 真源 | 叶子治理层 | 补齐 `1-场景` 家族父级与 `1-场景/2-设计` | 把场景链固定为 `清单 -> 设计 -> 面板` | 场景清单不再悬空 |
| 场景链已有 design synthesis，但 `panel_handoff` 没有实际消费入口 | 下游承接层 | 补齐 `1-场景/3-面板` 叶子技能 | 在阶段父级显式登记 scene panel 为 active 入口 | 场景链真正形成 `清单 -> 设计 -> 面板` 闭环 |
| 角色链停在 `1-清单`，没有 design synthesis 真源 | 叶子治理层 | 补齐 `2-角色/2-设计` 父 skill、shared I/O、team 与角色设计 carrier | 把角色链固定为 `清单 -> 设计 -> 面板/生图` | 角色设计不再依赖临时拼接 |
| 服装链只有空目录，没有独立 design-source / design / panel 真源 | 类目治理层 | 建立 `3-服装` 父级与 `1-清单 / 2-设计 / 3-面板` 三段 active 入口 | 把服装链固定为 `角色清单 -> 服装清单 -> 设计 -> 面板` | 服装链不再挤在角色设计的局部字段里 |
| 输出路径继续漂到旧仓或 `主体/` 旧口径 | 路径真源层 | 当前先统一落到 `projects/<项目名>/4-Design/` | 在阶段父级合同中固定当前 buildout 目标路径 | 产物路径可预测 |
| 父级路由状态陈旧，仍把已落地子路径写成 pending | 路由状态层 | 同步更新 `4-Design/SKILL.md` 的 active/pending 列表 | 每新增一个 active 子路径，就同步更新阶段父级状态与路由图 | 父级合同与真实可执行入口一致 |
| 新增 panel leaf 后父级仍缺少 panel route 说明 | 阶段路由层 | 在 `Execution Summary` 中补写 panel packet 入口与回接口径 | 对每个新增 panel leaf 同步更新阶段父级摘要与 case log | 用户能从父级直接进入正确 panel 入口 |
| 道具链只有 design master，没有 panel dossier handoff | 叶子治理层 | 建立 `4-道具/3-面板` 叶子技能并回接阶段父级路由 | 让 `4-Design` 的 prop 家族形成 `清单 -> 设计 -> 面板` 真正闭环 | `4-Design/SKILL.md` 能正确路由到 prop panel |

## Repair Playbook

1. 先查上游 `3-Detail/第N集.json` 是否存在且符合 shared schema。
2. 再查当前任务属于角色、场景、服装还是道具。
3. 若只需要建立对象池，优先进入对应 `1-清单`。
4. 若叶子合同未补齐，停止在父级并报告缺口。

## Reusable Heuristics

- `4-Design` 的首要价值不是立即出设计图，而是把导演事实收敛成可复用的 design-source 对象池。
- 阶段父级一旦从空骨架升级为可用入口，就应显式列出当前 active 子路径，避免用户被过时状态误导到 pending 分支。
- 当类目父级已经存在且叶子技能已落地时，阶段父级应路由到“类目父级 -> active 叶子”，而不是继续把该类目写成空目录。
- 对道具链来说，`bridge` 不是最终交付；最稳的落点是把稳定设计事实写进 canonical JSON，把 prompt 下放 sidecar。
- 对场景链来说，`1-清单` 和 `2-设计` 必须一起出现才算闭环；只有对象池没有设计接手合同，仍不算可执行。
- 对场景链来说，`2-设计` 出现后如果 `panel_handoff` 已稳定，就应继续补齐 `3-面板`；否则会在 design 阶段留下悬空的下游合同。
- 对服装链来说，最稳的 canonical source 不是再扫一遍导演 JSON，而是消费 `2-角色/1-清单/角色清单.json` 里已经锁定的穿搭事实，再独立沉淀服装真源。
