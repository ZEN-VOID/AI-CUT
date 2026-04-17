---
name: aigc-design-object-design
description: Use when `4-Design/2-设计` needs to consume `1-清单` design-source JSON plus `0-Init` and `2-Global` truths, then route the current design work under `projects/aigc/<项目名>/4-Design/` for downstream `3-面板`.
governance_tier: full
---

# aigc 4-Design / 2-设计

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`2-设计` 是 `4-Design` 阶段承接 `1-清单`、连接 `3-面板` 的 tranche parent。

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
- `projects/aigc/<项目名>/4-Design/validation-report.md` 的阶段级验收摘要

父层不拥有：

- 重写 `1-清单` canonical JSON
- 替 leaf 生成跨类目总稿
- 把 `_manifest.json` 或 thinking sidecar 升格成业务真源

## Stage Coverage Status

| unit | status | first_input_root | default_output_root |
| --- | --- | --- | --- |
| `场景` | active | `4-Design/场景/1-清单/第N集/*.json` | `4-Design/场景/2-设计/第N集/` |
| `角色` | active | `4-Design/角色/1-清单/第N集/*.json` | `4-Design/角色/2-设计/第N集/` |
| `服装` | pending-migration | 暂无 active 服装清单 leaf | 暂不声明 active runtime；不得在初始化时预建 `4-Design/服装/*` |
| `道具` | active | `4-Design/道具/1-清单/第N集/*.json` | `4-Design/道具/2-设计/第N集/` |

## Shared Canonical Sources (Mandatory)

- `.agents/skills/aigc/4-Design/SKILL.md`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/4-Design/1-清单/SKILL.md`
- `.agents/skills/aigc/4-Design/2-设计/_shared/design-input-contract.md`
- `.agents/skills/aigc/4-Design/2-设计/_shared/design-output-contract.md`
- `.agents/skills/aigc/4-Design/2-设计/_shared/design-slot-review-contract.md`
- `.agents/skills/aigc/4-Design/2-设计/_shared/subagent-supervision-contract.md`
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
6. 设计文件生成后必须继续调用 `.agents/skills/api/image/nano-banana/general` 的单主体快路径；默认通过 `_shared/image-generation-execution-contract.md` 规定的后台批量并发模式提交，图片与设计文件同目录同 stem。
7. 父层只路由真实存在的 leaf，不为未迁回 sibling 伪造 active 状态。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/4-Design/1-清单/SKILL.md + CONTEXT.md`
5. 本 `SKILL.md + CONTEXT.md`
6. `.agents/skills/aigc/4-Design/2-设计/_shared/design-input-contract.md`
7. `.agents/skills/aigc/4-Design/2-设计/_shared/design-output-contract.md`
8. `.agents/skills/aigc/4-Design/2-设计/_shared/design-slot-review-contract.md`
9. `.agents/skills/aigc/_shared/image-generation-execution-contract.md`
10. `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
11. `.agents/skills/aigc/4-Design/2-设计/_shared/subagent-supervision-contract.md`
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

- 命中 `场景`：`projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/场景清单.json`
- 命中 `角色`：`projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json`
- 命中 `道具`：`projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/道具清单.json`

### 强烈建议输入

- `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/role_design_bridge.json`
- `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色研究.json`
- `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/场景研究.json`
- `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/scene_design_bridge.json`
- `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/道具研究.json`
- `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/prop_design_bridge.json`
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
6. 父层阶段摘要只写到 `projects/aigc/<项目名>/4-Design/validation-report.md`。
7. 监制强化只允许 patch 当前轮输出，不得生成第二份设计真源或平行 reviewer 总稿。

## Field Master

| field_id | output_position | requirement | owner_step | quality_dimension | fail_code |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DESIGN-02-01` | tranche boundary | 明确父层只负责路由、输入裁决与 handoff | `S1` | boundary clarity | `FAIL-DESIGN-02-01` |
| `FIELD-DESIGN-02-02` | dispatch decision | 明确命中 leaf、selected objects 与 selective dispatch | `S2` | routing stability | `FAIL-DESIGN-02-02` |
| `FIELD-DESIGN-02-03` | shared inputs | 固定 `1-清单 + 0-Init + 2-Global` 三层输入口径 | `S3` | truth alignment | `FAIL-DESIGN-02-03` |
| `FIELD-DESIGN-02-04` | output governance | 锁各 active leaf 的 canonical truth / projection / `_manifest.json` 边界，并把当前轮目标解析到 slot bundle | `S4` | canonical governance | `FAIL-DESIGN-02-04` |
| `FIELD-DESIGN-02-05` | handoff | 明确 `3-面板` 默认消费 `full_generation_prompt` 与同 stem 单主体图片作为批量 SMART 参照 | `S5` | closure completeness | `FAIL-DESIGN-02-05` |
| `FIELD-DESIGN-02-06` | `full_generation_prompt + auto_image_asset` | 完整 prompt 必须含全局风格前缀；图片请求必须通过共享 guard 以后台批量并发模式提交，并能在完成后确认为每个 Markdown 同目录同名落盘 | `S5` | image fast-path completeness | `FAIL-DESIGN-02-06` |
| `FIELD-DESIGN-02-07` | reference cleanliness policy | 父层必须把场景空镜、角色纯色背景、道具纯物图作为 leaf prompt 与自动生图前置门禁 | `S5` | reference cleanliness | `FAIL-DESIGN-02-07` |
| `FIELD-DESIGN-02-08` | subagent supervision closeout | 输出后必须读取项目根 `team.yaml`，按共享合同裁定当前轮 closeout 的 refine / review-gate 关系、reviewer 顺序与设计型补选，并先把当前轮文件解析到 slot bundle，再只对当前轮业务文件做监制/设计向优化 | `S6` | council closeout | `FAIL-DESIGN-02-08` |

