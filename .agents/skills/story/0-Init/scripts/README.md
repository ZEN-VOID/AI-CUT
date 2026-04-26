# Scripts Boundary

`story-init` 本目录的 `scripts/` 只保存 Skill 2.0 分区说明和机械辅助入口说明。

## Canonical Runtime Script

实际项目初始化脚本位于：

```bash
python3 .agents/skills/story/scripts/init_project.py \
  "./projects/story/示例小说" "示例小说" "悬疑" \
  --init-mode "team代入模式"
```

## Boundary

- 脚本可以创建目录、写模板、同步 JSON/YAML、执行 dry-run 或校验。
- 脚本不得替代 LLM 对故事核、读者承诺、创意缺口、team 选择理由或 planning 直答的主创判断。
- 如果脚本输出与 `SKILL.md`、`references/` 或 `review/` 合同冲突，先修脚本或模板，不把冲突沉默为经验层例外。

## Validation

Skill 2.0 结构校验使用工作车间 validator：

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/0-Init
```
