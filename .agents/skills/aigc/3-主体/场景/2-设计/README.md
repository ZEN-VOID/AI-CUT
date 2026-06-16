# aigc 3-主体 / 场景 / 2-设计

`$aigc-scene-design` 将上游 `场景/1-清单` 的汇总式场景清单扩展为单个场景主体的细目设计稿。它负责研究、物语、空间解构、摄影语汇和英文图像提示词，不负责重新生成场景清单，也不直接生成图片。研究层必须形成 `research_brief`、来源姿态、不确定性、视觉翻译和 prompt 证据链，而不是只写考据段。

## 快速入口

```bash
# 结构检查
test -f .agents/skills/aigc/3-主体/场景/2-设计/SKILL.md
test -f .agents/skills/aigc/3-主体/场景/2-设计/CONTEXT.md
find .agents/skills/aigc/3-主体/场景/2-设计 -maxdepth 2 -type f | sort
```

## 目录树

```text
2-设计/
├── references/
│   ├── scene-design-contract.md
│   ├── design-output-contract.md
│   ├── design-slot-review-contract.md
│   └── workflow-supervision-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── scene-design-heuristics.md
├── types/
│   └── scene-design-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

`test-prompts.json` 用于 runtime-spine dry-run / regression prompts，覆盖单场景设计、增量补缺和纯空镜 prompt repair。

## 输出位置

- 单场景设计稿：`projects/aigc/<项目名>/3-主体/场景/2-设计/S###-<场景名>.md`
- 可选执行报告：`projects/aigc/<项目名>/3-主体/场景/2-设计/执行报告.md`

## 固定画面约束

- 场景设计固定为纯空镜。
- 不出现人物、人体局部、剪影、倒影或人群。
- 英文 prompt 必须包含 `empty shot, no people, no human figures` 等等价约束。
- `## 4. 解构` 下方必须先写 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID、英文 prompt 开头保持一致。
- 最终英文整合 prompt 必须以主体 ID 号开头，显式包含有来源姿态的时间和地域锚点，并能通过 prompt 证据链回指来源姿态或保守化处理；不得编造具体年代、地点、族群、宗教或建筑流派。
- 最终英文整合 prompt 必须按场景类型包含空间风格 token：建筑/室内/街区可用建筑或室内风格；自然、超现实、交通或抽象空间应使用地理/生态/材质/变形规则/路径节点逻辑，不得强行建筑化。
- 最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息；只拼主体 ID、风格、时间地域或 no people 等前缀/后缀不算完成。
- `design-output-contract.md`、`design-slot-review-contract.md` 和 `workflow-supervision-contract.md` 必须进入入口加载、执行节点和 review gate，不得作为旁路文档漂移。

## 研究层升级要点

- `research_brief`：记录研究问题、证据矩阵和会影响设计的判断。
- `source_posture`：区分项目资料、用户资料、常识、LLM 推断、网络来源和未解不确定性。
- `uncertainty_register`：冷门、文化、年代、地域、建筑制式等风险不能被写成确定事实。
- `visual_translation`：每条关键研究必须落到可见空间、材质、光线、陈设、构图或 prompt token。
- `prompt_evidence_chain`：英文 prompt 的关键 token 必须能回指研究、视觉翻译、Scene Design 或 Cinematography；主体 ID 开头、时间与地域 token、`space_style_token`、`deconstruction_coverage` 是必查 token 组。
