# aigc 14-审片

## Purpose

`14-审片` 用于审查 `13-画布` 或 LibTV 入口产出的实际视频素材，覆盖视频本体问题、prompt 匹配、创作质量、好/坏示例比较学习，并把发现的问题落到正确修复层。`SKILL.md` 是唯一 runtime spine，直接承载 `N0 -> N7` 主节点、模块授权、触发表、量化口径、注意力协议、检查点和输出门；审片方法按素材信号选择 source fidelity、连续性、表演、摄影、节奏、声音、道具、伦理安全、AIGC 伪影、prompt 执行、候选片比较和修复设计等方法。

- `14-审片/`：审片报告和证据。
- `10-分组/`：高置信的分镜组修复。
- `CONTEXT.md`：跨项目可复用的鉴赏力学习。
- 源层技能：极高置信、可复现的系统性问题。

执行顾问与复核流程时，本技能把项目 `team.yaml` 中的监制组相关成员作为审片顾问团，只提供节点级证据补强、prompt 归因、创作质量门、示例校准和落点风险建议；最终 verdict、报告落盘和上游修复仍由主 agent 按本技能合同裁决。

## LibTV Intake

审片目标可以直接来自 LibTV：

- `LibTV 链接 + 视频名`：从 `canvas?projectId=<uuid>` 提取项目，视频名默认等于明确给出的分镜组 ID。
- `LibTV 画布名 + 视频名`：通过 `libtv project list --name` 唯一匹配画布。
- `projectUuid + 视频名` 或当前 `.libtv/project.json` 绑定项目。

所有远端入口都必须先走 `.agents/skills/cli/libTV`：查询节点、保存 node query、下载真实视频到 `projects/aigc/<项目名>/13-画布/`，再抽帧审片。远端 prompt、taskInfo 和 result URL 只作为生成路线证据，不能替代真实视频内容分析。

## Directory Tree

```text
14-审片/
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
├── README.md
├── CHANGELOG.md
├── agents/openai.yaml
├── references/
│   ├── libtv-intake-contract.md
│   ├── review-method-palette-contract.md
│   ├── video-evidence-contract.md
│   └── video-naming-contract.md
├── review/
├── types/
├── knowledge-base/
├── templates/
└── scripts/
```

## Runtime Output

```text
projects/aigc/<项目名>/14-审片/第N集/<group_id>[-variant]-审片.md
```
