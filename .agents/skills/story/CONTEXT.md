# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2919
current_lines: 67
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-08T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 根目录缺少总 `SKILL.md` / `CONTEXT.md`，导致执行者只能看到分阶段 skill | root source contract | 在 `.agents/skills/story/` 补齐根级入口与根级经验层 | 把跨阶段拓扑、总路由、共享 carrier 边界固定在根级真源，不再散落到各阶段自己解释 | 泛化 `story2026` 请求能先命中根入口，再转到唯一阶段 |
| 跨阶段共享 reference 被误下沉到某一阶段，后续产生第二真源 | canonical source governance | 回到根级 `references/README.md` 重新确认共享归属 | 共享合同只放根级 `references/`，阶段只保留私有细则 | 同一份 schema 不再被多个阶段各自改写 |
| 用户问题同时触发多个阶段，执行者直接跳到“看起来最像”的下游阶段 | routing contract | 先判 truth role，再按总路由表选择最早 owner | 在根级 `SKILL.md` 固化 route matrix 与 owner 表 | 问题能稳定落到唯一默认入口 |
| 共享 helper 被多个阶段复制维护，导致路径或状态规则漂移 | shared script layer | 把共用 helper 收束到根级 `scripts/` | 对 2+ 阶段共用的路径/状态/CLI 逻辑，统一提升为共享入口 | 脚本调用路径与运行态规则只需修一处 |
| 根级 skill 变成“阶段细则合集”，反而制造第二层重复 | scope discipline | 收缩根级 skill，只保留总线职责 | 阶段细节留在各阶段 `SKILL.md`，根级只保留拓扑和边界 | 根级文件可快速说明系统，不需要复制阶段合同 |
| `story2026` 用户命令已切到 `/story-*`，但 skill frontmatter、workflow registry、模板 metadata 仍残留 `webnovel-*` / `story2026-*`，导致命名双真源 | canonical naming governance | 新增根级 `references/command-naming-contract.md`，并同步改写 skill/frontmatter、workflow、模板与命令文档 | 将命名迁移固定为“命名合同 -> 文档/技能 -> workflow/state -> 测试”的单一升级顺序，旧名只留 alias 层 | 用户侧、状态层与模板层都只写 canonical `story-*`，旧名仅能被兼容读取 |
| 共享脚本已经开始写 `.webnovel/tasks/<run_id>/` 三省工件，但根/阶段合同不承认它们 | governance artifact governance | 在根级与关键阶段 skill 中显式加入 `.codex/*` 真源回指和 shadow 工件链说明 | 把 task artifact chain 固化成跨阶段共享证据层，并要求命令文档、阶段技能、CONTEXT 同步承认 | 运行脚本、技能合同、命令文档对任务工件链口径一致 |

## Repair Playbook

1. 先判断问题是“缺总入口”“路由错”“真源错认”“共享 carrier 误放置”中的哪一种。
2. 若问题跨两个以上阶段，先回根级 `story/SKILL.md` 做总线诊断，再进入阶段修复。
3. 若同一规则在多个阶段重复出现，优先找根级 canonical source，而不是逐个阶段补丁。
4. 若共享脚本或共享 reference 失配，先修共享层，再让阶段合同回指共享层。
5. 收尾验证固定检查：
   - 根级 `SKILL.md` 是否能解释主链与卫星关系
   - 根级 `CONTEXT.md` 是否记录跨阶段经验
   - 根级 `references/README.md` 是否仍只列跨阶段共享合同
   - 泛化请求是否能稳定路由到唯一 owner

## Reusable Heuristics

- 根级 skill 最有价值的工作不是“替阶段再说一遍”，而是回答“该去哪一层、该信哪一层、哪些共享层先读”。
- 当一个体系已经有多个成熟阶段 skill 时，缺的往往不是更多子技能，而是一个总线级 canonical source。
- 跨阶段共享文档如果不能一句话说明“被哪些阶段共同消费”，就不该放在根级 `references/`。
- 遇到泛化 `story2026` 请求，先判 truth role，再判 stage，通常比先看动词更稳。
- 主链阶段默认串行，卫星技能默认侧挂；不要把 `query / resume` 写成新的主流程阶段，也不要让仅剩用户层入口的辅助命令伪装成正式卫星技能。
- 当用户命令、skill id、workflow command、模板 metadata 同时出现改名需求时，不要逐层碰运气替换；先建立一份根级命名合同，再让其他载体回指这份真源。
- 若某个命令只剩用户命令层入口、已不再对应 tracked workflow 或正式 skill，必须在命名合同与根级路由合同里显式标成“auxiliary command”，不要让它继续挂在卫星技能表里伪装成正式阶段。
- 当共享脚本已能写出治理工件，而阶段合同还没承认这些工件时，优先补根 skill 与命令文档，再补关键阶段 skill，避免脚本能力再次沦为隐形层。
