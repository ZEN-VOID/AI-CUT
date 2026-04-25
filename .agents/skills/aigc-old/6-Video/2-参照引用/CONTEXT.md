# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-Video/2-参照引用` 的经验层知识库，不是过程日志。
- 调用本技能时，应在父级 `6-Video` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `Assets/` 中明明有图，但请求对象仍保持空数组 | 候选推导层 | 回查 `group_id / shot_id / 出场角色及穿搭` 是否成功转成候选请求 | 在脚本固定“画板优先、角色/服装其次”的候选生成顺序 | `_manifest.json` 能看到候选与绑定数 |
| 同一 token 命中多个高分候选，被误选为其中一个 | 歧义裁决层 | 停止自动绑定并在报告中记为 `ambiguous` | 在脚本里把“同分最高候选”固定为硬失败，不允许默选 | `match-report.md` 不再出现猜测性绑定 |
| 绑定结果仍残留旧 `image_url` 骨架 | 模板兼容层 | 在回写前统一重建 `image_markers` 四字段结构 | 固定“本技能输出只使用 `image_ref + ref_kind + related_subject + image_no`” | 输出 JSON 不再混用新旧结构 |
| `reference_images` 中出现外部路径或不存在路径 | 资产边界层 | 只允许 `Assets/` 内真实文件落盘，其他路径全部阻断 | 在严格校验中固定“路径存在 + 位于 Assets 内”双门 | 所有已绑定路径都能真实打开 |
| 没有命中任何资产，但仍保留了占位 marker | 跳过策略层 | 若无真实命中，两个字段都清空 | 在脚本固定“未命中=空数组，不保留占位骨架” | 空绑定 packet 不再带 `<图片引用>` 占位 |
| dry-run 自检时报 `'model'` KeyError | 校验脚本层 | 把严格校验函数的输入从整 packet 修正为 `model` payload，避免层级误取 | 在脚本中固定 `validate_bound_packet(model_payload, ...)` 的签名，不再混淆 packet/model 边界 | `--dry-run` 能稳定跑完空资产和已绑定两类请求对象 |

## Repair Playbook

1. 先查输入请求对象来自 `全能参照` 还是 `首帧参照`。
2. 再查 `3-Detail` 中该 packet 对应的 `group_id / shot_id / 出场角色及穿搭` 是否存在。
3. 再查 `Assets/` 中对应目录是否有文件，并确认文件名是否真的包含结构化 token。
4. 若存在多候选同分，直接阻断，不做猜测性绑定。
5. 回写后复查 `reference_images / image_markers` 长度、顺序与路径真实性。
6. 最后看 `_manifest.json` 与 `match-report.md` 是否能支撑人工复核。

## Reusable Heuristics

- `2-参照引用` 最重要的不是“尽量多绑图”，而是“只绑那些可解释、可验证、可稳定复现的图”。
- 对帧级请求来说，最稳的第一类参照永远是 `Assets/分镜画板/分镜帧/` 中带 `shot_id` 的图片。
- 对组级请求来说，最稳的第一类参照通常是 `Assets/分镜画板/分镜故事板/` 或 `漫画/` 中带 `group_id` 的图片。
- 角色和服装引用要分目录处理：角色身份锚点优先去 `Assets/角色/`，服装锚点优先去 `Assets/服装/`。
- 若 `Assets/` 中没有图，不是失败；若 `Assets/` 中有多张同分候选且无法分辨，才是失败。
- `reference_images` 是 provider 消费顺序位，`image_markers` 是语义解释位；两者必须一一对应，不能各写各的。
