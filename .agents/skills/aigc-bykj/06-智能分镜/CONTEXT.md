# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-bykj/06-智能分镜` 的经验层知识库，不是执行日志。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出、节点、门禁或路径合同；只提供可复用失效模式、修复顺序和执行启发。

## Context Health

- soft_limit_chars: 14000
- hard_limit_chars: 28000
- status: ok
- last_checked_at: 2026-05-29

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 06 被拆回旧 5-摄影/6-分组 runtime | 阶段整合层 | 回到 `output/[项目名]/06-智能分镜/` JSON-first 输出 | `SKILL.md` 固定旧能力只作为内部细部模块 | 不写 `projects/aigc/<项目名>/5-摄影/6-分组/` |
| 规则同步被误解为路径同步 | 规则/路径边界层 | 保留 BYKJ 输出路径，只把 group/bridge/statistics 内容规则全量同步原 `6-分组` | `AIGC 6-分组 Rule Synchronization Contract` 明确同步规则不是同步路径 | 输出仍在 `06-智能分镜`，但 group/bridge 字段完整镜像原规则 |
| 分镜只是复述剧本动作 | 摄影决策层 | 补 `shot_function`、camera、lighting、attention、handoff | `PASS-06-04` 固定非复述型摄影决策门 | 删除源句事实后仍能读出镜头如何看 |
| frame ID 不稳定 | ID 规范层 | 重建四段式 `episode-scene-group-frame` | `PASS-06-05` 固定 ID 门 | `镜头列表.json` 全部 ID 可解析 |
| 角色/道具/场景无证据漂移 | 资产引用层 | 回到 `05R/05` 资产索引或 `03` 剧本证据 | `asset_refs` 必须回指上游 | report 有 `asset_style_alignment` |
| prompt 好看但不可视频生成 | AI 稳定层 | 改成 camera-first，补方向参照、光线结果、微动态 | 吸收 `5-摄影` AI 视频稳定性规则 | `generation_payload.ai_video_stability_notes` 非空 |
| group 按字数或情绪硬切 | 分组边界层 | 回到 frame 时长累计和 atomic unit 完整性 | 吸收 `6-分组` 约 15 秒、18 秒硬上限规则 | `groups[].duration_seconds <= 18` |
| group 缺定场和构图账本 | 生产组身份层 | 补 `establishing_shot` 与六分区 ledger | `PASS-06-07` 阻断缺失 | 每组 left/center/right/foreground/midground/background 完整 |
| group 只保留简化 JSON stats | 原 6-分组规则缺失层 | 补场景标题、定场镜头、画面构图、六分区、画面属性、三项风格行、group_body、五项 YAML 等价统计和计数边界 | group schema 必须镜像原 `6-分组` 输出模板 | `group_rule_sync_check` pass |
| bridge 变成新剧情或尾钩 | 连接件边界层 | 改为上一组尾帧到下一组首帧 3-4 秒缝合过程 | `PASS-06-08` 固定连接件不新增事实 | bridge 只有过程、运动、运镜、透视适应 |
| bridge 字段被压缩为一句 transition | 原连接件规则缺失层 | 补连接件标题等价、场景标题行、三项风格行、连接类型、连接方法、时长、变化过程、主体运动、运镜设计、透视适应、避免元素和禁用字段 | bridge schema 必须镜像 `bridge-shot-contract.md` | `bridge_rule_sync_check` pass |
| 风格词随机堆叠 | 04 消费层 | 回读 `04R/04` 风格，按当前 group/frame 投影 | style projection 必须回指全局预设 | `style_projection` 不脱离项目风格 |
| 普通道具抢焦点 | 道具准入层 | 删除或降级无互动道具镜头 | 吸收 `5-摄影` 道具镜头准入规则 | `props` 只保留重要叙事/生成锁定物 |

## Repair Playbook

1. 先锁定 `03` 集稿、`04/04R` 风格和 `05/05R` 资产；缺任一类先记录降级，不直接伪造。
2. 分镜前先建立 visual unit，不要从场景摘要直接跳到 frame prompt。
3. 每个 frame 先问“这镜删除后损失什么”：信息、关系、动作结果、情绪压力、观看发现或交出锚点。
4. 每个 frame 的 prompt 必须从摄影决策推导；不要从资产设计直接拼图像提示词。
5. 对话场景先判断说话者/听者/空间压力/观众知情层级，不机械正反打。
6. 情绪强变化优先正面近景、正面双眼特写、慢推或可见微动态，不用快速复杂环绕抢表演。
7. 道具镜头必须通过互动、证据、规则、危险源或必要环境交代任一准入条件。
8. 分组前先累计 frame `duration_seconds`，保持 visual unit 的 atomic 完整；超过 18 秒必须重裁。
9. group 规则同步是内容规则同步，不是路径同步；不要把 BYKJ 输出路径改回旧 `projects/aigc/<项目名>/6-分组/`。
10. group 定场镜头不是摘要剧情，而是给下游生成看的空间身份、主体站位、光色材质和构图账本；必须保留原 `6-分组` 的场景标题、定场、构图、六分区、画面属性、三项风格行、正文和统计完整规则。
11. bridge 等下一个 group 首帧明确后再写；只描述中间过程，不复述端点，不新增剧情，并完整保留原连接件字段形态。
12. 输出前检查四段式 ID、资产引用、style projection、frame->group->bridge 索引是否可互相解析，同时检查 `group_rule_sync_check` 与 `bridge_rule_sync_check`。

## Reusable Heuristics

- BYKJ `06` 的核心不是“先 5 再 6 复制一遍”，而是把摄影决策和生产分组落成同一套可消费 JSON；但其中生产分组的内容规则必须完整继承原 `6-分组`。
- `5-摄影` 贡献的是镜头语言密度，`6-分组` 贡献的是生产单元边界；两者在 `06` 中的交汇点是 frame duration 和 group atomic unit。
- 用户说“同步原 6-分组”时，优先理解为同步输出内容规则和审查规则，不是同步旧输出路径。
- JSON-first 不是简化规则。原 `6-分组` 的 Markdown 结构要以 JSON 等价字段完整承载：标题、场景标题、定场、构图、六分区、画面属性、三项风格行、正文、统计、连接件。
- 好的 frame 不是把动作写漂亮，而是让下游知道摄影机站在哪里、怎么动、看什么、何时停、交给什么。
- 好的 group 不是把 frame 装满 15 秒，而是可以独立生成：起始空间清楚、主体站位清楚、风格清楚、时长不过载、尾帧能连接。
- 旧 `north_star` 在 BYKJ 中应由 `04/04R` 全局预设承担；不要要求 BYKJ 项目必须存在 `0-初始化/north_star.yaml`。
- 资产引用要保守：角色、场景、道具 ID 比漂亮描述更重要；无法确定 ID 时先写 `unresolved_ref` 并报告。
- 如果局部分镜缺少 `04/05` 上游，只能标记 `draft_storyboard`，不能假装已可进入正式图像/视频阶段。
