---
name: story-drafting-reading-power
description: Use when `3-Drafting` needs the governed child skill that upgrades reader pull through pressure, hook, payoff, and chapter-end continuation design in the current episode draft.
governance_tier: lite
---

# 3-Drafting / 6-追读力强化

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `3-Drafting/SKILL.md`、`../_shared/drafting-child-output-contract.md`、`../_shared/drafting-instant-validation-contract.md`。
- 正式处理前，必须读取 Step 5 已写回后的当前 `第N集.md`。
- 必须按需读取根级共享真源 `../../_shared/reading-power-taxonomy.md`。
- 必须按需读取根级共享工程指南 `../../_shared/cool-points-guide.md`。
- 必须读取本地执行细则 `references/reading-power-execution-playbook.md`。

## Parent Positioning

本 child 负责：

- 把“张力”升级成可操作的“追读力”设计
- 同时处理压力、钩子、微兑现、爽点与章末续读牵引
- 让本章既有局部满足，也保留下一章的继续阅读冲动

它不负责：

- 重写 chapter board 主干义务
- 越权新增脱离规划的新主线
- 取代 Step 7 统一文风

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../_shared/drafting-child-output-contract.md`
- `../_shared/drafting-instant-validation-contract.md`
- `../../_shared/core-constraints.md`
- `../../_shared/reading-power-taxonomy.md`
- `../../_shared/cool-points-guide.md`
- `./references/reading-power-execution-playbook.md`

## Canonical Source Governance

- `../../_shared/reading-power-taxonomy.md` 是钩子类型、爽点模式、微兑现分类和题材投影的唯一 taxonomy 真源。
- `../../_shared/cool-points-guide.md` 是爽点强度、组合技、疲劳防控与虐爽配合的唯一工程指南真源。
- 本 child 只拥有“如何把 taxonomy 投影到当前正文重写”的执行权，不再局部复制一份分类体系。
- 本 child 也只消费爽点工程指南，不在本地再复制一份共享爽点手册。
- 若当前项目未显式启用 `type-pack` 或没有题材型投影输入，则仅使用 taxonomy 的通用部分，不强行套题材偏好。

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 让本集在章内持续给读者“小收获 + 新风险 + 续读牵引”，而不是只在语气上显得激烈。 |
| `business_object` | Step 5 后正文、chapter board 债务、写作日志、当前项目的 reader signal / type-pack 投影（若存在），以及根级追读力 taxonomy。 |
| `constraint_profile` | 追读力必须来自既有规划、角色选择和局势推进，不能靠硬插事故、滥用悬念或无兑现钩子。 |
| `success_criteria` | 本章至少形成清晰推进梯度、可感知局部兑现、有效章末牵引，并能说清当前主要 hook / payoff 是什么。 |
| `topology_fit` | `root reread -> reading-power debt scan -> tactic bundle select -> rewrite -> ending pull audit -> regression guard` |

## Total Input Contract

- 必需输入：
  - 当前 `第N集.md`
  - `Planning/全息地图.json`
  - `写作日志.yaml`
- 可选增强输入：
  - `reader signal`
  - `type-pack` 对 drafting stage 的当前投影
  - 最近章节的 hook / cool-point 使用情况
- 硬规则：
  - 追读力强化不能违背已建立的因果。
  - 不能只靠激烈措辞、感叹句或突然出事冒充追读力。
  - 章内必须兼顾“即时满足”与“后续牵引”，不能只留坑不兑现。
  - 同一章末不得堆叠多个互相打架的主钩子。

## Output Contract

- `manuscript_patch`
  - 追读力强化后的正文
- `process_log_entry`
  - `step_id: 6`
  - `focus_dimension: reading_power`
- owned manuscript dimension：
  - 压力梯度
  - 钩子与续读牵引
  - 微兑现与爽点着陆
  - 章末 pull

## Immediate Validation Hook Contract

- 本 step 写回后，父层必须按 `../../4-Validation/_shared/validation-dimension-registry.yaml` 触发当前 step 登记的 inline validators。
- 若 hook 失败，不得直接进入 Step 7；必须在当前 step 本地重写，或回退到 registry 指向的更早受影响 step。

## Reference Loading Guide

1. 先读 `../../_shared/reading-power-taxonomy.md` 的通用 taxonomy。
2. 再读 `../../_shared/cool-points-guide.md`，判断强度梯度、主副爽点组合与防疲劳策略。
3. 若当前项目存在明确题材 / type-pack 投影，再读对应 genre section。
4. 最后按 `references/reading-power-execution-playbook.md` 把分类映射为本章可执行的重写动作。

## Visual Map

```mermaid
flowchart TD
    A["回读 Step 5 正文"] --> B["标记 reading-power debts"]
    B --> C["判断本章缺的是压力 / 钩子 / 微兑现 / 章末牵引"]
    C --> D["从共享 taxonomy 选 tactic bundle"]
    D --> E["重写章内推进与局部满足"]
    E --> F["补强章末主钩"]
    F --> G["回查是否过量、失真或越权"]
