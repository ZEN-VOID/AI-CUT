# Scope: Stage Output

用于修复 `0-初始化` 到 `8-分组` 及文本型阶段输出。

## Fixed Context

- 必须定位目标文件所属 stage，并加载该 stage 的 `SKILL.md + CONTEXT.md`。
- 文本修复必须保持该阶段字段、编号、路径和 Output Contract。
- 下游问题先判断是否源于本阶段规则，不默认在下游补丁中掩盖。

## Review Gate

- `source_rules_reviewed` 包含 owning stage。
- 新文本仍符合 owning stage 的字段和格式门禁。
