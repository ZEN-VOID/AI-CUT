# aigc 9-审片

## Purpose

`9-审片` 用于审查 `8-视频` 产出的实际视频素材，覆盖视频本体问题、prompt 匹配、创作质量、好/坏示例比较学习，并把发现的问题落到正确修复层：

- `9-审片/`：审片报告和证据。
- `5-分组/`：高置信的分镜组修复。
- `CONTEXT.md`：跨项目可复用的鉴赏力学习。
- 源层技能：极高置信、可复现的系统性问题。

执行顾问与复核流程时，本技能把项目 `team.yaml` 中的监制组相关成员作为审片顾问团，只提供节点级证据补强、prompt 归因、创作质量门、示例校准和落点风险建议；最终 verdict、报告落盘和上游修复仍由主 agent 按本技能合同裁决。

## Directory Tree

```text
9-审片/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── agents/openai.yaml
├── references/
├── steps/
├── review/
├── types/
├── knowledge-base/
├── templates/
└── scripts/
```

## Runtime Output

```text
projects/aigc/<项目名>/9-审片/第N集/<group_id>[-variant]-审片.md
```
