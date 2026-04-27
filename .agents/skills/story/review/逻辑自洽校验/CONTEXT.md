# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `逻辑自洽校验` 子技能包的局部经验层，只服务逻辑与设定自洽、例外代价与 source trace 维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 一切跨层返工经验优先回写到父层 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 明明是 card 或 planning 冲突，却要求正文自行补圆 | source trace | 改判为 `back_to_source_contract` | issue 字段固定保留 `source_layer_owner` | drafting 不再反复背锅 |
| 逻辑问题只写“别太巧合”，没有具体断点 | causal check | 回到因果链逐步拆解 | 在 metrics 中固定 `cause_effect_breaks` | 每条问题都能指出断在哪里 |
| 把风格不自然误判成逻辑错误 | boundary split | 先问“能否发生”，不要先问“写得顺不顺” | 将逻辑维度的非目标写死在 child contract | issue 分类更稳定 |
| 设定破例只有结果，没有条件或代价 | exception contract | 逐条补查 `trigger + cost + precedent_or_explanation` | 在技能主合同和 reference 中固定“例外四格”检查 | 破例问题不再被包装成“爽点特权” |
| 世界规则稳定，但社会/资源后果时有时无 | social ecology | 把组织、资源、环境反应也纳入逻辑审查 | 将 `social_ecology_conflicts` 固定为核心 metric | 同类事件的世界反应更稳定 |
| 能力边界其实漂移了，却只记成状态问题 | power scale | 单独拆出能力上限、越级条件和资源消耗核查 | 将 `capability_conflicts` 与 `exception_cost_gaps` 分离 | 战力问题不再混在一锅“逻辑怪”里 |

## Repair Playbook

1. 先锁当前 source truth：人物状态、物品状态、场景规则、chapter board。
2. 再按“世界铁律 -> 力量体系 -> 社会生态”三支柱检查正文，而不是先从阅读感受出发。
3. 若命中设定破例，补查 `trigger + cost + precedent_or_explanation + visibility`。
4. 若某事件只能靠“作者想让它发生”成立，就要显式标成 `contrivance`。
5. 若上游真源先互相打架，立刻转 `source trace`，不要让 drafting 背锅。

## Reusable Heuristics

- 逻辑维度最重要的不是挑刺，而是识别“到底是谁的锅”。
- 只要 source owner 没写清楚，返工成本通常会被放大一轮以上。
- 幻想设定不怕离奇，怕的是同一条规则在剧情压力下长出第二口径。
- 每次设定破例都应留下代价；没有代价的破例，几乎都会在后续章节里放大成系统性漏洞。
- 世界观的社会与资源后果不是装饰细节，它们本身就是逻辑证据。
