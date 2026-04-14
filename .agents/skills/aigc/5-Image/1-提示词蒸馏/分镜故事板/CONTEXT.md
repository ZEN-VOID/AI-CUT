# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在根 `.agents/skills/aigc/SKILL.md` 与父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 之后加载本文件。
- 当前仓没有独立的 `.agents/skills/aigc/5-Image/SKILL.md` 阶段根合同；若再次出现该旧回链，应视为源层漂移。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把图片落盘当主产物 | 输出合同层 | 回退到 `第N集.json` 图像请求集合 | 在 `SKILL.md` 固化“json 为主，生成后置” | 主产物指向 `第N集.json` |
| prompt 没有固定英文前缀 | Prompt 合同层 | 重新按固定前缀 + `storyboard_group` 拼接 | 在 `N4` 与 `FIELD-SB-SHEET-02` 固化前缀逐字保留与拼接顺序 | prompt 开头逐字一致 |
| `storyboard_group` 漏掉组级或镜级内容 | 输入覆盖层 | 回到 director schema 重新提取分镜组内容 | 在 `N3` 固化字段覆盖检查 | prompt 可回链 `剧本正文 + 组间设计 + 分镜明细[]` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 在 `.agents/skills/aigc/5-Image/_shared` 固定共享 JSON 模板 | `model` 骨架与共享模板一致 |
| 规范又被拆回 `references` 或其他副本 | 真源治理层 | 回收规范到当前 `SKILL.md` | 固化“单文件真源 + `复杂链路的骨架 / 细则分层: false`” | 目录下不再存在第二套规范载体 |
| 节点只有动作没有路由与门禁 | 思行网络层 | 给对应节点补 `route_out / gate` | 在 `Thinking-Action Node Contract` 强制六槽位 | 每个关键节点都可回退或汇流 |
| 仍引用不存在的 `5-Image/SKILL.md` | 上游回链层 | 改回根 `aigc` + 父级 `1-提示词蒸馏` 加载顺序 | 在 `Total Input Contract` 固化真实加载链 | 本包内不再出现旧路径引用 |

## Repair Playbook

1. 先查 `N0` 是否锁定了“组级 storyboard 请求 JSON 蒸馏”而不是其他对象。
2. 再查 `N1` 的 shared schema 与 `分镜组列表[]` 是否成立。
3. 再查 `N2` 的 `group_id + source_shot_ids` 是否唯一且有序。
4. 再查 `N3` 是否已经覆盖 `剧本正文 + 组间设计 + 分镜明细[]`。
5. 再查 `N4` 是否严格等于“固定英文前缀 + storyboard_group”。
6. 再查 `N5` 是否仍以共享模板骨架承接，并确认 `reference_images / image_markers` 没被删。
7. 最后查 `N6` 是否正确落 `第N集.json`，以及 `full_trace` 时 `_manifest.json` 是否与之互相追溯。

## Reusable Heuristics

- `分镜故事板` 的消费单位始终是“组”，不是“帧”。
- 对这个叶子技能而言，复杂度主要来自节点门禁与汇流，而不是多角色协作；优先用单技能知行网络，不要过早升格为 subagents。
- 上游进入 `分镜故事板` 时，优先把 `projects/aigc/<项目名>/3-Detail/第N集.json` 视为第一事实源；`3-Detail/evidence/` 只作为人工可读证据。
- 当 `复杂链路的骨架 / 细则分层` 固定为 `false` 时，复杂节点细则必须直接留在 `SKILL.md`，不能再借 `references/` 旁路外包。
- 对本技能来说，最常见漂移不是画风，而是把“图像请求 JSON 蒸馏”误做成“直接图片落盘”或“只写线性步骤不写汇流门”。
- 最稳的节点主干是：`组边界 -> storyboard_group -> 固定前缀 -> 模板骨架 -> 落盘汇流`。
- `思考过程` 应留在调用侧摘要或 `full_trace` 侧车，不要写进 canonical JSON 业务真源。
