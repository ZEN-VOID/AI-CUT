# Review Contract

本 review gate 只裁决 `B-分镜故事板参照` 的结构、三步 handoff、LibTV 队列与输出路径，不改写业务主真源。

## Review Dimensions

| dimension | pass condition | fail route |
| --- | --- | --- |
| structure_compliance | Skill 2.0 必需目录、根文件、`agents/openai.yaml` 与 output template 齐备 | 修结构 |
| group_source | 每个目标组可从 `4-分组/第N集.md` 唯一回指，组正文完整 | `references/group-source-contract.md` |
| prompt_authorship | prompt 主体直接使用现有分镜组内容，LLM 只做保真指令化组织 | `SKILL.md#LLM-First Creative Authorship Contract` |
| reference_binding | 参照图路径真实、位于 `6-图像/B-分镜故事板`；无图为空引用；多候选阻断 | `references/storyboard-image-binding-contract.md` |
| libtv_handoff | YAML 可投影为合法提交；远端 handoff 有故事板图时锁 `modeType=singleImage2video` 和 `imageList[0]`，无图时锁 `text2video`；生成 prompt 保留故事板总参照身份与图片 token/编号绑定 | `references/libtv-handoff-contract.md` |
| prompt_fidelity | 默认 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false`；未 opt-in 时远端不得优化、摘要、重新编排或补镜头 | `references/libtv-handoff-contract.md` |
| queue_tracking | 多任务均有 queue row、sessionId 或明确失败原因、next_action | `.agents/skills/cli/libTV/SKILL.md` |
| concurrency | 并发只写临时结果，最终 report / results 单线程汇流 | `steps/storyboard-video-workflow.md` |
| route_clarity | 当前 mode、skipped stages、rework entry 与 next entry 清楚 | `types/type-map.md` |

## Verdict Model

- `pass`：结构与语义 gate 均通过。
- `pass_with_todo`：存在非阻断 TODO，例如部分任务仍在 LibTV 远端排队。
- `blocked`：缺少必需文件、LLM 主创被脚本替代、引用或 LibTV handoff 存在硬失败。

## Local Review Checklist

1. 运行 `validate_skill_2_0.py`。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁与输出合同。
3. 检查 step1 是否以 `4-分组` 为主信息来源，并直接保留组正文。
4. 检查 step2 是否只按 `group_id` 绑定真实故事板图；无图是否为空引用。
5. 检查 step3 是否在有故事板图时锁 `modeType=singleImage2video` 和 `imageList[0]`，无图时锁 `text2video`。
6. 检查远端 `*-libtv-submission.txt` 的 `【直接生成请求】` 是否使用 `【故事板参照说明】 + 【分镜组源文本】` 作为生成 prompt 完整体；不得出现裸图片 token 丢失故事板总参照身份。
7. 检查远端 `*-libtv-submission.txt` 是否声明 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 和禁止优化/重排/摘要/改写/补镜头约束；除非 submit plan 记录用户 opt-in，否则 query 中不得出现远端自行生成的优化版提示词、镜头计划或摘要分镜。
8. 检查生成前是否要求 `LIBTV_ACCESS_KEY credential check`。
9. 检查批量并发是否有 queue ledger、sessionId、next_action 和单线程汇流。
10. 检查输出路径是否全部位于 `projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/`。
