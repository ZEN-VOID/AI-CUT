# Init Heuristics

本文件保存 `story-init` 的稳定经验和可复用启发，不拥有入口路由权。

## Reusable Heuristics

- 初始化最重要的是路由正确：小说走 `projects/story/<项目名>/`，影视走 `projects/aigc/<项目名>/`。
- `team.yaml` 必须先于 `north_star.yaml` 锁定；否则下游无法判断初始化判断来自谁。
- 少量用户 brief 不等于需要问卷模式。先让 planning 固定题包直答，并把下游问题写入 `unknowns`。
- 初始化输出不要压成单主文件；`team.yaml + STATE.json + MEMORY.md + story-source-manifest + init_handoff` 的分工能降低后续漂移。
- `MEMORY.md` 只写当前项目长期偏好和禁区；跨项目调试经验写回技能 `CONTEXT.md` 或本知识库。
- 创意资料统一从 `creative-seed-routing/module-spec.md` 进入，避免父技能散点直连 leaf docs。
- 重初始化要覆盖刷新 team 与 state 管理工件，但不可无授权删除故事主源。
- 当真实 subagents 或 reviewer 被上层策略阻断时，宁可明确 blocked/降级，也不要写成“顾问团已执行”。

## Repair Playbook

1. 媒介混线：先检查 registry、`agents/openai.yaml` 和 `Scope` 负向路由。
2. team 双真源：删除或降级平行 manifest，统一回 `team.yaml`。
3. runtime 半完成：同步审计目录、`STATE.json.paths`、`stage_progress`、`task_log`。
4. planning 直答缺证据：回到 `roles.planning.members` 与 fixed packet，不用问卷补洞。
5. 输出模板漂移：回到 `templates/output-template.md`，逐项对齐 Output Contract 五字段。

## Success Pattern

一次健康的初始化应能回答：

- 这是哪本书、面向谁、承诺什么体验？
- 谁作为 planning kickoff owner 给出第一轮判断？
- 哪些内容已确定，哪些留给 cards/planning？
- 下游应该读哪个文件，不能读哪个旧文件？
