# Subject Reference Binding Contract

本文件承接旧 `2-参照引用` 的核心语义，并将其特化为主体识别向绑定，负责 `reference-binding/` 段。

## Scope

- 输入是 `distill/` 段生成的稳定组级 request JSON，或兼容迁移时旧 `全能参照` 的稳定 request JSON。
- 绑定资产只允许来自 `projects/aigc/<项目名>/Assets/`。
- 本段不生成、挑选、移动或重命名图片资产。

## Subject Taxonomy

| subject_type | source signals | preferred directories | binding role |
| --- | --- | --- | --- |
| `character` | `主体锚定.角色`、`出场角色及穿搭`、镜级动作主体 | `Assets/角色/` | 角色身份锚点 |
| `costume` | `出场角色及穿搭`、服装描述、角色状态 | `Assets/服装/` | 角色外观连续性 |
| `prop` | `主体锚定.道具`、镜级道具及状态、动作承载物 | `Assets/道具/` | 可见物件与动作锚点 |
| `scene` | `主体锚定.场景`、空间描写、组级环境 | `Assets/场景/` | 场景空间锚点 |
| `storyboard_support` | `meta.group_id`、`meta.source_shot_ids[]` | `Assets/分镜画板/分镜故事板/`、`Assets/分镜画板/分镜帧/` | 只作为辅助连续性，不作为主体第一锚点 |

## Subject Index Policy

- `subject-index.json` 必须列出每个主体的 `subject_id`、`subject_type`、`label`、`source_shot_ids`、`source_fields`、`priority` 与 `asset_candidates`。
- 主体必须能回链到 `3-Detail` 中的主体锚定、组级穿搭、镜级动作或可见物。
- 不得把风格词、情绪词、镜头术语或 provider 参数列为主体。
- 对同一主体的角色与服装，应保持可关联但不混成一个资产类型。
- 只有稳定出现、视觉上可识别、对视频一致性有价值的对象才进入主体索引；一次性背景碎片可留在 prompt，不必强行建主体。

## Binding Policy

- 未命中资产不是失败；保持空数组或跳过该主体，并在报告中说明。
- 同一候选出现多个同分最高匹配时，必须阻断，不得猜测性选取。
- 所有路径必须真实存在，且位于当前项目 `Assets/` 内。
- 绑定顺序默认是角色、服装、道具、场景、辅助故事板。
- 每个 marker 固定为 `image_ref + ref_kind + related_subject + image_no`。
- `related_subject` 应写入主体标签或 `subject_id`，不得只写模糊的 `图像参考`。
- `reference_images` 与 `image_markers` 必须一一对应，`image_no` 严格递增为 `图1..图N`。

## Binding Output

- `reference-binding/subject-index.json`
- `reference-binding/subject-report.md`
- `reference-binding/<episode_id>.json`
- `reference-binding/_manifest.json`
- `reference-binding/subject-match-report.md`

报告必须写清：

- 已识别主体及来源
- 已绑定资产及依据
- 未命中且可跳过的主体
- 歧义失败与候选列表
- 最终 `validation_status`
