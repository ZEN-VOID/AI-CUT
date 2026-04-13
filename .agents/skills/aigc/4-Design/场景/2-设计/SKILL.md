---
name: aigc-design-scene-design
description: Use when the `4-Design/场景/2-设计` stage needs to turn scene catalog, global style, and director evidence into canonical scene design cards and an episode-level scene design carrier in the current project runtime.
governance_tier: full
---

# 4-Design / 1-场景 / 2-设计

## Mode Selection

- 本次重构采用 `$skill-知行合一` 的单技能真源口径，并显式退役原 `.codex/agents/aigc/设计组/场景设计` 外挂 agent 组。
- `复杂链路的骨架 / 细则分层`：`false`
- canonical source：仅本 `SKILL.md`
- 角色能力不再外放为 subagents，而是内收为本技能的六组能力镜面。
- `templates/scene-design-card.md` 保留为输出结构载体，不再承担第二规则真源。

## 概述

`2-设计` 负责把 `1-清单` 已锁定的场景对象池，继续收束为当前集的场景设计卡与 episode 级 `场景设计.json`。

交付类型：`内容输出型`

## When To Use

- 已有 `1-清单` 的 scene catalog，需要进一步产出场景设计稿。
- 需要把 `2-Global` 的全局风格、类型元素与导演意图压回具体空间设计字段。
- 需要形成可被 `3-面板 / 5-Image / 6-Video` 继续消费的 `scene_designs[]` 与 per-scene 卡片。

## When Not To Use

- 还没有 `1-清单` 的 scene catalog，应先回退到 `1-清单`。
- 当前诉求是图片生成、视频请求或镜头 prompt，不在本阶段执行。
- 任务只是补导演事实，不应在本技能改写 `3-Detail` 真源。

## 单一真源边界

### `2-设计` 拥有

- `scene catalog -> scene design` 的唯一收束合同。
- 场景设计六组能力镜面的调度、汇流、复核与审计。
- `projects/<项目名>/4-Design/场景/2-设计/第N集/` 下 canonical 设计产物写回。

### `2-设计` 不拥有

- 重写 `1-清单` 的场景对象池定义。
- 越权修改 `2-Global` 或 `3-Detail` 真源。
- 让任何中间能力面直接写最终文件。

## Internal Capability Recomposition

以下能力已从外部 agent 合同收编回本技能内部，不再作为独立 agent 真源存在：

| 能力镜面 | 责任 | 典型输出位 |
| --- | --- | --- |
| `统筹判题镜` | 锁定本轮命中场景、优先级、证据缺口 | `scene_dispatch_plan` |
| `空间逻辑镜` | 锁定功能区、分区、动线、视线、水风路径与观看关系 | `space_layout / function_attribute / circulation_plan / photo_shot_size / camera_angle` |
| `建筑语言镜` | 锁定作品/现实参照锚点、时代结构、材料、时期地域与文化约束 | `design_master / period_region / material_detail / structural_detail / symbolic_design` |
| `布景氛围镜` | 锁定陈设层次、人文痕迹、室内/景观差异化细节、灯光氛围与摄影设计 | `lighting_design / furniture_design / ecology_design / atmosphere / composition_layout` |
| `审景复核镜` | 检查设计一致性、反漂移和下游可消费性 | `review_status / review_note` |
| `真源审计镜` | 检查路径、schema、trace、writeback 边界 | `audit_trace / acceptance_notes` |

## Business Requirement Analysis Contract

### 业务目标

- 把场景对象池继续压成可复用、可审阅、可下游消费的场景设计真源。

### 业务对象

- `1-清单` 的 `第N集.json`
- `2-Global` 的风格、类型与导演意图
- `3-Detail` 的镜头级证据
- `0-Init` 的 north star 与初始化预设

### 复杂度来源

