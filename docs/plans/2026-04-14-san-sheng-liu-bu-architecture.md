# AIGC-DREAM-MAKER 三省六部制改造升级复评包

## 1. 任务模式与目标边界

- 任务模式：`改造升级` 下的二次复评，不是从零原生构建。
- 评估对象：仓库整体 HARNESS 工程，重点是 `.agents/skills/aigc/` 作为核心 suite skill 的实现成色。
- 评估模式：`hybrid`
  - 静态真源：`AGENTS.md`、`HARNESS.md`、`.codex/registry/*`、`.codex/runbooks/*`、`.codex/templates/harness/*`、`.agents/skills/aigc/*`
  - 动态证据：`projects/aigc/2049退休老头的快乐生活/` 运行时样本、`scripts/aigc_harness_audit.py --strict`、`scripts/aigc_skill_audit.py --strict`
- 当前结论：
  - 仓库已经完成 HARNESS bootstrap 基线，不再属于“只有理念、没有载体”的状态。
  - `aigc` 已经是实际运行的总入口，而不是目录说明页。
  - 当前主要矛盾已经从“缺骨架”转为“根投影、review carrier、总览文档与项目样本是否持续同步”。
- 成熟度判断：`bootstrap complete / shadow partial / cutover incomplete`

## 2. 宪章层设计与现状判断

### 2.1 已落地真源

- 根宪章已经明确以 `AGENTS.md` 为第一真源，并把 `projects/aigc/<项目名>/` 固定为 canonical runtime。
- `HARNESS.md` 已被降级为总览投影，不再自称第一真源。
- 三省共享合同、registry、runbook、task carrier、audit 入口都已落地。

关键证据：

- `AGENTS.md` 已将三省六部、bootstrap_compat、runtime canonical 与 rollout 标准固化。
- [HARNESS.md](/Volumes/AIGC/AIGC-DREAM-MAKER/HARNESS.md:5) 明确自己是派生总览，而不是第一真源。
- [scripts/aigc_harness_audit.py](/Volumes/AIGC/AIGC-DREAM-MAKER/scripts/aigc_harness_audit.py:11) 将 HARNESS bootstrap carrier 纳入严格检查。

### 2.2 宪章层结论

- 宪章层强，且已经具备“治理不是比喻”的最低工程形态。
- 当前宪章层的主要问题不是缺规则，而是派生总览仍有局部路径漂移，说明同步链条还未完全收紧。

## 3. 三省治理层设计与现状判断

### 3.1 当前实现

- 中书省：已通过 registry、runbook 与 task carrier 绑定起草流程。
- 门下省：已具备 `review` 卫星技能与 `preflight / acceptance / learning` 三个 subtype。
- 尚书省：已通过 `aigc` 根技能、`query / resume`、项目 runtime 与阶段产物样本体现执行侧控制面。

关键证据：

- [office-governance-contract.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/templates/harness/office-governance-contract.md:15) 已定义 canonical carriers、entry gates、handoff 与 closure。
- [中书省.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/agents/harness治理/中书省.md:29)、[门下省.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/agents/harness治理/门下省.md:27)、[尚书省.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/agents/harness治理/尚书省.md:26) 都已从目录骨架进化为执行合同。
- [aigc 根技能](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/SKILL.md:162) 已把项目级治理工件、卫星桥接与根闭环写入总合同。

### 3.2 三省层结论

- 三省已经“存在且有职责”，不是单 orchestrator 假装分权。
- 但门下省 carrier 口径仍有一个高风险冲突，说明复核链还没有完全和运行样本对齐。

## 4. 六部能力层设计与现状判断

