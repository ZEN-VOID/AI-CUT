# CONTEXT.md

本文件是 `aigc/query` 的经验层知识库，不是执行日志。它保存 truth-role 判定、真源选路、冲突拆分和查询回答中的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-04-26
```

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 把 `.agents/skills/aigc/` 当成项目结果目录 | project-root guard | 先定位 `projects/aigc/<项目名>/` | 在 `SKILL.md#Thinking-Action Node Map` 固定 root lock | 证据路径落在真实项目根 |
| 沿用旧 `3-Detail` 或 `2-编导` 查询当前编导主文件 | stage migration layer | 按意图改查 `2-编剧/第N集.md`、`4-导演/第N集.md` 或 `5-表演/第N集.md`，必要时标注 legacy fallback | 在 `references/project-runtime-layout.md` 固定 current/legacy 映射 | 回答同时说明 canonical owner 与 legacy source |
| 查询视觉资产时混用 `4-Design/5-Image/6-Video` | runtime naming layer | 新链路查 `11-主体/12-图像/13-画布` | 在 data-flow 表中保留 legacy only 字段 | 不把 legacy 当默认输出 |
| 把文件存在当作验收通过 | validation distinction | 补读 `validation-report.md` 或 `执行报告.md` | review gate 固定“存在不等于 PASS” | 答复明确区分存在/通过 |
| 问当前断点时只看目录结构 | governance carrier layer | 读 `governance-state.yaml`、`STATE.json` 与初始化核心工件 | system data flow 固定治理 carrier 顺序 | 结论带治理载体证据 |
| 问制度路由时只扫项目目录 | registry route layer | 读取 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml` | `governance_system` mode 固定 registry first | 能指出制度层漂移 |
| 轻量初始化态被误判为治理失败 | init layering layer | 确认 `STATE.json`、`0-初始化/`、`MEMORY.md` 与 `CONTEXT/` | data-flow 写清 core first, governance lazy | 回答为“轻量初始化态” |
| 查询结论像脚本模板 | scripted conclusion layer | 标记 `FAIL-QUERY-SCRIPTED-CONCLUSION`，回到 carrier 证据和 status distinction 重判 | scripts 只列路径和字段，不生成判断 | 答复能说明证据如何支撑结论 |

## Repair Playbook

1. 任何查询先锁 `PROJECT_ROOT`，再判定 truth role。
2. 用户问“有没有 / 在哪”时回答产物存在；用户问“完成了吗 / 通过了吗”时必须补查验收载体。
3. 用户问“为什么路由到这里”时，优先查 registry/routes，再查阶段 `SKILL.md`。
4. 新 `aigc` 链路以当前中文阶段名为 canonical；旧英文阶段名与旧 `2-编导 / 3-运动 / 4-摄影` 只作为 legacy compatibility。
5. 若 registry 中残留旧路径而本地技能树不存在，应把它作为制度层漂移报告，不要沉默纠正。
6. 若查询发现可复用失败模式，先写入本 `CONTEXT.md`；稳定后再晋升到 `SKILL.md` 或 `references/`。
7. 脚本输出只能作为 evidence pack；最终“存在/完成/通过/下一入口”必须由 LLM 按证据区分裁决。

## Reusable Heuristics

- `query/` 的价值不是全仓搜索，而是先回答“哪个文件有资格回答这个问题”。
- 对项目事实，`projects/aigc/<项目名>/` 高于 registry；对制度事实，registry/routes 高于项目目录。
- 新链路阶段名以当前 `.agents/skills/aigc` 真实目录为准：`0-初始化`、`1-分集`、`2-编剧`、`3-美学`、`4-导演`、`5-表演`、`6-氛围`、`7-分镜`、`8-摄影`、`9-光影`、`10-分组`、`11-主体`、`12-图像`、`13-画布`、`14-审片`；旧 `2-编导`、`3-运动`、`4-摄影` 只作 legacy fallback。
- `STATE.json` 是轻量状态入口，`governance-state.yaml` 是结构化治理快照；两者不得被解释成彼此的替代品。
- 没有 `validation-report.md` 或阶段 `执行报告.md` 时，只能说“未见验收证据”，不能说失败或通过。
- 查询回答的四字段齐全不等于可信；如果结论只是把路径扫描结果套模板，应返工到 `Q6/Q7`。
