# Context: nano-banana-background-swap（背景替换）

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: auto
current_lines: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-23T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为背景替换子技能的经验层，聚焦主体锁定、背景清除与边缘融合的失败模式。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-BGS-SUBJECT-DRIFT` | 换背景后主体面部/服装/姿态发生变化 | 主体锁定描述不足 | 强化"严禁漂移"与主体锁定措辞 | 在 desc 中补充主体不可改字段 | 人工比对主体身份与服装 |
| `TM-BGS-BACKGROUND-LEAK` | 原背景元素残留，出现双重环境 | 旧背景清除要求不够强 | 在提示词中显式要求移除原背景元素 | 默认保留"移除图一原背景"句群 | 检查输出是否仍有旧建筑/天空/室内陈设 |
| `TM-BGS-EDGE-HALO` | 主体边缘发丝/衣摆出现抠图白边或硬切割 | 边缘融合要求不足 | 在 desc 中补充发丝、半透明边缘与接地阴影要求 | 默认保留"边缘过渡自然"与"接地阴影合理" | 放大检查边缘细节 |
| `TM-BGS-IMAGE-ORDER` | 输出背景和主体都主要来自同一张图 | `--image-url` 顺序颠倒 | 严格遵循：第一张=主体源，第二张=背景源 | Step 1 参数解析时打印确认日志 | 检查主体来自图A、环境来自图B |

## Repair Playbook

1. 检查两张图是否正确传入（第一张=主体，第二张=背景）
2. 检查比例适配是否从主体原图动态计算
3. 检查提示词是否完整（主体锁定 + 背景替换 + 清除旧背景）
4. 若主体漂移，在 `--desc` 中追加主体身份与服装锁定描述
5. 若旧背景残留，在 `--desc` 中点名要清除的旧背景元素
6. 若边缘发虚或抠图痕迹明显，在 `--desc` 中追加发丝、半透明边缘和接地阴影要求

## Reusable Heuristics

- 图序严格：第一张=主体源（锁定人物/主体），第二张=背景源（提供环境）
- 比例从主体原图动态适配，不硬编码
- 背景参照图优先选空间结构清晰、景深明确、光线方向稳定的图
- 若主体脚下接地点在原图中较弱，最好在 `--desc` 中补一句接地阴影与投影要求
- 永不覆盖原文件：输出命名自动递增，避免误覆盖
