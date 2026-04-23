---
name: next
governance_tier: lite
description: 用于刷新编号技能树或工作流目录下游交互合同的命令型 skill。
---

# /next

## Context Loading Contract

- 每次命中本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次命中本技能时，必须同时加载本文件与同目录 `CONTEXT.md`。

用于维护编号技能树或工作流目录的下游路由。当目录顺序、阶段关系或叶子技能交互提示发生漂移时，刷新目标目录下的 `## Interaction` 段落。

## 何时使用

- 新增、重排、拆分、合并一组带编号的技能目录后，需要同步下游提示。
- 需要把旧命令文档或旧路由提示迁移为当前仓库可执行的交互合同。
- 需要让一组编号技能在完成后给出清晰的下一步、并行分支、返回路由器或终点动作。

## 输入

- 必需输入：
  - 一个目标根目录，例如 `.agents/skills/story/stages/3-Drafting`
  - 该目录对应的组级 `SKILL.md` 或上游合同
- 可选输入：
  - 用户指定的额外提示语、耗时说明、推荐顺序说明
  - 明确覆盖默认编号推断的路由规则
- 禁止输入：
  - 只给一个散乱目录，不给任何上游合同，就强行发明下游关系
  - 沿用外部工程残留，如 `AskUserQuestion`、旧项目命令名或失效路径

## 颗粒度约定

- 若目标路径本身是叶子技能目录，直接在该目录级别配置 `Interaction`。
- 若目标路径是组级目录或大目录，默认先读组级 `SKILL.md`，再扫描其直接子技能目录，最终在每个子技能目录级别写入或刷新 `Interaction`。
- 只有当用户显式说明“只更新组级路由器”时，才允许停在当前目录。

## 根因优先

- 先修规则源，再修叶子文件。若下游关系不清，先回查组级 `SKILL.md`、`_shared` 合同、阶段总路由，再决定是否写入子技能。
- 固定上溯链：`症状/漂移 -> 直接技术原因 -> 组级或共享合同 -> AGENTS.md / 仓库元规则`
- 若上层合同本身没有定义某段路由，不得伪造“看起来合理”的下一步；应显式报告空缺，并把修复落点指回源层合同。

## 决策方法

下游关系必须三层收敛，不允许“看到编号就盲跳下一号”：

1. 粗裁决：先读目标组级 `SKILL.md`，提取显式定义的路由、耦合关系、禁止跳转和终点条件。
2. 细裁决：仅在上层合同未覆盖时，才使用编号顺序、同级 siblings、命名语义和已有 `Interaction` 段落做收窄。
3. 离散裁决：为每个叶子技能输出一个明确的 `trigger_type`：
   - `sequential`
   - `parallel_fork`
   - `router_return`
   - `bundle_gate`
   - `endpoint`

冲突解消：

- 显式合同永远优先于编号。
- 同级多个候选都成立时，优先选择更保守、返工更少、与下游消费者更一致的路径。
- 若无交集，保留上层合同并报告缺口，不做隐式 override。

## 默认推断规则

### 通用编号规则

- 目录名优先识别 `^\\d+-`、`^\\d+\\.\\d+-`、`^\\d+\\.\\d+\\.\\d+-`。
- 同一父目录下，按数值顺序排序，不按字典序排序。
- `_shared`、`templates`、`references`、`assets` 这类支撑目录不计入下游候选。
- 默认语义基线：
  - 有数字序号的子技能目录，默认优先视为 `sequential`
  - 无数字序号的子技能目录，默认优先视为 `parallel_fork` 或 `router_return`

### `story2026` 顶层阶段链

- `0-Init -> 1-Cards -> 2-Planning -> 3-Drafting -> 4-Polish -> 5-Validation -> 6-Loopback`

### `1-Cards`

- `1-Cards` 是组级路由器，不应把卡族强行串成线性流水线。
- 叶子卡族技能若缺显式下游，默认优先提供返回组级路由器，或进入当前任务真正需要的下一个卡族。

