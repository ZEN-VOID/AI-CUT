# Group Source Contract

本文件定义 step1：以 `projects/aigc/<项目名>/5-分组` 为主要信息来源，获取每个分镜组的完整内容，并直接作为生视频提示词主体。

## Source Roots

固定读取：

```text
projects/aigc/<项目名>/5-分组/第N集.md
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
- `8-视频/B-分镜故事板参照` 默认完全忽略连接件块：不进入 `group_content`、视频 prompt、storyboard reference manifest、LibTV batch 或视频文件命名。
- `group_id` 使用三段式模式 `episode-scene-group`，例如 `1-1-1`。
- 若组底存在 fenced YAML，应保留在索引中供审查与报告使用；视频 prompt 主体仍以完整组内容为主，不用 YAML 替代正文。

## Extraction Payload

每个组至少输出：

```yaml
group_id: "1-1-1"
episode_id: "第1集"
source_file: "projects/aigc/<项目名>/5-分组/第1集.md"
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
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `5-分组` 修复 |
| group_content 被截断 | 重新按下一个二级标题定位边界 |
| 连接件进入 group_content 或 prompt | 按 `## x-y-z~x-y-z` 重新切块并忽略连接件 |
| 组正文被摘要或改写 | 回到本合同，恢复完整现有内容 |
| `分镜N` 统计不完整 | 保留原正文，报告 `shot_count_unverified` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 本轮项目、集号和目标 `group_id` 是否只从 `projects/aigc/<项目名>/5-分组/第N集.md` 锁定，且 `MEMORY.md` / `CONTEXT/` 没有覆盖组正文？ | `GATE-SBVID-01` | `FAIL-SBVID-INPUT` | `N1-INTAKE` / `N2-CONTEXT` | input manifest 记录项目根、集号、source file、目标组范围与辅助上下文只读说明 |
| 每个目标普通分镜组是否按 `## x-y-z` 唯一识别，三段式 `group_id` 未被四段式分镜号、连接件或正文关键词替代？ | `GATE-SBVID-02` | `FAIL-SBVID-GROUP` | `N3-GROUP-INDEX` | group index 包含 `group_id`、heading、line range 或 `source_body_hash` |
| `## x-y-z~x-y-z` 连接件是否完全排除在 `group_content`、prompt、storyboard manifest、batch 和视频命名之外？ | `GATE-SBVID-02` | `FAIL-SBVID-GROUP` | `N3-GROUP-INDEX` | group index 记录 connector headings ignored，prompt / batch 无连接件 ID |
| `group_content` 是否从组标题后完整保留到下一个普通组、连接件或文件结尾之前，没有截断、吞并下一组或漏掉正文？ | `GATE-SBVID-03` | `FAIL-SBVID-PROMPT` | `N3-GROUP-INDEX` | source line range、body hash、prompt package 可回放完整组正文 |
| 组底 fenced YAML 是否只作为审查和报告证据保留，而没有替代完整组正文成为视频 prompt 主体？ | `GATE-SBVID-03` | `FAIL-SBVID-PROMPT` | `N3-GROUP-INDEX` / `N5-YAML` | prompt package 以原 `## group_id` 与完整正文起笔，YAML 不单独取代正文 |
| `duration_estimate_seconds` 是否按组底 `时长估算` 优先、分镜秒数求和次之、明确 fallback 最后的顺序生成？ | `GATE-SBVID-04` | `FAIL-SBVID-DURATION` | `N3-GROUP-INDEX` | group index 记录 `duration_source`、原始时长文本、估算值与 fallback 原因 |
| 连接件时长是否没有参与普通分镜组的 `duration_estimate_seconds`，且 `duration_hint` 后续按 4-15 秒 clamp？ | `GATE-SBVID-04` | `FAIL-SBVID-DURATION` | `N3-GROUP-INDEX` / `N5-YAML` | duration evidence 显示连接件排除，batch 中 `duration_hint=clamp(...)` |
| `source_shot_labels` / `shot_count` 是否只做统计证据，无法确认时标记 `shot_count_unverified`，没有因此改写原组正文？ | `GATE-SBVID-02` | `FAIL-SBVID-GROUP` | `N3-GROUP-INDEX` | group index 记录 `source_shot_labels`、`shot_count` 或 `shot_count_unverified` |
| `prompt.md` 是否默认不另起故事板参照说明段，只在 final fenced YAML 的 `故事板参照` 对象注入真实槽位字段？ | `GATE-SBVID-08` | `FAIL-SBVID-PROMPT` | `N5-YAML` / `N7-DISPATCH` | draft / final prompt 对照，final fenced YAML 含真实 `reference_index / uploaded_url / image_token` |
| prompt 主体是否没有摘要、压缩、改写剧情事实、对白事实、镜头顺序、角色关系、场景结果或组边界？ | `GATE-SBVID-11` | `FAIL-SBVID-FIDELITY` | `N5-YAML` / `N6-REVIEW` | prompt package 与 source hash / excerpt 对照；若压缩，报告用户授权或硬限制依据 |
| step1 readiness 是否留下可复核证据，而不是只给出“已提取”结论？ | `GATE-SBVID-15` | `FAIL-SBVID-REPORT` | `N11-CLOSE` | 执行报告列出 source file、唯一命中、line/hash、duration source、connector ignored、返工入口 |
