# Context: B.分镜故事板参照

本文件是 `6-Video/B.分镜故事板参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `6-Video` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 融合包只复制旧三段目录说明，没有统一输出根 | 入口合同层 | 回到 `SKILL.md` Output Contract，固定 `B.分镜故事板参照/<episode>/` | 每个融合段都必须声明 runtime 子目录 | 三段产物能在同一 episode 根下追溯 |
| 组级 prompt/TXT 被脚本直接生成 | LLM 主创层 | 停止脚本主创，改为 LLM 直出 canonical creative truth | `references/prompt-distillation-contract.md` 固定脚本只做投影/校验 | 最终 prompt 有人工/LLM 审美裁决证据 |
| 分镜组视频请求漏掉组内某个镜头 | 组级覆盖层 | 回到 `全能参照` 覆盖门，逐镜补齐剧情桥段与镜头控制 | `N2` 固定 `source_shot_ids` 与组内镜头数审计 | manifest 能回链全部镜头 |
| 故事板引用在 provider handoff 临时拼参数 | 引用治理层 | 回到 `reference-binding/` 先生成可复核三件套 | workflow 中把引用绑定作为 provider 前置 gate | `submit-plan.json` 消费的是已严检请求对象 |
| group_id 命中多个故事板候选却被默选 | 歧义裁决层 | 停止绑定并报告 ambiguous | `reference-binding-contract.md` 固定同分候选硬失败 | match-report 清楚列出候选 |
| 用户只要局部模式，执行者却跑完整链 | mode 判定层 | 回 `types/type-map.md` 重新锁定 mode | `N1` 必须输出 mode 与 skipped stages | 未执行段不补占位、不伪造产物 |
| `N1` 只锁定路径和 mode，没有消化旧 `全能参照` 配置 | 配置画像层 | 回 `steps/storyboard-reference-workflow.md#N1` 生成 `omni_config_profile` | 凡进入 `N2` 或判定旧请求来源，都先吸收 `全能参照/SKILL.md + CONTEXT.md`、`prompt-assembly-spec.md` 与共享图生视频原则 | `omni_config_profile` 能解释 BC 结构、TXT 模板、压缩优先级、字段标题禁令、对白槽、引用骨架和脚本边界 |
| 旧三段语义迁入后路径漂移 | 迁移映射层 | 查 `references/source-fusion-map.md` 的 source-to-owner 表 | 新包新增规则先登记来源与 owner | 每个旧核心段都能找到新 owner |

## Repair Playbook

1. 先确认当前请求是 `distill_only`、`bind_references`、`handoff_provider`、`full_chain` 还是 `compat_migration`。
2. 再查 `3-Detail/<episode>.json` 是否已经稳定到可消费；不稳定时停止，不下游补猜。
3. 若问题在创作性 prompt 或 TXT，优先回 `references/prompt-distillation-contract.md`，不要改脚本凑结果。
4. 若问题在引用字段，回 `references/reference-binding-contract.md`，先区分“无图可跳过”和“歧义必须失败”。
5. 若问题在 provider 计划，回 `references/provider-handoff-contract.md`，先判定 `reference_driven / prompt_only / unresolved`。
6. 修复后按 `review/review-contract.md` 复核三段 gate，并在最终报告中列出非阻断事项；可复用经验再沉淀到 `CONTEXT.md`。

## Reusable Heuristics

- 组级融合包的价值不是把旧三段文档堆在一起，而是把“全能参照 -> 故事板绑定 -> 生成 handoff”之间最容易跳步的 handoff 变成显式 gate。
- `distill_only` 可以单独完成，但 `handoff_provider` 不应绕过引用状态判定。
- `Assets/分镜画板/分镜故事板/` 与 `Assets/分镜画板/漫画/` 有图且没有显式 `prompt_only / no_reference` 时，空引用通常是 `unresolved`，不是天然 prompt-only。
- 同一 episode 根下分 `distill / reference-binding / generation-handoff`，比继续复制旧技能树编号更适合回放和审计。
- 当旧包继续存在时，新包的文案必须说清“来源兼容”与“当前真源”，避免执行者同时改两边造成第二真源。
- `B.分镜故事板参照` 的第一步若只做“项目/集号/group_id/mode”锁定，会让后续 N2 重新凭印象理解旧 `全能参照`；更稳的是先把旧配置压成 `omni_config_profile`，再让 prompt/TXT、引用骨架和 review 共用同一执行画像。
