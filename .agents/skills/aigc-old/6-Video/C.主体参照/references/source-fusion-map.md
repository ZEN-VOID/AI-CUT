# Source Fusion Map

本文件记录用户指定的旧三段技能内容如何进入 `C.主体参照`，防止融合时丢语义或建立第二真源。

## Source Packages

| source_path | source_role | target_owner | operation | semantic_risk |
| --- | --- | --- | --- | --- |
| `1-提示词蒸馏/全能参照/SKILL.md` | 组级视频请求蒸馏入口、LLM 主创、三件套落盘、Field/Pass 表 | `SKILL.md` Step 1 摘要入口；`references/prompt-distillation-contract.md`；`steps/subject-reference-workflow.md#N1-N2`；`review/review-contract.md` | summarize + split | high |
| `1-提示词蒸馏/全能参照/prompt-assembly-spec.md` | 组级设计块、镜级融写句法、TXT 渲染合同、canonical JSON spec | `SKILL.md` Step 1 的 `omni_reference_digest`；`references/prompt-distillation-contract.md`、`references/shared-prompt-principles.md`、`steps/subject-reference-workflow.md#N1-N2`、`templates/request-packet.template.json` | rewrite + preserve core constraints | high |
| `1-提示词蒸馏/全能参照/scripts/generate_episode_packets.py` | episode carrier 兼容入口；旧脚本带 LLM-first 防越权提示 | `scripts/README.md` 作为 legacy helper 指引；本包不把它设为默认主创入口 | reference only | medium |
| `1-提示词蒸馏/全能参照/CONTEXT.md` | 全能参照失败模式、预算、字段覆盖与句法经验 | `CONTEXT.md`、`steps/subject-reference-workflow.md#N1`、`knowledge-base/video-subject-reference-heuristics.md` | summarize | medium |
| `2-参照引用/SKILL.md` | `Assets/` 匹配、引用字段重建、歧义阻断、报告落盘 | `references/subject-reference-binding-contract.md`、`steps/subject-reference-workflow.md#N3-N4`、`review/review-contract.md` | split with subject-oriented specialization | high |
| `2-参照引用/scripts/bind_reference_assets.py` | 机械匹配与校验 helper | `scripts/README.md` 作为 legacy helper 指引；未来可移植为主体参照辅助脚本 | reference only | medium |
| `2-参照引用/CONTEXT.md` | 引用绑定经验 | `CONTEXT.md`、`knowledge-base/video-subject-reference-heuristics.md` | summarize | medium |
| `3-视频生成/SKILL.md` | provider 路由、引用状态判定、submit-plan/brief、provider 槽位语义 | `references/provider-handoff-contract.md`、`steps/subject-reference-workflow.md#N5`、`templates/submit-plan.template.json` | split | high |
| `3-视频生成/CONTEXT.md` | handoff 经验与 prompt-only/unresolved 分流 | `CONTEXT.md`、`knowledge-base/video-subject-reference-heuristics.md` | summarize | medium |

## Subject-Oriented Specialization

- `C.主体参照` 继承 `全能参照` 的组级 prompt/TXT 蒸馏，但把 `主体锚定`、`出场角色及穿搭`、可见道具与场景线索提升为引用绑定前置证据。
- `C.主体参照` 的 `N1` 必须先形成 `omni_reference_digest`，把 `全能参照` 的输入门、`BC` 结构、TXT 渲染、预算策略、三件套形状和主体候选证据桥显式消化后，才允许进入 `N2` 蒸馏或消费旧 `distill/` 产物。
- `C.主体参照` 继承 `2-参照引用` 的严格绑定政策，但优先匹配 `Assets/角色/`、`Assets/服装/`、`Assets/道具/`、`Assets/场景/`，而不是优先匹配故事板或分镜帧。
- `C.主体参照` 继承 `3-视频生成` 的 handoff 包政策，要求 provider 前明确 `reference_driven / prompt_only / unresolved`。

## Non-Removal Rule

- 原三个 source packages 本轮不删除、不移动。
- 本融合包可以回指旧包作为来源证据，但运行时执行本包时，以本包 `SKILL.md` 与分区文件为当前入口真源。
- 后续若要替代旧三段链路，必须另开迁移任务，扫描并同步所有引用。
