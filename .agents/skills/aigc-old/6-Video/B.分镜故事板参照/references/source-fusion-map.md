# Source Fusion Map

本文件记录用户指定的旧三段技能内容如何进入 `B.分镜故事板参照`，防止融合时丢语义或建立第二真源。

## Source-To-Owner Matrix

| source_path | source_content | target_owner | operation | semantic_risk |
| --- | --- | --- | --- | --- |
| `1-提示词蒸馏/全能参照/SKILL.md` | 分镜组视频请求蒸馏入口、LLM 主创、三件套落盘、Field/Pass 表、输入完整性门与加载顺序 | `SKILL.md` 摘要入口；`steps/storyboard-reference-workflow.md#N1` 配置画像；`references/prompt-distillation-contract.md`；`steps/storyboard-reference-workflow.md#N2`；`review/review-contract.md` | summarize + split | high |
| `1-提示词蒸馏/全能参照/prompt-assembly-spec.md` | 组级设计块、镜级融写句法、TXT 渲染合同、canonical JSON spec、预算层级、对白句槽与引用骨架 | `steps/storyboard-reference-workflow.md#N1` 配置画像；`references/prompt-distillation-contract.md`、`references/shared-prompt-principles.md`、`templates/request-packet.template.json` | rewrite + preserve core constraints | high |
| `1-提示词蒸馏/全能参照/scripts/generate_episode_packets.py` | episode carrier 与 legacy 兼容入口；旧脚本带 LLM-first 防越权提示 | `scripts/README.md` 作为 legacy helper 指引；本包不把它设为默认主创入口 | reference only | medium |
| `1-提示词蒸馏/全能参照/CONTEXT.md` | 组级蒸馏失败模式、预算、字段覆盖、runtime drift 经验与脚本越权风险 | `steps/storyboard-reference-workflow.md#N1` 配置画像；`CONTEXT.md`、`knowledge-base/video-reference-heuristics.md` | summarize | medium |
| `2-参照引用/SKILL.md` | `Assets/` 到 `reference_images / image_markers` 的绑定规则 | `references/reference-binding-contract.md`、`steps/storyboard-reference-workflow.md#N3` | summarize + specialize | high |
| `2-参照引用/scripts/bind_reference_assets.py` | group_id / shot_id / 角色 / 服装候选匹配与严格校验 | `scripts/README.md` 作为机械辅助入口；本包不直接复制脚本 | reference only | medium |
| `3-视频生成/SKILL.md` | provider 路由、引用模式判定、submit-plan/brief | `references/provider-handoff-contract.md`、`steps/storyboard-reference-workflow.md#N4`、`templates/submit-plan.template.json` | summarize + specialize | high |

## Non-Removal Rule

- 原 `1-提示词蒸馏/全能参照`、`2-参照引用`、`3-视频生成` 技能包暂不移除。
- 新包拥有 `B.分镜故事板参照` 的融合入口、runtime 输出根和三段 gate；旧包继续作为兼容入口与语义来源。
- 若后续需要把旧包迁为 deprecated，必须另开任务并执行全仓引用扫描。
