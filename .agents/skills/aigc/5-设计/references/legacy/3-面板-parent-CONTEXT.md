# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-设计/3-面板` 的经验层知识库，不是过程日志。
- 调用 `3-面板` tranche 或其 active leaf 时，应先读取本文件，再进入 leaf 局部 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-面板` 父目录为空导致父层无法路由 | tranche source-layer | 补齐 `SKILL.md + CONTEXT.md + _shared bridge` | 父 tranche 只声明 active leaf 与 pending sibling | `5-设计/SKILL.md` 能条件读取 `3-面板/SKILL.md` |
| active leaf 与父 tranche 列表不一致 | coverage 同步层 | 将 `场景 / 角色 / 道具` active 状态同步到父 `3-面板/SKILL.md` | registry、父 tranche、阶段父层三处同步核对 | active leaf 列表一致且服装仍 pending |
| leaf 直接调用 API，形成多套生图桥 | canonical bridge 层 | 把生图映射收回 `_shared/panel_auto_generate.py`，默认转为内置 imagegen request sidecar | leaf 只写 layout 与调用共享桥；真实生成由 Codex 内置 `image_gen` 执行 | leaf 脚本没有私造 API payload 逻辑 |
| 角色 leaf 私有扫描 `Assets/角色`，与场景/道具 SMART 行为漂移 | canonical bridge 层 | 角色 leaf 改为只写 layout，并把 continuity roots 交给共享 bridge | `_shared/panel_auto_generate.py` 统一 mode、Assets 扫描、request sidecar 与 imagegen handoff | 角色脚本无私有 `run_generation_from_docs` 与 `match_auto_refs` |
| 批量任务没自动引用已有设计图 | SMART 判型层 | `continuous-batch` 扫描 `2-设计` 同 stem 单主体图片 | SMART 策略写入父 tranche 与共享桥，并回指 `2-设计/_shared/design-output-contract.md` | request trace 有 `continuity_reference_images` |
| `direct-request` 多文件目录被误判为 `continuous-batch` | SMART 判型层 | `pipeline_context=direct-request` 的 `auto` 固定解析为 `single-doc-t2i` | 批量资格只由 `panel-stage` 上下文或显式 `continuous-batch` 赋予，不靠 packet 数量推断 | 多 layout direct-request dry-run `continuity_reference_images=[]` |
| `layout-only/json-only` 没有 request sidecar，无法审计后续补跑 | delivery trace 层 | 共享 bridge 增加 request-sidecar-only 停点 | leaf 在 layout-only 时仍调用共享 bridge，但 `generate=False` | `generated/requests/panel_auto_generate_batch.json` 存在且未调用 nano |
| 三个 panel leaf 的 dry-run 旗标不一致，批量命令在部分 leaf 直接报参数错误 | leaf CLI contract 层 | 将“写 layout + request sidecar + nano dry-run”的统一别名收束为 `--generation-dry-run`，并保留 `--dry-run` 兼容 | 父 tranche 固化跨 leaf CLI 停点语义，避免批量推进时记忆分叉 | `场景/角色/道具` 都接受 `--generation-dry-run` 且落盘 request sidecar |
| 面板层重新拼 prompt 或漏掉 `global_style_prefix` | prompt 真源层 | 回到 `2-设计` 的 `full_generation_prompt` 或 Markdown `prompt整合` | 父 tranche 固定优先读取 `full_generation_prompt`，不在面板层二次润色 | layout prompt 可回链到上游设计文件 |
| JSON 设计项同时存在 `prompt_integration` 与 `full_generation_prompt` 时面板误取未加前缀正文 | prompt 字段优先级层 | 将场景/角色面板 JSON prompt 读取顺序改为先取 `full_generation_prompt` | 面板脚本字段序必须与父 tranche 经验合同一致，`prompt_integration` 仅作兼容 fallback | batch request prompt 以 `Global style prefix:` 开头 |
| manifest 批量模式读取 Markdown 时仍只认 `prompt整合` | Markdown 字段优先级层 | Markdown 抽取同样按 `full_generation_prompt -> prompt整合` 顺序 | JSON 与 Markdown 两种入口共享同一 prompt 真源优先级 | manifest 批量 request prompt 以 `Global style prefix:` 开头 |
| 单文件任务被自动塞入历史参照 | SMART 污染层 | 单文件/自然语言默认 `single-doc-t2i` | 只有显式 `--reference` 才加入参照 | request trace 无自动 continuity refs |
| 面板图批量生成依赖 API key / 远端 provider，导致 layout 交付和后续审计被外部时延阻塞 | execution mode layer | 先写 `panel_auto_generate_batch.json` 与 bridge report，再由 Codex 内置 `image_gen` 逐张生成 | 共享 `image-generation-execution-contract.md` + `_shared/panel_auto_generate.py` 默认 `codex-builtin-imagegen`，API/CLI 仅显式 fallback | manifest/bridge report 含 `request_ready`、`provider_skill=imagegen`、`default_model=GPT-IMAGE-2` 与 request batch |

## Repair Playbook

1. 先确认当前 leaf 是否在父 tranche 声明为 active。
2. 再确认 leaf 是否先写 layout JSON，而不是直接调用生图。
3. 检查 `prompt` 是否直接来自 `2-设计` 产物的 `full_generation_prompt / prompt整合`。
4. 检查 `SMART` 模式：批量走 `continuous-batch` 并只扫描同 stem 单主体图，单文件/自然语言走 `single-doc-t2i`。
5. 若 imagegen 请求映射失败，先查 `_shared/panel_auto_generate.py`，再查 `imagegen` 技能合同。
6. 判断生成状态时区分 `request_ready` 与真实图片完成；只有本地图片文件能证明产图完成。

## Reusable Heuristics

- 面板层最稳的真源不是设计 JSON 的完整正文，而是上游已经收束好的 `full_generation_prompt / prompt整合`；面板只做版式化与派生生图。
- 面板模板的固定 layout 词应始终低于上游设计 prompt：模板负责组织版式、审阅维度和防漂移，不得覆盖主体身份、时代、风格、材质、尺度或叙事功能。
- 面板中的参考图应被描述为 continuity anchor，而不是替换主体或复制构图的强参照；批量自动参照尤其需要在模板层防止把历史图的偶发噪声带入新面板。
- 图片内精确文字不是稳定生成能力；面板模板应优先要求固定 badge 区域与短 ID，可把准确中文名交给后期叠字或 manifest，而不是强压模型生成长文本。
- 当 JSON 中同时有 `full_generation_prompt` 与 `prompt_integration`，面板层必须优先使用前者；后者通常是主体设计正文，不保证包含全局风格前缀。
- 当面板批量入口通过 manifest 回读 Markdown 时，也必须优先读取 `full_generation_prompt`；不能让 Markdown 入口成为绕过全局前缀的第二路径。
- SMART 参照图是批量连续性机制，不是所有单次生图的默认行为；`direct-request` 即使一次传入多个 layout，也不自动升级为批量连续上下文。
- `2-设计` 同目录同名图片是批量 panel 的 continuity reference 候选，不是 layout JSON 的替代物。
- 父 tranche 应持有共享桥与路由口径，leaf 只持有领域 prompt 提取、模板装配和局部 manifest。
- JSON-only 停点不等于没有 handoff；应保留 request sidecar 和 bridge report，供审计或后续补跑。
- 批量面板链路里，`--generation-dry-run` 应被视为跨 leaf 的统一停点口令；局部旧别名可以保留，但不能再让同层兄弟脚本各说各话。
- 面板层默认完成口径是 layout + request sidecar + 内置 imagegen 生成/复制证据；不要把 `request_ready` 写成图片已完成态。
- active leaf 每新增一个，都要同步父 `3-面板`、`5-设计` 父层与 registry；否则批量路由会出现“文件存在但入口仍 pending”的断层。
