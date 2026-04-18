# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `writing-craft-catalog`，用于沉淀 craft 症状到 leaf note 的映射经验。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 跨 step 的共性经验应回写根 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 一次性把所有 craft docs 都读了 | load strategy | 回到症状分类，只保留最小必要 1-2 个 leaf notes | 固定本模块的“最小加读”原则 | `loaded_references` 显著收缩 |
| 读了 leaf note 但问题不对症 | symptom mapping | 重做症状识别，再换对应 leaf note | 在本模块里维护症状到文档映射 | craft note 与问题类型一致 |
| craft note 覆盖了上层真源 | authority boundary | 回退到调用 step 模块，由上层裁决最终是否采用 | 固定 craft 只做局部强化，不做真源替代 | 叶子建议不会改写章节板块职责 |
| 基础对白文档和高阶声口文档抢同一个入口 | canonical craft routing | 把 `dialogue-writing.md` 降格为基础体检，把 `voice-register-and-duel.md` 固定为高阶对白主入口 | 在 module-spec 里写死症状到文档映射 | 命中“同声同气/无位移”时优先进入 `voice-register-and-duel.md` |

## Repair Playbook

1. 先说清症状。
2. 再挑 1-2 个最直接的 leaf notes。
3. 再把加读收益转写成调用 step 能执行的动作。
4. 若 craft 建议与真源冲突，永远先保真源。

## Reusable Heuristics

- `writing-craft-catalog` 的价值在于“准”，不在于“多”。
- `typesetting.md` 最适合 Step 4 终检，`genre-hook-payoff-library.md` 最适合 Step 1 的题材命中强化。
- 当问题描述还是“大概不够好看”时，先别进 craft catalog，先逼自己把症状说清楚。
- craft 叶子文档应保持在 `writing-craft-catalog/leaf-notes/` 这个模块私域下，不要再悬挂回 `references/` 根层与 step 模块抢入口语义。
- `dialogue-writing.md` 负责基础对白体检；只要问题已经升级为“角色说话像一个模子”“对手戏没有权力位移”，就应切到 `voice-register-and-duel.md`。

