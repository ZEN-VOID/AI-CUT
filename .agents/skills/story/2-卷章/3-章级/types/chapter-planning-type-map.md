# Chapter Planning Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件承载章级 planning 的类型变量和分型策略。完整执行步骤由 `steps/chapter-planning-workflow.md` 拥有。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `domain_type` | `story` | 处理小说创作 planning |
| `artifact_type` | `markdown` | 主要输出为 `第N章.md` |
| `task_mode` | `create`, `revise`, `review` | 新建、局部修订或只审查 |
| `chapter_scope` | `single-chapter`, `batch-chapters` | 单章或同卷多章；批量仍按单章依次落盘 |
| `execution_type` | `llm-authored`, `script-assisted-validation` | 核心规划由 LLM 完成，脚本只做校验 |
| `topology_type` | `hybrid` | 串行回读、中段分支、末段汇流 |
| `review_type` | `checklist`, `provider-assisted` | 默认 checklist，可接 reviewer subagent |
| `output_type` | `chapter-plan`, `section-patch`, `review-verdict` | 完整章规划、局部 patch 或审查结论 |
| `genre_payoff_profile` | `xuanhuan_fantasy`, `wuxia_xianxia`, `urban_power`, `mystery_suspense`, `romance`, `comedy_slice`, `political_strategy`, `horror_weird`, `hybrid`, `custom` | 章级爽点类型画像，详见 `types/payoff-genre-type-map.md` |

## Mode Matrix

| type signal | step impact | reference impact | review impact |
| --- | --- | --- | --- |
| `task_mode=create` | 执行完整 `N1` 到 `N7` | 读取全部章级硬规则与模板 | 检查所有必填标题 |
| `task_mode=revise` | 先执行 `N1`，再进入命中的 section 节点，最后 `N7` 汇流 | 读取对应 section 细则与 Output Contract | 检查局部改动未破坏未命中 section |
| `task_mode=review` | 不写业务真源，只读取并审查 | 读取 `review/` 与 Output Contract | 输出 verdict 和 findings |
| `chapter_scope=batch-chapters` | 按章串行处理，不共享未审查 patch | 每章都回指同一卷规划 | 每章独立 verdict |
| `output_type=section-patch` | 只返回有效 patch，不补空字段 | 模板作为结构校验，不强制重写全文 | patch 后文档仍需满足必填标题 |
| `genre_payoff_profile=*` | 在 `N4-CHAPTER-PAYOFF` 前加载 `types/payoff-genre-type-map.md` 并形成类型画像 | 爽点规则按类型校准口味、禁忌和兑现尺度 | 检查 `本章爽点设计.genre_payoff_profile` 与 `payoff_mode` 是否匹配 |

## Field Matrix

| field | required | downstream consumer | validation note |
| --- | --- | --- | --- |
| `章标题` | yes | drafting 起盘 | 不得只写编号 |
| `本章故事概要` | yes | drafting Step 1 | 必须含起点、推进、转向、章末状态 |
| `本章冲突` | yes | drafting 冲突执行 | 表层、深层、状态变化都要出现 |
| `本章爽点设计` | yes | drafting Step 1 / Step 2 / 读者满足设计 | 必须含 `reader_desire / promise_source / genre_payoff_profile / character_anchor / payoff_mode / payoff_variation_axis / build_up / delivery_action / satisfaction_delta / exaggeration_logic / cost_or_aftershock / aftertaste_hook`；若 `payoff_mode` 包含高超对决，还必须含 `duel_variation_axis`；并能按类型画像和动能式、势能式或浪能式裁定主爽点；爽点必须与角色个性高度相关，夸张但合情理 |
| `本章节奏曲线` | yes | drafting Step 2 / 2-节奏优化 | 必须含 rhythm handoff slots、`payoff_type / rhythm_intensity / previous_next_contrast` 和 Mermaid，且与 `本章爽点设计` 一致 |
| `本章任务线` | yes | drafting 任务推进 | 必须含汇聚动作与未汇聚去向 |
| `本章线索` | yes | drafting 信息释放 | 只写当前可见信息推进 |
| `本章伏笔` | yes | 后续兑现追踪 | 必须拆 `铺设 / 兑现` |
| `规避` | yes | drafting 禁飞区 | 必须具体可执行 |