- 同一场景需要同时满足剧情用途、空间逻辑、时代风格、陈设氛围和镜头阅读。
- 场景设计必须是单一真源，不能再由多个角色各写平行主稿。
- 下游需要的是结构化 handoff，而不是抒情长文。

### 非目标

- 不重新建立场景对象池。
- 不直接生成图像或视频请求。
- 不输出平行版本的场景主稿。

### 成功标准

- 每个命中场景都有稳定的 `scene design card` 与 `scene_designs[]` 条目。
- 设计卡既能解释空间怎么搭，也能被下游直接转成展示、画面或视频输入。
- 最终只由本技能写出 `场景设计.json` 与 `<scene_key>.md`。

## Total Input Contract

### Canonical Inputs

- `projects/<项目名>/4-Design/场景/1-清单/第N集/第N集.json`
- `projects/<项目名>/2-Global/全局风格.md`
- `projects/<项目名>/2-Global/类型元素.md`
- `projects/<项目名>/2-Global/导演意图.md`
- `projects/<项目名>/3-Detail/第N集.json`
- `projects/<项目名>/0-Init/north_star.yaml`
- `projects/<项目名>/0-Init/init_handoff.yaml`
- `templates/scene-design-card.md`

### 输入顺序硬规则

1. 先读 `1-清单`，锁定对象池。
2. 再读 `2-Global`，锁定风格和类型约束。
3. 再回看 `3-Detail`，补镜头用途和动作证据。
4. 最后读 `0-Init`，只作为初始方向和约束补充。

### 输出落点

- `projects/<项目名>/4-Design/场景/2-设计/第N集/场景设计.json`
- `projects/<项目名>/4-Design/场景/2-设计/第N集/<scene_key>.md`
- 可选 `projects/<项目名>/4-Design/场景/2-设计/第N集/_manifest.json`

## Mermaid Visual Contract

- Mermaid 是本技能的关键治理真源，而不是装饰图。
- 当前至少保留 3 张图，分别承担：
  - 主工作流
  - 能力镜面与汇流关系
  - 状态推进与返工闭环
- 图里的节点名必须与下文 `D0-D8` 的思行节点保持一致。
- 若图与 prose 冲突，以更严格的节点、字段和 gate 说明为准，并立即修正图。

## Visual Maps (Mermaid)

```mermaid
flowchart TD
    A["D0 锁定目标与输入顺序"] --> B["D1 选择命中场景"]
    B --> C["D2 组装证据包"]
    C --> D["D3 空间逻辑镜"]
    D --> E["D4 建筑语言镜"]
    E --> F["D5 布景氛围镜"]
    F --> G["D6 汇流成 scene design candidate"]
    G --> H["D7 审景复核镜"]
    H --> I["D8 真源审计镜 + 写回"]
```

```mermaid
flowchart LR
    A["scene catalog"] --> D["统筹判题镜"]
    B["2-Global"] --> D
    C["3-Detail / Init"] --> D
    D --> E["空间逻辑镜"]
    E --> F["建筑语言镜"]
    F --> G["布景氛围镜"]
    G --> H["candidate"]
    H --> I["审景复核镜"]
    I --> J["真源审计镜"]
    J --> K["场景设计.json + <scene_key>.md"]
```

```mermaid
stateDiagram-v2
    [*] --> CatalogLocked
    CatalogLocked --> Dispatched
    Dispatched --> Spatialized
    Spatialized --> Structured
    Structured --> Dressed
    Dressed --> Converged
    Converged --> Reviewed
    Reviewed --> Audited
    Audited --> Written
    Reviewed --> Rework
    Audited --> Rework
    Rework --> Dispatched
```

## Thinking-Action Node Contract

### D0. 锁定目标与输入顺序

- `objective`
  - 确认本轮只做场景设计，不重建对象池，也不越权做下游生成。
- `inputs`
  - 用户目标、`1-场景` 父级合同、本技能 `CONTEXT.md`。
