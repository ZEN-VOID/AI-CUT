# Group Shot Source Contract

本文件定义 step1：以 `projects/aigc/<项目名>/4-分组` 为主要信息来源，获取每个分镜组的完整内容，并把组内镜头映射为四段式 `分镜ID`。

## Source Roots

固定读取：

```text
projects/aigc/<项目名>/4-分组/第N集.md
```

辅助上下文可读但不得覆盖组正文：

```text
projects/aigc/<项目名>/MEMORY.md
projects/aigc/<项目名>/CONTEXT/
```

## Group Boundary

- 分镜组标题固定识别为 Markdown 二级标题：`## x-y-z`。
- 连接件标题固定识别为 Markdown 二级标题：`## x-y-z~x-y-z`，它不是分镜组。
- 一个分镜组从该标题开始，到下一个 `## x-y-z`、下一个 `## x-y-z~x-y-z` 或文件结尾前结束。
- `7-视频/A-分镜画面参照` 默认完全忽略连接件块：不进入 `group_content`、四段式 `shot_id` 映射、视频 prompt、reference manifest、LibTV batch 或视频文件命名。
- `group_id` 使用三段式模式 `episode-scene-group`，例如 `1-1-1`。
- 视频 prompt 主体使用完整组内容，不用底部 YAML 或摘要替代正文。

## Shot ID Mapping

- 组内每个 `分镜N`、`分镜 N` 或同义镜头标签默认映射为 `x-y-z-N`。
- 若组稿已经明确提供四段式 `分镜ID`，以现有 `分镜ID` 为基准，不重新编号覆盖。
- 一个四段式 `shot_id` 必须唯一隶属于一个 `group_id`。
- 用户输入四段式 `shot_id` 时，本技能应回推所属 `group_id`，再以组为单位生成视频 job。

## Extraction Payload

每个组至少输出：

```yaml
group_id: "1-1-1"
episode_id: "第1集"
source_file: "projects/aigc/<项目名>/4-分组/第1集.md"
heading: "## 1-1-1"
group_content: "<从标题后到下一个普通组标题或连接件标题前的现有完整内容>"
source_body_hash: "<sha256>"
duration_estimate_seconds: 15
duration_source: "group_yaml / shot_sum / fallback_default"
shots:
  - shot_id: "1-1-1-1"
    source_label: "分镜1"
    line_hint: 0
    reference_annotation: "1-1-1-1"
```

## Duration Extraction Rule

- 优先读取组底 YAML 的 `时长估算`，例如 `约12秒` 解析为 `duration_estimate_seconds: 12`。
- 若 `时长估算` 缺失，才从组正文 `分镜明细` 中的 `约N秒` 或 `N-M秒` 求和估算；区间时长优先取上限，避免动作被截断。
- 若仍无法估算，`duration_estimate_seconds` 回退为 `15`，并记录 `duration_source: fallback_default` 与原因。
- 连接件块的 `时长` 不参与分镜组视频时长估算。
- 最终提交给 LibTV 的 `duration_hint` 由 handoff 层按 `clamp(duration_estimate_seconds, 4, 15)` 生成；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。

## Prompt Body Rule

- `group_content` 是 LibTV prompt 的主体，不得摘要替代；`prompt.md` 必须以原 `## group_id` 起笔。
- 默认不在 `group_content` 前添加参照说明段；LibTV 运输层约束只出现在 `libtv-submission.txt` 的调用锁和直接生成请求中。
- 对有图的镜头，唯一允许改写源文本的位置是 fenced YAML：新增或更新 `分镜画面参照` 列表，写入 `shot_id / source_label / uploaded_url`；不得用 `shot_id@path`、`@图N` 或另起参照说明段作为远端真源。
- 不得改写剧情事实、对白事实、镜头顺序、角色关系、场景结果或组边界。
- 如需压缩，只能在用户明确要求或 LibTV 硬限制触发时执行，并必须记录压缩依据与被压缩字段；默认不压缩。

## Readiness Gate

通过 step1 必须满足：

1. `source_file` 存在且可读。
2. 每个目标 `group_id` 唯一出现。
3. `group_content` 非空。
4. `duration_estimate_seconds` 可追溯到组底 `时长估算`、组内分镜秒数求和或明确 fallback。
5. 每个目标 `shot_id` 可回指源组和组内标签；无法解析时标记 `shot_id_unresolved` 并阻断该镜参照绑定。
6. 输出 group-shot index 记录 source file、heading、line range 或 hash，便于回放。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `4-分组` 修复 |
| group_content 被截断 | 重新按下一个二级标题定位边界 |
| 连接件进入 group_content 或 prompt | 按 `## x-y-z~x-y-z` 重新切块并忽略连接件 |
| 组正文被摘要或改写 | 回到本合同，恢复完整现有内容 |
| `分镜N` 与四段式 ID 对不上 | 优先使用已提供的 `分镜ID`，并在 index 中记录映射依据 |
