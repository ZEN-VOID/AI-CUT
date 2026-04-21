# Type-Pack Loading Contract

`comic/type-pack` 当前采用“目录知识优先 + 运行时配置/题材元数据动态发现”的 `bootstrap_compat` 口径。

## Current Canonical Source

- 根目录：`comic/type-packs/`
- 当前活跃知识库根：
  - `comic/type-packs/漫画/`
- 当前强制加载合同：
  - `comic/_shared/type-pack-loading-contract.md`
- 当前运行时装载器：
  - `comic/scripts/data_modules/comic_type_pack_resolver.py`
- 当前动态配置真源：
  - `comic/type-packs/runtime.yaml`
- 当前题材元数据真源：
  - `comic/type-packs/漫画/<题材>/meta.yaml`
- 维护说明：
  - `comic/type-packs/扩维与调整指南.md`

说明：

- 当前 runtime 的有效事实来源是：
  - `漫画/<题材>/` 下的目录知识
  - `runtime.yaml` 中的 `method/base/primary/platform/audience` 默认规则
  - 各题材目录 `meta.yaml` 中的 `aliases / semantic_tags / stage_projection`

## Current Structure

### 入口题材目录

形态：

- `comic/type-packs/漫画/热血战斗/热血战斗.md`
- `comic/type-packs/漫画/中二战斗/中二战斗.md`
- `comic/type-packs/漫画/狗血言情/狗血言情.md`

规则：

- 目录名就是题材 key。
- 同名主文件是该题材默认入口。
- 同目录下可继续放细化 `.md`，共同构成该题材的漫画知识包。
- 同目录 `meta.yaml` 是该题材的动态装载元数据。

### 题材细化目录

形态：

- `comic/type-packs/漫画/狗血言情/*.md`
- `comic/type-packs/漫画/热血战斗/*.md`
- `comic/type-packs/漫画/悬疑惊悚/*.md`

规则：

- 同一题材内的多份 `.md` 共同服务一个题材入口。
- 这些细化文件不是并列题材，只是该题材内部的角色、节奏、爽点、视觉、标题等细分知识。
- 不允许把跨题材通用知识重新拆成根层“工艺类目录”；若某模式确实跨题材复用，优先在多个题材内部各自写成适配版本。

### 动态配置位

形态：

- `comic/type-packs/runtime.yaml`
- `comic/type-packs/漫画/<题材>/meta.yaml`

当前规则：

- `runtime.yaml` 负责根级默认栈与平台/受众/主轴规则。
- `meta.yaml` 负责单题材的 `aliases / semantic_tags / stage_projection`。
- 任务执行时，resolver 每次都会重新扫描目录和这些 YAML，因此类型包升级后无需改 Python 代码即可自动命中最新版本。

## Current Runtime Behavior

当前 resolver 的默认行为是：

1. `infer_type_stack()` 固定给出：
   - `method_kernel = comic-core-v1`
   - `base = _base`
   - `primary = 漫画高冲击`
2. `platform / audience` 通过 `runtime.yaml` 中的 alias 规则吸收。
3. `secondary` 通过扫描 `漫画/<题材>/meta.yaml` 的 alias 和目录名动态命中。
4. `resolve()` 通过目录扫描，把命中的 `漫画/<题材>/` 下 `.md` 文件写入 `knowledge_refs`。
5. `stage_projection` 由 `runtime.yaml + meta.yaml` 动态合并，不再写死在 resolver 内部。
6. `pack_revisions` 会记录每个命中题材目录的当前 revision，用于追踪本次任务吸收到的最新版本。

## Loading Order

当前推荐加载顺序：

1. 先读取本合同，确认当前是“目录优先 + 动态发现”的口径。
2. 再锁定目标题材目录 `comic/type-packs/漫画/<题材>/`。
3. 若存在同名主文件 `<题材>.md`，先读它。
4. 再读同目录 `meta.yaml`。
5. 再补读同目录下的细化 `.md`。
6. 同时读取 `runtime.yaml`，合并 base/primary/platform/audience 的默认投影。

默认题材命中规则：

- 若用户或 1 号技能锁定的题材名与 `comic/type-packs/漫画/<题材>/` 同名，除非人工显式覆盖，否则默认走该目录。
- 当前跨阶段差异化 pack 以 `runtime.yaml + 题材 meta.yaml + 目录知识` 为准，不得在 consumer 中假定还需要手写硬编码映射。

## Hard Rules

- `comic` 不再把“系统 / 维度 / 工艺”做成目录真源。
- 当前目录真源只按题材分类。
- 不允许只新增题材目录而不补 `meta.yaml`。
- 不允许继续把题材 alias、semantic tags、stage projection 写死在 resolver 代码里。
- 结构迁移时，必须按“目录变更 -> 全仓引用扫描 -> 合同更新”的顺序执行。
- 若未来调整 `runtime.yaml` 或任一 `meta.yaml`，下次任务执行时应自动吸收最新版本；若未生效，应优先排查 resolver 动态扫描链路，而不是先改 consumer。

## Active Type Stack Contract

`comic` 当前 active stack 仍固定为：

- `method_kernel`
- `base`
- `primary`
- `secondary[]`
- `platform[]`
- `audience[]`
- `active_packs[]`

其中：

- `secondary[]` 是当前唯一对外显式题材层。
- `base / primary / platform / audience` 仅作为 resolver 内部兼容字段与跨阶段 artifact 稳定槽位存在，不对应当前目录分类。
- `type_pack_context.pack_revisions` 是动态机制的版本追踪槽位。

当 1 号技能输出 `formatted_source_script.json` 时，默认应把：

- `type_stack_ref`
- `type_pack_context`

写入结构化真源，并作为 2/3/4/5 段的共享上游语义层。
