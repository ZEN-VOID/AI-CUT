# Type Map

本文件只帮助 `$fine-tuning` 判定调优对象类型，不替代 `SKILL.md` 的 `Type Routing Matrix`。

## Package Index

| package_id | path | applies_when | owner |
| --- | --- | --- | --- |
| `stage-output-types` | `types/stage-output-types.md` | 调优对象需要识别为阶段产物、候选 patch、review finding、外部参考或 provider 证据 | `fine-tuning` |

## Default Package Rule

- 默认加载 `types/stage-output-types.md`。
- 若目标对象无法映射到 `2-10`，不得继续候选生成；回到 `N1-INTAKE` 或转路由。
- 类型包只输出 `type_profile`，不得裁决调优质量或写回路径。

## Loading Flow

1. `N1-INTAKE` 读取用户请求、路径、标题、字段和目标产物。
2. 加载 `types/stage-output-types.md` 生成 `type_profile`。
3. 将 `type_profile` 回交 `Type Routing Matrix` 和 `N2-SCHEME-MATCH`。
4. 若类型冲突，按 owning stage 合同与用户显式指令裁决。
