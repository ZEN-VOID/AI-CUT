# Query Workflow

`query/` 的步骤必须同时表达判断、动作、证据和失败回路。

## Node Network

| node_id | input | judgment | action | output | fail route |
| --- | --- | --- | --- | --- | --- |
| `N0-load-contract` | 用户查询 | 是否命中 `$aigc-query` | 加载 `SKILL.md + CONTEXT.md` | loaded contract | missing context -> report baseline gap |
| `N1-project-root` | cwd、用户路径、项目名 | 是否唯一定位项目根 | 锁定 `projects/aigc/<项目名>/` | `project_root_lock` | multiple candidates -> ask project name |
| `N2-truth-role` | 用户问题 | 主 truth role 是哪类 | 查 `types/query-type-map.md` | `type_profile` | ambiguous -> split primary/secondary |
| `N3-carrier-read` | `type_profile` | 哪些 carrier 有资格回答 | 读 canonical carrier | `evidence_pack` | carrier missing -> legacy fallback or gap |
| `N4-validation-crosscheck` | `evidence_pack` | 是否涉及完成/通过 | 补读验收/执行报告 | `status_distinction` | no report -> mark not evidenced |
| `N5-governance-crosscheck` | 制度类问题 | registry/routes 是否需要参与 | 读 registry/routes/stage skill | `governance_evidence` | drift -> report conflict |
| `N6-answer` | all evidence | 输出是否覆盖四字段 | 按模板输出 | final answer | incomplete -> return to missing node |

## Project Root Guard

允许的判定顺序：

1. 若当前工作目录位于 `projects/aigc/<项目名>/` 下，取最近祖先目录。
2. 若用户给出项目名，使用 `projects/aigc/<项目名>/`。
3. 若用户给出绝对或相对项目路径，确认该路径包含 `STATE.json`、`MEMORY.md`、`0-初始化/` 或任一阶段目录。
4. 若 `projects/aigc/` 下只有一个候选项目，可谨慎推断并在回答中说明。
5. 多候选时停止追问，不能全仓扫后混答。

## Evidence Gate

- 每个结论至少带一个可复核路径。
- 每个“完成/通过”结论至少带一个验收或执行报告证据。
- 每个“缺失”结论必须说明查过的 canonical path。
- 每个“legacy fallback”结论必须说明对应 current canonical path。
