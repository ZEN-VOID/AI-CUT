# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/角色` 的经验层知识库，不是过程日志。
- 调用本技能时，应在 `SKILL.md` 之后预加载本文件。

## Context Health

- soft_limit_chars: 22000
- hard_limit_chars: 44000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| Markdown 三段式被整篇塞进面板 prompt | prompt extraction layer | 只抽取 `**prompt整合**` 段 | 脚本与 SKILL 固化 prompt 部分直引 | `design_subject` 不含 `**物语**` / `**解构**` |
| `_manifest.json` 说明无 `character_design.json`，脚本却只读 JSON | input compatibility layer | 同时支持 manifest + per-role Markdown | 输入合同声明多型设计产物 | 项目样例能解析 5 个 Markdown 任务 |
| 批量角色面板没有吃已有图 | SMART reference layer | batch 模式扫描设计目录和 `Assets/角色` | SMART 表固定 batch-only 自动参照 | batch request 中匹配图片进入 `images[]` |
| 角色脚本私有扫描/私有 API 调用与父 bridge 漂移 | canonical bridge layer | 角色脚本只写 layout，调用 `_shared/panel_auto_generate.py` 完成参照扫描、request sidecar 与 imagegen handoff | active leaf 不保留第二套 `match_auto_refs` 或 `run_generation_from_docs` 调用 | request sidecar 落到 `generated/requests/`，trace 记录 continuity refs |
| 单文件重跑被错误绑定其它角色图 | dispatch boundary layer | prompt-file 单文件默认 `single-doc-t2i` | 单文件模式禁止隐式 continuity 扫描 | 单文件 dry-run `images=[]` |
| JSON 落盘后没有自动调用生图 | delivery boundary layer | 默认调用 built-in imagegen；只在显式停点跳过 | CLI 默认值与 SKILL 同步 | 无 `--layout-only` 时进入 generation 分支 |
| 批量面板统一使用 `--generation-dry-run` 时，角色 leaf 只接受旧 `--dry-run` 名称 | leaf CLI compatibility layer | 为 `--dry-run` 增加 `--generation-dry-run` 别名 | sibling CLI 的 dry-run 停点语义保持统一，批量路由不再依赖脚本私有记忆 | `generate_character_panels.py --help` 显示 `--dry-run, --generation-dry-run` |
| 旧 `角色面板` 模板被同义改写导致布局漂移 | template contract layer | 镜像参照模板字段结构 | 模板作为单一布局真源 | `prompt_payload.layout.template_type=CHARACTER_ATMOSPHERIC_DOSSIER` |
| 项目运行时缺少 `4-Design/角色/2-设计/第N集/`，批量验证无法启动 | runtime precondition layer | 改用显式 `--prompt-file` 或先执行角色 `2-设计` | CLI 对缺失设计目录返回 `FAIL-RP-INPUT`，避免静默生成空面板 | 错误信息指向缺失目录，fixture dry-run 可继续验证脚本 |

## Repair Playbook

1. 先检查输入模式：project batch、prompt-file、prompt-text。
2. 再检查主体锚点：manifest / JSON / Markdown / 文件名是否能给出 `role_id + role_name`。
3. prompt 异常时优先检查 `prompt整合` 抽取，不要在面板层重写角色。
4. 参照图异常时先看共享 bridge 的 SMART 模式，batch 才允许自动扫图。
5. 生图异常时用 `generated/requests/panel_auto_generate_batch.json` 直接 dry-run built-in imagegen。
6. 若项目批量入口报设计目录不存在，先确认 `2-设计/角色` 是否实际落盘；验证脚本时可用 `.tmp` fixture 或显式 `--prompt-file`，不要把空项目误判为脚本解析失败。

## Reusable Heuristics

- 角色面板最稳的设计主体不是完整 Markdown，而是上游已经收束好的 `prompt整合`。
- 当前 `4-Design/角色` 可能只有逐角色 Markdown 和 `_manifest.json`，不要假设一定存在 `character_design.json`。
- 批量链路的自动参照应按主体名/ID 过滤，宁可少绑定，也不要把同集其它角色的图塞入当前角色。
- 单文件/自然语言模式默认 T2I 是防止误绑定的关键边界；显式参考图才进入 I2I。
- 角色 leaf 不应维护私有 Assets 扫描；它只负责把 `continuity_source_roots` 写进 layout，匹配和 request 由父级共享 bridge 负责。
- 和场景/道具同层批量执行时，优先维护兼容别名而不是重命名停点参数；批量 orchestration 应记一个统一口令，而不是每个 leaf 一套。
