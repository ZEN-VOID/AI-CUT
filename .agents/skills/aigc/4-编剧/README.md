# aigc 4-编剧

`4-编剧` 将 `1-分集` 或用户指定的单集小说正文改编为逐集影视剧本。它负责题材类型解析、叙事情节解析、保真剧本化、短剧节奏机制、高潮强化、尾钩设计、必要细节补充、陈述性信息转语音，以及 AIGC 下游交接证据。技能支持 `正剧` 与 `解说剧` 两种模式；没有显式指定时默认 `正剧`。`解说剧` 必须完全按照故事源内容，先建立 `Jieshuoju Source Unit Coverage Map`，再把陈述性部分全部处理为 `旁白（主体）` 与 `旁白画面`，并用 `Jieshuoju Field Variety Map` 防止正文退化为连续旁白清单。

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
- 模式：默认 `正剧`；显式要求 `解说剧` 时，先按 source 单元类型覆盖 source，再让陈述性 source 信息全部走 `旁白/旁白画面`；上游已有对白仍逐字冻结为对白，可见动作和环境不被过度旁白化；正文不得用方括号叙事小标题，含 3 条及以上旁白对的场景必须有非旁白视觉字段承托。
- 输出：`projects/aigc/<项目名>/4-编剧/第N集.md`。
- 报告：`projects/aigc/<项目名>/4-编剧/执行报告.md`，正式写回时必须包含 `Screenplay Mode Decision`、`Execution Decision Trace`、`Reference Execution Matrix`、`Upstream Creative Direction Matrix`、`Type Style Application Map`、`Subject Registry Application Map`、`Scene Asset Integration Map` 或 N/A、`Rule Evidence Map`、显式 `解说剧` 的 `Jieshuoju Source Unit Coverage Map` 与 `Jieshuoju Field Variety Map`、`N/A Justification`、`Repair Log`、`Audio Visual Pairing Map` 和 `Same Frame Continuity Map`。
- 下游：`5-导演`、`6-分镜`、`7-摄影`、`8-分组` 等阶段可消费剧本层输出；这些下游真源不得被本技能提前越权写入。`backup/5-表演`、`backup/6-氛围`、`backup/9-光影` 仅作显式 legacy 回读。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `references/` 只作为被 `SKILL.md` 授权的细则层。
- `knowledge-base/` 只保存外部资料索引。
- `scripts/` 只做机械辅助，不生成创作正文。