- `from_angles`
  - 本轮是否已有 `scene catalog`。
  - 最终只写哪些文件。
  - 哪些输入是首选真源，哪些只是补证据。
- `actions`
  1. 锁定本轮 canonical 输出为 `场景设计.json + <scene_key>.md`。
  2. 确认 `1-清单` 是第一真源，不允许跳过。
  3. 明确 `_manifest.json` 仅在追溯或批量调试时输出。
- `evidence`
  - 任务边界与输出模式判定。
- `route_out`
  - 成功：进入 `D1`。
  - 失败：停止并上抛边界冲突。
- `gate`
  - 若输入真源顺序不清，不得进入设计节点。

### D1. 选择命中场景

- `objective`
  - 用 `统筹判题镜` 锁定本轮实际需要设计的场景集合与优先级。
- `inputs`
  - `scene catalog`
  - 用户约束
  - 时间窗口
- `from_angles`
  - 哪些场景必须本轮完成。
  - 哪些场景证据不足，应保守延后。
  - 本轮是逐场覆盖还是只覆盖命中子集，是否已显式声明。
  - scene dispatch 顺序是否合理。
- `actions`
  1. 读取 `scene catalog` 的 `scenes[] / group_scene_map[] / summary`。
  2. 生成 `scene_dispatch_plan`，列出命中场景、优先级、证据缺口。
  3. 标记本轮覆盖模式：`full-episode` 或 `targeted-subset`。
  4. 排除未命中场景，避免补空设计稿。
  5. 为每个场景登记后续节点需要吸收的重点证据。
- `evidence`
  - `scene_dispatch_plan`
  - `selected_scene_keys`
- `route_out`
  - 成功：进入 `D2`。
  - scene catalog 缺失：回退 `1-清单`。
- `gate`
  - 不允许为未命中场景生成任何占位设计结果。

### D2. 组装证据包

- `objective`
  - 为每个命中场景建立同一口径的 `evidence_packet`。
- `inputs`
  - `scene_dispatch_plan`
  - `2-Global`
  - `3-Detail`
  - `0-Init`
- `from_angles`
  - 场景名、类型、时期、阶层、原型是否明确。
  - 当前原型是否被泛化成抽象类型词。
  - 全局风格真源要求该场景最终朝什么方向收敛。
  - 剧情功能是什么。
  - 风格和类型底座是什么。
  - 哪些镜头动作必须支撑空间设计。
  - 这个场景是否存在可直接借鉴的作品场景、现实场所或历史母题。
  - 若没有直接参照，允许在哪些题材边界内大胆外扩，而不是无约束发明。
  - 历史文化框架属于硬约束、软约束还是仅提供气质边界。
  - 哪些标志性元素已经被上游证据预埋，后续必须转成可见设计。
- `actions`
  1. 提取命中场景相关的 `group_scene_map` 和镜头证据。
  2. 汇总 `全局风格 / 类型元素 / 导演意图`。
  3. 为每个场景建立 `scene_profile`，至少写清 `scene_name / design_type / period_region / social_class_hint / prototype_anchor`。
  4. 判断 `prototype_anchor` 是否过泛；若只剩“宫殿 / 街道 / 森林”之类泛词，必须继续压缩到更具体的空间原型。
  5. 从 `2-Global` 中提取 `global_style_convergence`，明确该场景本轮收敛方向。
  6. 识别 `reference_anchor`，优先记录“可借鉴的作品场景 / 现实场所 / 历史母题”，并注明借鉴重点是空间、结构、气质还是叙事功能。
  7. 判定 `reference_mode`：是 `direct_reference`、`bounded_extrapolation` 还是 `culture_bounded_invention`，明确后续是贴近参照还是在边界内大胆畅想。
  8. 只补必要的 `north_star / init_handoff` 约束，不让初始化设定盖过 scene catalog。
  9. 提前记录 `iconic_elements_seed`，收束为后续必须落地的标志性元素种子。
  10. 形成每个场景的 `evidence_packet`。
