# 5-设计 / 2-设计 Slot-Level Mapping And Review Contract

## Module Identity

- `module_type`: `stage-local-shared-slot-governance-contract`
- `primary_consumers`: `5-设计/2-设计` tranche parent、`场景`、`角色`、`道具` leaf、`_shared/subagent-supervision-contract.md`
- `target_scope`: 当前轮 `2-设计` canonical truth、Markdown projection、template slot、review bundle 与 rework landing

## Purpose

本合同补足 `5-设计/2-设计` 过去只停留在“文件级 review bundle”的缺口，把共享真源下沉到更细颗粒的槽位级：

1. 统一每个域的 canonical carrier / projection / provider-ready prompt carrier
2. 统一 `canonical JSON slot -> Markdown slot` 的共享映射
3. 统一当前轮顾问团 / 监制 / 评审 应盯的 `slot bundle`
4. 统一 `slot finding -> patch target -> rework entry` 的落点顺序

本合同不替代各 leaf 的本地字段表；它负责跨域共享结构。各 leaf 只补本域细节，不再各自发明第二套 bundle 语义。

## Canonical Sources

- `.agents/skills/aigc/5-设计/{场景,角色,道具}/references/design-output-contract.md`
- `.agents/skills/aigc/5-设计/{场景,角色,道具}/references/subagent-supervision-contract.md`
- `.agents/skills/aigc/5-设计/角色/templates/character_masterprompt.structured.v2.md`
- `.agents/skills/aigc/5-设计/道具/templates/prop_masterprompt.structured.v2.md`
- `.agents/skills/aigc/5-设计/场景/templates/scene_masterprompt.structured.v2.md`
- `.agents/skills/aigc/5-设计/角色/references/character-design-assembly.md`
- `.agents/skills/aigc/5-设计/场景/references/scene-design-assembly.md`
- `.agents/skills/aigc/5-设计/道具/references/prop-design-io-contract.md`

## Canonical Carrier Registry

| domain | canonical_truth | projection | provider_ready_prompt_carrier | note |
| --- | --- | --- | --- | --- |
| `场景` | `scene_design.json.scenes[]` | `[场景名].md` | `scenes[].full_generation_prompt` + Markdown `prompt整合` | Markdown 是 projection，不是 machine-first truth |
| `角色` | `character_design.json.roles[]` | `[角色名].md` | `roles[].full_generation_prompt` + Markdown `prompt整合` | Markdown 是 projection，不是 machine-first truth |
| `道具` | `<prop_id>-<canonical_name>.md` | `道具设计.json`、`prop_design_prompt.json`（显式兼容导出） | Markdown `prompt整合` | 当前仓道具以 Markdown 为 canonical truth |

硬规则：

1. slot 级 review 必须先锁本表中的 `canonical_truth`，再看 projection。
2. provider-ready prompt 问题默认先 patch canonical truth 中承载 prompt 的字段；projection 只做同步。
3. 若问题属于模板结构漂移、renderer 漂移或 validator 失效，不得把业务文件硬改成第三种结构；必须回到模板/脚本/合同真源。

## Slot Bundle Registry

### 场景

| bundle_id | canonical carrier | canonical slots | Markdown slots | review focus | default patch target | downstream consumers |
| --- | --- | --- | --- | --- | --- | --- |
| `SCENE-BUNDLE-01-story-world` | `scene_design.json.scenes[]` | `story_premise`、`compendium`、`source_trace` | `物语` | 叙事空间是否成立、故事世界是否读得出 | `scene_design.json` | `3-面板/场景`、后续 image/video |
| `SCENE-BUNDLE-02-design-structure` | `scene_design.json.scenes[].structured_fields.scene_design` | `scene_design.*` | `解构 / Scene Design` | 空间结构、材料、动线、时期/地域与文化元素 | `scene_design.json` | `3-面板/场景` |
| `SCENE-BUNDLE-03-cinematography` | `scene_design.json.scenes[].structured_fields.cinematography` | `cinematography.*` | `解构 / Cinematography` | 镜头、光线、色彩、取景与构图可执行性 | `scene_design.json` | `3-面板/场景`、image/video |
| `SCENE-BUNDLE-04-prompt-cleanliness` | `scene_design.json.scenes[]` | `reasoning_pivot`、`prompt_integration`、`global_style_prefix`、`full_generation_prompt`、`quality_flags` | `Reasoning Pivot`、`prompt整合` | 必须是 `empty environmental shot`、`no characters`，且 integrated prompt 可被稳定提取 | 先 patch canonical prompt slots，再同步 Markdown | `auto_image`、`3-面板/场景` |

### 角色

| bundle_id | canonical carrier | canonical slots | Markdown slots | review focus | default patch target | downstream consumers |
| --- | --- | --- | --- | --- | --- | --- |
| `ROLE-BUNDLE-01-identity-pressure` | `character_design.json.roles[]` | `role_id`、`role_name`、`role_tier`、`costume_state`、`story_premise`、`identity_hook`、`narrative_tension` | `物语`、`Identity & Story Pressure` | 身份钩子、戏剧压力、关系轴是否稳定 | `character_design.json` | `3-面板/角色`、后续 image |
| `ROLE-BUNDLE-02-visual-system` | `character_design.json.roles[]` | `style_backbone`、`character_style`、`structured_fields.face_* / hair_* / body_* / costume_*` | `Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design` | 脸、发、体态、服装和连续性是否形成系统 | `character_design.json` | `3-面板/角色` |
| `ROLE-BUNDLE-03-camera-readability` | `character_design.json.roles[]` | `structured_fields.camera_*`、`midjourney_params` | `Cinematography` | 角色定妆图的镜头可读性与单主体构图 | `character_design.json` | `3-面板/角色`、image |
| `ROLE-BUNDLE-04-prompt-cleanliness` | `character_design.json.roles[]` | `prompt_integration`、`global_style_prefix`、`full_generation_prompt`、`quality_flags` | `prompt整合` | 必须是 `solid color background`、`no scene background elements`，且 integrated prompt 保留身份与服装差异轴 | 先 patch canonical prompt slots，再同步 Markdown | `auto_image`、`3-面板/角色` |

