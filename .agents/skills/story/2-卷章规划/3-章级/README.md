# story-plan-chapter-level

`story-plan-chapter-level` 是 `2-卷章规划` 的章级子技能，负责把卷级规划下钻为 `projects/story/<项目名>/2-卷章规划/第N卷/第N章.md`。

## 目录树

```text
3-章级/
├── references/
│   ├── chapter-planning-contract.md
│   └── chapter-rhythm-rules.md
├── scripts/
│   └── README.md
├── templates/
│   ├── chapter-planning.template.md
│   └── output-template.md
├── review/
│   └── chapter-planning-review.md
├── steps/
│   └── chapter-planning-workflow.md
├── knowledge-base/
│   └── chapter-planning-heuristics.md
├── types/
│   └── chapter-planning-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## 快速入口

- 调用技能：`$story-plan-chapter-level`
- 必需上游：`projects/story/<项目名>/2-卷章规划/整体规划.md` 与 `projects/story/<项目名>/2-卷章规划/第N卷/卷规划.md`
- 输出真源：`projects/story/<项目名>/2-卷章规划/第N卷/第N章.md`

## 关键门禁

- 章级只写 planning，不写正文。
- `本章节奏曲线` 必须包含 `selected_pack / selected_mode / 七步职责映射 / 规划义务 / 义务段位 / 建议写法` 与 Mermaid 图。
- `本章任务线` 必须包含 `汇聚动作 / 未汇聚任务去向`。
- `本章线索` 与 `本章伏笔` 必须分离。

## 验证

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章规划/3-章级
```
