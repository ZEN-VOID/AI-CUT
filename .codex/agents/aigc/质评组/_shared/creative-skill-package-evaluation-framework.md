# 创作型技能包综合质量评估共享框架

## 1. 适用范围

本文件是 `质评组` 的共享真源，用于评估“创作类型技能包”是否同时具备：

1. 清晰稳定的契约治理。
2. 可复用的创作能力上限。
3. 可运行、可返工、可观测的工程执行面。
4. 可持续升级、不易失控的演化能力。

本框架服务的对象不是单次生成结果，而是能长期驱动创作任务的技能包系统，包括但不限于：

- 根技能、阶段技能、受治理子技能
- `SKILL.md`、`CONTEXT.md`、`references/`、`subtypes/`
- 共享模板、schema、runbook、validator、脚本
- 与技能树绑定的 harness 编排与运行时契约

## 2. 真源治理声明

- 本文件是“创作型技能包综合质量评估”的共享维度真源。
- 面向具体领域的评估专家，只允许在本文件基础上增加领域增量，不得平行重写一套新的总维度系统。
- 若未来有多个创作技能树共用同一套四层评估结构，应继续回收本文件，而不是在各 agent 文档中复制演化。

## 3. 评估哲学

评估创作型技能包时，默认回答四个问题：

1. 这套技能包的结构与治理，是否足够清晰、稳定、无歧义。
2. 这套技能包是否真的能稳定产出高质量创作，而不是只会写漂亮合同。
3. 这套技能包是否具备可执行的工程运行面，而不是依赖操作者猜测。
4. 这套技能包是否能在后续升级中持续演化，而不是每次改动都引入第二真源或结构漂移。

## 4. 四层维度体系

### 4.1 契约治理层

核心问题：这套技能包的结构与真源关系是否成立。

必查子维度：

- 目录结构合理性
- 父子层级设计科学性
- 单一真源与 canonical landing
- 路由清晰度与进入条件
- 术语、职责、输出合同的无歧义性
- 隐藏第二真源风险
- 抗漂移与跨层同步质量

高危失效信号：

- 根技能、子技能、shared carrier 同时定义同一条规则
- 目录很多，但无法回答“从哪里进入、最终写回哪里”
- `references/`、`subtypes/`、模板之间职责重叠
- 同一结构在多个 sibling 中平行复制演化

### 4.2 创作能力层

核心问题：这套技能包是否真的具备可复用的创作能力上限。

必查子维度：

- 创作目标命中与结果质量
- 创作技法深度与表达密度
- 风格控制能力与审美一致性
- 类型化处理策略的完整性与区分度
- 知识库本身质量
- 知识调用方式与装载策略
- 生成结果的稳定上限与复现性

高危失效信号：

- 规则很长，但对作品质量没有可见提升
- 只会给原则，不会给可执行技法
- 类型化处理只停留在标签命名，没有进入路由与产出差异
- 知识库堆很多材料，但没有明确调用入口与停用条件
- 单次效果好，重复执行明显失稳

### 4.3 工程运行层

核心问题：这套技能包是否具备可持续运行的工程支撑。

必查子维度：

- `CONTEXT.md` 的知识库质量
- 上下文装载策略与最小必要加载
- harness 编排质量
- 可观测性与诊断入口
- 返工入口与 repair entry
- 验证链路与回归检查
- 冗余控制与重复逻辑收敛

高危失效信号：

- `CONTEXT.md` 是流水账，不是知识库
- 执行顺序只能靠操作者自行猜
- 出错后没有明确 repair entry
- 有 validator 名义，但不对应真实门禁
- 多个脚本、模板、runbook 做同一件事

### 4.4 演化持续层

核心问题：这套技能包是否便于后续升级，而不是越改越脆。

必查子维度：

- 关键部位可替换性
- 局部升级能力
- 调优成本与改动半径
- 版本兼容与迁移成本
- 经验沉淀机制
- 从经验到规范的晋升路径

高危失效信号：

- 改一个阶段必须同时手改多个 sibling
- 增加新 subtype 会破坏既有路由
- 成功/失败经验无法回写真源
- provider、模型、模板升级只能靠人工全局搜改

## 5. 证据策略

### 5.0 静态评估与动态评估双轨制

