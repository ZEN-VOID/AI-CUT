# Changelog

## 2026-06-11

- 同步 `2-美学` 输出 scope：分镜阶段读取 `画面基调` 全局 singleton；分镜风格按当前 `第N集` 优先读取 `2-美学/第N集/分镜风格/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`README.md` 与 agent prompt，辅助摄影/角色/场景风格也采用逐集优先、项目级回退。

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求分镜拆分证明上游画面点、心理/表演/氛围字段和 `2-美学` 如何投影为节拍、构图、空间层次和时值。
- 新增 `FAIL-SB-UPSTREAM-CONTEXT`、`GATE-SB-24` 和报告 `Upstream Context Application Map`，并将审查门扩展到 `GATE-SB-01..24`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-04

- 初始化 `aigc/6-分镜` Skill 2.0 runtime-spine 包。
- 明确分镜时码以 0.5 秒为最小颗粒，`N-N秒` 中的 `N` 可为整数或 `.5` 小数；同步 `SKILL.md`、`CONTEXT.md`、duration reference、README、agent prompt 和测试 prompt，避免整数秒模板化。
- 默认承接 `5-导演/第N集.md`，并允许用户指定 source override。
- 新增 `2-美学/画面基调` 与 `2-美学/分镜风格` 为必读上下文。
- 将旧 `4-摄影` 的画面匹配、节拍、构图、景深、时值、计划汇流和连续性合同重构为 `6-分镜/references/` 下的 4 个专用细则。
- 输出格式收束为每个画面点先写 `节拍量化：beat=N（beat1: BT-xx...）`，再写 `分镜N（N-N秒）：景别，景深，构图形式，前景，中景，后景，主体站位。`；移除主体陪体背景长描述字段，避免重复上游画面正文。
- 新增 `knowledge-base/shot-composition-taxonomy.md`，将构图方式收束为受控摄影构图词表，并同步 `SKILL.md`、`shot-composition-contract.md`、`CONTEXT.md`、`README.md` 与测试 prompt，避免构图字段随机化或被画面描述替代。
- 移除分镜数量范围、复杂动作上限和 set-piece 上限口径；源层规则收束为“有效画面节拍数 = 分镜数”。
- 新增正文 `节拍量化：beat=N（beat1: BT-xx...）` 行；`beat=N` 即有效画面节拍数，分镜数必须匹配 `shot_count_decision` 和实际分镜条数；`BT` 只作为各 beat 的触发依据，并由 `GATE-SB-21` 审查。
- 明确 beat 计算协议：`beat=N` 必须由 `candidate_trigger_set -> state_change_cluster_map -> beat_count_formula` 得出，禁止字段类型、静态/动态分类、动作复杂度标签、经验数量范围、BT 标签数量或脚本规则直接决定 beat 数。
- 新增 `GATE-SB-23` / `FAIL-SB-BEAT-CALCULATION-DRIFT`，作为 beat 计算漂移专项验收门；执行报告新增 `Beat Calculation Audit` 证据要求。
- 新增 `references/start-frame-spatial-continuity-contract.md`，要求先从单个画面点解析 `spatial_field_map`，再用 `within_point_spatial_continuity_map` 约束同一画面点多条分镜的前景/中景/后景/主体站位连续性。
- 新增 `GATE-SB-22` / `FAIL-SB-SPATIAL-CONTINUITY-WITHIN-POINT`，阻断同一画面点内空间层次或主体站位无解释跳变。
