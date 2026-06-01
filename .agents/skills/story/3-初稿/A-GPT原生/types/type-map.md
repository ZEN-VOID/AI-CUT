# Drafting Type Package Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。
- 任何题材类型包都必须同时经过 `../../../_shared/genre-trope-quality-filter.md` 过滤；类型包只提供原料，不得把机械爽点密度、占有式关系奖励或模板化震惊反应写成硬命令。

## Default Package Rule

- 未指定更窄题材时，默认先加载 `webnovel-index` 包。
- 若 `north_star.yaml.genre_contract`、章级 planning 或用户请求能识别到明确题材，则叠加对应 concrete subgenre 包或运行时命中的同目录题材包。
- 重写、续写、局部修复和 review 返工必须在原题材包基础上叠加 `draft-repair-policy`，不得改写题材真源。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `webnovel-index` | `types/网文/` | 默认网文初稿、未指定更窄题材、需要先识别题材目录 | fallback | `types/网文/README.md` | none | none |
| `urban-brainhole` | `types/网文/都市脑洞/` | 都市脑洞、现代异能、都市爽点、现实框架叠加超常设定 | stackable | `types/网文/都市脑洞/都市脑洞.md` | none | `webnovel-index` |
| `suspense-brainhole` | `types/网文/悬疑脑洞/` | 悬疑脑洞、反转谜题、线索推进、强钩子章节 | stackable | `types/网文/悬疑脑洞/悬疑脑洞.md` | none | `webnovel-index` |
| `xuanhuan-drama` | `types/网文/玄幻剧/` | 玄幻、修炼体系、战力升级、强冲突爽点 | stackable | `types/网文/玄幻剧/xuanhuan-plot-patterns.md` | none | `webnovel-index` |
| `romance-drama` | `types/网文/狗血言情/` | 狗血言情、强情绪拉扯、替身/误会/追妻类张力 | stackable | `types/网文/狗血言情/romance-tropes.md` | none | `webnovel-index` |
| `detective-drama` | `types/网文/侦探剧/` | 侦探剧、案件推理、线索设计、嫌疑人管理 | stackable | `types/网文/侦探剧/core-elements.md` | none | `webnovel-index` |
| `draft-repair-policy` | `types/网文/` | 重写、续写、修复、补章时保持原题材味与连续性 | stackable | `types/网文/README.md` | none | `webnovel-index` |

## Loading Flow

1. 先读取本文件，确认是否命中 `网文` 以及更窄题材包。
2. 若用户或项目显式指定题材，加载对应题材目录下的全部 `.md` 文件；Package Index 中列出的 concrete rows 是默认 validator anchor，不限制运行时选择其他已存在题材目录。
3. 若没有显式题材，加载与 `north_star.yaml.genre_contract` 或章节规划最接近的题材包；仍无法判断时，加载 `webnovel-index` 并报告类型包缺口，不凭空套用。
4. 已命中的题材包必须与 `../../../_shared/genre-trope-quality-filter.md` 同时作为固定上下文进入 `steps/chapter-drafting-workflow.md`，再进入正文创作。
5. 经验、失败模式和跨项目材料只从 `knowledge-base/` 按需检索。
