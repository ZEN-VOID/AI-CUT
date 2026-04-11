# 首帧参照 思维链细则

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-VID-FFR-01 | `prompt_style.type / prompt_style.language / prompt_style.char_limit / meta.shot_level / meta.group_id / meta.source_shot_ids` | 以独立 `prompt_style` 声明帧级提示词约束，并锁定组级归属与单一目标 `分镜ID` | S1 | 输入覆盖完整度 | FAIL-VID-FFR-01 |
| FIELD-VID-FFR-02 | `prompt / prompt_char_count` | prompt 必须覆盖目标分镜的剧情桥段、全局风格和压缩后的上下文，且隐藏字段标题 | S2-S4 | Prompt 蒸馏稳定性 | FAIL-VID-FFR-02 |
| FIELD-VID-FFR-03 | `model.reference_images / model.image_markers` | 当前按共享模板骨架保留，不擅自填入虚构图片信息 | S5 | 模板兼容性 | FAIL-VID-FFR-03 |
| FIELD-VID-FFR-04 | `第N集.json / 第N集.txt / _manifest.json` | 双输出文件可追溯、可继续 handoff | S6 | 输出可消费性 | FAIL-VID-FFR-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-VID-FFR-01 | 当前目标 `分镜ID` 是谁，属于哪个 `分镜组` | 锁定 `prompt_style + shot_level + group_id + source_shot_ids` | 分镜定位冲突或缺失 |
| S2 | FIELD-VID-FFR-02 | `剧本正文` 中哪一段才对应目标分镜 | 提取对应分镜帧的剧情桥段 | 直接整段照搬剧本正文 |
| S3 | FIELD-VID-FFR-02 | 哪些内容必须原文保留，哪些内容应压缩 | 直贴 `全局风格`，压缩其余组级与目标镜级字段 | 固定块被改写或压缩失衡 |
| S4 | FIELD-VID-FFR-02 | 如何隐藏字段标题仍保住结构 | 仅保留组ID/镜ID显式标签 | 出现字段标题残留 |
| S5 | FIELD-VID-FFR-03 | 参照图字段当前如何处理 | 保持共享模板骨架，不填虚构信息 | 擅自补图或删字段 |
| S6 | FIELD-VID-FFR-04 | 输出是否能同时被视频工具与人工审阅消费 | 写 JSON、TXT、manifest 与统计字段 | 只产出单文件 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-VID-FFR-01 | `prompt_style.type / meta.shot_level` 合法，且 `group_id` 与长度为 1 的 `source_shot_ids` 同时成立 | FAIL-VID-FFR-01 | S1 |
| FIELD-VID-FFR-02 | prompt 满足桥段提取、固定块保留、隐藏标题与字数窗 | FAIL-VID-FFR-02 | S2-S4 |
| FIELD-VID-FFR-03 | 图片字段保留共享模板骨架且无虚构内容 | FAIL-VID-FFR-03 | S5 |
| FIELD-VID-FFR-04 | JSON、TXT 与 manifest 可追溯可 handoff | FAIL-VID-FFR-04 | S6 |
