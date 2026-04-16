# /master-check-team

用于在不显式传入 reviewer selector 的情况下，自动针对“当前上下文中最后一个有效输出文件”建立评审团，优先读取关联项目的 `team.yaml`，再从 `.agents/skills/team/` 中匹配适合的“大师视角” reviewer，完成评审与必要优化。

## 语法

```text
/master-check-team
```

不需要后续参数。

## 何时使用

- 用户刚生成完一个文件，想马上让“顾问团/大师视角”做复盘。
- 当前上下文已经有明确目标文件，不想手工再写路径。
- 目标文件已经位于某个 `projects/aigc/<项目名>/` 下，希望自动读取该项目的 `team.yaml`。

## 自动目标选择

按以下优先级选择评审对象：

1. 当前会话中最后一个明确被创建、修改或提及的真实文件路径
2. 当前会话中最近一次输出里声明的 canonical target
3. 若以上都无法唯一确定，停止并只问一个简短问题：`要评审哪个文件？`

禁止把目录、会话摘要或纯描述文本误判成评审对象。

## 项目与 `team.yaml` 解析

确定目标文件后，向上查找最近的项目根：

- 优先命中 `projects/aigc/<项目名>/`
- 若命中项目根，读取 `<项目根>/team.yaml`
- 若目标不在项目目录下，或项目根没有 `team.yaml`，进入无 `team.yaml` 回退模式

## `team.yaml` 驱动的 reviewer 选择

若找到了 `team.yaml`，按以下优先级抽取 reviewer：

1. `team_setup.shared_agents`
2. `roles.*.members`
3. `roles.*.source_skill_refs`

抽取规则：

- 优先保留 `.agents/skills/team/` 下的 skill。
- 若 `team.yaml.enabled == false` 但存在可用 reviewer 映射，允许继续使用这些映射做一次“手动触发的评审团评审”，并说明这是手工 override。
- 若显式映射不足，再根据以下信息补齐必要 reviewer：
  - 启用的 role
  - `runtime_policy.use_subagents_by_default`
  - 目标文件类型

## 无显式 reviewer 映射时的补选规则

只在 `team.yaml` 未提供足够 reviewer 且目标确实需要评审时才使用补选。

### 文本/剧作/分镜/方案类

- 优先补：
  - 导演组 1 位
  - 编剧组 1 位
  - 视情况补摄影组或设计组 1 位

### 设计/空间/视觉系统类

- 优先补：
  - 设计组 1 位
  - 美学组 1 位
  - 视情况补导演组 1 位

### 动作/打戏/调度类

- 优先补：
  - 武术组 1 位
  - 导演组 1 位
  - 视情况补摄影组 1 位

### 只允许补 2-4 位 reviewer

- 不全量拉起整个 `team` 技能树。
- 若需要推断具体人物，必须在结论里说明这是推断选择，不是 `team.yaml` 的显式声明。

## 模式裁决

默认逻辑：

1. `team.yaml.runtime_policy.use_subagents_by_default == true` 且 reviewer 为 2-4 个
   - 优先 `parallel-council`
2. 目标明显需要链式 refine
   - 改为 `serial-refine`
3. 目标不可编辑，或更适合保留独立判断
   - 改为 `independent-only`

### Subagent Dispatch Gate

- `master-check-team` 的默认执行语义是：只要项目 `team.yaml` 给出 `runtime_policy.use_subagents_by_default: true`，且已解析出 reviewer，就应真实启动 reviewer 对应的 subagents，而不是先默认本地模拟。
- 当 reviewer 为 `2-4` 个时，subagent 分发是默认硬门槛；模式裁决只决定并行、串行还是独立，不决定“要不要真的起 subagents”。
- 仅在以下情况允许降级：
  - 当前环境无法真实使用 subagents
  - 更高优先级策略明确阻断 subagent 调度
  - 用户显式要求不要启用 subagents
- 降级时必须在输出中明确写出降级原因与替代执行方式。

若当前环境不能真实使用 subagents，或被更高优先级策略阻断：

- 显式说明降级
- 顺序读取 reviewer 的 `SKILL.md` / `CONTEXT.md`
- 生成模拟顾问纪要

## 输出裁决

默认 `output: auto`：

- 目标可编辑且上下文意图是“评审并优化” -> 直接 patch
- 目标不可编辑或风险高 -> 输出汇总建议

## 标准流程

1. 从当前会话中锁定最后一个有效输出文件。
2. 判断该文件是否处于 `projects/aigc/<项目名>/` 下。
3. 若存在项目根 `team.yaml`，先读取它。
4. 解析 reviewer：
   - 先用显式映射
   - 再做必要补选
5. 加载 `.agents/skills/team/SKILL.md`。
6. 对每个 reviewer：
   - 读取其 `SKILL.md`
   - 读取同目录 `CONTEXT.md`
7. 读取目标文件和最少必要上下文。
8. 选择执行模式。
9. 只要已解析出 reviewer 且无上层阻断，就启动 subagents：
   - 默认一个 subagent 对应一个 reviewer skill
   - 并行或串行执行
10. 主 agent 做 synthesis，并在适合时直接 patch 目标文件。
11. 输出 reviewer 来源、模式、关键结论、已实施的优化或未落盘原因。

## Subagent 合同

- 一个 reviewer skill 对应一个 subagent。
- subagent 只负责本 skill 的局部判断和建议。
- 最终写回权始终归主 agent。
- 不让 `team.yaml` 抢走 `.agents/skills/team/` 的 skill 真源职责。
- 当 `team.yaml.runtime_policy.use_subagents_by_default == true` 时，除非被上层策略阻断，否则不得把本地顺序模拟当作正常主路径。

## 输出模板

```yaml
master_check_team_result:
  inferred_target: "<path>"
  project_root: "<path-or-null>"
  team_yaml: "<path-or-null>"
  reviewer_source: "team-explicit|team-inferred|fallback-no-team"
  reviewers: []
  mode: "parallel-council|serial-refine|independent-only|single-reviewer"
  patched_target: false
  key_findings: []
  synthesis: ""
```

## Error Handling

- 若上下文中没有可唯一确定的最后输出文件：
  - 停止
  - 只问一个问题：`要评审哪个文件？`
- 若找到了项目根但 `team.yaml` 缺失：
  - 显式说明
  - 进入无 `team.yaml` 回退模式
- 若 `team.yaml` 存在但无法解析出任何可用 reviewer：
  - 先尝试基于目标类型补选 2-4 个 reviewer
  - 若仍失败，停止并说明该项目缺少可执行的 reviewer 映射

## 稳定经验

- `master-check-team` 的关键不是“完全自动”，而是“自动到足够可靠后再执行”。
- 当前上下文里“最后一个输出文件”必须是一个真实存在的文件路径，不能靠猜测。
- 即使 `team.yaml.enabled == false`，只要用户显式调用了本命令，也可以把 `team.yaml` 当 reviewer 线索源使用，但要说明这是人工触发而非常驻运行时。
- 如果 `team.yaml` 和目标类型都无法提供稳定 reviewer 线索，宁可停下来问一个问题，也不要臆造整套评审团。
