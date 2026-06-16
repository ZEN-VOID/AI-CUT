# Changelog

## 2026-06-11

- 同步 `2-美学` 输出 scope：摄影阶段读取 `画面基调` 全局 singleton；摄影风格按当前 `第N集` 优先读取 `2-美学/第N集/摄影风格/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`README.md` 与 agent prompt，辅助分镜/角色/场景风格也采用逐集优先、项目级回退。

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求运镜注入证明 `6-分镜` 既有空间层次、轴线、起始状态帧和 `2-美学` 摄影风格如何投影为机位、路径、速度和焦点行为。
- 新增 `FAIL-CAM-UPSTREAM-CONTEXT`、`GATE-CAM-08-UPSTREAM-CONTEXT` 和报告 `Upstream Context Application Map`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-05

- 将“机械指标不得 pass”落成硬门：覆盖率、四要素齐全、重复率下降、报告字段完整和脚本扫描通过只能作为格式底线或风险信号，不能替代作者性、差异化和运镜动机验收。
- 将“repair 不得用脚本改正文”落成硬门：脚本只能辅助列失败点、做 source diff、统计风险和落盘；不得用正则、映射表、词库轮换或批量改写生成/替换运镜正文、焦点行为、速度曲线和镜头角度。
- 新增 `FAIL-CAM-MECHANICAL-PASS` 与 `FAIL-CAM-REPAIR-SCRIPTED` 对应 gate、报告字段、经验层修复打法和回归提示。

## 2026-06-04

- 新建 `7-摄影` Skill 2.0 runtime-spine 包。
- 固定默认 source 为 `6-分镜/第N集.md` 或用户指定稿。
- 固定主要上下文为 `2-美学/画面基调` 与 `2-美学/摄影风格`。
- 新增九个 `references/` 细则，覆盖原文增量保真、运镜动机、动态语言、一镜到底、连续性、高点、过渡边界和 AI 视频可执行性。
- 明确 `7-摄影` 是全新阶段，不套用旧阶段链路。
