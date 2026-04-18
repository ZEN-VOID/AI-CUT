# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~2600
current_lines: ~55
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T18:40:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Purpose & Loading Contract

- 本文件保存 `4-转场特效` 的经验层。
- 命中本 skill 时必须和同目录 `SKILL.md` 一起加载。
- 默认以知识库模式维护：优先更新 Type Map、Repair Playbook、Reusable Heuristics，不把它写成过程流水账。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 一上来先想转场或特效名称 | 思维入口层 | 先补 `transition_problem_frame`，把问题说成时间/空间/情绪/感知缺口 | 在主 `SKILL.md` 固定“先框定问题，再比较直切” | 执行记录里先出现问题框定，再出现效果决策 |
| 明明直切最强却硬写转场 | 决策门层 | 回到 `cut_priority_decision`，允许空 patch 或 `直切最佳` | 在主合同与模块细则中固定直切优先 | 空 patch 能被视为合格结果，而不是漏写 |
| `组内 / 组间 / 特效` 三个叶子一起膨胀 | 路由层 | 只保留真正命中的叶子，删除无收益 patch | 在主 `SKILL.md` 固定最小命中集路由 | sidecar 不再出现“全叶子全开” |
| 特效开始抢戏或替代叙事 | 叶子越权层 | 先删 `fx_decision`，回退到 `组内` 或 `组间`，必要时退回直切 | 在 `特效` 叶子固定“默认答案优先是不需要” | 转场不再盖过角色、动作和摄影主轴 |
| 主 `SKILL.md` 太薄，执行只靠 `module-guide` 记忆 | 真源分层层 | 把 cut-first、leaf-routing、trim gate 提升到主合同 | 保持“主文档骨架化，细则下沉但显式回链” | 只读主 `SKILL.md` 也能看清 branch 执行顺序和失败门 |
| `组间` 只写“送入感”，却没锁 `尾出帧 -> 首入锚` | 叶子方法层 | 先补双锚解构和主导 delta，再决定是否需要尾钩 | 在 `组间/module-spec.yaml` 固定 exit-entry anchoring 和四类连接选型 | `inter_group_hook` 能说清“从哪送出、往哪接住” |
| 四类连接被整段照搬成完整视频 prompt | 方法迁移层 | 把描述收缩为 detail 阶段最小尾钩，只保留连接语法和送入收益 | 在 `组间` 细则中固定“吸收 7.1.2 内核，但不产出完整视频 prompt” | 输出不再预写下一组，也不出现整段 provider 化提示词 |
| 连接类型对了，但透视变化没写 | 6.2.3 对齐层 | 回到 `组间` 补景别/占比/位置/朝向的透视适应，最少写“变化趋势”或“保持一致” | 在 `组间/module-spec.yaml` 把透视适应列入 must-answer 与 quality gate | `inter_group_hook` 不再只有抽象送入感，还能说明视觉接续依据 |
| detail 叶子开始回填 `前序连接/后序连接/status` | 真源越界层 | 删掉对 `connection_optimization` 的直接写入，只保留当前镜头字段内的组间尾钩 | 在 `组间/module-guide.md` 明示 `6.2.3` 才是双向回填真源 | `3-Detail` 不再和 `6.2.3` 争夺字段所有权 |

## Repair Playbook

1. 先回读当前 root，确认 `分镜构图 / 摄影美学 / 运镜手法` 已作为前置存在。
2. 用一句话写出当前组真正的衔接缺口，不要先发明效果名。
3. 强制比较直切、普通收尾和极轻 handoff 是否已经足够。
4. 只有在“不补不够”的情况下，才按 `组内 -> 组间 -> 特效` 命中必要叶子。
5. 汇流时先删重复解释，再删喧宾夺主的特效，最后保留最小有效 patch。
6. 结束前检查 `thinking_process` 四键和唯一 target path 是否齐备。
7. 若命中 `组间`，必须额外检查：是否已经锁了 `尾出帧 -> 首入锚`、是否选了四类连接之一、是否仍保持尾钩级别。
8. 若命中 `组间`，再检查：透视适应是否写清，且没有越界去改 `connection_optimization`。

## Reusable Heuristics

- `4-转场特效` 最有价值的输出，往往是证明“这里不用效果更强”。
- 如果说不清观众到底在哪一刀被硌住，通常说明这里还不需要显式转场。
- 转场 branch 的第一职责不是“更好看”，而是“更顺地送过去，同时不抢戏”。
- 只有当普通画面与保守转场都不够时，`特效` 才有资格进入候选集。
- 主 `SKILL.md` 应该拥有 cut-first、route-only-what-is-needed、trim-before-output 这三个总闸门；`module-guide.md` 再负责展开 craft 细节。
- `组间` 最稳的写法不是描述“下一组会看到什么”，而是描述“观众带着什么离开这一组，并凭什么自然接住下一组”。
- 四类连接在 detail 阶段的作用是帮助选送入语法：依赖型保锚，流动型保势，变形型保识别，复合型保主辅两层；它们不是让 `组间` 直接升级成视频提示词生成器。
- 真正对齐 `6.2.3` 不只是写出连接类型，还要把透视适应写出来；否则连接语法成立，视觉接续仍然是空的。
- `6.2.3` 负责批量分析和双向回填，`3-Detail/组间` 只负责把这套分析语法压缩成当前镜头字段里的尾钩提示，两者不能混成一个真源。
