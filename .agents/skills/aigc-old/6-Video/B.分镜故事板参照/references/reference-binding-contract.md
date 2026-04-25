# Reference Binding Contract

本文件承接旧 `2-参照引用` 的核心语义，负责 `reference-binding/` 段的资产绑定与严格校验。

## Scope

- 输入是 `distill/` 段生成的稳定组级 request JSON，或兼容迁移时旧 `全能参照` 的稳定 request JSON。
- 绑定资产只允许来自 `projects/aigc/<项目名>/Assets/`。
- 本段不生成、挑选、移动或重命名图片资产。

## Candidate Priority

| signal | preferred directories | binding role |
| --- | --- | --- |
| `meta.group_id` | `Assets/分镜画板/分镜故事板/`、`Assets/分镜画板/漫画/` | 组级故事板/漫画视觉连续性 |
| `meta.source_shot_ids[]` | `Assets/分镜画板/分镜帧/` | 可选镜级补充锚点 |
| 角色名 | `Assets/角色/` | 角色身份锚点 |
| 角色-服装锚点 | `Assets/服装/` | 服装视觉锚点 |

## Binding Policy

- 未命中资产不是失败；保持空数组并在报告中说明跳过。
- 同一候选出现多个同分最高匹配时，必须阻断，不得猜测性选取。
- 所有路径必须真实存在，且位于当前项目 `Assets/` 内。
- 绑定顺序默认是故事板/漫画、可选分镜帧、角色、服装。
- 每个 marker 固定为 `image_ref + ref_kind + related_subject + image_no`。
- `reference_images` 与 `image_markers` 必须一一对应，`image_no` 严格递增为 `图1..图N`。

## Binding Output

- `reference-binding/<episode_id>.json`
- `reference-binding/_manifest.json`
- `reference-binding/match-report.md`

报告必须写清：

- 已绑定资产及依据
- 未命中且可跳过的候选
- 歧义失败与候选列表
- 最终 `validation_status`
