# 7-设计 Incremental Reconciliation Contract

## Purpose

`7-设计` 必须支持上游 `6-分组` 分批完成的生产节奏。项目可以先完成若干集分组并执行设计，之后继续追加新的 `第N集.md`；后续执行不得把既有清单、设计稿或生成资产当作一次性全量覆盖对象。

本合同为 `场景 / 角色 / 道具` 三个域提供统一的增量对账规则。它不替代任何域的 `1-清单` 主真源，也不替代 `2-设计` / `3-生成` 的创作或生成合同。

## Ownership

| scope | owner |
| --- | --- |
| 上游范围扫描、已消费集数识别、缺口定位 | 域组根 |
| 主体新增、别名归并、首次登场、清单写回 | 对应域 `1-清单` |
| 清单主体到设计稿的缺口补齐 | 对应域 `2-设计` |
| 设计稿到主图、多视图、JSON 的缺口补齐 | 对应域 `3-生成` |
| 跨叶子状态索引 | `design-manifest.yaml` sidecar |

## Runtime State

每个域可以维护一个状态索引：

```text
projects/aigc/<项目名>/7-设计/<域>/design-manifest.yaml
```

`design-manifest.yaml` 是 sidecar 状态索引，只记录来源范围、主体映射、已完成文件和缺口；它不得替代 `1-清单/<域>清单.md` 作为主体真源，不得替代 `2-设计/*.md` 作为设计真源，也不得替代 `3-生成/*` 作为生成资产真源。

推荐字段：

```yaml
source_episodes:
  - 第1集.md
  - 第2集.md
subjects:
  - id: DOMAIN-001
    canonical_name: 主体名
    aliases: []
    first_appearance: 第1集 1-1-1
    list_status: active
    design_file: 2-设计/主体名.md
    generation_assets:
      main: 3-生成/主体名-主图.png
      multiview: 3-生成/主体名-多视图.png
      prompts:
        - 3-生成/主体名-主图.json
        - 3-生成/主体名-多视图.json
```

## Reconciliation Pass

任意域级执行在进入叶子前，必须完成以下对账：

1. 锁定当前可读上游：`projects/aigc/<项目名>/6-分组/第N集.md`，或用户指定的集号子集。
2. 读取已有域内输出：`1-清单/`、`2-设计/`、`3-生成/` 与可选 `design-manifest.yaml`。
3. 生成本轮 `reconcile_delta`：
   - `new_subjects`: 新上游中出现、既有清单无对应主体。
   - `merge_candidates`: 新称呼可能指向既有主体。
   - `renamed_subjects`: canonical 名称可能需要调整。
   - `stale_or_missing_sources`: manifest 记录但上游文件不可读或已移除。
   - `design_gaps`: 清单有主体但 `2-设计` 缺设计稿。
   - `generation_gaps`: 设计稿存在但 `3-生成` 缺主图、多视图或 JSON。
   - `overwrite_risks`: 本轮可能覆盖既有设计稿或生成资产。
4. 先处理最早缺口：清单未合并时不得直接进入设计；设计稿缺失时不得直接进入生成。

## List Merge Rules

- 清单更新采用 merge 模式，不采用静默全量覆盖。
- 精确同名默认归并，并追加来源证据。
- 别名、代称、同一地点/角色/道具的状态称呼，必须由 LLM 裁决是否归并。
- 新主体追加进清单；首次登场取所有已知来源中最早分镜组。
- 后续集数补充的关键词可以更新 `原文描述（关键词式）`，但不得扩写成设计正文。
- 无法确定归并关系时写入 `执行报告.md` 的待核项，不强行拆分或合并。

## Stable Identity Rules

- 已分配给主体的稳定 ID 或已有文件锚点不得因清单重排而重排。
- 场景 `S###` 一旦写入设计稿，后续新增场景应追加新编号，不重新编号旧场景。
- 角色/道具同名冲突使用清单主体、首次登场或 manifest 映射消歧，不静默覆盖同名文件。
- canonical 名称变化时，默认保留既有文件名并在 manifest 或执行报告记录 `canonical_name` 映射；重命名文件必须先同步扫描引用。

## Design Gap Rules

- `2-设计` 默认只处理 `design_gaps` 或用户明确指定的主体。
- 已有设计稿默认跳过；除非用户明确要求 repair / regenerate，不得覆盖。
- 清单主体被归并到已有主体时，不新建设计稿，只记录 alias merge。
- 下游发现清单错误时，只写修复建议并回到 `1-清单`，不得在 `2-设计` 私自改清单真源。

## Generation Gap Rules

- `3-生成` 默认只处理 `generation_gaps` 或用户明确指定的主体。
- 已有主图、多视图和 JSON 默认跳过。
- 覆盖、重生或替换 prompt 必须获得用户明确授权；否则使用版本化命名并记录 `supersedes` / `variant_of`。
- 生成阶段不得因为新上游追加而重写 `2-设计`。

## Reporting

每次增量执行建议在对应 leaf 的 `执行报告.md` 或域级状态摘要中记录：

| field | required content |
| --- | --- |
| `source_scope` | 本轮扫描的集号或文件 |
| `previous_scope` | 已有 manifest 或既有清单覆盖范围 |
| `new_subjects` | 本轮新增主体 |
| `merged_subjects` | 本轮归并关系与理由 |
| `skipped_existing` | 已有设计或生成资产，未覆盖 |
| `filled_gaps` | 本轮补齐的设计或生成缺口 |
| `risks` | 待核归并、命名冲突、上游缺失或覆盖风险 |

## Failure Routing

| symptom | repair route |
| --- | --- |
| 新增集数后直接覆盖清单 | 对应域 `1-清单` merge 模式 |
| 新别名生成了重复主体 | 对应域 `1-清单` LLM 归并裁决 |
| 场景 `S###` 因清单重排而变化 | 场景 `2-设计` stable identity rules |
| 已有设计稿被静默覆盖 | 对应域 `2-设计` design gap rules |
| 已有图片或 JSON 被静默覆盖 | 对应域 `3-生成` generation gap rules |
| manifest 与清单冲突 | 清单真源优先，manifest 作为 sidecar 修复 |
