# Drafting Type Package Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。
- 任何题材类型包都必须同时经过 `../../../_shared/genre-trope-quality-filter.md` 过滤；类型包只提供原料，不得把机械爽点密度、占有式关系奖励或模板化震惊反应写成硬命令。

## Default Package Rule

- 未指定更窄题材时，默认先加载 `webnovel` 包。
- 若 `north_star.yaml.genre_contract`、章级 planning 或用户请求能识别到明确题材，则叠加对应 `webnovel-subgenre`。
- 重写、续写、局部修复和 review 返工必须在原题材包基础上叠加 `draft-repair`，不得改写题材真源。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `webnovel` | `types/网文/` | 默认网文初稿、未指定更窄题材 | fallback | 先锁定 `types/网文/` 下的实际题材目录，再加载该目录内真实存在的 Markdown 文件；不得把通配符当作 literal path。 | none | none |
| `webnovel-subgenre` | `types/网文/` | 用户指定题材、项目 `north_star.yaml.genre_contract`、章节规划中的题材标签 | stackable | 选择一个或多个真实存在的题材目录，例如 `types/网文/武侠/`、`types/网文/现实题材/`、`types/网文/知乎短篇/`，并加载其中 Markdown 文件。 | none | `webnovel` |
| `draft-repair` | `types/网文/` | 重写、续写、修复、补章时保持题材味与连续性 | stackable | 沿用原章已命中的真实题材目录；若原题材无法追溯，先报告类型包缺口，不得用占位路径代替。 | none | `webnovel-subgenre` |

## Loading Flow

1. 先读取本文件，确认是否命中 `网文` 以及更窄题材包。
2. 若用户或项目显式指定题材，加载对应真实题材目录下的全部 `.md` 文件。
3. 若没有显式题材，加载与 `north_star.yaml.genre_contract` 或章节规划最接近的题材包；仍无法判断时，报告类型包缺口，不凭空套用。
4. 已命中的题材包必须与 `../../../_shared/genre-trope-quality-filter.md` 同时作为固定上下文进入 `steps/chapter-drafting-workflow.md`，再进入 provider 初稿生成。
5. 经验、失败模式和跨项目材料只从 `knowledge-base/` 按需检索。
