# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件定义 `B-分镜故事板` 的任务分型和 route。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `storyboard_sheet_default` | `types/storyboard-sheet-default.md` | B-分镜故事板所有组级 storyboard sheet 任务 | fallback | `types/storyboard-sheet-default.md` | none | none |

## Default Package Rule

默认加载 `types/storyboard-sheet-default.md`。生成、修复或审查时再按 mode 额外读取 `steps/storyboard-sheet-workflow.md`、`review/review-contract.md` 或 provider handoff 合同。

## Loading Flow

1. 锁定 `target_scope`、`execution_intent`、`source_state` 与 `frame_unit_state`。
2. 加载默认包 `types/storyboard-sheet-default.md`。
3. 将类型画像交给 `steps/storyboard-sheet-workflow.md`。
4. 生成前检查主体参照、场景锚定和 imagegen route；审查时加载 `review/review-contract.md`。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `target_scope` | `single_group / group_batch / episode_batch / review_existing` | 处理范围 |
| `execution_intent` | `prompt_only / generate / repair / review_only` | 是否执行 imagegen |
| `source_state` | `group_source_ready / group_source_partial / group_source_missing` | `6-分组` 可用性 |
| `frame_unit_state` | `frame_units_ready / frame_units_partial / frame_units_missing` | storyboard panel 落点是否已基于视觉节拍识别 |
| `reference_state` | `all_bound / partial_missing / no_assets / ambiguous` | 主体参照状态 |
| `scene_visual_state` | `scene_anchor_bound / scene_anchor_missing / no_scene_reference` | 场景参照图是否承担风格、光影、氛围锚定 |
| `imagegen_route` | `built_in / cli_confirmed / blocked` | imagegen 路由 |

## Mode Matrix

| type profile | mode | route |
| --- | --- | --- |
| `single_group + generate + group_source_ready` | `single_group_generate` | `steps/storyboard-sheet-workflow.md` 的 N3-N3A-N8 |
| `episode_batch + generate + group_source_ready` | `episode_batch_generate` | `N3-N3A-N8` with group-level sequential or controlled batch dispatch |
| `group_batch + generate + group_source_ready` | `group_batch_generate` | `N3-N3A-N8` for selected groups |
| `* + prompt_only + group_source_ready` | `prompt_only` | `N3-N6, N9-N10` |
| `review_existing + review_only` | `review_only` | `review/review-contract.md` |
| `* + repair` | `repair` | route to owning failed section |
| `* + group_source_missing` | block | ask user to provide/fix source |
| `* + frame_units_missing` | block | return to `references/group-source-extraction.md#storyboard-frame-unit-derivation` |

## Reroute Rules

- 单一四段式 `分镜ID` 或单帧画面请求：转 `A-分镜画面`。
- 漫画页、气泡文字、阅读顺序或漫画分镜页：转 repo-local `comic` workflow。
- 视频生成前故事板参照：转 `9-视频/B-分镜故事板参照`。
- 需要重写 `6-分组` 内容：转 `6-分组` 修复，不在本技能内改写。

## Gate

进入 `generate` 前必须同时满足：

1. `source_state != group_source_missing`。
2. `frame_unit_state == frame_units_ready`；若为 `frame_units_partial`，必须先人工确认或报告 prompt-only 风险，不得直接生成。
3. `imagegen_route == built_in`，除非用户显式确认 CLI/API fallback。
4. `reference_state != ambiguous`，除非 ambiguous 条目已被移除或用户确认。
5. 若存在场景参照图，`scene_visual_state == scene_anchor_bound`。
6. 输出路径位于项目内 `8-图像/B-分镜故事板`。
