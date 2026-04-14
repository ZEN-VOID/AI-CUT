# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `6-视频/3-视频生成` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/6-Video/3-视频生成/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 请求对象还没稳定，却直接组织提交计划 | 输入完备性层 | 停止并回到命中的 `1-提示词蒸馏/*` 子技能 | 在本层固定 `request_ready` 检查，不允许空转 handoff | `submit-plan.json` 的 source request 可追溯 |
| provider 目录存在就被误判为本地可执行 skill | provider 槽位语义层 | 把 provider 目录收敛为槽位说明，不把其当作能力存在 | 只有出现 `SKILL.md + CONTEXT.md` 的 provider 才算 governed child skill | 不再把空目录当能力存在 |
| 主合同之外仍把规则下沉到 `references/` 或 `providers/README.md` | 真源治理层 | 把字段、流程、路由与输出契约收束回 `SKILL.md` | 保持 `SKILL.md` 为唯一规范真源，其他文件只做经验或说明 | 关键规则不再分散 |
| `2-视频生成` 与 `3-视频生成` 混写 | 路径归一层 | 统一收敛到真实磁盘路径 `.agents/skills/aigc/6-Video/3-视频生成/` | 在父级、根级与经验层同步路径口径 | 不再出现双编号漂移 |
| 只给一句“去用某 provider”，不写 `submit-plan.json` | 输出契约层 | 补齐 `submit-plan.json + submit-brief.md` | 将 handoff 包固定为叶子最低交付 | 计划目录中有完整可读计划 |
| 把上游请求对象中的 `image_ref` 直接当成 Dreamina CLI 的最终 `--image` 参数 | provider 输入解析层 | 先把 `image_ref + ref_kind` 解析成 Dreamina 可上传的本地文件路径，再写入 handoff 包 | 在本层固定 provider-neutral -> provider-specific 的解析责任，避免上游模板再次绑定到某个 CLI 私有字段 | Dreamina handoff 中的参照图输入最终都是可验证的本地路径 |
| 该先做 `2-参照引用` 的请求对象，带着空骨架或半解析引用直接进入 handoff | 引用模式分流层 | 先判定 `reference_driven / prompt_only / unresolved`，`unresolved` 立即回退到 `2-参照引用` | 在本层固定“空引用 ≠ 未解析引用”，避免把该阻断的请求偷偷降级成 prompt-only | handoff 不再混用占位与真实引用 |

## Repair Playbook

1. 先确认本轮目标是否真的属于“提交前组织”。
2. 再确认上游请求 JSON 是否稳定可提交。
3. 再判断 provider 是否已明确，还是只输出推荐与对比。
4. 产出 `submit-plan.json` 与 `submit-brief.md`。
5. 最后给唯一下一入口：外部 provider skill、人工提交，或回上游补请求对象。
6. 收尾复扫是否仍残留 `2-视频生成` 或 `references/` 作为规则真源。

## Reusable Heuristics

- `3-视频生成` 的价值不在“替代 provider”，而在“把提交前的不确定性压缩成可复核的 handoff 包”。
- provider 名称如果只有目录没有合同，就应该被视为槽位，而不是能力。
- 对视频阶段来说，最危险的跳步是“有请求 JSON 就直接下命令”，因为这样会丢失下一入口、失败回放与计划证据。
- 只要字段表、流程或输出契约还散落在 sidecar 文件里，父 skill 就还没有真正升格成单一真源。
- 上游请求对象里的 `image_ref` 只是中性引用，不是任何 provider 的最终参数；对 Dreamina 这类本地上传 CLI，最稳的做法是先下载/解码/落盘，再把本地路径写进 handoff。
- 空引用和未解析引用不是一回事：前者表示“本轮不使用参照图”，后者表示“本轮本来需要参照图但还没完成绑定”；两者的 provider 路由必须分开处理。
