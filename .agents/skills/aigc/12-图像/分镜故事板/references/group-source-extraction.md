# Group Source Extraction Contract

本文件定义 step1 的输入锁定：以 `projects/aigc/<项目名>/10-分组` 为主要信息来源，获取每个分镜组的完整内容。

## Source Roots

固定读取：

```text
projects/aigc/<项目名>/10-分组/第N集.md
```

辅助上下文可读但不得覆盖组正文；legacy `north_star.yaml` 仅在旧项目已存在且本轮需要回读风格边界时加载：

```text
projects/aigc/<项目名>/MEMORY.md
projects/aigc/<项目名>/CONTEXT/
projects/aigc/<项目名>/0-初始化/north_star.yaml (legacy optional)
```

## Group Boundary

- 分镜组标题固定识别为 Markdown 二级标题：`## x-y-z`。
- 连接件标题固定识别为 Markdown 二级标题：`## x-y-z~x-y-z`，它不是分镜组。
- 一个分镜组从该标题开始，到下一个 `## x-y-z`、下一个 `## x-y-z~x-y-z` 或文件结尾前结束。
- `12-图像/分镜故事板` 默认完全忽略连接件块：不进入 `group_body`、storyboard prompt、YAML 主体基准、shot_count、reference manifest 或 imagegen plan。
- 组底 fenced YAML 必须作为该组的结构化主体来源；正文和 YAML 都要保留各自角色，不得互相替代。
- prompt 基础必须保留该组完整内容：`group_full_source = group_body + fenced YAML`。连接件仍然排除，不属于完整分镜组内容。
- `group_id` 使用三段式模式 `episode-scene-group`，例如 `1-1-1`。

## Extraction Payload

每个组至少输出：

```yaml
group_id: "1-1-1"
episode_id: "第1集"
source_file: "projects/aigc/<项目名>/10-分组/第1集.md"
heading: "## 1-1-1"
group_body: "<从标题后到 YAML 前的现有内容>"
group_full_source: "<从标题后到该组结束前的完整内容，包含 fenced YAML，不含连接件>"
group_yaml:
  字数统计: ""
  角色: []
  场景: []
  道具: []
shot_count: 0
source_shot_labels: []
storyboard_frame_units:
  - panel_no: 1
    panel_image_aspect_ratio: "16:9"
    source_shot_labels: []
    source_span: ""
    visual_beat: ""
    panel_description: ""
    panel_description_density: "rich_brief"
    panel_description_source: "source_span"
    character_name_labels:
      - name: ""
        source: "group_yaml.角色"
        placement: "above_character_head"
    annotation_plan:
      red_body_movement_arrows: ""
      blue_camera_movement_arrows: ""
      green_framing_composition_marks: ""
      orange_lighting_direction_marks: ""
      purple_emotion_sound_narrative_marks: ""
      black_text_notes_and_panel_label: ""
    mapping_type: "one_to_one | split_from_shot | merged_from_shots"
    rationale: ""
```

## Shot Count

- 优先统计组正文中的 `分镜N:` 标签。
- `source_shot_labels` 保留原始顺序，例如 `分镜1`、`分镜2`。
- `shot_count` 和 `source_shot_labels` 只表示上游运镜/镜头处理标签，不等同于 storyboard 的 panel count。
- 不要求把三段式组拆成四段式单镜输出；单镜任务应转到 `分镜画面`。

## Storyboard Frame Unit Derivation

- `storyboard_frame_units` 必须由 LLM 基于当前 `group_body` 的资料来源识别，不能由脚本用 `分镜N` 标签机械派生。
- frame unit 的落点依据是画面中需要单独表达的视觉节拍，包括关键动作变化、构图/景别变化、运镜造成的显著画面状态、情绪或光影转折，以及上游分组已经写明的关键画面。
- `分镜1`、`分镜2` 等标签只作为 `source_shot_labels` 和追溯线索。允许一个 `分镜N` 拆为多个 frame unit；也允许多个连续 `分镜N` 合并为一个 frame unit。
- 每个 frame unit 必须记录 `source_span` 或等价源文本摘要，能回指 `group_body` 的具体片段；不得补写上游没有的动作、情绪结果、角色事实或场景事实。
- 每个 frame unit 必须记录 `panel_description`，作为 storyboard panel 图片下方的文字内容。该描述由 LLM 从 `source_span` 和分组稿对应分镜描述原文中保真精简整合，默认 `panel_description_density: rich_brief`；不得由脚本模板拼接生成，不得引入上游没有的信息。
- `rich_brief` 精简规则：保留当前 panel 的主体/动作/画面状态；尽量纳入原文已有的景别/构图/运镜、情绪/声音/叙事强调、关键场景或道具信息；删除重复风格词、过长对白、执行说明和无关修饰。推荐 40-90 个中文字符，最多 120 个中文字符；若同一 sheet 的 frame units 很多，可压缩到 25-60 个中文字符。
- 每个 frame unit 必须记录 `panel_image_aspect_ratio`，默认 `16:9`；只有用户显式指定时才可改为 `9:16` 或其他比例。
- 每个 frame unit 必须记录 `character_name_labels`：每个可见角色头顶显示一个黑色文本角色名，角色名必须与当前组底 YAML `角色` 字段或分组稿中的角色名完全一致；不得简写、改名、翻译或按外观猜名。
- 每个 frame unit 必须记录 `annotation_plan`，从 `source_span` 与上游镜头信息中提取可标注项；不适用的标注类型写 `none`，不得发明不存在的运动、机位、灯光、声音或叙事强调。
- 若无法稳定判断 frame unit 数量，保持 `storyboard_frame_units_status: partial`，在报告中说明需要人工确认；不得退回“分镜标签数 = panel 数”的默认假设。

