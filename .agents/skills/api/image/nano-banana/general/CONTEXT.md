# Context: nano-banana-general（通用生图）

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
last_checked_at: 2026-03-20T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 nano-banana 通用生图子技能的经验层。API 层经验（参数枚举、请求格式、并发调度）由父级 `../CONTEXT.md` 维护，本文件聚焦通用 T2I/I2I 场景的 prompt 技巧与调用模式。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| （待积累） | | | | | |

## Repair Playbook

继承父级 `../CONTEXT.md` Repair Playbook 的完整排查顺序。通用生图场景下补充以下优先检查项：

1. prompt 是否为空或仅含空白字符（最常见的通用调用错误）
2. 参数是否被默认值正确补齐：
   - 未指定 `aspect_ratio` 时是否自动变为 `16:9`
   - 未指定 `image_size` 时是否自动变为 `4K`
   - 显式传入的合法值是否被保留而非被默认值覆盖
3. 参考图场景（I2I）：
   - URL / 本地文件是否成功转为 `inline_data`
   - `mime_type` 是否匹配真实图片类型
4. 结构化 JSON 承接（`--input-json`）：
   - 空字符串、`null` 字段是否被正确识别为"未指定"并触发默认值补齐
   - 多任务数组是否自动进入并发模式
5. 以上均正常则上溯父级完整排查链路（`.env` 配置、请求体格式、响应解析等）

## Reusable Heuristics

- 用户只说"生张图"时走本技能，不路由到特化子技能
- 未指定比例/清晰度时由父级 API 契约自动补齐 16:9 / 4K，无需在本技能层重复注入
- 参考图场景建议加 `--no-report` 减少冗余文件
- `--input-json` 中字段值为空字符串或 `null` 等同于"未指定"，会触发默认值补齐，不会报错
- 多任务批量调用时无需上游手写外部并发，`--input-json` 传入数组即可自动并发