- `evidence`
  - 可复用的 `evidence_packet`。
- `route_out`
  - 成功：进入 `D3`。
  - 证据严重缺失：返回 `D1` 重新缩范围。
- `gate`
  - 没有 scene-specific 证据包，或 `scene_profile` 仍未明确，不得进入具体设计。

### D3. 空间逻辑镜

- `objective`
  - 锁定场景的空间主锚点、功能分区、动线、自然流线与镜头阅读顺序。
- `inputs`
  - `evidence_packet`
- `from_angles`
  - 空间怎么搭、怎么分区。
  - 角色如何进入、停留、转向。
  - 人、风、水、视线怎么穿过空间。
  - 空间如何被感知与观看。
  - 镜头最依赖的观看关系是什么。
  - 哪些空间分区是剧情必须的。
  - 标志性元素应该落在主锚点、次锚点还是动线终点，才能被镜头读到。
- `actions`
  1. 定义 `space_type / function_attribute / space_layout`，说明场景的原型、用途和分区骨架。
  2. 梳理 `circulation_plan`，明确人物、风、水、视线与镜头的穿行路径。
  3. 提炼 `photo_shot_size / lens_type / camera_angle`，说明空间如何被观看。
  4. 标记需要后续结构或陈设落实的空间锚点。
  5. 为 `iconic_elements_seed` 预留空间落位，避免后续标志物只能漂浮成装饰词。
  6. 检查空间结构、分区与动线是否达到“可画、可拍、可生成”最低标准。
- `evidence`
  - 空间逻辑结论。
  - 镜头支撑依据。
- `route_out`
  - 成功：进入 `D4`。
  - 空间逻辑与镜头冲突：回到 `D2` 补证据。
- `gate`
  - 不允许只写氛围词而没有空间可执行结构；若原型仍泛化或不可画、不可拍、不可生成，必须返工。

### D4. 建筑语言镜

- `objective`
  - 将时代、类型和风格约束压成参照体系、结构语言、材料细节与文化边界。
- `inputs`
  - `evidence_packet`
  - `scene_profile`
  - `space_layout`
- `from_angles`
  - 这个场景最适合参照哪部作品的哪个场景，或哪类现实/历史空间母题。
  - 哪个建筑参照最服务当前原型，而不是只满足抽象美学。
  - 若要大胆畅想，应该在什么结构层做外扩，哪些部分必须继续服从题材与时代底座。
  - 参照如何转成当前项目实体，并避免滑向错误文化或错误空间原型。
  - 建筑骨架是什么。
  - 材料、配件和色彩如何服务剧情。
  - 哪些文化/时代误读必须禁止。
- `actions`
  1. 写出 `design_master / design_concept / design_style_detail`，明确参照大师、流派、理念与当前项目收敛方向。
  2. 写出 `period_region / structural_detail`，说明哪些结构逻辑必须服从历史文化框架，哪些局部允许风格化变形或大胆外扩。
  3. 写出 `material_detail / color_theme`，让材料、工艺、配件和色彩与时代、地域、阶层或世界观保持同一口径。
  4. 写出 `symbolic_design / ornament_pattern`，把文化和人文线索压成可见结构或纹样，而不是抽象说明。
  5. 写出 `cultural_constraints` 与 `reverse_taboos` 的结构部分，明确宗教、历史、民俗、礼制、地域等不可越界点。
  6. 明确 `reference_translation_rule`：参照对象如何被转写为当前项目实体，哪些部分禁止直接照搬。
- `evidence`
  - 参照锚点、结构与材料结论。
- `route_out`
  - 成功：进入 `D5`。
  - 与空间逻辑冲突：回到 `D3` 对齐。
- `gate`
  - 不允许把抽象风格词堆叠成空泛建筑描述，也不允许让参照直接滑成错误文化或错误空间原型。

