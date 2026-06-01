# Review Contract: libTV画布流

本 review 合同检查 `libTV画布流` 是否完成计划层职责，并是否正确把真实执行交给最新版 `.agents/skills/cli/libTV`。

## Review Gates

| gate_id | gate | pass condition | fail code |
| --- | --- | --- | --- |
| `REV-LIBTVCANVAS-01` | route | 路线唯一；默认主体参照流，分镜参照流只在显式指定时占位 | `FAIL-ROUTE` |
| `REV-LIBTVCANVAS-02` | group source | 目标 `## x-y-z` 分镜组原文和 fenced YAML 可回指；连接件跳过 | `FAIL-GROUP-SOURCE` |
| `REV-LIBTVCANVAS-03` | subject binding | 主体绑定表只来自 YAML `角色 / 场景 / 道具`，含 `stable_subject_id/yaml_name/category/node_key/assetId/url`，并可回指 stable subject mapping | `FAIL-SUBJECT-BINDING` |
| `REV-LIBTVCANVAS-04` | duration/spec | duration 4-15 秒 clamp，规格默认 720p / 16:9 或用户显式覆盖 | `FAIL-DURATION-SPEC` |
| `REV-LIBTVCANVAS-05` | prompt hygiene | 远端创作 prompt 只含原样分镜组正文和完整 YAML；已验证 `{{Image N}}` 主体引用只出现在 YAML `角色 / 场景 / 道具` 条目后，不含 `{{Portrait N}}`、绑定表、执行锁或诊断文本 | `FAIL-PROMPT-HYGIENE` |
| `REV-LIBTVCANVAS-06` | reference budget | 单组参考图 <= 9；预算排除有记录 | `FAIL-REFERENCE-BUDGET` |
| `REV-LIBTVCANVAS-07` | official CLI handoff | 使用 `.agents/skills/cli/libTV` 的 `libtv` 命令；无旧会话接口 / HTTP fork | `FAIL-OFFICIAL-HANDOFF` |
| `REV-LIBTVCANVAS-08` | download policy | 默认不下载；显式下载才计划或执行 `libtv download` | `FAIL-DOWNLOAD-POLICY` |
| `REV-LIBTVCANVAS-09` | evidence artifacts | manifest、submit plan、queue record、CLI handoff plan、执行报告路径完整 | `FAIL-EVIDENCE` |
| `REV-LIBTVCANVAS-10` | reference mode | 有可用参考图时显式 `mixed2video` 或经模型 schema 等价确认；不得静默 text2video fallback | `FAIL-REFERENCE-MODE` |
| `REV-LIBTVCANVAS-11` | prompt identity | 保留上游场景/镜头身份、镜头先行顺序、方向参照和光线结果 | `FAIL-PROMPT-IDENTITY` |
| `REV-LIBTVCANVAS-12` | active registry | `projectUuid::category::yaml_name` active 唯一；替换时旧记录 inactive | `FAIL-ACTIVE-REGISTRY` |
| `REV-LIBTVCANVAS-13` | CLI auth boundary | 检查登录状态只用 `libtv account info` 摘要，不输出 token/credentials | `FAIL-CLI-AUTH` |
| `REV-LIBTVCANVAS-14` | plan/execution boundary | 本技能只做计划；真实执行记录显示由 `.agents/skills/cli/libTV` 承接 | `FAIL-PLAN-EXECUTION-BOUNDARY` |
| `REV-LIBTVCANVAS-15` | planned left input order | `planned_left_input_edges[]` 与主体绑定表、active registry 的稳定主体 ID 一致 | `FAIL-LEFT-INPUT-ORDER` |
| `REV-LIBTVCANVAS-16` | runtime image map before run | 每个新视频节点在 `--run` 前已查询 `data.params.imageList[]` 或等价左侧输入顺序，`runtime_image_placeholder_map[]` 能把每个 `{{Image N}}` 唯一回指到正确 `stable_subject_id / node_key / assetId/url` | `FAIL-RUNTIME-IMAGE-MAP` |

## Verdict Model

```yaml
verdict: pass | blocked | needs_rework
route: subject_reference_flow | storyboard_reference_flow | prompt_only | query_or_download | repair_or_review
fail_codes: []
rework_targets: []
evidence:
  manifest: ""
  submit_plan: ""
  queue_record: ""
  cli_handoff_plan: ""
  report: ""
```

## Required Checks

1. `rg` 或等价扫描本轮输出，不得出现旧会话接口命令、旧项目切换命令、旧文件上传命令、旧下载命令或旧本地凭据包装器。
2. submit plan 必须含 `cli_handoff.executor_skill: .agents/skills/cli/libTV`。
3. CLI handoff plan 必须能回指 `.agents/skills/cli/libTV` 的命令文档或 `libtv --help`。
4. 若执行已完成，queue record 必须记录 project / group / node / command summary，而不是旧会话 ID 作为主执行证据。
5. 若没有执行，只能报告 plan-only 或 blocked，不得说视频已生成。
6. 有参考图时，submit plan 必须包含 `planned_left_input_edges[]`；节点创建/更新后、`--run` 前，queue record 必须记录 `queried_runtime_image_map_verified=true`。若首次 runtime map 与 prompt 语义不一致，应先执行自动修复并记录 `auto_repair_actions[]`，而不是直接把可修复错位作为最终阻断。
7. `video_node.params.prompt` 中出现的每个 `{{Image N}}` 必须能在 `runtime_image_placeholder_map[]` 中找到唯一主体绑定，且只能出现在底部 YAML 主体条目后；不得出现在分镜正文或出现未登记编号。
8. 决定性检查点固定在最终节点参数、左侧输入和远端 prompt 都写定之后、`--run` 之前；review 只以这一轮远端查询的 `data.params.imageList[] + data.params.prompt` 判定是否放行。
9. 若决定性查询到的远端 `data.params.prompt` 中出现 `{{Portrait N}}`、绑定表、参考图清单、执行锁或诊断文本，必须先自动清理并重写最终 prompt；只有 CLI 无法写回或远端持续污染时，状态才为 `needs_rework`。
10. 若决定性查询到的 `data.params.imageList[]` 顺序与 prompt 中主体语义不一致，必须先按 `runtime_image_placeholder_map[]` 重写 prompt；只有图片无法唯一回指主体、左侧输入无法重建或重写后仍不一致时，状态才为 `needs_rework`。

## Rework Targets

| fail code | rework target |
| --- | --- |
| `FAIL-OFFICIAL-HANDOFF` | `references/official-libtv-cli-handoff.md`、`steps/libtv-canvas-workflow.md` |
| `FAIL-CLI-AUTH` | `.agents/skills/cli/libTV/commands/login.md`、`.agents/skills/cli/libTV/commands/account.md` |
| `FAIL-PLAN-EXECUTION-BOUNDARY` | `SKILL.md Runtime Guardrails`、`scripts/README.md` |
| `FAIL-EVIDENCE` | `templates/submit-plan-template.md`、`templates/queue-record-template.md`、`templates/output-template.md` |
| `FAIL-PROMPT-HYGIENE` | `references/subject-reference-flow.md` |
| `FAIL-LEFT-INPUT-ORDER` | `references/subject-reference-flow.md`、`templates/libtv-remote-prompt-template.md` |
| `FAIL-RUNTIME-IMAGE-MAP` | `references/subject-reference-flow.md`、`templates/libtv-remote-prompt-template.md`、queue record |
