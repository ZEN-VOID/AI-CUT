# Polishing Heuristics

本文件保存人工维护的稳定经验和领域 playbook。执行中新增经验优先写入同目录 `CONTEXT.md`，稳定后再提炼到这里。

## Stable Heuristics

- 章节起稿最先失真的地方通常不是剧情点，而是“为什么这一章必须如此发生”的约束包；先锁 planning 义务，再谈文风。
- 当前三模型分工中，GPT 原生流的主场是结构化判断、问题发现、repair brief 和调度验证；进入 `4-润色` 正文修补时仅在用户显式点名、诊断样本或对照实验中使用。
- GPT 参与润色诊断时，优先输出“哪些地方必须动、哪些地方不能动”的修补边界，不要把局部问题扩大成整章改写。
- `north_star` 在 polishing 阶段不应原样引用，应压缩为当前章的整书承诺与章末牵引。
- 上一章缺失不是停工理由；`卷规划.md + 第N章.md` 才是硬输入兜底。
- frontmatter 只做 `润色模型`、`初稿来源` 与 `字数` 标记；约束索引和资料证据放在 context pack / sidecar。
- 只要正文里还能看到 planning 的标题语言，小说化转换就没有完成。
- GPT 原生路径必须留下 context pack、authored draft 与 final writeback 的证据链，避免“我读过了”的口头不可审计状态。

## Source Boundary

- `knowledge-base/` 不承载强制执行合同；强制规则应在 `SKILL.md` 或 `references/`。
- 跨项目可复用故障先写 `CONTEXT.md`，稳定后再提炼到本文件。