### D5. 布景氛围镜

- `objective`
  - 将场景使用痕迹、人文痕迹、陈设层次、灯光氛围和摄影感落实到具体字段。
- `inputs`
  - `evidence_packet`
  - `space_layout`
  - `structural_detail`
- `from_angles`
  - 场景里具体有什么。
  - 哪些物件和痕迹支撑剧情功能。
  - 人文痕迹怎样压到空间里。
  - 材料与配件是否可信且服务剧情。
  - 灯光与气氛如何服务而不是替代设计。
  - 观众进入画面后，第一眼应该记住什么标志性元素。
  - 大胆畅想应落实成哪些具体可见物，而不是停在抽象概念层。
- `actions`
  1. 写出 `story_narrative`，以文学化正文说明此空间如何被人物经历、时间和情绪激活。
  2. 按场景类型补齐差异字段：室内优先写 `lighting_design / lamp_design / furniture_design / wall_decor / floor_material`；景观优先写 `ecology_design / water_design / art_installation`。
  3. 写出 `atmosphere / weather / season_time`，并把人文痕迹压到可见的陈设、磨损、纹样、湿度、风向或使用痕迹里。
  4. 写出 `composition_layout / composition_method / shape_sense / line_sense / tonal_sense / focus_sense / rhythm_sense / texture_sense / momentum`。
  5. 补齐 `main_light / fill_light / back_light / lighting_type / color_hue / color_value / color_saturation / color_temperature / color_psychology / camera_model / aperture / shutter / iso / focal_length / resolution`。
  6. 补齐 `design_direction` 与 `reverse_taboos` 的氛围部分，说明哪些视觉夸张是允许的，哪些会破坏历史文化或作品锚点。
  7. 为下游 prompt 汇总提炼具体短语，至少覆盖“参照锚点 + 标志性元素 + 想象增量 + 摄影观看方式”。
- `evidence`
  - 陈设与氛围结论。
- `route_out`
  - 成功：进入 `D6`。
  - 若只有抽象情绪词：返回本节点重做。
- `gate`
  - 不允许用“压抑、冷、空灵”之类空泛词替代具体设计物。

### D6. 汇流成 scene design candidate

- `objective`
  - 把前面各能力镜面的结论收束为单一场景设计候选。
- `inputs`
  - `scene_profile`
  - `space_layout`
  - `period_region`
  - `structural_detail`
  - `material_detail`
  - `circulation_plan`
  - `atmosphere`
  - `composition_layout`
- `from_angles`
  - 字段是否齐全。
  - 是否能直接写进三段式 Markdown 模板。
  - 是否已经具备下游 prompt handoff。
  - 是否同时说清“参照什么、外扩到什么程度、受什么文化边界约束、靠什么元素被记住”。
  - 是否已经把参照、美学、人文转成当前项目实体。
  - 空间结构、分区、动线是否可画、可拍、可生成。
- `actions`
  1. 生成 `scene_design_candidate`。
  2. 合成 `prompt_integration`，并同步写出 `final_scene_prompt` 作为下游兼容镜像。
  3. 写出 `panel_handoff` 与 `source_scene_ids`。
  4. 为三段式 Markdown 卡和 JSON 条目准备同一份语义主稿。
  5. 交叉检查 candidate 是否形成一条完整链：`reference_anchor -> translation_rule -> structural/cultural boundary -> iconic/human trace cluster -> downstream prompt`。
- `evidence`
  - 单一候选设计对象。
- `route_out`
  - 成功：进入 `D7`。
  - 字段缺失：返回对应能力节点。
- `gate`
  - 不允许出现多个相互竞争的 scene design candidate。

### D7. 审景复核镜

- `objective`
  - 检查候选设计是否与 scene catalog、全局约束和剧情用途一致。
- `inputs`
  - `scene_design_candidate`
  - `evidence_packet`