## Thought Pass Map

| step_id | focus | actions | evidence | route_out | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `S1` | 锁 tranche 边界 | 明确父层拥有项与不拥有项 | `boundary_note` | `S2` | `S1` |
| `S2` | 裁决命中 leaf | 锁 `场景 / 角色 / 道具` active leaf 与 selected objects | `dispatch_note` | `S3` | `S2` |
| `S3` | 锁共享输入 | 回链 `1-清单 + 0-Init + 2-Global` 三层输入 | `input_lock_note` | `S4` | `S3` |
| `S4` | 锁输出边界 | 固定 canonical truth、derived projection 与 slot bundle 边界 | `output_governance_note + slot_bundle_note` | `S5` | `S4` |
| `S5` | 写 handoff、参照洁净门禁与图片快路径 | 声明 `3-面板` 默认读取 `full_generation_prompt` 与同 stem 图片；按共享输出合同锁定 `场景=empty environmental shot`、`角色=solid color background`、`道具=isolated pure prop view` 后，再触发 `ensure_design_auto_images.py` 写批量 request sidecar 并按默认后台批量并发模式提交单主体自动图 | `handoff_note + reference_cleanliness_note + auto_image_note` | `S6` | `S5` |
| `S6` | 写 subagents 监制强化收尾 | 读取 `team.yaml`，按共享合同裁定当前轮 closeout 是否可进入、合并 `roles.supervision.members`、可选 `4-Design review gate members` 与设计型补选，并先把当前轮文件解析到 slot bundle，再真实启动 reviewer subagents 对当前轮输出做复审/优化 | `supervision_review_note + subagent_supervision_result` | `done` | `S6` |

## Pass Table

| field_id | pass_condition | fail_code | rework_entry |
| --- | --- | --- | --- |
| `FIELD-DESIGN-02-01` | 父层不越权生成业务主稿 | `FAIL-DESIGN-02-01` | `S1` |
| `FIELD-DESIGN-02-02` | 命中 leaf 与 selective dispatch 明确 | `FAIL-DESIGN-02-02` | `S2` |
| `FIELD-DESIGN-02-03` | 三层输入真源优先级清晰 | `FAIL-DESIGN-02-03` | `S3` |
| `FIELD-DESIGN-02-04` | 结构化真源与人读投影边界稳定 | `FAIL-DESIGN-02-04` | `S4` |
| `FIELD-DESIGN-02-05` | `3-面板` handoff 明确 | `FAIL-DESIGN-02-05` | `S5` |
| `FIELD-DESIGN-02-06` | `_manifest.json.auto_image.execution_mode=background-batch-concurrent` 且 `request_batch_path/background_pid/background_log` 可追踪；最终验收时每个主体文件都有含全局风格前缀的完整 prompt 与同目录同名图片 | `FAIL-DESIGN-02-06` | `S5` |
| `FIELD-DESIGN-02-07` | 每个 leaf 的 `Integrated prompt` 都含对应洁净锚句，且自动生图前不得出现该域禁止的污染主体 | `FAIL-DESIGN-02-07` | `S5` |
| `FIELD-DESIGN-02-08` | `team.yaml` 已读取，当前轮 closeout 已按共享合同完成 refine / gate 分层裁定，`source_skill_refs` 未被当授权字段，reviewer 解析遵循共享合同，且 `use_subagents_by_default=true` 时真实起 reviewer subagents | `FAIL-DESIGN-02-08` | `S6` |