### 道具

| bundle_id | canonical carrier | canonical slots | Markdown slots | review focus | default patch target | downstream consumers |
| --- | --- | --- | --- | --- | --- | --- |
| `PROP-BUNDLE-01-story-function` | `<prop_id>-<canonical_name>.md` | `物语`、`narrative_significance` 对应叙事信息 | `物语` | 道具在叙事中的功能、重要性与特殊性是否可见 | canonical Markdown | `3-面板/道具`、后续 image/video |
| `PROP-BUNDLE-02-design-structure` | canonical Markdown | `style_backbone`、`prop_type`、`design_inspiration`、`functionality`、`material/texture/decoration/pattern`、`ergonomics` | `解构 / Prop Design` | 功能、材质、形态、工艺和状态痕迹 | canonical Markdown | `3-面板/道具` |
| `PROP-BUNDLE-03-photography-readability` | canonical Markdown | `photo_type`、`photo_shot_size`、`photo_background` | `解构 / Photography` | 单道具参照图的取景与背景是否正确 | canonical Markdown | `3-面板/道具`、image |
| `PROP-BUNDLE-04-prompt-cleanliness` | canonical Markdown | `reasoning_pivot`、`global_style_prefix`、`prompt_integration`、`full_generation_prompt`、`reference_cleanliness_note` | `Reasoning Pivot`、`prompt整合` | 必须是 `isolated pure prop view`、`no hands`、`no characters`，且不把使用者写进画面主体 | canonical Markdown | `auto_image`、`3-面板/道具` |

## Shared Review Bundle Resolution

当 `2-设计` 或其 leaf 记录当前轮 post-write audit note 时，review target 不再只停留在文件名，而必须解析成：

1. target files
   - `canonical truth`
   - `projection`
   - `_manifest.json`
   - 按需 `validation-report.md`
2. slot bundles
   - 场景：`SCENE-BUNDLE-01~04`
   - 角色：`ROLE-BUNDLE-01~04`
   - 道具：`PROP-BUNDLE-01~04`

硬规则：

1. reviewer finding 必须尽量回指 `bundle_id`，而不是只说“这个文件有问题”。
2. 若一个 finding 同时影响多个 bundle，应先归到最上游可修复 bundle。
3. 若当前轮命中多个域，主代理可以按域汇流，但不得把不同域的 bundle 混成一份平行总稿。

## Slot Finding To Patch Order

| issue_type | symptom | patch order | rework rule |
| --- | --- | --- | --- |
| `canonical_missing_or_thin` | machine-first truth 缺字段、字段过薄、槽位未落盘 | 先补 canonical truth，再回写 projection | 不得只修 Markdown 外观 |
| `projection_drift` | Markdown/compat projection 与 canonical truth 不一致 | 先补 canonical truth 映射，再重投影 | 若是模板或 renderer 漂移，升格为 source-layer 修复 |
| `prompt_cleanliness_failure` | 空镜/纯色背景/纯道具锚句缺失，或污染主体回流 | 先补 prompt carrier 与 reasoning/cleanliness note，再重跑 auto image | 不得靠裁切图片或 reviewer prose 兜底 |
| `template_shape_drift` | 模板章节缺失、顺序漂移、validator 与模板口径不一致 | 先修模板/renderer/validator 真源，再重建 projection | 不得把临时业务文件升为新模板 |
| `handoff_not_ready` | `3-面板` 仍需重猜字段或 prompt | 回到对应 bundle 的 canonical slots 修正 handoff-ready 字段 | 不得在 `3-面板` 私补对象/风格主键 |

## Bundle To Reviewer Focus

| domain | preferred design checks | preferred reviewers |
| --- | --- | --- |
| `场景` | `space_and_scale`、`material_and_texture`、`light_and_weather`、`blocking_and_wayfinding` | `隈研吾`、`叶锦添` |
| `角色` | `silhouette_and_pose`、`costume_and_layering`、`face_hair_makeup`、`camera_readability` | `张叔平`、`叶锦添` |
| `道具` | `function_and_affordance`、`material_and_finish`、`state_trace`、`hand_relation_offscreen` | `张叔平`、`叶锦添` |

说明：

- 当前 post-write audit 不再依赖 reviewer roster；若未来独立审计工作流恢复 reviewer 解析，应由新的 audit contract 裁决。
- 本表只负责告诉 reviewer 应优先盯哪些 slot bundle，不负责授权。

## Domain Extension Rule

1. 各 leaf 可在本地 `references/*-assembly.md` 继续维护本域专有的 slot 细节、字段含义与保守模式。
2. 但跨域共享的 bundle 命名、canonical carrier 边界、review bundle 解析顺序与 patch order，必须以上述表格为真源。
3. 若新增 `服装` leaf，必须先在本合同补 `carrier registry + slot bundle registry + reviewer focus`，再宣称 active。

## Verification Checklist

1. 当前轮目标已能从“文件级”解析到“slot bundle 级”。
2. 每个 active 域都能回答：哪个 carrier 是 canonical truth，哪个 carrier 只是 projection。
3. reviewer finding 能回指 `bundle_id` 或至少能回指对应 slot cluster。
4. prompt / cleanliness 问题不会再直接退化成“手改 Markdown 两行”。
5. `template drift` 能被识别为 source-layer 问题，而不是业务文件问题。
