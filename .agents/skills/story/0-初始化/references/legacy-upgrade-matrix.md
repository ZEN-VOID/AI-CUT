# Legacy Upgrade Matrix

本矩阵记录 `story-init` 从长篇单文件合同升级到 Skill 2.0 分区结构时，旧 section 与资源的 owner 归属。删除或改写旧段落前必须能在本文件追到去向。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter、description、governance_tier | entry metadata | `SKILL.md` | keep | low | `agents/openai.yaml` 保持 `$story-init` 唤起 | validator |
| `SKILL.md` | `Context Loading Contract` | entry contract | `SKILL.md` | keep and tighten | high | 同步项目 `MEMORY.md` 与 `CONTEXT/` 加载口径 | validator + manual semantic check |
| `SKILL.md` | `概述`、`When to Use`、`When Not to Use` | routing contract | `SKILL.md` | rewrite | medium | `.codex/registry/routes.yaml` 已保留 story/aigc 分流 | manual route check |
| `SKILL.md` | `业务需求分析合同` | business analysis | `SKILL.md` Business Requirement Analysis Contract、`types/init-type-map.md` | keep and tighten | medium | 业务画像回收进 runtime spine，类型变量仍由 `types/` 展开 | review gate |
| `SKILL.md` | `Visual Maps` | topology map | `SKILL.md` Visual Maps | keep and tighten | low | Mermaid 与节点表统一在 `SKILL.md`，不再下沉到 steps | markdown check |
| `SKILL.md` | `Total Input Contract` | input contract | `SKILL.md`、`references/mode-and-team-contract.md` | split | high | `Input Contract` 留在根，team 细则进 references | validator |
| `SKILL.md` | `Internal Capability Fusion Contract` | capability rules | `SKILL.md` Thinking-Action Node Map、`references/mode-and-team-contract.md` | split | high | 主节点回收进 `SKILL.md`，team 细则留在 references | manual semantic check |
| `SKILL.md` | `Initialization Mode Contract` | mode rules | `references/mode-and-team-contract.md` | move | high | 根 `Mode Selection` 保留摘要 | manual semantic check |
| `SKILL.md` | `Team Manifest Contract` | team truth contract | `references/mode-and-team-contract.md` | move | high | 下游只读 `team.yaml` | review gate |
| `SKILL.md` | `Prompt Packet Contract` | direct-answer contract | `references/prompt-packet-contract.md` | move | high | subagent 阻断/降级口径保留在根与 reference | manual semantic check |
| `SKILL.md` | `Canonical Landing`、`Project State Synchronization Contract` | runtime contract | `references/runtime-and-handoff-contract.md` | move | high | 模板和脚本入口仍指向标准五件套 | script/dry-run check |
| `SKILL.md` | `Execution Procedure` | workflow | `SKILL.md` Thinking-Action Node Map | rewrite | high | 主干节点、分支、证据、route 和 gate 均由 `SKILL.md` 直接承载 | review gate |
| `SKILL.md` | `Sufficiency Gate` | review gate | `review/init-review-gate.md` | move | high | 根 Completion gate 保留摘要 | review gate |
| `SKILL.md` | `Root-Cause Execution Contract` | root-cause contract | `SKILL.md`、`review/init-review-gate.md` | keep and route | high | 加入 Section Owner 上溯链 | validator |
| `SKILL.md` | `Verification` | verification | `review/init-review-gate.md`、`scripts/README.md` | move | medium | 根 Output Contract 保留完成门禁 | command check |
| `SKILL.md` | `Field Master`、`Step to Field Mapping`、`Field to Quality Mapping` | field mapping | `SKILL.md`、`review/init-review-gate.md` | split | medium | 根保留字段中心映射，质量细则进 review | validator |
| `CONTEXT.md` | initialization type map and heuristics | experience layer | `CONTEXT.md` | keep | low | 不迁入规范层，避免经验覆盖合同 | context audit |
| `references/creative-seed-routing/*` | creative seed module | reference module | `references/creative-seed-routing/*` | keep | medium | 根只引用 `module-spec.md`，leaf docs 由模块内部路由 | link check |
| `references/advisor-council-mode/` | retired empty legacy mode directory | legacy residue | none | archive/drop empty | low | 全仓无活跃引用后移除空目录 | `rg` reference sync |
| `references/fast-mode/` | retired empty legacy mode directory | legacy residue | none | archive/drop empty | low | 全仓无活跃引用后移除空目录 | `rg` reference sync |
| `references/autonomous-mode/` | retired empty legacy mode directory | legacy residue | none | archive/drop empty | low | 全仓无活跃引用后移除空目录 | `rg` reference sync |
| `north-star.template.yaml`、`story-source-manifest.template.yaml`、`init-handoff.template.yaml`、`project-memory.template.md` | output artifact templates | templates | `templates/` | keep | medium | 新增 `templates/output-template.md` 作为五字段对齐说明 | validator |
| `agents/openai.yaml` | product metadata | agents metadata | `agents/openai.yaml` | keep | low | default prompt 已显式提到 `$story-init` | validator |

## Reference Sync Notes

- 已移除的旧空目录：`references/advisor-council-mode/`、`references/fast-mode/`、`references/autonomous-mode/`。
- 这些目录在本轮扫描中没有外部活跃引用；若外部系统仍保存路径，需人工更新到 `references/mode-and-team-contract.md` 或 `references/prompt-packet-contract.md`。
- `references/creative-seed-routing/` 保持独立模块入口，父技能不得绕过 `module-spec.md` 直接点名 leaf docs。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 旧 `SKILL.md` section 与旧资源是否都能追到现有 owner、保留动作和验证门？ | `dynamic_reference` | `FAIL-INIT-DYNAMIC-REFERENCE` | 本文件 Migration Matrix、目标 owner 分区 | migration matrix coverage |
| 删除或退休的旧路径是否不再作为活跃引用出现？ | `integration` | `FAIL-INIT-INTEGRATION` | 本文件 Reference Sync Notes、全仓引用同步 | retired path `rg` 结果 |
| 模板、review、types、scripts 的迁移是否没有制造第二真源？ | `structure` / `integration` | `FAIL-INIT-STRUCTURE` / `FAIL-INIT-INTEGRATION` | README Directory Tree、`SKILL.md` Module Loading Matrix | owner map、validator/smoke output |
