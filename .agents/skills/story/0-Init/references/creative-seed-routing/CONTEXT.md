# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `references/creative-seed-routing/`，用于沉淀创意路由的局部经验，而不是记录执行流水。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 跨模块经验与根技能路由经验应回写到 `0-Init/CONTEXT.md`，不要长期滞留在本地经验层。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 父 `SKILL.md` 或 planning 固定题包直答 sidecar 仍直接点名内部 leaf references | module routing contract | 改为只指向 `references/creative-seed-routing/module-spec.md` | 把创意相关 leaf reference 映射固定只保留在本模块 | 全仓检索不再出现活跃 `references/creativity/` 或上层入口直连 leaf docs |
| 创意缺口一出现就把整个目录全读 | route classification | 先回到 `Phase 1` 判断真实缺口，再缩到最小读取清单 | 在模块合同里把“4 份以上 leaf references = 过载信号”写成返工门禁 | `loaded_leaf_references` 数量与当前缺口相称 |
| 反套路包选错题材映射 | anti-trope mapping | 用题材映射表重选 `anti-trope-*.md` | 把 genre -> anti-trope 映射固化在模块规范里，由父技能不再重复维护 | `planning_seed.anti_trope` 与题材走廊一致 |
| 趋势资料被当成默认参考 | trend gate | 仅在用户显式要求时读取 `market-trends-2026.md` 并配合联网校验 | 把趋势资料保持为 L3 双闸门：显式请求 + WebSearch/WebFetch | 没有显式请求时，任务日志不出现趋势校准读取 |
| 创意参考结果停留在说明墙，没有回写结构化槽位 | slot landing contract | 将结果压缩进 `creative_mandate / planning_seed / unknowns` | 在模块中固定“非内容输出型”交付与 Phase 3 槽位回写 | 初始化 handoff 只看到结构化字段，不看到参考资料堆砌 |
| 模块写了三轴三重，但没有事实/推断分层、增强验证和落盘矩阵，看起来像用了 `think-think`，实际还没真正执行完 | think-think execution contract | 按 `chain-optimization` 补齐事实/推断表、保留/修正/重建矩阵、验证矩阵、分重落盘映射与正式报告 | 对任何被 `think-think` 强化的模块，强制满足“显式矩阵 + reports/ 正式报告”双门禁 | 仓库中可同时看到强化后的模块矩阵和 `reports/思维链设计报告-*.md` |

## Repair Playbook

1. 先确认问题是“路由入口散点化”还是“当前回合读太多”。
2. 若是入口散点化，优先改父 `SKILL.md` 与 planning 固定题包直答 入口，不先碰 leaf docs。
3. 若是读取过重，先把缺口压回 `约束包 / 卖点 / 商业定位 / 复合题材 / 灵感救援 / 反套路 / 趋势校准` 七类之一。
4. 若是输出像资料墙，直接回到 `Phase 3`，只保留写回槽位和 provenance。
5. 若涉及当下平台风向，先确认用户是否显式要求，再决定是否开趋势闸门。

## Reusable Heuristics

- 对初始化来说，创意 references 的价值不在“文档多”，而在“能不能只读最小一组就补齐 `planning_seed` 的阻塞缺口”。
- 当同一组创意 leaf docs 被父技能与 planning 固定题包直答 共享时，最稳的治理方式不是复制触发规则，而是建立一个统一路由模块。
- 反套路包是题材映射问题，不是 team 编组问题；把它绑在上层 team 路由里会越改越乱。
- 趋势资料天然比其他 leaf docs 更不稳定，因此必须永远保持 L3 受控入口。
- `think-think` 真正执行到位的标志，不是“模块里出现了三轴三重标题”，而是能看到事实/推断分层、增强验证、落盘矩阵和正式设计报告同时成立。
