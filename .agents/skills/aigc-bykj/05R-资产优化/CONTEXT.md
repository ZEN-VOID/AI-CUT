# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/05R-资产优化` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 05R 被当成重新提取 | 阶段边界层 | 回到 `05` 源稿锁定，只做 patch 或优化版 JSON | `Source Continuity Contract` 固定 05R 只承接 05 输出 | manifest 回指 `05-资产提取` |
| 用户自然语言被直接写成 prompt | 意图解析层 | 先补 `asset_intent_map`，再改字段 | `N2A-INTENT-PARSE` 固定为前置节点 | 每条反馈有 asset type、field、risk |
| 角色误合并 | 证据判断层 | 恢复分离，添加 `possible_alias_of` 或冲突说明 | 合并必须同时满足姓名/身份/关系/出场证据 | patch 记录合并依据 |
| 场景标题被改写成新地点 | 上游保真层 | 恢复剧本原标题，只优化空间设计和 prompt | 场景标题默认来自 `02`/`05` 真源 | scenes JSON 保留 `source_scene_title` |
| 道具去噪误删关键物 | 叙事功能层 | 将删除改为降级，补功能评分和证据 | 先降级后删除，关键物需人工证据复核 | `narrative_function_score` 有理由 |
| design_spec 退化为摘要 | 模板对齐层 | 回到 05 子技能模板子段，补齐缺项 | `PASS-05R-07` 阻断模板子段缺失 | `template_slot_check` pass |
| prompt 漂移到无证据设定 | 提示词约束层 | 删除无证据词，回指 `design_spec` 与固定画面约束 | prompt 修复必须绑定 evidence chain | `prompt_constraint_review` pass |
| patch 合法但 full JSON 不一致 | 汇流层 | 重新从 patch 投影优化 JSON，复核 index | 写回前做 cross asset alignment | optimized index 引用全可解析 |
| 用户偏好被写入长期记忆 | 记忆边界层 | 回收为本轮优化报告字段 | 未明确“记住”不写项目 `MEMORY.md` | 项目记忆无未授权变更 |
| 需要重提取却在 05R 伪造结果 | 路由层 | 输出 `handoff_to_05`，停止写优化终稿 | 新主体、新证据、新剧情事实回到 05/02R | report 标记 blocked/handoff |

## Repair Playbook

1. 先判断问题属于源稿锁定、自然语言意图、范围授权、证据政策、角色合并、场景标题、道具筛选、模板子段、prompt 约束、跨资产引用还是写回。
2. 若源稿缺失，先修 `N1-SOURCE-LOCK`；不要用用户记忆或上游剧本直接生成 05R。
3. 若用户只说“整理一下”“更好一点”，先做 `asset_intent_map` 和澄清门；不要直接大改资产表。
4. 若角色合并不稳，宁可保留两个资产并加 `possible_alias_of`，不要硬合并。
5. 若道具过多，先按叙事功能、证据强度、复现频率和因果作用排序；普通环境物降级，不直接删除边界物。
6. 若场景问题来自剧本标题本身，输出回到 `02R` 或 `05` 的 handoff，不在 `05R` 改写标题事实。
7. 若 `design_spec` 字段缺失，优先修模板子段，不顺手重写资产身份和剧情事实。
8. 若 prompt 不稳，先约束主体完整性、背景、镜头、负面词，再增加风格词；不要堆空泛质量词。
9. 若跨资产引用断裂，优先修 ID 和引用表，再调整单个资产内容。
10. 若输出要给下游直接使用，优先同时提供 patch 和 full optimized JSON；只审查任务只输出报告。

## Reusable Heuristics

- `05R` 的价值在于把用户反馈变成可审查的资产 patch，而不是再做一次更漂亮的资产提取。
- 角色合并要保守；“同名”“相似称呼”不足以合并，必须有身份、关系、行为或上下文证据。
- 场景优化的主线是可生成性：空间层级、材质、光线、无人物约束、镜头语言，而不是改剧情地点。
- 道具优化的主线是叙事功能：证据、信物、武器、设备、转折物优先；纯装饰和一次性环境物默认降级。
- `design_spec` 的模板子段是下游稳定性的硬约束；05R 不应把它压缩成“外观+prompt”。
- prompt 修复必须由设计字段推导；没有设计证据的英文词越多，越容易让下游漂移。
- Patch-first 能保留可追溯性；full optimized JSON 只在需要直接交付下游时投影生成。
- 多轮优化要保留 rollback note，否则用户无法表达“保留这部分，撤销那部分”。
