# Review Contract

本 review gate 只裁决 `B.分镜故事板参照` 的结构、三段 handoff、输出路径和可复核性，不改写业务主真源。

## Review Dimensions

| dimension | pass condition | fail route |
| --- | --- | --- |
| structure_compliance | Skill 2.0 必需目录、根文件、`agents/openai.yaml` 与 output template 齐备 | 修结构 |
| source_fusion | `全能参照 + 2-参照引用 + 3-视频生成` 的核心语义均能在新 owner 找到 | `references/source-fusion-map.md` |
| omni_config_digest | 涉及蒸馏或旧请求判源时，`N1` 已形成可回放的 `omni_config_profile`，覆盖 `全能参照/SKILL.md + CONTEXT.md`、`prompt-assembly-spec.md` 与共享图生视频原则 | `steps/storyboard-reference-workflow.md#N1` |
| authorship | prompt/TXT 创作正文由 LLM 主创，脚本没有被设为默认主创 | `references/prompt-distillation-contract.md` |
| reference_binding | 绑定路径真实、位于 `Assets/`、无歧义默选、无占位残留 | `references/reference-binding-contract.md` |
| provider_handoff | `submit-plan.json + submit-brief.md` 写清 provider、input mode、引用解析与下一入口 | `references/provider-handoff-contract.md` |
| route_clarity | 当前 mode、skipped stages、rework entry 与 next entry 清楚 | `steps/storyboard-reference-workflow.md` |

## Verdict Model

- `pass`：结构与语义 gate 均通过。
- `pass_with_todo`：存在非阻断 TODO，但不影响本包作为入口使用。
- `blocked`：缺少必需文件、三段来源语义丢失、LLM 主创被脚本替代、引用或 handoff 存在硬失败。

## Local Review Checklist

1. 运行 `validate_skill_2_0.py`。
2. 检查 `SKILL.md` 是否只保留入口、路由、门禁与输出合同。
3. 检查 `references/source-fusion-map.md` 是否覆盖三段旧包。
4. 检查 `N1-INTAKE` 是否在需要时输出 `omni_config_profile`，且不是只列旧路径而漏掉配置吸收。
5. 检查模板路径是否全部位于 `projects/aigc/<项目名>/6-Video/B.分镜故事板参照/<episode_id>/`。
6. 检查父级路由、registry 与审计脚本是否已登记新 leaf。
