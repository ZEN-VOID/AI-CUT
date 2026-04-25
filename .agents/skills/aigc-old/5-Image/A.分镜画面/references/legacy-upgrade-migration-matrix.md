# Legacy Upgrade Migration Matrix

本矩阵用于追踪原三个技能包如何融合进 `A.分镜画面`。原技能包暂不移除。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1-提示词蒸馏/分镜帧/SKILL.md` | Context / mode / ownership | 入口与真源边界 | `SKILL.md`、`references/fusion-boundary.md` | rewrite | medium | 父级路由增加融合入口 | Skill 2.0 validator |
| `1-提示词蒸馏/分镜帧/SKILL.md` | LLM-First Creative Authorship | 强制主创规则 | `SKILL.md`、`references/request-distillation.md` | keep+summarize | high | 保留旧脚本 guard | 人工语义审查 |
| `1-提示词蒸馏/分镜帧/SKILL.md` | Canonical Inputs / Landing | 输出路径合同 | `SKILL.md` Output Contract、`references/fusion-boundary.md` | keep | medium | 不新增 runtime 真源 | 路径标记检查 |
| `1-提示词蒸馏/分镜帧/SKILL.md` | Node Network / Workflow | 执行拓扑 | `steps/frame-image-workflow.md` | fully absorbed+renumbered | medium | 旧 `N1-N8` 映射到 `F1-F4/F9` | review gate |
| `1-提示词蒸馏/分镜帧/SKILL.md` | Prompt Assembly Rules | prompt 细则 | `references/request-distillation.md` | fully absorbed | high | 旧 `prompt-assembly-spec.md` 保留为兼容证据 | prompt gate |
| `1-提示词蒸馏/分镜帧/prompt-assembly-spec.md` | Composition / JSON spec / budgeting | 句法装配、字段顺序与压缩等级 | `references/request-distillation.md` | fully digested | high | 不再要求运行时回读旧 spec，除非做兼容核对 | prompt gate |
| `1-提示词蒸馏/分镜帧/CONTEXT.md` | Type Map / Playbook / Heuristics | 经验层 | `CONTEXT.md`、`knowledge-base/frame-image-heuristics.md` | merge | medium | 无外部引用迁移 | context audit |
| `2-参照引用/SKILL.md` | Single Truth / Candidate Gate | 参照绑定规则 | `references/reference-binding.md` | rewrite | high | provider 模块路径合并 | binding review |
| `2-参照引用/SKILL.md` | Workflow / Output Contract | 三件套落盘 | `steps/frame-image-workflow.md`、`SKILL.md` Output Contract | merge | medium | next_entry 继续指向生成 handoff | output gate |
| `2-参照引用/references/*.md` | jimeng / nano 绑定模块 | provider 运输层 | `references/provider-modules.md` | summarize | medium | 原模块保留 | provider gate |
| `2-参照引用/CONTEXT.md` | 失败模式与保守绑定 heuristic | 经验层 | `CONTEXT.md`、`knowledge-base/frame-image-heuristics.md` | merge | low | 无 | context audit |
| `3-图像生成/SKILL.md` | Provider route / handoff | 生成提交前组织 | `references/generation-handoff.md`、`references/provider-modules.md` | rewrite | high | 默认 provider 保持 builtin image_gen | handoff review |
| `3-图像生成/SKILL.md` | Output Image Path Contract | 输出路径治理 | `references/generation-handoff.md`、`SKILL.md` Output Contract | keep+summarize | high | 不改 runtime 槽位 | path gate |
| `3-图像生成/references/*.md` | provider 模块 | provider 细则 | `references/provider-modules.md` | summarize | medium | 原模块保留 | provider gate |
| `3-图像生成/CONTEXT.md` | handoff 经验 | 经验层 | `CONTEXT.md`、`knowledge-base/frame-image-heuristics.md` | merge | low | 无 | context audit |

## Residual Compatibility

- 旧三个技能包仍可被直接调用。
- 本融合包优先作为单帧端到端入口。
- 若旧脚本、旧 provider 模块出现变更，应同步复核本矩阵中对应 target owner。