- 静态评估：评估 `SKILL.md`、`CONTEXT.md`、`references/`、`subtypes/`、模板、schema、runbook、validator、shared carrier。
- 动态评估：评估真实任务运行、代表性输出、回放结果、重复执行稳定性、返工成本与回归表现。
- 默认结论必须显式说明：当前结论是 `静态成立`、`动态成立`，还是 `静态成立但动态未验真`。
- 任何“稳定高质量”结论都不应只基于静态文档。

### 5.1 最小证据束

至少应读取：

- 目标 `SKILL.md`
- 同层 `CONTEXT.md`（若存在）
- 相关 `references/`、`subtypes/`、模板、schema、runbook、脚本

### 5.2 增强证据束

如要评估创作能力层或稳定上限，应尽量补充：

- 代表性输出样本
- 任务回放证据
- validator / audit 结果
- 用户反馈或回归记录

### 5.3 证据不足的评分约束

- 若缺少真实输出或回放证据，创作能力层最高不应直接判到“优秀”。
- 若缺少验证链路或运行证据，工程运行层的“稳定上限”相关判断必须降置信度。
- 若仅有文档、没有执行证据，允许做合同级评估，但必须明确标注“未完成运行侧验真”。

### 5.4 证据等级

| level | 名称 | 说明 | 允许支撑的结论上限 |
| --- | --- | --- | --- |
| `L0` | doc-only | 仅有合同文档与静态结构 | 只允许做静态成立判断 |
| `L1` | doc-plus-sample | 文档 + 样例或展示材料 | 可做低置信度创作判断 |
| `L2` | single-run | 文档 + 单次真实运行 | 可做单轮可用性判断 |
| `L3` | replay-validated | 多次回放或回归验证 | 可做稳定性判断 |
| `L4` | cross-context-validated | 跨题材、跨任务、跨版本验证 | 可做推广级判断 |

## 6. 评分与门禁

### 6.1 评分结构

- 契约治理层：`0-25`
- 创作能力层：`0-30`
- 工程运行层：`0-25`
- 演化持续层：`0-20`
- 总分：`100`

### 6.2 硬门禁

- 契约治理层 `< 15`：`FAIL-COVENANT`
- 出现隐藏第二真源且影响执行：`FAIL-COVENANT`
- 无法回答 canonical landing 或 repair entry：至少 `PASS-WITH-REWORK`
- 创作能力层证据严重不足时，不得给出“稳定高质量”结论
- 若仅达到 `L0-L1` 证据等级，不得推荐进入 `R3-R4` 发布级别

### 6.3 分档锚点

#### 差

- 结构混乱，真源不清，创作规则无法稳定驱动结果
- 工程层缺少可执行入口，升级风险高

#### 一般

- 有基本框架，但创作、工程、演化至少一层明显虚弱
- 可以用，但需要大量人工补脑与手工兜底

#### 好

- 四层基本成立，能支撑重复执行
- 仍有少量同步、证据或演化成本问题

#### 优秀

- 真源清楚，创作能力强，运行面稳定，升级路径明确
- 评估结论能直接转成高杠杆升级动作

## 7. 反投机机制

以下情况必须重扣分或直接触发返工：

- 用长 prompt 掩盖目录、路由与真源缺失
- 用大量术语掩盖创作技法贫弱
- 用大体量知识库掩盖没有有效调用策略
- 用“支持持续升级”的口号掩盖不可替换结构
- 用格式完整的评分卡掩盖证据不足

## 8. 横切专项检查

除四层主评分外，还必须执行以下横切检查：

### 8.1 路由质量专项

检查：

- 命中率：是否能把任务路由到正确阶段/子技能
- 错路由率：是否频繁进入错误模块
- 过路由率：是否把简单任务过度拆分
- 漏路由率：是否遗漏必要子技能
- 回写正确率：子技能输出是否正确回流共享目标

### 8.2 知识拓扑专项

检查：

- 哪些知识应该留在 `SKILL.md`
- 哪些经验应沉到 `CONTEXT.md`
- 哪些共用规则应上收 shared carrier / template / schema
- 哪些材料只是 sidecar 或参考样本

若知识放错层，即使内容本身不错，也必须扣分，因为这会直接损害可维护性。

### 8.3 质量上限与质量下限专项

必须分别判断：

