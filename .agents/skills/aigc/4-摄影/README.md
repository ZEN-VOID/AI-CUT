# aigc 4-摄影

`4-摄影` 将 `projects/aigc/<项目名>/3-运动/第N集.md` 的逐集运动强化稿升级为摄影稿：保留原画面性字段标题，并把字段正文改写为连续 `[起始秒-结束秒]` 分镜时间段；用户明确跳过运动强化时可回退 `2-编导/第N集.md`。组间与跨场景创意转场由下游 `5-分组` 连接件承接。

## 目录树

```text
4-摄影/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## 快速入口

- 技能入口：`SKILL.md`
- 运行上下文：`CONTEXT.md`
- 项目级必读：`projects/aigc/<项目名>/MEMORY.md`
- 项目北极星：`projects/aigc/<项目名>/0-初始化/north_star.yaml`
- 项目团队配置：`projects/aigc/<项目名>/team.yaml`
- 画面匹配：`references/visual-matching-contract.md`
- 节奏术语表：`references/global-rhythm-terminology-glossary.md`
- 节拍判断：`references/beat-analysis-contract.md`
- 画面节奏：`references/visual-rhythm-analysis-contract.md`
- 段落密度曲线：`references/sequence-density-curve-contract.md`
- 镜头时值与短剧·AIGC 压缩：`references/shot-duration-decision-contract.md`
- 高潮分镜：`references/peak-shot-language-contract.md`
- 边界交出：`references/transition-design-contract.md`
- 段落观看意图与逐点归属：`references/visual-sequence-alignment-contract.md`
- 分镜计划汇流：`references/shot-planning-integration-contract.md`
- 功能性影视投影：`references/functional-cinematic-projection-contract.md`
- 非复述型分镜：`references/functional-cinematic-projection-contract.md#Content-Paraphrase-Is-Not-Shot-Detail`、`review/review-contract.md#Acceptance-Checklist`
- AI 视频提示词执行稳定性：`references/ai-video-prompt-execution-contract.md`
- 摄影语法变化：`steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR`、`references/cinematic-technique-library.md`
- 动态时间段画面：`references/dynamic-lens-language-contract.md`
- 自然成稿：`references/natural-shot-detail-writing-contract.md`
- 镜头连续性：`references/shot-continuity-contract.md`
- 技法库：`references/cinematic-technique-library.md`
- 流程：`steps/cinematography-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`
- 逐集摄影模板（含多场景示例）：`templates/episode-cinematography.template.md`
- 可复用摄影经验：`knowledge-base/cinematography-heuristics.md`

## 输出

- 输入：优先 `projects/aigc/<项目名>/3-运动/第N集.md`；回退模式为 `projects/aigc/<项目名>/2-编导/第N集.md`
- 输出：`projects/aigc/<项目名>/4-摄影/第N集.md`
- 报告：`projects/aigc/<项目名>/4-摄影/执行报告.md`
- 分镜落盘格式：保留画面性字段标题，字段下固定写 `[起始秒-结束秒]`，例如 `[0-2秒]`、`[2-3秒]`；`心理反应/心理变化/情绪反应/思考反应/认知变化/内心反应` 也必须转译为可见表演微动态后画面化，不新增统一 `分镜画面：` 字段，也不附加第二套摄影说明字段。
- 当前格式是连续性承载面：原字段标题保归属，字段内连续时间段保镜内首尾，相邻字段块末段/首段保上下画面、摄影和运镜交接。
- 段落级连续运镜只作为内部 `sequence_profile`；最终仍按画面句子逐点落在原字段标题下，每个时间段必须能回指所属 `visual_unit`。
- 连续观看段落必须按需形成内部 `sequence_density_curve`，先判断整段哪里省镜头、哪里加密、哪里停顿、哪里硬切、哪里交出；5-6 镜只作为 set-piece 链条例外，必须每镜都有独立动作结果或声音打点。
- 每个时间段还应能稳定改写为 AI 视频提示词：镜头先行包裹动作、方向参照明确、光线写出结果、表演微动态可见，但不在原字段标题下直接粘贴完整提示词分栏模板。
- 每个时间段必须通过源句复述扣除测试：去掉上游原句已有主体、动作、道具和事实后，仍能读出摄影机如何看、动、停、转焦、布光或交接。
- 机械校验脚本已扩展：frontmatter 存在性检查、短剧·AIGC 时间段范围提示（<1s / >3s / >5s）、抽象阐释词扫描、空原字段时间段组检查、时间段连续性检查，以及 2 段集中提示。快节奏平台默认允许高切换密度；仅在显式 `--strict-segment-distribution` 时将 2 段集中视为错误。
- 机械校验脚本只证明结构有效；交付前还必须执行 `review/review-contract.md` 的质量门禁。
