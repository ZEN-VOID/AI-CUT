# Reference Binding Contract

## Scope

承接组级 storyboard request JSON，把本地真实图片资产绑定到 `reference_images / image_markers`，并输出参照绑定三件套。

## Source Priority

1. 已有 request JSON 中显式 `image_markers[].related_subject`。
2. `分镜组ID` 与 `source_shot_ids` 回链出的组级角色、主空间和关键道具。
3. `projects/aigc/<项目名>/4-Design/` 与 `Assets/` 中可唯一证明的本地图片。
4. 旧 compat `组间设计.出场角色及穿搭` 仅作辅助证据，不覆盖 canonical detail root。

## Conservative Binding Rule

允许绑定：

- 完整角色名，并且资产候选唯一。
- 组级主空间锚点，并且同类候选唯一。
- 完整复合道具名或上游显式 marker。
- 用户显式指定的本地图片路径。

禁止直接绑定：

- 单字、泛词或高复用空间词。
- 子串命中。
- 一个 token 命中多张图片。
- 只靠 prompt 全文泛扫得到的弱候选。

## Required Outputs

- 主 JSON：`第N集.json`
- manifest：`_manifest.json`
- 报告：`match-report.md`

`match-report.md` 必须同时列出：

- `bound_assets`
- `ambiguous_candidates`
- `rejected_candidates`
- 每个候选的 `match_reason / evidence_level / evidence_field / confidence`

## Next Entry

参照绑定三件套必须写出 `next_entry`，指向 `5-Image/3-图像生成` 的 provider handoff。
