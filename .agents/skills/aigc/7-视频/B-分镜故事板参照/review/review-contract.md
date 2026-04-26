# Review Contract

本 review gate 只裁决 `B-分镜故事板参照` 的结构、三步 handoff、Dreamina 队列与输出路径，不改写业务主真源。

## Review Dimensions

| dimension | pass condition | fail route |
| --- | --- | --- |
| structure_compliance | Skill 2.0 必需目录、根文件、`agents/openai.yaml` 与 output template 齐备 | 修结构 |
| group_source | 每个目标组可从 `4-分组/第N集.md` 唯一回指，组正文完整 | `references/group-source-contract.md` |
| prompt_authorship | prompt 主体直接使用现有分镜组内容，LLM 只做保真指令化组织 | `SKILL.md#LLM-First Creative Authorship Contract` |
| reference_binding | 参照图路径真实、位于 `6-图像/B-分镜故事板`；无图为空引用；多候选阻断 | `references/storyboard-image-binding-contract.md` |
| dreamina_handoff | YAML 可投影为合法 `multimodal2video` 或 `text2video` 命令 | `references/dreamina-handoff-contract.md` |
| queue_tracking | 多任务均有 queue row、submit_id 或明确失败原因、next_action | `.agents/skills/cli/dreamina-cli/SKILL.md` |
| concurrency | 并发只写临时结果，最终 report / results 单线程汇流 | `steps/storyboard-video-workflow.md` |
| route_clarity | 当前 mode、skipped stages、rework entry 与 next entry 清楚 | `types/type-map.md` |

## Verdict Model

- `pass`：结构与语义 gate 均通过。
- `pass_with_todo`：存在非阻断 TODO，例如部分任务仍在 Dreamina 远端排队。
- `blocked`：缺少必需文件、LLM 主创被脚本替代、引用或 Dreamina handoff 存在硬失败。

## Local Review Checklist

1. 运行 `validate_skill_2_0.py`。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁与输出合同。
3. 检查 step1 是否以 `4-分组` 为主信息来源，并直接保留组正文。
4. 检查 step2 是否只按 `group_id` 绑定真实故事板图；无图是否为空引用。
5. 检查 step3 是否在有图时走 `multimodal2video`，无图时走 `text2video`。
6. 检查生成前是否要求 `dreamina user_credit`。
7. 检查批量并发是否有 queue ledger、submit_id、next_action 和单线程汇流。
8. 检查输出路径是否全部位于 `projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/`。
