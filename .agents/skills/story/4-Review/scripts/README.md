# Scripts

本分区记录 `4-Review` 的机械辅助脚本入口。脚本只做读取、校验、汇流、路径定位和投影，不替代 LLM 或 reviewer 对叙事质量、设定自洽和返工归因的判断。

## Current Runtime Scripts

| script | role |
| --- | --- |
| `.agents/skills/story/scripts/review_runner.py` | 本地 review runner、provider 汇流、aggregate 投影 |
| `.agents/skills/story/scripts/workflow_manager.py` | workflow 状态检测与下游提示 |

## Skill 2.0 Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/4-Review
```

## Boundary

- 可以做 schema 检查、路径检查、registry 读取和 aggregate 写入。
- 不得以脚本规则拼接替代维度审查的叙事判断。
