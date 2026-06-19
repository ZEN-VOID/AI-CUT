# Context: libTV画布流

本文件是 `libTV画布流` 的经验层。它不重定义 `SKILL.md`、`references/` 或 LibTV CLI 命令真源。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 16000
hard_limit_chars: 32000
status: ok
```

## Type Map

| type_id | symptom | likely cause | immediate fix | verification |
| --- | --- | --- | --- | --- |
| `LTVCTRL-TM-01` | YAML 已有 UUID 但视频主体错绑 | 把 `{{Image N}}` 当作 YAML 顺序，而远端 `imageList` 顺序不同 | 本地先写 `图片N 主体名 UUID`，提交 prompt 时重排为 `图片N 主体名 {{Image N}} UUID`，再直接写 `imageList/mixedList` 为同顺序 | 查询节点 `data.params.imageList[]` |
| `LTVCTRL-TM-02` | 逐张 `--left-add` 后顺序仍不变 | LibTV 入边变更未重算 `params.imageList` | 连线后再次写入 `imageList/mixedList/imageListOrder/mixedListOrder` | final query 顺序等于 YAML |
| `LTVCTRL-TM-03` | 道具和场景复用同一图片 | 同一 UUID 出现在多条主体行 | 同组内相同 UUID 复用同一个 `图片N` | YAML 和 runtime map 都只占一个图位 |
| `LTVCTRL-TM-04` | 同一项目空间下画布重名 | 只按 `项目名-第N集` 查重，未区分 `projectSpaceId/folderId` 和画布名 | 先锁定 `projectSpaceId/folderId`，默认画布名用 `第N集`，冲突追加 `V2`、`V3`；无法锁定项目空间时才退回旧兼容命名 | project list 中 `uuid` 不重复，目标条目的 `projectSpaceId/folderId` 与报告一致 |
| `LTVCTRL-TM-05` | prompt 出现绑定表、命令或诊断 | handoff 文案进入视频 prompt | 重写 prompt，只保留分镜组正文 + fenced YAML | 远端 prompt hygiene pass |
| `LTVCTRL-TM-06` | 远端 prompt 看似不同但只替换 `group_id`、主体名或 `{{Image N}}` | scripted prompt projection | 标记 `FAIL-LTVCTRL-SCRIPTED-PROMPT`，恢复直接使用完整分镜组正文 + fenced YAML | final query prompt 可回指完整组正文，而不是模板句 |
| `LTVCTRL-TM-07` | 用户要求重生成已存在分镜组，执行器却跳过或覆盖旧节点 | 把分镜组 ID 当作视频节点唯一键 | 为同一 `source_group_id` 创建新的 `video_node_instance_id`，默认递增 `batch_no`；二修递增 `revision_no` 并记录父实例 | registry 中同一 source_group_id 有多个 instances，旧节点仍可查询 |
| `LTVCTRL-TM-08` | `libtv node --left-add` 对已经存在的入边长时间无返回 | 对同一视频节点重复追加同一 image edge | 不对已存在边重复执行 `--left-add`；创建时一次性带有序入边，随后直接重写 `imageList/mixedList` 并以 final query 为准 | final query 的 `data.params.imageList[]` 等于 YAML 顺序 |
| `LTVCTRL-TM-09` | 创建视频节点报 `图片最多 9 个` | 单组绑定图片超过 LibTV 当前视频节点输入上限 | 前置裁剪到 9 张：优先保留用户强指定的多维主角参照、所有关键角色和场景，再在容量内保留道具；被裁掉主体回写为未绑定文本并记录 skip reason | create 成功且 manifest/queue 记录被裁剪主体 |
| `LTVCTRL-TM-10` | 单组 YAML 修复后相邻分组标题消失或 prompt 夹带下一组正文 | 用局部 fragment 的 offset 回写全局 markdown，替换范围跨过 fence 边界 | 只用全局 regex span 或结构化 markdown block 边界替换；回写后立即校验 `^##` 分组数、每组 fenced YAML 可解析、目标 prompt 不含相邻 `group_id` | source group count 与原始计划一致，目标 final prompt 不含相邻分组标题 |
| `LTVCTRL-TM-11` | 视频规格时长被整数化，或应保留的 `.5` 秒丢失 | 把 LibTV schema `duration.step=1` 误解为只能整数秒，或用 `ceil` / `round` / `parseInt` 处理分镜组 `时长估算` | 保留分镜组 `时长估算` 或用户覆盖的小数值；若项目策略要求半秒尾帧缓冲，仅在结果仍处于 LibTV `4–15` 秒范围内对整数时长 `+0.5s`，否则保持边界值并记录原因；同步 queue record、submit plan、summary/report 和远端 `settings.duration` | 本地 queue/submit/report 与远端 final query 的 `duration` 一致，`.5` 未被整数化，且所有值在 `4–15` 秒范围内 |
| `LTVCTRL-TM-12` | 用户觉得画布节点数多于分组稿 | 目标画布执行前已有旧 video 节点，且本轮未获删除授权所以保留 | 预检时区分 `current_batch_video_nodes`、`legacy_video_nodes` 和 `reference_image_nodes`；最终汇报必须说明旧节点数量和名称前缀，避免误读为本轮多建 | remote node list 中本轮节点数等于分组数，legacy 节点单独列示 |
| `LTVCTRL-TM-13` | `mixed2video` 视频节点用 `--prompt` 写入后，远端 prompt 把 YAML 主体行的 `{{Image N}}` 自动改成 `{{Mixed N}}` | CLI 写入路径对 mixed 输入占位符做了自动规范化，但画布流 prompt hygiene 仍要求 YAML 主体行保留 `{{Image N}}` | 创建节点后用 `libtv node <node> -s prompt="$(< prompt.txt)"` 重写 prompt，再 final query；若仍被服务端规范化，记录为 runtime normalization 并以 `imageList/mixedList` 顺序为完成证据 | final query 中无 `{{Portrait N}}`，YAML 主体行占位符符合合同或报告记录服务端规范化原因 |
| `LTVCTRL-TM-14` | 创建 video 节点时报 `params.settings.enableSound=true 不在允许范围。可选: on, off` | LibTV video schema 的 `enableSound` 是枚举字符串，不接受布尔值 | 在 `settings` 中写 `enableSound:"on"` 或 `enableSound:"off"`；不得写 `true/false` | create/update 成功，final query 的 `data.params.settings.enableSound` 为 `on` 或 `off` |
| `LTVCTRL-TM-15` | 用户要求多分镜参照模式，但视频 prompt 只有连续段落或 YAML，没有逐个分镜明细 | prompt 虽引用了所有 `{{Image N}}`，但没有把每张分镜图落实为显式编号动作段，降低多分镜可审计性 | 在 prompt 主体中加入 `分镜段 01...` 的逐段明细，每段写明参照图名、`{{Image N}}`、构图/动作/运动承接；更新远端节点后重新 final query | 本地与远端 prompt 中分镜段数量等于分镜参照图数量，且 `imageList/mixedList` 顺序不变 |
| `LTVCTRL-TM-16` | `--run` 返回 `参考图可能包含真人形象`，但再次提交同一节点仍失败 | CLI 自动合规只把 `assetId` 或 `compliantExempt` 写回 `imageList`，`mixed2video` 实际提交仍依赖未同步的 `mixedList` | 从失败返回的 `params.imageList[]` 中按 `nodeId` 复制 `assetId/compliantExempt` 到 `mixedList[]`，同时保持 `mediaType:"image"` 和原顺序，再重写节点参数后重试 | final query 中 `imageList/mixedList` 同一 `nodeId` 均带合规字段；重试 queue record 成功或明确记录阻塞 |
| `LTVCTRL-TM-17` | 报告有上传清单和 queue record，但缺少上游如何导向视频节点的说明 | 上游方向继承缺失 | 补 `LibTV Upstream Video Direction Matrix`，把完整分镜组正文、YAML 图片顺序、主体/图像参照、项目约束和 LibTV 限制映射到 prompt、imageList、settings、run boundary 和 final query | `GATE-LTVCTRL-UPSTREAM-DIRECTION` 通过；矩阵不是上传清单，而是节点决策证据 |
| `LTVCTRL-TM-18` | Skill 包有完整目录，但最新版 validator 拒绝 `steps/`、缺 runtime-spine blocks 或缺 `test-prompts.json` | 旧步骤文件仍承载节点真源，`SKILL.md` 没有可解析业务分析、模块触发、收敛和评估资产 | 将 N1-N9 节点、Mermaid、gate 和 route 收回 `SKILL.md`；删除 `steps/`；补 `test-prompts.json` 和 Module Trigger Matrix | `validate_skill_2_0.py --mode delivery` 与 `smoke_test_skill_2_0.py --mode delivery` 通过 |

