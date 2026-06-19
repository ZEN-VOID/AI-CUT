# aigc 4-编剧

`4-编剧` 将 `1-分集` 或用户指定的单集小说正文改编为逐集影视剧本。它负责题材类型解析、叙事情节解析、戏剧意图提炼、影视化缺口诊断、保真剧本化、受控情节补写、短剧节奏机制、高潮强化、尾钩设计、必要细节补充、陈述性信息转语音，以及 AIGC 下游交接证据。

本包现阶段不把武侠、玄幻、科幻、魔幻拆成子技能，而是在 Skill 2.0 父级合同下用 `types/` 做二维类型配置：先选 `呈现方式`，再选 `题材类型`，最终按 `呈现方式 x 题材类型` 形成本集可消费的编剧策略画像。呈现方式支持 `正剧` 与 `解说剧`；没有显式指定时默认 `正剧`。`解说剧` 必须完全按照故事源内容，先建立 `Jieshuoju Source Unit Coverage Map`，再把陈述性部分全部处理为 `旁白（主体）` 与 `旁白画面`，并用 `Jieshuoju Field Variety Map` 防止正文退化为连续旁白清单。

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
│   ├── type-map.md
│   ├── default/default.md
│   ├── presentation/
│   │   ├── 正剧.md
│   │   └── 解说剧.md
│   └── genre/
│       ├── 武侠剧.md
│       ├── 玄幻剧.md
│       ├── 科幻剧.md
│       └── 魔幻剧.md
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
- 类型组合：每次主链先生成 `type_axis_selection`，选择 `types/presentation/*.md` 中一个呈现方式包，并优先继承 `2-美学/类型风格.md` 的 `Genre Axis Classification` / `primary_genre_axis` 选择 `types/genre/*.md` 或 `types/default/default.md` 中一个题材包，再生成 `screenwriting_type_combination_profile`；组合画像只能影响声音字段、节奏、受控补写、高潮/尾钩和边界检查，不替代父级输出路径或 review gate。
- 输出：`projects/aigc/<项目名>/4-编剧/第N集.md`。
- 报告：`projects/aigc/<项目名>/4-编剧/执行报告.md`，正式写回时必须包含 `Screenplay Mode Decision`、`Type Axis Selection Map`、`Screenwriting Type Combination Profile`、`Execution Decision Trace`、`Reference Execution Matrix`、`Upstream Creative Direction Matrix`、`Type Style Application Map`、`Subject Registry Application Map`、`Scene Asset Integration Map` 或 N/A、`Dramatic Intent Map`、`Dramatization Gap Map`、`Controlled Adaptation Plan`、`Continuity Detail Map`、`Rewrite Scope Check`、`Rule Evidence Map`、显式 `解说剧` 的 `Jieshuoju Source Unit Coverage Map` 与 `Jieshuoju Field Variety Map`、`N/A Justification`、`Repair Log`、`Audio Visual Pairing Map` 和 `Same Frame Continuity Map`。
- 下游：`5-导演`、`6-分镜`、`7-摄影`、`8-分组` 等阶段可消费剧本层输出；这些下游真源不得被本技能提前越权写入。`backup/5-表演`、`backup/6-氛围`、`backup/9-光影` 仅作显式 legacy 回读。

## Runtime Spine

- `SKILL.md` 是 runtime spine 和唯一主合同。
- `CONTEXT.md` 是经验层，每次调用随 `SKILL.md` 加载。
- `references/` 只作为被 `SKILL.md` 授权的细则层。
- `knowledge-base/` 只保存外部资料索引。
- `scripts/` 只做机械辅助，不生成创作正文。
