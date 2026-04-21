# Type-Pack Loading Contract

`type-pack` 当前处于“目录知识优先、系统 catalog 预留但未落地”的 `bootstrap_compat` 口径。

## Current Canonical Source

- 根目录：`story/type-packs/`
- 当前活跃知识库根：
  - `story/type-packs/网文/`
- 当前强制加载合同：
  - `story/_shared/type-pack-loading-contract.md`
- 当前运行时装载器：
  - `story/scripts/data_modules/type_pack_resolver.py`
- 维护说明：
  - `story/type-packs/扩维与调整指南.md`

说明：

- `story/type-packs/pack-catalog.yaml` 目前在本仓库中尚未落地，不能被当成当前硬依赖真源。
- `story/type-packs/<pack_id>/pack.yaml` 也是预留扩展位，不是当前网文题材目录的必需载体。
- 当前 runtime 的有效事实来源是：
  - `网文/<题材>/` 下的目录知识
  - resolver 内置的 method/base/primary/platform/audience 推断规则
  - 若未来显式落地的 `pack.yaml` / `pack-catalog.yaml`

## Current Structure

### 入口题材目录

形态：

- `story/type-packs/网文/修仙/修仙.md`
- `story/type-packs/网文/末世/末世.md`
- `story/type-packs/网文/豪门总裁/豪门总裁.md`
- `story/type-packs/网文/武侠/武侠.md`

规则：

- 目录名就是题材 key。
- 同名主文件是该题材的默认入口。
- 同目录下可以继续放细化 `.md`，但如果希望 resolver 返回的 `knowledge_refs` 先命中入口文件，辅助文件命名应避免排在同名主文件之前。

### family craft 目录

形态：

- `story/type-packs/网文/狗血言情/*.md`
- `story/type-packs/网文/古言剧/*.md`
- `story/type-packs/网文/现实题材/*.md`
- `story/type-packs/网文/玄幻剧/*.md`
- `story/type-packs/网文/侦探剧/*.md`
- `story/type-packs/网文/知乎短篇/*.md`

规则：

- 这些目录承载共享 craft。
- 它们不是单题材的唯一入口。
- 入口题材只按设定补读必要的 family，不默认把同层 family 全量灌入。

### 预留系统 pack 扩展位

预留形态：

- `story/type-packs/pack-catalog.yaml`
- `story/type-packs/<pack_id>/pack.yaml`

当前规则：

- 这些载体尚未在本仓库落地，因此不能被文档、模板或 consumer 当成“当前一定存在”的真源。
- 若未来需要跨阶段统一 `aliases / semantic_tags / stage_projection / cards_projection / source_dirs`，可以落地这些文件；但必须与 resolver、tests、合同说明在同一轮同步。

## Current Runtime Behavior

当前 resolver 的默认行为是：

1. `infer_type_stack()` 固定给出：
   - `method_kernel = story-core-v1`
   - `base = _base`
   - `primary = 网文高冲击`
2. `platform / audience` 由 resolver 内置别名规则吸收。
3. `secondary` 优先通过 `网文/<题材>/` 目录同名命中。
4. `resolve()` 通过目录扫描，把命中的 `网文/<题材>/` 下 `.md` 文件写入 `knowledge_refs`。
5. 若未来存在 `pack.yaml` 或 `pack-catalog.yaml`，resolver 可以吸收其 overlay；当前没有时不得阻断。

## Loading Order

当前推荐加载顺序：

1. 先读取本合同，确认当前是“目录优先、catalog 预留”的口径。
2. 再锁定目标题材目录 `story/type-packs/网文/<题材>/`。
3. 若存在同名主文件 `<题材>.md`，先读它。
4. 若当前题材还需要共享 craft，再补读对应 family 目录下的相关 `.md`。
5. 只有当 `pack-catalog.yaml` 或 `<pack_id>/pack.yaml` 真正落地时，才把它们当作 system overlay 继续读取。

默认题材命中规则：

- 若用户或 `1-题材选型` 锁定的题材名与 `story/type-packs/网文/<题材>/` 同名，除非人工显式覆盖，否则默认走该目录。
- family craft 只按小说设定补读，不默认把同层所有 family 目录一起灌入。
- 当前不存在强制 catalog 时，抽象 pack 的跨阶段语义应以 resolver 当前内置规则与已落地文件为准，不得在 consumer 中假定“catalog 一定可读”。

## Hard Rules

- 不再默认要求旧版平铺配置文件存在。
- 不再默认要求旧版单一映射表存在。
- 不再默认要求 `pack-catalog.yaml` 已经落地。
- 若代码或文档还把 `pack-catalog.yaml` 写成当前强依赖真源，必须视为 stale reference 并同步修正。
- 结构迁移时，必须按“目录变更 -> 全仓引用扫描 -> 合同更新”的顺序执行。
- 若未来真的引入 `pack-catalog.yaml`，必须同步更新：
  - `type_pack_resolver.py`
  - 相应 tests
  - 本合同
  - `扩维与调整指南.md`
- 在 catalog 未落地前，任何跨阶段差异化 pack 变更都必须至少同步 resolver、tests 与合同说明，不能只改 consumer 文案。