- 质量上限：最佳条件下能做到多好
- 质量下限：在普通任务、普通操作者、普通上下文下最低能稳到什么程度

高上限但极不稳，不能等同于高质量技能包。

### 8.4 反作弊专项

建议至少使用以下方法之一做对抗性检查：

- 改写任务表述后重跑
- 缩减非必要上下文后重跑
- 更换题材或约束条件后重跑
- 使用隐藏 benchmark task 做抽查

## 9. 基准任务集合同

高成熟度评估应尽量依赖 benchmark suite，而不是只靠人工阅读合同。

推荐最小任务集类型：

- `baseline`：常规标准任务
- `boundary`：边界条件任务
- `stress`：高复杂度或高负荷任务
- `adversarial`：对抗性或投机性任务
- `regression`：历史失败模式回归任务

每个 benchmark task 至少应声明：

- `task_id`
- `task_type`
- `goal`
- `input_profile`
- `expected_properties`
- `checks`
- `pass_threshold`
- `evidence_paths`

共享模板与 schema 真源：

- 模板：`.codex/templates/quality-evaluation/creative-skill-package-benchmark-suite.yaml`
- schema：`.codex/schemas/creative-skill-package-benchmark-suite.schema.yaml`

## 10. 发布级别合同

综合评估不应只输出 `PASS/FAIL`，还应推荐发布级别。

发布级别真源：`.codex/agents/质评组/_shared/creative-skill-package-release-levels.md`

## 11. 输出合同

固定优先输出“分层评分卡 + 高杠杆改进动作”。

```yaml
evaluation_meta:
  evaluator: ""
  scope: ""
  target_paths: []
  confidence: high|medium|low
  evaluation_mode: static|dynamic|hybrid
  evidence_level: L0|L1|L2|L3|L4
  output_landing: reports/

type_profile:
  package_kind: creative-skill-package
  domain: ""
  target_runtime: ""
  primary_truth_source: ""
  comparison_baseline: ""

layer_scorecard:
  covenant_governance:
    score: 0
    max_score: 25
    band: 差|一般|好|优秀
    evidence: []
    findings: []
  creative_capability:
    score: 0
    max_score: 30
    band: 差|一般|好|优秀
    evidence: []
    findings: []
  engineering_operation:
    score: 0
    max_score: 25
    band: 差|一般|好|优秀
    evidence: []
    findings: []
  evolution_sustainability:
    score: 0
    max_score: 20
    band: 差|一般|好|优秀
    evidence: []
    findings: []

improvement_priorities:
  - priority: P0|P1|P2
    layer: covenant_governance|creative_capability|engineering_operation|evolution_sustainability
    issue: ""
    action: ""
    landing_point: ""
    expected_gain: ""

gate_summary:
  verdict: PASS|PASS-WITH-REWORK|FAIL-COVENANT|FAIL-QUALITY
  total_score: 0
  max_score: 100
  top_risk: ""
  anti_gaming_flags: []
  repair_entry: ""
  recommended_release_level: R0|R1|R2|R3|R4

closure:
  root_cause_location: ""
  immediate_fix: ""
  systemic_prevention_fix: ""
  layered_trace:
    symptom: ""
    direct_cause: ""
    rule_source: ""
    meta_rule_source: ""
    fix_landing_points: []
```

## 12. 标准工作流

1. 锁定评估对象与作用域。
2. 先判本轮是静态评估、动态评估还是双轨混合评估。
3. 收集最小证据束，并判断证据等级。
4. 若存在 benchmark suite，优先按 benchmark 运行。
5. 先判契约治理层，再判创作能力层。
6. 再判工程运行层与演化持续层。
7. 执行路由质量、知识拓扑、质量上限/下限与反作弊专项检查。
8. 结合证据等级与专项检查，给出发布级别建议。
9. 标记证据不足导致的置信度上限。
10. 输出前 `1-3` 个最高杠杆改进项，不平均发力。
11. 若命中结构漂移或升级困难，必须补 `layered trace`：
   - `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

## 13. 完成信号

一次评估完成，至少应满足：

- 能明确指出四层中最强与最弱的一层
- 能明确回答为什么当前还达不到更高档
- 能指出最高杠杆的修复动作与落点
- 能说明结论依赖了哪些证据、哪些层仍缺运行验真
- 能说明当前建议发布级别，以及为什么不是更高一级
