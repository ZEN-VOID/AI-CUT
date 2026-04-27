# Source Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


| type_id | detection | split_strategy | notes |
| --- | --- | --- | --- |
| `explicit_episode` | 出现稳定 `第N集`、`Episode N`、`EP N` 等集标 | 保留原边界 | 最高优先级 |
| `chaptered_novel` | 出现 `第N章`、卷、章、节等小说结构 | 章节作为候选边界，再按 2500-3000 字目标窗合并或拆分 | 章节不等于集数 |
| `plain_novel` | 连续正文，缺少标题或编号 | 按自然段、叙事闭合点和目标字数切分 | 需避免硬截断 |
| `mixed_source` | 多文件、多版本或正文夹杂设定 | 先建立 primary source，再把设定降级为参照 | 执行报告必须说明取舍 |
| `blocked_source` | 无正文、乱码、图片、扫描件或权限不可读 | 停止并返回缺口 | 不得伪造分集 |
