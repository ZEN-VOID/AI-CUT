# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-面板设计/角色` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `aigc` 根技能 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 面板 prompt 直接吃整份 Markdown，混入 `物语 / 解构` | prompt 提取层 | 只抽 `**prompt整合**` 段作为 `design_subject` | 在脚本与 `SKILL.md` 固化“prompt整合-only”规则 | `design_subject_source=markdown_prompt_integration` |
| `2-设计` 缺少 Markdown 或 `prompt整合` | 输入回退层 | 从 `character_design.json.roles[]` 合成保守版 `design_subject` | 在 packet 中记录 fallback 来源，避免 silent drift | `design_subject_source=fallback_json_synthesis` |
| 模板被平行改写成第二真源 | 模板治理层 | 固定只读 `templates/角色面板-提示词.json` | 把 layout、critical requirements 与 prompt segments 统一从模板继承 | packet 中 `template_path` 指向同一路径 |
| crowd 角色仍被当成单人 turnaround 处理 | 角色层级策略层 | `role_tier=crowd` 时自动打 `group_portrait=true` | 在类型策略中固化 crowd 群像策略 | manifest 统计到 `group_portrait_count` |
| 父级合同仍把 `3-面板` 写成 pending | 路由状态层 | 同步更新 `2-角色` 与 `4-Design` 父级状态 | 每新增 active leaf 同步回写父级真源与经验层 | 父级合同不再出现 stale pending |
| 主合同改成知行合一后，prompt 来源/类型策略仍留在并列 `references/` | 真源治理层 | 把 prompt 来源判型、role tier 策略、输出合同收回主 `SKILL.md` | 对 `复杂链路的骨架 / 细则分层=false` 的面板技能，只保留迁移 stub，不保留并列 reference 真源 | 当前目录不再出现平行执行真源 |
| 连续批量任务进入 `3-面板` 时，`2-设计` 图像没有自动变成参考图 | SMART bridge 层 | 先把 packet 写稳，再按 `continuous-batch` 扫描 `2-设计` 图像并桥接 `nano-banana/general` | 在 packet 中固化 `image_generation` 字段，并统一走共享 bridge 脚本 | request sidecar 中能看到 continuity refs |
| runner 仍按旧路径 `2-角色/2-设计` 推断输出根，导致当前 canonical runtime 无法执行 | runner 路径推断层 | 将输出根推断切到 `4-Design/角色/2-设计 -> 3-面板`，并保留旧路径兼容 | 以后凡 design/panel runtime 改路径，需同步更新 runner 的默认推断逻辑与 dry-run 校验 | 直接传 `character_design.json` 即可自动落到 `4-Design/角色/3-面板/第N集/` |

## Repair Playbook

1. 先确认 `character_design.json` 是否存在且 `roles[]` 非空。
2. 再确认逐角色 Markdown 是否存在，并优先抽 `prompt整合`。
3. 若 `prompt整合` 缺失，回退到 JSON synthesis，但必须在 packet 中留痕。
4. 再检查模板路径、layout 和 critical requirements 是否完整继承。
5. 最后检查 packet 命名、episode 路径和 `_manifest.json` 是否一致。

## Reusable Heuristics

- 角色面板最稳的 prompt 源不是整份设计卡，而是 `prompt整合` 这个已经被 `2-设计` 压好的下游消费段。
- panel 阶段最怕的不是“文案不华丽”，而是把设计事实、layout 规则和出图执行混成一层；因此本阶段只做 packet，停在写回。
- 如果上游设计稿还不完整，宁可保守 fallback 到 JSON synthesis，也不要把 `物语 / 解构` 之类分析段直接灌给下游。
- crowd 角色的 panel 更像“同一阶层群像设计板”，不是单人 front/side/back 转身图。
- 当用户显式要求知行合一且 `复杂链路的骨架 / 细则分层=false` 时，`3-面板` 的 prompt 来源策略、群像策略、reference image 规则和 output contract 都应回收到主 `SKILL.md`，不再让 `references/` 承载并列步骤真源。
- 若角色面板要自动生图，最稳的做法不是在 bridge 层再拼 prompt，而是直接复用 packet 的 `prompt_payload.prompt_text`，并把 `2-设计` 图像通过 SMART continuity refs 自动并入。
- 只要 runner 负责“默认推断输出根”，它就必须兼容当前 canonical runtime；否则 dry-run 成功率会先于业务逻辑崩掉。
