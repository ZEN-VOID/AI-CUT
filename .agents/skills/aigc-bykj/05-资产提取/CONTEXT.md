# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/05-资产提取` 父级导引 skill 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写父级路由、子技能真源边界或输出路径；只记录资产提取阶段的路由经验、失败模式和修复顺序。

## Context Health

- soft_limit_chars: 10000
- hard_limit_chars: 20000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 父级直接生成资产正文 | 路由边界层 | 回到命中的子技能 `SKILL.md + CONTEXT.md` | 父级固定为 `governance_tier: router` | 父级只输出路由、汇总和 handoff |
| 从小说源或旧 runtime 提取资产 | 上游真源层 | 移回 `output/[项目名]/02-剧本处理/` | 父级和子技能都固定 `02` 为默认输入 | 报告中有 `upstream_lock` |
| 角色、场景、道具混成一张无边界表 | 资产类型边界层 | 分别路由到三个子技能，再做索引汇总 | 父级只做汇流，不重写子技能字段 | 子输出目录独立存在 |
| 道具清单膨胀成所有物件列表 | 道具筛选层 | 交回 `道具提取` 的叙事功能门 | 道具子技能固定 `narrative_function_score` | 主清单只含关键叙事功能道具 |
| 提取后缺设计规格 | 提取/设计汇流层 | 回到对应子技能的 design spec 节点 | 子技能固定 `design_spec` 为主条目必填 | JSON 主条目包含模板子段镜像设计规格 |
| 输出仍停留在 Markdown 清单 | 输出格式层 | 改为 JSON canonical 输出，Markdown 只作为派生视图 | 父级和子技能输出合同固定 `.json` | manifest 指向 JSON 文件 |

## Repair Playbook

1. 先判断用户要完整资产提取，还是只提取角色、场景或道具。
2. 若输入不是 `02-剧本处理` 输出，先建立上游锁定或报告缺口。
3. 子技能缺失或未初始化时，先补齐对应 `SKILL.md + CONTEXT.md`。
4. 完整资产提取按 `角色 -> 场景 -> 道具` 串行执行，每个子技能都完成提取与设计规格，再做 JSON 索引汇总。
5. 若跨资产字段冲突，优先修对应子技能结果，不在父级手工覆盖。

## Reusable Heuristics

- 资产提取阶段现在采用“提取 + 设计规格 JSON”一体化输出；设计规格应镜像 AIGC 7-设计对应模板子段，但不产出图片，也不默认写回 AIGC 7-设计 Markdown runtime。
- 角色提取的核心风险是同一角色多名并存；场景提取的核心风险是改写场景标题；道具提取的核心风险是把所有物件都纳入。
- 父级汇总越轻，子技能越稳定；父级只做索引、状态和交接，不应成为第四份资产正文。
