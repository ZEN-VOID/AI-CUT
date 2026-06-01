# Context: libTV画布流

本文件是 `aigc/8-视频/libTV画布流` 的经验层知识库，不重定义 `SKILL.md` 的入口合同。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 16000
hard_limit_chars: 32000
status: ok
last_checked_at: 2026-05-30
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 预防检查 |
| --- | --- | --- | --- | --- |
| `TM-LIBTVCANVAS-01` | 用户没有指定路线但任务涉及角色/场景/道具参照出视频 | 默认路线不明确 | 使用 `subject_reference_flow` | `types/type-map.md` 默认包指向主体参照流 |
| `TM-LIBTVCANVAS-02` | 主体名称和图片不匹配 | 依赖随机图片顺序或计划层 `Image N` | 重建 `主体绑定表: stable_subject_id -> yaml_name -> node_key -> assetId/url`，再查询 runtime `imageList` 生成 `{{Image N}}` | 查询验证 `runtime_image_placeholder_map[]` |
| `TM-LIBTVCANVAS-03` | 所有视频都生成 15 秒 | 未读取组底 YAML `时长估算` | 重新提取并按 4-15 秒 clamp | submit plan 记录 duration source |
| `TM-LIBTVCANVAS-04` | 生成后本地目录出现非显式下载文件 | 下载策略未锁定 | 默认 plan 中 `download=false` | 只有用户显式要求才加入 `libtv download` |
| `TM-LIBTVCANVAS-05` | 画布素材只上传成 URL，未变成节点 | 沿用旧 OSS URL-only 思路 | 用新版 `libtv upload` 创建资源节点 | active registry 记录 node_key / url / name |
| `TM-LIBTVCANVAS-06` | 分镜参照流被误执行 | 占位路线被当作已实现 | 返回 `not_implemented_placeholder` | 类型包和 references 都标注空白占位 |
| `TM-LIBTVCANVAS-07` | 远端或执行者重写、压缩 `5-分组` 正文 | handoff 未锁定 prompt 保真 | 重建 clean prompt 和禁止优化锁 | review 检查 prompt identity |
| `TM-LIBTVCANVAS-08` | 主体列表比 YAML 多，混入正文泛词 | 用正文子串或猜测名扩展主体 | 丢弃非 YAML 主体 | review gate 检查 YAML subject baseline |
| `TM-LIBTVCANVAS-09` | 同画布重复上传已有主体图 | 忽略 active URL 复用策略 | 优先复用同 projectUuid 下 active URL | 只有缺 URL、歧义、替换才上传 |
| `TM-LIBTVCANVAS-10` | 单组参照图超过预算 | 未做 9 图裁决 | 角色和场景优先，道具先排除 | `images/mixedList <= 9` |
| `TM-LIBTVCANVAS-11` | active URL 复用口径变化 | 缺少 registry 真源 | 使用 `libtv-canvas-active-registry.json` | 同名 active 只能有一条 |
| `TM-LIBTVCANVAS-12` | 文档仍要求旧本地 env 凭据或旧 access-key 模式 | 旧会话接口迁移残留 | 改为新版 CLI 登录与 `libtv account info` | rg 扫描旧执行入口 |
| `TM-LIBTVCANVAS-13` | 视频节点提示词没有 `{{Image N}}` 或左侧输入，表现为纯文生 | 没有显式锁定 `mixed2video` 或没有连接参考节点 | 阻断并重建 handoff | 有可用参考图时必须有 `planned_left_input_edges[]` 和 `runtime_image_placeholder_map[]` |
| `TM-LIBTVCANVAS-16` | `{{Image N}}` 指向错误主体 | 只验证计划左侧输入，未验证 runtime `data.params.imageList[]` | 清理旧左侧输入，按 canonical order 用 `--left/--left-add` 逐张重连；查询 `imageList` 后按 runtime map 回写 prompt | `runtime_image_placeholder_map[]` 与 queried `imageList` 一致 |
| `TM-LIBTVCANVAS-19` | 稳定 `--left` 顺序后角色图仍匹配错误 | LibTV 节点 runtime `data.params.imageList[]` 重排，prompt 仍按计划顺序解释 `{{Image N}}` | 建节点但不运行 -> 查询 `imageList` -> 用 `node_key + assetId/url` 建 `runtime_image_placeholder_map[]` -> 按 runtime map 自动回写 prompt/queue -> 最终放行查询后运行 | `queried_runtime_image_map_verified=true` 后才允许 `--run` |
| `TM-LIBTVCANVAS-20` | 画布节点 ID 和图片都正确但生成仍角色错位 | 决定性远端检查缺失；`data.params.prompt` 实际含旧 `{{Portrait N}}`、绑定表或执行元数据，本地 prompt 文件与远端节点不一致 | 自动修复可控项：按 runtime map 重写 prompt、清理污染字段、必要时重建左侧输入；最终节点参数、左侧输入和 prompt 写定后，`--run` 前做一次决定性远端查询 | `REV-LIBTVCANVAS-05` 检查远端 prompt，而不是只查本地文件 |
| `TM-LIBTVCANVAS-14` | prompt 里出现执行说明或失败诊断 | handoff / prompt 分层失败 | 诊断移入 manifest / queue / report | prompt hygiene gate |
| `TM-LIBTVCANVAS-15` | 新版 CLI 执行失败但本技能报告已完成 | 混淆计划完成和远端执行完成 | 状态分为 planned / handed_off / executed / blocked | queue record 必须记录执行阶段 |
| `TM-LIBTVCANVAS-17` | 画布上已有准确命名参照图，但实际匹配仍错 | 没有先查询画布 image 节点和设计 manifest，直接用本地生成目录或文件顺序兜底 | 重建匹配链路：画布节点名/ID 前缀 -> 设计 manifest/清单别名 -> active registry -> 本地上传 | manifest 记录每个主体的候选节点、命中依据和排除原因 |
| `TM-LIBTVCANVAS-18` | 新分镜组仍默认提交 `star-video2-fast` | 继承历史任务或示例命令中的 fast 模型 | 改为默认 `model=star-video2`，fast 仅用户显式覆盖 | submit plan / queue / report 记录模型及覆盖原因 |

