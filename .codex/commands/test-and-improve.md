# /test-and-improve

用于在一次优化、修复、重构或规则改写之后做针对性验证；如果验证失败，继续进入“测试 -> 诊断 -> 源层修复 -> 复测”的连续迭代闭环。

## 何时使用

- 一轮默认的优化、修复或规则改写刚结束，需要根据当前上下文做针对性验证。
- 用户明确要求“测一下”“验证是否真的修好”“看看有没有引发别的问题”“继续迭代优化”。
- 现有自动化测试不存在、太粗、或不能覆盖这次变更最关键的实例风险。
- 本轮修改涉及 `SKILL.md`、`CONTEXT.md`、runbook、模板、脚本、validator、workflow 入口等源层工件。

## 输入

- 必需输入：
  - 本轮刚完成的变更声明：修了什么、优化了什么、预期修复什么问题
  - 至少一个与本轮变更直接相关的实例、样例或失败症状
  - 受影响的工件路径、命令入口或运行面
- 可选输入：
  - 已有测试命令、日志、报错、用户反馈
  - 邻近风险面、已知历史回归点、性能或质量约束
- 禁止输入：
  - 只说“帮我测一下”却不基于当前上下文收束测试目标
  - 只跑泛化全量测试，不验证本轮变更真正命中的实例
  - 发现失败后只修表层产物，不上溯到源层规则或入口

## 根因优先

- 固定上溯链：`Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`
- `Rule Source` 默认优先检查：
  - 当前变更涉及的 `SKILL.md`
  - `CONTEXT.md`
  - runbook / template / validator / workflow 脚本
  - 明确的执行入口
- `Meta Rule Source` 默认优先检查：
  - `AGENTS.md`
  - `.agents/skills/meta/` 下相关 meta skill 合同
  - 仓库级共享治理约束
- 失败时优先修复高杠杆源层，不允许只修本次输出表象后宣布完成。

## 决策方法

### Base Range

先根据本轮变更类型确定验证主面：

- `bugfix` -> 失败复现 + 修复实例 + 最邻近回归点
- `optimization` -> 目标收益实例 + 负面副作用实例 + 性能/质量守门实例
- `refactor` -> 行为等价实例 + 入口兼容实例 + 关键边界实例
- `skill/rule update` -> 触发命中实例 + 合同遵循实例 + 验证/运行时实例

### Range Narrowing

- 用户刚反馈的症状是否仍可复现
- 本轮改动涉及的文件是否属于源层关键入口
- 是否已有现成命令/脚本/测试可直接复用
- 是否存在明显的相邻回归风险

### Final Selection

输出一个明确的最小执行包：

- `targeted-example-check`
- `focused-regression-check`
- `source-layer-contract-check`
- `hybrid-check`

## 标准流程

1. 重建本轮变更合同：明确“声称修好了什么”。
2. 选 1-3 个高信号实例：至少包含一个主命中实例；若风险明显，再补一个边界或回归实例。
3. 先做最小可执行验证：优先复用已有命令、脚本、dry-run、局部检查。
4. 若失败：立即执行分层上溯，找出 `Direct Cause -> Rule Source -> Meta Rule Source`。
5. 优先修源层：先修 `SKILL.md`、`CONTEXT.md`、runbook、template、validator、entrypoint 等高杠杆源点。
6. 复测同一实例：先验证原失败点已被消除。
7. 扩测相邻风险：只补跑与本轮修改最接近的回归面。
8. 输出闭环：`root cause location + immediate fix + systemic prevention fix + layered trace path`

## 连续迭代规则

- 允许连续多轮重复执行，直到满足以下任一停止条件：
  - 主实例通过，且相邻高风险实例未出现新问题
  - 已达到明确 blocker，需要人工提供缺失输入或外部依赖
  - 连续两轮没有新的源层信息增量
- 每一轮都必须有新的验证目标、新的根因收束或新的源层增强；禁止空转。

## 输出模板

### JSON-first

```json
{
  "schema_version": "test-and-improve/v1",
  "meta": {
    "command_id": "test-and-improve",
    "iteration_index": 1,
    "change_type": "bugfix|optimization|refactor|skill-update",
    "scope_refs": [],
    "target_surface": "targeted-example-check|focused-regression-check|source-layer-contract-check|hybrid-check"
  },
  "content": {
    "validation_examples": [],
    "commands_or_checks": [],
    "findings": [],
    "layered_trace": [],
    "improvement_actions": [],
    "rerun_decision": "rerun-now|rerun-next-iteration|blocked"
  },
  "gate_summary": {
    "status": "PASS|FAIL|BLOCKED",
    "fail_codes": [],
    "repair_entry": null
  }
}
```

### 口头总结

- 根因位置
- 立即修复
- 系统预防修复

## 验证通过标准

- 至少有 1 个与本轮变更直接相关的主命中实例。
- 一旦出现失败或回归，已经给出分层上溯链与源层优先修复方案。
- 已复测原失败实例，并按风险补测必要的相邻实例。
- 若仍未完成，明确进入下一轮迭代，而不是把未验证状态包装成完成。

## 稳定经验

- 先压缩到 1 个主命中实例，再逐步扩开，比默认全量回归更稳。
- 如果本轮修改碰到了 `SKILL.md`、模板、validator、runbook 或 entrypoint，默认按源层问题处理。
- 复测顺序固定为“原失败点 -> 相邻风险面”。
- 若守门器、validator 或 cleanup 逻辑依赖人类可读 git 输出，至少补 1 个中文或其他非 ASCII 路径实例。
