# aigc 5-分组

`5-分组` 将 `projects/aigc/<项目名>/4-摄影/第N集.md` 的逐集摄影稿切成完整分镜组；当用户要求直接接手剧本/编导稿，或项目缺少 `4-摄影` 但存在可读剧本源时，也会进入 `direct_screenplay` 路径，自动按约 15 秒/组拆成 production-ready 分镜组。每组重复当前场景标题，在场景标题下方输出 `全局风格：`，再输出组级 `画面风格：`、普通分镜正文和 YAML 统计；相邻分镜组的连续性由下一组第一个普通 `[0-N秒]` 分镜行承担，这个内部口径称为 `回龙帧`。回龙帧必须完整代入上一组结尾状态画面点内容，只调整景别和镜头视角；若该点来自对白、独白、旁白或音效画面，必须同步带入对应声音内容；不生成 `## A~B` 组间连接件，也不输出 `增补首帧：` 或 `回龙帧：` 字段。

## 目录树

```text
5-分组/
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
- 初始化综合：`projects/aigc/<项目名>/team.yaml.init_synthesis.stage_seed_summary."5-分组"`、`init_handoff.grouping_seed`、`north_star.yaml.创作阶段不变量.分组`
- 边界规则：`references/group-boundary-contract.md`
- north_star 风格整理：`references/north-star-projection-contract.md`
- 画面风格：`references/group-visual-tone-contract.md`
- YAML 统计：`references/statistics-yaml-contract.md`
- 流程：`steps/grouping-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`
- 机械校验：`scripts/validate_storyboard_groups.py`

## 输出

- 输入：优先 `projects/aigc/<项目名>/4-摄影/第N集.md`；也接受用户显式指定的剧本/编导稿 direct screenplay source
- 风格真源：`projects/aigc/<项目名>/0-初始化/north_star.yaml`
- 分组综合：只读消费冻结初始化综合，不调用 team 身份、旧 stage profile 或新顾问问答
- 时长口径：标准摄影路径先按 `4-摄影` 正文中每个原画面性字段最后 `[起始秒-结束秒]` 的结束秒累计；direct screenplay 路径由 LLM 按剧本声画 atomic unit 规划约 15 秒/组；落盘后均使用当前分镜组基准下连续递增的 `[N-N秒]`，后一个时间段起点接前一个终点，组内 `时长估算` 取最后结束秒；组头、场景标题、全局风格、画面风格和 YAML 不计入
- 输出：`projects/aigc/<项目名>/5-分组/第N集.md`
- 报告：`projects/aigc/<项目名>/5-分组/执行报告.md`
