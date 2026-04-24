# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-Planning/1-分集` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/1-Planning/references/episode-splitter-contract.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父 `1-Planning/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 输入根没有锁到 `projects/aigc/<项目名>/Story/` | 输入真源层 | 回到故事目录重新锁定输入范围 | 在 `SKILL.md` 固化故事目录优先，manifest 只作索引证据 | 输入清单与用户口径一致 |
| readiness 未通过仍继续正式分集 | gate 层 | 停止执行并返回缺口 | 把 blocked / incremental / full_season 写成强门禁 | 不再出现 blocked 仍落盘正式结果 |
| 把 storyboard / hybrid 中的镜头语言清洗掉 | 源文本保真层 | 恢复原文切分，不做小说化改写 | 在 `SKILL.md` 固化“只切分，不清洗镜头语言” | 输出仍保留源文本结构证据 |
| `1-分集/第N集.md` 文件已生成，但 `【剧本正文】` 后正文区被截断 | QA / 输出完整性层 | 以采纳边界对应的上游片段补回缺失正文，并重新核对结尾锚点 | 在 `SKILL.md` 固化“文件存在不等于正文完整；带 wrapper 时必须校验 `【剧本正文】` 后正文区覆盖完整” | 分集文件正文区与上游采纳片段首尾一致 |
| 漏写 `source_profile` 或 `bootstrap_output` handoff | 下游交接层 | 重建父级 patch | 在字段主表与模板中固定 handoff 字段 | `2-Global` 可直接消费 handoff |
| `episode-split-plan.json` 与 `1-分集/第N集.md` 漂移 | 机读一致性层 | 回读模板并重建索引 | 强制模板化生成机读文件 | 索引与上游原文真源一致 |
| `0-Init` 已登记 `development_briefs` 允许开发式分集，但 `1-分集` 仍把执行案视为绝对非法 | 父子技能合同层 | 允许在 `incremental` 条件下把 manifest 中已登记的 `development_briefs` 作为边界辅证消费 | 在 `SKILL.md` 中固化“辅证可用、正文真源不升格、coverage 缺口必须显式保留” | 执行报告与机读索引都能看见“开发式分集”说明 |
| 为单一分集裁决单元保留孤立 subagent | 结构治理层 | 将边界判断、落盘与 handoff 全部收回 `1-分集` skill 本体 | 在父 skill、leaf skill、入口元数据与审计脚本中固化“`1-分集` 直达执行” | 不再存在已删除的旧分集 subagent 回指 |
| 只把 `1-分集` 改成知行合一标题，但业务分析、节点动作与汇流门没有真正同源 | 思行网络层 | 把输入分析、路由分支、节点动作、汇流条件与输出合同重新收回同一 `SKILL.md` | 在 `SKILL.md` 固化 `Business Requirement Analysis + Topology + Thinking-Action Node + Convergence + One-Shot Output` 五层结构 | 不再出现“看似升级、实际仍是旧线性 steps”的伪改造 |

## Repair Playbook

1. 先确认 `projects/aigc/<项目名>/Story/` 的实际输入范围。
2. 再确认主路由是否真的遵守 `P1>P2>P3`。
3. 再看候选边界是否有结构/戏剧证据，而不是字数硬切。
4. 最后才检查 `episode-split-plan.json` 与 handoff patch。

## Reusable Heuristics

- 在 DREAMER 里，`1-分集` 的 canonical 输出应是 `projects/aigc/<项目名>/1-Planning/1-分集/第N集.md`，由 `2-格式` 再继续整理成主稿。
- 只要 `story-source-manifest.yaml` 已经把 `storyboard_script` 和锁轴写清，分集阶段就应保留这些结构信号，而不是先清洗再切分。
- `episode-split-plan.json` 的价值不是替代正文，而是给 `2-格式`、父 skill、规划组其他角色和 `2-Global` 一个稳定机读入口。
- `1-Planning/1-分集/第N集.md` 若采用 frontmatter + 说明 + 正文包装结构，验收时不要直接拿整文件和 `Story/` 做行数比较；应只比对 `【剧本正文】` 后的正文区是否完整覆盖源片段。
- 当 `Story/` 里同时有正文和执行案时，最稳的做法不是二选一，而是把正文留在 `primary_story_source`，把执行案留在 `development_briefs`，并只在 `incremental` 条件下让执行案辅助边界裁决。
- `1-分集` 的证据侧车最多保留一份 `projects/aigc/<项目名>/1-Planning/1-分集/执行报告.md`；逐集报告会把证据层拆碎，不利于规划阶段收口。
- 在 `1-分集` 里，不要为了单一裁决面额外保留 subagent；边界判断、落盘、索引更新和 QA 应统一留在 skill。
- 若某个 leaf 当前只有一个命中的角色且没有独立变体路由价值，应直接融合回 skill 本体，而不是再维护一层 team/agent 合同。
- 对 `1-分集` 做知行合一改造时，最稳的方式不是发明新业务，而是把现有 `P1>P2>P3`、VSM、字段主表和 QA 重新编织成“串行主干 + 条件分支 + 汇流门”的单技能网络。
- 思行裁决摘要应压缩进 `执行报告.md` 的既有区块，不要额外挂一个 reasoning 文件把分集再次拆成第二真源。
