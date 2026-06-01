# 6-设计 Parent Review Contract

## Scope

本合同只验收 `6-设计` 父级路由、增量对账、legacy 边界和阶段 closeout 聚合。它不拥有 `场景 / 角色 / 道具` 业务主稿的创作或改写权；域级清单、设计和生成资产仍由对应 leaf 的 `review/review-contract.md` 裁决。

## Review Gates

| gate_id | scope | blocking condition | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- | --- |
| `GATE-DESIGN-INC-01` | source scope lock | 未先锁定本轮可读上游、用户指定集号子集和既有 6-设计输出范围 | `FAIL-DESIGN-INC-SOURCE-SCOPE` | `D-N3-RECONCILE`；`references/incremental-reconciliation-contract.md` | `source_scope`、`previous_scope`、已读取输入和既有产物摘要 |
| `GATE-DESIGN-INC-02` | sidecar truth boundary | `design-manifest.yaml` 替代清单、设计稿或生成资产真源 | `FAIL-DESIGN-INC-MANIFEST-TRUTH` | `D-N3-RECONCILE`；`references/incremental-reconciliation-contract.md` | manifest 与 canonical 文件路径对照，冲突处理说明 |
| `GATE-DESIGN-INC-03` | delta completeness | `reconcile_delta` 缺少新增、归并、重命名、失效来源、设计缺口、生成缺口或覆盖风险任一必要项 | `FAIL-DESIGN-INC-DELTA-INCOMPLETE` | `D-N3-RECONCILE` | `reconcile_delta` 完整字段记录 |
| `GATE-DESIGN-INC-04` | gap order | 清单未合并就进入设计，或设计稿缺失就进入生成 | `FAIL-DESIGN-INC-GAP-ORDER` | `D-N3-RECONCILE -> D-N4-DISPATCH`；对应域 leaf | `filled_gaps`、跳过/延后说明、路由到的 leaf |
| `GATE-DESIGN-INC-05` | list merge judgment | 别名、代称或同一主体状态称呼未由 LLM 裁决，或不确定项被强行合并/拆分 | `FAIL-DESIGN-INC-MERGE` | 对应域 `1-清单` merge 模式 | `new_subjects`、`merged_subjects`、归并理由、待核项 |
| `GATE-DESIGN-INC-06` | stable identity | 既有稳定 ID、场景 `S###`、文件锚点或 canonical 名称映射因清单重排而漂移 | `FAIL-DESIGN-INC-STABLE-ID` | `references/incremental-reconciliation-contract.md`；对应域清单或设计 leaf | 旧 ID/文件锚点与新映射对照、引用扫描或待扫描说明 |
| `GATE-DESIGN-INC-07` | design gap overwrite guard | `2-设计` 覆盖既有设计稿，或处理了非 `design_gaps` 且无用户授权 | `FAIL-DESIGN-INC-DESIGN-OVERWRITE` | 对应域 `2-设计` | `design_gaps`、`skipped_existing`、用户授权或版本化说明 |
| `GATE-DESIGN-INC-08` | generation gap overwrite guard | `3-生成` 静默替换既有主图、多视图或 JSON，或因新增上游重写 `2-设计` | `FAIL-DESIGN-INC-GEN-OVERWRITE` | 对应域 `3-生成` | `generation_gaps`、`skipped_existing`、授权/版本化记录 |
| `GATE-DESIGN-INC-09` | reporting coverage | 增量执行报告缺少 source scope、previous scope、新增、归并、跳过、补缺或风险证据 | `FAIL-DESIGN-INC-REPORT` | `D-N6-CLOSEOUT`；`references/incremental-reconciliation-contract.md` | `执行报告.md`、域级状态摘要或 `validation-report.md` 的七项字段 |
| `GATE-DESIGN-ROUTE-01` | parent scope lock | 未锁定项目根、6-设计输出根、集数或候选输入文件就进入域级调度 | `FAIL-DESIGN-ROUTE-SCOPE` | `D-N1-INTAKE`；`references/思行网络.md` | `design_scope`、project root、episode/input roots、可定位或可创建说明 |
| `GATE-DESIGN-ROUTE-02` | active domain route | 命中域为空、命中未 active sibling，或仍把旧 `1-清单 / 2-设计 / 3-面板` tranche 当作当前入口 | `FAIL-DESIGN-ROUTE-DOMAIN` | `D-N2-DOMAIN`；`references/阶段路由矩阵.md` | `domain_routes`、触发词、active/pending 判定、legacy 改路由记录 |
| `GATE-DESIGN-ROUTE-03` | domain dispatch load | 未按命中域加载对应 `SKILL.md + CONTEXT.md`，调度未命中域，或绕过增量缺口直接全量覆盖 | `FAIL-DESIGN-ROUTE-DISPATCH` | `D-N4-DISPATCH`；对应域级 `SKILL.md + CONTEXT.md` | `domain_execution_plan`、已加载域级合同、跳过/处理范围 |
| `GATE-DESIGN-CLOSEOUT-01` | domain output gate | 父级 closeout 未检查域内 `1-清单 / 2-设计 / 3-生成` 产物，或把根目录平铺文件、manifest sidecar 当作业务真源 | `FAIL-DESIGN-CLOSEOUT-DOMAIN-GATE` | `D-N5-DOMAIN-GATE`；对应域级 Output Contract | `domain_verdicts`、canonical output paths、manifest 与业务真源边界说明 |
| `GATE-DESIGN-CLOSEOUT-02` | domain repair routing | 域级 review 失败后，父级直接补写清单、设计、生成正文，或未要求 leaf direct repair + re-review | `FAIL-DESIGN-CLOSEOUT-REPAIR-ROUTE` | `D-N5R-DOMAIN-REPAIR`；对应域级 leaf `review/review-contract.md` | failed findings、repair owner、repair action、re-review verdict |
| `GATE-DESIGN-CLOSEOUT-03` | stage report verdict | `validation-report.md` 缺少命中域 verdict、repair actions、顾问/本地复核状态、遗留风险，或把未通过域写成通过 | `FAIL-DESIGN-CLOSEOUT-REPORT` | `D-N6-CLOSEOUT`；`Stage-Closeout Review-Repair Contract` | `validation-report.md`、domain verdict matrix、residual risks |
| `GATE-DESIGN-LEGACY-01` | legacy archive boundary | `references/legacy/*` 被当作 active skill 入口或阻断真源 | `FAIL-DESIGN-LEGACY-ACTIVE-ENTRY` | `D-N2-DOMAIN`；`references/阶段路由矩阵.md` | 旧路径引用、改路由结果 |
| `GATE-DESIGN-LEGACY-02` | active contract revalidation | legacy archive 中的经验被直接执行，未通过当前 active 域级合同复核 | `FAIL-DESIGN-LEGACY-UNVALIDATED-RULE` | `D-N4-DISPATCH`；对应 active 域级 `SKILL.md + CONTEXT.md` | 被复用 legacy 经验、active 合同位置、采用/废弃理由 |
| `GATE-DESIGN-LEGACY-03` | deprecated path cleanup | 旧 tranche 路径、旧单 catalog 或旧 manifest 口径仍冒充 canonical truth | `FAIL-DESIGN-LEGACY-PATH-DRIFT` | `D-N2-DOMAIN -> registry/routes/shared runtime 修复`；`references/阶段路由矩阵.md` | `rg` 搜索结果、更新引用清单、无法自动更新的遗留引用 |

## Verdict Shape

```yaml
verdict: pass | needs_rework | blocked
scope:
  project_root: projects/aigc/<项目名>/
  design_root: projects/aigc/<项目名>/6-设计/
  source_scope: []
findings:
  - gate_id: GATE-DESIGN-INC-01
    fail_code: FAIL-DESIGN-INC-SOURCE-SCOPE
    severity: critical | high | medium | low
    evidence: ""
    rework_target: ""
domain_verdicts:
  场景: pass | needs_rework | not_touched
  角色: pass | needs_rework | not_touched
  道具: pass | needs_rework | not_touched
residual_risks: []
```

## Gate Rules

- `critical` finding blocks parent closeout and must route to the listed rework target.
- Parent review may repair routing, registry, references and reports, but must not directly author domain list/design/generation content.
- Legacy archive findings must resolve by rerouting to active domain packages or documenting the archive as non-authoritative; do not resurrect deprecated `1-清单 / 2-设计 / 3-面板` as active entries.
