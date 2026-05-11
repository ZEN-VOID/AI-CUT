# Context: aigc-image-storyboard-sheet

本文件是 `B-分镜故事板` 的经验层知识库，不是执行日志。它用于沉淀从 `4-分组` 生成组级多格 storyboard 时的类型判断、修复打法和可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-group-storyboard-specific
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-SHEET-01` | prompt 像单帧画面而不是多格 storyboard | prompt object boundary | 恢复固定英文开头，并保留完整组正文 | 在 `prompt-assembly-contract.md` 固化组级边界 | prompt 第一行即声明 multi-panel storyboard |
| `TM-SHEET-02` | 绑定了正文泛称主体而不是 YAML 主体 | subject source drift | 只消费组底 YAML 的 `角色 / 场景 / 道具` | reference gate 检查 `source: group_yaml` | manifest 中每个主体可回指 YAML |
| `TM-SHEET-03` | 有多视图图却绑定到主图 | asset priority drift | 重新扫描同名 `-多视图` 图片 | 在绑定规则中固定多视图优先 | bound 条目记录 `selected_variant: multi_view` |
| `TM-SHEET-04` | 只有 JSON 没有 PNG/JPEG/WebP 却被视为可参照 | asset existence drift | 将该主体列入 missing 并移除参照槽位 | binding gate 要求真实图片存在 | 所有 bound path 均存在且为图片 |
| `TM-SHEET-05` | 批量执行覆盖同一输出文件 | execution boundary | 一组一文件，已有文件按 rerun 策略处理 | imagegen plan 固定 group_id 级写锁 | `images/<group_id>.png` 无多任务冲突 |
| `TM-SHEET-06` | 组正文被摘要导致镜头缺失 | source fidelity | 使用原组正文作为 prompt 主体，不做压缩 | review 检查分镜编号完整性 | 分镜1..N 均出现在 prompt 主体 |
| `TM-SHEET-07` | 本地参照图只写入路径但未进入对话上下文 | imagegen source semantics | 生成前逐张 `view_image` 已绑定本地图片并标注角色 | 在 handoff 与 review gate 固化 `view_image` 前置门禁 | results/report 记录 `reference_input_status: visible_in_conversation_context` |
| `TM-SHEET-08` | storyboard 每格被机械映射成原文 `分镜1`、`分镜2` | panel mapping drift | 重建 `storyboard_frame_units`，按当前分组正文中的视觉节拍判断 panel 落点 | group extraction 与 prompt gate 固化 frame-unit plan | 每个 panel 有 `source_span`，且允许 split/merge |
| `TM-SHEET-09` | 成图只像全局风格，不像场景参照图的光影氛围 | scene visual anchor missing | 在场景绑定、prompt 和 imagegen plan 中加入 `style_lighting_atmosphere` 锚定 | reference 与 review gate 固化场景图双重职责 | manifest/prompt/plan 均记录 scene visual anchor |
| `TM-SHEET-10` | 分镜故事板 2K 出图导致单个 panel 细节不清晰 | resolution target too low | 将 prompt、plan、result 的 `resolution_target` 统一改为 `4K` | imagegen handoff 与 review gate 固化 4K 默认 | prompt / plan / report 均记录 4K |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、主体参照、imagegen handoff、输出持久化还是报告闭环。
2. 若 `group_id` 不唯一或组正文截断，回到 `references/group-source-extraction.md` 重新建立 `group-index.json`。
3. 若固定开头不是用户指定文本，回到 `references/prompt-assembly-contract.md` 重写 prompt 包。
4. 若主体来自正文而非 YAML，清空该轮绑定，重新从 fenced YAML 建立 subject list。
5. 若存在 `-多视图.png|jpg|jpeg|webp`，不得退到 `-主图`。
6. 若只有 `.json` 设计稿而无图片，主体应进入 `missing`，不要保留空字符串路径。
7. 若批量 imagegen 部分失败，保留成功结果，报告失败组与可重试命令，不回滚成功图片。
8. 若镜头数过多导致单图完整性风险，优先报告分页/分批建议；没有用户确认前不要擅自拆分 canonical 组。
9. built-in `image_gen` 使用本地参照图时，路径记录不够；必须先 `view_image` 让图片进入对话上下文。确无绑定图片时才记录 `reference_input_status: no_reference_images_bound` 并走 text-prompt-only。
10. 若 panel 数与原始 `分镜N` 标签数不一致，不是错误；只要 `storyboard_frame_units` 能回指源正文，就按 frame units 生成。
11. 若绑定场景图，必须把它视为空间、风格、光影、氛围的综合参照；只写全局风格文字不足以约束 storyboard 整体画面。
12. 多格 storyboard 不适合沿用 2K 默认；即便单组 frame units 不多，也按 4K 固定生成，避免后续放大审片时 panel 不清晰。

## Reusable Heuristics

- `B-分镜故事板` 的核心对象是 `group_id`，不是四段式单镜 `shot_id`。
- `source_shot_labels` 是运镜中心结果的追溯标签，`storyboard_frame_units` 才是多格 storyboard 的 panel 落点。
- `4-分组` 已经包含足够的组级风格、场景、分镜明细和入出场信息；本技能不需要重新蒸馏上游剧情。
- 组底 YAML 是主体参照绑定的唯一默认入口；正文中出现的普通名词不自动变成参照对象。
- 多格 storyboard 的固定英文开头必须足够明确，否则生图模型容易把它当成单张电影 still。
- 分镜故事板默认 4K 出图；2K 是单格可读性风险，不作为本技能可接受默认值。
- 场景参照图是 storyboard 整体风格、光影、氛围的一致性锚点；全局风格文字锁定只是辅助手段。
- 缺图不是阻塞 prompt 的理由，但必须阻塞“伪绑定”；空槽位应移除或进入 missing。
- 批量生成默认是计划层能力，不等于后台并行执行；索引、prompt 包、manifest 和报告应统一汇流写入。
- 已绑定本地参照图必须在生成前通过 `view_image` 可见化；否则只能算路径证据，不能算已传入视觉参照。
