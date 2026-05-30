# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/05-资产提取/场景提取` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写场景提取的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 场景标题被改写成漂亮名字 | 标题保真层 | 恢复 `source_title`，把规范名放入 `normalized_name` | `source_title` 和 `normalized_name` 分字段 | 原标题逐字可回指 |
| 剧情 beat 被当成场景 | 场景粒度层 | 回到 `N2-TITLE-SCAN`，只认空间/时间/slugline 证据 | 缺标题回退也必须基于空间时间变化 | 无纯情绪/剧情标题 |
| 同一地点重复条目过多 | 聚合层 | 用 `location_key` 聚合，同地异时做 variant | `duplicate_resolution_table` 必填 | 重复标题有处理理由 |
| 没有标题却伪装显式场景 | 推断标记层 | 改为 `source_title_type: inferred` | 推断场景必须写依据 | 报告列出推断来源 |
| 场景设计出现人物 | 纯空镜约束层 | 回到 `N6-DESIGN-SPEC`，删除人物、剪影、倒影和人群 | 参考场景 `2-设计` 固定 empty shot 约束 | prompt 明确 no people |
| 场景设计脱离原标题 | 设计锚点层 | 回到 `source_title` 和 `source_evidence`，重写 design_spec | 设计必须消费提取条目 | 设计字段可回指标题 |

## Repair Playbook

1. 先判断失败是漏标题、改标题、误合并、误拆分、伪推断还是输出路径错误。
2. 若有明确场景标题，优先保留原标题，不要美化命名。
3. 若同名场景重复，先看时间、状态和空间功能，再决定合并或变体。
4. 若缺标题，只能按空间/时间/内外景变化推断，不能按情绪或剧情作用推断。
5. 若下游需要统一命名，保留 `source_title`，另补 `normalized_name`。
6. 若设计规格漂移，先回到场景标题、空间/时间证据和 `source_posture`，不要新增剧情场景。

## Reusable Heuristics

- 场景提取最稳的真源通常就是 `02` 剧本里的场景标题；不要在提取阶段重新命名。
- `location_key` 用来帮助合并和设计，`source_title` 用来保真追溯，两者不要互相替代。
- 同一地点不同时间或状态，比“重复标题”更常见；拆成 variant 往往比强合并更适合下游生成。
- 场景设计 JSON 的关键不是散文氛围，而是能稳定说明空间结构、材质、光线、构图和空镜约束。
