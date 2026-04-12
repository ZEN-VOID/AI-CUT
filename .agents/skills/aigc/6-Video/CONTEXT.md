# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/6-Video` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/6-Video/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 执行者跳过视频请求整理层，直接写 CLI 命令 | 阶段边界层 | 回到 `6-视频` 先生成请求 JSON | 在父级 `When Not to Use` 和 handoff 里固化与 `dreamina-cli` 的边界 | 视频任务先有请求对象再提交 |
| 输入不再读取 `3-Detail/第N集.json`，而改读临时稿或历史 sidecar | 输入真源层 | 回退到 canonical director root file | 在父级 `Execution Summary` 固化唯一主文件 | 新任务先声明 source file |
| 任务明明是分镜组蒸馏，却被误判成首帧类路径 | 父级路由层 | 默认回到 `1-提示词蒸馏/全能参照` | 在父级 `Route Summary` 固化唯一默认入口 | 分镜组视频请求默认落到 `1-提示词蒸馏/全能参照` |
| 只输出 prompt，不输出请求字段与落点 | 输出契约层 | 补写 episode JSON 与 manifest | 在 `output-template.md` 固化“prompt 不是唯一交付” | JSON 能直接进入视频工具或 handoff |
| 继续沿用 `6-视频` 搁浅旧认知 | 根级状态同步层 | 同步更新根技能、registry、routes 与 HARNESS | 把“阶段由搁浅转为部分可执行”视为必须向上同步的元修复 | 根技能与控制面不再把 `6-视频` 视为 frozen |
| 父合同把 `2-视频生成` 写成可执行，但叶子自身仍分散规则或路径口径漂移 | 子路径合同层 | 收敛到唯一 `.agents/skills/aigc/6-Video/2-视频生成/` 路径，并把 provider 空目录降级为 `providers/` 槽位 | 在审计脚本新增“叶子路径、主合同与 sidecar 目录说明必须一致”检查 | `2-视频生成` 的文档、磁盘与审计口径一致 |

## Repair Playbook

1. 先确认当前任务是否仍属于“视频请求整理层”，而不是已进入模型提交层。
2. 再确认 `projects/<项目名>/3-Detail/第N集.json` 是否存在且字段完整到可被蒸馏。
3. 再判断当前是组级 `1-提示词蒸馏/全能参照`、帧级 `1-提示词蒸馏/首帧参照`，还是提交前的 `2-视频生成`。
4. 若命中未补齐子路径，显式报告缺口，不下伪执行链。
5. 若阶段状态已变更，记得同步回根技能、registry、routes 与 `HARNESS.md`。

## Reusable Heuristics

- `6-视频` 的第一复杂度不是“怎么生成视频”，而是“怎样先把上游真源变成稳定的视频请求对象”。
- 对当前仓来说，`3-Detail/第N集.json` 比任何临时 prompt 草案都更接近视频阶段的第一事实源。
- 视频阶段与 `dreamina-cli` 的边界应固定为：`6-视频` 负责请求对象，`dreamina-cli` 负责提交与轮询。
- 当阶段从 `shelved` 升级为“部分可执行”时，最容易漏掉的不是叶子文件，而是根技能、registry、routes 与 HARNESS 的同步。
- 当同一视频入参模板开始被多个叶子子技能共用时，应优先提升到 `6-视频/_shared/`，不要继续留在某个子技能私有 `templates/` 中演化。
- 当视频入参既要给工具消费，又要给人直接审读时，优先采用 `第N集.json + 第N集.txt` 双输出，而不是只保留 JSON。
- 当同一 tranche 同时承载组级与帧级叶子子技能时，共享模板必须先抽成中性骨架，再由叶子子技能各自补 `shot_level + source_shot_ids` 约束；不要把组级字段硬写死成全阶段默认。
- 当请求对象已经稳定、任务目标也已转向真实生成时，最稳的做法不是直接跳到 provider 命令，而是先通过 `2-视频生成` 产出可复核的 handoff 包。

## Case Log

### Case-20260412-AIGC-VIDEO-4-DESIGN-RUNTIME-SYNC

