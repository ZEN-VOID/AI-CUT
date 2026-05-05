# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 组级视频 prompt 包、镜级分镜画面参照 manifest、LibTV batch YAML、`*-libtv-submission.txt`、queue ledger、submit/result JSON、逐集执行报告和可选视频文件 |
| Output format | Markdown prompt / report / queue ledger + YAML batch config + LibTV submission text + JSON manifest / result + MP4 |
| Output path | `projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/` |
| Naming convention | episode 保留 `第N集`；job 和视频用 `<分镜组ID>`；远端提交文本为 `prompts/<分镜组ID>-libtv-submission.txt`；技能 id 为 `aigc-video-frame-visual-reference` |
| Completion gate | `validate_skill_2_0.py` 通过；有分镜画面图时 `*-libtv-submission.txt` 首段默认锁定 `modeType=image2video`，首尾帧显式任务才允许 `frames2video`；当前 mode 的 review verdict 为 `pass` 或 `pass_with_todo` |

## Runtime Tree

```text
projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/
├── 第N集-group-shot-index.json
├── 第N集-video-prompts.md
├── 第N集-reference-manifest.json
├── 第N集-libtv-batch.yaml
├── 第N集-libtv-queue.md
├── 第N集-libtv-results.json
├── 执行报告.md
├── prompts/
│   └── <分镜组ID>-libtv-submission.txt
└── <分镜组ID>.mp4
```

## Final Response Shape

- mode:
- source_root:
- frame_reference_root:
- output_root:
- completed_artifacts:
- submitted_jobs:
- querying_jobs:
- downloaded_jobs:
- failed_or_skipped:
- validation:
- next_entry:
- residual_todo:
