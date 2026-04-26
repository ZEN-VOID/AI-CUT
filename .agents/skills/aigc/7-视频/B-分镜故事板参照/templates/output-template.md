# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 组级视频 prompt 包、故事板参照 manifest、Dreamina batch YAML、queue ledger、submit/result JSON、逐集执行报告和可选视频文件 |
| Output format | Markdown prompt / report / queue ledger + YAML batch config + JSON manifest / result + MP4 |
| Output path | `projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/` |
| Naming convention | episode 保留 `第N集`；job 和视频用 `<分镜组ID>`；技能 id 为 `aigc-video-storyboard-reference` |
| Completion gate | `validate_skill_2_0.py` 通过；当前 mode 的 review verdict 为 `pass` 或 `pass_with_todo` |

## Runtime Tree

```text
projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/
├── 第N集-group-index.json
├── 第N集-video-prompts.md
├── 第N集-reference-manifest.json
├── 第N集-dreamina-batch.yaml
├── 第N集-dreamina-queue.md
├── 第N集-dreamina-results.json
├── 执行报告.md
└── videos/
    └── <分镜组ID>.mp4
```

## Final Response Shape

- mode:
- source_root:
- storyboard_reference_root:
- output_root:
- completed_artifacts:
- submitted_jobs:
- querying_jobs:
- downloaded_jobs:
- failed_or_skipped:
- validation:
- next_entry:
- residual_todo:
