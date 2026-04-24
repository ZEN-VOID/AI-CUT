# Upgrade Point Absorption Map

本参考文件用于回答一个关键问题：

`外部升级点到底该被吸收到目标 skill 的哪里，哪些面需要同步，哪些面不该误改？`

## 1. 升级点判型表

| point_type | 常见信号 | 最佳主落点 | 必查同步面 | 不要误落 |
| --- | --- | --- | --- | --- |
| `trigger_discovery` | “这个 skill 什么时候该触发”不清、命中率低、描述失真 | frontmatter `description`、`何时使用`、registry/routes | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`、可选 `agents/openai.yaml` | 只改正文，不改发现入口 |
| `workflow_contract` | 主流程、分支、门禁、输入输出合同需要升级 | `SKILL.md` 骨架，必要时配 `references/` | 父级 skill、下游 handoff、validator/脚本消费点 | 只写进 `CONTEXT.md` |
| `heuristic_learning` | 新经验、失败模式、repair 策略、启发式 | 目标 `CONTEXT.md`；跨 skill 模式进本技能 `CONTEXT.md` | `CHANGELOG.md` | 直接提升为主合同 |
| `schema_runner` | 字段、schema、runner、validator、template 需要升级 | `references/`、shared carrier、scripts/templates | siblings、shared validator、示例输入输出 | 只改一个叶子 skill |
| `group_handoff` | 目标 skill 和父级/同级/下游之间的边界或交接变了 | 父级 `SKILL.md`、目标 `SKILL.md`、shared contract | siblings、routes、runtime layout | 只改 leaf 文案 |
| `audit_validation` | 审核方式、检查项、quality gate 要升级 | validator、review checklist、`SKILL.md` gate | scripts、审计入口、reviewer 口径 | 只在总结里口头说明 |
| `compat_migration` | 旧结构兼容、新旧路径共存、迁移中间态 | `references/` + runner/validator compat 分支 | shared carrier、CHANGELOG、兼容说明 | 在主合同里堆大量历史细节 |

## 2. 技能组上下文扫描清单

在给升级点选落点前，至少回答下面问题：

1. 目标 skill 是父技能、子技能、卫星技能，还是单目录命令型 skill？
2. 它的父级 skill 是谁？本轮升级会不会改变父级对子技能的边界定义？
3. 有哪些 siblings 在消费同一份 shared contract、schema、template、runner 或 routes？
4. 该 skill 是否已经登记到 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml`？
5. 升级点会不会改变“发现它”的方式、“调用它”的方式，或“验收它”的方式？
6. 需要把经验沉淀到目标 `CONTEXT.md`，还是应上升到更高层 shared contract？

## 3. 同步范围裁决

### 最窄有效原则

优先选择最窄但足够生效的落点；只有当升级点跨越当前 skill 边界时，才向上或向旁同步。

### 典型同步模式

- `leaf_only`
  - 只影响目标 skill 自身的局部经验或局部文案。
- `leaf_plus_parent`
  - 目标 skill 的边界、入口、交接方式改变，父级必须同步。
- `leaf_plus_siblings`
  - shared schema、shared runner、shared template 或共用检查项变动。
- `leaf_plus_registry`
  - 触发语义、技能发现方式或 route policy 变动。
- `group_level_recut`
  - 升级点已经超出单叶子，需回到父级技能重切结构。

## 4. Review Gate 触发器

满足任一项时，必须进入 `review/review-contract.md` 的 review gate，并默认采用 `code-reviewer` 口径；若上层策略、工具权限或用户授权阻断真实 reviewer/subagent dispatch，则降级为 `degraded-local-review` 并报告阻断来源。

- 修改了 `scripts/`、validator、template 或 shared carrier
- 修改了 registry/routes
- 修改了 2 个以上载体类型
- 存在 sibling parity 风险
- 用户明确要求“不要草率拼接，要有机融合”

## 5. 学习沉淀规则

- 目标 skill `CONTEXT.md`
  - 收这次升级对目标 skill 自身最有价值的局部经验。
- `北冥神功/CONTEXT.md`
  - 收跨 2+ skill 可复用的吸收模式、判型经验与 parity 教训。
- `CHANGELOG.md`
  - 收时间序变更摘要，不承载规范裁决。
