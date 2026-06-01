# story-plan-chapter-level

`story-plan-chapter-level` 是 `2-卷章` 的章级子技能，负责把卷级规划下钻为 `projects/story/<项目名>/2-卷章/第N卷/第N章.md`。

## 目录树

```text
3-章级/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   ├── chapter-planning-contract.md
│   ├── chapter-payoff-rules.md
│   └── chapter-rhythm-rules.md
├── scripts/
│   └── README.md
├── templates/
│   ├── chapter-planning.template.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── chapter-planning-workflow.md
├── knowledge-base/
│   └── chapter-planning-heuristics.md
├── types/
│   ├── type-map.md
│   ├── chapter-planning-type-map.md
│   └── payoff-genre-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## 快速入口

- 调用技能：`$story-plan-chapter-level`
- 必需上游：`projects/story/<项目名>/2-卷章/整体规划.md` 与 `projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- 输出真源：`projects/story/<项目名>/2-卷章/第N卷/第N章.md`
- 运行时边界：`guardrails/guardrails-contract.md`

## 关键门禁

- 章级只写 planning，不写正文。
- `本章爽点设计` 必须包含读者期待、上承 promise、类型画像、角色锚点、爽点形态、蓄势、兑现动作、满足差值、夸张逻辑、代价余波和余味牵引。
- 爽点必须与角色个性高度相关，允许夸张，但必须能回指角色动机、处境压力或成长轨迹。
- 爽点必须经过 `genre_payoff_profile` 类型画像校准，避免不同类型小说变成同一种爽法。
- 所有高潮点都必须用 `payoff_variation_axis` 标明与近邻章节的差异，避免反杀、揭秘、打脸、升温、治愈、牺牲或奇观重复。
- 多章出现高超对决时，必须用 `duel_variation_axis` 标明对手、场域、胜法、代价或情绪色彩的差异。
- `本章悬念开关` 必须包含 `上承卷级悬念 / 本章读者可知 / 本章角色可知 / 本章悬念线程动作 / 本章需要隐藏的 / 本章误导/疑阵 / 本章揭秘的 / 本章只埋不揭的 / 章末悬念压力 / 本章悬念负载 / 正文禁止上帝视角说明`。
- `本章节奏曲线` 必须包含 `selected_pack / selected_mode / mode_selection_reason / payoff_type / rhythm_intensity / previous_next_contrast / 七步职责映射 / 规划义务 / 义务段位 / 建议写法` 与 Mermaid 图。
- `payoff_type / micro_payoff` 必须消费爽点设计，不得另起一套读者满足判断。
- `本章任务线` 必须包含 `汇聚动作 / 未汇聚任务去向`。
- `本章线索` 与 `本章伏笔` 必须分离，并服从 `本章悬念开关`。

## 验证

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章/3-章级 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/smoke_test_skill_2_0.py .agents/skills/story/2-卷章/3-章级 --mode delivery
```
