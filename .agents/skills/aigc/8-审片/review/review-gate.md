# Review Gate

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-REVIEW-01` | input lock | video path、project root、group_id、variant 已锁定 |
| `GATE-REVIEW-02` | source lock | `4-分组` 中对应组唯一可读 |
| `GATE-REVIEW-03` | real video understanding | 元数据、关键帧 / 联系表、音频说明和 `observed_content_summary` 足以证明已真实理解视频内容 |
| `GATE-REVIEW-04` | video intrinsic review | 基础废片、逻辑合理性、一致性和 AIGC 常见瑕疵已逐项判断 |
| `GATE-REVIEW-05` | prompt alignment | 视频与 prompt / 分镜组的一致性已判断；错配已归因到 prompt、模型、混合原因或证据缺口 |
| `GATE-REVIEW-06` | creative quality | 反平庸、艺术方向、美学完整性和节奏质量有可观察依据 |
| `GATE-REVIEW-07` | example calibration | 用户好/坏示例已按可观察维度比较；未把一次性偏好误写成硬规则 |
| `GATE-REVIEW-08` | subagents advisor consult | 启动 subagents 模式时，已按 `team.yaml` 审片监制顾问形成 `review_advisor_packet`，问题绑定当前 node/pass/gate，或完整记录上层阻断降级 |
| `GATE-REVIEW-09` | compare | expected / actual 明确，不把生成偏差当剧情事实 |
| `GATE-REVIEW-10` | landing | finding 落点和置信度匹配 |
| `GATE-REVIEW-11` | patch scope | 只改 owning source，不顺手改无关组 |
| `GATE-REVIEW-12` | thinking process | 输出含思考过程，说明 why this route |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-REVIEW-INPUT` | group_id 不明确或视频不可读 | Naming Contract |
| `FAIL-REVIEW-SOURCE` | 找不到对应 `4-分组` | Finding Landing Contract |
| `FAIL-REVIEW-EVIDENCE` | 证据不足以支持结论，或没有先完成真实视频内容分析 | Video Evidence Contract |
| `FAIL-REVIEW-FINDING` | finding 没有 expected/actual/evidence | Review Gate |
| `FAIL-REVIEW-LANDING` | 低置信却改源层 | Source Escalation Contract |
| `FAIL-REVIEW-PROMPT-MATCH` | prompt 错配没有归因，或把 prompt 问题误判成模型问题 | Review Dimensions Contract |
| `FAIL-REVIEW-QUALITY` | 创作质量判断只有口号，没有可观察依据或示例对照 | Example Comparison Learning Contract |
| `FAIL-REVIEW-ADVISOR` | 启动 subagents 模式时缺少真实顾问 dispatch、节点级问题、packet 汇流，或缺少降级说明 | Team Advisor Consultation Contract + SKILL.md Subagents Execution Mechanism |
