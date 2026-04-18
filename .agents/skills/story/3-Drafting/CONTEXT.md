# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Reusable Heuristics

- 写作层先固定上下文、审查、润色、数据回写的顺序边界，避免阶段职责互相吞并。
- 初始化若已在 `TEAM.toml["监制"]` 指派 AGENTS，`3-Drafting` 就必须把他们当作制作治理层接入 Step 0/Step 1，而不是继续把 `TEAM.toml` 当摆设。
- `3-Drafting` 已经自带 Step 4 润色位时，不要再额外挂一个薄封装的 polish stage；把边界直接写回写作主合同更稳。
- `3-Drafting` 的 references 最稳的层级不是“根技能逐文件直连”，而是“根技能先路由 step module，再按需进入 craft module，leaf docs 永远留在二级加载层”。
- `3-Drafting/references` 的根层应只保留路由与模块目录；step appendix 必须收回各自模块，craft leaf docs 必须收回 `writing-craft-catalog/leaf-notes/`，否则顶层语义会重新混成一锅。
- 如果 `module-spec.md` 里只有“三轴/三重标题 + 结论句”，没有 `驱动/判废/对比` 字段、落盘映射和验证矩阵，那还不算真正执行了 `think-think`，最多只是借用了术语外壳。
- 规划真源切到 `Planning/8-全息地图.json` 后，`extract_chapter_context.py`、章节标题解析和续写恢复都应统一做 holomap-first；旧 `大纲/` 只能作为兼容回退，不能再冒充默认入口。
- `story.py preflight` 不应只校验脚本是否存在，还应显式报告当前项目的规划源状态：`canonical`、`legacy_fallback` 或 `missing`，这样能在真正写作前就看见入口是否漂回旧大纲。
- 若共享硬约束已把“`大纲即法律`”升级为“`规划真源即法律`”，润色指南、审查清单和写作入口说明也必须同步改名；否则步骤间会出现判断标准漂移。
- Step 顺序、白名单和标题文件命名一旦被写成“硬规则”，就必须在 `workflow_manager.py` / 验证脚本里同步落地；只写在 `SKILL.md` 的 gate 最终一定会漂。
- `3-Drafting` 最稳的加载方式不是“重读所有上游材料”，而是分成：硬约束层、章节编排层、运行态层、对象切片层、写作引导层五层执行包。
- 上游 `1-Cards` 在写作阶段默认应按本章 `chapter_board` 做定向切片；只有追溯或排障时才回读整库或 planning 证据层。
- 若 references 里只有“对白/情绪/战斗/场景”的通用技法，而缺少“声口差异化”“氛围美学”“段内节奏”三个专项文档，写作层会在高级表现力上出现系统性短板。
- Anti-AI 终检若把词表、比例和统一句法当成硬指标，最终修掉的往往不是 AI 味，而是角色声口、题材修辞和作者自觉保留的节奏差。
- craft 目录里若同时存在“基础对白体检”和“高阶对白主入口”，必须写死症状到文档的映射；否则执行者会误把基础模板当成对白真源。
- 若全息地图的章节节点使用 `bundled_elements` 容器，`chapter_outline_loader.py` 必须把它视为 canonical schema 读取入口；否则写作上下文会只剩“第X章”标题，失去事件/冲突/线索等执行信息。
- 当用户明确放弃某个特殊入口方案时，不能只删正文样稿；必须同时回滚 `SKILL.md` 合同、references、脚本入口、测试和项目产物，否则废案会继续以默认能力残留在工作流里。
- 若 workflow 已经把某一阶段的 shadow 工件链写出来，而该阶段 `SKILL.md` 还没有承认它们，优先补阶段合同与 Completion Gate，而不是再扩脚本分支。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 初始化已生成 `TEAM.toml`，但 `3-Drafting` 执行时不读取 `监制` 布阵 | stage team governance | 在 `3-Drafting/SKILL.md` 的 Step 0 与工具策略中接入 `TEAM.toml["监制"]`，并要求有指派 AGENTS 时创建后台监制 subagents | 将“监制团队只负责制作决议、不替代 Step 3 审查”写成根技能硬规则 | 执行 `3-Drafting` 时能明确区分监制决议与 `4-Validation` 审查结论 |
| tracked workflow 已能旁路写三省工件，但 `3-Drafting` 合同仍只承认旧状态链 | workflow governance contract | 在写作阶段合同中显式承认 `.webnovel/tasks/<run_id>/` shadow 工件链 | 将写作阶段的 Step 3-5 结果与 `artifact_manifest / validation_report / learning_record` 对齐，避免闭环证据再次隐形 | 写作 run 完成后，脚本输出、技能合同与 task artifact chain 能互相回指 |
| Step 4 的 Anti-AI 规则过硬，导致文本越修越像统一声线 | polish gate contract | 把词表和比例阈值降级为症状提示，保留 `anti_ai_force_check` 但改为关键部位与症状优先 | 在 polish appendix 中写死“角色声口/题材修辞优先于表面计数” | 终检时不会再因机械命中词表就直接改坏文本 |
| `Step 1.5` 旧命名继续污染 Step 1 真源 | drafting shared references | 同步清理主 skill、appendix 与共享 references 的旧命名 | 新增文档改动时联查 shared refs、appendix 与 system-data-flow | 仓内非 legacy 文档不再把 `Step 1.5` 当现行入口 |

