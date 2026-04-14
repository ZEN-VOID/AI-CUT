# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/场景/1-清单` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc -> 4-Design/1-主体清单` 共享消费合同之后加载本文件。
- 当前技能采用知行合一单合同；经验层只存放复用知识，不再承载并行规则真源。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把 `1-清单` 误写成研究链或设计链 | 阶段边界层 | 回退到 scene catalog 最小输出壳 | 在 `SKILL.md` 固化“只输出 scenes[] / group_scene_map[] / statistics” | 主产物不含研究与设计字段 |
| `scene_name` 与 `scene_variant` 拆分不稳 | 抽取规则层 | 保守只锁 `scene_name`，其余回收到 `scene_variant` 或整句 | 在 `SKILL.md + 脚本` 固定 earliest-marker 与 keep-raw 回退 | 同一主场景不再裂成多个伪场景 |
| 把整句 `角色背景面` 直接升格成 `scene_name`，导致一镜一场景 | 场景主键层 | 先归并到主场景家族，再把原句保留到 `scene_variant` | 固定“主场景实体优先，完整背景句做 variant”的抽取顺序 | `scenes[]` 数量回到可被设计阶段复用的主场景规模 |
| 上游 episode JSON 缺少 shared schema 壳 | 输入合同层 | 停止并报告缺失字段 | 在 `SKILL.md` 中把 `N1` 作为硬门槛 | 不在缺壳情况下伪造清单 |
| 输出落回旧 `output/影片/...` 路径 | runtime 落点层 | 改回 `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/` | 在 `SKILL.md` 和脚本默认落点里固定当前仓口径 | 输出目录符合当前技能合同 |
| sibling leaf 各自输出命名漂移，场景链独占 `第N集.json` | canonical output 治理层 | 收回到共享 `list-output-contract`，把主清单名改成 `场景清单.json`，`_manifest.json` 统一为审计侧车 | 在父层共享合同中固定“`<领域>清单.json + _manifest.json + 按需派生 sidecar`” | 场景/角色/道具/服装的清单阶段文件角色一致 |
| `3-Detail` canonical 与 legacy `编导` 路径被各 leaf 各自解释 | 真源治理层 | 固定 `3-Detail/第N集.json` 为第一输入根，`编导/第N集.json` 仅作 fallback | 在 `1-主体清单/_shared` 共享消费合同里统一路径与字段映射 | 场景链与角色/道具链的 detail 输入规则一致 |
| 主文档与 `references/` 规则漂移 | 真源治理层 | 把有效规则全部收回 `SKILL.md` | 删除或退役明细 `references/`，避免第二真源 | 当前目录只剩单一规则主合同 |

## Repair Playbook

1. 先查上游 episode JSON 是否存在 `final_output.main_content.分镜组列表[]`。
2. 再查每个 `分镜明细[]` 是否含 `分镜ID` 与 `角色背景面`；legacy `场景及方位` 仅作 fallback。
3. 再查 `scene_name / scene_variant` 是否按“主场景优先”保守收口。
4. 最后查 `场景清单.json` 是否同时具备 `statistics / scenes[] / group_scene_map[] / acceptance_notes`。

## Reusable Heuristics

- `1-清单` 的高质量标准不是“写得更丰富”，而是“把下游要复用的场景主键锁稳”。
- 当 `角色背景面` 同时含空间实体和朝向短语时，优先保住空间实体；legacy `场景及方位` 命中时也按同一规则处理，方位信息宁可全部留在 `scene_variant`。
- 如果 `角色背景面` 本身是一整句导演背景描述，就先找可复用的主场景家族名，再把细节句留在 `scene_variant`；不要让每一镜都长出一条新的场景主键。
- 对本链路来说，`unknown` 是合格回退，不是失败遮羞布；真正的失败是静默跳过镜头。
- 若规则已经收回单一 `SKILL.md`，经验层只补 heuristics，不再额外复制流程、表格和输出契约。
- 多个 sibling leaf 共用同一 upstream episode JSON 时，最该先统一的是 canonical 输入路径和字段映射，而不是每个 leaf 自己发明一套 fallback 解释。
- sibling leaf 要统一的是“清单阶段的文件分层”，不是强迫所有领域都产出同样数量的研究/bridge 文件；场景链应对齐到 `场景清单.json + _manifest.json`，而不是继续持有 episode-only 命名特权。
