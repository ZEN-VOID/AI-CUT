# aigc 3-主体/角色

角色域 router Skill 2.0 包，用于把角色清单、角色细目设计、角色图像生成、增量对账和域级 closeout 路由到正确叶子。

## Directory Tree

```text
角色/
├── 1-清单/
├── 2-设计/
├── 3-生成/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── SKILL.md
├── test-prompts.json
└── README.md
```

## Quick Entry

- 调用名：`$aigc-design-character`
- router 输出：路由决定、命中叶子、上游缺口或域级状态摘要。
- 叶子真源：`1-清单` 写角色清单，`2-设计` 写单角色设计稿，`3-生成` 写主图/多视图和同名 JSON。
- 边界：组根不生成角色正文或 prompt，不补未命中叶子占位。

## Runtime Notes

- 未明确阶段时按 `1-清单 -> 2-设计 -> 3-生成` 找最早缺口。
- 分批追加上游时先做增量对账，保护既有角色、设计稿和生成资产。
- 所有创作型正文由命中叶子 LLM-first 节点逐条理解后落盘，脚本只能做机械辅助。
