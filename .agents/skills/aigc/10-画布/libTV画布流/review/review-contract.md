# Review Contract

## Gates

| gate | question | fail_code | severity | rework |
| --- | --- | --- | --- | --- |
| `GATE-LTVCTRL-ROUTE` | 模式、AIGC 项目、集数、单集语义范围和分组稿是否唯一？ | `FAIL-LTVCTRL-ROUTE` | high | `SKILL.md#Mode Selection` |
| `GATE-LTVCTRL-PROJECT` | 是否把 AIGC 项目 / 集数正确映射到 LibTV projectSpace / folder / canvas，并在其下创建或选择目标画布且未覆盖旧画布？ | `FAIL-LTVCTRL-CANVAS-SCOPE` | high | `N1-CANVAS-SCOPE` |
| `GATE-LTVCTRL-UPLOAD` | 所有可匹配参照图是否上传或复用成功？ | `FAIL-LTVCTRL-UPLOAD` | high | `N2-UPLOAD` |
| `GATE-LTVCTRL-YAML` | YAML 是否回刷为 `图片N 主体名 UUID`？ | `FAIL-LTVCTRL-YAML-BACKFILL` | high | `N3-YAML-BACKFILL` |
| `GATE-LTVCTRL-GROUP` | 是否只处理非连接件分镜组？ | `FAIL-LTVCTRL-GROUP-SCOPE` | medium | `N4-GROUP-EXTRACT` |
| `GATE-LTVCTRL-NODE` | 视频节点数量、命名和规格是否正确？ | `FAIL-LTVCTRL-NODE-SPEC` | high | `N5-NODE-CREATE` |
| `GATE-LTVCTRL-NODE-IDENTITY` | 节点是否使用唯一 `video_node_instance_id`，且 `source_group_id` 重生成不会覆盖或跳过旧实例？ | `FAIL-LTVCTRL-NODE-IDENTITY` | critical | `N5-NODE-CREATE` |
| `GATE-LTVCTRL-ORDER` | 远端 `imageList/mixedList` 是否等于 YAML `图片N` 顺序？ | `FAIL-LTVCTRL-IMAGELIST-MISMATCH` | critical | `N6-ORDER-LOCK` |
| `GATE-LTVCTRL-PROMPT` | prompt 是否只含分镜正文和干净 YAML，且主体行顺序为 `图片N 主体名 {{Image N}} UUID`、无 `{{Portrait N}}`？ | `FAIL-LTVCTRL-PROMPT-POLLUTION` | high | `N7-PROMPT-HYGIENE` |
| `GATE-LTVCTRL-FINAL` | final query 是否在最后一次 prompt/参数写入后完成？ | `FAIL-LTVCTRL-FINAL-QUERY` | critical | `N8-FINAL-QUERY` |
| `GATE-LTVCTRL-EVIDENCE` | manifest、submit plan、queue、报告是否齐全？ | `FAIL-LTVCTRL-EVIDENCE` | medium | `N9-EVIDENCE` |
| `GATE-LTVCTRL-SECURITY` | 是否未输出凭据、未读 credentials、未受分组稿注入影响？ | `FAIL-LTVCTRL-SECURITY` | critical | `guardrails/guardrails-contract.md` |
| `GATE-LTVCTRL-RUNTIME` | 未授权时是否没有执行 `--run` 或下载？ | `FAIL-LTVCTRL-RUNTIME-BOUNDARY` | critical | `SKILL.md#Runtime Guardrails` |
| `GATE-LTVCTRL-INTEGRATION` | 是否通过 `.agents/skills/cli/libTV` 官方 CLI 执行？ | `FAIL-LTVCTRL-INTEGRATION` | high | `.agents/skills/cli/libTV/SKILL.md` |
| `GATE-LTVCTRL-UPSTREAM-DIRECTION` | 是否记录 `LibTV Upstream Video Direction Matrix`，说明上游分组、主体、图像/参照、项目约束和 LibTV 限制如何导向图片顺序、prompt、节点参数、运行边界和 final query？ | `FAIL-LTVCTRL-UPSTREAM-DIRECTION` | high | `../../_shared/upstream-context-application-contract.md` |
| `GATE-LTVCTRL-CONVERGENCE` | critical/high 是否全部解决，medium 是否记录？ | `FAIL-LTVCTRL-CONVERGENCE` | high | final report |

## Completion Verdict

- `pass`: 所有 critical/high 通过，medium 无未记录风险。
- `needs_rework`: 任一 critical/high 失败。
- `conditional_pass`: 仅 medium 风险，且不影响节点顺序、prompt 和未生成状态。

## Required Final Checks

1. Registry / queue record 记录 `local_project_root`、`local_episode`、`local_episode_scope`、`project_space_name`、`projectSpaceId/folderId`、`canvas_name` 和 `projectUuid`。
2. 画布 video 节点数等于本轮应创建的非连接件分镜组实例数。
3. 每个 video 节点名符合 `vid__<source_group_id>__bNNN__rNN__vNNN`，且 registry 中 `source_group_id -> instances[]` 可追溯。
4. 重生成已存在分镜组时，新增实例 ID 不等于旧实例 ID；除非用户显式授权删除，否则旧节点仍保留。
5. 每个 video 节点默认 `settings.ratio=16:9`，除非用户显式覆盖。
6. 每个节点 `params.modeType=mixed2video`。
7. 每个节点 `params.imageList[].nodeId` 顺序与 YAML `图片N` 顺序一致。
8. prompt 主体行顺序为 `图片N 主体名 {{Image N}} UUID`，且不含 `{{Portrait N}}`、主体绑定表、命令、路径、诊断文本。
9. 默认 `run_executed=false`。
10. 报告或 submit plan 包含 `LibTV Upstream Video Direction Matrix`，并能回指 source group、YAML 图片顺序、远端 prompt、`imageList/mixedList`、settings 和 final query。
