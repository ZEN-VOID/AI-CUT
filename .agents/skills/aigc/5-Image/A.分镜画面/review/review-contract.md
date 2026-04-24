# Review Contract

## Scope

交付前审查以下维度：

| dimension | checks |
| --- | --- |
| input | 项目、集号、`分镜ID` 或 source request 是否唯一 |
| prompt | LLM 主创、固定英文前缀、单帧边界、模板骨架 |
| references | 本地路径真实、候选证据强、歧义与拒绝清单完整 |
| provider | provider 唯一、输入运输层匹配、next_entry 清楚 |
| output | request、binding、handoff 均写到兼容 runtime 槽位 |
| fusion | 执行链、跳过链、返工入口和旧包兼容关系清楚 |

## Default Provider

- 默认辅助 reviewer/provider 候选：`code-reviewer`。
- 若上层策略未显式允许真实 subagent 或外部 reviewer 调度，则降级为本地 review checklist。
- 降级时必须记录阻断层级、原计划 provider、实际路径和未真实启动的 reviewer。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付 |
| `pass_with_todo` | 可交付，有非阻断 TODO |
| `needs_rework` | 必须返工 |
| `blocked` | 缺输入、权限或 provider 选择 |

## Checklist

1. `SKILL.md` 是否只承担入口、路由、门禁和输出合同。
2. `references/` 是否承载旧三包融合细则。
3. `steps/` 是否表达判断、动作、证据、路由和 gate。
4. `types/` 是否先判型再进入步骤。
5. `templates/output-template.md` 是否映射 Output Contract 五字段。
6. `CONTEXT.md` 是否保持经验层，不写成过程日志。
7. 原三个技能包是否未被删除或移动。

## Gate Rule

不得在以下情况宣布完成：

- source request 不唯一。
- prompt 正文由脚本主创。
- 引用绑定存在未处理歧义。
- provider 不唯一却写了最终 submit-plan。
- 输出图像 canonical 路径漂到 submit 包目录之外。
