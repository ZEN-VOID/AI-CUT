# Context: libTV画布流

本文件是 `aigc/9-视频/libTV画布流` 的经验层知识库，不重定义 `SKILL.md` 的入口合同。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 16000
hard_limit_chars: 32000
status: ok
last_checked_at: 2026-05-12
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 预防检查 |
| --- | --- | --- | --- | --- |
| `TM-LIBTVCANVAS-01` | 用户没有指定路线但任务涉及角色/场景/道具参照出视频 | 默认路线不明确 | 使用 `subject_reference_flow` | `types/type-map.md` 默认包必须指向主体参照流 |
| `TM-LIBTVCANVAS-02` | 主体名称和图片不匹配 | 依赖了随机 `Image N` 或画布框体顺序 | 重建 `主体绑定表: yaml_name -> node_key -> URL` | 远端消息必须声明绑定表是唯一真源 |
| `TM-LIBTVCANVAS-03` | 所有视频都生成 15 秒 | 未读取组底 YAML `时长估算` | 重新提取并按 4-15 秒 clamp | submit plan 必须记录 duration source |
| `TM-LIBTVCANVAS-04` | 生成后本地目录出现非显式下载文件 | 沿用了官方 CLI 自动下载旧习惯 | 删除默认下载步骤，仅保留画布结果 | `download=false` 是本技能默认策略 |
| `TM-LIBTVCANVAS-05` | 画布素材显示为 `素材图片` | 只创建 resource node 未改节点名 | 用节点更新能力按原文件名修正 | 资产上传后检查 node name / data.name |
| `TM-LIBTVCANVAS-06` | 分镜参照流被误执行 | 占位路线被当作已实现 | 返回 `not_implemented_placeholder` | 类型包和 references 都标注空白占位 |
| `TM-LIBTVCANVAS-07` | 远端 Agent 重写、压缩或优化 `6-分组` 正文 | 未锁定 `allow_libtv_prompt_optimization=false` | 重提并明确禁止远端优化，除非用户显式 opt-in | submit plan、queue、report 必须记录 opt-in 状态 |
| `TM-LIBTVCANVAS-08` | 主体列表比 YAML 多，混入正文泛词 | 用正文子串或猜测名扩展主体 | 丢弃非 YAML 主体，只用组底 `角色 / 场景 / 道具` | review gate 检查 YAML subject baseline |
| `TM-LIBTVCANVAS-09` | 批量任务重复上传同画布已有主体图 | 忽略 active URL 复用策略 | 优先复用同 projectUuid 下同 YAML 名 active URL | 只有缺 URL、歧义、替换/更新才上传 |
| `TM-LIBTVCANVAS-10` | 单组参照图超过 LibTV 预算 | 未做 9 图预算裁决 | 角色和场景优先，道具先排除，无法压缩则阻断 | `images[] / mixedList <= 9` |
| `TM-LIBTVCANVAS-11` | active URL 复用口径随执行者变化 | 缺少 registry 真源和主键 | 使用 `libtv-canvas-active-registry.json` 与 `projectUuid::category::yaml_name` | 同名 active 只能有一条，替换时旧记录 inactive |
| `TM-LIBTVCANVAS-12` | `.env` 自动加载只停留在文档口径 | 直接调用官方脚本时未加载环境 | 通过 `run_libtv_with_env.py` 转官方脚本 | wrapper 只加载环境和 allowlist，不改官方逻辑 |
| `TM-LIBTVCANVAS-13` | 提交的视频节点提示词没有主体参照图 URL，表现为纯文生视频 | 只写了主体绑定意图，没有显式锁定“全能参考 / 多图主体参考生成视频”，或参考图审核失败后静默 text2video fallback | 阻断并重建提交：远端消息必须含真实 `URL + node_key + yaml_name + 用途`；审核失败则记为 `reference_asset_review_failed` | 有可用参考图时不得 text2video；无用户显式授权不得纯文生 fallback |
| `TM-LIBTVCANVAS-14` | 远端 prompt 头部出现 `本轮不提交任何参考图 URL` 等执行说明 | 把队列诊断或 fallback 备注泄漏进创作 prompt | 删除诊断句，移入 manifest / submit plan / queue / report；重新提交干净 prompt | prompt hygiene gate 检查负面占位句和内部诊断语 |
| `TM-LIBTVCANVAS-15` | 远端 prompt 头尾重复 StyleBible、声音约束或出现 `其中，...` 复述段 | 把提交前摘要、项目风格摘要和分镜组正文重复拼接 | 使用干净 `params.prompt` 结构；分镜组正文已有风格/声音时不再追加 StyleBible/audio | review gate 检查重复风格、重复声音和尾部复述 |
| `TM-LIBTVCANVAS-16` | 组底 YAML 的角色/场景/道具没有进入视频节点 prompt | 只把 YAML 用于时长或本地计划，没有保留完整 YAML | `params.prompt` 底部完整保留 fenced YAML，并在已绑定主体名后插入对应画布 `@` 资产引用；绑定表只写 handoff/evidence | prompt 必须含完整 YAML，且不得把 YAML 降级成摘要主体清单 |
| `TM-LIBTVCANVAS-17` | prompt 用“令狐冲为男性武侠人物”等泛化身份替代参考绑定 | 主体缺图或审核失败后用文本补洞 | 阻断或记录 missing；已绑定主体必须用 URL/node_key，不用泛化身份替代 | 泛化主体替代句进入 forbidden list |
| `TM-LIBTVCANVAS-18` | 只写“全能参考”但没有传标准 `modeType`，或 plan/queue/prompt 中模式名不一致 | 把业务口径误当 LibTV 官方字段 | 统一写入 `modeType=mixed2video`；用户指定模式时归一为标准称谓 | `modeType` 只能是 type-map 标准表中的 6 个值 |
| `TM-LIBTVCANVAS-19` | `allow_libtv_prompt_optimization=false` 已记录，但远端实际 `params.prompt` 仍被压缩改写或混入执行元信息 | 只把 false 当结构字段，或把 handoff message 整段塞进 prompt | 在 handoff message 写入提示词锁定句，禁止优化/重排/摘要/压缩/改写/补镜头，并要求 `params.prompt` 严格等于“分镜组正文 + 完整 YAML” | review gate 检查字段和自然语言锁定同时存在；查询后检查 `params.prompt` 干净且保真 |
| `TM-LIBTVCANVAS-20` | 多主体视频按上传图片顺序错配主体 | 远端依赖 `Image N` / `imageList` 顺序而不是主体名绑定 | 在分镜组原文主体名后插入 LibTV 画布 `@` 资产引用 / node mention（标准名称待官方确认），并声明 `@` 引用与 `主体绑定表` 优先于图片顺序 | review gate 检查 `@` 引用来自 `主体绑定表` 的 `canvas_node_name/node_key/URL`，且不是普通文本伪造；无法验证时记录 `at_asset_mention_unverified` |
| `TM-LIBTVCANVAS-21` | `params.prompt` 里出现执行锁、生成参数、主体绑定表、missing/excluded 原因等大量废信息 | 混淆 handoff message 与视频节点创作 prompt | 重建分层提交：handoff 放执行与绑定，`params.prompt` 只放分镜正文 + 完整 YAML + 主体 `@` 引用 | 查询 `create_generation_task.params.prompt`，出现执行锁/绑定表/诊断即判 `remote_prompt_rewritten_or_polluted` |
| `TM-LIBTVCANVAS-22` | 同一主体在同一视频任务中重复提交两张同义主体图 | 没有按 YAML 主体去重，active 图与新上传图同时进入 imageList | 按 `projectUuid + category + yaml_name` 去重，默认每主体只保留一张 active/最新可信图 | 除非用户显式要求多视图或多版本对比，否则 `imageList` 不得含同主体重复图 |
| `TM-LIBTVCANVAS-23` | 视频节点按图1/图2顺序把 URL 错绑到主体 | `imageList` 使用上传顺序或文件扫描顺序，且远端按数组下标解释主体 | 按 YAML `角色` -> `场景` -> `道具` 展示顺序生成 canonical reference order，并按该顺序构造 `source_node_keys/source_node_url_mapping/imageList` | review/query gate 检查数组顺序和 URL/node_key 映射都与主体绑定表一致 |

