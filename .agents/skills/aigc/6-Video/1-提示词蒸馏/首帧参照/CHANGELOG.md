# CHANGELOG

## 2026-04-14 - image-to-video style governance

### 修改

- 新增 `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md` 作为组级与帧级叶子共享的 `图生视频` 句法原则真源。
- 重写 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/prompt-assembly-spec.md` 的组级桥接句与镜级句法顺序，使单镜 prompt 更偏“主体锚点 -> 镜头起势 -> 当前动作与空间 -> 环境光感 -> 视觉焦点”的 `image-to-video` 组织方式，但内容来源仍保持当前 `3-Detail` 字段。
- 同步更新共享文本模板、父级 `6-Video/SKILL.md`、本地 `SKILL.md / CONTEXT.md / agents/openai.yaml`，把新的 shared-principles -> local-spec 继承关系固化为真源结构。

## 2026-04-14 - prompt-assembly spec elevation

### 修改

- 新增 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/prompt-assembly-spec.md` 作为 `首帧参照` 的句法真源，显式收束组级桥接句、镜级 `P1/P2/P3` 槽位、`tight/ultra` 压缩策略与 `转场特效` 可选挂句。
- 更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/scripts/generate_episode_packets.py`：改为解析并消费 spec，不再把句法字符串散落硬编码在 `build_group_context / build_camera_sentence / build_shot_text / compose_prompt` 等函数里。
- 同步将镜级输入门提升到和 shared director schema 更接近的口径：`道具及状态 / 分镜表现 / 摄影美学` 也纳入硬校验。
- 同步更新 `SKILL.md`、`CONTEXT.md` 与 `agents/openai.yaml`，把 `SKILL.md + prompt-assembly-spec.md` 固化为新的双真源结构。

## 2026-04-14 - char-window raised to 1900

### 修改

- 将 `首帧参照` 的默认字数合同从 `800-1200` 调整为 `1900` 以内，并同步更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`。
- 更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/scripts/generate_episode_packets.py`：`prompt_style.char_limit` 改为 `1900`，`within_target_range` 改按 `<= 1900` 判定，预算状态收敛为 `normal / tight`。
- 更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`，移除“必须逼近下限”的旧经验口径，固定“1900 以内优先保真，不为凑字数硬扩写”。

## 2026-04-14 - detail handoff gate sync

### 修改

- 将 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md` 的输入门、Pass、质量清单与根因合同同步到重构后的 `3-Detail` shared-root handoff：只消费 `metadata.document_phase=ready`，并要求目标分镜所属组 `分镜切换 == len(分镜明细[])`。
- 删除已失效的 `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md` 引用，统一回指当前真实真源 `.agents/skills/aigc/3-Detail/SKILL.md`，并补充 `projects/aigc/<项目名>/3-Detail/validation-report.md` 作为辅助证据入口。
- 更新 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md` 与 `agents/openai.yaml`，把 `ready gate + 分镜切换对齐门` 固化为经验层和入口默认提示。

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
- `single_shot / direct_match / ambiguous` 桥段机制不变；预算机制已在 `2026-04-14 - char-window raised to 1900` 调整为 `normal / tight`。
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
