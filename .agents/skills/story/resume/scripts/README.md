# Scripts Boundary

`$story-resume` 不在本分区自带业务脚本。恢复操作统一通过 story 根技能共享 CLI：

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow detect
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow cleanup --chapter {N}
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow cleanup --chapter {N} --confirm
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow fail-task --reason "{reason}"
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow clear
```

## Rules

- 脚本只做机械检测、清理、状态标记和格式化输出，不替代 LLM 对恢复策略的判断。
- 所有恢复命令必须走统一 `story.py` 入口，不直接拼内部模块路径。
- `cleanup --confirm` 必须在 preview 和用户确认之后执行。
- 禁止在 resume 脚本层新增主创正文生成逻辑。
