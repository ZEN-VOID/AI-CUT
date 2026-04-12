# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type                                                   | root_cause_layer    | immediate_fix                                                                    | systemic_prevention                                                      | verification_point                                    |
| ------------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------- |
| `2-Global` 只有概念引用，没有真实父 skill                               | 阶段锚点层          | 建立 `SKILL.md + CONTEXT.md + openai.yaml + shared I/O`                        | 将 `2-Global` 视为规划后、明细前的独立父级真源                         | 根技能与 registry 能回指真实路径                      |
| 导演组角色直接争夺最终文档                                                | 编排边界层          | 收回三份 Markdown 的写回权到父 skill                                             | 在 team 与父 skill 固化 `agents_plan + patch / note / report`          | 角色文档不再宣告阶段完成                              |
| 导演组角色只有边界合同，没有高质量创作方法                                | 创作方法真源层      | 新建导演组共享方法合同，收口证据梯度、决策顺序、质量门禁与退化规则               | 让父 skill / team / 角色 / 模板统一回指共享方法真源，而不是各自平行发明  | 角色提示不再只剩目标与禁令，输出更具体可消费          |
| 项目级风格/类型文档被 episode 内容污染                                    | 输出治理层          | 把项目级总则与 episode/group 级内容重新拆层                                      | 在模板中固定“项目总则”与“第N集/组ID”分区                             | `全局风格.md`、`类型指导.md` 不再出现某集局部细节 |
| `导演意图.md` 只剩抽象口号                                              | 角色合同层          | 强制回到 `第N集 -> 组ID -> 画面任务` 粒度                                      | 在角色合同中固化“剧情任务 + 画面重点 + 情绪推进 + 下游指导”            | 当前集每组都能被 `3-Detail` 直接消费                |
| 上游 `3-分组` 仍是摘要稿，不能直接回链分镜组切口                        | 上游输入层          | 回到 grouped script 输入，按 `【x-x-x】` 读取分组边界                          | 在 shared I/O 与模板固化“`3-分组/第N集.md` 直接带三段式分镜组ID标题” | `导演意图.md` 能直接对齐上游组切口                  |
| 仓内仍残留 `.agents/skills/aigc/2-组间` 旧路径                          | 引用同步层          | 全仓扫描并把显式旧路径同步到 `2-Global`                                        | 将路径同步纳入本阶段 rollout 门禁                                        | 不再存在显式旧目录路径残留                            |
| `2-Global` 文档仍引用失效的导演组旧 team，或未写默认后台 subagents 模式 | subagent 编排合同层 | 把 team 引用统一收口到 `.codex/agents/aigc/导演组/team.md`，并补写后台执行规则 | 让 audit 同时检查 `.codex/agents/aigc/**` 路径存在性与阶段合同完整性   | 追因路径、入口提示与执行形态不再互相打架              |

## Repair Playbook

1. 先看 `2-Global/SKILL.md` 是否仍能清楚解释父 skill、team 和三份输出的关系。
2. 再看 `.codex/agents/aigc/导演组/team.md` 是否仍把写回权保留在父 skill。
3. 再看 `.codex/agents/aigc/导演组/_shared/CREATIVE_METHOD.md` 是否仍覆盖证据梯度、决策顺序、质量门禁与退化规则。
4. 再检查三份输出是否保持“项目级总则”与“episode/group 级内容”分层。
5. 最后才看单次文案是否需要返工。

## Reusable Heuristics

- `2-Global` 最稳的定位不是“另一个导演 JSON 阶段”，而是“给 `3-Detail` 提前锁定导演总则的三份 Markdown 真源”。
- 风格、类型、导演构思这三件事最容易混写；最稳的做法是让项目级稳定项和按集按组的增量项分开落盘。
- `导演` 角色只有在已经有稳定分组时才应该进入，否则它只会把想象错写成事实。
- 父 skill 的价值不在于重复写 prompt，而在于决定哪一份文档要刷新、哪一份只做增量 patch。
- 如果角色文档只有目标、输入输出和越权禁令，模型通常只会学会“别写错”，不会稳定地产出“写得好”的导演判断；方法层必须另有共享真源。
- 对 `2-Global` 而言，旧 `2-组间` 显式路径残留本身就是规则层 bug，不应靠人工记忆兜底。
- 对 `2-Global` 来说，`ordered tranche` 只说明风格、类型、导演的依赖顺序；如果不把“默认后台派发、父级统一收束”写出来，调用层仍会误解成交互式前台流程。
- 对 `2-Global` 来说，`agents_plan` 适合承载项目级风格/类型/导演裁决路径；最终 Markdown 仍只能由父 skill 写回，不能把思考计划倒灌成业务真源。
- `2-Global` 读取 `3-分组` 时，最稳的入口不是摘要表，而是正文里的三段式 `分镜组ID` `【x-x-x】`；这样下游导演意图和后续分镜体系才能直接回链。
