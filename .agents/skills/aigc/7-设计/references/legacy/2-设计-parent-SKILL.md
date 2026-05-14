---
name: aigc-design-object-design
description: Use when `7-设计/2-设计` needs to consume `1-清单` design-source JSON plus `0-Init` and `2-Global` truths, then route the current design work under `projects/aigc/<项目名>/7-设计/` for downstream `3-面板`.
governance_tier: full
---

# aigc 7-设计 / 2-设计

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`2-设计` 是 `7-设计` 阶段承接 `1-清单`、连接 `3-面板` 的 tranche parent。

当前 source-layer 已落地的子技能为：

1. `场景`
2. `角色`
3. `道具`

保留中的 sibling 目录：

- `服装`

`服装` 当前只保留路径位，不宣称本轮可执行。

父层拥有：

- `2-设计` 入口判定与 selective dispatch
- `1-清单/*.json + 0-Init + 2-Global` 的共享输入口径裁决
- `3-面板` handoff 的设计真源约束
- `projects/aigc/<项目名>/7-设计/validation-report.md` 的阶段级验收摘要

父层不拥有：

- 重写 `1-清单` canonical JSON
- 替 leaf 生成跨类目总稿
- 把 `_manifest.json` 或 thinking sidecar 升格成业务真源

## Stage Coverage Status

| unit | status | first_input_root | default_output_root |
| --- | --- | --- | --- |
| `场景` | active | `7-设计/场景/1-清单/第N集/*.json` | `7-设计/场景/2-设计/第N集/` |
| `角色` | active | `7-设计/角色/1-清单/第N集/*.json` | `7-设计/角色/2-设计/第N集/` |
| `服装` | pending-migration | 暂无 active 服装清单 leaf | 暂不声明 active runtime；不得在初始化时预建 `7-设计/服装/*` |
| `道具` | active | `7-设计/道具/1-清单/第N集/*.json` | `7-设计/道具/2-设计/第N集/` |

## Shared Canonical Sources (Mandatory)