## Repair Playbook

1. 先确认本轮是 `full_canvas_control`、`backfill_only`、`node_rebuild_only` 还是 `repair_order`。
2. 对已有视频节点错序，优先删除重建；若不能删除，则清边、逐张连线、再直接重写 `imageList/mixedList`。
3. 所有 `{{Image N}}` 都必须来自本地 YAML `图片N` 和 final remote query 的双重一致性，不来自上传顺序、画布布局或 CLI 参数顺序。
4. 缺图主体跳过回刷，不写负面占位，不把相邻主体图拿来代替。
5. 每次执行后更新 `queue-record.json`，状态必须区分 `created_not_run`、`run_executed`、`blocked`。
6. prompt hygiene 不只查污染词，也要查伪差异；如果多节点 prompt 的差异主要来自锚点替换，不能进入生成。
7. 同一分镜组重新生成时先查询 active registry 和远端节点名，生成下一个 `vid__<source_group_id>__bNNN__rNN__vNNN`；不得因为同组已有实例而跳过。
8. 如果 create 命令已经把图片节点连入 video 节点，后续不要再次对同一入边执行 `--left-add`；重复追加既有边可能卡住 CLI。需要修正顺序时直接重写 `imageList/mixedList/imageListOrder/mixedListOrder`，再 final query。
9. 单个 video 节点当前按 9 张图片输入上限处理；计划阶段若 `ordered_subjects` 超过 9，必须先裁剪并记录被裁剪主体，不要等远端 create 失败后才发现。
10. 任何单组 YAML 边界修复后，必须先本地验证 `^##` 分组数量、所有 fenced YAML 可解析、目标 prompt 不含前后相邻 `group_id`，再写远端节点；不得用未验证的 prompt 覆盖 LibTV 节点。
11. 视频规格时长归一时，优先保留分镜组 `时长估算` 或用户覆盖值中的小数；不要因为 LibTV schema `step=1` 就取整。若采用半秒尾帧缓冲，只对仍能留在 `4–15` 秒范围内的整数时长追加 `0.5` 秒，例如 `13.0 -> 13.5`；`15.0` 保持 `15.0` 并记录 `max_duration_bound`，低于 `4.0` 的值先抬到模型下限再记录原因。同步本地证据后必须重新扫描所有 queue record 和远端 final query。
12. 复用已有画布时，执行前后都要按名称前缀统计远端 video 节点：本轮 `vid__<episode>-*`、历史遗留、图片参照分别报告。没有用户明确删除授权时，旧 video 节点必须保留，但最终汇报不能只报总节点数。
13. 对 `mixed2video` 节点，如果 create 阶段使用 `--prompt` 导致远端把 `{{Image N}}` 改为 `{{Mixed N}}`，不要误判为用户 prompt 写错；先用 `-s prompt=` 重写并重新 final query，再决定是否记录服务端规范化。
14. 对 video 节点声音开关，`enableSound` 按 LibTV schema 写枚举字符串 `on/off`；不要用 JSON boolean。若计划层使用布尔值，应在 CLI 提交前归一为 `on/off`。
15. 多分镜参照模式下，prompt 不能只用一段连续 prose 概括多张图；必须有逐段编号的分镜明细，并在每段内同时出现分镜图名、`{{Image N}}`、动作细节和与前后段的承接关系。
16. 对 `mixed2video` 节点触发真人参考图合规失败后，不要只接受 CLI 自动更新后的 `imageList`；必须把同一合规字段同步进 `mixedList` 后再重试，否则后端可能继续按未合规的 mixed 输入失败。
17. `LibTV Upstream Video Direction Matrix` 要和 final query 绑在一起看：prompt 主体、YAML `图片N`、`imageList/mixedList`、settings、run authorization 都要有远端证据锚点；只有本地计划没有 final query 证据不能判 pass。
18. 若 Skill 2.0 元规范升级，优先检查目标包是否仍有 `steps/`、缺 `Module Trigger Matrix`、缺 `Convergence Contract` 或缺 `test-prompts.json`。修复时先把节点真源收回 `SKILL.md`，再同步 README、type map、template 和脚本边界。