- milestone_type: source_contract_change
- outcome: 将 `6-视频` 父级与引用细则中的 design 资产输入口径，从旧的 `主体/` 运行时统一回收到了 `projects/<项目名>/4-Design/`。
- root_cause_or_design_decision: `4-Design` 父级与其叶子技能已经把 design-source 产物稳定落到 `projects/<项目名>/4-Design/`，但 `6-视频` 仍延续旧的 `主体/` 路径，会让视频阶段回读到失效 runtime。
- final_fix_or_heuristic: 以 `.agents/skills/aigc/_shared/project-runtime-layout.md` 为 runtime 单一真源，同步调整 `6-视频/SKILL.md` 与 `references/execution-flow.md` 的 design 资产引用路径。
- prevention_or_replication_checklist:
  - [x] `6-视频` 父级合同已改为读取 `4-Design`
  - [x] `references/execution-flow.md` 已同步 design 资产路径
  - [x] `2-视频生成` 引用资产路径已同步
- evidence_paths:
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/6-Video/references/execution-flow.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
- user_feedback_or_constraint: 用户确认继续把 `4-Design` 父级与 shared runtime 一并收口，避免下游继续读旧的 `主体/` 口径。

### Case-20260410-AIGC-VIDEO-STAGE-ACTIVATION

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/6-视频` 从空壳搁浅目录升级为“父级阶段合同 + 首个可执行子路径 `1-提示词蒸馏/全能参照`”。
- root_cause_or_design_decision: 根技能、registry 与 HARNESS 都把 `6-视频` 标成 `shelved`，但实际需求已经明确要求“从 `3-Detail/第N集.json` 蒸馏视频工具入参 JSON”，继续维持搁浅会造成根入口与子技能落地目标冲突。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md + references/*.md`，再补 `1-提示词蒸馏/全能参照` 子技能，并同步更新根技能、registry、routes 与 HARNESS 的阶段状态。
- prevention_or_replication_checklist:
  - [x] `6-视频` 父级合同已补齐
  - [x] `1-提示词蒸馏/全能参照` 子技能已补齐
  - [x] 根技能与 registry 状态已同步
  - [x] `HARNESS.md` 已同步
- evidence_paths:
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/6-Video/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
  - `.codex/registry/skills.yaml`
  - `HARNESS.md`
- user_feedback_or_constraint: 用户明确要求完善 `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照`，并指定上游默认路径、shared schema、模板目标和 prompt 压缩规则。

### Case-20260410-AIGC-VIDEO-SHARED-TEMPLATE-PROMOTION

- milestone_type: source_contract_change
- outcome: 将 `全能参照` 子技能内的 `video-generation-input.template.json` 提升为 `6-视频/_shared/` 共享模板，改为父级共享真源。
- root_cause_or_design_decision: 模板结构已经不再只是 `全能参照` 专属，而是承载整个 `6-视频` 阶段下多个视频子技能都可能复用的请求骨架；继续放在子技能私有目录会形成隐藏第二真源。
- final_fix_or_heuristic: 把模板移动到 `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`，并要求叶子子技能只回指共享模板，不再各自维护同名私有模板。
- prevention_or_replication_checklist:
  - [x] 共享模板已移入 `6-视频/_shared/`
  - [x] 父级合同已标注共享模板真源
  - [x] 子技能模板引用已改为回指共享路径
  - [x] 私有旧模板已移除
- evidence_paths:
  - `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
- user_feedback_or_constraint: 用户明确要求将该模板从 `全能参照` 子技能私有模板提升为 `6-Video` 共享模板，并同步调整引用机制与移除旧模板设定文件。

### Case-20260410-AIGC-VIDEO-DUAL-OUTPUT-MODE

- milestone_type: source_contract_change
- outcome: 为 `6-视频` 增加共享文本模板，并将 `全能参照` 的产物切换为 `第N集.json + 第N集.txt` 双输出模式。
- root_cause_or_design_decision: 现有共享 JSON 模板已经足够承载工具消费，但缺少一个给人直接查看提示词与字数统计的轻量文本视图，导致叶子子技能仍偏单一 JSON 视角。
- final_fix_or_heuristic: 在 `6-Video/_shared/` 新增 `视频生成入参.template.txt`，并将 `全能参照` 输出合同统一调整为 JSON 主文件 + TXT 阅读视图 + manifest。
- prevention_or_replication_checklist:
  - [x] 共享 txt 模板已落盘
  - [x] 父级合同已标注双模板
  - [x] 子技能已切换双输出命名
  - [x] 相关落点与输出契约已同步
- evidence_paths:
  - `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
