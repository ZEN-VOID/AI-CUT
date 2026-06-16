# Changelog

## 2026-06-04

- 按 `skill-2.0` runtime-spine 最新规范升级：在 `SKILL.md` 补齐业务画像、量化口径、注意力协议、检查点、评估 prompts、模块授权矩阵、模块触发矩阵、收敛合同和 review gate binding。
- 删除旧 workflow 第二执行链，将 project root lock、truth role、carrier 读取、validation distinction 和输出节点收束到 `SKILL.md`。
- 新增 `test-prompts.json`，覆盖项目治理状态、阶段/资产验收、路径冲突诊断三类回归场景。
- 同步 README、类型图、迁移矩阵、CONTEXT 与 knowledge-base 中的旧 workflow 引用，并通过 delivery validator 与 smoke test。

## 2026-04-26

- 初始化 `.agents/skills/aigc/query` 为 Skill 2.0 查询卫星技能包。
- 参照 `.agents/skills/aigc-old/query` 保留 `PROJECT_ROOT` guard、truth-role first、存在不等于验收、registry/routes 制度查证等配置意图。
- 对齐当前 `.agents/skills/aigc` 中文阶段链路：`0-初始化`、`1-分集`、`2-编导`、`3-运动`、`4-摄影`、`8-分组`、`3-主体`、`9-图像`、`10-画布`、`11-审片`。
- 将旧英文阶段路径降级为 legacy compatibility，并写入 `references/legacy-migration-matrix.md`。
