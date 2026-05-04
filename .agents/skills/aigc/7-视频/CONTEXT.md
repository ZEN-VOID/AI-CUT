# Context: aigc 7-视频

本文件是 `7-视频` 父级入口的经验层知识库。调用同目录 `SKILL.md` 时必须同时加载本文件。它只保存路由经验、修复打法与常见误判，不承载叶子技能的执行细则。

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
| frame visual reference | 用户提到分镜画面图、镜级图、多张图、四段式 `分镜ID`、`6-图像/A-分镜画面` | `A-分镜画面参照` | 核对每个 `shot_id` 是否来自目标分镜组；缺图由叶子处理，不在父级补图 |
| storyboard reference | 用户提到分镜故事板、组级 storyboard、整张故事板图、`6-图像/B-分镜故事板` | `B-分镜故事板参照` | 核对 `group_id` 与故事板图唯一对应；没有故事板图时由叶子决定 text-only |
| subject reference | 用户提到角色、场景、道具、主体参照、组底 YAML、`5-设计/*/3-生成` | `C-主体参照` | 以组底 YAML 为主体槽位真源；不要用正文泛词猜主体 |
| hybrid board subject reference | 用户提到主体参照和分镜故事板参照合二为一、同一 prompt 同时导入主体图和故事板、主体后 `@参照图`、故事板总参照 | `D-主板混合参照` | 故事板只做整组总参照；主体参照必须跟在对应 YAML 主体后 |
| query or download | 用户给 LibTV `sessionId`、queue ledger、videos 目录、查询/下载状态 | 先定位所属叶子 | 通过路径、ledger 文件名、report 或输出目录回推 A/B/C/D |
| repair or review | 用户要求修 prompt、manifest、LibTV batch、队列、下载结果或只审查 | 原所属叶子 | 未定位原所属叶子前不新建另一条路线 |
| ambiguous video | 用户只说“生成视频”且 A/B/C 都可能 | 需要最小澄清或按现有资产最强证据选择 | 优先使用用户点名资产；其次既有输出目录；再其次上游已完成度 |
| local model parameter drift | 未显式指定模型时仍在本地 submit plan 中强塞旧模型参数 | A/B/C/D 叶子 handoff | 改为 `$libTV` 后端默认路由；只有用户显式指定时才把模型要求写入自然语言任务 |
| video filename drift | 下载视频使用 sessionId、provider id 或非 group_id 文件名，导致 `8-审片` 无法回推分镜组 | A/B/C/D 叶子 output contract | canonical 视频名改为 `<group_id>.mp4`；同组多变体用 `<group_id>-a.mp4`、`<group_id>-b.mp4`，sessionId 写 queue/report |

## Repair Playbook

1. 先判断用户要的是参照路线选择、全新视频生成、查询下载、修复审查，还是 A/B/C 对比。
2. 父级只输出路由判断；不要在父级临时写 prompt、YAML、manifest、queue 或 report。
3. 只要用户点名 `分镜画面`、`分镜故事板`、`主体参照` 中任一路线，就直接进入对应叶子，不默认补跑其他路线。
4. 若用户只说“把第 N 集生成视频”，先看是否已有明确视频策略或既有 `7-视频/<叶子>/` 产物；仍不明确时询问最小澄清。
5. query / repair / review 必须尊重既有产物所属叶子；不要因为另一条路线看起来更完整就迁移真源。
6. 若父级发现叶子技能缺失或上下文不可读，报告配置缺口；不要复制其他叶子合同来代替。
7. 若需要上传参照图、创建 LibTV 会话、并发、`sessionId`、下载状态，交给叶子加载 `.agents/skills/cli/libTV`，父级只确认路由。
8. 下载视频进入可审片状态前，必须确认文件名能直接回推 `4-分组` 的 `group_id`；同组变体只能使用小写字母后缀。

## Reusable Heuristics

- `A-分镜画面参照` 的关键词是镜级、四段式 `分镜ID`、多张分镜画面图；它产出组级视频 job，不是单镜视频 job。
- `B-分镜故事板参照` 的关键词是组级、三段式 `group_id`、整张故事板图；它适合用一张组级 storyboard 图约束连续视频。
- `C-主体参照` 的关键词是角色、场景、道具和组底 YAML；它适合在缺少分镜图或更重视主体一致性时使用。
- `D-主板混合参照` 的关键词是故事板总参照 + YAML 主体参照；它适合需要同一组级 prompt 同时锁定整体构图连续性和主体外观一致性时使用。
- A/B/C/D 是互斥候选，不是默认串行阶段；父级不能为了“结构完整”补空目录、空报告或空占位。
- 视频阶段的上游事实主源通常是 `4-分组`；`5-设计` 和 `6-图像` 提供参照资产，不应反向改写分组正文。
- 缺少参照图不一定阻断视频路线；错用参照图、猜测主体、空路径占位、重复提交才是父级需要警惕的路由风险。
- 只要任务涉及实际 prompt 组装、参照路径绑定、LibTV submit plan、queue ledger 或下载，就已经进入叶子技能职责。
- 视频生成未显式指定模型时，父级和叶子都应按 `$libTV` 后端默认路由理解；具体模型选择不在 `7-视频` 本地硬编码。用户显式指定模型时，保留原话进入 LibTV 任务正文。
- 视频文件名是 `7-视频` 和 `8-审片` 之间的主接口；不要把审片依赖绑到 sessionId 或下载顺序上。
