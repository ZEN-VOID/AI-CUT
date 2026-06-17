# Story Query Type Packages

`types/` 是 `$story-query` 的判型展开层，不是执行主链。主路由、节点、gate 和输出合同以 `SKILL.md` 为唯一真源。

## Package Index

| package | load_when | purpose | return_to |
| --- | --- | --- | --- |
| `types/query-type-map.md` | 每次 `$story-query` 需要判定 truth role | 定义 `truth_role`、source scope、signal matrix、canonical carrier map 和 source priority | `SKILL.md` `N3-TRUTH-ROLE` |

## Default Package Rule

- 默认加载 `types/query-type-map.md`。
- 不新增平行的 type package，除非新的查询类型会显著扩大 signal matrix 且已在 `SKILL.md` 的 `Type Routing Matrix` 中登记。
- `types/` 可以提供判型变量和 carrier map，但不得新增未被 `SKILL.md` 声明的 mode、route、fail code 或完成门。

## Loading Flow

1. `N1-INTAKE` 收集用户问题、项目线索和疑似 truth role。
2. `N3-TRUTH-ROLE` 读取 `types/query-type-map.md`，形成 `type_profile`。
3. `N4-MODULE-LOAD` 根据 `type_profile` 和 `Module Trigger Matrix` 加载授权 reference、review、template 或 scripts 边界。
4. `N6-CROSS-CHECK` 用 `Source Priority Rules` 拆分 planned/current/validated_actual/quality/execution。
