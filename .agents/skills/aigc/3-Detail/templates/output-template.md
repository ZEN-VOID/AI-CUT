# 3-Detail Output Template

本模板是 `3-Detail` Output Contract 的渲染层，不拥有独立路径、命名或完成门禁。

## Output Contract Alignment

- Required output: `projects/aigc/<项目名>/3-Detail/第N集.json` 与 `projects/aigc/<项目名>/3-Detail/validation-report.md`。
- Output format: JSON 使用 `_shared/episode_detail.json` 的 `meta + groups[].global/detail` 结构；Markdown 报告使用下方章节。
- Output path: 运行时输出固定写入 `projects/aigc/<项目名>/3-Detail/`。
- Naming convention: 集文件为 `第N集.json`；分镜 ID 使用四段式 `episode-scene-group-frame`，如 `1-1-1-1`；报告固定为 `validation-report.md`。
- Completion gate: `scripts/validate_stage_output.py <第N集.json>` 通过，或在报告中明确写出阻塞、Root-Cause 上溯和下一入口。

## JSON Skeleton

参照 `.agents/skills/aigc/3-Detail/_shared/episode_detail.json`。运行时必须保留：

- `meta.剧名 / 集数 / 组数 / 总时长`
- `groups[].分镜组ID`
- `groups[].global.剧本正文 / 全局风格 / 类型元素 / 导演意图`
- `groups[].detail.分镜数`
- `groups[].detail.分镜列表.<分镜ID>.时间 / 剧本正文 / 主体锚定 / 分镜构图 / 运镜手法 / 角色表现 / 氛围表现 / 摄影表现 / 转场特效`

## validation-report.md Template

```markdown
# 3-Detail Validation Report

## Layered Trace

- episode:
- scope_type:
- field_type:
- source:
- target:
- rework_entry:

## 已执行校验

- command:
- result:
- blocking_errors:

## Academy Knowledge Evidence

- knowledge_mode: applied | unused_with_reason
- knowledge_domain:
- selected_bundles:
- applied_passes:
- translation_targets:

## Thinking-Action Closure

### 思考过程

### 关键证据

### 风险/例外

### 下一入口
```