## Readiness Gate

通过 step1 必须满足：

1. `source_file` 存在且可读。
2. 每个目标 `group_id` 唯一出现。
3. `group_body` 非空。
4. fenced YAML 可解析，至少能得到 `角色 / 场景 / 道具` 三类字段；缺项可以为空数组但必须记录。
5. `shot_count` 大于 0；若无法自动统计，进入 `partial`，由人工审查确认完整性。
6. `storyboard_frame_units` 非空，且每个 frame unit 可回指源正文，并具备 `panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 与 `panel_image_aspect_ratio`；若为 `partial`，必须报告不确定原因。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `10-分组` 修复 |
| YAML fenced block 缺失 | 阻断参照绑定，允许 prompt-only 并报告 |
| group_body 被截断 | 重新按下一个二级标题定位边界 |
| group_full_source 缺 YAML 或缺正文 | 重新按组边界提取完整分镜组内容 |
| 连接件进入 group_body 或 prompt | 按 `## x-y-z~x-y-z` 重新切块并忽略连接件 |
| `分镜N` 统计不完整 | 保留原正文，报告 `shot_count_unverified` |
| storyboard panel 机械等同 `分镜N` | 回到 `Storyboard Frame Unit Derivation`，重新基于视觉节拍识别 |
| panel 缺描述文字、过度简略、过度冗长或默认比例 | 从 `source_span` 与分组稿对应分镜描述原文重建 `rich_brief panel_description`，并设 `panel_image_aspect_ratio: 16:9` |
| 角色头顶名称缺失或与分组稿不一致 | 从组底 YAML `角色` 字段重建 `character_name_labels` |
| annotation_plan 缺失或凭空补标注 | 从 `source_span` 重建标注计划；不适用项写 `none` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 目标 `group_id` 是否只能从 `projects/aigc/<项目名>/10-分组/第N集.md` 的 `## x-y-z` 标题锁定，且辅助上下文没有覆盖组正文？ | `G1-SOURCE` | `FAIL-SHEET-GROUP` | `N3-GROUP-INDEX` / `references/group-source-extraction.md#source-roots` | `group-index.json` 记录 `source_file`、`heading`、`group_id`、aux context 仅作上下文说明 |
| `## x-y-z~x-y-z` 连接件是否被识别为非分镜组，并完全排除出 `group_body`、storyboard prompt、YAML 主体基准、shot_count、manifest 和 imagegen plan？ | `G1-SOURCE` | `FAIL-SHEET-GROUP` | `N3-GROUP-INDEX` / `references/group-source-extraction.md#group-boundary` | `group-index.json` 记录 excluded connector headings，prompt / manifest / plan 无连接件条目 |
| 每个组的 `group_body`、`group_full_source` 与组底 fenced YAML 是否都被保留且职责分离，没有用正文替代 YAML 或用 YAML 覆盖正文？ | `G1-SOURCE` | `FAIL-SHEET-GROUP` | `N3-GROUP-INDEX` / `references/group-source-extraction.md#extraction-payload` | `group-index.json` 同时包含非空 `group_body`、`group_full_source` 与 `group_yaml`，并标明 YAML 解析状态 |
| `group_yaml` 是否至少解析出 `角色 / 场景 / 道具` 三类字段，缺项是否显式落为空数组并报告？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N3-GROUP-INDEX` / `N5-REF-BIND` | `group-index.json` 与 `reference-manifest.json` 记录三类字段、missing yaml fields 和空数组原因 |
| `shot_count` 与 `source_shot_labels` 是否只作为上游运镜标签追溯，而没有被当作 storyboard panel count？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `references/group-source-extraction.md#shot-count` | `group-index.json` 分开记录 `shot_count`、`source_shot_labels`、`storyboard_frame_units` 与 `mapping_type` |
| `storyboard_frame_units` 是否由 LLM 基于当前 `group_body` 的视觉节拍判断，而不是脚本按 `分镜N` 机械派生？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `references/group-source-extraction.md#storyboard-frame-unit-derivation` | 每个 frame unit 记录 `visual_beat`、`source_span`、`mapping_type` 和 LLM rationale |
| 每个 frame unit 是否能回指源正文片段，且没有补写上游不存在的动作、情绪结果、角色事实或场景事实？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N6-REVIEW` | `storyboard_frame_units[].source_span` 可定位，review note 标明未发现 invented fact |
| 每个 frame unit 是否包含来自 `source_span` 的 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 与默认 `panel_image_aspect_ratio: 16:9`，且 panel 描述没有新增事实、过度简略或过度冗长？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N4-PROMPT` | `group-index.json`、prompt 和 plan 中的 frame unit 字段一致，review note 抽查描述来源与长度 |
| frame unit 数量无法稳定判断时，是否保留 `storyboard_frame_units_status: partial` 并在报告中写明人工确认需求，而不是退回“分镜标签数 = panel 数”？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N3A-FRAME-UNITS` / `N10-CLOSE` | 执行报告记录 partial 原因、受影响 `group_id` 和返工入口 |
