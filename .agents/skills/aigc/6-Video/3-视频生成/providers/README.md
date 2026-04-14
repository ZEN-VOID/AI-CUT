# Providers Slot Notes

本目录只保留 `2-视频生成` 的 provider 槽位命名。

具体规则、路由、handoff 合同与失败闭环以上层 [`SKILL.md`](../SKILL.md) 为准；本文件不是规范真源。

- `grok`
- `kling`
- `seedance`
- `sora`
- `veo`
- `vidu`

硬规则：

1. 这些目录默认不是本地 governed child skill。
2. 只有当某 provider 目录补齐 `SKILL.md + CONTEXT.md` 后，才可被视为本地可执行子技能。
3. 在此之前，`2-视频生成` 只把 provider 当作 handoff 目标名，不把它们当作“已实现能力”。
