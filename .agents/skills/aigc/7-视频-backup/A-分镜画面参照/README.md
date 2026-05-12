# A-分镜画面参照

`7-视频` Skill 2.0 包：从 `4-分组` 读取完整分镜组内容，把组内分镜映射为四段式 `分镜ID`，按 `shot_id` 绑定 `6-图像/A-分镜画面` 的可选镜级图，并通过 $libTV skill scripts 批量生成组级多图参照视频。

## Directory Tree

```text
A-分镜画面参照/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

- 技能目录：`.agents/skills/aigc/7-视频-backup/A-分镜画面参照/`
- 主要输入：`projects/aigc/<项目名>/4-分组/第N集.md`
- 分镜画面参照：`projects/aigc/<项目名>/6-图像/A-分镜画面/第N集/images/<分镜ID>.*`
- 项目输出根：`projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/`
- 主要模式：`prompt_only`、`single_group_generate`、`episode_batch_generate`、`group_batch_generate`、`shot_batch_generate`、`query_or_download`、`repair`、`review_only`

```mermaid
flowchart LR
    A["4-分组"] --> B["A-分镜画面参照"]
    C["6-图像/A-分镜画面"] --> B
    B --> D["$libTV"]
    D --> E["7-视频/A-分镜画面参照/videos"]
```

## Runtime Artifacts

```text
第N集-group-shot-index.json
第N集-video-prompts.md
第N集-reference-manifest.json
第N集-libtv-batch.yaml
第N集-libtv-queue.md
第N集-libtv-results.json
执行报告.md
<分镜组ID>.mp4
```
