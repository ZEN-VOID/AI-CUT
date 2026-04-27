# Scripts

本技能当前没有私有主创脚本。脚本分区只允许承载机械辅助，例如结构校验、标题检查、模板投影或父层 validator 调用说明。

## Available Checks

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章规划/3-章级
python3 .agents/skills/story/2-卷章规划/scripts/validate_planning_outputs.py --help
```

## Boundary

- 不得用脚本生成章级故事概要、冲突、节奏 handoff、线索、伏笔或建议写法。
- 这些核心 planning 判断必须由 LLM 直接完成。
