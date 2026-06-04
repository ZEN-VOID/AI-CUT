# Aesthetic Style Analysis Contract

本文件定义 `shot-by-shot` 如何把参考素材逐镜分析转成 `.agents/skills/aigc/3-美学` 六个子技能可消费的 side context。它只提供证据、候选原则、去污染提示和下游 handoff，不生成或改写 `3-美学` 的正式协议正文。

## Boundary

- `3-美学/画面基调` 拥有正式 `全局风格协议.md`。
- `3-美学/角色风格` 拥有正式 `角色风格协议.md`。
- `3-美学/场景风格` 拥有正式 `场景风格协议.md`。
- `3-美学/道具风格` 拥有正式 `道具风格协议.md`。
- `3-美学/摄影风格` 拥有正式 `摄影风格协议.md`。
- `3-美学/分镜风格` 拥有正式 `分镜风格协议.md`。
- `shot-by-shot` 只拥有 `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/` 下的解析 side context。

## Canonical Side Context Files

整体美学桥接时输出以下 6 个解析文件：

| file | downstream subskill | focus | forbidden |
| --- | --- | --- | --- |
| `画面基调解析.md` | `3-美学/画面基调` | 媒介、渲染、光影范式、美学哲学、大师/作品锚点候选、全局 prompt 候选和污染审计 | 具体人物、物件、场景、构图、焦段、镜头运动 |
| `角色风格解析.md` | `3-美学/角色风格` | 轮廓语言、妆发纪律、服装结构倾向、体态张力、年龄质感、表演外观边界 | 具体角色卡、姓名、剧情动作、完整定装、参考人脸 |
| `场景风格解析.md` | `3-美学/场景风格` | 空间类型、空间压力、材质/光影秩序、空镜规则、世界地理视觉信号 | 具体场景清单、人物剪影、参考场景构图复制 |
| `道具风格解析.md` | `3-美学/道具风格` | 道具功能层级、材质体系、细节密度、符号边界、生成禁区 | 具体道具清单、纹章、地图文字、专属符号复制 |
| `摄影风格解析.md` | `3-美学/摄影风格` | 构图秩序、景别体系、机位高度、镜头运动、运动速度、视角关系、节奏密度、稳定性 | 具体分镜正文、镜头编号、参考片镜头顺序 |
| `分镜风格解析.md` | `3-美学/分镜风格` | 节奏密度、景别流转、镜头组合、转场逻辑、动作承接、信息揭示、段落推进、下游容错 | 具体分镜表、剧情动作、摄影参数、资产设计 |

`分镜风格解析.md` 不替代 `分镜脚本.md`。`分镜脚本.md` 继续由 `references/storyboard-script-contract.md` 约束。

## Required Markdown Shape

每个解析文件至少包含：

```markdown
# <解析文件名>

## 使用边界

- side_context_for:
- not_canonical:
- do_not_import:

## Source Evidence

| evidence_id | source_shots | observable_fact | evidence_grade |
| --- | --- | --- | --- |

## Transferable Principles

| principle_id | source_shots | transferable_principle | project_fit | downstream_use |
| --- | --- | --- | --- | --- |

## Style Seeds

| seed_id | source_shots | allowed_seed | why_it_maps | boundary |
| --- | --- | --- | --- | --- |

## Pollution Audit

| item | risk | action | verdict |
| --- | --- | --- | --- |

## Do Not Import

-
```

## Specialized Field Requirements

### `画面基调解析.md`

必须至少覆盖：

- `medium_and_rendering_seed`
- `light_atmosphere_seed`
- `aesthetic_paradigm_seed`
- `master_anchor_candidate`
- `global_style_prompt_candidate`
- `contamination_scan`

### `角色风格解析.md`

必须至少覆盖：

- `silhouette_language_seed`
- `hair_makeup_discipline_seed`
- `costume_structure_tendency`
- `body_tension_seed`
- `age_texture_seed`
- `performance_appearance_boundary`

### `场景风格解析.md`

必须至少覆盖：

- `space_type_seed`
- `spatial_pressure_seed`
- `material_light_order`
- `empty_scene_rule`
- `world_geography_signal`
- `scene_do_not_import`

### `道具风格解析.md`

必须至少覆盖：

- `prop_function_hierarchy`
- `material_system_seed`
- `detail_density_rule`
- `symbol_boundary`
- `generation_forbidden_zone`
- `prop_do_not_import`

### `摄影风格解析.md`

必须至少覆盖：

- `composition_order`
- `shot_size_system`
- `camera_height_rule`
- `camera_movement_profile`
- `movement_speed_rhythm`
- `continuity_rule_seed`

### `分镜风格解析.md`

必须至少覆盖：

- `rhythm_density`
- `shot_size_transition`
- `shot_combo_grammar`
- `transition_logic`
- `action_carryover_rule`
- `information_reveal_flow`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否只输出 side context，不生成或改写 3-美学正式协议？ | `GATE-SBS-AES-01` | `FAIL-SBS-AESTHETIC-CANONICAL-OVERREACH` | `N5A-AESTHETIC-BRIDGE` | 使用边界与未写 canonical 路径清单 |
| 整体美学桥接是否覆盖六个解析文件，部分点名是否只覆盖点名子技能？ | `GATE-SBS-AES-02` | `FAIL-SBS-AESTHETIC-ROUTE` | `N5A-AESTHETIC-BRIDGE` | enabled subskill matrix |
| 角色/场景/道具是否拆分为三份解析，而不是继续聚合成旧设计总包？ | `GATE-SBS-AES-03` | `FAIL-SBS-DESIGN-SPLIT` | `N5A-AESTHETIC-BRIDGE` | three asset style files |
| 摄影风格与分镜风格是否分离，且 `分镜风格解析.md` 不替代 `分镜脚本.md`？ | `GATE-SBS-AES-04` | `FAIL-SBS-CINE-STORYBOARD-MIX` | `N5A-AESTHETIC-BRIDGE` | two file manifests and boundary notes |
| 是否没有参考片具体人物、构图、镜头顺序、纹章、文字或对象细节进入 style seeds？ | `GATE-SBS-AES-05` | `FAIL-SBS-STYLE-POLLUTION` | `N6-RIGHTS-FEASIBILITY` | pollution audit and do-not-import ledger |
