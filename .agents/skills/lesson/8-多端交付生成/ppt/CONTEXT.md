# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `lesson/8-多端交付生成/ppt` 的经验层知识库，不是第二份 PPT 交付合同。
- 调用 `.agents/skills/lesson/8-多端交付生成/ppt/SKILL.md` 时，必须同时加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > 父包 `SKILL.md` > 本叶子 `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- recommended_action: keep-ppt-delivery-heuristics

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| PPT 叶子重新决定三端交付范围 | parent packet 缺失 | 回到父包生成 ppt leaf packet | PPT 叶子只消费父包 packet | `packet_inventory` 指向父包 manifest |
| slide bullets 像模板套句 | LLM-first 违规 | 废弃机械产物，回到 `N4-LLM-SLIDE-ADAPTATION` | 脚本只做 PPTX 组装和导出 | authorship note 可追踪 |
| deck 只有页数没有教学节奏 | architecture 缺口 | 回到 `N3-SLIDE-ARCHITECTURE` 补结构、活动和备注 | deck 结构先于组装 manifest | plan 包含 slide groups |
| PPTX 组装覆盖了未授权 slides | update scope 漂移 | 只改受影响 slides 并更新 manifest diff | 正式写回前记录 overwrite note | changed slides 和 manifest 一致 |
| PPT 与 DOC/HTML 术语不一致 | cross-channel consistency 缺口 | 回到父包 delivery map 或本叶子 gate | 术语和目标以父包 map 为真源 | consistency section 无冲突 |

## Repair Playbook

1. 先确认任务确实是 PPT、PowerPoint、slides、授课演示或讲者备注交付。
2. 缺父包 packet 时回到 `$lesson-delivery`，不要在 PPT 叶子补父包 manifest。
3. 页数、授课时长和场景不清时先定 deck variant。
4. 所有 `.pptx` 组装都必须从 LLM-approved slide plan 和 manifest 出发。
5. 修订既有 PPT 时只改受影响 slides，并同步 `ppt-assembly-manifest.json`。

## Reusable Heuristics

- PPT 的优势是授课节奏和视觉提示，不应复制 DOC 的长段落。
- 每个 slide group 应有教学目标、讲者备注和互动/停顿提示。
- 版式、导出、动效和备注写入属于机械组装，不属于 PPT 文案主创。
- 缺视觉素材时应保守列缺口或占位说明，不臆造版权状态。
- 如果 PPT 与父包 map 冲突，优先修 PPT 叶子，不改父包事实。

## Case Log

### Case-001

- milestone_type: ppt_leaf_creation
- outcome: 建立 PPT/PowerPoint 交付叶子的 Skill 2.0 runtime spine。
- design_decision: PPT 叶子拥有 deck 结构、slide plan、speaker notes、assembly manifest 和可选 PPTX 组装目标。
- replication_checklist: 父包 packet -> slide architecture -> LLM slide 适配 -> assembly manifest -> consistency gate。
- evidence_paths: `.agents/skills/lesson/8-多端交付生成/ppt/SKILL.md`
