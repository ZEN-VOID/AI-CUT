# AIGC Skill Quality Evaluation

```yaml
evaluation_meta:
  evaluator: AIGC技能质量评估专家
  scope: root-suite
  target_paths:
    - .agents/skills/aigc
  confidence: high
  output_landing: reports/aigc-skill-quality-evaluation-20260410.md

type_profile:
  target_kind: root-suite
  governance_tier: full
  lifecycle_status: active-with-rework
  canonical_runtime: projects/<项目名>/
  primary_truth_source: .agents/skills/aigc/_shared/project-runtime-layout.md

scorecard:
  covenant_compliance:
    score: 8
    band: 好
    evidence:
      - 根技能、阶段技能、governed leaf 基本都具备 SKILL.md + CONTEXT.md + Root-Cause 合同
      - scripts/aigc_skill_audit.py --strict 返回 failures: 0
      - 根 CONTEXT 健康度仍在阈值内，约 22740 chars / 19 cases
    why_it_matters: 合同壳体已经成形，说明这棵技能树不是“空目录 + 漂亮表格”。
  goal_fit:
    score: 9
    band: 优秀
    evidence:
      - 根技能明确定位为总入口、总路由、总闭环
      - 5-画面、6-视频 等阶段边界与上下游关系表达清楚
      - registry 与 HARNESS 都把 aigc 视为仓库级总入口
    why_it_matters: 这套合同明显是围绕 AIGC 影视创作工作台设计，而不是 generic skill 模板。
  source_governance:
    score: 6
    band: 一般
    evidence:
      - _shared/project-runtime-layout.md 声明 5-画面 -> projects/<项目名>/画面/，6-视频 -> projects/<项目名>/视频/
      - 5-画面/SKILL.md 改写为 projects/<项目名>/5-画面/
      - 1-规划/SKILL.md 同时出现 projects/<项目名>/1-规划/ 与 projects/<项目名>/Init/ 两套落点
    why_it_matters: runtime 真源出现并行定义后，父级、leaf、CONTEXT 与 future scripts 都会被迫猜测“哪份才算真源”。
  executability:
    score: 8
    band: 好
    evidence:
      - 根技能、1-规划、5-画面、6-视频 都给出唯一主入口与停止条件
      - 5-画面 与 6-视频 的 references 分拆清楚，执行者可按模块补证据
      - 7-后期 已明确标记为搁浅，不会误入伪执行链
    why_it_matters: 大多数执行者已经能根据合同直接选阶段、定入口、找落点。
  differentiation_and_feedback:
    score: 8
    band: 好
    evidence:
      - 维度体系能区分根层、阶段层、leaf、shared carrier、agent metadata
      - 根技能与阶段技能都有 field / pass / rework 结构
      - 本轮问题能被压缩成少数高杠杆动作，而不是散点吐槽
    why_it_matters: 反馈能直接服务下一轮修补，而不是只留下抽象印象分。
  anti_drift:
    score: 6
    band: 一般
    evidence:
      - strict audit 只验证壳体、registry 与最小合同，不验证 runtime 路径一致性
      - CONTEXT 已记录“5-画面 landing 改到 projects/<项目名>/5-画面/”，但 _shared layout 仍保留 projects/<项目名>/画面/
      - 1-规划 的主合同、leaf、CONTEXT 之间仍保留旧/新路径混写
    why_it_matters: 这会产生“审计绿灯但真源已分裂”的假稳定状态。
  cross_layer_sync:
    score: 6
    band: 一般
    evidence:
      - root / shared layout / stage contracts / CONTEXT 的 runtime 路径未完全同步
      - registry 与 HARNESS 已同步 6-视频 active、7-后期 shelved，但没有继续下钻到阶段落点一致性
      - 1-规划 在 When to Use、Canonical Landing、Field Master、validation 路径之间互相打架
    why_it_matters: 根入口虽然能路由，但跨层回写尚未彻底完成，容易在继续扩树时复发。

improvement_priorities:
  - priority: P0
    issue: runtime canonical landing 仍存在多份并行真源
    action: 先明确单一 authoritative mapping，然后统一 root SKILL、_shared/project-runtime-layout、阶段 SKILL、references、CONTEXT 的 runtime 路径口径；不得继续让 `Init/画面/视频/设定` 与 `1-规划/5-画面/4-主体` 两套命名并行演化
    landing_point: .agents/skills/aigc/_shared/project-runtime-layout.md
    expected_gain: 一次性消除跨层路径歧义，降低后续 leaf、模板、脚本和项目落盘的系统性漂移
  - priority: P1
    issue: 审计脚本未覆盖 runtime 路径一致性，导致“failures: 0”与实际漂移并存
    action: 为 scripts/aigc_skill_audit.py 增加 runtime mapping consistency checks，至少对 root SKILL、shared layout、阶段 SKILL/references、registry/HARNESS 做比对
    landing_point: scripts/aigc_skill_audit.py
    expected_gain: 让未来同类漂移在审计阶段暴露，而不是靠人工复核才发现
  - priority: P1
    issue: 1-规划 是当前最明显的示范性冲突点，既影响父级路由，也会误导后续 leaf 落盘
    action: 先把 1-规划 的 When to Use、职责边界、Visual Maps、子路径路由矩阵、Field Master、validation 路径统一到同一 runtime 方案，再回写对应 CONTEXT 与 leaf 引用
    landing_point: .agents/skills/aigc/1-规划/SKILL.md
    expected_gain: 先修最显眼的入口冲突点，给后续 4-主体/5-画面/6-视频 的口径收束提供模板

gate_summary:
  verdict: PASS-WITH-REWORK
  total_score: 51
  max_score: 70
  top_risk: strict audit 未覆盖 runtime 真源一致性，导致路径漂移可长期潜伏
  anti_gaming_flags:
    - strict audit 绿灯不等于 runtime 真源单一
    - CONTEXT 与 shared layout 已出现相互竞争的路径记忆
  repair_entry: 先统一 canonical runtime mapping，再补审计器，然后按统一口径回写阶段合同

closure:
  root_cause_location: .agents/skills/aigc/_shared/project-runtime-layout.md + .agents/skills/aigc/1-规划/SKILL.md + scripts/aigc_skill_audit.py
  immediate_fix: 选择单一 runtime 命名体系并回写 root/shared/stage/references 的路径合同
  systemic_prevention_fix: 在 scripts/aigc_skill_audit.py 中新增 runtime mapping consistency audit，阻止未来再出现“合同完整但真源分裂”
  layered_trace:
    symptom: strict audit 通过，但 1-规划、5-画面、4-主体 与 shared runtime layout 出现不同 canonical landing
    direct_cause: runtime 路径合同被复制到多个层次并独立演化，现有审计只查壳体和最小注册关系
    rule_source: .agents/skills/aigc/_shared/project-runtime-layout.md, .agents/skills/aigc/1-规划/SKILL.md, .agents/skills/aigc/5-画面/SKILL.md, scripts/aigc_skill_audit.py
    meta_rule_source: 根 AGENTS.md 的 Root-Cause First + Canonical Source Governance 合同
    fix_landing_points:
      - .agents/skills/aigc/_shared/project-runtime-layout.md
      - .agents/skills/aigc/SKILL.md
      - .agents/skills/aigc/1-规划/SKILL.md
      - .agents/skills/aigc/4-主体/SKILL.md
      - .agents/skills/aigc/5-画面/SKILL.md
      - scripts/aigc_skill_audit.py
```

