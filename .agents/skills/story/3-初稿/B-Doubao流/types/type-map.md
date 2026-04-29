# Drafting Type Package Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。

## Default Package Rule

- 未指定更窄题材时，默认先加载 `webnovel` 包。
- 若 `north_star.yaml.genre_contract`、章级 planning 或用户请求能识别到明确题材，则叠加对应 `webnovel-subgenre`。
- 重写、续写、局部修复和 review 返工必须在原题材包基础上叠加 `draft-repair`，不得改写题材真源。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `webnovel` | `types/网文/` | 默认网文初稿、未指定更窄题材 | fallback | `types/网文/*/*.md` | none | none |
| `webnovel-subgenre` | `types/网文/<题材>/` | 用户指定题材、项目 `north_star.yaml.genre_contract`、章节规划中的题材标签 | stackable | `types/网文/<题材>/*.md` | none | `webnovel` |
| `draft-repair` | `types/网文/<题材>/` | 重写、续写、修复、补章时保持题材味与连续性 | stackable | `types/网文/<题材>/*.md` | none | `webnovel-subgenre` |

## Loading Flow

1. 先读取本文件，确认是否命中 `网文` 以及更窄题材包。
2. 若用户或项目显式指定题材，加载对应 `types/网文/<题材>/` 下的全部 `.md` 文件。
3. 若没有显式题材，加载与 `north_star.yaml.genre_contract` 或章节规划最接近的题材包；仍无法判断时，报告类型包缺口，不凭空套用。
4. 已命中的题材包作为固定上下文进入 `steps/chapter-drafting-workflow.md`，再进入 provider 初稿生成。
5. 经验、失败模式和跨项目材料只从 `knowledge-base/` 按需检索。
