# aigc 3-摄影

`5-摄影` 将 `projects/aigc/<项目名>/4-表演/第N集.md` 的逐集编导稿升级为带大师级分镜、摄影、运镜、光影、色彩和边界交出锚点的摄影分镜明细稿。组间与跨场景创意转场由下游 `6-分组` 连接件承接。

## 目录树

```text
5-摄影/
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
- 节拍判断：`references/beat-analysis-contract.md`
- 画面节奏：`references/visual-rhythm-analysis-contract.md`
- 段落密度曲线：`references/sequence-density-curve-contract.md`
- 镜头时值与短剧·AIGC 压缩：`references/shot-duration-decision-contract.md`
- 高潮分镜：`references/peak-shot-language-contract.md`
- 边界交出：`references/transition-design-contract.md`
- 段落观看意图与逐点归属：`references/visual-sequence-alignment-contract.md`
- 分镜计划汇流：`references/shot-planning-integration-contract.md`
- 功能性影视投影：`references/functional-cinematic-projection-contract.md`
- AI 视频提示词执行稳定性：`references/ai-video-prompt-execution-contract.md`
- 摄影语法变化：`steps/cinematography-workflow.md#N6.2-CAMERA-GRAMMAR`、`references/cinematic-technique-library.md`
- 动态分镜明细：`references/dynamic-lens-language-contract.md`
- 自然成稿：`references/natural-shot-detail-writing-contract.md`
- 镜头连续性：`references/shot-continuity-contract.md`
- 技法库：`references/cinematic-technique-library.md`
- 流程：`steps/cinematography-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`
- 逐集摄影模板（含多场景示例）：`templates/episode-cinematography.template.md`
- 可复用摄影经验：`knowledge-base/cinematography-heuristics.md`

## 输出

- 输入：`projects/aigc/<项目名>/4-表演/第N集.md`
- 输出：`projects/aigc/<项目名>/5-摄影/第N集.md`
- 报告：`projects/aigc/<项目名>/5-摄影/执行报告.md`
- 分镜落盘格式：每条分镜固定写成 `分镜N（约X秒）:`，默认应用短剧·AIGC 时值压缩；对白、旁白和画外音台词量必须进入时值预算，`约3秒` 以上镜头必须有台词、读秒、表演变化、复杂调度、空间重置或高点证据。
- 段落级连续运镜只作为内部 `sequence_profile`；最终仍按正上方画面句子逐点落 `分镜明细：`，每条分镜必须能回指所属 `visual_unit`。
- 连续观看段落必须按需形成内部 `sequence_density_curve`，先判断整段哪里省镜头、哪里加密、哪里停顿、哪里硬切、哪里交出；5-6 镜只作为 set-piece 链条例外，必须每镜都有独立动作结果或声音打点。
- 每条分镜还应能稳定改写为 AI 视频提示词：镜头先行包裹动作、方向参照明确、光线写出结果、表演微动态可见，但不在 `分镜明细` 中直接粘贴完整提示词分栏模板。
- 机械校验脚本已扩展：frontmatter 存在性检查、短剧·AIGC 秒数范围提示（<1s / >3s / >5s）、抽象阐释词扫描和空分镜明细块检查。