- `from_angles`
  - 是否反漂移。
  - 是否把局部镜头感觉误写成场景总设。
  - 是否可被下游直接消费。
- `actions`
  1. 检查字段完整性。
  2. 检查 scene catalog 回链。
  3. 检查 `prompt_integration / final_scene_prompt / panel_handoff` 是否足够具体。
  4. 检查三段式 Markdown 是否已形成 `物语 -> 解构 -> prompt整合` 闭环。
  5. 写出 `review_status` 与 `review_note`。
- `evidence`
  - review 结论。
- `route_out`
  - `pass`：进入 `D8`。
  - `rework`：回到对应节点重做。
- `gate`
  - 没有复核通过，不得进入最终写回。

### D8. 真源审计镜 + 写回

- `objective`
  - 审计路径、schema、trace，并完成唯一 canonical 写回。
- `inputs`
  - review 通过的 `scene_design_candidate`
  - 输出模板
  - 输出路径
- `from_angles`
  - 写回边界是否正确。
  - 文件结构是否完整。
  - trace 是否足够支持后续追因。
- `actions`
  1. 生成 `audit_trace`。
  2. 按三段式 Markdown 模板写 `<scene_key>.md`。
  3. 聚合并写 `场景设计.json`。
  4. 按需写 `_manifest.json`。
  5. 写 `acceptance_notes`，声明是否可交给 `3-面板 / 5-Image / 6-Video`。
- `evidence`
  - canonical 文件落盘。
  - audit 结论。
- `route_out`
  - 通过：任务完成。
  - 失败：回到对应节点返工。
- `gate`
  - 只有本节点允许写最终文件。

## Convergence Contract

- 汇流点固定为 `D6 -> D7 -> D8`。
- `FAIL-SCN-DES-01`：绕过 `1-清单` 或输入顺序漂移，回到 `D0-D1`。
- `FAIL-SCN-DES-02`：对象命中或证据包不成立，回到 `D1-D2`。
- `FAIL-SCN-DES-03`：空间、建筑、布景字段缺口或冲突，回到 `D3-D5`。
- `FAIL-SCN-DES-04`：candidate 无法收束为单一主稿，回到 `D6`。
- `FAIL-SCN-DES-05`：复核或审计未通过，回到指定返工节点。

## One-Shot Output Contract

### Canonical Outputs

- `projects/<项目名>/4-Design/场景/2-设计/第N集/场景设计.json`
- `projects/<项目名>/4-Design/场景/2-设计/第N集/<scene_key>.md`
- 可选 `projects/<项目名>/4-Design/场景/2-设计/第N集/_manifest.json`

### `场景设计.json` 最低结构

1. `episode_id`
2. `source_scene_catalog`
3. `scene_designs`
4. `summary`
5. `acceptance_notes`

### `scene_designs[]` 最低字段

- 身份与回链字段：`scene_key`、`scene_name`、`scene_variant`、`source_scene_ids`、`design_markdown_path`
- 三段式 Markdown 投影字段：
  `story_narrative`、`design_type`、`design_master`、`design_concept`、`design_style_detail`、`period_region`、`function_attribute`、`space_layout`、`space_type`、`material_detail`、`structural_detail`、`circulation_plan`、`color_theme`、`symbolic_design`、`ornament_pattern`、`lighting_design`、`lamp_design`、`furniture_design`、`wall_decor`、`floor_material`、`ecology_design`、`water_design`、`art_installation`、`atmosphere`、`weather`、`season_time`、`photo_shot_size`、`lens_type`、`camera_angle`、`composition_layout`、`composition_method`、`shape_sense`、`line_sense`、`tonal_sense`、`focus_sense`、`rhythm_sense`、`texture_sense`、`momentum`、`main_light`、`fill_light`、`back_light`、`lighting_type`、`color_hue`、`color_value`、`color_saturation`、`color_temperature`、`color_psychology`、`camera_model`、`aperture`、`shutter`、`iso`、`focal_length`、`resolution`、`prompt_integration`