- `.agents/skills/aigc/7-设计/SKILL.md`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/7-设计/1-清单/SKILL.md`
- `.agents/skills/aigc/7-设计/2-设计/_shared/design-input-contract.md`
- `.agents/skills/aigc/7-设计/2-设计/_shared/design-output-contract.md`
- `.agents/skills/aigc/7-设计/2-设计/_shared/design-slot-review-contract.md`
- `.agents/skills/aigc/7-设计/2-设计/_shared/subagent-supervision-contract.md`
- `.agents/skills/aigc/_shared/image-generation-execution-contract.md`
- `场景/SKILL.md`
- `角色/SKILL.md`
- `道具/SKILL.md`

硬规则：

1. `2-设计` 只消费 `1-清单` 已稳定落盘的 design-source JSON。
2. `0-Init` 与 `2-Global` 只作为风格/题材/故事边界层，不作为对象识别层。
3. `3-面板` 的默认上游是 `2-设计` 的结构化设计真源，而不是 `1-清单` 直接越级输入。
4. 每个主体 prompt 必须自动加载 `_shared/design-output-contract.md` 规定的统一全局风格前缀，并让 `Integrated prompt` 保持完全英文、约 2000 UTF-8 bytes 的整合 brief。
5. 每个主体自动图必须遵守参照图防污染模式：场景为空镜头、角色为纯色背景、道具为纯道具图。
6. 设计文件生成后必须继续进入内置 `$imagegen` / `image_gen` 单主体快路径；默认模型口径为 `GPT-IMAGE-2`，由 `_shared/image-generation-execution-contract.md` 规定 request sidecar、项目复制与状态记录，图片与设计文件同目录同 stem。不得默认调用 `.agents/skills/api/anyfast/image/nano-banana/general` 或任何需要 API key 的 provider。
7. 父层只路由真实存在的 leaf，不为未迁回 sibling 伪造 active 状态。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/7-设计/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/7-设计/1-清单/SKILL.md + CONTEXT.md`
5. 本 `SKILL.md + CONTEXT.md`
6. `.agents/skills/aigc/7-设计/2-设计/_shared/design-input-contract.md`
7. `.agents/skills/aigc/7-设计/2-设计/_shared/design-output-contract.md`
8. `.agents/skills/aigc/7-设计/2-设计/_shared/design-slot-review-contract.md`
9. `.agents/skills/aigc/_shared/image-generation-execution-contract.md`
10. `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
11. `.agents/skills/aigc/7-设计/2-设计/_shared/subagent-supervision-contract.md`
12. 命中 `场景` 时，加载 `场景/SKILL.md + CONTEXT.md`
13. 命中 `角色` 时，加载 `角色/SKILL.md + CONTEXT.md`
14. 命中 `道具` 时，加载 `道具/SKILL.md + CONTEXT.md`
15. `projects/aigc/<项目名>/0-Init/{north_star,init_handoff,story-source-manifest}.yaml`
16. `projects/aigc/<项目名>/2-Global/全局风格.md`
17. `projects/aigc/<项目名>/2-Global/全集类型元素.md`
18. `projects/aigc/<项目名>/2-Global/导演意图.md`
19. `projects/aigc/<项目名>/team.yaml`（若存在）

## Total Input Contract (Mandatory)

### 必需输入

- 命中 `场景`：`projects/aigc/<项目名>/7-设计/场景/1-清单/第N集/场景清单.json`
- 命中 `角色`：`projects/aigc/<项目名>/7-设计/角色/1-清单/第N集/角色清单.json`
- 命中 `道具`：`projects/aigc/<项目名>/7-设计/道具/1-清单/第N集/道具清单.json`

### 强烈建议输入

- `projects/aigc/<项目名>/7-设计/角色/1-清单/第N集/role_design_bridge.json`
- `projects/aigc/<项目名>/7-设计/角色/1-清单/第N集/角色研究.json`
- `projects/aigc/<项目名>/7-设计/场景/1-清单/第N集/场景研究.json`
- `projects/aigc/<项目名>/7-设计/场景/1-清单/第N集/scene_design_bridge.json`
- `projects/aigc/<项目名>/7-设计/道具/1-清单/第N集/道具研究.json`
- `projects/aigc/<项目名>/7-设计/道具/1-清单/第N集/prop_design_bridge.json`
- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
- `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`
- `projects/aigc/<项目名>/2-Global/全局风格.md`
- `projects/aigc/<项目名>/2-Global/全集类型元素.md`
- `projects/aigc/<项目名>/2-Global/导演意图.md`

### 可选输入

- `projects/aigc/<项目名>/2-Global/分组类型元素.md`
- 用户显式指定的 `selected_scenes[] / selected_roles[] / selected_props[]`

## Canonical Output Governance (Mandatory)

| domain | canonical_design_truth | derived_projection | auto_image_asset | audit_sidecar |
| --- | --- | --- | --- | --- |
| `场景` | `scene_design.json` | `[场景名].md` | `[场景名].<ext>` | `_manifest.json` |
| `角色` | `character_design.json` | `[角色名].md` | `[角色名].<ext>` | `_manifest.json` |
| `服装` | pending-migration | pending-migration | pending-migration | pending-migration |
| `道具` | `[prop_id]-[canonical_name].md` | `道具设计.json`、`prop_design_prompt.json`（显式兼容导出） | `[prop_id]-[canonical_name].<ext>` | `_manifest.json` |

父层补充规则：

1. `scene_design.json` 与 `character_design.json` 是对应 leaf 的 machine-first canonical truth。
2. 道具 leaf 当前以逐道具 Markdown 为 canonical truth，兼容 JSON 不得反向抢权。
3. `[场景名].md` / `[角色名].md` 是从结构化字段导出的 human projection，不得漂成第二真源。
4. `_manifest.json` 只承担审计与覆盖率侧车职责。
5. `auto_image_asset` 是由 `full_generation_prompt` 派生的单主体概念图，不得反向抢占设计真源。
6. 父层阶段摘要只写到 `projects/aigc/<项目名>/7-设计/validation-report.md`。
7. 首次落盘后的收尾 refine 不再属于 `监制`；若需要后置审计，只能进入阶段 audit/validation 机制，不得生成第二份设计真源或平行 reviewer 总稿。

## Field Master

| field_id | output_position | requirement | owner_step | quality_dimension | fail_code |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DESIGN-02-01` | tranche boundary | 明确父层只负责路由、输入裁决与 handoff | `S1` | boundary clarity | `FAIL-DESIGN-02-01` |
| `FIELD-DESIGN-02-02` | dispatch decision | 明确命中 leaf、selected objects 与 selective dispatch | `S2` | routing stability | `FAIL-DESIGN-02-02` |
| `FIELD-DESIGN-02-03` | shared inputs | 固定 `1-清单 + 0-Init + 2-Global` 三层输入口径 | `S3` | truth alignment | `FAIL-DESIGN-02-03` |
| `FIELD-DESIGN-02-04` | output governance | 锁各 active leaf 的 canonical truth / projection / `_manifest.json` 边界，并把当前轮目标解析到 slot bundle | `S4` | canonical governance | `FAIL-DESIGN-02-04` |
| `FIELD-DESIGN-02-05` | handoff | 明确 `3-面板` 默认消费 `full_generation_prompt` 与同 stem 单主体图片作为批量 SMART 参照 | `S5` | closure completeness | `FAIL-DESIGN-02-05` |
| `FIELD-DESIGN-02-06` | `full_generation_prompt + auto_image_asset` | 完整 prompt 必须含全局风格前缀；图片请求必须通过共享 guard 以内置 imagegen 模式提交，并能在完成后确认为每个 Markdown 同目录同名落盘 | `S5` | image fast-path completeness | `FAIL-DESIGN-02-06` |
| `FIELD-DESIGN-02-07` | reference cleanliness policy | 父层必须把场景空镜、角色纯色背景、道具纯物图作为 leaf prompt 与自动生图前置门禁 | `S5` | reference cleanliness | `FAIL-DESIGN-02-07` |
| `FIELD-DESIGN-02-08` | post-write audit boundary | 输出后必须明确：`team.yaml.roles.supervision` 不再承担 closeout；当前轮只写阶段 audit note 与 handoff，不触发 `监制` 收尾 | `S6` | audit boundary | `FAIL-DESIGN-02-08` |

