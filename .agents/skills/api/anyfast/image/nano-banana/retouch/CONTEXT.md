# Context: nano-banana-retouch（修图）

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

本文件作为修图子技能的经验层，聚焦自然精修、身份稳定与不过度重绘的失败模式。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-RT-PLASTIC-SKIN` | 皮肤被磨得过于光滑，失去真实质感 | 真实感锁定不足 | 强化"保留皮肤纹理/毛孔"措辞 | 默认保留真实感锁定句群 | 放大查看皮肤细节 |
| `TM-RT-IDENTITY-DRIFT` | 修图后脸型、五官或发型发生变化 | 身份锁定描述不足 | 在 `--desc` 中补充不可改变的人物特征 | 默认保留"严禁改成另一张脸"句群 | 人工比对原图与输出 |
| `TM-RT-OVER-CLEAN` | 小瑕疵被修掉，但同时丢失面料/场景细节 | 修图目标写得太泛或太强 | 改成"轻量自然精修"，点名仅修哪些局部问题 | 对局部修复尽量给出具体 desc | 检查衣料纹理与环境细节 |
| `TM-RT-LOCAL-ARTIFACT` | 指定要修的区域仍残留穿帮、污点或噪点 | desc 不够具体，未点明局部问题 | 在 `--desc` 中直接描述问题区域与目标效果 | 局部修复优先提供部位级描述 | 放大检查目标区域 |

## Repair Playbook

1. 检查原图路径是否正确，且输出命名不会覆盖原文件
2. 检查比例适配是否从原图动态计算
3. 检查提示词是否完整（自然修图 + 身份锁定 + 真实感锁定）
4. 若磨皮过度，在 `--desc` 中追加"保留皮肤纹理/妆面质感/毛孔"
5. 若身份漂移，在 `--desc` 中追加不可改变的五官、发型、脸型描述
6. 若局部穿帮未修掉，在 `--desc` 中点明具体部位、瑕疵类型和处理目标

## Reusable Heuristics

- 默认走轻量自然精修，不默认做风格化重绘
- 没有明确需求时，优先修曝光、色偏、轻微瑕疵和关键区域清晰度
- 局部修图类请求最好在 `--desc` 中写明"哪里有问题，要修成什么样"
- 人像修图要显式写"保留皮肤纹理"，否则容易出现塑料感
- 永不覆盖原文件：输出命名自动递增，避免误覆盖
