# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/3-面板/场景` 的经验层知识库，不是执行日志。
- 调用本技能时，应在 `4-Design/3-面板` 父级与共享 SMART 合同之后加载本文件。
- 优先级固定为：用户显式请求 > `AGENTS.md` / meta 规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 24000
- hard_limit_chars: 48000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把 Markdown 的 `物语/解构` 全文塞进面板 prompt | 输入解析层 | 只提取 `**prompt整合**` 后的 prompt 段 | 在脚本和 SKILL 固化 prompt-only 提取门 | layout `prompt` 不含 `物语/解构` 标题 |
| 当前仓 `scene_design.json.scenes[]` 与旧仓 `scene_designs[]` 字段不一致 | 迁移兼容层 | 同时支持 `scenes[] / scene_designs[]`，按 prompt 字段优先级读取 | skill_manifest 写清当前第一输入为 `scene_design.json` | 脚本可 dry-run 当前新路径 |
| 批量执行时未拿到场景参照图 | SMART 输入根层 | layout 写入 `continuity_source_roots` 指向对应 `2-设计` 目录与 Markdown 同级目录 | 共享 SMART 桥在 `continuous-batch` 扫描主体 token | request `images[]` 可见匹配图 |
| 单文件/自然语言直调误扫参考图 | SMART 场景判型层 | `--prompt-file` / `--prompt-text` 默认 `pipeline_context=direct-request` | `single-doc-t2i` 不读取 continuity refs | `continuity_reference_images=[]` |
| `--prompt-file` 指向目录时被数量误判为批量 | SMART 场景判型层 | direct-request 下的 `auto` 固定为 `single-doc-t2i` | 只有父级 batch 或显式 `continuous-batch` 才自动扫参照 | 目录直调 request trace 无 continuity refs |
| JSON-only 没有 request sidecar，后续补跑不可复盘 | delivery trace 层 | layout-only 时仍调用共享 bridge 的 request-sidecar-only 停点 | request sidecar 与 bridge report 是 JSON 停点的必备派生证据 | `generated/requests/panel_auto_generate_batch.json` 存在 |
| 批量面板脚本统一使用 `--generation-dry-run` 时，场景 leaf 直接报参数错误 | leaf CLI compatibility 层 | 为 `--dry-run` 增加 `--generation-dry-run` 别名 | 同层 leaf 的“写 layout + request sidecar + nano dry-run”停点语义统一，旧参数仅作兼容 | `generate_scene_panels.py --help` 显示 `--dry-run, --generation-dry-run` |
| layout JSON 已写但生图失败 | 下游 API 层 | 保留 layout 与 request sidecar，按 nano-banana root-cause 链排查 API key/参数/图像编码 | 默认先写 JSON，再调用 nano，避免失败时丢业务真源 | `_manifest.json.image_generation.success=false` 且有 report |

## Repair Playbook

1. 先确认输入类型：默认批量 `scene_design.json`、目录 Markdown、单文件、JSON、自然语言。
2. 再确认 prompt 来源：优先 `prompt整合 / prompt_integration / design_prompt / final_prompt / final_scene_prompt`。
3. 检查模板 `prompt_payload` 是否存在，比例是否仍为 `16:9 + 3x3`。
4. 若参考图异常，查看 `smart_mode_resolved` 与 request JSON 的 `prompt_reference`。
5. 生图失败或 JSON-only 补跑时不重写 layout；先看 `generated/requests/panel_auto_generate_report.json`。

## Reusable Heuristics

- 场景面板应继承设计阶段的 prompt 密度，但不继承设计阶段的推导正文。
- `layout.json` 顶层字段应尽量直接对齐 nano-banana 输入，减少中间树重复。
- 批量连续链路适合自动参考图；单点 prompt 直调更适合保持 T2I，除非用户显式给参考图。
- 与同层 sibling 做批量推进时，dry-run 停点参数必须保持同义；需要升级口径时优先加兼容别名，而不是让调用方记住多个变体。
