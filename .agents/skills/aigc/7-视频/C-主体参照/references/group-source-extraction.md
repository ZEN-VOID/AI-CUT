# Group Source Extraction Contract

本文件定义 step1 的输入锁定：以 `projects/aigc/<项目名>/4-分组` 为主要信息来源，获取每个分镜组的完整内容。

## Source Roots

固定读取：

```text
projects/aigc/<项目名>/4-分组/第N集.md
```

辅助上下文可读但不得覆盖组正文：

```text
projects/aigc/<项目名>/MEMORY.md
projects/aigc/<项目名>/CONTEXT/
projects/aigc/<项目名>/0-初始化/north_star.yaml
```

## Group Boundary

- 分镜组标题固定识别为 Markdown 二级标题：`## x-y-z`。
- 一个分镜组从该标题开始，到下一个 `## x-y-z` 或文件结尾前结束。
- 组底 fenced YAML 必须作为该组的结构化主体来源；正文和 YAML 都要保留各自角色，不得互相替代。
- `group_id` 使用三段式模式 `episode-scene-group`，例如 `1-1-1`。

## Extraction Payload

每个组至少输出：

```yaml
group_id: "1-1-1"
episode_id: "第1集"
source_file: "projects/aigc/<项目名>/4-分组/第1集.md"
heading: "## 1-1-1"
group_body: "<从标题后到 YAML 前的现有内容>"
group_yaml:
  字数统计: ""
  角色: []
  场景: []
  道具: []
shot_count: 0
source_shot_labels: []
```

## Video Prompt Source Rule

- `group_body` 是视频 prompt 的主要正文来源。
- 不删除组间连接件、分镜明细、音效、对白、环境描写和表演提示。
- 不把 YAML 合并进正文主段；YAML 只用于 reference manifest 和主体参照说明，其中有图主体必须追加 `@<图片路径>`。
- 若组正文过长，只允许在 LibTV handoff 层做可审查压缩摘要，并保留完整原文路径和原文字数。

## Readiness Gate

通过 step1 必须满足：

1. `source_file` 存在且可读。
2. 每个目标 `group_id` 唯一出现。
3. `group_body` 非空。
4. fenced YAML 可解析，至少能得到 `角色 / 场景 / 道具` 三类字段；缺项可以为空数组但必须记录。
5. `shot_count` 大于 0；若无法自动统计，进入 `partial`，由人工审查确认完整性。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 找不到 `## x-y-z` | 确认集号或 group_id，必要时回上游 `4-分组` 修复 |
| YAML fenced block 缺失 | 阻断参照绑定，允许 prompt-only 并报告 |
| group_body 被截断 | 重新按下一个二级标题定位边界 |
| `分镜N` 统计不完整 | 保留原正文，报告 `shot_count_unverified` |
