# aigc-resume

`aigc-resume` 是 `.agents/skills/aigc/` 的根级续跑恢复卫星技能，用于中断恢复、治理缺口识别和唯一下一入口回接。

## 目录树

```text
resume/
├── references/
│   ├── migration-matrix.md
│   ├── project-runtime-layout.md
│   └── workflow-resume.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── resume-review-gate.md
├── steps/
│   └── resume-workflow.md
├── knowledge-base/
│   └── resume-heuristics.md
├── types/
│   └── resume-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## 快速入口

- 调用名：`$aigc-resume`
- 默认输入：项目名、项目路径或当前位于 `projects/aigc/<项目名>/` 的工作目录。
- 默认输出：恢复模式、证据链、缺口、唯一下一入口。

## 验证

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/resume
python3 scripts/skill_context_audit.py --root .agents/skills/aigc/resume --strict
```
