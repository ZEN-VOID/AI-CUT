# Skills-Update Absorption Workflow

本文件是 `北冥神功` 的思行网络真源。节点同时表达判断、动作、证据、路由和 gate。

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 把升级点有机吸收到目标 skill，并让后续同类升级可复用 |
| `business_object` | `SKILL.md`、`CONTEXT.md`、分区文件、registry/routes、shared carrier、模板或脚本 |
| `constraint_profile` | 上下文加载、真源分层、同步范围、review 降级、脚本不得主创 |
| `success_criteria` | 升级点有明确 `point_type -> landing_set -> sync_scope -> validation_gate` |
| `non_goals` | 不处理普通业务内容生成，不把升级点无差别追加进单文件 |
| `complexity_source` | 目标 skill 与父级、同级、shared carrier 的同步关系 |
| `topology_fit` | 前段串行扫描，中段按类型分支，后段统一 review 与学习沉淀 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-MISSION-LOCK` | 锁定本轮升级边界 | 用户请求、目标路径、升级点 | 明确 `target_skill`、`upgrade_points`、禁区与成功标准 | mission summary | `N2` | 目标与升级点均可定位 |
| `N2-TARGET-STATE-SCAN` | 读清目标 skill 当前配置 | 目标 `SKILL.md + CONTEXT.md`、目录清单 | 找出现有合同、缺口、已有资源与不可碰面 | target baseline | `N3` | 不再把目标 skill 当黑盒 |
| `N3-GROUP-CONTEXT-SCAN` | 建立技能组上下文 | 父级、siblings、shared carrier、registry/routes | 判断本轮是否影响发现、路由、shared schema 或 sibling parity | group map | `N4` | 同步范围有依据 |
| `N4-POINT-TYPING` | 判定升级点真实类型 | 升级点、吸收矩阵、类型表 | 生成 `point_type` 与候选 landing surfaces | type profile | `N5` | 每个升级点都有类型 |
| `N5-LANDING-DECISION` | 裁决最窄有效落点 | type profile、group map | 选择 `landing_set`、`sync_scope`、`parity_targets`、验证门 | decision packet | `N6` | 落点与同步范围可解释 |
| `N6-PATCH-AND-PARITY` | 实施改造与同步 | decision packet、文件系统 | 修改目标载体并同步必要 shared/registry/template/script | diff summary | `N7` | 不留下半升级状态 |
| `N7-REVIEW-AND-VALIDATE` | 执行质量门 | diff、review contract、validator | 运行结构、链接、语义和 reviewer 降级检查 | validation summary | `N8` 或 `N5` | 阻断问题已修复或记录 |
| `N8-LEARNING-DEPOSITION` | 沉淀可复用经验 | validation summary、diff | 写回目标经验、本技能经验与时间序变更 | learning summary | done | 局部与跨 skill 经验均有落点 |

## Branch Rules

- `N1 -> N2 -> N3` 不得跳过。
- `N4` 可以按 `trigger_discovery`、`workflow_contract`、`heuristic_learning`、`schema_runner`、`group_handoff`、`audit_validation`、`compat_migration` 分支。
- 任一分支修改发现入口，必须检查 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml`。
- 任一分支修改 shared carrier、脚本、validator 或模板，必须补 sibling parity 检查。
- 所有分支必须汇流到 `N7`；不得用最终总结替代 review gate。
