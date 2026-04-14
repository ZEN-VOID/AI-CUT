# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/场景/2-设计` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc -> 4-Design -> 1-场景` 根链之后加载本文件。
- 本技能当前已取消 `references/` 规范载体，也不再依赖 `.codex/agents/aigc/设计组/场景设计/`。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: 6281
current_lines: 123
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-13T00:25:52-0700
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍从 `3-Detail` 直接发明场景设计 | 输入真源层 | 回退到 `scene catalog -> 2-Global -> optional detail` 的输入顺序 | 在 `SKILL.md` 的 `Total Input Contract` 与 `Field Master` 固化第一输入根 | 不再跳过 `1-清单` |
| 规范内容再次分裂到 `references/*` 或外置场景设计 agent | 真源治理层 | 把流程、节点、判型与 gate 全部收回 `SKILL.md` | 在 `Legacy Migration Mapping` 固化“旧载体已内联并删除” | 技能目录不再残留第二真源 |
| 场景设计只剩风格词，没有空间/建筑/布景实义 | 能力拆解层 | 回到 `D3-D5`，按空间、建筑、布景三条能力链重做 | 在 `Thinking-Action Node Contract` 固化每链的着手面 | 设计卡具备可拍、可搭、可消费细节 |
| review 或 audit 缺位，直接写回 | 汇流门层 | 阻止写回，补跑 `D7-D8` 并按返工入口回退 | 在 `Convergence Contract` 固化双重 gate | `场景设计.json` 总带最小 trace |
| `panel_handoff` 或 `final_scene_prompt` 仍需下游重猜 | 下游接口层 | 回到 `D6` 重新整合 candidate、prompt 与 handoff | 在 `One-Shot Output Contract` 固化下游最小接口 | `3-面板 / 5-Image / 6-Video` 可直接继续消费 |
| 逐场景 Markdown 卡仍沿用旧分块模板，无法承载物语/解构/摄影参数 | 输出合同层 | 将卡片模板改为三段式 Markdown，并在 `SKILL.md` 固化 Markdown 与 JSON 映射 | 把三段式结构与兼容字段同步写进 `One-Shot Output Contract` | `<scene_key>.md` 与 `场景设计.json` 不再脱节 |

## Repair Playbook

1. 先确认问题属于输入真源、能力拆解、聚合收束、review gate、audit gate 还是下游 handoff。
2. 若输入根错，立刻回到 `scene catalog`，停止从导演 JSON 自由发挥。
3. 若内容空泛，优先检查 `D3-D5` 是否被混写或跳步。
4. 若写回异常，优先检查 `D7-D8` 是否被跳过，以及路径是否仍在 `projects/aigc/<项目名>/4-Design/场景/2-设计/`。
5. 若发现旧 `references/*` 或 `.codex/agents/aigc/设计组/场景设计/*` 回链，视为源层回退，直接修主合同而不是补兼容文案。

## Reusable Heuristics

- 对场景设计来说，最稳的输入顺序永远是：先对象池，再导演约束，再命中镜头补证据。
- 真正高质量的场景设计不是“多写点形容词”，而是让空间、建筑、布景三条链各自负责不同层面的确定性。
- `review -> audit -> writeback` 不能压成一句“复核通过”；必须显式区分内容复核和真源审计。
- 当用户要求“每个思行节点一步一步足够细”，最有效的做法不是再长角色文档，而是把着手面直接固化进节点 playbook。
- 对“这个场景像什么”不要只给抽象风格词，先判定 `reference_anchor` 是作品场景、现实场所、历史母题，还是只能在题材边界内做 `bounded_extrapolation`。
- “大胆畅想”不能脱离约束单独存在；最稳的写法是先在 `D4` 锁住历史文化和结构边界，再在 `D5` 把想象增量落成具体可见物与标志性元素。
- `templates/scene-design-card.md` 可以保留，因为它是落盘模板；但凡字段主表、workflow、判型或 output contract 跑到别的文档里，第二真源就会重新长出来。
- 当用户要求场景卡改成三段式时，不能只改 Markdown 皮相；必须同步补进节点合同，让 `物语 / 解构 / prompt整合` 都有明确生成责任。
