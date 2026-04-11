# 分镜故事板思维链细则

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SB-SHEET-01 | `prompt_style.type / prompt_style.language / prompt_style.char_limit / meta.shot_level / meta.group_id / meta.source_shot_ids` | 以独立 `prompt_style` 声明多格故事板提示词约束，并锁定组级来源与镜头顺序 | S1 | 输入覆盖完整度 | FAIL-SB-SHEET-01 |
| FIELD-SB-SHEET-02 | `prompt / prompt_char_count` | prompt 必须由固定英文前缀与完整 `storyboard_group` 内容块组成，且字数统计位于顶层 | S2-S3 | Prompt 蒸馏稳定性 | FAIL-SB-SHEET-02 |
| FIELD-SB-SHEET-03 | `model.model_version / model.ratio / model.image_size / model.output_format / model.num_images / model.reference_images / model.image_markers` | `model` 必须保持图像侧模板骨架完整；无图时也保留参照槽位 | S4 | 模板兼容性 | FAIL-SB-SHEET-03 |
| FIELD-SB-SHEET-04 | `第N集.json / _manifest.json` | 输出文件可追溯、可继续 handoff 给后续一致性处理与图像生成 | S5 | 输出可消费性 | FAIL-SB-SHEET-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SB-SHEET-01 | 当前目标分镜组是谁，组内镜头顺序是否稳定 | 锁定 `prompt_style + shot_level + group_id + source_shot_ids` | 组定位冲突或镜头顺序缺失 |
| S2 | FIELD-SB-SHEET-02 | `storyboard_group` 需要覆盖哪些上游字段 | 提取 `剧本正文 + 组间设计 + 全部 分镜明细[]` | 漏掉组级字段或镜级字段 |
| S3 | FIELD-SB-SHEET-02 | prompt 是否严格满足“固定前缀 + storyboard_group” | 逐字保留固定前缀并拼接内容块 | 前缀缺失、顺序错误或额外插入说明 |
| S4 | FIELD-SB-SHEET-03 | 图像请求模板字段是否完整且不虚构参照图 | 保留图像侧参数骨架与参照图槽位 | 删字段、乱序或擅自补图 |
| S5 | FIELD-SB-SHEET-04 | 输出是否已形成可 handoff 的单集 JSON | 写 `第N集.json`，按需补 `_manifest.json` | 仍把图片落盘当主产物或缺少 JSON |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SB-SHEET-01 | `prompt_style.type / meta.shot_level` 合法，且 `group_id` 与有序 `source_shot_ids` 同时成立 | FAIL-SB-SHEET-01 | S1 |
| FIELD-SB-SHEET-02 | prompt 满足固定前缀、完整 `storyboard_group` 与顶层字数统计 | FAIL-SB-SHEET-02 | S2-S3 |
| FIELD-SB-SHEET-03 | 图像侧 `model` 骨架完整，`reference_images` 与 `image_markers` 保持共享模板兼容 | FAIL-SB-SHEET-03 | S4 |
| FIELD-SB-SHEET-04 | `第N集.json` 可追溯可 handoff；若要求 full trace，则 `_manifest.json` 同步成立 | FAIL-SB-SHEET-04 | S5 |
