# Type Map Entry

本文件是 validator 约定的类型入口，规范真源仍由同目录 `book-level-type-map.md` 承载。

## Loading Contract

- 每次调用 `story-plan-book-level` 时，必须加载 `book-level-type-map.md`。
- 本入口不新增类型变量、不改写路由矩阵，只把 canonical `types/type-map.md` 回接到既有部级类型真源。

## Package Index

| package | role |
| --- | --- |
| `book-level-type-map.md` | 部级规划类型变量、分支矩阵与默认画像 |

## Default Package Rule

默认加载 `book-level-type-map.md`；若未来新增更细类型包，必须先在本入口登记再允许被调用。

## Loading Flow

1. 先加载本文件，确认 canonical type entry。
2. 再加载 `book-level-type-map.md`。
3. 将其产出的 type profile 交给 `steps/book-level-planning-workflow.md` 消费。

## Canonical Type Source

- `book-level-type-map.md`

