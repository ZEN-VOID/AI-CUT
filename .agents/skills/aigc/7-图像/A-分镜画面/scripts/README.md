# Scripts

本目录只承载机械辅助脚本，不替代 LLM 主创。

允许脚本执行：

- 读取 `5-分组` 并抽取候选标题、`分镜N`、YAML 统计和源行号。
- 检查四段式 ID 是否唯一。
- 统计英文 prompt 的 English word count；字符数只作为辅助信息。
- 检查参照图片路径是否存在。
- 检查 prompt / manifest / plan 中是否存在 `scene_visual_style_lock_status` 与固定提示词字段。
- 检查 `第N集-分镜画面-prompts.md` 是否覆盖指定范围全部 `shot_id`，并早于 imagegen 执行计划进入生成阶段。
- 生成带 `execution_order` / `serial_index` 的 imagegen 串行任务清单或 dry-run plan。

禁止脚本执行：

- 自动生成 canonical prompt 正文。
- 自动从场景图生成 canonical 风格描述或代替 LLM 判断光影、色调、氛围。
- 自动改写剧情桥段、角色动作、分镜明细或画面审美判断。
- 猜测主体名称或为缺失主体伪造引用路径。
- 未经用户许可切换 `.agents/skills/cli/imagegen` 的 CLI/API fallback。
- 生成并发、后台并行、分片并跑或跳过前镜结果的批量执行计划。
- 生成边生图边补写后续 prompt 的批量执行计划。
