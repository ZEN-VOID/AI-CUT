# Context: C.主体参照

本文件是 `6-Video/C.主体参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `6-Video` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 融合包只复制旧三段目录说明，没有统一输出根 | 入口合同层 | 回到 `SKILL.md` Output Contract，固定 `C.主体参照/<episode>/` | 每个融合段都必须声明 runtime 子目录 | 三段产物能在同一 episode 根下追溯 |
| 组级 prompt/TXT 被脚本直接生成 | LLM 主创层 | 停止脚本主创，改为 LLM 直出 canonical creative truth | `references/prompt-distillation-contract.md` 固定脚本只做投影/校验 | 最终 prompt 有人工/LLM 审美裁决证据 |
| 主体识别把故事板、单帧或风格词当作主体资产 | 主体类别层 | 回到主体识别表，按角色/服装/道具/场景重新归类 | `subject-reference-binding-contract.md` 固定主体类别与禁区 | subject-index 不混入非主体第一参照 |
| 主体索引无法回链到 `3-Detail` 镜头或主体锚定 | 证据回链层 | 重建 `source_shot_ids` 与来源字段 | 在 `N3` 固化主体必须带来源镜头、来源字段和置信等级 | subject-report 可逐项复核 |
| 同一主体 token 命中多个资产却被默选 | 歧义裁决层 | 停止绑定并报告 ambiguous | 主体绑定合同固定同分候选硬失败 | subject-match-report 清楚列出候选 |
| 已有主体 Assets，handoff 却被当作 prompt-only | 引用模式层 | 回到 `reference-binding/` 完成主体资产绑定 | provider handoff 前固定 `reference_driven / prompt_only / unresolved` 判定 | submit-plan 不把未解析引用偷换成 prompt-only |
| 用户只要局部模式，执行者却跑完整链 | mode 判定层 | 回 `types/type-map.md` 重新锁定 mode | `N1` 必须输出 mode 与 skipped stages | 未执行段不补占位、不伪造产物 |
| 旧三段语义迁入后路径漂移 | 迁移映射层 | 查 `references/source-fusion-map.md` 的 source-to-owner 表 | 新包新增规则先登记来源与 owner | 每个旧核心段都能找到新 owner |
| N1 只锁定 mode 和输出根，没有真正吸收 `全能参照` 配置 | 融合入口摄入层 | 回 `SKILL.md` Step 1 与 `steps/subject-reference-workflow.md#N1`，补出 `omni_reference_digest` | 融合包 intake 必须把源技能输入门、BC 结构、TXT 主稿、预算策略、主体证据桥和三件套形状汇成显式证据 | `N1` evidence 中存在 `omni_reference_digest.status=ready` 或明确跳过理由 |

## Repair Playbook

1. 先确认当前请求是 `distill_only`、`identify_subjects`、`bind_subject_references`、`handoff_provider`、`full_chain` 还是 `compat_migration`。
2. 再查 `N1` 是否已经形成 `omni_reference_digest`；若只是引用旧 `全能参照` 路径，先补输入门、BC 结构、TXT 主稿、预算策略、主体证据桥和三件套形状。
3. 再查 `3-Detail/<episode>.json` 是否已经稳定到可消费；不稳定时停止，不下游补猜。
4. 若问题在创作性 prompt 或 TXT，优先回 `references/prompt-distillation-contract.md`，不要改脚本凑结果。
5. 若问题在主体识别，回 `references/subject-reference-binding-contract.md`，先确认主体类别、来源镜头和主体优先级。
6. 若问题在引用字段，仍回 `references/subject-reference-binding-contract.md`，区分“无图可跳过”和“歧义必须失败”。
7. 若问题在 provider 计划，回 `references/provider-handoff-contract.md`，先判定 `reference_driven / prompt_only / unresolved`。
8. 修复后按 `review/review-contract.md` 复核三段 gate，并把非阻断事项写入 `TODO.md`。

## Reusable Heuristics

- 主体参照融合包的价值不是把旧三段文档堆在一起，而是把“全能参照 -> 主体识别和绑定 -> 生成 handoff”之间最容易跳步的 handoff 变成显式 gate。
- `subject-index.json` 是主体识别证据层，不是新的剧情真源；它只能回链 `3-Detail`、项目资产和请求对象。
- 对主体参照来说，角色与服装通常是第一锚点，道具和场景是第二锚点，故事板/单帧画板只能作为辅助视觉连续性，不应冒充主体资产。
- 当 `Assets/角色/` 或 `Assets/服装/` 已有明确命中且没有显式 `prompt_only / no_reference`，空引用通常是 `unresolved`，不是天然 prompt-only。
- 同一 episode 根下分 `distill / reference-binding / generation-handoff`，比继续复制旧技能树编号更适合回放和审计。
- 当旧包继续存在时，新包的文案必须说清“来源兼容”与“当前真源”，避免执行者同时改两边造成第二真源。
- 融合包的 step 1 必须先把旧 `全能参照` 消化为可检查的 `omni_reference_digest`；只有路径回指、没有配置摘要和 gate 证据，等同于没有完成 intake。