## Key Evidence

- `_shared/project-runtime-layout.md` 仍把 `1-规划` 固定到 `projects/<项目名>/Init/`，把 `4-主体/5-画面/6-视频` 固定到 `projects/<项目名>/设定/画面/视频/`。
- `1-规划/SKILL.md` 同时声明：
  - `projects/<项目名>/1-规划/` 是阶段产物与验证报告目录；
  - `projects/<项目名>/Init/` 是 canonical landing；
  - `projects/<项目名>/1-规划/validation-report.md` 与 `projects/<项目名>/Init/validation-report.md` 两套路径并存。
- `5-画面/SKILL.md` 已把 canonical landing 重写为 `projects/<项目名>/5-画面/`，与 shared runtime layout 的 `projects/<项目名>/画面/` 不一致。
- `scripts/aigc_skill_audit.py --strict` 通过，但脚本当前只检查：
  - governance_tier / Root-Cause / field-pass 表存在性；
  - CONTEXT 的基础章节；
  - registry 与 routes 的最小锚点；
  - active/shelved 阶段基础存在性；
  - 并未检查 shared runtime mapping 与 stage landing 是否一致。

## Bottom Line

这棵 `.agents/skills/aigc` 技能树已经不是“空壳”。它的边界、阶段链、shared carrier、Root-Cause 合同和大部分 leaf 可执行性都已经达到了可复用水平，因此不该判成 `FAIL`。

但它现在还不是“优秀”。最关键的缺口不是内容贫乏，而是 canonical runtime 治理还没有真正收束成单一真源，且审计器尚未覆盖这类漂移。所以本轮结论是 `PASS-WITH-REWORK`，最高优先级是先修 runtime 真源与审计闭环，而不是继续盲目扩 leaf。