```

```mermaid
flowchart LR
    A["无压力但有事件"] --> B["补选择 / 代价 / 未知"]
    C["章内一直拖延"] --> D["补 micro-payoff"]
    E["有高光没余味"] --> F["补 aftermath 与 reader pull"]
    G["章末平收"] --> H["选 crisis / mystery / desire / choice / emotion 主钩"]
```

```mermaid
stateDiagram-v2
    [*] --> Reread
    Reread --> Diagnose
    Diagnose --> BundleSelected
    BundleSelected --> RewriteCommitted
    RewriteCommitted --> EndingAudited
    EndingAudited --> Passed
    EndingAudited --> ReworkCurrent
    ReworkCurrent --> Diagnose
```

## Thinking-Action Network

| node_id | field_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-ROOT-REREAD` | `FIELD-RP6-01` | 回读当前正文与 chapter 债务 | 读取 Step 5 结果、chapter board、写作日志 | `input_note` | -> `N2` | 正文最新 |
| `N2-DEBT-SCAN` | `FIELD-RP6-02` | 扫描追读力缺口 | 标记平段、弱钩、无兑现段、收束过平段 | `debt_scan` | -> `N3` | 缺口具体 |
| `N3-BUNDLE-SELECT` | `FIELD-RP6-03` | 选择重写策略包 | 从共享 taxonomy 选择 hook / payoff / cool-point 组合 | `bundle_note` | -> `N4` | 组合不过载 |
| `N4-INNER-REWRITE` | `FIELD-RP6-04` | 重写章内推进 | 补压力梯度、微兑现、场面推进和转折落点 | `rewrite_note` | -> `N5` | 章内不再平推 |
| `N5-ENDING-PULL` | `FIELD-RP6-05` | 审核并补强章末牵引 | 选主钩、显代价、留后续欲望 | `ending_pull_note` | -> `N6` | 章末有单一主牵引 |
| `N6-REGRESSION-GUARD` | `FIELD-RP6-06` | 防失真与防过量 | 检查越权加戏、钩子过载、只留坑不兑现 | `guard_note` | done | 不违背因果 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-RP6-01` | 当前正文与债务输入 | 已回读 Step 5 正文与当前 chapter 债务 | `FAIL-RP6-01` | `N1` |
| `FIELD-RP6-02` | 追读力缺口扫描 | 已定位平段 / 弱钩 / 无兑现 / 平收位置 | `FAIL-RP6-02` | `N2` |
| `FIELD-RP6-03` | tactic bundle | 已选出适配当前章的 hook / payoff / pattern 组合 | `FAIL-RP6-03` | `N3` |
| `FIELD-RP6-04` | 章内强化版正文 | 章内至少有清晰推进与局部满足 | `FAIL-RP6-04` | `N4` |
| `FIELD-RP6-05` | 章末 pull | 章末存在单一主钩且能拉向下一章 | `FAIL-RP6-05` | `N5` |
| `FIELD-RP6-06` | regression guard | 无越权加戏、无钩子过载、无纯口号式激烈 | `FAIL-RP6-06` | `N6` |

## Completion Contract

- 当前正文已从“张力修辞”升级为“追读力结构”。
- 本章能明确说出当前主钩、主要微兑现和章末续读牵引。
- `process_log_entry` 已记录本次选择了哪些 tactic bundle。
