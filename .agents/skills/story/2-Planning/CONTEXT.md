# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 7600
current_lines: 145
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T23:40:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 `2-Planning` 当成 `references/*` 模块集，而不是父 skill + 子技能包 | source contract | 回到父 `SKILL.md` 的 child dispatch 合同 | 在 root docs / workflow labels / child paths 中统一使用子技能包路径 | 不再出现 `references/*/module-spec` 作为执行入口 |
| 子技能只写本地 artifact，没有写 `story_map_patch` | child output contract | 补齐本地模板中的 `story_map_patch` | 在 shared branch contract 固化“evidence artifact + patch”双输出 | 任一 child artifact 都能指出 owned slots |
| 后一 child 没有回读当前 root，导致连续性断裂 | progressive commit | 回到串行 dispatch，强制每步重读 `2-Planning/全息地图.json` | 在父技能硬写 reread rule，并让 validator 检查 root 必备槽位 | 后序 child 读取到前序已提交字段 |
| 父层 normalize 越权重写 1-7 的领域判断 | ownership gate | 把父层压回 normalize-only | 在 shared contract 固定父层只拥有三轴 / cross-thread / lifecycle / actualization | 1-7 的领域结论只会在对应 child 中修改 |
| story_map root 丢失 `content.holomap` 兼容入口 | compatibility contract | 恢复 `content.holomap` 根槽 | 在 shared schema 中把 `content.holomap` 固化为 required | query / drafting 仍可 holomap-first |
| planning 系统只有文档，没有 stage validator | stage completeness | 增加 `validate_story_map_output.py` 最小校验器 | 在父技能 completion contract 与 shared contract 中固定验证入口 | `--help` 可用，样例 root 可被校验 |
| child skill 把 shared branch contract 写成跨出父阶段的一层更高路径，导致读到不存在的 `_shared` | child path governance | 统一改回 `../_shared/planning-branch-output-contract.md` | 约定 child 只可回读父阶段 `_shared/`，不得直接猜根级 `_shared/` 承载 stage-local contract | 7 个 planning child 的 shared contract 路径全部落到 `2-Planning/_shared/` |
| 7 个 child artifact 没有稳定落点，最后只能把 evidence 混回 root JSON | branch artifact carrier | 统一改为 `2-Planning/pass-artifacts/1-7*.json` | 在 `planning_paths.py` 与 shared contract 固定 pass-artifacts 路径组 | 每个 child 的分析结论、patch、gate summary 都可单独回读 |

## Repair Playbook

1. 先问问题是父层顺序门、child output、story_map ownership，还是下游兼容。
2. 若多个 child 后果同时漂移，先查最后一个“没有回读当前 root”的 child。
3. 若 `2-Planning/全息地图.json` 看起来像摘要页，优先区分是 1-7 没有 progressive commit，还是父层 normalize 失效。
4. 若引用路径失效，先做全仓引用同步，不要只修当前文档。
5. 收尾时必须同时验证：evidence artifact、story_map root、validator。

## Reusable Heuristics

- 对 planning 阶段来说，“子技能包化”只有在每个 child 都拥有明确 `story_map` 槽位时才成立；否则只是把 module-spec 换了目录。
- `2-Planning/全息地图.json` 最稳的用法不是最后一次性拼出来，而是让它从 Step 1 开始逐步长出来。
- 若后续 child 质量看似还行但整体连续性很差，首查是否跳过了“回读当前 root”。
- 父层 normalize 最常见的越权，是把收束当成重写前面 1-7 的自由许可；必须始终把它压回 normalize-only。
- planning 真源要兼顾新结构和既有运行时，因此保持 `content.holomap` 比贸然改成新字段名更稳。
- 若 child 要读取 stage-local shared contract，默认先找父阶段的 `_shared/`，不要把路径上溯到根级 `_shared/`。
