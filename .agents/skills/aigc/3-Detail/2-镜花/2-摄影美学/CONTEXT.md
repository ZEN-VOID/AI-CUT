# CONTEXT.md

## Purpose & Loading Contract

- 本文件保存 `2-摄影美学` 的经验层知识库，不是过程日志。
- 命中本 skill 时必须和同目录 `SKILL.md` 一起加载。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父级 `3-Detail` / `2-镜花` 合同 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-18

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `module-spec.yaml` 列表项以反引号开头，导致 YAML 解析失败 | 合同语法层 | 把以 code span 起始的列表项改成 quoted scalar | 在本 skill 的 YAML 合同里，凡列表项以反引号起始都统一加引号，并用解析器回读 | `yaml.safe_load` 能通过四个 `module-spec.yaml` |
| 只写“冷、硬、高级”，没有可执行摄影判断 | branch 汇流层 | 回到 `visual_control_line -> cinematography_strategy_note`，先锁控制线再落叶子 | 在 `SKILL.md + module-guide.md` 固定控制线与策略句是叶子前置 | `摄影美学` 能回答光从哪来、色怎么控、材料怎么见 |
| 高调/低调写了情绪，却没交代主亮区和暗部保留 | 影调控制层 | 回到 `CG-S2 -> CG-S5`，先补高低调走向、主亮区和阴影融合边界 | 在 `SKILL.md + 光影模块` 固定“最亮处/暗部边界”是光影必答项 | 删除形容词后，仍能说清哪里最亮、哪里可黑 |
| 当前 root 未回读就沿旧快照继续写 | 输入锁定层 | 回到 `CG-S1-ROOT-LOCK`，重新读取当前 `第N集.json` | 在 `SKILL.md` 固定“branch 开始前必须重读当前 root” | `摄影美学` 明确依附当前 `分镜构图` |
| 叶子模块各自发明目标，汇流后像三段摘要 | 叶子调度层 | 回到 `CG-S4-STRATEGY`，先压一句稳定摄影判断，再重跑叶子 | 在主 `module-guide` 固定“叶子只吸收控制线，不另起总线” | 汇流后保留单一摄影主收益 |
| 色彩只写冷暖或情绪词，没有说明关系模式和综合色来源 | 色彩叶子层 | 回到色彩叶子，按 `主导色相/关系模式 -> 明度 -> 饱和度 -> 色温` 重写 | 在 `色彩/module-guide + module-spec.yaml` 固定固有色/环境色与关系模式门 | 布景、服装或调色都能接住这组色彩判断 |
| 质感只报材料名，没有说明靠什么显出来 | 质感叶子层 | 回到质感叶子，补 `显影机制 + 表面行为 + 节制边界` | 在 `质感/module-guide + module-spec.yaml` 固定扫射光/镜面高光/逆光/漫射等显影机制 | 读者能说清材质是怎样被镜头看见的 |
| 质感或色彩压过人物与动作可读性 | 局部节制层 | 收掉次级材料或色彩修辞，优先保主体和空间可读性 | 在 `Convergence Contract` 固定 `visual_control_line > readability > 风格走廊 > 局部强化` | 画面增强但不喧宾夺主 |
| branch sidecar 只有 patch，没有思考过程 | sidecar 合同层 | 补 `thinking_process.context_anchor / creative_thesis / execution_steps / self_check` | 在 `SKILL.md` Completion Contract 固定 sidecar 必填槽位 | reviewer 能追到本组摄影判断来源 |

## Repair Playbook

1. 先确认当前 root 是否已经回读，且命中镜头有 `分镜构图`。
2. 再确认本组摄影必须继承的风格承诺、禁区、影调极性和综合色温。
3. 若 `visual_control_line` 说不清主体控制、空间剥离、影调极性、综合色温、质感入口、观看压力，直接回退，不要急着写叶子。
4. 若 `cinematography_strategy_note` 不能回答“哪里最亮、哪里可黑、颜色怎么走、材质如何显出”，说明摄影主张还没锁住。
5. 光影先看来源、主亮区和阴影边界，色彩先看色相/明度/饱和度/色温与关系模式，质感先看“最先被感到的材料”和显影机制。
6. 汇流前必须补 `group_lighting_note`；没有组内推进，说明还没从单镜描述升级成组级摄影判断。
7. sidecar 完成后再做一次越权检查：是否改了构图骨架、是否发明剧情事实、是否只剩漂亮话。

## Reusable Heuristics

- 摄影 branch 最重要的不是“写得更美”，而是先锁定一条足以约束光影、色彩、质感的控制线。
- `cinematography_strategy_note` 应该像总调度句，而不是总结句；它的作用是约束叶子，不是装饰汇流段落。
- 高调和低调都必须有锚点：高调要留少量深色支点，低调要留少量高光层次，否则画面会发飘或死黑。
- 当摄影判断开始发虚时，先问“最亮处落在哪、暗部保留到哪”；这通常比追问“氛围是什么”更快把分支拉回可执行状态。
- 色彩只有挂到光线与空间上才算成立；如果说不清是固有色主导还是环境色主导，说明还没真正完成色彩叶子。
- 质感最有效的写法通常不是多，而是准；先锁材料焦点，再决定它靠扫射光、镜面高光、逆光还是漫射被看见。
- 组级摄影判断比单镜漂亮话更重要；没有 `group_lighting_note`，通常说明还停在局部描写层。
- 质感最容易越权抢戏，优先写“最先被感到的材料”，不要面面俱到。
- 当色彩、光影、质感发生冲突时，先保住观看重心和空间可读性，再谈风格化强化。
