# aigc 3-Detail

`aigc-detail` 将 `2-Global/episode_root.json` 细化为镜级 detail root。它固定先执行 `1-分镜构图`，再按 `角色表现 / 氛围表现 / 摄影表现 / 运镜手法 / 转场特效` 写回，最后刷新阶段 `validation-report.md`。

## Directory Tree

```text
3-Detail/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── TODO.md
├── agents/
│   └── openai.yaml
├── knowledge-base/
│   └── detail-heuristics.md
├── references/
│   ├── incremental-patch-playbook.md
│   ├── validation-report-closure-guide.md
│   ├── 创作评审标尺.md
│   ├── 思行网络.md
│   ├── 模板字段填写指南.md
│   ├── 正反例.md
│   ├── 电影学院派知识接线.md
│   ├── 编剧手册.md
│   ├── 能力通道图谱.yaml
│   ├── 路由画像.yaml
│   └── 镜头语言.md
├── review/
│   └── review-contract.md
├── scripts/
│   ├── validate_creative_guidance.py
│   ├── validate_node_packs.py
│   └── validate_stage_output.py
├── steps/
│   └── detail-thinking-action-workflow.md
├── templates/
│   └── output-template.md
├── types/
│   └── type-map.md
├── _shared/
└── legacy/
```

## Quick Entry

```bash
python3 .agents/skills/aigc/3-Detail/scripts/validate_node_packs.py
python3 .agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py
python3 .agents/skills/aigc/3-Detail/scripts/validate_stage_output.py .agents/skills/aigc/3-Detail/_shared/episode_detail.json
```

## Runtime Output

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/3-Detail/validation-report.md`

## Notes

- `references/思行网络.md` 仍保留为旧校验器和既有引用的兼容入口。
- `steps/detail-thinking-action-workflow.md` 是 Skill 2.0 的节点真源。
- `legacy/compat/` 只用于迁移、投影和对照，不参与当前主链写回。
