# Scripts Boundary

本目录只允许保存机械辅助说明或本地校验脚本。

当前 `libTV画布流` 定位为计划层，不在本目录保存 LibTV provider bridge、HTTP 调用、旧会话接口或远端执行脚本。

允许：

- 解析 `6-分组/第N集.md` 的分镜组和 YAML。
- 校验 manifest / submit plan / queue record schema。
- 检查 artifact 路径、命名、重复主体、预算上限。
- 生成不含凭据的 dry-run / report。

禁止：

- 复制或改写 `.agents/skills/cli/libTV` 的命令实现。
- 重新引入旧会话接口、旧项目切换、旧文件上传、旧下载或旧本地凭据包装脚本。
- 直接发 HTTP 请求到 LibTV。
- 读取、打印或保存 `~/.libtv/credentials.json`、token、cookie、API key。
- 用脚本生成核心创作 prompt 正文。

真实执行必须交给 `.agents/skills/cli/libTV`，并在 submit plan / queue record 中记录 CLI handoff 摘要。
