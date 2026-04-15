# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-面板/道具` 的局部经验层知识库，不是过程日志。
- 调用本 leaf 时，先读取父 `3-面板/CONTEXT.md`，再读取本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 旧面板脚本只读兼容 JSON，无法消费当前 Markdown 主稿 | 输入真源层 | 增加 Markdown `**prompt整合**` 提取 | 在 `SKILL.md` 固定 Markdown 为默认输入，compat JSON 为 fallback | sample Markdown 能 dry-run 生成 layout |
| layout 后没有自动生图 | 交付边界层 | 默认调用共享 SMART bridge | `--layout-only/--json-only` 才停在 JSON | manifest 有 `image_generation` 状态 |
| 批量 panel 不能复用 2-设计 已有图片 | SMART continuity 层 | layout 写入 `continuity_source_roots` | `_shared` 统一扫描同主体图片 | request trace 有 continuity refs |
| 单文件或自然语言任务被历史图片污染 | SMART 上下文层 | 单次输入默认 `direct-request/single-doc-t2i` | 单次任务不写 continuity roots | request trace 默认 reference_count=0 |
| 形制高风险道具生成现代错误形态 | prompt guardrail 层 | 对杯、细链、图纸、铜铃注入 guardrails | 在 runner 中集中维护 morphology map | layout prompt 含对应形制约束 |

## Repair Playbook

1. 先看输入是不是 `--project/--episode` 批量，还是 `--prompt-file/--text` 单次。
2. Markdown 优先提取 `**prompt整合**`；若缺失，不要从全文拼接。
3. 兼容 JSON 只读 `prompt_cn / prompt_anchor / prompt`，不把 JSON 全文当 prompt。
4. layout 一定先于生图；生图失败时保留 request sidecar 方便补跑。
5. SMART 参照异常时先查 `_shared/panel_auto_generate.py`，不要在 leaf 复制扫描逻辑。

## Reusable Heuristics

- 当前仓的道具面板最稳定输入是逐道具 Markdown 的 `**prompt整合**`；旧仓 JSON 配置只保留为兼容入口。
- `layout.json` 既是生图前置请求，也是失败后可补跑的审计证据。
- 批量连续性与单次创作是两种不同语义；不要为了“更像上一次”而污染用户单次 prompt。
