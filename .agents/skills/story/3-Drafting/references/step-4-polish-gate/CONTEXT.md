# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `step-4-polish-gate`，沉淀润色阶段的问题修复与终检经验。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 若经验涉及上游审查字段或全技能流程闸门，需晋升回根 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| Step 4 变成重写剧情 | step boundary | 回到最小必要修改，只修问题不改规划真源 | 固定 Step 4 为问题修复 gate | 修复后剧情职责不漂移 |
| 修完问题但终检没过 | polish gate | 继续留在 Step 4，完成 Anti-AI / 排版 / No-Poison 终检 | 让 `anti_ai_force_check` 成为放行字段 | fail 时不进入 Step 5 |
| 修复项与 craft 加读混乱 | load strategy | 先完成 severity 修复，再按症状读取 craft note | craft 模块只服务局部强化 | 进入 craft 的理由明确 |

## Repair Playbook

1. 先按 severity 排序。
2. 再判断哪些是事实层问题，需回上游合同。
3. 再做最小必要修复。
4. 最后做 Anti-AI、No-Poison、排版终检。

## Reusable Heuristics

- Step 4 最稳的节奏是“先止血，再美化，再放行”。
- 如果一个修法需要重写大段剧情，通常说明问题不该由 Step 4 独自承担。
- `typesetting.md` 这类 craft note 最适合放在终检段，而不是一开始就掺进修复动作。

