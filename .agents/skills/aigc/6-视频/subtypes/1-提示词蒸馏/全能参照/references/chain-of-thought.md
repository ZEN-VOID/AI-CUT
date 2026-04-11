# 全能参照 思维链细则

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-VID-SUBJ-01 | `prompt_style.type / prompt_style.language / prompt_style.char_limit / meta.shot_level / meta.group_id / meta.source_shot_ids` | 以独立 `prompt_style` 声明提示词风格约束，并按二选一关系锁定组级或帧级来源 | S1 | 输入覆盖完整度 | FAIL-VID-SUBJ-01 |
| FIELD-VID-SUBJ-02 | `prompt / prompt_char_count` | prompt 覆盖整组或目标分镜内容，固定块原文保留，其余压缩且隐藏标题；字数统计位于顶层 | S2-S4 | Prompt 蒸馏稳定性 | FAIL-VID-SUBJ-02 |
| FIELD-VID-SUBJ-03 | `model.reference_images / model.image_markers` | `reference_images` 保留上传顺序位，`image_markers` 记录 URL / 主体 / 图号，二者顺序一致 | S5 | 模板兼容性 | FAIL-VID-SUBJ-03 |
| FIELD-VID-SUBJ-04 | `第N集.json / 第N集.txt / _manifest.json` | 双输出文件可追溯、可继续 handoff | S6 | 输出可消费性 | FAIL-VID-SUBJ-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-VID-SUBJ-01 | 当前到底是全能/首尾帧/首帧，且是组级还是帧级 | 锁定 `prompt_style + shot_level + group_id/source_shot_ids` | 分镜定位冲突或缺失 |
| S2 | FIELD-VID-SUBJ-02 | 哪些内容必须原文保留 | 直贴 `剧本正文` 与 `全局风格` | 固定块被改写 |
| S3 | FIELD-VID-SUBJ-02 | 哪些内容应均匀压缩 | 压缩其余组级与镜级字段 | 漏字段或压缩失衡 |
| S4 | FIELD-VID-SUBJ-02 | 如何隐藏字段标题仍保住结构 | 仅保留组ID/镜ID显式标签 | 出现字段标题残留 |
| S5 | FIELD-VID-SUBJ-03 | 参照图字段当前如何处理 | 保留 `reference_images: []`，并组织 `image_markers` 锁上传顺序 | 删除字段、乱序或虚构 URL |
| S6 | FIELD-VID-SUBJ-04 | 输出是否能同时被视频工具与人工审阅消费 | 写 JSON、TXT、manifest 与统计字段 | 只产出单文件 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-VID-SUBJ-01 | `prompt_style.type / meta.shot_level` 合法，且 `group_id` 与 `source_shot_ids` 按二选一成立 | FAIL-VID-SUBJ-01 | S1 |
| FIELD-VID-SUBJ-02 | prompt 满足固定块、压缩块、隐藏标题与字数窗 | FAIL-VID-SUBJ-02 | S2-S4 |
| FIELD-VID-SUBJ-03 | `reference_images` 存在，且 `image_markers` 的 URL / 主体 / 图号完整、顺序稳定 | FAIL-VID-SUBJ-03 | S5 |
| FIELD-VID-SUBJ-04 | JSON、TXT 与 manifest 可追溯可 handoff | FAIL-VID-SUBJ-04 | S6 |