## Root-Cause Execution Contract (Mandatory)

当 `2-设计` 出现以下问题时，必须先修源层而不是补某个单角色产物：

- `1-清单` JSON 明明存在，但 `2-设计` 继续回读旧上游长文
- `0-Init` 与 `2-Global` 信号被混成一锅，无法分清谁负责题材、谁负责风格
- `[场景名].md` 与 `scene_design.json` 互相漂移
- `[角色名].md` 与 `character_design.json` 互相漂移
- 道具兼容 JSON 反向抢走逐道具 Markdown 主权
- 设计文件已生成但没有继续触发 nano-banana general 单主体生图
- 设计自动生图仍以前台逐个串行方式阻塞批量 pipeline，或后台提交后把状态伪装成已产图成功
- 生图 prompt 只传了局部主体描述，缺统一全局风格前缀
- 场景/角色/道具参照图 prompt 混入其他主体，导致下游 panel 或 image 阶段引用污染
- `3-面板` 仍需重新猜对象主键或风格骨架
- 当前轮监制强化仍停留在文件级，无法说明具体哪个 slot bundle 失真
- 当前轮输出已落盘，但没有读取项目根 `team.yaml` 做监制强化收尾
- 把 `4-Design` 的 stage-end refine 与 final-stage review gate 混成同一条权限线
- 把 `roles.supervision.source_skill_refs` 误当 reviewer skill，导致 council 命中阶段技能而不是 `.agents/skills/team/` reviewer
- `runtime_policy.use_subagents_by_default == true` 时，仍把本地顺序模拟伪装成正常 council

固定链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

## Subagents 监制强化收尾（Mandatory）

1. 当前轮输出已稳定后，必须读取 `projects/aigc/<项目名>/team.yaml` 与 `_shared/subagent-supervision-contract.md`。
2. 当前轮 closeout 的进入裁决、reviewer precedence、manual override 与结构化 summary 全部以 `_shared/subagent-supervision-contract.md` 为准。
3. `4-Design` 的 stage-end refine 与 final-stage review gate 必须分层理解：前者负责当前轮 `2-设计` 输出收口，后者若在 `team.yaml` 中显式覆盖 `4-Design`，只并入 reviewer 池，不取代本地 closeout。
4. `source_skill_refs` 只证明 provenance / 领域提示，不得充当 runtime 授权字段。
5. 当前轮 review target 必须按 `_shared/design-slot-review-contract.md` 先解析到 slot bundle，再进入 reviewer council；不得停留在“只看文件名”的粗粒度模式。
6. 若显式 reviewer 不足，本阶段按设计型目标补选 reviewer：
   - 父层 / shared：`张叔平 -> 叶锦添`
   - `场景`：`隈研吾 -> 叶锦添`
   - `角色`：`张叔平 -> 叶锦添`
   - `道具`：`张叔平 -> 叶锦添`
7. `runtime_policy.use_subagents_by_default == true` 且环境支持时，必须真实启动 reviewer subagents；不得用本地模拟冒充。
8. 监制强化只允许 patch 当前轮命中的 canonical 输出、projection、`_manifest.json` 与按需阶段 `validation-report.md`，不得新造 reviewer 总稿或第二业务真源。

## Completion Criteria

1. 已建立 `2-设计` tranche parent。
2. 已锁 `1-清单 + 0-Init + 2-Global` 为唯一上游口径。
3. 已把 `场景 / 角色 / 道具` active leaf 接回父层总线。
4. 已给出 `3-面板` 的默认消费口径。
5. 已按 `_shared/design-output-contract.md` 为每个主体输出 `full_generation_prompt`，其中场景/角色/道具分别满足空镜、纯色背景、纯道具参照洁净门禁。
6. 已自动生成同目录同名图片，且图片 prompt 通过参照洁净复核。
7. 若 provider 处于后台执行中，已写出 request sidecar、`background_pid/background_log` 与 `background_submitted` 状态；不得把该状态冒充为最终图片成功。
8. 已按 `_shared/design-slot-review-contract.md` 把当前轮目标收束为 slot bundle，并据此进入 reviewer council。
9. 已按 `team.yaml + _shared/subagent-supervision-contract.md` 完成当前轮 `subagents` 监制强化，并把有效建议回写到当前轮目标文件。
