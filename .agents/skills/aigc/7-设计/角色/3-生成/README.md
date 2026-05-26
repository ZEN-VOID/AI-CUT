# aigc 7-设计/角色/3-生成

Skill 2.0 包：从 `角色/2-设计` 的角色设计文档调用 imagegen，生成角色单主体主图、多视图主体设计图，并同步落 JSON prompt。

## Directory Tree

```text
3-生成/
├── references/
│   └── character-generation-contract.md
├── scripts/
│   └── README.md
├── templates/
│   ├── character-main-image-prompt-template.json
│   ├── character-multiview-prompt-template.json
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── character-generation-workflow.md
├── knowledge-base/
│   └── character-generation-heuristics.md
├── types/
│   └── character-generation-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Use

调用 `$aigc-design-character-generation`，提供 `projects/aigc/<项目名>/` 或单个角色名。技能会读取：

- `projects/aigc/<项目名>/7-设计/角色/2-设计/<角色名>.md`
- `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`

输出到：

- `projects/aigc/<项目名>/7-设计/角色/3-生成/<主体ID>-<主体名称>-主图.<ext>`
- `projects/aigc/<项目名>/7-设计/角色/3-生成/<主体ID>-<主体名称>-主图.json`
- `projects/aigc/<项目名>/7-设计/角色/3-生成/<主体ID>-<主体名称>-多视图.<ext>`
- `projects/aigc/<项目名>/7-设计/角色/3-生成/<主体ID>-<主体名称>-多视图.json`

## Boundary

本技能只消费上游设计文档并调用 imagegen。它不重新设计角色主体，不修改上游 `2-设计`，不生成场景、道具或视频提示词。

## Visual Governance

- 入口拓扑、证据链和状态流位于 `SKILL.md` 的 `Visual Maps`。
- 批量/降级汇流、失败回路和 worker 返回形状位于 `steps/character-generation-workflow.md`。
- reviewer provider 与本地 checklist 口径位于 `review/review-contract.md`。
