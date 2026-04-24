# Upgrade Point Type Map

本文件是 `北冥神功` 的类型策略层。执行前先形成 `type_profile`，再进入 `steps/` 分支。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `point_type` | `trigger_discovery`, `workflow_contract`, `heuristic_learning`, `schema_runner`, `group_handoff`, `audit_validation`, `compat_migration` | 升级点本质 |
| `target_role` | `root_skill`, `child_skill`, `satellite_skill`, `single_skill`, `shared_carrier` | 目标 skill 在技能组中的位置 |
| `artifact_surface` | `SKILL.md`, `CONTEXT.md`, `references`, `steps`, `review`, `types`, `templates`, `scripts`, `registry`, `routes` | 可能被修改的载体 |
| `sync_scope` | `leaf_only`, `leaf_plus_parent`, `leaf_plus_siblings`, `leaf_plus_registry`, `group_level_recut` | 同步范围 |
| `review_depth` | `light`, `standard`, `deep` | 审计深度 |

## Mapping Matrix

| point_type | primary landing | sync surface | review impact |
| --- | --- | --- | --- |
| `trigger_discovery` | frontmatter、`何时使用`、registry/routes | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`、`agents/openai.yaml` | 检查可发现性与旧触发不漂移 |
| `workflow_contract` | `SKILL.md` 骨架、`steps/`、必要 `references/` | 父级 skill、下游 handoff、模板 | 检查流程门禁、输入输出合同 |
| `heuristic_learning` | 目标 `CONTEXT.md`，跨 skill 模式进入本技能 `CONTEXT.md` 或 `knowledge-base/` | `CHANGELOG.md` | 检查经验未误升为硬规则 |
| `schema_runner` | `references/`、shared carrier、`scripts/`、`templates/` | siblings、validator、示例输入输出 | 检查脚本只做机械辅助 |
| `group_handoff` | 父级 `SKILL.md`、目标 `SKILL.md`、shared contract | siblings、routes、runtime layout | 检查边界和回接关系 |
| `audit_validation` | `review/`、validator、`SKILL.md` completion gate | 审计入口、reviewer 口径 | 检查 findings、severity、verdict |
| `compat_migration` | `references/`、runner compat、`CHANGELOG.md`、`TODO.md` | old/new path 引用 | 检查旧语义可追踪 |

## Fusion Rule

1. `N4-POINT-TYPING` 形成 `type_profile`。
2. `N5-LANDING-DECISION` 根据 `type_profile` 选择最窄有效 landing set。
3. `steps/` 执行动作，`review/` 负责验收，`CONTEXT.md` 只保留经验。
