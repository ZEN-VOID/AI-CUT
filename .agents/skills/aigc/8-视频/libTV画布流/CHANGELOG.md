# Changelog

## 2026-05-31

- 强化主体图占位符源层合同：每个新视频节点必须先创建/更新并查询 runtime `data.params.imageList[]`，用 `node_key + assetId/url` 建立 `runtime_image_placeholder_map[]`，确认 `{{Image N}}` 与稳定主体 ID 一致后才能 `--run`。
- 将计划层 `left_input_edges[] / image_placeholder_map[]` 口径收束为 `planned_left_input_edges[] / runtime_image_placeholder_map[]`，并同步 review gate、模板、type package 和 handoff 细则。
- 补强决定性运行前检查：最终节点参数、左侧输入和远端 prompt 写定后，`--run` 前只做一次权威远端查询；以该次 `data.params.imageList[] + data.params.prompt` 为放行真源，可修复错位先自动重写 prompt 或重建左侧输入，不可自动修复才 `needs_rework`。
- 禁止 `{{Portrait N}}`、绑定表、参考图清单、执行锁、路径或诊断文本进入远端视频 prompt；manifest、submit plan、queue record 和 review 增加最终 prompt hygiene 证据字段。
- 明确人工操作等价逻辑：参照图可按原命名上传画布，但进入视频节点后必须接受 `Image 1/2/3` 运行时编号；源层先建稳定名称映射，再按 YAML 顺序逐张传入，最后按 runtime 编号装配最终 prompt。
- 收紧占位插入口径：`{{Image N}}` 只插入底部 fenced YAML 的 `角色 / 场景 / 道具` 主体条目后，分镜正文保持原样，不再在正文主体第一次出现处插入占位。

## 2026-05-30

- 将 active `8-视频/libTV画布流` 从旧会话执行包迁移为 LibTV 视频生成计划层。
- 真实项目、分组、节点、上传、运行与下载统一交给最新版 `.agents/skills/cli/libTV` 执行；本技能只产出 manifest、submit plan、queue record、CLI handoff plan 和审查证据。
- 父级 `.agents/skills/aigc/8-视频` 补齐 router 合同与 `CONTEXT.md`，默认路由到 `libTV画布流`，旧 A/B/C/D 路线仅保留为 backup 兼容入口。
- 适配最新版 CLI 稳定主体引用机制：主体图按 canonical order 通过 `--left/--left-add` 连到视频节点左侧，prompt 使用 `{{Image N}}`，并以 `left_input_edges[]`、`image_placeholder_map[]` 和查询到的左侧输入顺序作为验收证据。

## 2026-05-22

- 吸收 AI 视频提示词学习：LibTV 画布流新增远端 prompt 执行身份保真门禁，提交时必须保留上游定场、场景/镜头身份、镜头先行顺序、方向参照和光线结果。
- 同步 `SKILL.md`、review 与经验层：禁止把 `5-分组` 正文改写成“人物做了什么”的主体动作摘要，查询远端 `params.prompt` 时检查 scene/shot identity 是否仍被保留。

## 2026-05-12

- 初始化 `libTV画布流` Skill 2.0 包。
- 从 `.agents/skills/cli/libTV` 继承官方调用逻辑索引，不修改官方技能包。
- 增加主体参照流默认路线、主体绑定表、画布资产管理、时长 clamp 和默认 `720p / 16:9`。
- 将自动下载默认策略改为关闭：结果先沉淀在画布，显式要求时再下载。
- 分镜参照流建立为空白占位。
- 强化主体参照流：锁定 `5-分组` 为主要信息来源，禁止回退到 `4-摄影` / `3-Detail` 重写；默认 `allow_libtv_prompt_optimization=false`；补充同画布 active URL 复用、多候选视觉消歧和单组 9 图参照预算裁决。
- 补全执行证据链：新增 active registry schema、subject-reference manifest schema、submit plan 模板和 queue record 模板；画布资产管理明确继承可见节点创建与素材命名修复细则。
- 追加全能参考硬门禁：有可用主体参照图时必须显式请求 `全能参考 / 多图主体参考生成视频`，handoff message 和工具入参必须含真实 `URL/node_key`，参考图审核失败不得静默降级为纯文生，内部诊断不得泄漏进 `params.prompt`。
- 固化 handoff / `params.prompt` 分层合同：handoff plan 承载执行锁、生成参数、主体绑定表和参考图清单；视频节点 prompt 只允许包含分镜组正文 + 底部完整 YAML，禁止把 `YAML主体清单`、`主体绑定表`、missing/excluded 诊断、StyleBible/audio 重复或 `其中，...` 尾段复述塞进视频节点 prompt。
- 补充 Seedance 2.0 标准 `modeType` 类型表：`text2video`、`singleImage2video`、`frames2video`、`image2video`、`audio2video`、`mixed2video`；主体参照流默认 `mixed2video`，指定模式时必须显式传标准称谓并保持全链路一致。
- 收紧 prompt 保真合同：`allow_libtv_prompt_optimization=false` 必须同时以字段和锁定计划出现，禁止远端优化、重排、摘要、压缩、改写或补镜头。
- 增加同主体参照去重规则：同一 YAML 主体默认只提交一张主体图；除非用户显式要求多视图或多版本对比，不得把 active 图和新上传图同时放入同一视频任务。
- 增加 canonical reference order：`subject_bindings`、`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 必须按 YAML `角色` 原顺序 -> `场景` 原顺序 -> `道具` 原顺序的选中子集传入；禁止上传顺序、画布创建时间、本地文件扫描顺序或 `Portrait N` 成为主体语义来源。
