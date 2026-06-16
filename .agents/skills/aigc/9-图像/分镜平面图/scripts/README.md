# Scripts

本目录只承载机械辅助脚本说明。`分镜平面图` 的空间理解、panel 裁决、角色站位、动线、机位、连续性判断、prompt 正文和审查结论必须由 LLM / skill 合同完成，脚本不得主创正文。

允许脚本承担：

- 扫描 `8-分组/第N集.md` 的 `## x-y-z` 标题和 fenced YAML。
- 检查目标组 ID 唯一性、连接件排除和输出路径。
- 检查图片路径是否存在。
- 校验 manifest JSON 字段、图片路径存在性、尺寸字段和报告引用。
- 汇总 imagegen 执行结果和 review gate 状态。

禁止脚本承担：

- 改写、扩写、摘要或补写分镜组正文。
- 生成 `source_spatial_comprehension`、`floor_plan_panels`、角色站位、运动路径、摄影机方向、连续性结论或 prompt 正文。
- 用关键词、正则、映射表或句式轮换批量生成空间逻辑。
- 猜测 YAML 未声明的主体。
- 绕过 `.agents/skills/cli/imagegen` 的内置 `image_gen` 路线，切换到 CLI/API/provider 专属控制。
