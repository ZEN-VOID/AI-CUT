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
| 设计阶段自动生图时 prompt 被临时改写，或缺统一全局风格前缀 | 上游 handoff 层 | 回到 design carrier 读取 `full_generation_prompt` | 在 `general/SKILL.md` 固化 `4-Design/2-设计` 三域 prompt 真源表与 same-dir same-stem 输出策略 | `scene/role/prop` 的 prompt 都能回链到上游设计载体，且包含 `global_style_prefix` |
| 单独点某个 JSON / 文档生图，却被错误当作 I2I | SMART 模式层 | 去掉隐式 continuity refs，只保留显式参考图 | 在 `general/SKILL.md` 固化“单文件默认 T2I” | 单文件请求的 `images[]` 为空时稳定按 T2I 执行 |

## Repair Playbook

继承父级 `../CONTEXT.md` Repair Playbook 的完整排查顺序。通用生图场景下补充以下优先检查项：

1. prompt 是否为空或仅含空白字符（最常见的通用调用错误）
2. 若来自 `4-Design/2-设计`，先核对 prompt 是否来自上游 design carrier 的 `full_generation_prompt`，并确认包含 `global_style_prefix`
3. 参数是否被默认值正确补齐：
   - 未指定 `aspect_ratio` 时是否自动变为 `16:9`
   - 未指定 `image_size` 时是否自动变为 `4K`
   - 显式传入的合法值是否被保留而非被默认值覆盖
4. 参考图场景（I2I）：
   - URL / 本地文件是否成功转为 `inline_data`
   - `mime_type` 是否匹配真实图片类型
5. 结构化 JSON 承接（`--input-json`）：
   - 空字符串、`null` 字段是否被正确识别为"未指定"并触发默认值补齐
   - 多任务数组是否自动进入并发模式
6. 若来自 `3-面板` 的 SMART sidecar，再核对：
   - `prompt_reference.prompt_field` 是否能回链到 panel packet
   - `smart_mode_resolved` 是否与实际上下文一致
7. 以上均正常则上溯父级完整排查链路（`.env` 配置、请求体格式、响应解析等）

## Reusable Heuristics

- 用户只说"生张图"时走本技能，不路由到特化子技能
- 未指定比例/清晰度时由父级 API 契约自动补齐 16:9 / 4K，无需在本技能层重复注入
- 参考图场景建议加 `--no-report` 减少冗余文件
- `--input-json` 中字段值为空字符串或 `null` 等同于"未指定"，会触发默认值补齐，不会报错
- 多任务批量调用时无需上游手写外部并发，`--input-json` 传入数组即可自动并发
- 若上游来自 `4-Design/2-设计`，最稳的做法不是“再润色一版 prompt”，而是直接读取域内已稳定的 `full_generation_prompt`
- 单主体设计快路径必须把 `--output-dir` 指向设计文件同目录，并把 `--output-filename` 指向设计文件同 stem；不要回退到 `generated/` 子目录。
- 若上游来自 `4-Design/3-面板`，最稳的做法不是在调用前再拼 prompt，而是直接承接 panel packet 写出的 `prompt_text` 与 `prompt_reference`
- `single-doc-t2i` 的本质是“单文件请求不做隐式 continuity ref 扫描”，不是“禁止用户显式给参考图”
