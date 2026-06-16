# Execution Workflow: 漫画生成

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 把单个 `nine_blade_comic_prompts.v1` group JSON 稳定投影成 9 个 built-in image_gen 单页任务，并在执行模式下得到 9 张漫画页 |
| `business_object` | group JSON、逐页 prompt、built-in handoff prompt set、项目内 PNG 资产、生成报告 |
| `constraint_profile` | 上游 JSON 真源、built-in image_gen 工具边界、项目落盘、跨阶段命名、非九宫格/非变体 |
| `success_criteria` | plan 有 9 个可审计 prompt specs；execute 有 `page01..page09` PNG 与报告 |
| `non_goals` | 重写剧情、替换角色设定、生成视频、默认调用 legacy provider 或 CLI/API |
| `complexity_source` | 单组/多组命名、项目根推断、built-in 默认保存路径、上游连续性投影 |
| `topology_fit` | 串行 plan 主干 + execute fan-out 分支 + 父任务 gather/persist 汇流 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定输入与执行模式 | 用户请求、`prompt_json` | 解析路径、确认 plan/execute、识别项目根 | input path、mode | `N2-VALIDATE` | JSON 文件存在 |
| `N2-VALIDATE` | 确保 2 号 JSON 可消费 | `prompt_json`、2 号 validator | 运行 validator，读取并 normalise JSON | validator stdout/stderr | `N3-TYPE-ROUTE` 或返工 2 号 | returncode=0 |
| `N3-TYPE-ROUTE` | 固定加载类型包 | `types/type-map.md`、mode | 选择 `built-in-imagegen-nine-page` + plan/execute profile | type_profile | `N4-TARGET` | type profile 唯一 |
| `N4-TARGET` | 锁定输出目录和命名 | group metadata、项目路径、参数 | 推断 `group_slug`、`output_dir`、prefix；创建目录 | resolved paths | `N5-PROMPTS` | 多组不覆盖 |
| `N5-PROMPTS` | 编译 9 个单页 prompt | normalized JSON | 保留 `positive_prompt`，追加页码、硬约束、built-in 单页后缀 | page prompt txt files | `N6-PLAN` | 9 个 prompt |
| `N6-PLAN` | 生成 handoff 计划 | page prompts、runtime profile | 写 `imagegen_handoff_plan.json`、`imagegen_prompt_set.json`、pending report | prompt set、plan | plan -> `N8-REPORT`; execute -> `N7-EXECUTE` | prompt set 9 条 |
| `N7-EXECUTE` | 调用 built-in image_gen | prompt set、imagegen skill | 每页一个 built-in image_gen 调用；默认 subagents 并发 fan-out，上限 10 | generated source path(s) | `N7B-PERSIST` 或 failure report | 9 个结果或 blocker |
| `N7B-PERSIST` | 项目落盘 | generated source path(s)、output_dir | 父任务复制/移动最终图到项目目录，归一命名 | PNG files | `N8-REPORT` | 9 PNG 位于项目目录 |
| `N8-REPORT` | 汇总交付证据 | plan、files、mode | 写最终 `comic_generation_report.json` | report path | done | report 可追溯 |

## Branch Rules

- Plan 不调用 built-in `image_gen`，也不要求 `OPENAI_API_KEY`。
- Execute 必须走 `.agents/skills/cli/imagegen` 的 built-in `image_gen`，不得跳转到 CLI/API、Seedream 或 Dreamina。
- 批量生成默认使用 subagents parallel fan-out，最大并发 10；只有用户明确要求主线程串行时才串行。
- Built-in 输出默认可能先落在 `$CODEX_HOME/generated_images` 或 subagent 路径；父任务必须把最终图复制/移动到项目 `output_dir`。
- 若用户给定共享 `output_dir`，命名自动带 `group_slug` 前缀。
- 若任何节点发现剧情、角色、场景或分镜源问题，回到 `2-九刀流漫画提示词`，不在 3 号修创作正文。

## Failure Routes

| fail_code | symptom | route |
| --- | --- | --- |
| `FAIL-CG-INPUT` | JSON 不存在或 validator 失败 | 退回 2 号 JSON |
| `FAIL-CG-TYPE` | mode/provider 混乱 | 重读 `types/type-map.md` |
| `FAIL-CG-PROMPT` | prompt 少于 9 个或缺页码 | 重跑 `N5-PROMPTS` |
| `FAIL-CG-RUNTIME` | 尝试 CLI/API 或 built-in 工具不可用 | 重读 `.agents/skills/cli/imagegen/references/mode-routing.md` |
| `FAIL-CG-PERSIST` | PNG 仍留在 `$CODEX_HOME` 或 subagent 路径 | 重读 `.agents/skills/cli/imagegen/references/output-persistence.md` |
| `FAIL-CG-FILES` | PNG 少于 9 个 | 检查 built-in 生成结果、文件名和 `output_dir` |
| `FAIL-CG-HANDOFF` | 4 号找不到图 | 修命名和 report manifest |
