# Registry

本目录是当前仓库的能力注册真源。

## 文件

- `skills.yaml`
  - repo-local skill 注册表
  - 记录当前已有能力、阶段状态、canonical runtime 与继承候选
- `routes.yaml`
  - 任务路由与前代资产映射表
  - 记录哪些任务优先走当前真源、使用哪个 control plane、哪些资产来自 `AIGC-ZEN-VOID`

## 使用约定

- 新增 repo-local skill 前，先更新 `skills.yaml`
- 新增复杂工作流前，先更新 `routes.yaml`
- 从上一代仓库引入资产时，必须先写入映射，不允许口头继承
- 对多阶段技能树，阶段 `active / shadow / shelved` 状态必须进入注册表，而不是只留在根 `SKILL.md`
- 若某工作流采用项目内 runtime（如 `projects/<项目名>/`），必须同时登记 canonical runtime 与镜像策略
