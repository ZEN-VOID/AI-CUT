# aigc 5-设计 / 场景 / 2-设计

`$aigc-scene-design` 将上游 `场景/1-清单` 的汇总式场景清单扩展为单个场景主体的细目设计稿。它负责研究、物语、空间解构、摄影语汇和英文图像提示词，不负责重新生成场景清单，也不直接生成图片。研究层必须形成 `research_brief`、来源姿态、不确定性、视觉翻译和 prompt 证据链，而不是只写考据段。

## 快速入口

```bash
# 结构检查
test -f .agents/skills/aigc/5-设计/场景/2-设计/SKILL.md
test -f .agents/skills/aigc/5-设计/场景/2-设计/CONTEXT.md
find .agents/skills/aigc/5-设计/场景/2-设计 -maxdepth 2 -type f | sort
```

## 目录树

```text
2-设计/
├── references/
│   └── scene-design-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── scene-design-workflow.md
├── knowledge-base/
│   └── scene-design-heuristics.md
├── types/
│   └── scene-design-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## 输出位置

- 单场景设计稿：`projects/aigc/<项目名>/5-设计/场景/2-设计/S###-<场景名>.md`
- 可选执行报告：`projects/aigc/<项目名>/5-设计/场景/2-设计/执行报告.md`

## 固定画面约束

- 场景设计固定为纯空镜。
- 不出现人物、人体局部、剪影、倒影或人群。
- 英文 prompt 必须包含 `empty shot, no people, no human figures` 等等价约束。

## 研究层升级要点

- `research_brief`：记录研究问题、证据矩阵和会影响设计的判断。
- `source_posture`：区分项目资料、用户资料、常识、LLM 推断、网络来源和未解不确定性。
- `uncertainty_register`：冷门、文化、年代、地域、建筑制式等风险不能被写成确定事实。
- `visual_translation`：每条关键研究必须落到可见空间、材质、光线、陈设、构图或 prompt token。
- `prompt_evidence_chain`：英文 prompt 的关键 token 必须能回指研究、视觉翻译、Scene Design 或 Cinematography。
