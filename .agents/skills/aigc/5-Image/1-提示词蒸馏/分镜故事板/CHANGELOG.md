# CHANGELOG

## 2026-04-12 - 分镜故事板全量升格为单文件真源

### 变更主题

- 按 `skill-subagents` 的扁平 skill 升格规则，将 `分镜故事板` 从“主合同 + references”重构为单文件 `SKILL.md` 规范真源。

### 新增

- `agents/openai.yaml`
- 单文件 `SKILL.md` 内联的执行流程、输出契约、类型策略、字段主表与验收门禁

### 修改

- `SKILL.md`
  - 删除 `Canonical Module References`
  - 合并原 `chain-of-thought / execution-flow / type-strategies / output-template`
  - 修正 shared template 路径为 `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
  - 修正 root-cause 与 context preload 中的旧路径
- `CONTEXT.md`
  - 保留经验层定位，删除“稳定后下沉到 references”的旧建议
  - 补充单文件真源收拢的里程碑案例
  - 同步 evidence path 到 `5-Image` 真实目录

### 迁移映射

- `references/chain-of-thought.md` -> `SKILL.md` 的 `Field Master / Thought Pass Map / Pass Table`
- `references/execution-flow.md` -> `SKILL.md` 的 `Canonical Inputs / Canonical Landing / 输入合同 / Mandatory Workflow / Handoff Rule`
- `references/type-strategies.md` -> `SKILL.md` 的 `Strategy Summary / Type Strategy Matrix`
- `references/output-template.md` -> `SKILL.md` 的 `Output Contract`

### 弃用 / 删除

- `references/chain-of-thought.md`
- `references/execution-flow.md`
- `references/type-strategies.md`
- `references/output-template.md`

### 旧路径收敛

- 与目标技能直接相关的文档回指由 `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/...`
  收敛到 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/...`

### 同步项

- 父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 的 Rule Source / Context Preload 路径已同步
- 父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/CONTEXT.md` 的 evidence path 已同步
