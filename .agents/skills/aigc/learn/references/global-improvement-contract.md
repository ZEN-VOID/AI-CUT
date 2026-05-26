# Global Improvement Contract

本文件定义 `aigc-learn` 如何把学习结论映射到 `.agents/skills/aigc/` 全局技能树，并保持多处改进协调一致。

## Target Skill Map

每次差距分析或执行型改进必须建立 `target_skill_map`：

| field | requirement |
| --- | --- |
| `root_router` | 是否需要同步 `.agents/skills/aigc/SKILL.md + CONTEXT.md` |
| `primary_owner` | 最窄有效 owning skill 或分区 |
| `related_stages` | 受影响的 `0-初始化` 到 `10-审片` 阶段 |
| `related_satellites` | query / resume / review / repair / shot-by-shot / learn 等旁路消费者 |
| `shared_carriers` | `_shared/`、registry、routes、audit scripts、templates |
| `project_runtime` | 是否影响 `projects/aigc/<项目名>/` 的产物路径、MEMORY 或 CONTEXT |
| `not_owned` | 明确不得由本次学习改写的真源 |

## Gap Matrix

| field | requirement |
| --- | --- |
| `learned_capability` | 学习对象中可迁移的能力、方法或检查项 |
| `current_support` | 当前 AIGC 技能树已有支持 |
| `gap` | 缺失、薄弱、矛盾或过期处 |
| `landing_candidate` | 建议落点：SKILL、references、steps、types、review、templates、scripts、CONTEXT |
| `sync_consumers` | 必须同步的根索引、routes、registry、审计脚本或下游技能 |
| `risk` | 版权、事实、越权、冲突、项目污染或执行成本 |

## Landing Rules

- 入口、触发、模式、输出和强制门槛落到 owning `SKILL.md`。
- 长规则、媒体处理细则、背景规范落到 `references/`。
- 判断-动作-证据节点落到 `steps/`。
- 对象类型、学习对象类型和固定上下文落到 `types/`。
- 质量门禁、隔离审计和 verdict 落到 `review/`。
- 输出样板落到 `templates/`。
- 可复用经验、失败模式和 heuristics 落到 `CONTEXT.md`。
- 外部资料索引、长参考包和人工维护知识落到 `knowledge-base/`。
- 机械抽取、校验、diff、引用扫描落到 `scripts/`。

## Sync Scope

执行型改进必须声明同步范围：

1. `local_only`: 只改目标 skill 内部分区。
2. `root_route`: 同步 AIGC 根 `SKILL.md`、`CONTEXT.md` 或卫星索引。
3. `registry_route`: 同步 `.codex/registry/skills.yaml` 和 `.codex/registry/routes.yaml`。
4. `audit_script`: 同步 `scripts/aigc_skill_audit.py` 或等价审计器。
5. `cross_skill`: 同步多个阶段、叶子、卫星或共享载体。

跨两类以上同步范围时，必须运行协调审计。
