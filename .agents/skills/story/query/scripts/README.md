# Scripts

`$story-query` 当前不拥有私有执行脚本。查询命令统一复用根级 story CLI：

```bash
python3 .agents/skills/story/scripts/story.py --project-root <PROJECT_ROOT> <command>
```

脚本边界：

- scripts 只做机械查询、索引读取、workflow 状态读取和格式化输出。
- scripts 不替代 LLM 对 truth role、证据优先级、冲突解释和边界说明的判断。
- 新增私有脚本时必须提供 dry-run 或只读模式，并在 `SKILL.md` 的 Module Loading Matrix 与 Module Trigger Matrix 中登记。