## Reusable Heuristics

- 最稳顺序锁定是四件套：`图片N` YAML、逐张 `--left-add`、`params.imageList/mixedList` 直接写入、final query 验证。
- 本地分组稿里 `图片N` 是给人和脚本看的既定顺序；远端 prompt 里 `{{Image N}}` 是 LibTV 模型实际消费的编号。两者必须在最终查询时一致。
- 在正确项目空间下创建新画布比在旧污染画布上修复节点更稳；旧节点可保留证据但不应继续作为新生成真源。
- `projectUuid` 是具体画布 UUID；`projectSpaceId/folderId` 是上层项目空间线索。执行 `libtv upload/node/group` 时只传画布 UUID。
- 本地 `projects/aigc/<项目名>/第N集` 是 AIGC 项目到 LibTV 画布的语义映射，不是输入文件路径；输入文件看 `8-分组/第N集.md`，证据目录看 `10-画布/libTV画布流/第N集/`。
- 默认视频规格使用 `star-video2 / mixed2video / 16:9 / 720p`；用户显式指定模型、模式、画幅或分辨率时覆盖对应默认值。
- LibTV prompt 的稳定做法是“完整组稿直入 + YAML 主体行重排为 `图片N 主体名 {{Image N}} UUID`”；脚本只负责把 `{{Image N}}` 对齐，不负责把组稿改写成新正文。
- 节点身份要两层存储：`source_group_id` 用于追溯上游分镜组，`video_node_instance_id` 用于远端节点名、证据文件名和 queue record 唯一键。
- 当用户要求主角多图参照且同组还有多名角色、场景和道具时，先计算图片槽位预算。若超过 9 张，角色和场景优先于道具；任何被裁掉的已知道具必须保留原 YAML 文本并在 manifest/queue/report 中说明是 `libtv_video_max_9`，不得静默丢失。
- 多分镜参照节点的最低 prompt 形态是“总体招式/场景说明 + 编号分镜段明细 + 连续运动总约束 + 声音/负面约束 + fenced YAML”。仅在 YAML 中列出分镜图不等于已经落实分镜明细。
- `steps/` 对最新版 runtime-spine 是结构性风险；节点表、route、gate 和 Mermaid 图必须留在 `SKILL.md`，reference 只保留长细则和 gate mapping。
