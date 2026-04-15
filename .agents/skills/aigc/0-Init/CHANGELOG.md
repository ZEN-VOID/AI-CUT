# CHANGELOG.md

本文件记录 `.agents/skills/aigc/0-Init/` 的结构迁移与目录治理说明，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-14

- 目录结构按最新单技能 SKILLS 口径收束为：
  - `SKILL.md`
  - `CONTEXT.md`
  - `CHANGELOG.md`
  - `agents/openai.yaml`
  - `templates/*`
- 在 [`SKILL.md`](./SKILL.md) 新增“单一真源目录合同”，明确：
  - 父 `SKILL.md` 是唯一规范真源
  - `CONTEXT.md` 只保留知识库
  - `agents/openai.yaml` 只保留入口元数据
  - `CHANGELOG.md` 只保留迁移索引
- 删除旧的 `references/advisor-council-mode/module-spec.md`、`references/fast-mode/module-spec.md`、`references/autonomous-mode/module-spec.md`。
  - 根因：这些文件已降级为历史 stub，仓内不存在有效回链，继续保留只会制造“模式子层仍在生效”的错觉。
  - 预防：后续三种初始化模式的合同、节点与 gate 一律只写回父 `SKILL.md`。
- 同步更新 `CONTEXT.md` 与 `agents/openai.yaml`，让经验层和入口元数据与当前目录形态一致。
- 同步升级初始化 runtime bootstrap skeleton：
  - 新增默认预建 `projects/aigc/<项目名>/2-Global/` 阶段根；`2-Global` 阶段执行后在根层写入四个 Markdown
  - 新增默认预建 `projects/aigc/<项目名>/3-Detail/水月/`、`镜花/`
  - 明确 `4-Design` 仍坚持 domain-first runtime，不把 `1-清单 / 2-设计 / 3-面板` 误投影成项目目录
- 同步新增项目级辅助资产库 bootstrap：
  - `projects/aigc/<项目名>/Assets/角色/`
  - `projects/aigc/<项目名>/Assets/道具/`
  - `projects/aigc/<项目名>/Assets/场景/`
  - `projects/aigc/<项目名>/Assets/服装/`
  - `projects/aigc/<项目名>/Assets/分镜画板/分镜帧/`
  - `projects/aigc/<项目名>/Assets/分镜画板/分镜故事板/`
  - `projects/aigc/<项目名>/Assets/分镜画板/漫画/`
  - 根因：初始化缺少统一资产沉淀层，容易把参考素材散落到阶段输出目录里。
- 收紧 `north_star` 真源边界：
  - 删除 `templates/north-star.template.yaml` 中的 `stage_entry_contract`
  - 在 `SKILL.md` 新增 `Stage Entry Ownership Contract`
  - 明确当前 live route truth 只属于 `project_state.yaml / governance-state.yaml`，初始化当轮 handoff 只属于 `init_handoff.yaml`
  - 根因：`north_star` 混入阶段路由和 `rebootstrap` 状态后，会从长期方向主物退化为状态本
  - 预防：审计脚本新增模板级禁用字段检查，样本 `north_star.yaml` 同步归一
- 新增 `benchmark-suite.yaml`，补齐 `0-Init` 的 baseline / boundary / regression 基准任务。
- 在 `SKILL.md` 补加 `Quality Evidence Source` 回链，明确 `benchmark-suite.yaml` 属于动态评测真源，而不是 `CONTEXT.md` 经验层内容。