## Repair Playbook

1. 先判断任务是主体参照流、分镜参照流、查询下载还是修复审查。
2. 默认进入主体参照流；只有用户显式说“分镜参照流”才进入占位路线。
3. 主体参照流先读 `5-分组/第N集.md`，不要回到 `4-摄影` 或重新编写组内容。
4. 主体绑定只认组底 YAML 名称、稳定主体 ID、画布节点名、URL、assetId 和 node_key，不认 UI 随机图片顺序。
5. `{{Image N}}` 是 runtime 占位符，不是计划层占位符；每个新视频节点先按 YAML canonical order 逐张连接主体图，再查询 runtime `data.params.imageList[]` 建立 `runtime_image_placeholder_map[]`，最后只在底部 YAML 主体条目后按 runtime map 写占位，分镜正文保持原样。
5a. 最具决定性的复查对象是 `--run` 前唯一一次远端视频节点查询返回的 `data.params.imageList[] + data.params.prompt`；旧节点里可能残留 `{{Portrait N}}`，即使本地 prompt 文件已经是 `{{Image N}}`。
6. 每条视频任务的时长都从当前分镜组 YAML 读取并 clamp。
7. 真实执行只用 `.agents/skills/cli/libTV` 的新版 `libtv` 命令；不要复制、改写或重建旧会话接口脚本。
8. 默认只报告画布计划、节点计划和执行状态；用户要求下载时再加入 `libtv download`。
9. 同画布 active URL 是主体参照流的默认加速项；不要为了 fresh resolve 重复上传同名主体图。
10. 单组参照图预算超过 9 张时先取舍，不要把超限 payload 交给远端试错。
11. 每组都留下 manifest / submit plan / queue record / CLI handoff plan；执行阶段必须可审计。
12. 若新版 CLI 官方包缺少 `CONTEXT.md`，记录缺口并按 `SKILL.md + commands/*.md` 执行，不要把旧经验层移植过去。
13. 若发现新可复用失败模式，优先写入本文件；稳定成强制规则后再晋升到 `SKILL.md` 或 `references/`。
14. 发现画布节点已规范命名时，先查询画布现有 image 节点；只有画布和 registry 都不能唯一命中，才扫描本地 `6-设计/*/3-生成`。
15. 每次新建视频节点前检查 submit plan 的 `model`；默认必须是 `star-video2`，不要继承上一次实际执行用过的 `star-video2-fast`。

## Reusable Heuristics

- 这个技能的关键价值是“画布语义稳定 + CLI handoff 可审计”，不是替代 LibTV CLI。
- 主体绑定表应使用固定中文名 `主体绑定表`，但只出现在 manifest、submit plan、queue record 和 CLI handoff plan，不进入视频节点 `params.prompt`。
- 最新版 CLI 稳定能力是左侧输入连线和 `{{Image N}}`；不要再把不可验证的 UI `@` 文本当成执行证据。
- 新建视频节点时默认按 canonical order 逐张连接：第一张用 `--left` 建立，后续用 `--left-add` 追加；重跑既有节点时先清理会造成编号漂移的旧输入，再按顺序追加。但 `{{Image N}}` 只能按创建后查询到的 runtime `data.params.imageList[]` 解释，不能按计划 `--left` 顺序解释。
- 新版 `libtv upload` 返回资源节点，active registry 应优先记录 node_key，而不是只保存旧 OSS URL。
- `5-分组` 组正文已经是 prompt 主体；本技能只做运输层组织、主体绑定和参数投影。
- 自动下载对画布流是副作用；默认关闭能减少重复本地文件和错误归档。
- `allow_libtv_prompt_optimization=false` 不是 text2video 开关；它只能约束远端不改写 prompt，不能替代全能参考模式声明。
- 看到 `params.prompt` 里出现执行锁、生成参数、主体绑定表、missing/excluded 状态，基本就是 handoff/prompt 分层失败。
- 视频阶段不是重新写 prompt 的地方。上游已经为 AI 视频稳定性写好的“定场/镜头身份 -> 镜头运动/方向 -> 人物动作 -> 表演微动态 -> 光线结果”顺序，应被运输到远端。
- 对 TMBR 这类中英混合项目，YAML 可能是中文主体名，设计资产和画布节点可能是 `C###` / `S###` / `PROP-###` 英文 canonical 名；匹配时必须先用设计 manifest 和清单文件建立别名桥，再绑定 node key。
- 历史执行报告中的 `star-video2-fast` 是事实记录，不应回写伪造；但新 submit plan 不得把历史 fast 当默认值。
