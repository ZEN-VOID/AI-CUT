# aigc-design-prop

`$aigc-design-prop` 是 `3-主体/道具` 组根 router，负责把道具域任务路由到 `1-清单`、`2-设计` 或 `3-生成`，并维护增量对账、顺序门和域级 closeout。

## Quick Entry

- 调用名：`$aigc-design-prop`
- 组根职责：路由、缺口判断、增量对账、域级状态摘要
- 叶子真源：`1-清单/SKILL.md`、`2-设计/SKILL.md`、`3-生成/SKILL.md`
- 禁止边界：组根不写清单正文、设计正文、JSON prompt 或图像资产

## Directory Tree

```text
道具/
├── 1-清单/
├── 2-设计/
├── 3-生成/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Runtime Notes

- `SKILL.md` 是 runtime spine；`SKILL.md` runtime spine 只在叶子目录中作为 legacy read-only reference，不再承载运行时节点真源。
- 创作型裁决必须 LLM-first；脚本只能做读取、枚举、校验、格式检查、manifest 和 dry-run 辅助。
- 任何道具域任务先判断最早缺口：缺清单进 `1-清单`，缺设计进 `2-设计`，缺生成资产进 `3-生成`。
