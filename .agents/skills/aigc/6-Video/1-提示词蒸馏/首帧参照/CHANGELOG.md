# CHANGELOG

## 2026-04-12 - first-frame-reference full elevation

### 新增

- 新建 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CHANGELOG.md`
- 新建 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/agents/openai.yaml`

### 修改

- 重写 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`，将字段表、执行流程、类型策略、输出契约与审计闭环收束为单一主合同
- 更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`，明确经验层与规范层边界，并补录本次 source-contract 升格案例

### 迁移 / 弃用

- 将 `references/chain-of-thought.md`、`references/execution-flow.md`、`references/type-strategies.md`、`references/output-template.md` 的稳定规范内容并入 `SKILL.md`
- 停止以 `references/` 作为本技能规范载体；目标目录下的 `references/` 文件已移除
- 将技能内默认路径从旧口径 `.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/首帧参照/` 统一为真实路径 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/`

### 关键映射

- 旧规范载体：`SKILL.md + references/*.md`
- 新规范载体：`SKILL.md`
- 旧入口路径：`.agents/skills/aigc/6-视频/subtypes/1-提示词蒸馏/首帧参照/`
- 新入口路径：`.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/`

### 同步检查

- 已回扫目标技能目录内对 `references/*.md` 的引用
- 已更新目标技能 `CONTEXT.md` 中的 evidence path 与路径口径
- 已补齐 skill interface metadata，避免升格后出现“主合同完成但入口元数据缺失”的半成品状态
