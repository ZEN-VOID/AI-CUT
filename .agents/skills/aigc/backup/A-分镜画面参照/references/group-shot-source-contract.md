# Group Shot Source Contract

本文件定义 step1：以 `projects/aigc/<项目名>/5-分组` 为主要信息来源，获取每个分镜组的完整内容，并把组内镜头映射为四段式 `分镜ID`。

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
- `8-视频/A-分镜画面参照` 默认完全忽略连接件块：不进入 `group_content`、四段式 `shot_id` 映射、视频 prompt、reference manifest、LibTV batch 或视频文件命名。
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
source_file: "projects/aigc/<项目名>/5-分组/第1集.md"
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
- 对有图的镜头，唯一允许改写源文本的位置是 fenced YAML：draft 阶段不写 `reference_index / uploaded_url`；final 阶段新增或更新 `分镜画面参照` 列表，写入 `reference_index / shot_id / source_label / uploaded_url / image_token`；不得用 `shot_id@path`、`@图N` 或另起参照说明段作为远端真源。
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
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `5-分组` 修复 |
| group_content 被截断 | 重新按下一个二级标题定位边界 |
| 连接件进入 group_content 或 prompt | 按 `## x-y-z~x-y-z` 重新切块并忽略连接件 |
| 组正文被摘要或改写 | 回到本合同，恢复完整现有内容 |
| `分镜N` 与四段式 ID 对不上 | 优先使用已提供的 `分镜ID`，并在 index 中记录映射依据 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 目标输入是否固定读取 `projects/aigc/<项目名>/5-分组/第N集.md`，且项目 `MEMORY.md` / `CONTEXT/` 没有覆盖分镜组正文？ | `GATE-FVID-GROUP-01` | `FAIL-FVID-INPUT` | `N3-GROUP-INDEX` | input manifest 记录 `source_file`、episode、target `group_id` 与辅助上下文使用说明 |
| 普通分镜组与连接件是否按二级标题精确切分，`## x-y-z~x-y-z` 连接件没有进入 `group_content`、prompt、manifest、batch 或视频命名？ | `GATE-FVID-GROUP-02` | `FAIL-FVID-GROUP-BOUNDARY` | `N3-GROUP-INDEX` | group index 记录 heading、line range/hash 与 ignored connector list |
| `group_content` 是否完整保留标题后的现有组正文，而不是底部 YAML、摘要、压缩版或重写版？ | `GATE-FVID-GROUP-03` | `FAIL-FVID-PROMPT` | `N3-GROUP-INDEX` | prompt package 以原 `## group_id` 起笔，并保留 `source_body_hash` |
| 组内 `分镜N` / `分镜 N` / 已有四段式 `分镜ID` 是否稳定映射为唯一 `shot_id`，四段式用户输入是否能回推所属 `group_id`？ | `GATE-FVID-SHOT-01` | `FAIL-FVID-SHOT-ID` | `N4-SHOT-ID` | `group-shot-index.json` 列出 `shot_id`、`source_label`、`group_id` 与映射依据 |
| `duration_estimate_seconds` 是否按组底 `时长估算`、组内秒数求和、明确 fallback 的顺序生成，且连接件时长没有参与组级估算？ | `GATE-FVID-DURATION-01` | `FAIL-FVID-DURATION` | `N3-GROUP-INDEX` | `duration_source`、原文时长证据、`duration_estimate_seconds` 与 fallback reason |
| LibTV prompt 主体是否没有改写剧情事实、对白事实、镜头顺序、角色关系、场景结果或组边界，且未在无用户授权时压缩？ | `GATE-FVID-PROMPT-01` | `FAIL-FVID-PROMPT` | `N6-YAML` | source-first prompt、原组正文 hash 对照、compression opt-in 或 hard-limit 记录 |
| 有图镜头的参照绑定是否只在 final fenced YAML 的 `分镜画面参照[]` 注入 `reference_index / shot_id / source_label / uploaded_url / image_token`，draft 阶段不伪造 URL，也不使用 `shot_id@path`、`@图N` 或另起参照说明段作为远端真源？ | `GATE-FVID-PROMPT-02` | `FAIL-FVID-PROMPT` | `N6-YAML` | draft/final YAML diff、`*-libtv-submission.txt` 截要、slot ledger |
| step1 readiness 是否能回放：`source_file` 可读、目标 `group_id` 唯一、`group_content` 非空、每个 `shot_id` 可回指源组和源标签？ | `GATE-FVID-REPORT-01` | `FAIL-FVID-REPORT` | `N12-CLOSE` | 执行报告列出 group source coverage、unresolved `shot_id`、rework entry |
