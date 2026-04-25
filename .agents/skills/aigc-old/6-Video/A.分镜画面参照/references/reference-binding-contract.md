# Reference Binding Contract

本文件承接旧 `2-参照引用` 的核心语义，负责 `reference-binding/` 段。

## Ownership

`reference-binding/` 拥有：

- 从 `Assets/` 到 `reference_images / image_markers` 的绑定规则。
- 自动匹配、保守跳过、歧义阻断的判定。
- 绑定后三件套和严格校验。
- `图1..图N` 顺序位稳定性。

`reference-binding/` 不拥有：

- 重新改写 distill prompt 或 `3-Detail` 事实。
- 在 `Assets/` 中生成、下载、移动或重命名图片。
- 直接把绑定结果转换成 provider 命令。

## Inputs

- `distill/<episode>.json` 或兼容旧链路请求 JSON。
- `projects/aigc/<项目名>/3-Detail/<episode>.json`
- `projects/aigc/<项目名>/Assets/`

## Matching Policy

| 线索类型 | 目标目录 | 说明 |
| --- | --- | --- |
| `shot_id` | `Assets/分镜画板/分镜帧/` | 首帧/单镜画面参考，默认最高优先级 |
| `group_id` | `Assets/分镜画板/分镜故事板/`、`Assets/分镜画板/漫画/` | 仅作为所属组空气层或缺少帧图时的辅助候选 |
| `角色名` | `Assets/角色/` | 角色身份锚点 |
| `角色-服装锚点` | `Assets/服装/` | 服装视觉锚点 |

Conservative rules:

- 无命中不是失败；可输出空数组并说明跳过。
- 多个同分候选是硬失败，不得猜测性选择。
- 绑定路径必须真实存在，并位于当前项目 `Assets/` 内。
- 绑定顺序稳定：帧级画板资产 -> 组级辅助画板资产 -> 角色资产 -> 服装资产。
- 若输入仍有旧 `image_url` 骨架，本段必须重建为 `image_ref + ref_kind + related_subject + image_no`。

## Output

- `reference-binding/<episode>.json`
- `reference-binding/_manifest.json`
- `reference-binding/match-report.md`

最低通过标准：

- `reference_images` 与 `image_markers` 长度一致。
- 所有 marker 包含 `image_ref / ref_kind / related_subject / image_no`。
- `ref_kind` 固定为 `local_path`。
- 若无真实匹配，两数组为空，不残留占位。
- 报告写清“已绑定 / 未命中可跳过 / 歧义失败”。
