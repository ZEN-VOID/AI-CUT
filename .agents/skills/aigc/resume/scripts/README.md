# scripts/

本目录只承载 `$aigc-resume` 的机械辅助说明或未来只读检查脚本。

允许：

- 读取项目状态与阶段文件清单。
- 校验 `STATE.json`、`governance-state.yaml`、恢复报告字段是否存在。
- 生成 dry-run 诊断摘要。

禁止：

- 由脚本生成恢复裁决正文并把它当 canonical truth。
- 自动覆盖阶段业务产物。
- 默认执行 Git hard reset、删除源文本、清空资产或迁移项目目录。

当前包不提供执行脚本；恢复裁决由 LLM 按 `SKILL.md`、`references/`、`steps/`、`types/` 与 `review/` 直接完成，脚本只可作为机械辅助。
