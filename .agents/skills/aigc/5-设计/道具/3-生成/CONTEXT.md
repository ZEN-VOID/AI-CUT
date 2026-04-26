# Context: aigc 道具 3-生成

本文件是 `$aigc-prop-generation` 的经验层知识库，不是过程日志。它沉淀道具生成阶段消费上游设计文档、调用 imagegen、保存主图与多视图资产时的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: initial
recommended_action: keep-generation-heuristics-target-scoped
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-PROP-GEN-01` | 生成阶段开始补写研究、物语或解构 | 阶段越界 | 回到只消费 `2-设计` 的“提示词设计” | 在 `SKILL.md` 和 `references/` 固定非目标 | 无 `2-设计` 文件改动 |
| `TM-PROP-GEN-02` | 多视图图像不像同一个道具 | 参考图断链 | 重跑 Step2，把 `主体名称-主图` 作为参照图 | 多视图 JSON 必填 `reference_image` | 主图和多视图共享轮廓、材质与识别点 |
| `TM-PROP-GEN-03` | JSON 提示词无法追溯来源 | 证据字段缺失 | 补 `source_design_doc`、`source_prompt_section`、`output_image` | 模板固定追溯字段 | JSON 能回指上游 Markdown 和输出图 |
| `TM-PROP-GEN-04` | 普通生成任务误用 CLI/API | imagegen 路由漂移 | 回到内置 `image_gen` 默认路径 | 每次读取 `$imagegen` 合同 | 无额外 API key 依赖 |
| `TM-PROP-GEN-05` | 文件名丢失 `-主图` 或 `-多视图` | 命名门禁缺失 | 按 Output Contract 重命名并同步 JSON | review gate 检查命名后缀 | 图像与 JSON 同 stem |
| `TM-PROP-GEN-06` | 输出被保存到 `$CODEX_HOME` 或临时目录 | 持久化缺口 | 复制最终资产到项目 canonical 输出目录 | 把项目路径写入 prompt/result 记录 | 报告路径在 workspace 内 |
| `TM-PROP-GEN-07` | Skill 2.0 文件齐全但执行者仍看不出分支与汇流 | 拓扑表达不足 | 在 `SKILL.md`、`steps/`、`types/` 或 `review/` 补 Mermaid 图和节点交接表 | 结构校验之外增加语义 review gate | 可从图表追踪 single/batch/prompt-only/repair/review 路径 |

## Repair Playbook

1. 先确认问题属于输入设计文档、主图生成、多视图参考、JSON 追溯、输出命名、路径持久化还是 imagegen 路由。
2. 若缺上游设计文档，回到 `道具/2-设计`；不要在生成阶段临时创作主体设计。
3. 若设计文档缺“提示词设计”，暂停生图并要求修复上游设计文档。
4. 若多视图漂移，优先强化参照图和锁定识别点，而不是新增设定。
5. 若图像已生成但未落盘到项目目录，按 `$imagegen` 的 persistence gate 把选定最终资产复制到 `3-生成`。
6. 若真实 subagent 或 reviewer 被阻断，按 `SKILL.md` 的 Subagent Execution Contract 报告降级路径。
7. 若校验器通过但用户指出“批量定制不细”，优先检查 Visual Maps、Node Network、Failure Routing、Provider Degradation 和 Output Contract Alignment 是否足够具体。

## Reusable Heuristics

- 生成阶段的创造力在于“忠实执行设计”，不是重新发现主体。
- 主图是多视图的视觉锚点；多视图模板是排版与视角组织，不是新设计合同。
- 道具多视图应先锁定 `subject_invariant_lock`，再安排 hero、orthographic、detail、scale/state 视图；功能部件数量、位置、材质老化和轮廓比例比画面装饰更重要。
- 道具多视图生产板必须有顶左身份牌：图中优先显示短 ASCII 道具 ID，完整主体名进入 JSON；若模型文字不稳，应保留干净 badge plate 供后期叠字。
- JSON 提示词是可复跑证据，应保存输入来源、最终 prompt、参考图和输出图路径。
- 对道具生成，最容易漂移的是尺度、材质老化和功能部件；这些应从上游 prompt 中原样保留。
- 普通项目生图默认使用 `$imagegen` 的内置 `image_gen` 路由；CLI/API 只在用户显式选择时使用。
- Mermaid 图不是装饰项；它承担把分型、分支、汇流和失败回路从文字清单中显形的职责。
