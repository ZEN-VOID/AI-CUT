# 道具生成执行报告

project: `projects/aigc/<项目名>`
output_dir: `projects/aigc/<项目名>/5-设计/道具/3-生成`

## 生成资产

| 主体 | 上游设计文档 | 主图 | 主图 JSON | 多视图 | 多视图 JSON | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `<主体名称>` | `5-设计/道具/2-设计/<主体名称>.md` | `<主体名称>-主图.png` | `<主体名称>-主图.json` | `<主体名称>-多视图.png` | `<主体名称>-多视图.json` | `pending` |

## Subagent Status

```yaml
worker: Worker-道具生成
reviewer: ""
subagent_status: real_subagent | tool_blocked_local_review | not_requested
degradation:
  blocker_layer: ""
  original_path: ""
  fallback_path: ""
  not_started: []
tool_blocker: ""
```

## Review Verdict

```yaml
verdict: pass | pass_with_followups | needs_rework | blocked
checked_at: ""
findings: []
next_action: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 每个主体一张单主体图、一个单主体 JSON、一张多视图主体设计图、一个多视图 JSON。 |
| Output format | 图像资产为 PNG/JPEG/WebP；提示词为 JSON；执行报告为 Markdown。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/5-设计/道具/3-生成/`。 |
| Naming convention | 单体图 `主体名称-主图`；多视图 `主体名称-多视图`；JSON 与对应图像同 stem。 |
| Completion gate | 每组资产回指上游 `2-设计` 文档，主图引用“提示词设计”，多视图引用主图，已完成 review verdict。 |
