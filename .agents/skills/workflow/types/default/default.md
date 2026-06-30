# Workflow Default Type Package

本文件是 `types/type-map.md` 的默认判型展开，不是独立路由真源。

## Route Tie-Break

| condition | preferred_route | reason |
| --- | --- | --- |
| 命中 workflow 且有内容、主时钟和素材池，用户未明确禁止渲染 | `full_hyperframes_edit` | workflow 普通完成态是最终成片 |
| 命中 workflow 且用户未指定输出目录 | 对应 route + `work_root=projects/output/<日期>/过程/<project-slug>/` + `single_final_root=projects/output/<日期>/` | 过程文件进入 `过程/`，单条 final 进入日期输出根 |
| 命中 workflow 批量成片任务 | 对应 route + `batch_root=projects/output/<日期>/过程/<batch-id>/` + `final_collection_root=projects/output/<日期>/成片/` | 批量过程文件和 final 分层，方便查看和交付 |
| 输入素材来自 `projects/素材/` 或 `projects/示例/` | source pool read-only | 两个目录是可累积通用素材池，不是当日内置素材或输出目录 |
| 命中 workflow 且用户未指定比例 | `full_hyperframes_edit` + `aspect_ratio=16:9` | workflow 普通视频默认 16:9、1920x1080 |
| 命中 workflow 且包含台词字幕 | `full_hyperframes_edit` + `dialogue_sync_validator=required` | 台词字幕 final 前必须通过机械同步校验 |
| 素材或参考样片为竖屏，但用户未明确要求竖屏输出 | `full_hyperframes_edit` + `aspect_ratio=16:9` | 竖屏素材只作构图证据，不改变默认输出比例 |
| 用户明确要求竖屏、短视频平台竖版、或项目真源已锁定其他尺寸 | 对应 route + 显式 `aspect_ratio` | 用户/项目规格覆盖默认 16:9，必须在 intake/report 记录依据 |
| 用户明确要求先看工程、预览或不要渲染 | `hyperframes_project_build` | 用户显式 no-render 覆盖默认 final 目标 |
| 用户要求 PRP、方案、storyboard | `plan_only` | 输出计划，不进入 author/render |
| 用户指出字幕/旁白错位 | `repair_dialogue_timing` | 主时钟优先于视觉修复 |
| 用户指出遮挡、黑屏、素材不贴、动效问题 | `repair_visual_composition` 或 `audit_existing` | 先根据是否允许写回裁决 |
| 用户只要求理解素材 | `asset_evidence_only` | 不创建 final 工程 |

## Downgrade Rules

- 缺音频主时钟且无 TTS 授权：默认请求补充音频或 TTS 授权；不得无声降级后宣称 workflow 完成。
- 缺源素材且无生成/抓取授权：project build 降级为 plan-only。
- 只有 final MP4 且无工程/素材：repair 降级为 audit-existing。
- CLI 不可用：full render 降级为 project/report，并报告阻断。
- 非 16:9 输出缺用户/项目显式依据：回到 N1/N6 改为 1920x1080，或补充合法豁免证据后再继续。
- 台词字幕缺 `caption_type`、逐 cue `audio_anchor`、脚本锚点或 validator fail：回到 `repair_dialogue_timing`，不能用总时长手工切分继续 C7。
- 输出误落到 `projects/素材/` 或 `projects/示例/`：回到 `N1/N9`，过程文件改用 `projects/output/<日期>/过程/`，final 改用 `projects/output/<日期>/` 或用户显式指定目录。
- 过程文件散落在 `projects/output/<日期>/` 日期根：回到 `N1/N9`，统一移动到 `projects/output/<日期>/过程/` 并同步报告、ledger 或 path map。
- 批量 final 未归集到 `projects/output/<日期>/成片/`：回到 `N9` 移动/归集 final，并同步 execution report 与 `asset_usage_ledger.json.final_path`。
