# Scripts

本目录只承载机械辅助说明。`A.分镜画面` 的核心 prompt、画面裁决和 provider route 必须由 LLM 按 `SKILL.md` 与分区合同完成。

## Compatible Legacy Runners

- request projection: `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜帧/scripts/generate_episode_packets.py`
- reference binding: `.agents/skills/aigc/5-Image/2-参照引用/scripts/bind_reference_assets.py`
- reference audit: `.agents/skills/aigc/5-Image/2-参照引用/scripts/audit_reference_binding.py`
- submit-plan generation: `.agents/skills/aigc/5-Image/3-图像生成/scripts/generate_submit_plan.py`

## Boundary

- 旧 request projection runner 不得作为默认 prompt 主创入口。
- 绑定和 handoff runner 可作为 dry-run、投影、校验或落盘辅助。
- 若未来新增本包本地 runner，必须只做机械编排，不得替代 LLM 主创。
