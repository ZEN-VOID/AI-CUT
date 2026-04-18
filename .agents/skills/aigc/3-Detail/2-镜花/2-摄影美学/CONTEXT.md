# CONTEXT.md

## Purpose & Loading Contract

- 本文件保存 `2-摄影美学` 的经验层知识库，不是过程日志。
- 命中本 skill 时必须和同目录 `SKILL.md` 一起加载。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父级 `3-Detail` / `2-镜花` 合同 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-17

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只写“冷、硬、高级”，没有可执行摄影判断 | branch 汇流层 | 回到 `visual_control_line -> cinematography_strategy_note`，先锁控制线再落叶子 | 在 `SKILL.md + module-guide.md` 固定控制线与策略句是叶子前置 | `摄影美学` 能回答光从哪来、色怎么控、材料怎么见 |
| 当前 root 未回读就沿旧快照继续写 | 输入锁定层 | 回到 `CG-S1-ROOT-LOCK`，重新读取当前 `第N集.json` | 在 `SKILL.md` 固定“branch 开始前必须重读当前 root” | `摄影美学` 明确依附当前 `分镜构图` |
| 叶子模块各自发明目标，汇流后像三段摘要 | 叶子调度层 | 回到 `CG-S4-STRATEGY`，先压一句稳定摄影判断，再重跑叶子 | 在主 `module-guide` 固定“叶子只吸收控制线，不另起总线” | 汇流后保留单一摄影主收益 |
| 质感或色彩压过人物与动作可读性 | 局部节制层 | 收掉次级材料或色彩修辞，优先保主体和空间可读性 | 在 `Convergence Contract` 固定 `visual_control_line > readability > 风格走廊 > 局部强化` | 画面增强但不喧宾夺主 |
| branch sidecar 只有 patch，没有思考过程 | sidecar 合同层 | 补 `thinking_process.context_anchor / creative_thesis / execution_steps / self_check` | 在 `SKILL.md` Completion Contract 固定 sidecar 必填槽位 | reviewer 能追到本组摄影判断来源 |

## Repair Playbook

1. 先确认当前 root 是否已经回读，且命中镜头有 `分镜构图`。
2. 再确认本组摄影必须继承的风格承诺、禁区和戏剧焦点。
3. 若 `visual_control_line` 说不清主体控制、空间剥离、质感方向、观看压力，直接回退，不要急着写叶子。
4. 若 `cinematography_strategy_note` 不能驱动后三叶子，说明摄影主张还没锁住。
5. 光影先看来源和戏剧用途，色彩先看色相/明度/饱和度/色温，质感先看“最先被感到的材料”。
6. 汇流前必须补 `group_lighting_note`；没有组内推进，说明还没从单镜描述升级成组级摄影判断。
7. sidecar 完成后再做一次越权检查：是否改了构图骨架、是否发明剧情事实、是否只剩漂亮话。

## Reusable Heuristics

- 摄影 branch 最重要的不是“写得更美”，而是先锁定一条足以约束光影、色彩、质感的控制线。
- `cinematography_strategy_note` 应该像总调度句，而不是总结句；它的作用是约束叶子，不是装饰汇流段落。
- 组级摄影判断比单镜漂亮话更重要；没有 `group_lighting_note`，通常说明还停在局部描写层。
- 质感最容易越权抢戏，优先写“最先被感到的材料”，不要面面俱到。
- 当色彩、光影、质感发生冲突时，先保住观看重心和空间可读性，再谈风格化强化。
