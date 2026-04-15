# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-Image/1-提示词蒸馏/分镜帧` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在阶段父级 `.agents/skills/aigc/5-Image/SKILL.md + CONTEXT.md` 与父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md` 之后加载本文件。
- 当前知识沉淀已与 `skill-知行合一` 对齐：优先记录节点边界、回退入口、汇流门和可复用 heuristics，而不是记录一次性过程描述。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-04-12T21:20:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `分镜ID` 仍是局部编号 | ID 归一层 | 重新归一为四段式 canonical ID | 在 `SKILL.md` 输入合同中固化四段式要求 | 单帧条目可全局回链 |
| 下游仍按旧 detail markdown sidecar 读取上游 | 输入真源层 | 切换到 `projects/aigc/<项目名>/3-Detail/第N集.json` 并按 shared schema 锁定目标分镜 | 在 `SKILL.md` 固化 `final_output.main_content.分镜组列表[].分镜明细[]` 取数路径 | 单帧条目能回链 shared director schema |
| `single_frame_shot` 混入整组剧情或大段对白 | 内容归纳层 | 收缩到当前目标分镜与其必要组级上下文 | 把 `single_frame_shot` 定义为单帧内容块，而非整组剧情摘要 | 内容块不再复述整段台词 |
| prompt 没有固定单帧前缀 | Prompt 合同层 | 重新按固定前缀 + `single_frame_shot` 拼接 | 在 `SKILL.md` 固化前缀逐字保留 | prompt 开头逐字一致 |
| 仍把图片落盘当主产物 | 输出契约层 | 回退到 `第N集.json` 单帧图像请求集合 | 将 JSON 视为必要 completeness carrier | 主产物指向 `第N集.json` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `5-Image/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |
| 叶子 skill 规范被切碎到多个 `references/*.md` | 真源治理层 | 把思维链、workflow、VSM、输出契约回收到单一 `SKILL.md` | 将 `SKILL.md` 设为叶子技能唯一规范真源，`CONTEXT.md` 只保留经验层 | 不再需要依赖 `references/` 才能完整执行 |
| 步骤不少，但每一步没有 `route_out` 或回退入口 | 节点合同层 | 把线性步骤改写为知行合一思行节点 | 在 `SKILL.md` 固化 `Topology + Node Network + Convergence` 三联合同 | 出错时能准确回到具体节点 |
| 汇流前已经写回，导致 JSON 和 manifest 口径漂移 | 汇流审计层 | 在落盘前增加统一审计门，先判 `json_only/full_trace` 再写回 | 将 `N7-CONVERGENCE-AUDIT` 固化为写回前硬门槛 | 输出模式与落盘文件保持一致 |
| `3-Detail` phase 未就绪却直接锁镜 | 阶段就绪层 | 在 `N1` 输入门先查 `metadata.document_phase` | 在 `SKILL.md` 固化 `detail_in_progress | ready` 才允许进入 `N2` | 不再从未完成 detail 根文件取镜 |
| 单帧上下文漏掉 `出场角色及穿搭` 或镜级 canonical 字段 | 上下文打包层 | 回到 `N3` 补齐组级穿搭与 `角色背景面 / 角色站位走位 / 道具及状态 / 分镜表现` | 在 `SKILL.md` 固化 frame context pack 最低覆盖面 | `single_frame_shot` 不再只有抽象镜头描述 |

## Repair Playbook

1. 先查 `metadata.document_phase` 是否已到 `detail_in_progress | ready`，再锁唯一 `分镜ID`。
2. 再检查 `single_frame_shot` 是否只服务当前目标分镜与其必要组级上下文。
3. 再检查 `prompt` 是否严格等于“固定单帧前缀 + single_frame_shot”。
4. 再确认共享模板骨架是否完整，尤其是 `reference_images / image_markers`。
5. 最后确认 JSON 是否为主产物，manifest 是否按需成立。
6. 若步骤无法说明“为什么能继续往下走”，优先修 `Topology / Node Network / Convergence Contract`，而不是继续堆补文字说明。

## Reusable Heuristics

- 单帧技能最容易漂移的不是画风，而是“对象边界”。
- 先锁 ID，再写 `single_frame_shot`，否则所有单帧内容块都会失真。
- 当上游导演真源已切到 `director_episode_output.schema.json` 后，`分镜帧` 必须先从 `final_output.main_content.分镜组列表[].分镜明细[]` 取镜，再做本地单帧投影。
- 对单帧技能来说，JSON / manifest 比图片更能证明这张图到底对应哪一镜。
- 当固定前缀已经定义“单帧、无多格、无文字覆盖”的页面约束时，最稳的做法是不再并行维护第二套私有 prompt 模板。
- 对这种边界稳定、字段数有限的叶子技能，`思行节点 + 汇流门 + 一次性输出` 通常比“长 checklist + 多张表”更抗漂移。
- 若一个节点不能同时回答“我处理了什么事实”和“我为什么可以流向下一步”，它通常还不是合格的叶子思行节点。
- 单帧 prompt 若不显式承接 `出场角色及穿搭` 与 `分镜表现`，通常会丢失服装锚点和镜头抓手，后续一致性也更容易漂移。
