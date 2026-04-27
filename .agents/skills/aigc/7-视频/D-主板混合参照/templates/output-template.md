# Output Template: D-主板混合参照

## Output Contract Alignment

| Output Contract field | Template mapping |
| --- | --- |
| Required output | prompt 包、混合参照 manifest、Dreamina submit plan、queue ledger、results、执行报告 |
| Output format | Markdown + JSON + queue Markdown + MP4 |
| Output path | `projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/` |
| Naming convention | 使用 `第N集-主板混合参照-video-prompts.md`、`第N集-reference-manifest.json`、`第N集-dreamina-submit-plan.json` 等命名 |
| Completion gate | 固定开头、故事板总参照、主体后缀参照、Dreamina plan、queue/report 均通过 review |

## Runtime Layout

```text
projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/
├── 第N集-hybrid-group-index.json
├── 第N集-主板混合参照-video-prompts.md
├── 第N集-reference-manifest.json
├── 第N集-dreamina-submit-plan.json
├── 第N集-dreamina-queue.md
├── 第N集-dreamina-results.json
├── 执行报告.md
├── prompts/
│   └── <group_id>.txt
└── videos/
    └── <group_id>.mp4
```

## Prompt Block

```markdown
## <group_id>

请参考故事板总参照图作为本分镜组的整体构图、镜头顺序、角色站位、场景连续性与情绪节奏参考；不要把故事板参照当作单一首帧。后文每个主体名称后的 @参照图 用于锁定对应角色、场景或道具外观，不得互相替换。根据以下完整分镜组内容生成一条连续视频。保持分镜顺序、角色动作、镜头运动、场景与情绪连续；不生成字幕，不生成BGM，保留物理互动音效与环境音。

故事板总参照：@图1 -> <storyboard_path 或 缺失说明>

主体参照：
- 角色：<name> @图2（<path>）
- 场景：<name> @图3（<path>）
- 道具：<name> @图4（<path>）

<完整 4-分组组正文>
```

## Report Block

```markdown
# 第N集 D-主板混合参照执行报告

## Verdict

- verdict:
- processed_groups:
- submitted:
- skipped:
- failed:

## Reference Summary

| group_id | storyboard | subjects_bound | missing | over_limit |
| --- | --- | --- | --- | --- |

## Queue Summary

| group_id | submit_id | local_status | remote_status | next_action |
| --- | --- | --- | --- | --- |
```
