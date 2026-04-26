# Scripts

本目录只承载机械性辅助脚本或说明，不替代 LLM 对部级规划的主创判断。

当前 `story-plan-book-level` 没有独立脚本。结构、路径或输出校验优先使用父层脚本：

```bash
python3 .agents/skills/story/2-Planning/scripts/validate_planning_outputs.py --help
```

允许未来加入的脚本范围：

- 检查 `整体规划.md` 是否包含必填标题。
- 检查 Mermaid 代码块是否存在。
- 统计缺失字段并输出报告。

禁止范围：

- 自动生成书名、故事大纲、卷划分、任务关系、冲突、节奏曲线或规避正文。
- 用模板拼接替代 LLM 主创判断。
