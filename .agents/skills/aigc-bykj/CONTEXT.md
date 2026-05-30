# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj` 父级导引 skill 的经验层知识库，不是过程日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写阶段路由和阶段真源边界；只记录路由经验、失败模式和修复顺序。

## Context Health

- soft_limit_chars: 8000
- hard_limit_chars: 16000
- status: ok
- last_checked_at: 2026-05-28

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 父级直接执行阶段正文 | 路由边界层 | 回到命中阶段 `SKILL.md + CONTEXT.md` | 父级固定为 `governance_tier: router` | 父级只输出路由和 handoff |
| `02-剧本处理` 被拆回原 `2/3/4` 三目录 | 单技能真源层 | 路由到 `02-剧本处理/` 并保留唯一输出目录 | 父级声明 `02` 是整合阶段 | 输出落在 `output/[项目名]/02-剧本处理/` |
| `03-智能分集` 被误接回小说源或旧 `1-分集` runtime | 阶段输入对象层 | 路由到 `03-智能分集/`，输入固定承接 `output/[项目名]/02-剧本处理/` 的处理后剧本 | 父级和阶段合同同时声明 BYKJ `03` 不默认读取 `projects/aigc/<项目名>/源/` | 输出落在 `output/[项目名]/03-智能分集/` |
| 阶段目录缺 `SKILL.md` 却被调用 | 基线完整性层 | 先报告缺口或补齐阶段合同 | 父级 boundary 固定阶段加载要求 | 调用前能定位阶段 `SKILL.md + CONTEXT.md` |

## Repair Playbook

1. 先判断用户意图命中哪个阶段。
2. 若阶段已初始化，加载该阶段 `SKILL.md + CONTEXT.md`。
3. 若阶段未初始化，报告缺口或按用户任务先补齐阶段合同。
4. 父级不得直接代替阶段生成创作正文。

## Reusable Heuristics

- BYKJ 父级最重要的职责是防止阶段真源漂移，而不是增加一个新的执行层。
- 对 `02-剧本处理`，保持“一阶段整合三能力”的单技能口径，比复用原三阶段输出目录更稳定。
- 对 `03-智能分集`，保持“承接处理后剧本再分集”的口径，比复用旧小说原文分集 runtime 更稳定。
