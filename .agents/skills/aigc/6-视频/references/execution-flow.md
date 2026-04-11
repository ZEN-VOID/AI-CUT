# 6-视频执行流程细则

## Canonical Inputs

- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 可选：`projects/<项目名>/4-主体/` 与 `projects/<项目名>/5-画面/` 中已存在的主体或画面锚点

## Canonical Landing

- 阶段根目录：`projects/<项目名>/视频/`
- `全能参照` 当前主落点：`projects/<项目名>/视频/全能参照/第N集/`
- `首帧参照` 当前主落点：`projects/<项目名>/视频/首帧参照/第N集/`
- `3-视频生成` 当前主落点：`projects/<项目名>/视频/生成任务/<provider>/第N集/`
- 若叶子子技能采用双输出模式，应在该目录内同时落 `第N集.json` 与 `第N集.txt`

## Workflow

1. 锁定本轮视频任务的权威输入与目标工具面。
2. 先由父级裁决唯一路由，再进入命中的叶子子技能。
3. 若命中的叶子子技能复用共享请求骨架，应先回指 `.agents/skills/aigc/6-视频/_shared/` 中的模板真源。
4. 由叶子子技能生成请求 JSON、必要台账与 handoff 信息。
5. 若任务进入真实生成阶段，先进入 `3-视频生成` 写 provider handoff 包。
6. 再 handoff 到命中的 provider skill。

## Handoff Rules

- `6-视频` 结束时，默认先交接给 `3-视频生成`，再由该子技能交给明确的视频 API 执行层。
- 若叶子子技能尚未补齐，则停在父级并返回缺口，不进入提交流程。
