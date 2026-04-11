# Context: nano-banana-costume-swap（角色换装）

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

本文件作为角色换装子技能的经验层，聚焦身份保持与服装还原的失败模式。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-CS-IDENTITY-DRIFT` | 换装后角色面部/发型/肤色变化 | 身份锁定描述不足 | 强化"严禁漂移"措辞 | 在 desc 中追加身份特征强调 | 人工比对面部 |
| `TM-CS-COSTUME-INCOMPLETE` | 服装细节未完整还原 | 图B信息不够清晰 | 提供更清晰服装参照图 | 在 desc 中补充服装细节 | 比对装饰细节 |

## Repair Playbook

1. 检查两张图是否正确传入（第一张=角色，第二张=服装）
2. 检查比例适配是否从角色原图正确映射
3. 检查提示词是否完整（身份锁定 + 服装替换）
4. 若身份漂移，在 `--desc` 中追加身份特征强调
5. 若服装还原不完整，建议用户提供更清晰的服装单品图

## Reusable Heuristics

- 图序严格：第一张=角色源（锁定身份），第二张=服装源（提供样式）
- 比例从角色原图动态适配，不硬编码
- 服装参照图越清晰（单品图/设计稿），还原度越高

## Case Log

（待积累）
