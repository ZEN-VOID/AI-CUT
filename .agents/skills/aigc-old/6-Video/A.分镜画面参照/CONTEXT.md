# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-Video/A.分镜画面参照` 的经验层知识库，不是过程日志。
- 调用本技能时，应在父级 `6-Video` 合同之后加载本文件。
- 规范真源以同目录 `SKILL.md` 和其动态引用分区为准；本文件只保存可复用经验、修复顺序与启发式。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 融合包只复制旧三段目录说明，没有统一输出根 | 入口合同层 | 回到 `SKILL.md` Output Contract，固定 `A.分镜画面参照/<episode>/` | 每个融合段都必须声明 runtime 子目录 | 三段产物能在同一 episode 根下追溯 |
| prompt/TXT 被脚本直接生成 | LLM 主创层 | 停止脚本主创，改为 LLM 直出 canonical creative truth | `references/prompt-distillation-contract.md` 固定脚本只做投影/校验 | 最终 prompt 有人工/LLM 审美裁决证据 |
| 参照图绑定在 provider handoff 临时拼参数 | 引用治理层 | 回到 `reference-binding/` 先生成可复核三件套 | 在 workflow 中把引用绑定作为 provider 前置 gate | `submit-plan.json` 消费的是已严检请求对象 |
| provider 目录或名称被当作真实执行能力 | provider 槽位层 | 在 `submit-brief.md` 标注 `manual_only` 或外部 skill | `provider-handoff-contract.md` 固定槽位语义 | 下一入口不再虚构自动提交能力 |
| 用户只要局部模式，执行者却跑完整链 | mode 判定层 | 回 `types/type-map.md` 重新锁定 mode | `N1` 必须输出 mode 与 skipped stages | 未执行段不补占位、不伪造产物 |
| 旧三段语义迁入后路径漂移 | 迁移映射层 | 查 `references/source-fusion-map.md` 的 source-to-owner 表 | 新包新增规则先登记来源与 owner | 每个旧核心段都能找到新 owner |
| N1 只锁定 mode 和输出根，没有真正吸收 `首帧参照` 语义 | 融合入口摄入层 | 回 `SKILL.md` Step 1 与 `steps/frame-visual-reference-workflow.md#N1`，补出 `first_frame_digest` | 融合包 intake 必须把源技能的输入门、桥段语义、prompt/TXT 合同、预算策略和三件套形状汇成显式证据 | `N1` evidence 中存在 `first_frame_digest.status=ready` 或明确跳过理由 |

## Repair Playbook

1. 先确认当前请求是 `distill_only`、`bind_references`、`handoff_provider`、`full_chain` 还是 `compat_migration`。
2. 再查 `N1` 是否已经形成 `first_frame_digest`；若只是引用旧 `首帧参照` 路径，先补输入门、桥段语义、prompt/TXT 合同、预算策略和三件套形状。
3. 再查 `3-Detail/<episode>.json` 是否已经稳定到可消费；不稳定时停止，不下游补猜。
4. 若问题在创作性 prompt 或 TXT，优先回 `references/prompt-distillation-contract.md`，不要改脚本凑结果。
5. 若问题在引用字段，回 `references/reference-binding-contract.md`，先区分“无图可跳过”和“歧义必须失败”。
6. 若问题在 provider 计划，回 `references/provider-handoff-contract.md`，先判定 `reference_driven / prompt_only / unresolved`。
7. 修复后按 `review/review-contract.md` 复核三段 gate，并在最终报告中列出非阻断事项；可复用经验再沉淀到 `CONTEXT.md`。

## Reusable Heuristics

- 融合包的价值不是把旧三段文档堆在一起，而是把三段之间最容易跳步的 handoff 变成显式 gate。
- `distill_only` 可以单独完成，但 `handoff_provider` 不应绕过引用状态判定。
- `Assets/` 有图且没有显式 `prompt_only / no_reference` 时，空引用通常是 `unresolved`，不是天然 prompt-only。
- 同一 episode 根下分 `distill / reference-binding / generation-handoff`，比继续复制旧技能树编号更适合回放和审计。
- 当旧包继续存在时，新包的文案必须说清“来源兼容”与“当前真源”，避免执行者同时改两边造成第二真源。
- 融合包的 step 1 必须先把旧 `首帧参照` 消化为可检查的 `first_frame_digest`；只有路径回指、没有语义摘要和 gate 证据，等同于没有完成 intake。
