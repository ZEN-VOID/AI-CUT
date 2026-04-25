# 1-Planning I/O 统一契约（Mandatory）

## 1. 目标

将 `1-Planning` 收敛为“一份分集原文真源 + 一份剧本主稿 + 一份分集机读索引 + 一份带分组切口的 grouped script”的单一工程口径，避免 `Story/`、`1-Planning/` 与后续 `2-Global/` 或 `3-Detail/` 之间再出现平行真相。

## 2. Canonical Outputs

- 默认输入根：`projects/aigc/<项目名>/Story/`
- `1-分集` 逐集原文真源：`projects/aigc/<项目名>/1-Planning/1-分集/第N集.md`
- `2-格式` 逐集主稿：`projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`
- `2-格式` 总执行报告：`projects/aigc/<项目名>/1-Planning/2-格式/执行报告.md`
- `3-分组` grouped script：`projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- `3-分组` 总执行报告：`projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md`
- 阶段验收：`projects/aigc/<项目名>/1-Planning/validation-report.md`
- `1-分集` 全剧集执行报告：`projects/aigc/<项目名>/1-Planning/1-分集/执行报告.md`
- `1-分集` 机读索引：`projects/aigc/<项目名>/1-Planning/episode-split-plan.json`

规则：

1. `1-分集` 的 canonical 输出固定为 `projects/aigc/<项目名>/1-Planning/1-分集/第N集.md`，只承担逐集原文真源，不直接写 `2-格式` 主稿。
2. `2-格式` 消费 `1-分集` 输出物，并写回 `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`。
3. `episode-split-plan.json` 只承担边界、coverage、`source_profile` 与下游 handoff，不替代 Markdown 主稿。
4. `3-分组` 的 canonical 输出固定为 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`，它必须以 grouped script 形式直接继承 `2-格式` 正文，并在切口处插入三段式 `分镜组ID` 标题 `【x-x-x】`。
5. `2-格式` 目录只保留一份 `执行报告.md` 总稿；每集 validator、变体裁决与返工项作为报告内 episode 区块登记，不再为每一集长出 `第N集-执行报告.md`。
6. `3-分组` 目录只保留一份 `执行报告.md` 总稿，不再为每一集长出单独报告，也不再默认生成 `.grouping.json`、`thinking/` 等平行真源。
7. `1-分集` 最多只保留一份全剧集执行报告，不再为每一集单独生成报告侧车。
8. `3-分组` 的 frontmatter 必须投影 `scene_unit_count / duration_policy / pace_tier / base_text_window / warn_window / hard_text_window / 默认组时长 / 分镜组时长映射 / 时长偏离证据`。

## 3. 输入路由总规则

1. 用户显式指定文件时，用户指定优先。
2. 用户未指定时，`1-分集` 默认扫描 `projects/aigc/<项目名>/Story/` 相关内容。
3. `2-格式` 默认只读取 `1-分集` 输出物，不回退到 `Story/` 重做自由切分。
4. 若 `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml` 存在，应将其作为输入索引与 coverage 证据优先消费。
5. `1-分集` 不得自行扩展到 `development_briefs` 或其他非故事正文材料。
6. 例外：当 `story-source-manifest.yaml` 已显式登记 `development_briefs`，且 `readiness` 明确允许“开发式/增量分集”时，`1-分集` 可把这些 brief 仅作为边界辅证输入。
7. 上述例外不改变真源层级：`development_briefs` 仍不是 `primary_story_source`，不得被写成“整季正文已就绪”或覆盖正文真源。

## 4. Handoff Contract

`1-分集` 至 `2-格式` / 父 skill / 下游阶段的最小 handoff 字段：

- `episode_id`
- `coverage_scope`
- `split_scope`
- `boundary_summary`
- `source_profile`
- `bootstrap_output`
- `upstream_paths`

`2-格式` 至父 skill / 下游阶段的最小 handoff 字段：

- `episode_id`
- `selected_variant`
- `script_output_path`
- `scene_count`
- `dialogue_policy`
- `narration_policy`
- `source_profile`
- `bootstrap_output`
- `upstream_paths`

`3-分组` 至父 skill / 下游阶段的最小 handoff 字段：

- `episode_id`
- `group_count`
- `group_order`
- `locked_anchor_ids`
- `duration_policy`
- `pace_tier`
- `handoff_summary`
- `bootstrap_output`
- `upstream_paths`

## 5. Source Profile Mapping

`source_profile` 必须优先映射自 `story-source-manifest.yaml`；若 manifest 缺失，则仅允许基于 `projects/aigc/<项目名>/Story/` 已知正文做保守推断：

- `source_type`
- `preset_retention_mode`
- `detail_expansion_mode`
- `locked_preset_axes`
- `preset_registry`

保守降级规则：

- 允许降级到 `standard / free_expansion`
- 不允许私自脑补新的锁轴或预设锚点

## 6. Compatibility Guardrails

1. 不复制 `AIGC-ZEN-VOID` 的 `output/影片/<项目名>/1-编剧/...` 路径结构。
2. 不在 `1-Planning` 里引入第二套 `runtime_profiles.json` 平行真源。
3. 不把 `episode_index.json` 作为 DREAMER 规划阶段的新 canonical 文件名；统一收敛为 `episode-split-plan.json`。
4. 不把 `1-分集/第N集.md` 误写成 `2-格式/第N集.md`；前者是上游原文真源，后者是下游 canonical 主稿。
5. 不把 `3-分组/第N集.md` 误写成第二份 `2-格式/第N集.md`；它只承载组级本地真源。
6. 不把四段式 `分镜ID` 误写进 `3-分组` 标题；本阶段标题只允许三段式 `分镜组ID`。
