# CHANGELOG

## 2026-04-12 - zhixing-action-network refactor

### 修改

- 在不改变现有输入输出、模板依赖、桥段提取规则、字数窗与三件套落点的前提下，将 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md` 重排为 `$skill-知行合一` 的 inline-full-spec 单技能网络。
- 新增 `Business Requirement Analysis Contract`、`Total Input Contract`、`Topology Contract`、`Convergence Contract` 与 `One-Shot Output Contract`，并将执行主干细化为 `N0-N9` 思行节点。
- 补充多张 Mermaid 图，显式承载主干流程、桥段判型、预算分支与状态推进。
- 更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`，沉淀本次知行合一重排案例与可复用 heuristic。
- 微调 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/agents/openai.yaml`，让入口描述与当前单技能网络口径对齐。

### 保持不变

- `projects/aigc/<项目名>/6-Video/首帧参照/第N集/` 三件套落点不变。
- `FIELD-VID-FFR-01` 到 `FIELD-VID-FFR-04` 字段主表不变。
- `single_shot / direct_match / ambiguous` 与 `normal / tight / underflow` 机制不变。
- 共享模板依赖仍为 `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json` 与 `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`。

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