| 能力域 | 当前落点 | 评估 |
| --- | --- | --- |
| 吏部 | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml` | 强。已能登记 stage、satellite、legacy mapping 与 bootstrap_compat。 |
| 户部 | `projects/aigc/<项目名>/STATE.json`、`governance-state.yaml`、`team.yaml` | 强。已经有项目控制面，不再只有聊天态。 |
| 礼部 | `.codex/templates/harness/*`、`_shared/project-runtime-layout.md`、阶段/卫星 `SKILL.md` | 强。carrier 与 shared contract 已成体系。 |
| 兵部 | `resume/`、`task-lifecycle.md`、项目级 `resume_contract` | 中强。已能恢复和续跑，但 preflight 普遍未进入真实项目闭环。 |
| 刑部 | `review/`、两个 audit 脚本、阶段 `validation-report.md` | 中强。已有验收和审计，但 review scope-carrier 有局部漂移。 |
| 工部 | `scripts/aigc_harness_audit.py`、`scripts/aigc_skill_audit.py`、validator 脚本 | 强。已不是手工检查。缺口在 benchmark/regression。 |

## 5. 工件、状态与评测闭环

### 5.1 已跑通的闭环

- HARNESS bootstrap audit 已通过，说明真源载体完整。
- AIGC skill audit 已通过，说明根/阶段/卫星/registry/runtime 的大框架一致。
- 样本项目已经把 `STATE.json + governance-state.yaml + validation-report.md` 用起来，不是纸面合同。

关键证据：

- `python3 scripts/aigc_harness_audit.py --strict`：通过。
- `python3 scripts/aigc_skill_audit.py --strict`：通过，仅 2 条 context hygiene warning。
- [STATE.json](/Volumes/AIGC/AIGC-DREAM-MAKER/projects/aigc/2049退休老头的快乐生活/STATE.json:1) 能给出当前阶段、下一入口与主产物索引。
- [governance-state.yaml](/Volumes/AIGC/AIGC-DREAM-MAKER/projects/aigc/2049退休老头的快乐生活/governance-state.yaml:32) 能给出 checkpoint、resume_contract 与 artifact_status。

### 5.2 闭环仍未完全打通的部分

- 项目样本已使用 `validation-report.md`，但 `mandate / mission-brief / route-plan / preflight / learning` 仍普遍缺失。
- 这意味着系统当前更像“执行态先跑起来，治理工件按需补齐”，而不是所有任务都稳定走完 `起草 -> 预审 -> 执行 -> 验收 -> 沉淀` 全链。

关键证据：

- [governance-state.yaml](/Volumes/AIGC/AIGC-DREAM-MAKER/projects/aigc/2049退休老头的快乐生活/governance-state.yaml:40) 中 `mandate / mission_brief / route_plan / preflight_verdict / learning_record` 仍为 `absent`。
- 同文件 [51-54 行](/Volumes/AIGC/AIGC-DREAM-MAKER/projects/aigc/2049退休老头的快乐生活/governance-state.yaml:51) 显示 `review_bridge` 仍是 `not_started`。

结论：

- HARNESS 已有“载体闭环”和“项目状态闭环”。
- 但“完整三省工件闭环”仍只部分落地，尚未进入全面 cutover。

## 6. 风险、反官僚化约束与验收标准

### 6.1 最高风险点

1. `review` 体系对 `2-Global` 的 acceptance carrier 与真实项目样本冲突。
2. `HARNESS.md` 仍残留旧的 `projects/<项目名>/` 总览口径，和真正真源 `projects/aigc/<项目名>/` 不一致。
3. 动态评测仍主要依赖单项目样本与静态审计，benchmark/regression 证据不足。

### 6.2 反官僚化判断

- 当前系统没有落入“多角色纯传话”。
- 主要原因是：
  - `aigc` 根技能已经承担总路由和唯一下一入口职责；
  - `query / resume / review` 作为卫星技能被显式隔离；
  - 项目运行时样本已经能直接驱动下一步，而不是只靠 office 文档想象。

### 6.3 当前验收标准

- 若要把当前仓库判为 `shadow 完成`，至少还需要满足：
  - review carrier 全仓口径统一；
  - `HARNESS.md` 与真源路径完全同步；
  - 至少 1 套 benchmark/regression 级动态评测被加入根级质量证据链；
  - 至少 1 个真实项目把 preflight / learning 两条门下省 carrier 跑通。

## 7. 现状诊断与 Layered Trace

### Finding P0: `2-Global` 验收 carrier 存在系统性漂移

- 症状：
  - `review` 体系把 `2-Global` acceptance 指向 `3-Detail/validation-report.md`。
  - 真实项目样本与 audit 期望却已把 `2-Global/validation-report.md` 作为独立 carrier。
- 直接原因：
  - `review/`、`acceptance-review/`、`review-modes.md`、`council-runtime`、`team.template.yaml` 与项目样本没有同步完。
- Rule Source：
  - [review/SKILL.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/review/SKILL.md:97)
  - [acceptance-review/SKILL.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/review/subtypes/acceptance-review/SKILL.md:15)
  - [review-modes.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/review/references/review-modes.md:31)
  - [council-runtime/module-spec.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/_shared/council-runtime/module-spec.md:32)
  - [team.template.yaml](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/_shared/council-runtime/team.template.yaml:57)
- Meta Rule Source：
  - [scripts/aigc_skill_audit.py](/Volumes/AIGC/AIGC-DREAM-MAKER/scripts/aigc_skill_audit.py:91)
  - [STATE.json](/Volumes/AIGC/AIGC-DREAM-MAKER/projects/aigc/2049退休老头的快乐生活/STATE.json:25)
  - [2-Global/validation-report.md](/Volumes/AIGC/AIGC-DREAM-MAKER/projects/aigc/2049退休老头的快乐生活/2-Global/validation-report.md:1)
- 立即修复：
  - 统一 `2-Global` acceptance carrier 到单一真源。
  - 我建议以 `2-Global/validation-report.md` 为准，因为运行样本、project_state 与 audit 已经站在这一侧。
- 系统预防修复：
  - 把 `COUNCIL_STAGE_REVIEW_PATHS`、`review` scope mapping、`team.template.yaml` 与 `review` 子技能共收束到一个 shared review carrier 真源，避免五处平行维护。

### Finding P1: `HARNESS.md` 派生总览仍有 runtime 路径漂移

- 症状：
  - `HARNESS.md` 多处仍写 `projects/<项目名>/`。
- 直接原因：
  - 总览投影没有跟 `AGENTS.md + registry + runbook + root skill` 的路径口径同步完。
- Rule Source：
  - [HARNESS.md](/Volumes/AIGC/AIGC-DREAM-MAKER/HARNESS.md:40)
  - [HARNESS.md](/Volumes/AIGC/AIGC-DREAM-MAKER/HARNESS.md:92)
- Meta Rule Source：
  - [AGENTS.md](/Volumes/AIGC/AIGC-DREAM-MAKER/AGENTS.md:50)
  - [registry/skills.yaml](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/registry/skills.yaml:12)
  - [routes.yaml](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/registry/routes.yaml:30)
- 立即修复：
  - 把 `HARNESS.md` 全量同步为 `projects/aigc/<项目名>/`。
- 系统预防修复：
  - 将 `HARNESS.md` 纳入一次“路径 canonical scan”，专门检查 `projects/<项目名>/` 漂移。

### Finding P2: 三省 carrier 闭环尚未在真实项目里全面消费

- 症状：
  - 项目样本已有 `project_state`、`governance-state`、阶段 `validation-report`，但缺 `mandate / mission-brief / route-plan / preflight / learning`。
- 直接原因：
  - 当前仓库处于 `bootstrap_compat`，执行链优先、治理工件后补。
- Rule Source：
  - [aigc/SKILL.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/SKILL.md:160)
  - [project-runtime-layout.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/_shared/project-runtime-layout.md:15)
- Meta Rule Source：
  - [task-lifecycle.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/runbooks/task-lifecycle.md:8)
  - [office-governance-contract.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/templates/harness/office-governance-contract.md:24)
- 立即修复：
  - 至少选一个真实项目，把 `preflight-verdict.yaml` 和 `learning-record.md` 正式跑通。
- 系统预防修复：
  - 在 `resume/review` 与后续项目模板里加入“高风险动作前必须补 preflight、完成验收后必须可选生成 learning” 的实战门。

### Finding P3: 质量证据链仍偏静态，benchmark 缺位

- 症状：
  - 根技能已改正为“benchmark-suite 待补”，但仓内尚无 AIGC 根级 benchmark suite。
- 直接原因：
  - 当前质量证明仍依赖静态审计 + 单项目样本。
- Rule Source：
  - [aigc/SKILL.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/SKILL.md:178)
  - [creative-skill-package-evaluation.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/runbooks/creative-skill-package-evaluation.md:22)
- Meta Rule Source：
  - [AIGC技能质量评估专家](/Volumes/AIGC/AIGC-DREAM-MAKER/.codex/agents/aigc/质评组/AIGC技能质量评估专家.md:118)
- 立即修复：
  - 增加根级 benchmark suite，先覆盖 `baseline + regression`。
- 系统预防修复：
  - 把 benchmark suite 纳入 root suite 发布门槛，而不是只靠 audit pass。

### Finding P3: `6-Video` 两个叶子 `CONTEXT.md` 仍残留 Case Log

- 症状：
  - `scripts/aigc_skill_audit.py --strict` 仅有的两条 warning 都落在 `6-Video/1-提示词蒸馏/全能参照` 与 `首帧参照`。
- 直接原因：
  - `CONTEXT.md` 已切知识库模式，但局部仍保留 milestone case。
- Rule Source：
  - [全能参照/CONTEXT.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md:1)
  - [首帧参照/CONTEXT.md](/Volumes/AIGC/AIGC-DREAM-MAKER/.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md:1)
- Meta Rule Source：
  - 根 `AGENTS.md` 的 rollout / context hygiene 规则
  - `scripts/aigc_skill_audit.py`
- 立即修复：
  - 将 Case Log 迁到 `CHANGELOG.md` 或 `reports/`。
- 系统预防修复：
  - 保持 `CONTEXT.md` 只留 Type Map / Playbook / Heuristics。

## 8. 旧结构到新结构映射表

| 现有对象 | 当前职责 | 当前问题 | 目标归属 | 迁移动作 |
| --- | --- | --- | --- | --- |
| 根 `AGENTS.md` + registry + runbook + templates | 宪章与 HARNESS 真源 | 基本稳定 | 宪章层 | 保持单一真源，不再分裂 |
| `HARNESS.md` | 总览投影 | 路径口径未完全同步 | 派生层 | 同步到 `projects/aigc/<项目名>/` |
| `.agents/skills/aigc/SKILL.md` | suite router + root closure | 正在快速进化，仍有未提交改动 | 中书/总控层 | 继续承担唯一下一入口与根投影同步 |
| `query / resume / review` | 卫星桥接 | 已成立，但 `review` carrier 口径漂移 | 尚书/门下旁路层 | 统一 carrier 真源 |
| `STATE.json + governance-state.yaml` | 项目控制面 | 强，但三省全工件未普及 | 户部控制面 | 在实战中补 preflight / learning |
| `validation-report.md` 链 | 阶段验收证据 | `2-Global` carrier 有歧义 | 刑部 carrier | 统一 scope-carrier mapping |
| audit 脚本 | bootstrap 与 skill 树审计 | 强，但不等于 benchmark | 工部 | 增补动态评测 |

## 9. 迁移阶段与防回归方案

### Phase A: Sync Repair

- 目标：先消灭根层与 review 层漂移。
- 必做：
  - 统一 `2-Global` acceptance carrier。
  - 同步 `HARNESS.md` 的 runtime 路径。
  - 清理 `6-Video` 两个 `CONTEXT.md` 的 Case Log。
- 验收：
  - `rg "projects/<项目名>/" HARNESS.md` 归零。
  - `review/* + council-runtime + team.template.yaml + project sample` 对 `2-Global` carrier 完全一致。

### Phase B: Shadow Hardening

- 目标：让真实项目开始消费完整三省工件链。
- 必做：
  - 选一个真实项目补跑 `preflight-verdict.yaml`。
  - 至少生成一次 `learning-record.md`。
  - 让 `review_bridge` 不再长期停在 `not_started`。
- 验收：
  - 项目根可读回 `preflight + validation + learning` 三件套中的至少两件。

### Phase C: Dynamic Evaluation

- 目标：从“能审计”升级到“可回归验证”。
- 必做：
  - 新增 `aigc` 根级 benchmark suite。
  - 至少覆盖 `baseline + regression`。
  - 将关键 stage/satellite 路由纳入动态样本验证。
- 验收：
  - 质量证据不再只靠结构 audit 和单项目观测。

## 10. 总结论

- 当前仓库在 harness engineering 上，已经明显超过“初始化口号期”，属于真正有骨架、有载体、有项目控制面、有审计入口的系统。
- `.agents/skills/aigc` 已经成为真实的 suite router，并通过 `query / resume / review` 把旁路治理能力显式化，这是当前系统最成功的部分。
- 当前最值得优先修的不是再加更多阶段或更多 agent，而是修复少数几个高杠杆同步漂移点，尤其是：
  - `2-Global` review carrier
  - `HARNESS.md` runtime 路径投影
  - preflight / learning 在真实项目中的消费
  - benchmark/regression 证据链
- 若这四项补齐，系统就能从 `bootstrap complete / shadow partial` 向 `shadow stable` 推进。
