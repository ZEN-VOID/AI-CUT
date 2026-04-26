# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/5-设计/1-清单` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/5-设计/1-清单/SKILL.md` 时，应在 `aigc -> 3-Detail -> 1-清单/_shared` 之后加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `场景` 叶子已迁回，但父层仍按 reserved/不可调度处理 | stage coverage 层 | 在父层 `SKILL.md` 把 `场景` 标为 active，并允许 `single-domain` 路由命中该叶子 | 把 coverage 状态、route rule 与 preload 顺序一起维护，避免只改表不改路由 | 父层可直接命中 `场景` leaf |
| `场景 / 角色 / 道具` 各自解释不同的 detail 输入口径 | 共享输入合同层 | 回到 `_shared/detail-output-consumption-contract.md` 统一第一输入根 | 父层 `SKILL.md` 固定 shared input order 与 fallback 规则 | 三个 active leaf 都先读同一份 `3-Detail/第N集.json` |
| 父层在 sibling 未回迁时仍宣称 full-build 可用 | 迁移状态层 | 把 stage coverage 改成 `reserved / pending`，只调度已落地 leaf | 在父层 `SKILL.md` 固定当前轮 active coverage | source-layer 状态不再虚报 |
| `服装` 跳过 `角色清单.json` 直接从导演 JSON 发明对象池 | 依赖门层 | 回退到 `角色 -> 服装` 顺序 | 在父层固定 `服装` 的前置条件与 full-build 顺序 | `服装` 只有在角色清单稳定后才执行 |
| 某个 leaf 试图把三真源写成三份并列总稿或把 manifest 当主稿 | 输出治理层 | 恢复 `清单/研究/bridge` 字段边界 | 在 `_shared/list-output-contract.md` 与父层同步锁定三真源分工 | 没有 `1-清单.json` 总稿或 manifest 承载业务事实 |
| full-build 时四域全串行导致成本过高 | 调度拓扑层 | 回到 `场景 + 角色 + 道具` 先行、`服装` 后置 | 在父层明确“并行可候选 + 依赖门”的调度规则 | 全量构建既满足依赖，又不过度串行 |
| leaf 输出存在，但 `2-设计` 仍需重猜主键 | canonical source 层 | 回查对象池主键与 shot/group 回链 | 在父层验收中强制检查 catalog 与 bridge 的 traceability | 下游直接消费，不再补猜 identity |
| 旧单 catalog 场景口径与当前三真源口径并存 | sibling output 治理层 | 统一回到 `清单 / 研究 / bridge` 三业务真源 | 在 `_shared/list-output-contract.md` 与父层治理表固定三文件字段边界 | `2-设计/场景` 默认读取 `场景清单.json + 场景研究.json + scene_design_bridge.json` |
| 用户要求 `场景/道具/角色` 统一三真源 | canonical output 治理层 | 将 shared contract 从单 catalog 口径改为 `清单 / 研究 / bridge` 三业务真源 | 明确三文件字段边界：清单管 identity，研究管 evidence/research，bridge 管 design handoff，manifest 只做审计 | 三个 leaf 默认输出三份业务 JSON |
| 父层把 leaf 标为 active，但 leaf 实际没有可执行入口 | stage runtime 层 | 先补 leaf pipeline，再做 tri-domain build | 在 leaf `SKILL.md` 固化 `Execution Entrypoints`，并把 dry-run 纳入最小验收 | active coverage 与真实可执行状态一致 |

## Repair Playbook

1. 先确认本轮命中的是哪一个 domain，避免把父层问题误修到某个 leaf。
2. 再检查 `3-Detail` 输入口径是否统一，尤其是 canonical 与 legacy fallback 是否混写。
3. 若命中 `服装`，先检查 `角色清单.json` 是否存在并属于当前 episode。
4. 再核对当前已落地域是否仍遵守 `清单 + 研究 + bridge + manifest` 的分层。
5. 最后才汇总到 `projects/aigc/<项目名>/4-设计/validation-report.md`，记录当前轮 dispatch、缺口与下一入口。

## Reusable Heuristics

- `1-清单` 最容易漂移的不是 leaf 内部抽取，而是父层在迁移窗口里把“规划中的 sibling”误写成“已可调度的 sibling”。
- `场景 / 角色 / 道具` 已经统一到三真源时，不要再保留“单 catalog 承载全部研究”的旧经验；清单管 identity，研究管 evidence，bridge 管 design handoff。
- `服装` 属于跨域消费链，因此父层必须显式守住 `角色 -> 服装` 的依赖门。
- 对父层来说，最稳的交付不是“再汇总一份总稿”，而是保证四个 domain catalog 都能被 `2-设计` 直接读取。
- `全量构建` 不等于“所有 leaf 都串行”; 真正的顺序约束只有依赖门，剩余应以 selective dispatch 降低成本。
- stage-level `validation-report.md` 只应记录 coverage、缺口和 handoff，不应回写 domain 事实。
- 当用户明确要求三真源时，不能只改 leaf；必须同步 shared output contract、父层 governance、leaf manifest 与脚本默认输出，且三文件要用字段边界避免互相抢真源。
- 父层 coverage 表只能声明“已可执行”的 leaf；active 状态至少要有一个稳定的 run 脚本和 dry-run 自检路径。
