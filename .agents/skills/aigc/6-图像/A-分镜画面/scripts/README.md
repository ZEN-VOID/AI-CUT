# Scripts

本目录只承载机械辅助脚本，不替代 LLM 主创。

允许脚本执行：

- 读取 `4-分组` 并抽取候选标题、`分镜N`、YAML 统计和源行号。
- 检查四段式 ID 是否唯一。
- 统计英文 prompt 字符数。
- 检查参照图片路径是否存在。
- 生成 imagegen 任务清单或 dry-run plan。

禁止脚本执行：

- 自动生成 canonical prompt 正文。
- 自动改写剧情桥段、角色动作、镜头语言或画面审美判断。
- 猜测主体名称或为缺失主体伪造引用路径。
- 未经用户许可切换 `.agents/skills/cli/imagegen` 的 CLI/API fallback。
