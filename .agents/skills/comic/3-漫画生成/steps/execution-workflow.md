# Execution Workflow: 漫画生成

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 把单个 `nine_blade_comic_prompts.v1` group JSON 稳定投影成 9 个 CLI imagegen 单页任务，并在执行模式下得到 9 张漫画页 |
| `business_object` | group JSON、逐页 prompt、CLI JSONL jobs、项目内 PNG 资产、生成报告 |
| `constraint_profile` | 上游 JSON 真源、CLI imagegen 参数、项目落盘、跨阶段命名、非九宫格/非变体 |
| `success_criteria` | dry-run 有 9 个可审计 job；execute 有 `page01..page09` PNG 与报告 |
| `non_goals` | 重写剧情、替换角色设定、生成视频、默认调用 legacy provider |
| `complexity_source` | 单组/多组命名、项目根推断、CLI 参数、上游连续性投影 |
| `topology_fit` | 串行主干 + execute/dry-run 分支 + 统一报告汇流 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定输入与执行模式 | 用户请求、`prompt_json` | 解析路径、确认 dry-run/execute、识别项目根 | input path、mode | `N2-VALIDATE` | JSON 文件存在 |
| `N2-VALIDATE` | 确保 2 号 JSON 可消费 | `prompt_json`、2 号 validator | 运行 validator，读取并 normalise JSON | validator stdout/stderr | `N3-TYPE-ROUTE` 或返工 2 号 | returncode=0 |
| `N3-TYPE-ROUTE` | 固定加载类型包 | `types/type-map.md`、mode | 选择 `cli-imagegen-nine-page` + dry-run/execute profile | type_profile | `N4-TARGET` | type profile 唯一 |
| `N4-TARGET` | 锁定输出目录和命名 | group metadata、项目路径、参数 | 推断 `group_slug`、`output_dir`、prefix；创建目录 | resolved paths | `N5-PROMPTS` | 多组不覆盖 |
| `N5-PROMPTS` | 编译 9 个单页 prompt | normalized JSON | 保留 `positive_prompt`，追加页码、硬约束、CLI 单页后缀 | page prompt txt files | `N6-PLAN` | 9 个 prompt |
| `N6-PLAN` | 生成 CLI 计划 | page prompts、CLI params | 写 `imagegen_jobs.jsonl`、plan、pending report | JSONL、plan | dry-run -> `N8-REPORT`; execute -> `N7-EXECUTE` | JSONL 9 行 |
| `N7-EXECUTE` | 调用 CLI imagegen | plan、API key、CLI script | 运行 `generate-batch --no-augment` | CLI exit code、PNG files | `N8-REPORT` 或 failure report | exit=0 且 9 PNG |
| `N8-REPORT` | 汇总交付证据 | plan、files、mode | 写最终 `comic_generation_report.json` | report path | done | report 可追溯 |

## Branch Rules

- Dry-run 不调用 API，也不要求 `OPENAI_API_KEY`。
- Execute 必须调用 `.agents/skills/cli/imagegen/scripts/image_gen.py`，不得跳转到 Seedream/Dreamina。
- 若用户给定共享 `output_dir`，命名自动带 `group_slug` 前缀。
- 若任何节点发现剧情、角色、场景或分镜源问题，回到 `2-九刀流漫画提示词`，不在 3 号修创作正文。

## Failure Routes

| fail_code | symptom | route |
| --- | --- | --- |
| `FAIL-CG-INPUT` | JSON 不存在或 validator 失败 | 退回 2 号 JSON |
| `FAIL-CG-TYPE` | mode/provider 混乱 | 重读 `types/type-map.md` |
| `FAIL-CG-PROMPT` | prompt 少于 9 个或缺页码 | 重跑 `N5-PROMPTS` |
| `FAIL-CG-RUNTIME` | CLI 参数不合法或缺 API key | 重读 `.agents/skills/cli/imagegen/references/cli.md` |
| `FAIL-CG-FILES` | PNG 少于 9 个 | 检查 CLI exit code、文件名、`--out-dir` |
| `FAIL-CG-HANDOFF` | 4 号找不到图 | 修命名和 report manifest |
