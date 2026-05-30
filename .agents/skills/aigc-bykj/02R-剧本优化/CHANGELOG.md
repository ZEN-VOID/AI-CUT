# CHANGELOG

## 2026-05-29

- 全量补入用户个人自然语言驱动机制。
- 新增 `Natural Language Driven Optimization Contract`，覆盖意图归一、模糊需求澄清门、临时个人偏好画像、修改强度档位、自然语言冲突映射、版本对照与可回退机制。
- 更新思行网络 Mermaid、状态图、字段关系图和节点表，新增 `N2A-INTENT-NORMALIZE` 与 `N2B-CLARIFY`。
- 更新输出合同、manifest schema、Review Gate、Pass Table、Root-Cause 和完成定义。
- 更新 `CONTEXT.md`、`README.md`，沉淀自然语言调优的失效模式和执行启发。

## 2026-05-28

- 初始化 `02R-剧本优化` 阶段技能包。
- 新增 `SKILL.md`，定义承接 `02-剧本处理` 输出的二次人工介入调优合同。
- 新增混合型思行网络：源稿锁定、范围判型、冲突扫描、整体/局部调优、汇流复核、写回。
- 新增局部调优冲突判别机制：局部目标与前后剧情硬冲突时，先输出冲突判别单，不擅自写终稿。
- 新增五段式 `SKILL.md Review Gate Configuration`、`Pass Table`、Root-Cause 合同和完成定义。
- 新增 `CONTEXT.md`、`README.md` 与 `agents/openai.yaml`。
