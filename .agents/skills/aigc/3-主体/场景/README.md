# aigc 3-主体 / 场景

`$aigc-design-scene` 是场景域父包，只负责路由 `1-清单`、`2-设计`、`3-生成`，不直接创作清单正文、设计稿或生成 prompt。

## Quick Entry

```text
使用 $aigc-design-scene，检查 projects/aigc/<项目名>/3-主体/场景 的清单、设计、生成状态，并路由到最早缺口叶子。
```

## 目录树

```text
场景/
├── agents/
│   └── openai.yaml
├── 1-清单/
├── 2-设计/
├── 3-生成/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Output

- 清单叶子写入 `projects/aigc/<项目名>/3-主体/场景/1-清单/场景清单.md`。
- 设计叶子写入 `projects/aigc/<项目名>/3-主体/场景/2-设计/S###-<场景名>.md`。
- 生成叶子写入 `projects/aigc/<项目名>/3-主体/场景/3-生成/` 图片与 JSON。
