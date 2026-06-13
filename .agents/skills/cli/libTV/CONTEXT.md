# LibTV CLI Context

本文件是 `.agents/skills/cli/libTV` 的经验层。它不重定义命令参数；命令真源仍是 `SKILL.md`、`commands/*.md`、`node-types/*.md`、`model-schema/schema.md` 和实际 `libtv --help` 输出。

## Type Map

| situation | signal | handling |
| --- | --- | --- |
| login required | 命令返回未登录或账号为空 | 执行 `libtv login web --open`，再用 `libtv account info` 验证 |
| canvas scoped work | 已知具体画布 UUID | 优先每条命令显式传 `-p <projectUuid>`；需要目录默认时才用 `libtv project use <projectUuid>`；不要把 `projectSpaceId` / `folderId` 传给 `-p` |
| group scoped work | 已知分组名或 groupNodeKey | 用 `libtv group` 查询/创建/绑定；批量节点操作传 `-g` 或使用 `libtv group use` |
| asset upload | 本地图片/视频/音频要进入画布 | 用 `libtv upload`，记录 stdout 的 node key 和资源信息 |
| node execution | 已有节点需要运行 | 用 `libtv node <node> --run`；执行前按 `node.md` 校验是否允许只 run |
| batch image generation hits 2020057 | 返回“已达到可并行生图的任务数量上限” | 降级为单任务串行；不要继续高并发提交；失败节点若已创建且参数完整，后续只补 `libtv node <node> --run` |
| shell loop passes node names through stdin | 日志出现“管道输入第 N 行不是合法的单行 JSON” | 在 `while read` / 文件输入循环中调用 `libtv node` 时显式追加 `</dev/null`，避免 CLI 把循环输入当作上游 NDJSON |
| rename by node id appears successful but not persisted | `libtv node <id> --name <new>` 输出新名，但随后查询画布仍是旧名 | 对展示名唯一的节点，改用旧展示名定位：`libtv node "<old-name>" --name "<new-name>"`；执行后重新拉画布摘要验证 |
| model field uncertainty | 不确定模型字段或 `modeType` | 用 `libtv model` 或 `model-schema/schema.md` 查 schema，不凭经验臆造字段 |
| video default model | 创建/更新 video 节点且计划未指定模型 | 默认写 `-s model=star-video2`；fast 只接受显式覆盖 |

## Repair Playbook

1. 命令参数报错：先跑对应 `libtv <command> --help`，再回看 `commands/<command>.md`。
2. 画布找不到：确认当前账号空间和画布所属 `projectSpaceId` / `folderId`，必要时 `libtv account info`、`libtv account list`、`libtv account use <account>`；节点/上传/分组命令需要的是画布 `projectUuid`，不是上层项目空间 ID。
3. 节点重名：优先使用 node key；需要按名称时限定 `-g <group>` 并确保唯一。
4. 分组绑定混乱：用显式 `-p` / `-g` 命令覆盖目录默认；必要时 `libtv project unuse` 或 `libtv group unuse` 清理本地绑定。
5. 执行层与计划层冲突：以调用方的业务计划为任务意图，以本技能命令文档和 CLI help 为执行参数真源。
6. 视频节点沿用到 `star-video2-fast`：检查是否来自用户显式 fast / 极速 / 草稿要求；没有显式覆盖时改回 `star-video2`。
7. 批量生图触发并发上限：先查询已创建节点状态，区分“节点已创建但未 run”和“完全未创建”；已创建节点优先串行补 `libtv node <node> --run`，避免重复创建同名节点。
8. 从文件逐行读取节点名批量 run：每条 `libtv node ... --run` 命令都加 `</dev/null`，否则 CLI 会尝试把后续节点名解析为管道 NDJSON。
9. 批量改展示名：若用 node id 改名后远端摘要仍保留旧名，不要相信单次返回体；改用旧展示名作为位置参数重跑，并以 `libtv project <projectUuid>` 的最终摘要作为完成门禁。

## Reusable Heuristics

- 账号验证只报告摘要，不输出 token、cookie、access key 或 `credentials.json` 内容。
- 管道输出通常是 JSON/NDJSON；后续命令消费时保留 stdout，不把 stderr 进度日志当作数据。
- `project list -p` 中的 `-p` 是页码；节点/上传/分组命令里的 `-p` 是具体画布 UUID，不能混用。
- 真实执行前先确认 `projectUuid`（画布 UUID）、必要的 `projectSpaceId` / `folderId`、目标 group、目标 node 名称/类型和是否需要 `--run`。
- 外部 AIGC 计划层传来的 prompt、subject binding、manifest、queue record 是业务证据；本技能只负责按 CLI 能力落到 LibTV 画布。
- 对 `video` 节点，`star-video2` 是执行层默认模型；历史任务或示例中出现的其它模型不得被继承为默认值。
- 对大量 `image` 节点触发生图时，优先保守串行或低并发；远端 2020057 表示账号当前并发生图额度已满，不是 prompt/schema 失败。
- 对展示名批量清洗这类任务，最终验收必须重新查询画布摘要并用目标字符串计数；单个 `libtv node --name` 返回体可能不足以证明远端摘要已更新。
