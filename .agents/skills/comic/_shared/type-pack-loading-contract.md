# Type-Pack Loading Contract

`comic/type-pack` 当前采用“单层题材目录 + runtime/meta 动态发现”的口径。

## Current Canonical Source

- 根目录：`comic/type-packs/`
- 当前活跃知识库根：`comic/type-packs/漫画/`
- 强制加载合同：`comic/_shared/type-pack-loading-contract.md`
- 运行时装载器：`comic/scripts/data_modules/comic_type_pack_resolver.py`
- 根级动态配置真源：`comic/type-packs/runtime.yaml`
- 单题材元数据真源：`comic/type-packs/漫画/<题材>/meta.yaml`
- 维护说明：`comic/type-packs/扩维与调整指南.md`

当前 runtime 的有效事实来源是：

- `漫画/<题材>/` 下的目录知识
- `runtime.yaml` 中的 `method/base/primary/platform/audience` 默认规则
- 各题材目录 `meta.yaml` 中的 `aliases / semantic_tags / stage_projection`

## Current Structure

### 单层题材目录

形态：

- `comic/type-packs/漫画/少年战斗冒险/少年战斗冒险.md`
- `comic/type-packs/漫画/青春恋爱/青春恋爱.md`
- `comic/type-packs/漫画/情感关系剧/情感关系剧.md`
- `comic/type-packs/漫画/推理悬疑/推理悬疑.md`
- `comic/type-packs/漫画/恐怖怪谈/恐怖怪谈.md`

规则：

- 目录名就是 canonical 题材 key。
- 同名主文件是该题材默认入口。
- 同目录下可继续放细化 `.md`，共同构成该题材的漫画知识包。
- 题材内可以吸收该题材专属的“工艺变体”，但这些变体不再升格成根层并列 pack。

### 题材内细化文件

形态：

- `comic/type-packs/漫画/少年战斗冒险/命名体系.md`
- `comic/type-packs/漫画/情感关系剧/关系原型.md`
- `comic/type-packs/漫画/推理悬疑/翻页悬念.md`

规则：

- 这些文件不是并列题材，只是当前题材内部的结构化细分知识。
- 一个题材目录内应优先覆盖：
  - 核心冲突引擎
  - 角色原型
  - 页面/分镜语法
  - 典型桥段库
  - 标题/钩子或题材特有变体
- 若某个技巧跨题材复用，默认以“各题材内部适配版本”沉淀，不再建立根层 `工艺/` 目录。

### 题材元数据控制面

每个 `meta.yaml` 除兼容旧链路所需的 `aliases / semantic_tags / stage_projection` 外，还应显式包含 `control_surface`，至少覆盖：

- `conflict_engine`
- `role_matrix`
- `page_turn_mechanism`
- `panel_grammar`
- `visual_carrier`
- `dialogue_register`
- `motif_system`
- `failure_modes`

这些字段是当前“经典漫画语法控制面”的最小骨架，用来回答“该题材如何通过漫画语言成立”，而不只是“它看起来像什么”。

### 动态配置位

- `comic/type-packs/runtime.yaml`
- `comic/type-packs/漫画/<题材>/meta.yaml`

当前规则：

- `runtime.yaml` 负责根级默认栈与平台/受众/主轴规则。
- `meta.yaml` 负责单题材的 `aliases / semantic_tags / stage_projection`。
- `meta.yaml.control_surface` 负责单题材的经典漫画语法控制面。
- resolver 每次任务执行都会重新扫描目录和这些 YAML，因此类型包升级后无需改 Python 代码即可自动命中最新版本。

## Current Runtime Behavior

当前 resolver 的默认行为是：

1. `infer_type_stack()` 固定给出：
   - `method_kernel = comic-core-v1`
   - `base = _base`
   - `primary = 经典漫画叙事`
2. `platform / audience` 通过 `runtime.yaml` 中的 alias 规则吸收。
3. `secondary[]` 通过扫描 `漫画/<题材>/meta.yaml` 的 alias 和目录名动态命中。
4. `resolve()` 通过目录扫描，把命中的 `漫画/<题材>/` 下 `.md` 文件写入 `knowledge_refs`。
5. `stage_projection` 由 `runtime.yaml + meta.yaml` 动态合并，不再写死在 resolver 内部。
6. `pack_revisions` 会记录每个命中题材目录的当前 revision，用于追踪本次任务吸收到的最新版本。

## Loading Order

当前推荐加载顺序：

1. 先读取本合同，确认当前是“单层题材目录 + 动态发现”的口径。
2. 再锁定目标题材目录 `comic/type-packs/漫画/<题材>/`。
3. 若存在同名主文件 `<题材>.md`，先读它。
4. 再读同目录 `meta.yaml`。
5. 再补读同目录下的细化 `.md`。
6. 同时读取 `runtime.yaml`，合并 base/primary/platform/audience 的默认投影。

默认题材命中规则：

- 若用户或 1 号技能锁定的题材名与 `comic/type-packs/漫画/<题材>/` 同名，除非人工显式覆盖，否则默认走该目录。
- 若用户给的是旧名称或题材内工艺词，优先通过题材 `meta.yaml` 的 alias 回收到对应题材 pack。

## Hard Rules

- `comic` 不再把“系统 / 维度 / 工艺”做成目录真源。
- 当前目录真源只按题材分类。
- 不允许只新增题材目录而不补 `meta.yaml`。
- 不允许继续把题材 alias、semantic tags、stage projection 写死在 resolver 代码里。
- 结构迁移时，必须按“目录变更 -> 全仓引用扫描 -> 合同更新”的顺序执行。

## Active Type Stack Contract

`comic` 当前 active stack 固定为：

- `method_kernel`
- `base`
- `primary`
- `secondary[]`
- `platform[]`
- `audience[]`
- `active_packs[]`

其中：

- `secondary[]` 是当前唯一对外显式题材层。
- `base / primary / platform / audience` 作为跨阶段 artifact 的稳定槽位存在。
- `type_pack_context.pack_revisions` 是动态机制的版本追踪槽位。

当 1 号技能输出 `第N组.md` 时，默认应把：

- `type_stack_ref`
- `type_pack_context`

落实到分组正文的语气、钩子、节奏与角色书写中，并作为 2/3/4/5 段的共享上游语义层。
