# Source Fusion Map

本文件记录用户指定的旧三段技能内容如何进入 `A.分镜画面参照`，防止融合时丢语义或建立第二真源。

## Source Packages

| source_path | source_role | target_owner | operation | semantic_risk |
| --- | --- | --- | --- | --- |
| `1-提示词蒸馏/首帧参照/SKILL.md` | 单镜首帧视频请求蒸馏入口、输入门、桥段裁切、LLM 主创、三件套落盘、Field/Pass 表 | `SKILL.md` Step 1 与 Field/Pass；`references/prompt-distillation-contract.md`；`steps/frame-visual-reference-workflow.md#N1` 的 `first_frame_digest`；`steps/frame-visual-reference-workflow.md#N2`；`review/review-contract.md` | summarize + split | high |
| `1-提示词蒸馏/首帧参照/prompt-assembly-spec.md` | 组级设计块、单镜融写句法、TXT 渲染合同、canonical JSON spec | `references/prompt-distillation-contract.md`、`references/shared-prompt-principles.md`、`templates/request-packet.template.json` | rewrite + preserve core constraints | high |
| `1-提示词蒸馏/首帧参照/scripts/generate_episode_packets.py` | episode carrier 与 `--shot-id` 兼容入口；旧脚本带 LLM-first 防越权提示 | `scripts/README.md` 作为 legacy helper 指引；本包不把它设为默认主创入口 | reference only | medium |
| `1-提示词蒸馏/首帧参照/CONTEXT.md` | 首帧蒸馏失败模式、桥段提取、预算与字段覆盖经验 | `CONTEXT.md`、`knowledge-base/video-reference-heuristics.md` | summarize | medium |
| `2-参照引用/SKILL.md` | `Assets/` 匹配、引用字段重建、歧义阻断、报告落盘 | `references/reference-binding-contract.md`、`steps/frame-visual-reference-workflow.md#N3`、`review/review-contract.md` | split | high |
| `2-参照引用/scripts/bind_reference_assets.py` | 机械匹配与校验 helper | `scripts/README.md` 作为 legacy helper 指引；未来可移植为融合包辅助脚本 | reference only | medium |
| `2-参照引用/CONTEXT.md` | 引用绑定经验 | `CONTEXT.md`、`knowledge-base/video-reference-heuristics.md` | summarize | medium |
| `3-视频生成/SKILL.md` | provider 路由、引用状态判定、submit-plan/brief、provider 槽位语义 | `references/provider-handoff-contract.md`、`steps/frame-visual-reference-workflow.md#N4`、`templates/submit-plan.template.json` | split | high |
| `3-视频生成/CONTEXT.md` | handoff 经验与 prompt-only/unresolved 分流 | `CONTEXT.md`、`knowledge-base/video-reference-heuristics.md` | summarize | medium |

## Non-Removal Rule

- 原三个 source packages 本轮不删除、不移动。
- 本融合包可以回指旧包作为来源证据，但运行时执行本包时，以本包 `SKILL.md` 与分区文件为当前入口真源。
- 后续若要替代旧三段链路，必须另开迁移任务，扫描并同步所有引用。
