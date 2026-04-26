# Scripts

`4-分组/scripts` 只承载机械辅助：

- 读取 Markdown 分组稿。
- 估算每组非 YAML 字数。
- 检查分镜组 ID、必填标题、组底 YAML 字段和相邻桥接一致性。
- 输出校验报告。

脚本不得生成分组边界、补位画面、角色/场景/道具创作判断或 canonical 分组正文。遇到缺失内容时，应报错并要求 LLM 或人工回到主创环节修复。

## Commands

```bash
python3 .agents/skills/aigc/4-分组/scripts/validate_storyboard_groups.py projects/aigc/<项目名>/4-分组/第N集.md
python3 .agents/skills/aigc/4-分组/scripts/validate_storyboard_groups.py projects/aigc/<项目名>/4-分组/
```