- 兼容与下游消费字段：`design_direction`、`reverse_taboos`、`final_scene_prompt`、`panel_handoff`、`review_status`、`audit_trace`

### 逐场景 Markdown 卡片结构

每个 `<scene_key>.md` 必须采用三段式 Markdown：

1. `# [scene_name]`
2. `物语`：创意性文学发散正文，对应 `story_narrative`
3. `解构`：显式拆成 `场景设计 + 摄影设计` 两组参数位
4. `prompt整合`：最终模型消费 prompt，对应 `prompt_integration`

### Markdown 与 JSON 兼容映射

- `prompt_integration` 是人读与模型消费共用的主 prompt 文本。
- `final_scene_prompt` 必须与 `prompt_integration` 同步，作为 `3-面板 / 5-Image / 6-Video` 的兼容消费字段。
- `panel_handoff` 继续保留在 JSON 中，不强制出现在三段式 Markdown 正文。

### 硬规则

1. 中间节点可以形成局部结论，但只有本技能最终写出 canonical 文件。
2. 不允许为未命中场景补空设计稿。
3. 每个 `<scene_key>.md` 必须固定为 `物语 -> 解构 -> prompt整合` 三段式，不得回退成旧的分块模板。
4. `prompt整合` 只保留可供下游消费的汇总，不堆叠中间推理长文。
5. 若字段证据不足，允许显式写 `待补定`，不得静默省略。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| FIELD-SCN-DES-01 | 输入真源合同 | 锁定 `1-清单 -> 2-Global -> 3-Detail -> Init` 的读取顺序 | scene catalog、全局风格、导演证据、初始化预设 | D0-D2 | 真源一致性 | FAIL-SCN-DES-01 |
| FIELD-SCN-DES-02 | `scene_dispatch_plan` | 明确命中场景、优先级、证据缺口 | scene catalog、用户范围 | D1 | 对象裁决稳定性 | FAIL-SCN-DES-02 |
| FIELD-SCN-DES-03 | `scene_profile / space_type / function_attribute / space_layout / circulation_plan / photo_shot_size / camera_angle` | 场景原型、空间分区、动线与观看关系具备可执行性 | 镜头证据、剧情用途、scene catalog | D2-D3 | 空间可拍摄性 | FAIL-SCN-DES-03 |
| FIELD-SCN-DES-04 | `design_master / design_concept / period_region / material_detail / structural_detail / symbolic_design / cultural_constraints` | 参照锚点、建筑转写、材料与时代约束明确 | 2-Global、Init、空间逻辑 | D4 | 结构可信度 | FAIL-SCN-DES-04 |
| FIELD-SCN-DES-05 | `story_narrative / lighting_design / furniture_design / ecology_design / atmosphere / composition_layout / design_direction / reverse_taboos` | 人文痕迹、室内/景观细节、氛围与摄影设计具体可消费 | 剧情线索、风格线索、结构语言 | D5 | 设计具体度 | FAIL-SCN-DES-05 |
| FIELD-SCN-DES-06 | `scene_design_candidate / prompt_integration / final_scene_prompt / panel_handoff` | 单一候选、三段式 Markdown 与下游 handoff 同时成立 | 前述字段汇流 | D6 | 汇流完整性 | FAIL-SCN-DES-06 |
| FIELD-SCN-DES-07 | `review_status / audit_trace / acceptance_notes` | 复核与审计闭环完整 | review 与 audit 结论 | D7-D8 | 闭环可追溯性 | FAIL-SCN-DES-07 |

