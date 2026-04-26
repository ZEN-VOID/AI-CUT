# Scripts Boundary

`$aigc-query` 当前不需要专属脚本。查询优先使用 `rg --files`、`sed`、`find`、`git status` 等只读命令。

## Allowed Mechanical Actions

- 定位项目根和候选项目。
- 列出阶段目录文件。
- 读取 `STATE.json`、`governance-state.yaml`、执行报告和 registry/routes。
- 统计文件数量、最近修改时间和路径存在性。

## Forbidden Actions

- 用脚本生成创作正文、分镜、提示词、设计稿或验收 verdict。
- 用脚本把文件存在自动判定为 PASS。
- 在用户未要求保存报告时写入项目文件。
