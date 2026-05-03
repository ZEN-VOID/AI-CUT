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
- 一个分镜组从该标题开始，到下一个 `## x-y-z` 或文件结尾前结束。
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
group_content: "<从标题后到下一个组标题前的现有完整内容>"
source_body_hash: "<sha256>"
shots:
  - shot_id: "1-1-1-1"
    source_label: "分镜1"
    line_hint: 0
    reference_annotation: "1-1-1-1"
```

## Prompt Body Rule

- `group_content` 是 LibTV prompt 的主体，不得摘要替代。
- 允许在 `group_content` 前添加固定视频生成约束和参照图说明。
- 对有图的镜头，prompt 的参照映射层必须表达为 `shot_id@path`，再投影到 LibTV `@图N`。
- 不得改写剧情事实、对白事实、镜头顺序、角色关系、场景结果或组边界。
- 如需压缩，只能在用户明确要求或 LibTV 硬限制触发时执行，并必须记录压缩依据与被压缩字段；默认不压缩。

## Readiness Gate

通过 step1 必须满足：

1. `source_file` 存在且可读。
2. 每个目标 `group_id` 唯一出现。
3. `group_content` 非空。
4. 每个目标 `shot_id` 可回指源组和组内标签；无法解析时标记 `shot_id_unresolved` 并阻断该镜参照绑定。
5. 输出 group-shot index 记录 source file、heading、line range 或 hash，便于回放。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `4-分组` 修复 |
| group_content 被截断 | 重新按下一个二级标题定位边界 |
| 组正文被摘要或改写 | 回到本合同，恢复完整现有内容 |
| `分镜N` 与四段式 ID 对不上 | 优先使用已提供的 `分镜ID`，并在 index 中记录映射依据 |