### `2-Planning`

- `2-Planning` 默认只有一个对外入口：组级 `SKILL.md`。
- 所有 leaf 子目录默认视为内部 planning pass，不应在用户只说“进入 2-Planning”时被直接当成首入口。
- 优先读取组级 `SKILL.md` 中的组合逻辑，而不是单纯 `1 -> 2 -> 3 -> 4 -> 5`。
- 默认强耦合：`1-章节 -> 2-事件`
- 默认可分叉：`2-事件 -> 3-节奏 / 4-悬念 / 5-伏笔`

### `3-Drafting`

- 必须服从组级合同，不得只按数字邻接推断。
- 默认主链：`1-draft-packet -> 2-prose-contract -> 3-draft-render`
- 默认阶段 handoff：`3-draft-render -> 4-Polish`

### `4-Polish`

- 默认主链：`1-rough-polish -> 2-surface-polish -> 3-manuscript-lock`
- 默认阶段 handoff：`3-manuscript-lock -> 5-Validation`

### `5-Validation`

- `5-Validation` 默认是专项并行，不是线性串行。
- 默认强耦合：
  - `continuity <-> timeline`
  - `character <-> logic`
  - `structure <-> logic`

### `6-Loopback`

- 默认主链：`1-outcome-extract -> 2-card-writeback -> 3-map-actualization -> 4-context-refresh`
- 只有 `PASS` 后才允许进入本阶段。

## 标准流程

1. 读取目标根目录的组级 `SKILL.md`，锁定显式耦合规则和禁止跳转。
2. 判断目标根目录是叶子技能目录还是大目录/组级目录。
3. 若是大目录，扫描其直接子技能目录，过滤 `_shared` 与资源目录。
4. 为每个目标子技能建立 `next_route_table`：
   - `source_path`
   - `trigger_type`
   - `recommended_target`
   - `secondary_targets`
   - `evidence`
5. 替换已有 `## Interaction` 段落；若不存在则追加一个。
6. 汇总更新、跳过项和无法确定项。

## Interaction 合同

写回叶子技能时，统一使用仓库内的中性合同：

```md
## Interaction

```yaml
interaction_contract:
  trigger_type: sequential|parallel_fork|router_return|bundle_gate|endpoint
  header: 下一步|下游选择|流程完成
  question: 当前技能完成后，下一步要进入哪里？
  preferred_runtime: request_user_input
  fallback_runtime: plain_message_single_question
  options:
    - label: 进入 [下游名] (Recommended)
      description: [为什么这是默认推荐]
      target_hint: [目录或技能名]
    - label: 返回组级路由器
      description: [当本轮仍需重新裁决下游时使用]
```
```

要求：

- 若当前运行模式支持结构化提问，优先用 `request_user_input`。
- 若当前模式不支持，则保留同样的 `header/question/options`，改为一条普通中文单题消息发问。
- 不写 `AskUserQuestion`、`/aigc-*`、`.codex/*` 或其他外部工程残留。

## 验证

- 所有 `target_hint` 都指向真实存在的目录或真实技能名。
- 新写入内容不再包含 `AskUserQuestion`、`/aigc-`、影视项目专属命令名。
- `story2026` 的 `1-Cards`、`2-Planning`、`3-Drafting`、`4-Polish`、`5-Validation` 与 `6-Loopback` 没有被误写成过期阶段链或旧中文 stage。
- 若发现“显式合同”和“编号顺序”冲突，报告冲突，不静默吞掉。

## 稳定经验

- 对 `story2026` 来说，“显式组级路由 > 目录编号 > 名称语义” 是默认优先级。
- `Interaction` 最稳的写法不是绑定单一提问工具，而是 `interaction_contract + runtime fallback`。
- 大目录默认完成标准应是“写到每个直接子技能目录”，而不是只更新当前目录说明。
