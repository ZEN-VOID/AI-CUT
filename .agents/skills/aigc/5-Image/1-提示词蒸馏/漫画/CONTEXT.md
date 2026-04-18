# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `.agents/skills/aigc/5-Image/SKILL.md + CONTEXT.md` 与 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md` 之后加载本文件。
- 本技能当前已取消 `references/` 规范载体；经验层只保留在 `CONTEXT.md`。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
current_chars: 5898
current_lines: 111
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-12T20:25:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把图片落盘当主产物 | 输出合同层 | 回退到 `第N集.json` 漫画图像请求集合 | 在 `SKILL.md` 的 `Convergence Contract` 与 `One-Shot Output Contract` 固化“json 为主，生成后置” | 主产物指向 `第N集.json` |
| `prompt` 没有固定漫画前缀 | Prompt 合同层 | 重新按固定前缀 + `comic_page_group` 拼接 | 在 `SKILL.md` 的 `Prompt Assembly Rules` 固化前缀逐字保留 | `prompt` 开头逐字一致 |
| `comic_page_group` 漏掉组级或镜级内容 | 输入覆盖层 | 回到 shared schema 重新提取分镜组内容 | 在 `SKILL.md` 的 `Field Master` 与 `Mandatory Workflow` 固化完整覆盖要求 | 可回链 `剧本正文 + 组间设计 + 分镜明细[]` |
| 图像侧模板字段被删掉或乱改 | 请求模板层 | 恢复共享模板骨架 | 以 `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json` 为唯一模板真源 | `model` 骨架与共享模板一致 |
| 文档再次引用 `5-画面/subtypes/...` 或 `references/*.md` | 真源治理层 | 统一替换回当前真实路径，并保持单一 `SKILL.md` 真源 | 在 `SKILL.md` 固化 `Shared Canonical Sources`、`Context Preload` 与 `Root-Cause Execution Contract`，禁止重建第二套规范载体 | 技能目录内不再残留旧路径或已删除 references 引用 |
| 合同只剩字段表与 workflow 摘要，节点没有做到“想清楚即执行” | 编排表达层 | 把业务分析、思行节点网络、节点执行 playbook、汇流门和一次性输出门补回 `SKILL.md` | 在主合同显式声明 `skeleton_detail_split: false`，并要求每个节点写清输入、动作、证据、路由与完成信号 | 执行者无需查额外细则即可完成整条漫画蒸馏链 |
| 仍把补证入口写成 `3-Detail/evidence/` | 补证路径层 | 改回 `3-Detail/水月/第N集.field-patch.json` 与 `3-Detail/镜花/第N集.field-patch.json` | 在 `SKILL.md` 固化真实 sidecar 路径与只读补证边界 | 不再引用不存在的补证目录 |
| 漫画页蒸馏没查 `document_phase` 或漏掉 `出场角色及穿搭` | 阶段就绪层 | 在 `N2/N4` 之前先查 phase、组级穿搭槽与镜级 canonical 字段 | 在 `SKILL.md` 固化 readiness gate 与内容抽取最低覆盖面 | 漫画页 prompt 不再建立在未就绪或空壳 detail 上 |
| 父层已切到 branch-owned，但漫画叶子仍把 legacy 四字段当基础镜级事实 | schema handoff 层 | 把 readiness gate 与内容抽取改成 branch-owned 八字段优先，legacy 四字段只作 panel 补证 | 在 `SKILL.md` 固化 `branch-owned first, legacy fallback` | 漫画页不再以 compatibility projection 充当主真相 |

## Repair Playbook

1. 先核对当前父路径是否指向 `.agents/skills/aigc/5-Image/1-提示词蒸馏/`，不要再引用不存在的 `5-画面/subtypes/...`。
2. 再查 `metadata.document_phase` 是否已到 `detail_in_progress | ready`，以及目标分镜组能否从 `3-Detail/第N集.json` 的 `分镜组列表[]` 唯一定位。
3. 再查 `prompt` 是否严格等于“固定前缀 + comic_page_group”。
4. 再查 `model` 是否仍保持共享模板骨架，且 `reference_images / image_markers` 未被删掉。
5. 最后查输出模式是 `json_only` 还是 `full_trace`，确认 `第N集.json` 与 `_manifest.json` 的落盘是否一致。
6. 若技能看起来“信息都在，但执行还是发虚”，回查 `SKILL.md` 是否具备 `Business Requirement Analysis / Thinking-Action Node Network / Node Execution Playbook / Convergence Contract / One-Shot Output Contract` 五段主脊梁。

## Reusable Heuristics

- 对这种确定性的叶子蒸馏技能，最稳的升格方式不是补 `team.md`，而是把规范内容收回单一 `SKILL.md` 真源。
- 只要 `references/` 承担了字段表、workflow、类型策略或输出合同，它就不再是“参考材料”，而是在偷渡第二套规范层。
- 阶段名称可以保留人类可读的图像语义，但文件路径必须以当前真实目录 `5-Image/1-提示词蒸馏/漫画/` 为准。
- 当前仓对本技能的阶段根合同已落到 `5-Image/SKILL.md`，因此加载顺序应先经过阶段父级，再进入 `1-提示词蒸馏` 父级。
- 漫画子技能最常见的漂移不是画风，而是把“漫画图像请求 JSON 蒸馏”误做成“直接页图落盘”。
- 对这种已经是叶子且又有多道判断门的蒸馏技能，最稳的知行合一改造不是继续拆 `references/`，而是把节点细则直接写进主 `SKILL.md`。
- 如果用户明确要求 `复杂链路的骨架 / 细则分层 = false`，就要把“可扫描性”交给 Mermaid 和节点表，而不是把执行细节外包给另一个文档。
- 漫画页 prompt 若没显式承接 `出场角色及穿搭` 与 branch-owned 八字段，通常只剩版式约束和旧投影残句，缺少稳定的角色服装、空间关系与镜头视觉抓手。
