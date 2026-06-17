# Prompt Assembly Contract

本文件定义 `N5-GROUP-CONSISTENCY` 与 `N6-PROMPT-PACKAGE`：把单个完整分镜组组织为 `.agents/skills/cli/imagegen` 组级 imagegen 任务包。多图输出必须是多张单独图片，不是故事板拼图。

## Mandatory Source Use

每个 `group_id` 的 prompt block 必须包含或可审计引用：

1. `group_full_content`：来自 `8-分组` 对应 `## x-y-z` 的完整正文。
2. `shot_points[]`：组内普通 `分镜N` 与 `shot_id` 的顺序映射。
3. `project_style_context`：来自 `2-美学/类型风格.md`、`2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的分镜/画面相关风格协议、项目 `MEMORY.md` 与相关 `CONTEXT/` 的风格边界直引或等价原文。
4. YAML 中对应角色、场景、道具主体图的参照状态。

禁止只把某个 `分镜N` 的片段作为 prompt 主源；组内前后关系、声音承托、画面风格和组底 YAML 都属于该组多图一致性的基础。

## Task Execution Prefix

每个组级 prompt 必须以前缀开头，并按当前组 `shot_count` 与画面比例填入数量。画面比例默认 `16:9`；只有用户显式要求时才替换为 `9:16` 或其他比例，并在 prompt、plan 和报告中记录 `aspect_ratio_override`：

```text
Imagegen storyboard-frame generation task. Use `.agents/skills/cli/imagegen` with the built-in `image_gen` route. Generate exactly <shot_count> separate <aspect_ratio> 2K cinematic live-action AIGC still images, one image for each numbered shot point in this storyboard group, in the exact order listed below. Do not create a storyboard sheet, collage, contact sheet, grid, comic page, multi-panel image, or variants of one frame. Return <shot_count> independent images that preserve the same character identities, costumes, scene design, lighting logic, color palette, material atmosphere, spatial anchors, and story continuity across the whole group.
```

若用户或上游指定其他画幅/分辨率，可替换 `<aspect_ratio> 2K`，但不得删除“separate images / not storyboard sheet / exact order / consistency”四类约束。未显式指定时，`<aspect_ratio>` 必须为 `16:9`。

## Required Markdown Shape

```markdown
## Group 1-1-1 Multi-Image Task

Task Execution Prefix:
<fixed prefix with shot_count>

Source Group Full Content:
```text
<完整引用 8-分组 中该组内容>
```

Project Style Context:
- global_style: <直引>
- genre_elements: <直引或 N/A>
- visual_style: <直引或 N/A>

Reference Images:
- Characters:
- Scene:
- Props:

Group Consistency Contract:
- character_identity_lock:
- costume_and_prop_lock:
- scene_space_lock:
- lighting_color_atmosphere_lock:
- spatial_axis_and_anchor_lock:
- continuity_between_images:
- non_collage_rule:

Image Order:
1. image_index: 1; shot_id: 1-1-1-1; source_shot_label: 分镜1
2. image_index: 2; shot_id: 1-1-1-2; source_shot_label: 分镜2

Image 1 / Shot ID 1-1-1-1:
- source_shot_label:
- source_shot_text:
- frame_state_to_restore:
- visible_subjects:
- scene_and_spatial_state:
- camera_and_composition:
- lighting_and_atmosphere:
- reference_usage:
- avoid:
- prompt: <natural English long prompt for this one image>

Image 2 / Shot ID 1-1-1-2:
...

Output Mapping:
- returned_image_1 -> 1-1-1-1.png
- returned_image_2 -> 1-1-1-2.png
```

`Aspect Ratio` 字段可写入 prompt block：

```yaml
Aspect Ratio:
  default: "16:9"
  selected: "16:9"
  override: null
```

## Prompt Authorship

- `prompt` 字段必须由 LLM 直接生成，不得脚本拼接主创正文。
- 每个 Image section 必须完整还原对应 `分镜N` 的画面状态：主体、动作结果、空间位置、镜头构图、可见道具、光影氛围和禁止项。
- 各 Image section 必须共享同一组 `Group Consistency Contract`，保持角色身份、服装、场景设计、色调、材质和关键道具一致。
- 不得把组稿翻译成一个总画面；必须保留 Image 1..N 的独立画面职责。
- 不得要求模型输出 storyboard sheet、multi-panel、grid、collage、contact sheet、comic page 或 variants。

## Reference Usage

- 角色、场景、道具参照图必须来自 `reference-manifest.json` 中 YAML 对应主体绑定结果。
- 参照图进入生成前必须 `view_image`，并在 prompt 中说明角色职责，例如 `character identity reference`、`scene visual style reference`、`prop reference`。
- 场景图既可作为空间/材质参考，也必须锁定画面风格、光影、色调和氛围。
- 缺参照图时记录 `missing_reference`，不得在 prompt 中伪称有图。

## Consistency Requirements

每个组级 prompt 必须覆盖：

- `same_character_identity`: 同一角色跨多图脸型、发型、服装、年龄、体态和气质一致。
- `same_scene_design`: 同一场景结构、材质、时代感、光线方向和色调一致。
- `spatial_continuity`: 角色站位、动线、视线、遮挡和关键道具位置能在同一 3D 空间中闭合。
- `shot_specific_state`: 每张图仍严格服从自己的 `分镜N`，不得为了一致性改写动作结果。
- `separate_output`: 每张图是单独 bitmap，不得在一张画布里分 panel。

## Imagegen Batch Count

- `expected_image_count` 必须等于 `shot_count`，并在 prompt、plan、result 与执行报告中保持一致。
- 批量多任务默认交由 `.agents/skills/cli/imagegen` 按 subagents 并发模式执行，最大并发数为 `10`；用户显式要求时才允许主线程逐一执行。
- 若 `shot_count` 或任务批量超过当前 imagegen 执行能力，不得静默拆分或漏图；应报告 `blocked_imagegen_batch_execution`，或在用户显式授权后改为拆组/重组方案。

## Word / Length Guidance

- 组级长提示词可以很长，但每个 Image section 应避免无关重复。
- 若 imagegen 对 prompt 长度报错，优先压缩重复风格词和已由 `Group Consistency Contract` 统一声明的内容，不得删除 `Source Group Full Content` 的审计引用或 Image section 的核心画面状态。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| prompt 是否以前缀明确要求生成 N 张单独图片，并禁止故事板/拼图/panel/variants？ | `G5-PROMPT` | `FAIL-FRAME-PROMPT` | `N6-PROMPT-PACKAGE` | prompt block 的 `Task Execution Prefix`。 |
| prompt 是否以完整组稿为基础，并按 Image 1..N 覆盖全部 `shot_points[]`？ | `G5-PROMPT` | `FAIL-FRAME-PROMPT` | `N6-PROMPT-PACKAGE` | `Source Group Full Content`、`Image Order`、Image sections 数量。 |
| 每张图是否还原对应分镜点画面状态，而不是合成一个总画面？ | `G5A-CONSISTENCY` | `FAIL-FRAME-CONSISTENCY` | `N5-GROUP-CONSISTENCY` / `N6-PROMPT-PACKAGE` | 每个 Image section 的 `source_shot_text`、`frame_state_to_restore`、英文 prompt。 |
| 角色、场景、道具参照和组级一致性是否进入 prompt 本体？ | `G4-REF` / `G5A-CONSISTENCY` | `FAIL-FRAME-REF` / `FAIL-FRAME-CONSISTENCY` | `N4-REF-BIND` / `N5-GROUP-CONSISTENCY` | `Reference Images` 与 `Group Consistency Contract`。 |
