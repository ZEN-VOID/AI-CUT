# Context: nano-banana-multiview-prop（道具多视图）

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: auto
current_lines: auto
current_cases: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-03-20T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为道具多视图子技能的经验层，聚焦三栏布局一致性与空场景护栏。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-MVP-HUMAN-LEAK` | 道具面板中出现人手/人物 | 空场景护栏约束被忽略 | 强化"no humans, creatures"措辞 | 检查所有模块无人形元素 | 人工检查 |
| `TM-MVP-PROP-DRIFT` | 不同视图间道具形态/材质不一致 | 身份锁定约束不够强 | 强化 stable silhouette/scale/material | 比对多视图一致性 | 人工比对 |
| `TM-MVP-LAYOUT-WRONG` | 输出不是三栏布局 | 布局规格被忽略 | 强化 PROP_DESIGN_SHEET 约束 | 检查布局结构 | 人工检查 |

## Repair Playbook

1. 检查图片是否正确传入
2. 检查提示词模板注入是否完整（prop_id / prop_name / desc）
3. 检查 aspect-ratio 是否为 16:9
4. 若出现人物/人手，强化空场景护栏措辞
5. 若布局错误，强化 PROP_DESIGN_SHEET 三栏约束

## Reusable Heuristics

- 固定 16:9，不从原图适配
- 空场景护栏是道具多视图的核心约束——画面中不出现任何人手、人物、人形剪影或生物
- 道具描述应涵盖功能、造型骨架、材质工艺、磨损痕迹、尺度比例
- 默认 `--no-report` 减少冗余文件
- 描述控制在 400 字以内

## Case Log

（待积累）