## Thought Pass Map

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| D0-D2 | FIELD-SCN-DES-01 / FIELD-SCN-DES-02 | 是否按正确顺序读取真源并锁定命中场景 | 锁定输入顺序、生成 dispatch plan 与 evidence packet | 绕过 `1-清单` 或为未命中场景建稿 |
| D3 | FIELD-SCN-DES-03 | 空间结构是否足以支撑剧情和镜头，并达到可画可拍可生成 | 生成场景原型、分区、动线与观看关系 | 只有氛围词，没有空间结构，或原型过泛 |
| D4 | FIELD-SCN-DES-04 | 参照锚点、时代、材料与建筑边界是否可信且已转写为当前项目实体 | 生成参照转写、建筑、结构与文化字段 | 风格词堆叠，缺少参照转写与结构约束 |
| D5 | FIELD-SCN-DES-05 | 人文痕迹、布景、氛围与摄影设计是否具体、可拍 | 生成物语、室内/景观细节、摄影参数与禁忌 | 只有抽象情绪词，没有可见标志物或观看设计 |
| D6 | FIELD-SCN-DES-06 | 是否已收束为单一候选，并同时满足三段式卡片与下游 handoff | 合成 candidate、prompt 与 panel_handoff | 出现多个候选、字段缺口或缺少参照/边界/标志元素闭环 |
| D7-D8 | FIELD-SCN-DES-07 | 结果是否通过复核、审计并可安全写回 | 输出 review、audit、acceptance 并写文件 | 无 trace、越权写回、路径漂移 |

## Pass Table

| field_id | 质量维度 | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- | --- |
| FIELD-SCN-DES-01 | 真源一致性 | 输入顺序明确，`1-清单` 是第一真源 | FAIL-SCN-DES-01 | D0 |
| FIELD-SCN-DES-02 | 对象裁决稳定性 | `scene_dispatch_plan` 只命中本轮实际需要场景 | FAIL-SCN-DES-02 | D1 |
| FIELD-SCN-DES-03 | 空间可拍摄性 | 场景原型、分区、动线、观看关系齐全，且空间可画可拍可生成 | FAIL-SCN-DES-03 | D3 |
| FIELD-SCN-DES-04 | 结构可信度 | 参照锚点、建筑转写、材料、文化约束明确且不冲突 | FAIL-SCN-DES-04 | D4 |
| FIELD-SCN-DES-05 | 设计具体度 | 物语、人文痕迹、室内/景观细节、氛围、摄影设计、方向、禁忌具体可消费 | FAIL-SCN-DES-05 | D5 |
| FIELD-SCN-DES-06 | 汇流完整性 | 只存在一个可写回的 candidate，且三段式卡片与下游 handoff 同时成立 | FAIL-SCN-DES-06 | D6 |
| FIELD-SCN-DES-07 | 闭环可追溯性 | review / audit / acceptance 完整，且仅本技能写最终文件 | FAIL-SCN-DES-07 | D7 |

## Root-Cause Execution Contract

当出现以下症状时，必须先修本子技能合同：

- `2-设计` 直接重扫 `3-Detail`，不复用 `1-清单`。
- 场景设计仍依赖外挂 agent docs，主合同与外部角色合同形成双重真源。
- 设计稿只剩风格词堆，没有空间结构、建筑边界或布景细节。
- 中间能力面各自产出平行主稿，无法汇成单一设计文件。
- 输出回到旧 runtime，或 review / audit 缺位。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/场景/2-设计/templates/scene-design-card.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/场景/SKILL.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - 根 `AGENTS.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-知行合一/SKILL.md`

用户闭环固定返回：

1. 根因位置
2. 立即修复
3. 系统预防修复

## Context Preload

- 执行前先加载 `.agents/skills/aigc/SKILL.md + CONTEXT.md`。
- 再加载 `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`。
- 再加载 `.agents/skills/aigc/4-Design/场景/SKILL.md + CONTEXT.md`。
- 最后加载本 `SKILL.md + CONTEXT.md` 与 `templates/scene-design-card.md`。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `aigc` 根技能 > `4-Design` 父级 > `1-场景` 父级 > 本 `SKILL.md` > 各级 `CONTEXT.md`。
