# Group Source Extraction Contract

本文件定义 step1 的输入锁定：以 `projects/aigc/<项目名>/5-分组` 为主要信息来源，获取每个分镜组的完整内容。

## Source Roots

固定读取：

```text
projects/aigc/<项目名>/5-分组/第N集.md
```

辅助上下文可读但不得覆盖组正文：

```text
projects/aigc/<项目名>/MEMORY.md
projects/aigc/<项目名>/CONTEXT/
projects/aigc/<项目名>/0-初始化/north_star.yaml
```

## Group Boundary

- 分镜组标题固定识别为 Markdown 二级标题：`## x-y-z`。
- 连接件标题固定识别为 Markdown 二级标题：`## x-y-z~x-y-z`，它不是分镜组。
- 一个分镜组从该标题开始，到下一个 `## x-y-z`、下一个 `## x-y-z~x-y-z` 或文件结尾前结束。
- `8-视频/C-主体参照` 默认完全忽略连接件块：不进入 `group_body`、视频 prompt、YAML 主体槽位、reference manifest、LibTV submit plan 或视频文件命名。
- 组底 fenced YAML 必须作为该组的结构化主体来源；正文和 YAML 都要保留各自角色，不得互相替代。
- `group_id` 使用三段式模式 `episode-scene-group`，例如 `1-1-1`。

## Extraction Payload

每个组至少输出：

```yaml
group_id: "1-1-1"
episode_id: "第1集"
source_file: "projects/aigc/<项目名>/5-分组/第1集.md"
heading: "## 1-1-1"
group_body: "<从标题后到 YAML 前的现有内容>"
group_yaml:
  字数统计: ""
  时长估算: ""
  角色: []
  场景: []
  道具: []
shot_count: 0
source_shot_labels: []
duration_estimate_seconds: 15
duration_source: "group_yaml / shot_sum / fallback_default"
```

## Video Prompt Source Rule

- `group_body` 是视频 prompt 的主要正文来源。
- 不删除分镜明细、音效、对白、环境描写和表演提示；默认跳过组间连接件。
- 不把 YAML 合并进正文主段；YAML 是主体参照注入的唯一位置。生成 `prompt.md` 时必须保留原 fenced YAML，只把有图且已上传的主体列表项扩展为对象并补 `uploaded_url`，缺图主体保持原名称。
- 若组正文过长，只允许在 LibTV handoff 层做可审查压缩摘要，并保留完整原文路径和原文字数。

## Duration Extraction Rule

- 优先读取组底 YAML 的 `时长估算`，例如 `约12秒` 解析为 `duration_estimate_seconds: 12`。
- 若 `时长估算` 缺失，才从组正文 `分镜明细` 中的 `约N秒` 或 `N-M秒` 求和估算；区间时长优先取上限，避免动作被截断。
- 若仍无法估算，`duration_estimate_seconds` 回退为 `15`，并记录 `duration_source: fallback_default` 与原因。
- 连接件块的 `时长` 不参与分镜组视频时长估算。
- 最终提交给 LibTV 的 `duration_hint` 不在本步骤决定；它由 handoff 层按 `clamp(duration_estimate_seconds, 4, 15)` 生成。

## Readiness Gate

通过 step1 必须满足：

1. `source_file` 存在且可读。
2. 每个目标 `group_id` 唯一出现。
3. `group_body` 非空。
4. fenced YAML 可解析，至少能得到 `角色 / 场景 / 道具` 三类字段；缺项可以为空数组但必须记录。
5. `duration_estimate_seconds` 可追溯到组底 `时长估算`、组内分镜秒数求和或明确 fallback。
6. `shot_count` 大于 0；若无法自动统计，进入 `partial`，由人工审查确认完整性。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否只从 `projects/aigc/<项目名>/5-分组/第N集.md` 锁定目标组，不回退 `4-摄影`、`3-Detail` 或更早阶段重写内容？ | `G1-SOURCE` | `FAIL-VIDSUBJ-GROUP` | `N3-GROUP-INDEX` / 本文件 `Source Roots` | `reference-manifest.json.group_source.source_file`、`heading`、源文件路径和读取范围 |
| `## x-y-z` 分镜组与 `## x-y-z~x-y-z` 连接件是否被正确区分，连接件是否未进入 group body、prompt、YAML 主体、manifest、submit plan 或视频命名？ | `G1-SOURCE` / `G2-CONTENT` | `FAIL-VIDSUBJ-GROUP` / `FAIL-VIDSUBJ-PROMPT` | `N3-GROUP-INDEX` / `N4-PROMPT` | group index 中的 `group_id`、`heading`、connector skipped 记录和 prompt 源文本片段 |
| 每个目标 `group_id` 是否唯一回指源标题，且 `group_body` 从标题后完整截到下一个二级标题或文件结尾前？ | `G1-SOURCE` | `FAIL-VIDSUBJ-GROUP` | `N3-GROUP-INDEX` | `source_span`、`group_body_length`、`shot_count`、截取边界说明 |
| fenced YAML 是否被作为结构化主体来源保留，且正文与 YAML 角色未互相替代？ | `G1-SOURCE` / `G3-SUBJECTS` | `FAIL-VIDSUBJ-GROUP` / `FAIL-VIDSUBJ-REF` | `N3-GROUP-INDEX` / `N5-REF-BIND` | `group_yaml` 原文、解析后的 `角色 / 场景 / 道具`、缺项记录 |
| prompt 源文本是否保留分镜明细、对白、音效、环境描写和表演提示，且没有把 YAML 合并进正文主段？ | `G2-CONTENT` / `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-PROMPT` / `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N4-PROMPT` | `prompt.md` 中原组正文和 fenced YAML 的源文对照 |
| `duration_estimate_seconds` 是否优先来自组底 `时长估算`，其次来自分镜秒数求和，最后才是明确 fallback？ | `G8-DURATION` | `FAIL-VIDSUBJ-DURATION` | `N3-GROUP-INDEX` | `duration_source`、`duration_estimate_seconds`、原始时长字段或分镜秒数计算证据 |
| `shot_count` 与 `source_shot_labels` 是否能证明组内分镜被完整识别；无法自动统计时是否进入 `partial / shot_count_unverified`？ | `G1-SOURCE` | `FAIL-VIDSUBJ-GROUP` | `N3-GROUP-INDEX` / `N6-REVIEW` | `shot_count`、`source_shot_labels`、`partial` finding 或人工复核说明 |
| step1 失败或降级是否留下可返工入口，而不是静默继续绑定主体或提交 LibTV？ | `G13-REPORT` | `FAIL-VIDSUBJ-REPORT` | `N6-REVIEW` / `N11-CLOSE` | 执行报告中的 `blocked / partial / prompt_only` 状态、失败信号和下一步返工入口 |

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `5-分组` 修复 |
| YAML fenced block 缺失 | 阻断参照绑定，允许 prompt-only 并报告 |
| group_body 被截断 | 重新按下一个二级标题定位边界 |
| 连接件进入 group_body 或 prompt | 按 `## x-y-z~x-y-z` 重新切块并忽略连接件 |
| `分镜N` 统计不完整 | 保留原正文，报告 `shot_count_unverified` |
