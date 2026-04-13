# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/1-提示词蒸馏` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 时，应先加载 `.agents/skills/aigc/SKILL.md`，再加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 三个叶子子技能都有，但父级不知道先走谁 | 父级路由层 | 回到 `1-提示词蒸馏` 父级先做对象裁决 | 在父级 `SKILL.md` 固化互斥路由与默认入口 | 同一请求只命中一个叶子 |
| 无序 sibling 被误当成并发批次 | 批量调度解释层 | 明确这层覆写默认并发规则 | 在父级合同写清“语义 sibling 互斥，不默认并发” | 不再同时生成三份叶子请求 |
| 单帧诉求被错误推进到组级故事板 | 对象判定层 | 重新按 `单一分镜ID` 回路由到 `分镜帧` | 在父级写清对象判定信号词与默认入口 | 单帧类请求稳定命中 `分镜帧` |
| `1-提示词蒸馏` 被误做成直接出图 | 阶段边界层 | 回退到“请求 JSON 为主产物” | 在父级合同固定 handoff 边界 | 输出保留到 JSON / manifest，而不是直接图片 |
| 叶子合同都存在，但后续 `2-一致性处理` / `3-图像生成` 接不上 | handoff 层 | 先补父级 handoff 总合同 | 在父级锁定“先蒸馏，再一致性/生成” | 下游可按单一请求对象继续消费 |

## Repair Playbook

1. 先查当前任务对象到底是 `分镜组`、`单一分镜ID` 还是 `漫画页`。
2. 再查请求是否真的只该命中一个叶子子技能。
3. 若用户没有给出明确对象，默认先走 `分镜故事板`。
4. 若输出已经漂移成图片，先退回请求 JSON 合同，再继续后续阶段。
5. 若下游接不上，优先修父级 handoff 边界，而不是各叶子重复补说明。

## Reusable Heuristics

- `1-提示词蒸馏` 的核心不是“写 prompt”，而是“先判对象，再把 prompt 蒸馏收口到正确的请求 JSON”。
- 当一层目录下全是语义 sibling 且彼此互斥时，必须由父级显式覆写“无序默认并发”的仓库级默认规则。
- 对 `5-画面` 来说，`分镜故事板` 是最宽容的默认入口；`分镜帧` 和 `漫画` 只在对象信号足够明确时再切入。
- 父级提示词蒸馏层不应自建第二套 prompt 模板；对象内细节继续留在叶子子技能。
- 若问题表现为“叶子都对，但整体还是接不上”，通常根因在父级路由或 handoff 合同缺失，而不在叶子 prompt 内容。
