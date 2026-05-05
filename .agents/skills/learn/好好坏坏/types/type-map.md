# Example Contrast Type Map

本文件是 `好好坏坏` 的类型策略层。执行前先根据好/坏差异选择一个或多个类型包，再进入 `steps/`。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `output-quality-contrast` | `types/output-quality-contrast/` | 好坏主要表现为表达质量、结构完整度、细节密度、风格和任务完成度差异 | stackable | `types/output-quality-contrast/output-quality-contrast.md` | none | none |
| `source-fidelity-contrast` | `types/source-fidelity-contrast/` | 好坏主要表现为是否忠实资料、是否错引、是否幻觉、是否遗漏输入证据 | stackable | `types/source-fidelity-contrast/source-fidelity-contrast.md` | none | none |
| `workflow-routing-contrast` | `types/workflow-routing-contrast/` | 好坏主要来自模式选择、子技能路由、阶段顺序、类型包命中或上下文加载差异 | stackable | `types/workflow-routing-contrast/workflow-routing-contrast.md` | none | none |
| `template-schema-contrast` | `types/template-schema-contrast/` | 好坏主要来自输出字段、命名、路径、schema、模板或机器可消费性差异 | stackable | `types/template-schema-contrast/template-schema-contrast.md` | none | none |
| `review-gate-contrast` | `types/review-gate-contrast/` | 坏示例本应被验收门拦截，或好示例体现了可复用 review 标准 | stackable | `types/review-gate-contrast/review-gate-contrast.md` | none | none |

## Selection Rules

1. 若用户没有显式说明差异类型，默认加载 `output-quality-contrast`。
2. 只要涉及资料事实、输入证据或参考来源，叠加 `source-fidelity-contrast`。
3. 只要坏示例来自错误阶段、错误模式、缺上下文或错误技能路线，叠加 `workflow-routing-contrast`。
4. 只要差异会影响下游消费、脚本读取或固定输出合同，叠加 `template-schema-contrast`。
5. 只要坏示例应被验收拦截而没有拦截，叠加 `review-gate-contrast`。

## Default Package Rule

1. 若用户没有显式指定类型包，默认加载 `output-quality-contrast`。
2. 若任务要求或示例涉及资料、事实、来源、引用、输入证据，必须叠加 `source-fidelity-contrast`。
3. 若好/坏示例的差异来自阶段、路线、上下文加载或技能调度，必须叠加 `workflow-routing-contrast`。
4. 若输出需要被下游工具、模板、schema 或固定路径消费，必须叠加 `template-schema-contrast`。
5. 若坏示例代表验收漏检，必须叠加 `review-gate-contrast`。

## Loading Flow

1. `N1-LOCK-CONTRAST-TASK` 收集目标 skill、任务环节、好/坏示例、任务要求和资料来源。
2. 读取本文件，依据 `Selection Rules` 与 `Default Package Rule` 生成 `type_profile`。
3. 加载 `type_profile.selected_packages` 对应的 `context_files` 作为固定上下文。
4. `steps/good-bad-learning-workflow.md` 消费已加载类型包，进入好/坏诊断和源层 owner 裁决。
5. 需要补充稳定经验时，从 `knowledge-base/good-bad-heuristics.md` 按需检索。
6. 交付前由 `review/review-contract.md` 检查类型选择、源层落点、过拟合风险和验证证据。

## Type Profile Shape

```yaml
type_profile:
  selected_packages: []
  match_evidence: []
  primary_contrast_axis: ""
  secondary_axes: []
  review_implications: []
```
