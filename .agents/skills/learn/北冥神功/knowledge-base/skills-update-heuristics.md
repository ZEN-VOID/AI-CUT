# Skills-Update Heuristics

本文件保存跨 skill 可复用的吸收模式。它不是运行状态，也不改写 `SKILL.md` 的入口合同。

## Stable Patterns

| pattern | use when | move |
| --- | --- | --- |
| `scan-before-patch` | 用户要求升级某个 skill | 先读目标 `SKILL.md + CONTEXT.md` 和相关技能组上下文 |
| `type-before-landing` | 升级点形态不清 | 先判 `point_type`，再选 `landing_set` |
| `narrowest-effective-surface` | 多个载体都可承接升级点 | 选最窄但足够生效的 owner，避免扩散 |
| `double-learning` | 升级来自真实失败或可复用成功 | 目标 skill 收局部经验，本技能收跨 skill 模式 |
| `review-on-parity-risk` | 修改 shared carrier、registry、脚本或模板 | 必须进入 review gate，必要时降级为本地 checklist |
| `workshop-for-structure-upgrade` | 目标 skill 自身要升级为 Skill 2.0 | 使用 `skill-工作车间` 的迁移矩阵与 validator，避免语义丢失 |

## Anti-Patterns

- 只改 `SKILL.md`，但升级点其实属于经验、模板、脚本、类型矩阵或 review gate。
- 只看目标 leaf，忽略父级 skill、siblings、shared carrier 和 registry/routes。
- 把 reviewer 被阻断误写成“不需要 review”。
- 用脚本拼接核心判断或生成创作型正文。
