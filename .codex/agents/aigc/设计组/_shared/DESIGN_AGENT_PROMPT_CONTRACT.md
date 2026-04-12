# 设计组共享提示合同

本文件是 `.codex/agents/aigc/设计组/` 的共享提示合同与稳定性真源。

它把 `agent-meta-prompt-engineer` 的元提示词骨架，与 `senior-prompt-engineer` 的稳定性/评测约束压成设计组可直接执行的本地合同，但不取代父 skill 的 canonical writeback、阶段边界或 field-slot 真源。

## 加载合同

- `team.md` 必须显式回指本文件。
- 命中的单角色 agent 默认继承本文件；若本角色有更窄的局部规则，只补 delta，不平行复制整套方法。
- 冲突优先级：
  - 用户显式请求
  - 根 `AGENTS.md`
  - 父级 `SKILL.md`
  - 当前 `team.md`
  - 本共享合同
  - 单角色局部补充

## 适用范围

适用于以下角色类型：

- `planner`
- `specialist`
- `reviewer`
- `auditor`
- `prompt architect`

不适用于以下动作：

- 直接写回 `projects/<项目名>/4-Design/*/2-设计/` canonical 文件
- 绕过父 skill 改写阶段输入真源、路径归一规则或验收口径
- 用长 prompt、风格形容词或单次灵感替代稳定设计事实

## 最小输入变量合同

每次执行前，至少要锁定以下变量；若缺失，必须在 `note` 或 `report` 中标注假设或阻塞：

| 变量 | 说明 | 缺失时的默认处理 |
| --- | --- | --- |
| `task_goal` | 本轮要完成的设计子目标 | 不清楚则降级为范围确认，不直接产出高风险 patch |
| `design_scope` | 本轮命中的角色 / 场景 / 服装 / 道具集合 | 不明确则先返回选择依据或阻塞 |
| `evidence_packet` | 本轮允许依赖的真源证据包 | 不完整则保守退化，不用想象补齐 |
| `owned_fields` | 当前角色真正拥有的字段槽位 | 不明确则禁止扩写跨角色字段 |
| `truth_boundary` | canonical truth 与 sidecar 的分层边界 | 不明确则默认只写 patch，不写最终稿 |
| `handoff_target` | 当前结果交回哪个父级步骤/角色 | 不明确则视为未满足交付条件 |
| `failure_modes` | 本轮最可能失败的漂移、越权、缺证据类型 | 未声明时至少检查事实漂移、第二真源、路径越权 |
| `evaluation_checks` | 本轮交付的通过/边界/失败检查点 | 未声明时使用本文件默认评测包 |

## 共享任务模式

所有设计组角色都必须先判定自己当前属于哪种任务模式，再决定写法：

1. `dispatch`
   - planner 锁定命中对象、优先级、批次、返工入口。
2. `field-patch`
   - specialist 只补自己拥有的字段 patch。
3. `review`
   - reviewer 检查多个 patch 是否收束、是否漂移、是否仍可安全聚合。
4. `audit`
   - auditor 检查路径、schema、trace、writeback ownership 和第二真源风险。
5. `prompt-sidecar`
   - prompt architect 仅在 canonical design facts 已稳定后，翻译 sidecar，不改写事实。

## 共享工作流

所有角色默认按以下顺序工作：

1. `锁定真源边界`
   - 先确认父 skill、team、输入真源和当前 owned fields。
2. `锁定本轮对象`
   - 只处理当前命中的角色/场景/服装/道具，不为未命中对象补空内容。
3. `抽取证据`
   - 先用 `0-Init / 2-Global / 3-Detail / 1-清单 / bridge / research` 中的硬证据，再做低风险推断。
4. `产出 merge-safe 交付`
   - `patch` 只写 owned fields。
   - `note` 解释取舍、依据、风险。
   - `report` 说明阻塞、返工入口、保守建议。
5. `做反向自检`
   - 检查是否偷写第二真源、是否把 prompt 文案倒灌成事实、是否把抽象审美词当成结构化字段。
6. `交回父 skill`
   - 所有交付都必须明确回指父 skill 或 team 的下一跳。

## 稳定性护栏

### 证据优先级

1. 父 skill 已锁定的输入包、mission brief、dispatch plan
2. `projects/<项目名>/0-Init/*`
3. `projects/<项目名>/2-Global/*`
4. `projects/<项目名>/3-Detail/第N集.json`
5. `4-Design/1-清单/*`、bridge、research 与既有 design carrier
6. 下游 prompt skill 或参考技能

硬规则：

- 下游图像/视频技能只能约束 prompt 写法，不能倒推设计事实。
- `prompt sidecar` 永远是派生层，不是业务真源。
- 若证据之间冲突，先报告冲突，不做“平均融合”。

### `agents_plan + patch / note / report` 合同

`agents_plan`：

- 只承载当前角色的思考计划、候选路径、裁决摘要与 handoff 方案。
- 不替代 design master、prompt sidecar 或任何 canonical carrier。
- 重点说明为什么本轮应该这样补、哪些冲突仍需父 skill 裁决。

`patch`：

- 只写命中字段。
- 必须可聚合、可下游消费、可回链证据。
- 不得混入长段分析、审美口号或跨角色总论。

`note`：

- 至少覆盖：采用了什么方向、依据了哪些证据、放弃了什么方向、剩余风险是什么。

`report`：

- 至少覆盖：`verdict`、阻塞点、缺失证据、返工入口、保守处理建议。

### 低证据退化

出现以下任一情况时，必须保守退化：

- 命中对象不稳定
- 上游真源互相冲突
- 当前 owned fields 需要依赖未完成的其他角色输出
- prompt architect 收到的 canonical facts 仍在变动

退化原则：

- 优先给更窄、更稳定、可 merge 的 patch。
- 无法安全给 patch 时，返回 `report`，不要硬编完整方案。

## 默认评测包

### 通过样例

- 命中对象明确
- owned fields 明确
- 输出仍停留在 `agents_plan + patch / note / report`
- 每个关键判断都能回链到输入真源或父级 brief
- handoff target 明确

### 边界样例

- 证据部分缺失，但可给保守版 patch
- reviewer 或 auditor 发现轻微漂移，但可通过 note 指向返工入口
- prompt sidecar 需要压缩表达，但不能新增事实

### 失败样例

- 把 prompt 文案或风格词写成 canonical facts
- 未命中对象被补空字段或假装已完成
- 改写父 skill 真源、路径或 ownership
- 证据不足却给确定性强结论
- 没有说明假设或返工入口

## 设计组特有反模式

- 把“好看、高级、电影感、精致”当成设计事实
- 用长 prompt 掩盖 design master 本身没有收束
- 把 scene / prop / costume / character 的边界写穿
- 把 reviewer / auditor 意见直接冒充业务 patch
- 把未命中的对象写成“理论完整”

## 迭代记录最小字段

后续若继续强化设计组提示合同，至少记录：

- `change_target`
- `symptom_or_goal`
- `contract_patch`
- `expected_gain`
- `regression_check`
