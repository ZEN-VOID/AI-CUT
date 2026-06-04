# Review Gate

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-REVIEW-00` | LibTV intake | LibTV 链接 / project UUID / 画布名 / 目录绑定已解析成唯一 project 和视频节点，远端 node query 已保存，真实视频已通过 `libtv download` 下载为本地可读文件 |
| `GATE-REVIEW-01` | input lock | video path、project root、group_id、variant 已锁定 |
| `GATE-REVIEW-02` | source lock | `5-分组` 中对应组唯一可读 |
| `GATE-REVIEW-03` | real video understanding | 元数据、关键帧 / 联系表、音频说明和 `observed_content_summary` 足以证明已真实理解视频内容 |
| `GATE-REVIEW-04` | video intrinsic review | 基础废片、逻辑合理性、一致性和 AIGC 常见瑕疵已逐项判断 |
| `GATE-REVIEW-05` | prompt alignment | 视频与 prompt / 分镜组的一致性已判断；错配已归因到 prompt、模型、混合原因或证据缺口 |
| `GATE-REVIEW-06` | creative quality | 反平庸、艺术方向、美学完整性和节奏质量有可观察依据 |
| `GATE-REVIEW-07` | example calibration | 用户好/坏示例已按可观察维度比较；未把一次性偏好误写成硬规则 |
| `GATE-REVIEW-08` | 顾问与复核流程 advisor consult | 执行顾问与复核流程时，已按 `team.yaml` 审片监制顾问形成 `review_advisor_packet`，问题绑定当前 node/pass/gate，或使用本地流程 |
| `GATE-REVIEW-09` | compare | expected / actual 明确，不把生成偏差当剧情事实 |
| `GATE-REVIEW-10` | landing | finding 落点和置信度匹配 |
| `GATE-REVIEW-11` | patch scope | 只改 owning source，不顺手改无关组 |
| `GATE-REVIEW-12` | thinking process | 输出含思考过程，说明 why this route |
| `GATE-REVIEW-13` | video naming and handoff | 视频路径、三段式 group_id、variant、扩展名、搜索顺序和 8-视频外部 id 归档方式符合命名合同；命名漂移已显式记录 |
| `GATE-REVIEW-14` | LibTV generation evidence | LibTV `params.prompt`、`imageList/mixedList`、`settings`、`taskInfo`、result URL 与本地 `8-视频` prompt/queue/report 的关系已记录 |
| `GATE-REVIEW-15` | LibTV rerun closure | 重新提交前后 query、clean prompt、task id、result URL、最终 query 和 queue/report 证据齐全 |
| `GATE-REVIEW-16` | method selection | 已在真实视频理解之后按素材信号和用户关注点选择审片方法；底座方法已覆盖，跳过方法有理由 |
| `GATE-REVIEW-17` | operation design | 重要 finding 已转成 candidate operations、chosen operation、拒绝其他操作的理由和闭环证据；operation 与 landing 未混淆 |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-REVIEW-LIBTV-INTAKE` | LibTV project / node / download 无法唯一闭环，或只凭远端 URL / node JSON 做审片 | LibTV Intake Contract + `N0-LIBTV-INTAKE` |
| `FAIL-REVIEW-LIBTV-EVIDENCE` | LibTV 生成路线证据未保存，无法追溯 prompt、imageList、taskInfo 或 result URL | LibTV Intake Contract + `N2-SOURCE-LOCK` |
| `FAIL-REVIEW-LIBTV-RERUN` | 重新提交缺少 prompt hygiene 验证、task id、final query 或 queue/report 回写 | LibTV Intake Contract + `N5-LANDING` / `N6-WRITE` |
| `FAIL-REVIEW-INPUT` | group_id 不明确或视频不可读 | Naming Contract |
| `FAIL-REVIEW-SOURCE` | 找不到对应 `5-分组` | Finding Landing Contract |
| `FAIL-REVIEW-EVIDENCE` | 证据不足以支持结论，或没有先完成真实视频内容分析 | Video Evidence Contract |
| `FAIL-REVIEW-FINDING` | finding 没有 expected/actual/evidence | Review Gate |
| `FAIL-REVIEW-LANDING` | 低置信却改源层 | Source Escalation Contract |
| `FAIL-REVIEW-PROMPT-MATCH` | prompt 错配没有归因，或把 prompt 问题误判成模型问题 | Review Dimensions Contract |
| `FAIL-REVIEW-QUALITY` | 创作质量判断只有口号，没有可观察依据或示例对照 | Example Comparison Learning Contract |
| `FAIL-REVIEW-EXAMPLE-CALIBRATION` | 用户好/坏示例未被锁定角色、未提炼可观察维度、未比较靠近/落入点，或把一次性偏好误写成技能硬规则 | Example Comparison Learning Contract + `N4-COMPARE` / `N6-WRITE` |
| `FAIL-REVIEW-SOURCE-ESCALATION` | 源层升级缺少多例/直接源层证据、未排除普通模型偶发、未定位 source owner、无清晰修复方式，或报告缺少 `Symptom -> Direct Cause -> Source Owner -> Rule Fix` | Source Escalation Contract + `N5-LANDING` |
| `FAIL-REVIEW-PATCH-SCOPE` | `group_repair` 或源层 patch 超出 owning source、顺手改无关组，或把文学重写当成生成稳定性修复 | Finding Landing Contract + `N6-WRITE` |
| `FAIL-REVIEW-REPORT` | 审片报告缺少必填字段、变更文件、思考过程或可回指证据，导致 landing 不可复查 | Finding Landing Contract + report template |
| `FAIL-REVIEW-VERDICT` | 最终 verdict 未综合视频本体、prompt/分镜组匹配和创作质量三层，或阻断级问题仍给 `pass` | Review Dimensions Contract + `N7-VERIFY` |
| `FAIL-REVIEW-ADVISOR` | 执行顾问与复核流程时缺少顾问问题、节点级问题、packet 汇流，或缺少本地流程 | Team Advisor Consultation Contract + SKILL.md Advisor Consultation Mechanism |
| `FAIL-REVIEW-NAMING` | 视频命名无法稳定解析三段式 group_id / variant，扩展名漂移未标注，搜索顺序未记录，或 sessionId / remote task id / provider id 被写入 canonical 文件名 | Video Naming Contract + `N1-INTAKE` / `N7-VERIFY` |
| `FAIL-REVIEW-METHOD-SELECTION` | 未在真实视频理解后选择审片方法，机械套固定流程，漏掉用户关注点或适用的表演/摄影/节奏/声音/道具/安全/AIGC 伪影/候选片比较方法 | Review Method Palette Contract + `N4-COMPARE` / `N4-METHOD-COMPARE` |
| `FAIL-REVIEW-OPERATION-DESIGN` | finding 只有评价或落点，没有候选操作、最终操作、拒绝理由、授权状态或闭环证据 | Review Method Palette Contract + Finding Landing Contract + `N5-LANDING` |