- user_feedback_or_constraint: 用户明确要求在 `.agents/skills/aigc/6-Video/_shared` 中新增 `视频生成入参.template.txt`，并将 `全能参照` 设定为 `第N集.json` 与 `第N集.txt` 双输出模式。

### Case-20260410-AIGC-VIDEO-FIRST-FRAME-ROUTE-ACTIVATION

- milestone_type: source_contract_change
- outcome: 将 `1-提示词蒸馏/首帧参照` 从空目录升级为可执行叶子子技能，并同步把 `6-视频` 父级路由从“仅全能参照可执行”更新为“组级 + 帧级双入口”。
- root_cause_or_design_decision: 用户已经明确要求按单一 `分镜ID` 做帧级蒸馏，并继续复用 `6-视频/_shared` 双模板；若父级与共享模板仍只按组级口径书写，会形成“叶子已存在但上层真源仍写待补”的状态漂移。
- final_fix_or_heuristic: 先把共享 JSON/TXT 模板收敛为兼容组级/帧级的中性骨架，再补 `首帧参照` 的帧级合同、剧情桥段提取规则与双输出落点，最后回写父级阶段状态。
- prevention_or_replication_checklist:
  - [x] 共享 JSON 模板已支持 `shot_level + source_shot_ids`
  - [x] 共享 TXT 模板已改为按 `prompt_style.char_limit` 解释字数窗
  - [x] 父级 `Route Summary` 已包含 `首帧参照`
  - [x] `1-提示词蒸馏/首帧参照` 已具备 `SKILL.md + CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`
  - `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求完善 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照`，并要求站在分镜帧颗粒度、默认读取 `projects/<项目名>/3-Detail/第N集.json`、沿用双输出模板，但把 `剧本正文` 解析为对应分镜帧的剧情桥段。

### Case-20260411-AIGC-VIDEO-GENERATION-TRANCHE-CONTRACT-REPAIR

- milestone_type: source_contract_change
- outcome: 将历史遗留的 `2/3-视频生成` 路径漂移收敛为真实的 `6-Video/2-视频生成/` 受治理叶子技能，并把 provider 空目录从误导性的“能力暗示”收口到 `providers/` 目录说明。
- root_cause_or_design_decision: 质量评估暴露出 `6-Video` 存在编号漂移与假阳性成熟度问题：父级与局部 sidecar 都声明提交入口已可执行，但磁盘路径、合同编号与规则载体长期不一致，导致“文档成立、目录存在、实际真源不唯一”的三层脱节。
- final_fix_or_heuristic: 将 `2-视频生成` 定义为“稳定请求 JSON -> provider 路由 -> handoff 包 -> provider skill”的唯一执行入口层；provider 名称本身只保留为 `providers/` 槽位，后续若需要本地执行合同，再单独晋升为 governed child skill。
- prevention_or_replication_checklist:
  - [x] `2-视频生成` 已具备 `SKILL.md + CONTEXT.md`
  - [x] provider 占位目录已从 `subtypes/` 收敛到 `providers/`
  - [x] 父级 `Route Summary`、`execution-flow` 与 `output-template` 已与 tranche 3 对齐
  - [x] 审计脚本已能检出文档声明但缺失合同的 subtype 路径
- evidence_paths:
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/6-Video/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/SKILL.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/CONTEXT.md`
  - `.agents/skills/aigc/6-Video/2-视频生成/providers/README.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户要求对评估发现的问题做全量修复，不能保留“目录像是有能力、实际没有合同”的状态。
