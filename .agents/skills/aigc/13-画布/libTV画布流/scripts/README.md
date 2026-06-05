# Scripts

本目录只承载机械辅助脚本，例如：

- 解析 `10-分组` fenced YAML。
- 投影本地 YAML 的 `图片N 主体名 UUID`。
- 生成提交 prompt 计划时，将主体行重排为 `图片N 主体名 {{Image N}} UUID`。
- 生成 LibTV CLI 命令计划。
- 校验远端 `imageList` 与本地 YAML 顺序。

脚本不得主创或改写分镜组正文，不得替代 LLM 对歧义主体、缺图跳过和交付裁决的判断。
