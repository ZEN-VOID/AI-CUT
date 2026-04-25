# CHANGELOG

## 2026-04-12 - 分镜故事板按知行合一重构为单文件思行网络

### 变更主题

- 在保留既有输入、模板、字段、落盘和 handoff 机制的前提下，将 `分镜故事板` 从“线性规则型单文件合同”升级为“知行合一单文件思行网络”。
- 明确设置：`复杂链路的骨架 / 细则分层: false`，因此所有规范性节点细则保留在 `SKILL.md` 内，不再另建 `references/`。

### 新增

- `SKILL.md` 中的 `Total Input Contract / Business Requirement Analysis Contract / Topology Contract / Convergence Contract / One-Shot Output Contract`
- `N0-N6` 思维·执行节点总表
- 逐节点 `Node Playbook`
- 4 张 Mermaid 图：主干图、分支回退图、关系图、状态图
- `CONTEXT.md` 中的知行合一升级里程碑案例与新失效类型

### 修改

- `SKILL.md`
  - 收掉不存在的 `.agents/skills/aigc/5-Image/SKILL.md` 旧回链
  - 把执行主干改写为 `N0 入口锁定 -> N1 上游完整性校验 -> N2 分镜组定位 -> N3 storyboard_group 组织 -> N4 prompt 装配 -> N5 模板映射 -> N6 落盘与验收`
  - 将原有字段主表、类型矩阵、输出合同回挂到节点网络与汇流门
  - 补齐 `route_out / gate`，避免“局部动作做完但无法结案”
- `CONTEXT.md`
  - 修正加载顺序到 `aigc -> 1-提示词蒸馏 -> 分镜故事板`
  - 补充“旧阶段根回链”“节点没有门禁”“思考过程不应污染业务真源”等经验项
- `agents/openai.yaml`
  - 更新默认提示，强调遵循 `N0-N6` 思行网络与 canonical output/handoff 边界

### 保持不变

- shared schema：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- shared template：`.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
- canonical business output：`projects/aigc/<项目名>/5-Image/分镜故事板/第N集/第N集.json`
- 可选 sidecar：`_manifest.json`
- 主字段骨架：`meta / prompt_style / model / prompt / prompt_char_count`

### 同步项

- 当前包内所有旧的 `.agents/skills/aigc/5-Image/SKILL.md` 回指已清除
- 当前包继续保持“单文件真源”，未回退为 `references/` 分拆

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
- legacy output contract reference -> `SKILL.md` 的 `Output Contract`

### 弃用 / 删除

- `references/chain-of-thought.md`
- `references/execution-flow.md`
- `references/type-strategies.md`
- legacy output contract reference

### 旧路径收敛

- 与目标技能直接相关的文档回指由 `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/分镜故事板/...`
  收敛到 `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板/...`

### 同步项

- 父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 的 Rule Source / Context Preload 路径已同步
- 父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/CONTEXT.md` 的 evidence path 已同步
