# Group Source Contract

本文件定义 step1：以 `projects/aigc/<项目名>/4-分组` 为主要信息来源，获取每个分镜组的完整内容，并直接作为生视频提示词主体。

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
- `7-视频/B-分镜故事板参照` 默认完全忽略连接件块：不进入 `group_content`、视频 prompt、storyboard reference manifest、LibTV batch 或视频文件命名。
- `group_id` 使用三段式模式 `episode-scene-group`，例如 `1-1-1`。
- 若组底存在 fenced YAML，应保留在索引中供审查与报告使用；视频 prompt 主体仍以完整组内容为主，不用 YAML 替代正文。

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
shot_count: 0
source_shot_labels: []
```

## Duration Extraction Rule

- 优先读取组底 YAML 的 `时长估算`，例如 `约12秒` 解析为 `duration_estimate_seconds: 12`。
- 若 `时长估算` 缺失，才从组正文 `分镜明细` 中的 `约N秒` 或 `N-M秒` 求和估算；区间时长优先取上限，避免动作被截断。
- 若仍无法估算，`duration_estimate_seconds` 回退为 `15`，并记录 `duration_source: fallback_default` 与原因。
- 连接件块的 `时长` 不参与分镜组视频时长估算。
- 最终提交给 LibTV 的 `duration_hint` 由 handoff 层按 `clamp(duration_estimate_seconds, 4, 15)` 生成；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。

## Prompt Body Rule

- `group_content` 是 LibTV prompt 的主体，不得摘要替代；`prompt.md` 必须以原 `## group_id` 起笔。
- 默认不在 `group_content` 前添加故事板参照说明段；LibTV 运输层约束只出现在 `libtv-submission.txt` 的调用锁和直接生成请求中。
- 对有故事板图的组，唯一允许改写源文本的位置是 fenced YAML：draft 阶段不写 `reference_index / uploaded_url`；final 阶段新增或更新 `故事板参照` 对象，写入 `name / role / reference_index / uploaded_url / image_token`；不得用 `故事板总参照：<url>` 或另起参照说明段作为远端真源。
- 不得改写剧情事实、对白事实、镜头顺序、角色关系、场景结果或组边界。
- 如需压缩，只能在用户明确要求或 LibTV 硬限制触发时执行，并必须记录压缩依据与被压缩字段；默认不压缩。

## Readiness Gate

通过 step1 必须满足：

1. `source_file` 存在且可读。
2. 每个目标 `group_id` 唯一出现。
3. `group_content` 非空。
4. `duration_estimate_seconds` 可追溯到组底 `时长估算`、组内分镜秒数求和或明确 fallback。
5. `source_shot_labels` 可从 `分镜N`、`分镜 N` 或等价标签中尽量统计；无法统计时标记 `shot_count_unverified`，不改写正文。
6. 输出 group index 记录 source file、heading、line range 或 hash，便于回放。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `4-分组` 修复 |
| group_content 被截断 | 重新按下一个二级标题定位边界 |
| 连接件进入 group_content 或 prompt | 按 `## x-y-z~x-y-z` 重新切块并忽略连接件 |
| 组正文被摘要或改写 | 回到本合同，恢复完整现有内容 |
| `分镜N` 统计不完整 | 保留原正文，报告 `shot_count_unverified` |