## Repair Playbook

1. 先判断任务是主体参照流、分镜参照流、查询下载还是修复审查。
2. 默认进入主体参照流；只有用户显式说“分镜参照流”才进入占位路线。
3. 主体参照流先读 `6-分组/第N集.md`，不要回到 `5-摄影` 或重新编写组内容。
4. 主体绑定只认组底 YAML 名称和画布节点名/URL/node_key，不认 UI 随机图片顺序。
5. 每条视频任务的时长都从当前分镜组 YAML 读取并 clamp，不使用全局固定 15 秒。
6. 调用 LibTV 只用 `.agents/skills/cli/libTV/scripts/` 官方脚本；不要复制改写官方脚本逻辑。
7. 生成完成后默认只报告画布和 session 状态；用户要求下载时再调用 `download_results.py`。
8. 默认不授权 LibTV 远端优化 prompt；用户显式 opt-in 才记录 `allow_libtv_prompt_optimization=true`。
9. 同画布 active URL 是主体参照流的默认加速项；不要为了 fresh resolve 重复上传同名主体图。
10. 单组参照图预算超过 9 张时先取舍，不要把超限 payload 交给远端试错。
11. 每组都留下 manifest / submit plan / queue record；远端优化 opt-in、预算排除和下载状态必须可审计。
12. 有可用主体参照图时，视频生成必须显式走“全能参考 / 多图主体参考生成视频”；参考图审核失败要阻断记录，不能静默改纯文生。
13. 外层 handoff message 放画布指令、生成参数、主体绑定表、真实参考 URL/node_key 和禁止优化锁；`create_generation_task.params.prompt` 只放分镜组正文 + 底部完整 YAML + 主体 `@` 引用。执行诊断、失败说明、fallback 决策只放证据工件。
14. 远端提交必须分层：handoff message 可有执行与绑定元信息；`params.prompt` 不得有执行锁、生成参数、`YAML主体清单`、`主体绑定表`、missing/excluded 诊断或文件路径。
15. 组底 YAML 要被消费三次：完整保留到 `params.prompt` 底部；`时长估算` 投影到 duration；`角色 / 场景 / 道具` 投影到参考绑定和证据工件。
16. 分镜组正文已有 StyleBible、声音、字幕或背景音乐要求时，不要在头部或尾部再复制一次。
17. 主体参照流默认 `modeType=mixed2video`；任何指定模式都必须传 Seedance 2.0 标准称谓，并在 manifest、submit plan、queue、远端 prompt 和实际工具入参中一致。
18. `allow_libtv_prompt_optimization=false` 要同时是证据字段和 handoff message 自然语言锁定；只写字段不足以防止 LibTV 中间 Agent 把 prompt 压缩成优化版单段。
19. 主体参照图不要只集中堆在绑定表或 URL 清单里；已绑定主体第一次出现在分镜组原文时，以及底部 YAML 对应主体名后，应插入 LibTV 画布 `@` 资产引用 / node mention（标准名称待官方确认），迫使远端按主体名精准匹配而不是按图片顺序匹配；若当前 CLI 无法验证 UI 级 `@` 引用，应记录 `at_asset_mention_unverified`。
20. 同一主体默认只提交一张图；active registry 中已有可用节点时不要再把同主体新上传图也塞进同一视频任务，除非用户明确要求多视图。
21. 参考数组顺序必须按 YAML 主体展示顺序：角色原顺序、场景原顺序、道具原顺序；预算排除只删除主体，不改变剩余主体相对顺序。即使如此，主体语义仍以 `yaml_name + category + node_key + URL` 绑定为准，不以数组下标为准。
18. 若发现新可复用失败模式，优先写入本文件；稳定成强制规则后再晋升到 `SKILL.md` 或 `references/`。

