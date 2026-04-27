# Polishing Heuristics

本文件保存人工维护的稳定经验和领域 playbook。执行中新增经验优先写入同目录 `CONTEXT.md`，稳定后再提炼到这里。

## Stable Heuristics

- 章节起稿最先失真的地方通常不是剧情点，而是“为什么这一章必须如此发生”的约束包；先锁 planning 义务，再谈文风。
- `north_star` 在 polishing 阶段不应原样引用，应压缩为当前章的整书承诺与章末牵引。
- 上一章缺失不是停工理由；`卷规划.md + 第N章.md` 才是硬输入兜底。
- frontmatter 只做润色模型标记；约束索引和资料证据放在 context pack / sidecar。
- 只要正文里还能看到 planning 的标题语言，小说化转换就没有完成。
- GPT 原生路径必须留下 context pack、authored draft 与 final writeback 的证据链，避免“我读过了”的口头不可审计状态。

## Source Boundary

- `knowledge-base/` 不承载强制执行合同；强制规则应在 `SKILL.md` 或 `references/`。
- 跨项目可复用故障先写 `CONTEXT.md`，稳定后再提炼到本文件。
