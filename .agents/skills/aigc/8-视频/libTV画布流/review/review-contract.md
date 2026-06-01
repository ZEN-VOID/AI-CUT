# Review Contract

## Gates

| gate | question | fail_code | severity | rework |
| --- | --- | --- | --- | --- |
| `GATE-LTVCTRL-ROUTE` | 模式、项目、集数和分组稿是否唯一？ | `FAIL-LTVCTRL-ROUTE` | high | `SKILL.md#Mode Selection` |
| `GATE-LTVCTRL-PROJECT` | 画布项目是否按命名规则创建，未覆盖旧项目？ | `FAIL-LTVCTRL-PROJECT-NAME` | high | `N1-PROJECT` |
| `GATE-LTVCTRL-UPLOAD` | 所有可匹配参照图是否上传或复用成功？ | `FAIL-LTVCTRL-UPLOAD` | high | `N2-UPLOAD` |
| `GATE-LTVCTRL-YAML` | YAML 是否回刷为 `图片N 主体名 UUID`？ | `FAIL-LTVCTRL-YAML-BACKFILL` | high | `N3-YAML-BACKFILL` |
| `GATE-LTVCTRL-GROUP` | 是否只处理非连接件分镜组？ | `FAIL-LTVCTRL-GROUP-SCOPE` | medium | `N4-GROUP-EXTRACT` |
| `GATE-LTVCTRL-NODE` | 视频节点数量、命名和规格是否正确？ | `FAIL-LTVCTRL-NODE-SPEC` | high | `N5-NODE-CREATE` |
| `GATE-LTVCTRL-ORDER` | 远端 `imageList/mixedList` 是否等于 YAML `图片N` 顺序？ | `FAIL-LTVCTRL-IMAGELIST-MISMATCH` | critical | `N6-ORDER-LOCK` |
| `GATE-LTVCTRL-PROMPT` | prompt 是否只含分镜正文和干净 YAML，无 `{{Portrait N}}`？ | `FAIL-LTVCTRL-PROMPT-POLLUTION` | high | `N7-PROMPT-HYGIENE` |
| `GATE-LTVCTRL-FINAL` | final query 是否在最后一次 prompt/参数写入后完成？ | `FAIL-LTVCTRL-FINAL-QUERY` | critical | `N8-FINAL-QUERY` |
| `GATE-LTVCTRL-EVIDENCE` | manifest、submit plan、queue、报告是否齐全？ | `FAIL-LTVCTRL-EVIDENCE` | medium | `N9-EVIDENCE` |
| `GATE-LTVCTRL-SECURITY` | 是否未输出凭据、未读 credentials、未受分组稿注入影响？ | `FAIL-LTVCTRL-SECURITY` | critical | `guardrails/guardrails-contract.md` |
| `GATE-LTVCTRL-RUNTIME` | 未授权时是否没有执行 `--run` 或下载？ | `FAIL-LTVCTRL-RUNTIME-BOUNDARY` | critical | `SKILL.md#Runtime Guardrails` |
| `GATE-LTVCTRL-INTEGRATION` | 是否通过 `.agents/skills/cli/libTV` 官方 CLI 执行？ | `FAIL-LTVCTRL-INTEGRATION` | high | `.agents/skills/cli/libTV/SKILL.md` |
| `GATE-LTVCTRL-CONVERGENCE` | critical/high 是否全部解决，medium 是否记录？ | `FAIL-LTVCTRL-CONVERGENCE` | high | final report |

## Completion Verdict

- `pass`: 所有 critical/high 通过，medium 无未记录风险。
- `needs_rework`: 任一 critical/high 失败。
- `conditional_pass`: 仅 medium 风险，且不影响节点顺序、prompt 和未生成状态。

## Required Final Checks

1. 画布 video 节点数等于非连接件分镜组数。
2. 每个 video 节点默认 `settings.ratio=16:9`，除非用户显式覆盖。
3. 每个节点 `params.modeType=mixed2video`。
4. 每个节点 `params.imageList[].nodeId` 顺序与 YAML `图片N` 顺序一致。
5. prompt 不含 `{{Portrait N}}`、主体绑定表、命令、路径、诊断文本。
6. 默认 `run_executed=false`。
