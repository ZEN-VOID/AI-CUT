# CHANGELOG.md

本文件记录 `aigc/3-Detail` 的结构性改动，不参与默认预加载。

## 2026-04-12

- `Case-20260412-AIGC-DETAIL-STAGING-COMPOSITION`
  - 将 `references/分镜表现.md` 的中段结构链从“景别 -> 焦点 -> 空间轴线”扩展为“景别 -> 主陪背景关系 -> 构图布局 -> 构图方式 -> 焦点 -> 空间轴线”。
  - 同步更新 `references/capability-playbook.md` 与 `references/chain-of-thought.md`，把主陪背景层级、构图布局、构图方式提升为 `FIELD-DETAIL-05` 的共享合同，而不是只留在局部细则。
  - 在 `CONTEXT.md` 沉淀新的排序 heuristic，固定 `structural_staging_engine` 的中段收束顺序。
- `Case-20260412-AIGC-DETAIL-SHOT-DESCRIPTORS`
  - 将 `景别 / 镜头属性 / 镜头框架 / 镜头类型 / 镜头视角` 收编为 `FIELD-DETAIL-05` 的 shot-level 镜头描述子槽。
  - 更新 `references/分镜表现.md`、`capability-playbook.md`、`chain-of-thought.md`、`_shared/IO_CONTRACT.md` 与 `output-template.md`，固定这些字段归属 `structural_staging_engine` 而非运镜/摄影链。
  - 扩展 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，将五个子槽设为可选字段并补充示例。
- `Case-20260412-AIGC-DETAIL-ZXY-FUSION`
  - 将 `3-Detail` 从“父 skill + 制作组 subagents”重构为单一 `SKILL.md` 统筹的知行合一并发链。
  - 新增 `references/chain-of-thought.md`、`execution-flow.md`、`type-strategies.md`、`capability-playbook.md`、`output-template.md`，形成“主文档骨架 / references 细则”的真源分层。
  - 更新 `_shared/IO_CONTRACT.md`、`agents/openai.yaml`、`CONTEXT.md` 与审计脚本，删除对旧制作组真源的执行级依赖。
  - 删除已被吸收的外置制作组 team、角色 agent 与 shared 手册目录。
- `Case-20260412-AIGC-DETAIL-DIMENSION-SPLIT`
  - 在 `references/` 下新增 `分镜表现.md`、`角色表现.md`、`场景氛围.md`、`运镜手法.md`、`摄影美学.md`、`转场特效.md` 六个维度细则真源。
  - 将 `capability-playbook.md` 收敛为共享总则、跨维度交接与 review/audit 协调层，不再承载六个维度的全部细节。
  - 更新主 `SKILL.md` 与审计脚本，使六个维度模块成为显式回链的 reference carriers。
  - 将“初始化预设显化 / 大师手法 / 作品桥段 / 具像化表述”植入前置串行链，并把“节奏 / 节拍 / 密度 / 景别 / 焦点 / 知识库命中”细化进 `分镜表现.md`。
  - 为六个维度细则补充 Mermaid 拓扑图，显式表现各自的串行链、并行分支、条件门与回退入口。
- `Case-20260412-AIGC-DETAIL-CINEMATOGRAPHY-LIGHTING`
  - 将 `references/摄影美学.md` 从“光影 / 色彩 / 摄影总协调”三段，扩展为“摄影底座回看 -> 光位与照明类型 -> 组级光影流动 -> 色彩心理 -> 摄影总协调”的可执行链。
  - 同步更新 `references/chain-of-thought.md`、`references/execution-flow.md`、`_shared/IO_CONTRACT.md` 与主 `SKILL.md`，固定摄影链对 `全局风格 / 类型元素 / 导演意图` 的前置吸收关系，以及 `光位 / 色彩` 并行、`光影推进 / 总协调` 串行的网络结构。
  - 在 `CONTEXT.md` 沉淀摄影维度的可复用 heuristic，并明确这次增强不扩 episode schema，只增强内部证据与最终 `摄影美学` 的生成质量。
- `Case-20260412-AIGC-DETAIL-CINEMATOGRAPHY-KB-HIT`
  - 将 `knowledge-base/电影学院派/电影摄影/影像的创造.md` 与 `摄影创作技法.md` 提升为 `references/摄影美学.md` 的显式直参考来源。
  - 新增 `CP-3 命中摄影知识库` 节点，要求先形成 `cinematography_academy_hit_note`，再把高命中规则转译到 `光位 / 组级光影推进 / 色彩心理` 分支。
  - 同步更新 `execution-flow.md`、`chain-of-thought.md`、`_shared/IO_CONTRACT.md` 与主 `SKILL.md`，把摄影知识库命中固定为摄影链的前置证据而不是可有可无的背景提示。