## Thought Pass Map

| step_id | focus | actions | evidence | route_out | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `S1` | 锁 tranche 边界 | 明确父层拥有项与不拥有项 | `boundary_note` | `S2` | `S1` |
| `S2` | 裁决命中 leaf | 锁 `场景 / 角色 / 道具` active leaf 与 selected objects | `dispatch_note` | `S3` | `S2` |
| `S3` | 锁共享输入 | 回链 `1-清单 + 0-Init + 2-Global` 三层输入 | `input_lock_note` | `S4` | `S3` |
| `S4` | 锁输出边界 | 固定 canonical truth、derived projection 与 slot bundle 边界 | `output_governance_note + slot_bundle_note` | `S5` | `S4` |
| `S5` | 写 handoff、参照洁净门禁与图片快路径 | 声明 `3-面板` 默认读取 `full_generation_prompt` 与同 stem 图片；按共享输出合同锁定 `场景=empty environmental shot`、`角色=solid color background`、`道具=isolated pure prop view` 后，再触发 `ensure_design_auto_images.py` 写批量 request sidecar，并由当前 Codex 会话逐张调用内置 `image_gen` 生成单主体自动图 | `handoff_note + reference_cleanliness_note + auto_image_note` | `S6` | `S5` |
| `S6` | 写输出后审计边界说明 | 读取 `team.yaml` 与共享占位合同，明确 `roles.supervision` 只作前置 advisory；当前轮如需后置收尾，只在 `validation-report.md` 留 audit note 与下一入口，不触发 reviewer subagents | `post_write_audit_note` | `done` | `S6` |

## Pass Table

