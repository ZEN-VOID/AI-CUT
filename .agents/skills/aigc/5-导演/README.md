# aigc 5-导演

逐集导演批注注入技能。默认读取 `projects/aigc/<项目名>/4-编剧/第N集.md`，结合 `2-美学/画面基调/全局风格协议.md` 和用户指名导演，在每个画面点后内联新增：

```text
（导演批注：XXX）
```

导演批注会和原剧本一起传递给下游表演技能包；关键批注必须让演员能把心理、关系、信息差和导演意图转成具体、显式、画面化的表演方式。

## Directory Tree

```text
5-导演/
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
├── agents/openai.yaml
├── references/anticlimax-strategy-contract.md
├── references/directorial-authorship-contract.md
├── references/director-annotation-contract.md
├── references/episode-visual-spine-contract.md
├── references/information-asymmetry-contract.md
├── references/scene-rhythm-contract.md
├── review/review-contract.md
├── templates/output-template.md
├── scripts/README.md
├── knowledge-base/director-style-index.md
├── CHANGELOG.md
└── README.md
```

## Runtime Output

- `projects/aigc/<项目名>/5-导演/` 下的 `第N集.md`
- `projects/aigc/<项目名>/5-导演/执行报告.md`
- 报告中的 `Performance Handoff Map`，用于表演技能包读取表演外化种子

## Required References

正式导演批注任务默认加载：

- `episode-visual-spine-contract.md`：整集导演意图规划与视觉主轴
- `directorial-authorship-contract.md`：导演创作干货与可演可拍取舍
- `information-asymmetry-contract.md`：观众/角色信息差与揭示/隐藏策略
- `scene-rhythm-contract.md`：场景节奏、信息密度和转出方式
- `anticlimax-strategy-contract.md`：高点满足/反高潮/延迟满足策略
