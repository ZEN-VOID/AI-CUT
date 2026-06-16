# LibTV CLI Context

本文件是 `.agents/skills/cli/libTV` 的经验层。它不重定义命令参数；命令真源仍是 `SKILL.md`、`commands/*.md`、`node-types/*.md`、`model-schema/schema.md` 和实际 `libtv --help` 输出。

## Type Map

| situation | signal | handling |
| --- | --- | --- |
| login required | 命令返回未登录或账号为空 | 执行 `libtv login web --open`，再用 `libtv account info` 验证 |
| canvas scoped work | 已知具体画布 UUID | 优先每条命令显式传 `-p <projectUuid>`；需要目录默认时才用 `libtv project use <projectUuid>`；不要把 `projectSpaceId` / `folderId` 传给 `-p` |
| group scoped work | 已知分组名或 groupNodeKey | 用 `libtv group` 查询/创建/绑定；批量节点操作传 `-g` 或使用 `libtv group use` |
| asset upload | 本地图片/视频/音频要进入画布 | 用 `libtv upload`，记录 stdout 的 node key 和资源信息 |
| batch upload hits HTTP 503 / upstream reset | 批量 `libtv upload` 中途返回 `HTTP 503: upstream connect error` 或连接重置 | 把每个成功上传的 stdout 立即登记到本地 manifest；中断后从 manifest 最后一条之后续传，对单文件做小次数重试；不要重传已登记节点 |
| node execution | 已有节点需要运行 | 用 `libtv node <node> --run`；执行前按 `node.md` 校验是否允许只 run |
| batch image generation hits 2020057 | 返回“已达到可并行生图的任务数量上限” | 降级为单任务串行；不要继续高并发提交；失败节点若已创建且参数完整，后续只补 `libtv node <node> --run` |
| shell loop passes node names through stdin | 日志出现“管道输入第 N 行不是合法的单行 JSON” | 在 `while read` / 文件输入循环中调用 `libtv node` 时显式追加 `</dev/null`，避免 CLI 把循环输入当作上游 NDJSON |
| image create-run returns failure after node exists | `libtv node create ... -r` 返回非零，但同名节点已出现在画布，且可能为 status=1/3 | 不要继续重试 create；先按展示名查询同名节点。若 status=2 则登记成功；否则对同名节点执行 `libtv node <node> -r` 接管重跑，保持命名和位置不变 |
| image task stalls near completion | 图片任务长时间停在 progress 99 且无 URL | 不立即判定失败；先旁路 `libtv node <node>` 查询。若最终 status=2 则登记；若转为 status=3 或本地 `-r` 返回非零，再用同名节点 `-r` 重跑 |
| rename by node id appears successful but not persisted | `libtv node <id> --name <new>` 输出新名，但随后查询画布仍是旧名 | 对展示名唯一的节点，改用旧展示名定位：`libtv node "<old-name>" --name "<new-name>"`；执行后重新拉画布摘要验证 |
| model field uncertainty | 不确定模型字段或 `modeType` | 用 `libtv model` 或 `model-schema/schema.md` 查 schema，不凭经验臆造字段 |
| video default model | 创建/更新 video 节点且计划未指定模型 | 默认写 `-s model=star-video2`；fast 只接受显式覆盖 |
| video run rehydrates stale params | 单独 `libtv node <video> --run` 后，远端把 `settings.duration` 等参数恢复成旧值 | 把关键 `-s` 参数与 `--run` 放在同一条命令里提交；完成后重新查询节点确认参数与 task 状态 |
| Seedance mixed video compliance mismatch | 参考图已有 `compliantExempt=true` 但无 `assetId`，运行失败提示“请先进行合规校验后重试” | 对当前视频节点的 `imageList` 与 `mixedList` 中对应项补 `portraitCompliantExempt=true`，并与关键生成参数同次 `--run`；不要只补其中一个 list |

## Repair Playbook

