# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design` 阶段父 skill 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/SKILL.md` 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 根技能声称 `4-Design` 已建合同，但仓内没有阶段父级 | 阶段总合同层 | 补 `4-Design/SKILL.md + CONTEXT.md` | 把“阶段已建”定义为至少存在 stage parent 真源，而不是只有 leaf 目录 | 根技能状态与仓内实体一致 |
| leaf preload 直接引用不存在的 stage/substage parent | 上下文装配层 | 先补真实存在的 stage parent / tranche parent，再重挂 preload | 叶子只回链真实存在的父级真源 | preload 不再断链 |
| tranche parent 缺失，导致 leaf 各自发明父链 | tranche 治理层 | 先补当前轮真正要用的父级；当前最低闭环已提升到 `1-清单/{场景,角色,道具} -> 2-设计/{场景,角色,道具} -> 3-面板/{场景,角色,道具}` | 把 tranche parent 视为 leaf 共享 context bridge，并在迁移窗口显式标记 partial-active / pending-migration | source-layer status 不再虚报 |
| 场景 leaf 已迁回，但父层仍只宣称 `角色/道具` active | coverage 同步层 | 同步 `4-Design` 与 `2-设计` 父层 coverage 到 `场景/角色/道具` | 每次新增 active leaf 后同步检查阶段父级、tranche parent 与 shared input contract | 父层状态与 leaf 实体一致 |
| `4-Design` 父层越权发明第二业务真源 | 输出治理层 | 收回到“只路由、不写业务主稿” | 在 stage parent 固化“业务真源只由 leaf 写回” | 不再出现 `4-Design` 总稿 |
| `3-面板/场景` 已重建但父级仍显示 pending | 状态同步层 | 把 `3-面板` 更新为 `partial-active`，并明确 `场景 / 角色 / 道具` leaf active | 父级 Stage Coverage 必须随真实 source-layer 落点同步 | 父级路由可进入 `3-面板/{场景,角色,道具}` |
| 面板阶段默认未生图或直调误带参考图 | SMART 桥接层 | 引入 `3-面板/_shared` SMART 合同：批量连续执行扫 `2-设计` 图，单文件/自然语言默认 T2I | 把 SMART 判型放到 tranche shared contract，不在 leaf 复制 | request sidecar 记录 `smart_mode_resolved` |
| `3-面板/道具` 已重建但父级 coverage 仍只列场景 | coverage 同步层 | 同步 `4-Design` 父层、registry 与 HARNESS，把 `3-面板/{场景,道具}` 标为 partial-active | 新增 panel leaf 时同轮更新父层 active leaf 列表与路由策略 | 父级路由可进入 `3-面板/道具` |
| `3-面板/角色` 已重建但父级仍只列场景/道具 | coverage 同步层 | 同步 `4-Design` 父层、registry 与 nano-banana 回链，把 `3-面板/{场景,角色,道具}` 标为 partial-active | 新增 panel leaf 时同轮更新父层 active leaf 列表、SMART handoff 与入口元数据 | 父级路由可进入 `3-面板/角色` |
| pending `服装` leaf 被写成 active runtime 输出路径 | active leaf / runtime 投影层 | 将 `服装` 标成 `pending-migration`，不再声明 `4-Design/服装/*` active 输出根 | 初始化 skeleton 只从 `_shared/project-runtime-layout.md` 继承 active 三类 `场景/角色/道具`，pending sibling 不预建目录 | 新项目 `4-Design/` 下不再出现空的 `服装` runtime |
| `2-设计` 已新增单主体自动图，但阶段父层仍只把图片交给 `3-面板` 或 `5-Image` | 输出快路径同步层 | 在 `4-Design/SKILL.md` 回指 `2-设计/_shared/design-output-contract.md` | 把 `full_generation_prompt + same-stem auto image` 写进阶段拓扑、路由和 completion | 批量 panel 可直接扫描 `2-设计` 同 stem 图片 |
| 项目根 `team.yaml` 已启用顾问团，但 `4-Design` 仍把首次落盘后的收尾挂在 `监制` 名下 | 角色边界层 | 在 `4-Design/SKILL.md` 明确 `roles.supervision` 只负责前置 advisory，post-write 收尾回到 audit/validation | 父层与 leaf 统一把 `监制` 从 closeout owner 名单中移除 | `validation-report.md` 只保留 audit note，不再要求 `监制强化` 槽位 |
| `4-Design` 把 post-write audit、final-stage review gate 与 `source_skill_refs` 混成一条 reviewer 权限线 | council runtime layering | 先收回 `roles.supervision` 的 closeout 权，再把 `source_skill_refs` 固定为领域提示 | 在 `4-Design/SKILL.md` 与 `2-设计/_shared/subagent-supervision-contract.md` 中显式声明停用边界 | closeout 结论不再依赖 reviewer roster |
| `4-Design` 的落盘后收尾继续把 `_manifest.json`、派生 PNG 或 request sidecar 当成“监制补丁”对象 | audit boundary layer | 将 post-write 问题收束为 `validation-report.md` 的 audit note；业务 patch 只留给后续独立审计机制 | 父层合同不再把派生资产纳入 `监制` closeout 目标 | 阶段边界不再被派生资产反向抢权 |
| 旧经验层仍提示 `4-Design` 要在落盘后起 subagents | context drift layer | 同步更新父层与 leaf `CONTEXT.md` 的经验条目 | 角色边界变更时，同轮更新自动预加载的经验层 | 预加载经验不会把执行者带回旧路径 |
| `2-设计` 的角色 prompt 漂成西方面孔、现代棚拍或全球时尚广告 | worldview fallback 层 | 在角色 builder 加当前项目的人种/地域/世界观硬约束，并把东亚武侠人物画像下沉到角色级 fallback | 在 `design-output-contract.md` 固定 `Worldview Fidelity Gate`，把 `urban-drama / western-face drift` 设为 hard fail token | 角色图不再脱离东亚武侠世界观 |
| `2-设计` 的场景 prompt 被全局词误导，夜市跑成王府/税关/赛博社区 | scene typology fallback 层 | 让场景 builder 先按 `scene_name + aliases + variants + anchors` 判型，再决定 domain defaults | 在共享合同写明场景默认 typology 只能优先跟随当前场景家族，不得被跨项目或跨场景词反向抢权 | 夜市/税关/王府各自回到正确空间家族 |
| `2-设计` 的道具 prompt 只剩 `generic prop` 或被误画成科幻器件 | prop semantic fallback 层 | 在道具 builder 按 `canonical_name` 绑定器物级默认材质/结构/磨损逻辑，并过滤 `unknown` | 在共享合同写明木牌/税单/册子/钱袋等必须先服从器物语义，再允许风格化展开 | 道具图先对器物，再谈风格 |
| 当前项目修好了，但修法直接写死在通用 builder，导致源层继续积累项目私货 | fallback ownership layer | 把项目专属角色/场景/道具 fallback 回收到 `projects/aigc/<项目名>/CONTEXT/4-design-fallback-registry.json`，builder 改为 registry-driven | 在共享输出合同固定“项目专属 fallback 必须归项目级 registry；通用 builder 不得长驻项目私货” | 更换项目时只需替换项目 registry，不再改通用 builder |

