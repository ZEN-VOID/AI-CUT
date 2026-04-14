# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/2-主体设计/服装` 的经验层知识库，不是过程日志。
- 调用本父 skill 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-设计` 跳过 `1-清单` 直接发明服装设计 | 输入锚点层 | 强制回到 `costume_design_bridge.json` 锁当前服装对象池 | 在 `SKILL.md`、`1-主体清单/服装` 合同与 `_shared/IO_CONTRACT.md` 固化“先清单、再设计” | 不再出现无对象池设计 |
| specialists 各写一整份服装稿，父 skill 无法收束 | 编排边界层 | 收回写回权到父 skill，只允许返回 `agents_plan + patch / note / report` | 在主 `SKILL.md` 与 `_shared/IO_CONTRACT.md` 固化 agents-plan-aware handoff | canonical 输出只由父 skill 写回 |
| 廓形、材质、配饰三条线互相打架 | reviewer 合同层 | 进入 `服装一致性复核`，要求指出冲突字段与返工入口 | 将跨字段一致性检查设为默认 tranche | reviewer 能给出明确 rework |
| 服装设计只剩 prompt，没有 machine-first carrier | 输出治理层 | 补回 `服装设计.json` 并让 Markdown 与其同源 | 在输出模板中固定 JSON 为 canonical | 下游面板/生图能稳定消费 JSON |
| `提示词架构师` 越权新增设计事实 | prompt 分层层 | 只允许写 `costume_design_prompt.json` patch | 在主 `SKILL.md` 与 `_shared/IO_CONTRACT.md` 固化“prompt 不得倒灌 design facts” | prompt sidecar 与 design master 分层稳定 |
| 父 skill 有 team 配置，但主合同仍偏线性说明 | 思行网络层 | 把 route mode、selected_costumes、specialist 切面、review gate 和 manifest 闭环全部收回同一 `SKILL.md` | 固化“串行锁定 + specialists 并行 + review 汇流 + prompt/audit 后段”的父技能网络 | `2-设计` 能在主合同中独立解释整条执行链 |
| `2-设计` 仍依赖不存在的平铺 `2-Global/全局风格.md` | 输入真源层 | 改读 `2-Global/全局风格/全局风格设计.md`，保持 `类型元素.md` 为兼容投影 | 在 `SKILL.md` 与 `_shared/IO_CONTRACT.md` 固化目录化风格真源 | 服装设计 preload 与项目真实文件一致 |

## Repair Playbook

1. 先查 `1-清单/costume_design_bridge.json` 是否存在且服装对象池稳定。
2. 再看主 `SKILL.md` 与 `_shared/IO_CONTRACT.md` 是否仍把写回权保留在父 skill。
3. 再看 `服装设计.json` 是否与逐服装 Markdown、prompt sidecar 同源。
4. 若服装设计冲突，优先回到 `服装一致性复核` 指定的字段槽位返工。
5. 最后才调整单次 prompt 话术。

## Reusable Heuristics

- 服装设计最稳的入口不是“按角色再想一次穿搭”，而是先有服装对象池，再做结构化设计。
- 对服装链来说，`prompt sidecar` 是下游执行话术，不是服装事实真源。
- `character_design.json` 最适合做约束输入，而不是被服装类目重新覆盖。
- 对服装设计来说，`agents_plan` 最适合承载 costume dispatch、字段补位顺序与 prompt/audit 返工摘要；最终 design master 仍只能由父 skill 写回。
- 对带能力镜面的父技能做知行合一改造时，最关键的是把原 team 拓扑翻译成主合同里的节点网络，而不是继续依赖不存在的外置 team 文档。
- 当 `2-Global` 的风格文件已经目录化时，服装链不应再等待平铺 `全局风格.md`；直接消费 `全局风格/全局风格设计.md` 更稳，也更符合当前 runtime。