## Reusable Heuristics

- 这个技能的关键价值是“画布语义稳定”，不是替代 LibTV 官方 CLI。
- 主体绑定表应使用固定中文名 `主体绑定表`，减少远端 Agent 把它当普通说明忽略的概率。
- LibTV 多图任务中，`node_key + URL + yaml_name` 比 `Image 1/2/3` 更稳定。
- `6-分组` 组正文已经是 prompt 主体；本技能只做运输层组织、主体绑定和参数投影。
- 自动下载对画布流是副作用；默认关闭能减少重复本地文件和错误归档。
- 候选图片消歧证据属于 manifest / submit plan，不属于远端 prompt；远端只需要稳定主体名、node_key、URL 和用途。
- wrapper 的价值是环境一致性，不是 fork 官方 libTV CLI；官方脚本行为仍是下游真源。
- `allow_libtv_prompt_optimization=false` 不是 text2video 开关；它只能约束远端不改写 prompt，不能替代全能参考模式声明。
- `allow_libtv_prompt_optimization=false` 也不是足够强的远端行为锁；必须配套“禁止优化/重排/摘要/压缩/改写/补镜头”的 handoff 自然语言句，且查询后要检查实际 `params.prompt` 是否仍被改写或污染。
- LibTV 画布 `@` 资产引用 / node mention 是解决多图顺序漂移的关键手段；标准名称仍待官方确认。不要用 `〔主体参照: ...〕`、`{{Portrait N}}` 这类普通文本或占位符伪造引用，也不要只让远端在顶部 URL 清单和正文之间自行联想。
- 看到 `其中，` 后接 StyleBible/audio 的尾部段落，基本就是重复拼接错误；应删除尾段而不是调整措辞。
- 看到 `params.prompt` 里出现【执行锁】、【生成参数】、【本次提交的9张参照图】、【主体绑定表】、missing/excluded 状态，基本就是 handoff/prompt 分层失败；应立即重建为“分镜正文 + 完整 YAML”的干净 prompt。
- 看到 `imageList` 正好等于上传顺序、而不是 YAML 主体顺序，应视为高风险错绑；必须重排为 canonical reference order，并在查询结果中核对 `source_node_url_mapping`。