| field_id | pass_condition | fail_code | rework_entry |
| --- | --- | --- | --- |
| `FIELD-DESIGN-02-01` | 父层不越权生成业务主稿 | `FAIL-DESIGN-02-01` | `S1` |
| `FIELD-DESIGN-02-02` | 命中 leaf 与 selective dispatch 明确 | `FAIL-DESIGN-02-02` | `S2` |
| `FIELD-DESIGN-02-03` | 三层输入真源优先级清晰 | `FAIL-DESIGN-02-03` | `S3` |
| `FIELD-DESIGN-02-04` | 结构化真源与人读投影边界稳定 | `FAIL-DESIGN-02-04` | `S4` |
| `FIELD-DESIGN-02-05` | `3-面板` handoff 明确 | `FAIL-DESIGN-02-05` | `S5` |
| `FIELD-DESIGN-02-06` | `_manifest.json.auto_image.execution_mode=codex-builtin-imagegen` 且 `provider_skill=imagegen`、`default_model=GPT-IMAGE-2`、`request_batch_path` 可追踪；最终验收时每个主体文件都有含全局风格前缀的完整 prompt 与同目录同名图片 | `FAIL-DESIGN-02-06` | `S5` |
| `FIELD-DESIGN-02-07` | 每个 leaf 的 `Integrated prompt` 都含对应洁净锚句，且自动生图前不得出现该域禁止的污染主体 | `FAIL-DESIGN-02-07` | `S5` |
| `FIELD-DESIGN-02-08` | `team.yaml` 已读取，且已明确 `roles.supervision` 不再承担当前轮 closeout；输出后只写审计边界说明与 handoff | `FAIL-DESIGN-02-08` | `S6` |

## Root-Cause Execution Contract (Mandatory)

当 `2-设计` 出现以下问题时，必须先修源层而不是补某个单角色产物：

- `1-清单` JSON 明明存在，但 `2-设计` 继续回读旧上游长文
- `0-Init` 与 `2-Global` 信号被混成一锅，无法分清谁负责题材、谁负责风格
- `[场景名].md` 与 `scene_design.json` 互相漂移
- `[角色名].md` 与 `character_design.json` 互相漂移
- 道具兼容 JSON 反向抢走逐道具 Markdown 主权
- 设计文件已生成但没有继续触发内置 imagegen 单主体生图
- 设计自动生图仍默认调用 API / nano-banana / anyfast，或把 request sidecar 状态伪装成已产图成功
- 生图 prompt 只传了局部主体描述，缺统一全局风格前缀
- 场景/角色/道具参照图 prompt 混入其他主体，导致下游 panel 或 image 阶段引用污染
- `3-面板` 仍需重新猜对象主键或风格骨架
- 当前轮输出已落盘后，仍继续触发 `监制` closeout
- 把 `7-设计` 的 post-write 收尾继续挂在 `roles.supervision` 或 `roles.review` 名下，导致审计层与顾问层混线
- 把 `roles.supervision.source_skill_refs` 误当落盘后收尾授权字段

固定链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

## 输出后审计占位（Mandatory）

1. 当前轮输出已稳定后，不再进入 `Subagents 监制强化`。
2. 读取 `projects/aigc/<项目名>/team.yaml` 与 `_shared/subagent-supervision-contract.md` 的目的，仅是确认 `roles.supervision` 在本轮 closeout 中已停用。
3. `source_skill_refs` 只证明 provenance / 领域提示，不得充当 runtime 授权字段。
4. 当前轮若需要定位问题，仍可按 `_shared/design-slot-review-contract.md` 把目标解析到 slot bundle，但这只服务审计记录，不再触发 `监制` patch。

## Completion Criteria

1. 已建立 `2-设计` tranche parent。
2. 已锁 `1-清单 + 0-Init + 2-Global` 为唯一上游口径。
3. 已把 `场景 / 角色 / 道具` active leaf 接回父层总线。
4. 已给出 `3-面板` 的默认消费口径。
5. 已按 `_shared/design-output-contract.md` 为每个主体输出 `full_generation_prompt`，其中场景/角色/道具分别满足空镜、纯色背景、纯道具参照洁净门禁。
6. 已自动生成同目录同名图片，且图片 prompt 通过参照洁净复核。
7. 若图片仍处于内置 imagegen 待执行状态，已写出 request sidecar 与 `request_ready` 状态；不得把该状态冒充为最终图片成功。
8. 已按 `_shared/design-slot-review-contract.md` 把当前轮目标收束为 slot bundle，并据此写出审计边界说明。
9. 已明确当前轮首次落盘后的收尾不再由 `监制` 执行。
