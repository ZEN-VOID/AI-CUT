# Context: aigc 9-视频

本文件是 `9-视频` 父级入口的经验层知识库。调用同目录 `SKILL.md` 时必须同时加载本文件。它只保存路由经验、修复打法与常见误判，不承载叶子技能的执行细则。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 12000
hard_limit_chars: 24000
status: ok
last_checked_at: 2026-04-26
```

## Type Map

| type | symptom | route | repair |
| --- | --- | --- | --- |
| frame visual reference | 用户提到分镜画面图、镜级图、多张图、四段式 `分镜ID`、`8-图像/A-分镜画面` | `A-分镜画面参照` | 核对每个 `shot_id` 是否来自目标分镜组；缺图由叶子处理，不在父级补图 |
| storyboard reference | 用户提到分镜故事板、组级 storyboard、整张故事板图、`8-图像/B-分镜故事板` | `B-分镜故事板参照` | 核对 `group_id` 与故事板图唯一对应；没有故事板图时由叶子决定 text-only |
| subject reference | 用户提到角色、场景、道具、主体参照、组底 YAML、`7-设计/*/3-生成` | `C-主体参照` | 以组底 YAML 为主体槽位真源；不要用正文泛词猜主体 |
| hybrid board subject reference | 用户提到主体参照和分镜故事板参照合二为一、同一 prompt 同时导入主体图和故事板、主体后 `@参照图`、故事板总参照 | `D-主板混合参照` | 故事板只做整组总参照；主体参照必须跟在对应 YAML 主体后 |
| query or download | 用户给 LibTV `sessionId`、queue ledger、videos 目录、查询/下载状态 | 先定位所属叶子 | 通过路径、ledger 文件名、report 或输出目录回推 A/B/C/D |
| repair or review | 用户要求修 prompt、manifest、LibTV batch、队列、下载结果或只审查 | 原所属叶子 | 未定位原所属叶子前不新建另一条路线 |
| ambiguous video | 用户只说“生成视频”且 A/B/C 都可能 | 需要最小澄清或按现有资产最强证据选择 | 优先使用用户点名资产；其次既有输出目录；再其次上游已完成度 |
| local model parameter drift | 未显式指定模型时仍在本地 submit plan 中强塞旧模型参数 | A/B/C/D 叶子 handoff | 改为 `$libTV` 后端默认路由；只有用户显式指定时才把模型要求写入自然语言任务 |
| video filename drift | 下载视频使用 sessionId、provider id 或非 group_id 文件名，导致 `10-审片` 无法回推分镜组 | A/B/C/D 叶子 output contract | canonical 视频名改为 `<group_id>.mp4`；同组多变体用 `<group_id>-a.mp4`、`<group_id>-b.mp4`，sessionId 写 queue/report |
| duplicate LibTV canvas | 同一 `projects/aigc/<项目名>/` 多次调用 `$libTV` 却生成多个 projectUrl / 画布 | 项目级画布 registry 缺失或未读 | 先读 `projects/aigc/<项目名>/9-视频/libtv-canvas-registry.json`；缺失时从 A/B/C/D queue/results/report 反建；已有 `canonical_sessionId` 时复用 |
| remote task type drift | LibTV 远端把 A/B/C/D 直接生视频解释成先做分镜图、故事板图、主体图、拆段或合成 | 目标叶子 handoff 口径过弱 | 所有 `*-libtv-submission.txt` 首行固定 `【LibTV 调用锁定】`；具体 `modeType` 与参照字段由 A/B/C/D 叶子合同定义 |
| subject reference mismatch | 用户指出 prompt 主体名称和引用参照图对不上，或要求 LibTV 端实际传入图必须匹配 YAML `@/uploaded_url` 对应名称 | `C-主体参照` 槽位注册 / 匹配机制缺失 | 交给 C 叶子用 `asset_uploads` 注册 `yaml_name -> uploaded_url`，用 `generation_slots` 注册 `reference_index / mixedList[n] -> uploaded_url -> yaml_name`；父级只确认这是 C 路线源层问题 |
| reference identity mismatch | 用户指出 A/B/D 中分镜ID、故事板总参照或混合参照身份和传入图对不上 | 对应叶子槽位注册 / 同步器缺失 | A 用 `frame_uploads + generation_slots`，B 用 `storyboard_uploads + generation_slots`，D 用 `asset_uploads + generation_slots`；提交前必须运行叶子 `build-upload-ledger.py --sync` 或等价同步器 |

## Repair Playbook

1. 先判断用户要的是参照路线选择、全新视频生成、查询下载、修复审查，还是 A/B/C 对比。
2. 父级只输出路由判断；不要在父级临时写 prompt、YAML、manifest、queue 或 report。
3. 只要用户点名 `分镜画面`、`分镜故事板`、`主体参照` 中任一路线，就直接进入对应叶子，不默认补跑其他路线。
4. 若用户只说“把第 N 集生成视频”，先看是否已有明确视频策略或既有 `9-视频/<叶子>/` 产物；仍不明确时询问最小澄清。
5. query / repair / review 必须尊重既有产物所属叶子；不要因为另一条路线看起来更完整就迁移真源。
6. 若父级发现叶子技能缺失或上下文不可读，报告配置缺口；不要复制其他叶子合同来代替。
7. 若需要上传参照图、创建 LibTV 会话、并发、`sessionId`、下载状态，交给叶子加载 `.agents/skills/cli/libTV`，父级只确认路由。
8. 下载视频进入可审片状态前，必须确认文件名能直接回推 `6-分组` 的 `group_id`；同组变体只能使用小写字母后缀。
9. 每次进入 A/B/C/D 叶子前，先解析项目级 `libtv-canvas-registry.json`；缺失时不要急着新建画布，先扫描既有队列和结果记录里的 `sessionId/projectUuid/projectUrl`。
10. 若 registry 中已有 `canonical_sessionId`，默认把它传给叶子用于 `create_session.py --session-id`；只有用户要求新画布、session 明确失效，或 registry 无法反建时才允许首个叶子创建新 session 并回写 registry。
11. 若远端代理反馈要先做图或拆段，优先检查原叶子的 `*-libtv-submission.txt` 是否缺少 `【LibTV 调用锁定】` 或混入本地路径；不要在父级改写路线或临时补跑另一个叶子。

## Reusable Heuristics

- `A-分镜画面参照` 的关键词是镜级、四段式 `分镜ID`、多张分镜画面图；它产出组级视频 job，不是单镜视频 job。
- `B-分镜故事板参照` 的关键词是组级、三段式 `group_id`、整张故事板图；它适合用一张组级 storyboard 图约束连续视频。
- `C-主体参照` 的关键词是角色、场景、道具和组底 YAML；它适合在缺少分镜图或更重视主体一致性时使用。
- `D-主板混合参照` 的关键词是故事板总参照 + YAML 主体参照；它适合需要同一组级 prompt 同时锁定整体构图连续性和主体外观一致性时使用。
- A/B/C/D 是互斥候选，不是默认串行阶段；父级不能为了“结构完整”补空目录、空报告或空占位。
- 视频阶段的上游事实主源通常是 `6-分组`；`7-设计` 和 `8-图像` 提供参照资产，不应反向改写分组正文。
- 缺少参照图不一定阻断视频路线；错用参照图、猜测主体、空路径占位、重复提交才是父级需要警惕的路由风险。
- 只要任务涉及实际 prompt 组装、参照路径绑定、LibTV submit plan、queue ledger 或下载，就已经进入叶子技能职责。
- 视频生成未显式指定模型时，父级和叶子都应按 `$libTV` 后端默认路由理解；具体模型选择不在 `9-视频` 本地硬编码。除非用户显式要求其他规格，否则基础输出默认 720P、15 秒、16:9；用户显式指定模型、时长、比例、分辨率或质量档时，保留原话进入 LibTV 任务正文。
- 视频文件名是 `9-视频` 和 `10-审片` 之间的主接口；不要把审片依赖绑到 sessionId 或下载顺序上。
- `## x-y-z~x-y-z` 连接件默认不属于 A/B/C/D 视频路线的 job 范围；遇到连接件时跳过，不生成 `<上组~下组>.mp4`，也不把连接件拼进相邻分镜组 prompt。连接件视频留给未来手动视频连接 skill。
- LibTV 远端当前不是按本地项目名自动找画布；可靠复用来自本地 registry 里的 `canonical_sessionId`。只有 `projectUuid/projectUrl` 而没有 sessionId 时，不要声称能强制复用指定画布。
- `【LibTV 调用锁定】` 是远端画布的第一行保险：父级只要求所有 A/B/C/D 提交都有这行，叶子负责锁定专属 `modeType`、参照字段和 uploaded URL 用法。
- 参照图的最终匹配不是“prompt 里有 URL”或“submit plan 顺序看起来一致”，而是目标叶子的槽位注册表证明 LibTV 端实际传入的 URL 与 prompt YAML 中的分镜ID、故事板身份或主体名称同槽对应；父级遇到这类投诉时先回原叶子同步器，不跨路线重做。
