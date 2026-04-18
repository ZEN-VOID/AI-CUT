# Context Contract v2

## 目的

- 为 `3-Drafting`、`4-Validation`、`review/` 提供统一的章节级上下文合同。
- 把上游 `0-Init / 1-Cards / 2-Planning` 收束为可消费的执行包，而不是全量回灌原始材料。
- 兼容现有脚本与测试，对外版本号继续固定为 `v2`。

## Canonical Roots

`v2` 的默认输入分五层：

1. Layer A：硬约束层
   - 项目承诺
   - `Init/north_star_contract.json.cards`
   - `state.json` 中的全局约束
2. Layer B：章节编排真源层
   - 默认入口：`Planning/8-全息地图.json`
3. Layer C：运行态层
   - `state.json`
   - 最近摘要
   - 最近 `chapter_meta / review_metrics / reading_power`
4. Layer D：对象定向切片层
   - 角色 / 场景 / 物品卡的相关切片
5. Layer E：写法优化层
   - `reader_signal`
   - `genre_profile`
   - `writing_guidance`
   - 可选 `rag_assist`

## 输出结构

根字段保持兼容：

- `meta`
- `sections`
- `template`
- `weights`

`meta` 中至少包含：

- `context_contract_version: "v2"`
- `chapter`
- `template`
- `ranker`
- `context_weight_stage: early|mid|late`

## Required Sections

`sections` 中的标准段：

- `core`
- `scene`
- `global`
- `reader_signal`
- `genre_profile`
- `writing_guidance`
- `story_skeleton`
- `memory`
- `preferences`
- `alerts`

说明：

- `memory` 对应 `.webnovel/project_memory.json`
- `preferences` 对应 `.webnovel/preferences.json`
- 两者都属于运行时辅助层，不覆盖 planning / cards 真源

## Section Semantics

### `reader_signal`

- 聚合最近章节 `chapter_reading_power`
- 聚合最近窗口 `hook_type_usage / pattern_usage`
- 聚合最近 `review_metrics` 趋势
- 输出低分区间与债务摘要

### `genre_profile`

- 由 `state.project.genre` 或 `project_info.genre` 归一化生成
- 参考根级：
  - `.agents/skills/story/references/genre-profiles.md`
  - `.agents/skills/story/references/reading-power-taxonomy.md`
- 支持复合题材，输出：
  - `genre`
  - `genres`
  - `composite`
  - `reference_hints`
  - `composite_hints`

### `writing_guidance`

- 基于 `reader_signal + genre_profile` 生成章节级建议
- 至少可输出：
  - `guidance_items`
  - `signals_used`
  - `checklist`
  - `checklist_score`

## Validation Projection

`extract_chapter_context.py` 在 `v2` 基础上额外投影出 `validation_fact_pack`，供 `4-Validation` 使用。

强制五个 slice：

- `promise_slice`
- `chapter_board`
- `cards_state_history_slice`
- `foreshadow_silence_slice`
- `style_gate`

规则：

- `validation_fact_pack` 是 `v2` 的派生投影，不是新的独立上下文体系。
- 若上述 slice 任一缺失，`4-Validation` 应按 `FAIL-COVENANT` 处理。

## 排序与紧凑文本策略

- `recent_summaries / recent_meta / story_skeleton / alerts` 默认按新近度与风险优先级排序。
- 超预算时采用紧凑文本输出：
  - 头部 + `…[TRUNCATED]` + 尾部
- `content` 保留结构化原文，`text` 用于注入模型上下文。

## 兼容性约束

- 不改变现有 key 名与字段语义。
- 可增加段或元数据，但不得破坏 `v2` 调用方。
- 若调用方只识别 `context_contract_version=v2`，应仍可正常消费。

## 关键配置项

- `context_reader_signal_*`
- `context_genre_profile_*`
- `context_writing_guidance_*`
- `context_writing_checklist_*`
- `context_writing_score_*`
- `context_dynamic_budget_*`

其中：

- `context_dynamic_budget_*` 控制 `meta.context_weight_stage`
- `context_genre_profile_support_composite` 控制复合题材解析
