# Changelog

## 2026-06-10

- 创建 `分镜平面图` Skill 2.0 包，承接原 `分镜故事板` 中的 spatial floor plan 职责。
- 定义组级多 panel 顶视图平面图概念：黑白建筑平面图底图、彩色几何角色图标、规定颜色动线/机位/运镜/强调标注。
- 建立 runtime spine、review gates、输出模板、类型包、guardrails、test prompts 和产品入口元数据。
- 收紧完成态：`分镜平面图` 不得停在 `imagegen-plan.json`；该文件只是调用 `.agents/skills/cli/imagegen` 的执行载体。
- 同步 `SKILL.md`、review、output template、type map 与 README，明确必须直接调用 `.agents/skills/cli/imagegen` 生成并持久化 `floor-plan-sheets/<分镜组ID>.png` 后才能 pass。
