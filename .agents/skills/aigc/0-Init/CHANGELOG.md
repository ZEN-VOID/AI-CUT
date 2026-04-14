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
  - 新增默认预建 `projects/aigc/<项目名>/2-Global/全局风格/`、`类型元素/`、`设计元素/`
  - 新增默认预建 `projects/aigc/<项目名>/3-Detail/水月/`、`镜花/`
  - 明确 `4-Design` 仍坚持 domain-first runtime，不把 `1-主体清单 / 2-主体设计 / 3-面板设计` 误投影成项目目录
- 同步新增项目级辅助资产库 bootstrap：
  - `projects/aigc/<项目名>/assets/角色/`
  - `projects/aigc/<项目名>/assets/道具/`
  - `projects/aigc/<项目名>/assets/场景/`
  - `projects/aigc/<项目名>/assets/服装/`
  - `projects/aigc/<项目名>/assets/分镜画板/分镜帧/`
  - `projects/aigc/<项目名>/assets/分镜画板/分镜故事板/`
  - `projects/aigc/<项目名>/assets/分镜画板/漫画/`
  - 根因：初始化缺少统一资产沉淀层，容易把参考素材散落到阶段输出目录里。
