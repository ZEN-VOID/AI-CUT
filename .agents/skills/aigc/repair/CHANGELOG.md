# Changelog

## 2026-06-04

- 按 `skill-2.0` runtime-spine 最新规范升级：在 `SKILL.md` 补齐业务画像、类型路由、主节点、模块授权/触发矩阵、收敛合同、review gate binding、量化口径、注意力协议、检查点和评估 prompt 合同。
- 删除旧 workflow 第二执行链，将 source review、impact map、owner route、Doubao lane、asset route、downstream sync 和 review gate 节点收束到 `SKILL.md`。
- 新增 `test-prompts.json`，覆盖 repair plan、execute text repair、asset route audit 三类回归场景。
- 同步 README、类型图、source ledger 与 Doubao execution reference 中的旧 workflow 引用，并通过 delivery validator 与 smoke test。

## 2026-05-24

- 初始化 `aigc-repair` Skill 2.0 卫星技能包。
- 增加源层回看、影响范围、豆包执行、中文润色、创意激发、生成资产修复路线和 review gate 合同。
