# libTV画布流

标准 AIGC 13-画布 LibTV 画布控制技能包。

## Directory Tree

```text
.agents/skills/aigc/13-画布/libTV画布流/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   ├── canvas-control-contract.md
│   └── image-order-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── canvas-control-workflow.md
├── knowledge-base/
│   └── libtv-canvas-control-heuristics.md
├── types/
│   ├── type-map.md
│   ├── full-canvas-control.md
│   ├── backfill-only.md
│   └── node-rebuild-only.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Use

输入：

- `projects/aigc/<项目名>/10-分组/第N集.md`
- `projects/aigc/<项目名>/11-主体/角色/3-生成/`
- `projects/aigc/<项目名>/11-主体/场景/3-生成/`
- `projects/aigc/<项目名>/11-主体/道具/3-生成/`

输出：

- LibTV 画布项目。
- 上传后的主体参考图节点。
- 已回刷 `图片N 主体名 UUID` 的分组稿。
- 提交 prompt 中按 `图片N 主体名 {{Image N}} UUID` 排列的主体信息。
- 未执行生成的视频节点。
- `projects/aigc/<项目名>/13-画布/libTV画布流/第N集/` 下的证据文件。