## Repair Playbook

1. 先确认 `4-Design` 是否存在真实 stage parent。
2. 再确认当前轮真正命中的 tranche parent 是否存在。
3. 若未全部迁回，不要假设全阶段 active；先把状态写清，再修命中的 leaf。
4. 最后才修具体 leaf 的业务合同。
5. 面板相关问题先查 `3-面板` 父合同和 `_shared` SMART 桥，再查具体 leaf。
6. 若项目根 `team.yaml` 启用顾问团，先判断本轮是否需要前置 advisory；不要在首次落盘后再从 `roles.supervision` 发起 closeout。
7. post-write 问题默认写入阶段 `validation-report.md` 的 audit note；不要在父层偷改派生资产，更不要把它包装成 `监制强化`。
8. 若用户显式要求对 `4-Design` 做落盘后复核，当前也只能记录为 audit/acceptance 需求，不应回退成旧的 `监制` runtime。

## Reusable Heuristics

- 对 `4-Design` 这种多 tranche、多类目的阶段来说，最容易坏的不是某个 leaf，而是“中间父级整层缺失”，然后文档仍假装全量 active。
- 一旦某个 tranche parent 与 leaf 已回迁，就要同步回收父总线的 `pending-migration` 口径；否则 source-layer 会自相矛盾。
- 场景链迁回时要同时看 `1-清单` 三真源与 `2-设计` 场景 leaf；只补 leaf 不改父层 coverage，会让后续路由继续误判为 reserved。
- 当多个 leaf 都想加载同一个不存在的父级时，根因通常不在 leaf，而在 stage parent / tranche parent 没有真正落地。
- `4-Design` 父级最稳的职责是路由、边界和 runtime 对齐，而不是跨类目再造第二真源。
- `3-面板` 的业务真源应停在 layout JSON；自动生图应作为派生动作由 SMART bridge 管理，避免 request/PNG 反向抢真源。
- `2-设计` 的单主体自动图是面板连续性的上游参照，不替代 `3-面板` 的 layout JSON；两类图片要通过路径和 manifest 明确分层。
- 新增 panel leaf 时，不只补 leaf 文件；必须同步父层 coverage、registry leaf_index 与 HARNESS 总览，否则入口层仍会按 pending 处理。
- 角色面板重建时要优先兼容当前 `2-设计/角色` 的 `character_design.json + 逐角色 Markdown + 同 stem 单主体图` 组合；Markdown 只作人读投影，不能反向替代 machine-first 真源。
- `服装` 可继续作为类目宇宙和 `Assets/服装/` 资产库存在；但只要 source leaf 没迁回 active，阶段合同和初始化 skeleton 都不能给出 `4-Design/服装/*` active 落盘路径。
- `4-Design` 里最稳的分层已经改成：`监制` 只做前置 advisory，首次落盘后的收尾直接回到 audit/validation。
- 对 `4-Design` 来说，现在最需要防的是“旧 closeout 语义借 CONTEXT 回流”，而不是再补一层 `监制 refine`。
- `source_skill_refs` 只适合做领域提示，不适合做 `4-Design` post-write 收尾的授权字段。
- 对《笑傲江湖4之风云再再起》这类强世界观项目，`2-设计` 最大风险不是“画得不够精”，而是 leaf 在信息不足时偷吃旧项目 fallback，结果三域一起偏题。
- 当角色缺五官实锚时，宁可用项目内角色专属画像 fallback，也不要把 `unknown_by_shot_evidence` 原样带进 prompt。
- 当场景缺材质/拓扑实锚时，先按当前场景名判夜市/税关/王府家族，再补 typology；不要从项目全局风格里乱捞地理词。
- 当道具缺细节时，先锁器物语义和主材质，再允许风格化；木牌先是木牌，税单先是纸单，钱袋先是布袋，不要直接漂成抽象工业件。
- 项目专属 fallback 若已经稳定，不要继续堆进通用 builder；优先回收到项目根 `CONTEXT/4-design-fallback-registry.json`，让 builder 保持 registry-driven。
