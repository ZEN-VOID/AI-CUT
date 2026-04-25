# Scripts

本目录只承载机械辅助说明和未来 runner 入口，不承载创作主真源。

## Compatible Legacy Entrypoints

```bash
python3 .agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/scripts/generate_episode_packets.py --help
python3 .agents/skills/aigc/5-Image/2-参照引用/scripts/bind_reference_assets.py --help
python3 .agents/skills/aigc/5-Image/3-图像生成/scripts/generate_submit_plan.py --help
```

## Rule

- prompt 正文必须由 LLM 直接完成。
- 脚本只允许读取、投影、校验、绑定候选、生成 handoff 包或执行 dry-run。
- 若旧脚本需要承担 legacy 主创路径，必须显式使用旧包声明的 guard，且不得把该路径写成本包默认主链。
