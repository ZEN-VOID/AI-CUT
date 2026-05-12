# Review Contract

## Required Checks

| check_id | target | pass condition | fail code |
| --- | --- | --- | --- |
| `REV-LIBTVCANVAS-01` | route | 默认主体参照流；分镜参照流仅显式选择且当前占位 | `FAIL-ROUTE` |
| `REV-LIBTVCANVAS-02` | group source | 每个任务可回指 `4-分组/第N集.md` 的 `## x-y-z` | `FAIL-GROUP-SOURCE` |
| `REV-LIBTVCANVAS-03` | subject binding | `主体绑定表` 含 `yaml_name / node_key / URL / usage` | `FAIL-BINDING` |
| `REV-LIBTVCANVAS-04` | image order safety | 远端消息声明图序冲突时以绑定表为准 | `FAIL-ORDER-SAFETY` |
| `REV-LIBTVCANVAS-05` | duration | 按 YAML 估算并 clamp 到 4-15 秒 | `FAIL-DURATION` |
| `REV-LIBTVCANVAS-06` | default spec | 未显式覆盖时为 `720p`、`16:9` | `FAIL-SPEC` |
| `REV-LIBTVCANVAS-07` | official handoff | 使用 `.agents/skills/cli/libTV/scripts/` 官方脚本 | `FAIL-OFFICIAL-HANDOFF` |
| `REV-LIBTVCANVAS-08` | download policy | 默认不下载；显式下载才调用 `download_results.py` | `FAIL-DOWNLOAD-POLICY` |
| `REV-LIBTVCANVAS-09` | source fidelity | prompt 主体直接采用 `4-分组` 组正文；未回到 `3-摄影` / `3-Detail` 重写 | `FAIL-SOURCE-FIDELITY` |
| `REV-LIBTVCANVAS-10` | YAML subject baseline | 主体只来自组底 YAML `角色 / 场景 / 道具`，没有正文泛词扩展 | `FAIL-YAML-SUBJECT` |
| `REV-LIBTVCANVAS-11` | prompt optimization | `allow_libtv_prompt_optimization=false`，除非用户显式 opt-in 且记录在 plan/queue/report | `FAIL-PROMPT-OPT` |
| `REV-LIBTVCANVAS-12` | active URL reuse | 同画布同 YAML 名 active URL 优先复用；替换/更新才上传 | `FAIL-ACTIVE-URL-REUSE` |
| `REV-LIBTVCANVAS-13` | visual disambiguation | 多候选先发送候选图到窗口做视觉消歧，无法唯一才 ambiguous | `FAIL-DISAMBIGUATION` |
| `REV-LIBTVCANVAS-14` | reference budget | `images[]` / `mixedList` <= 9；超限有排除记录，不可压缩则不得提交 | `FAIL-REFERENCE-BUDGET` |
| `REV-LIBTVCANVAS-15` | env loading | 调用官方脚本前自动加载 `.env` 中的 `LIBTV_ACCESS_KEY` | `FAIL-ENV-LOADING` |
| `REV-LIBTVCANVAS-16` | active registry | `libtv-canvas-active-registry.json` 使用 `projectUuid::category::yaml_name` 主键；同名 active 唯一；替换时旧记录 inactive | `FAIL-ACTIVE-REGISTRY` |
| `REV-LIBTVCANVAS-17` | manifest schema | 每组 manifest 含主体绑定、候选/消歧证据、预算排除、进入 LibTV 图片且 `libtv_images <= 9` | `FAIL-MANIFEST` |
| `REV-LIBTVCANVAS-18` | submit plan / queue | submit plan 与 queue record 同步记录 opt-in、wrapper、官方脚本、download=false 和阻断/提交状态 | `FAIL-QUEUE-EVIDENCE` |
| `REV-LIBTVCANVAS-19` | official canvas asset detail | 上传资产时创建可见 resource node；默认 `素材图片` 时按官方细则修正 `name/data.name`，不新建重复节点 | `FAIL-CANVAS-ASSET-DETAIL` |
| `REV-LIBTVCANVAS-20` | reference generation mode | 有可用参考图时，远端消息显式请求“全能参考 / 多图主体参考生成视频”，并含真实 `URL + node_key + yaml_name + 用途` | `FAIL-REFERENCE-MODE` |
| `REV-LIBTVCANVAS-21` | no silent text fallback | 参考图预处理/审核失败时状态为 `needs_rework / reference_asset_review_failed`；无用户显式授权不得降级为纯文生视频 | `FAIL-SILENT-TEXT-FALLBACK` |
| `REV-LIBTVCANVAS-22` | prompt hygiene | `create_generation_task.params.prompt` 不包含内部诊断、负面占位句、执行锁、生成参数、主体绑定表或 missing/excluded 状态，如 `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频` | `FAIL-PROMPT-HYGIENE` |
| `REV-LIBTVCANVAS-23` | prompt assembly structure | handoff message 与 `params.prompt` 分层；handoff 可包含执行/绑定元信息，`params.prompt` 只含分镜正文 + 底部完整 YAML + 主体 `@` 引用 | `FAIL-PROMPT-STRUCTURE` |
| `REV-LIBTVCANVAS-24` | YAML subject projection | 组底 YAML 完整保留在 `params.prompt` 底部；已绑定主体在正文首次出现处和 YAML 对应主体名后插入画布 `@` 资产引用 / node mention | `FAIL-YAML-PROJECTION` |
| `REV-LIBTVCANVAS-25` | no duplicated style/audio | 不重复追加 `StyleBible`、`StyleBible_Summary`、声音、字幕、背景音乐约束；无 `其中，...` 尾部复述 | `FAIL-PROMPT-DUPLICATION` |
| `REV-LIBTVCANVAS-26` | no generic subject substitution | 不用 `角色与道具按原文生成`、泛化人物身份或泛化道具描述替代 YAML 主体绑定 | `FAIL-GENERIC-SUBJECT-SUBSTITUTION` |
| `REV-LIBTVCANVAS-27` | standard modeType | `modeType` 显式为 Seedance 2.0 标准称谓之一；主体参照流默认 `mixed2video`；指定类型时 manifest/plan/queue/prompt/tool params 一致 | `FAIL-STANDARD-MODETYPE` |
| `REV-LIBTVCANVAS-28` | prompt lock natural language | `allow_libtv_prompt_optimization=false` 同时出现在字段和 handoff message 自然语言锁定句中，明确禁止优化、重排、摘要、压缩、改写或补镜头，并要求 `params.prompt` 严格等于分镜正文 + 完整 YAML | `FAIL-PROMPT-LOCK` |
| `REV-LIBTVCANVAS-29` | canvas @ asset mentions | `分镜组原文` 与底部 YAML 中已绑定 YAML 主体后插入 LibTV 画布 `@` 资产引用 / node mention（标准名称待官方确认）；引用绑定来自 `主体绑定表` 的 `canvas_node_name / node_key / URL`，不依赖上传图片顺序、`Image N` 或 `imageList` 顺序，且不得伪造成普通文本解释、URL 注释或 `{{Portrait N}}`；无法验证时记录 `at_asset_mention_unverified` | `FAIL-CANVAS-AT-ASSET-MENTION` |
| `REV-LIBTVCANVAS-30` | remote prompt fidelity after query | 查询结果中的实际 `create_generation_task.params.prompt` 未被压缩、摘要、重排、改写为优化版单段 prompt，且未混入执行锁、生成参数、主体绑定表、missing/excluded 诊断；若发生则标记 `needs_rework / remote_prompt_rewritten_or_polluted` | `FAIL-REMOTE-PROMPT-REWRITTEN` |
| `REV-LIBTVCANVAS-31` | duplicate subject reference | 同一 YAML 主体默认只进入一张参照图；除非用户显式要求多视图或多版本对比，`imageList/mixedList` 不含同主体重复图 | `FAIL-DUPLICATE-SUBJECT-REFERENCE` |
| `REV-LIBTVCANVAS-32` | canonical reference order | `subject_bindings`、`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 按 YAML `角色` 原顺序 -> `场景` 原顺序 -> `道具` 原顺序的选中子集排列；不得按上传顺序、画布创建时间、本地文件扫描顺序或 `Portrait N` 排列 | `FAIL-REFERENCE-ORDER` |
| `REV-LIBTVCANVAS-33` | reference mapping consistency | 查询到的 `source_node_url_mapping` 中每个 `node_key/url` 与主体绑定表的 `yaml_name/category` 一一对应；不得用数组第 N 项反推主体 | `FAIL-REFERENCE-MAPPING` |

## Verdict

- `PASS`: 所有必查项通过。
- `BLOCKED`: 必需输入或主体绑定缺失。
- `PLACEHOLDER`: 用户选择了分镜参照流，但该流尚未实现。
- `REWORK`: LibTV 远端返回主体错绑、参考顺序/URL 映射不一致、工具错误、内容审核拦截、任务停滞，或实际 `params.prompt` 被远端压缩改写/混入 handoff 元信息。
