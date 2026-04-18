# Type-Pack Loading Contract

`type-pack` 当前已经从旧版平铺配置体系，重构为知识目录优先的加载结构。

## Current Canonical Source

- 根目录：`story/type-packs/`
- 当前活跃知识库根：
  - `story/type-packs/网文/`
- 维护说明：
  - `story/type-packs/扩维与调整指南.md`

## Current Structure

### 入口题材目录

形态：

- `story/type-packs/网文/修仙/修仙.md`
- `story/type-packs/网文/末世/末世.md`
- `story/type-packs/网文/豪门总裁/豪门总裁.md`

规则：

- 目录名就是题材 key
- 同名主文件是该题材的默认入口

### family craft 目录

形态：

- `story/type-packs/网文/狗血言情/*.md`
- `story/type-packs/网文/古言剧/*.md`
- `story/type-packs/网文/现实题材/*.md`
- `story/type-packs/网文/玄幻剧/*.md`
- `story/type-packs/网文/侦探剧/*.md`
- `story/type-packs/网文/知乎短篇/*.md`

规则：

- 这些目录承载共享 craft
- 它们不是单题材的唯一入口
- 入口题材可按需补读对应 family

## Loading Order

当前推荐加载顺序：

1. 锁定目标题材目录 `story/type-packs/网文/<题材>/`
2. 若存在同名主文件 `<题材>.md`，先读它
3. 若该题材还需要共享 craft，再补读对应 family 目录下的相关 `.md`

默认题材命中规则：

- 若用户或 `1-题材选型` 锁定的题材名与 `story/type-packs/网文/<题材>/` 同名，除非人工显式覆盖，否则默认走该目录。
- family craft 只按小说设定补读，不默认把同层所有 family 目录一起灌入。

## Hard Rules

- 不再默认要求旧版平铺配置文件存在。
- 不再默认要求旧版单一映射表存在。
- 不再默认要求旧版 schema / resolver 合同文件存在。
- 若代码或文档还按旧结构引用这些文件，必须视为 stale reference 并同步修正。
- 结构迁移时，必须按“目录变更 -> 全仓引用扫描 -> 合同更新”的顺序执行。
