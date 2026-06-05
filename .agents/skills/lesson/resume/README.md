# lesson-resume

`lesson-resume` 是课程课件工作流的恢复卫星技能，用于中断续跑时重建项目证据、缺口、风险和唯一安全下一入口。

## 目录树

```text
resume/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## 快速入口

- 调用名：`$lesson-resume`
- 默认输入：项目名、项目路径，或当前位于 `projects/lesson/<项目名>/` 的工作目录。
- 默认检查：`MEMORY.md`、`CONTEXT/`、0-8 阶段目录、阶段 canonical files、`content-model/`、`8-多端交付生成/doc|ppt|html` 状态。
- 默认输出：恢复证据摘要、缺口、风险、一个安全下一入口或 blocker。

本技能不主创课程内容，不直接续写阶段产物，不生成 DOC/PPT/HTML 成品。

## 验证

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/resume --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/resume --mode delivery
```
