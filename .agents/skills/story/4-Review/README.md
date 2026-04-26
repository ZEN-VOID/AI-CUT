# 4-Review

`4-Review` 是 `story2026` 的卷级终验父技能包。它锁定同一轮 fact pack，调度 mandatory 维度审查，聚合唯一 `第V卷.validation.json`，并决定进入返工、`review/` 或 `5-Loopback`。

## Directory Tree

```text
4-Review/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── _shared/
├── 人物一致性/
├── 任务汇聚/
├── 时间线/
├── 结构兑现/
├── 连续性/
├── 逻辑自洽校验/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/4-Review
```

## Runtime Notes

- `_shared/` 仍是 runner 与子技能消费的兼容运行时载体。
- Skill 2.0 的入口、分区职责、迁移矩阵、review gate 与 output template 已落入 canonical 分区。
- 子技能 sidecar 只做证据；父层 aggregate JSON 是唯一 gate truth。
