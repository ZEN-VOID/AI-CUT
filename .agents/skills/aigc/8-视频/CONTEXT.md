# Context: aigc 8-视频

本文件是 `8-视频` 父级入口的经验层知识库。调用同目录 `SKILL.md` 时必须同时加载本文件。它只保存路由经验、修复打法与常见误判，不承载叶子技能的执行细则。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 12000
hard_limit_chars: 24000
status: ok
last_checked_at: 2026-05-30
```

## Type Map

| type | symptom | route | repair |
| --- | --- | --- | --- |
| libtv canvas plan | 用户只说视频阶段、生视频、LibTV、画布流、按 `5-分组` 组级出视频 | `libTV画布流` | 默认路线；生成计划和 CLI handoff，不在父级直接执行 |
| legacy frame visual reference | 用户明确点名旧 A、分镜画面参照、修复旧 A 产物 | `backup/A-分镜画面参照` | 只兼容回读或修复，不迁为默认路线 |
| legacy storyboard reference | 用户明确点名旧 B、分镜故事板参照、修复旧 B 产物 | `backup/B-分镜故事板参照` | 只兼容回读或修复 |
| legacy subject reference | 用户明确点名旧 C、主体参照、修复旧 C 产物 | `backup/C-主体参照` | 默认新任务仍优先用 active `libTV画布流` |
| legacy hybrid reference | 用户明确点名旧 D、主板混合参照、修复旧 D 产物 | `backup/D-主板混合参照` | 只在用户明确要求时进入 |
| query or download | 用户给 LibTV projectUuid、node id、group id、queue record、视频结果查询或下载 | 原所属叶子 -> `.agents/skills/cli/libTV` | 未定位原叶子前不要新建视频真源 |
| cli migration drift | 文档仍写旧会话接口、旧 access-key 凭据模式或旧本地包装器 | active leaf migration | 改为 `libtv login/account/project/group/node/upload/download/model` 交接 |
| parent overreach | 父级直接创建节点、跑 `libtv node --run` 或写 queue/report | 父级边界失守 | 回收为叶子计划层；父级只路由和汇总 |

## Repair Playbook

1. 先判断用户要的是参照路线选择、全新视频计划、查询下载、修复审查，还是旧路线兼容。
2. 父级只输出路由判断；不要在父级临时写 prompt、YAML、manifest、queue、CLI 命令或 report。
3. 默认新视频任务进入 `libTV画布流`；旧 A/B/C/D 只有明确点名、旧产物修复或路径回读时才进入。
4. 只要任务涉及实际 prompt 组装、主体绑定、submit plan、CLI handoff、queue record 或结果报告，就已经进入叶子职责。
5. 只要任务涉及真实 LibTV 远端操作，就必须由叶子加载 `.agents/skills/cli/libTV`，再按新版 `libtv` CLI 命令执行。
6. 若新版 CLI 没有 `CONTEXT.md`，记录为官方 1.0.1 包结构缺口；不要复制旧会话接口经验层冒充新版 CLI 经验层。
7. 若出现旧会话接口词汇，优先修 `libTV画布流/references/official-libtv-cli-handoff.md`、`steps/libtv-canvas-workflow.md`、`review/review-contract.md` 和 templates。

## Reusable Heuristics

- `8-视频` 与 `.agents/skills/cli/libTV` 的关系应类似 `photoGPT` 与 `.agents/skills/cli/imagegen`：前者做计划、类型判断和质量门禁，后者拥有实际 provider / CLI 执行边界。
- 新版 `libtv` 的项目复用真源是 `libtv project use <projectUuid>` 或显式 `-p <projectUuid>`，不是旧会话 ID。
- 新版 `libtv` 的可执行单位是 project / group / node / upload / download / model；AIGC 叶子应把分镜组计划投影成这些命令的 handoff，而不是发一段自然语言执行请求。
- 视频文件名是 `8-视频` 和 `9-审片` 之间的主接口；不要把审片依赖绑到旧会话 ID、node id 或下载顺序上。
- `## x-y-z~x-y-z` 连接件默认不属于新视频计划 job 范围；遇到连接件时跳过，不生成 `<上组~下组>.mp4`。
