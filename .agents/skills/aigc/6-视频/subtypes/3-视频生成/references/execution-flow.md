# 3-视频生成执行流程细则

## Canonical Inputs

- 命中的 `6-视频` 请求 JSON
- `projects/<项目名>/编导/第N集.json`
- `.agents/skills/aigc/6-视频/_shared/video-generation-input.template.json`
- 可选：`projects/<项目名>/画面/` 与 `projects/<项目名>/主体/` 中的引用资产

## Canonical Landing

- tranche 根目录：`projects/<项目名>/视频/生成任务/`
- provider 计划目录：`projects/<项目名>/视频/生成任务/<provider>/第N集/`
- 主计划文件：`submit-plan.json`
- 主简报：`submit-brief.md`

## Workflow

1. 读取上游稳定请求对象，确认 `request_ready`。
2. 若不满足提交前条件，停止并回上游补请求对象。
3. 锁定唯一 provider 或推荐主案。
4. 写 `submit-plan.json`，包括 source request、目标 provider、输出目录、执行说明与回退入口。
5. 写 `submit-brief.md`，包括本轮边界、理由、风险与下一入口。
6. handoff 到外部 provider skill 或人工执行入口。

## Handoff Rules

- 本层结束时默认只给一个下一入口。
- 若 provider 已有外部执行 skill，可直接 handoff。
- 若 provider 当前无本地执行 skill，也必须保留完整 handoff 包，禁止只留一句“手动提交”。
