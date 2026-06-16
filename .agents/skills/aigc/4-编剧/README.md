# aigc 4-编剧

`4-编剧` 将 `1-分集` 或用户指定的单集小说正文改编为逐集影视剧本。它负责题材类型解析、叙事情节解析、保真剧本化、短剧节奏机制、高潮强化、尾钩设计、必要细节补充、陈述性信息转对白/独白/喊出式台词，以及 AIGC 下游交接证据。

## Directory Tree

```text
4-编剧/
├── agents/openai.yaml
├── references/
│   ├── imported-reference-adaptation-map.md
│   ├── screenwriting-masters-and-shortdrama-rhythm-contract.md
│   └── copied contracts from references/
├── review/review-contract.md
├── templates/output-template.md
├── types/
├── knowledge-base/research-sources.md
├── scripts/README.md
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Usage

- 输入：`projects/aigc/<项目名>/1-分集/第N集.md` 或用户粘贴的单集小说正文。
- 输出：`projects/aigc/<项目名>/4-编剧/第N集.md`。
- 报告：`projects/aigc/<项目名>/4-编剧/执行报告.md`，正式写回时必须包含 `Execution Decision Trace`、`Reference Execution Matrix`、`Rule Evidence Map`、`N/A Justification`、`Repair Log`、`Audio Visual Pairing Map` 和 `Same Frame Continuity Map`。
- 下游：`5-导演`、`6-分镜`、`7-摄影`、`8-分组` 等阶段可消费剧本层输出；这些下游真源不得被本技能提前越权写入。`backup/5-表演`、`backup/6-氛围`、`backup/9-光影` 仅作显式 legacy 回读。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `references/` 只作为被 `SKILL.md` 授权的细则层。
- `knowledge-base/` 只保存外部资料索引。
- `scripts/` 只做机械辅助，不生成创作正文。