1. 命令参数报错：先跑对应 `libtv <command> --help`，再回看 `commands/<command>.md`。
2. 画布找不到：确认当前账号空间和画布所属 `projectSpaceId` / `folderId`，必要时 `libtv account info`、`libtv account list`、`libtv account use <account>`；节点/上传/分组命令需要的是画布 `projectUuid`，不是上层项目空间 ID。
3. 节点重名：优先使用 node key；需要按名称时限定 `-g <group>` 并确保唯一。
4. 分组绑定混乱：用显式 `-p` / `-g` 命令覆盖目录默认；必要时 `libtv project unuse` 或 `libtv group unuse` 清理本地绑定。
5. 执行层与计划层冲突：以调用方的业务计划为任务意图，以本技能命令文档和 CLI help 为执行参数真源。
6. 视频节点沿用到 `star-video2-fast`：检查是否来自用户显式 fast / 极速 / 草稿要求；没有显式覆盖时改回 `star-video2`。
7. 批量生图触发并发上限：先查询已创建节点状态，区分“节点已创建但未 run”和“完全未创建”；已创建节点优先串行补 `libtv node <node> --run`，避免重复创建同名节点。
8. 从文件逐行读取节点名批量 run：每条 `libtv node ... --run` 命令都加 `</dev/null`，否则 CLI 会尝试把后续节点名解析为管道 NDJSON。
9. 批量图片节点 create+run：若 `create -r` 超时、失败或被中断，下一步必须先按展示名查询同名节点。节点已存在时禁止再次 create；按 status 分流：`2` 直接登记，`1/3/4/空` 用同名节点 `-r` 重跑或查询确认。
10. 批量改展示名：若用 node id 改名后远端摘要仍保留旧名，不要相信单次返回体；改用旧展示名作为位置参数重跑，并以 `libtv project <projectUuid>` 的最终摘要作为完成门禁。
11. 视频节点只运行后参数回退：立即重新查询节点；若 `settings.duration` 等关键参数回退，把关键 `-s` 参数与 `--run` 合并提交，不要分两步先改再跑。
12. Seedance 2.0 混合参考视频合规失败：若失败原因是参考图可能包含真人形象，检查 `imageList` / `mixedList` 中无 `assetId` 的项；已有 `compliantExempt=true` 仍可能不足，需在两个 list 的同一项补 `portraitCompliantExempt=true` 后同次运行。
13. 批量上传本地素材时，如果 `libtv upload` 中途遇到 HTTP 503、upstream reset 或连接终止，优先按本地成功登记续传：逐个上传、逐个保存 nodeKey、失败项小次数重试，最终用 `libtv project <projectUuid>` 查询远端节点名前缀并对比 expected/remote 名称清单。

## Reusable Heuristics

- 账号验证只报告摘要，不输出 token、cookie、access key 或 `credentials.json` 内容。
- 管道输出通常是 JSON/NDJSON；后续命令消费时保留 stdout，不把 stderr 进度日志当作数据。
- `project list -p` 中的 `-p` 是页码；节点/上传/分组命令里的 `-p` 是具体画布 UUID，不能混用。
- 真实执行前先确认 `projectUuid`（画布 UUID）、必要的 `projectSpaceId` / `folderId`、目标 group、目标 node 名称/类型和是否需要 `--run`。
- 外部 AIGC 计划层传来的 prompt、subject binding、manifest、queue record 是业务证据；本技能只负责按 CLI 能力落到 LibTV 画布。
- 对 `video` 节点，`star-video2` 是执行层默认模型；历史任务或示例中出现的其它模型不得被继承为默认值。
- 对大量 `image` 节点触发生图时，优先保守串行或低并发；远端 2020057 表示账号当前并发生图额度已满，不是 prompt/schema 失败。
- 对大量 `image` 节点使用 `create -r` 时，远端任务可能在 99% 写回阶段长尾，或本地命令返回失败但节点已创建；批处理脚本应按 node name 幂等恢复，并把每个成功节点写入独立 row/manifest 后再聚合。
- 对展示名批量清洗这类任务，最终验收必须重新查询画布摘要并用目标字符串计数；单个 `libtv node --name` 返回体可能不足以证明远端摘要已更新。
- 视频节点改时长后运行，最终验收至少看三层：节点 `settings.duration`、`taskInfo.status/progressPercent`、新 URL 的媒体探测时长；画布 `resourceMeta.durationSec` 可能滞后保留旧产物时长。
- 对大量本地图片上传，命名和排序应在上传前机械生成，远端验收看“本地 expected names 与画布 remote names 完全一致”，不要只看上传命令返回的成功条数。
