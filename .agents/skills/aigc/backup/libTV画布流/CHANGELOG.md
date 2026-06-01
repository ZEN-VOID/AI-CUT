# Changelog

## 2026-05-22

- 吸收 AI 视频提示词学习：LibTV 画布流新增远端 prompt 执行身份保真门禁，提交时必须保留上游定场、场景/镜头身份、镜头先行顺序、方向参照和光线结果。
- 同步 `SKILL.md`、review 与经验层：禁止把 `5-分组` 正文改写成“人物做了什么”的主体动作摘要，查询远端 `params.prompt` 时检查 scene/shot identity 是否仍被保留。

## 2026-05-12

- 初始化 `libTV画布流` Skill 2.0 包。
- 从 `.agents/skills/cli/libTV` 继承官方调用逻辑索引，不修改官方技能包。
- 增加主体参照流默认路线、主体绑定表、画布资产管理、时长 clamp 和默认 `720p / 16:9`。
- 将自动下载默认策略改为关闭：结果先沉淀在画布，显式要求时再下载。
- 分镜参照流建立为空白占位。
- 强化主体参照流：锁定 `5-分组` 为主要信息来源，禁止回退到 `4-摄影` / `3-Detail` 重写；默认 `allow_libtv_prompt_optimization=false`；补充 `.env` 自动加载、同画布 active URL 复用、多候选视觉消歧和单组 9 图参照预算裁决。
- 补全执行证据链：新增 env wrapper、active registry schema、subject-reference manifest schema、submit plan 模板和 queue record 模板；画布资产管理明确继承官方可见节点创建与 `素材图片` 命名修复细则。
- 追加全能参考硬门禁：有可用主体参照图时必须显式请求 `全能参考 / 多图主体参考生成视频`，handoff message 和工具入参必须含真实 `URL/node_key`，参考图审核失败不得静默降级为纯文生，内部诊断不得泄漏进 `params.prompt`。
- 固化 handoff / `params.prompt` 分层合同：handoff message 承载执行锁、生成参数、主体绑定表和参考图清单；`create_generation_task.params.prompt` 只允许包含分镜组正文 + 底部完整 YAML + 主体 `@` 资产引用，禁止把 `YAML主体清单`、`主体绑定表`、missing/excluded 诊断、StyleBible/audio 重复或 `其中，...` 尾段复述塞进视频节点 prompt。
- 补充 Seedance 2.0 标准 `modeType` 类型表：`text2video`、`singleImage2video`、`frames2video`、`image2video`、`audio2video`、`mixed2video`；主体参照流默认 `mixed2video`，指定模式时必须显式传标准称谓并保持全链路一致。
- 收紧远端 prompt 保真合同：`allow_libtv_prompt_optimization=false` 必须同时以字段和自然语言锁定句出现，禁止远端优化、重排、摘要、压缩、改写或补镜头；分镜组原文中已绑定主体首次出现处必须插入 LibTV 画布 `@` 资产引用 / node mention（标准名称待官方确认），禁止用普通文本参照说明伪造引用，避免远端按上传图片顺序错配；当前 CLI 无法验证 UI 级 `@` 引用时必须记录 `at_asset_mention_unverified`。
- 增加同主体参照去重规则：同一 YAML 主体默认只提交一张主体图；除非用户显式要求多视图或多版本对比，不得把 active 图和新上传图同时放入同一视频任务。
- 增加 canonical reference order：`subject_bindings`、`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 必须按 YAML `角色` 原顺序 -> `场景` 原顺序 -> `道具` 原顺序的选中子集传入；禁止上传顺序、画布创建时间、本地文件扫描顺序或 `Portrait N` 成为主体语义来源。
