# Changelog

## 2026-06-04

- 按最新 `skill-2.0` runtime-spine 规范重构 `SKILL.md`：补齐 `Runtime Spine Contract`、`Core Task Contract`、`Business Requirement Analysis Contract`、`Type Routing Matrix`、`Thinking-Action Node Map`、`Module Loading Matrix`、`Module Trigger Matrix`、`Convergence Contract`、`Review Gate Binding`、`Quantifiable Execution Criteria Contract`、`Attention Concentration Protocol`、`Checkpoint Contract`、`Evaluation Prompt Contract` 与 `Learning / Context Writeback`。
- 收束旧 `steps/video-review-workflow.md` 第二节点真源：N0-N7、Mermaid 拓扑、gate、fail code 和返工目标统一回到 `SKILL.md`。
- 同步各 `references/` 中的旧步骤引用，改为回指 `SKILL.md#Thinking-Action Node Map` 的对应节点。
- 新增 `test-prompts.json`，覆盖本地单片审查、LibTV 取证审片、示例校准变体选择和授权分组修复四类回归 prompt。
- 更新 `README.md` 与 `CONTEXT.md`，记录新版结构、评估资产和步骤真源漂移修复经验。

## 2026-06-01

- 增加 `references/review-method-palette-contract.md`，将审片从固定流程升级为“默认自动化载体 + 动态方法库 + 操作设计”。
- 新增方法族：source fidelity、连续性、表演、摄影、剪辑节奏、声音、关键道具、伦理安全、AIGC 伪影、prompt 执行、候选片比较和修复设计。
- 扩展 landing / operation 合同：支持接受、条件接受、变体比较、同 prompt 重跑、换 seed/model 重跑、LibTV prompt 修复并重提、拆并组、资产引用修复、图片顺序修复、声音策略修复、补证和 reject 归档。
- 同步 `GATE-REVIEW-16/17`、`FAIL-REVIEW-METHOD-SELECTION`、`FAIL-REVIEW-OPERATION-DESIGN`、报告模板和类型映射。
- 标准化 LibTV 审片入口：支持 `LibTV 链接 + 视频名`、`projectUuid + 视频名`、`画布名 + 视频名` 与 `.libtv/project.json` 默认项目。
- 新增 `references/libtv-intake-contract.md`，要求通过 `.agents/skills/cli/libTV` 查询项目、查询视频节点、保存 node query、下载真实视频，再进入抽帧审片。
- 将审片步骤拓扑升级为 `N0-LIBTV-INTAKE -> N1 -> N2 -> N3...`，避免只凭 prompt、远端 URL 或节点 JSON 做文本判断。
- 同步 `types/type-map.md`、`review/review-gate.md`、`templates/review-report.template.md`、`video-evidence-contract.md` 与 `video-naming-contract.md`，补齐 LibTV evidence、prompt hygiene 和 rerun closure 门禁。
- 在 `CONTEXT.md` 沉淀本轮经验：远端 node query 是生成路线证据，`libtv download` 后的本地视频关键帧/联系表才是审片 verdict 的事实基础。

## 2026-05-04

- 初始化 `14-审片` Skill 2.0 包。
- 固定视频命名规范：`<分镜组ID>.mp4`，同组变体为 `<分镜组ID>-a.mp4` / `-b.mp4`。
- 建立审片到 `10-分组` 修复、rerun 建议和源层升级的落盘合同。
- 按 `skill-知行合一` 要求加入业务需求分析、思行节点网络、Mermaid 拓扑与思考过程输出合同。
- 明确审片三层能力：视频本体问题、prompt 匹配与错配归因、创作质量/反平庸/美学鉴定。
- 增加用户好/坏示例比较学习合同，支持将稳定、可复用的鉴赏经验沉淀到本技能 `CONTEXT.md`。
- 参照 `4-表演` 与 `4-摄影`，新增 `14-审片` 顾问与复核流程定义：以项目 `team.yaml` 监制组作为审片顾问团，节点级请教后汇流为 `review_advisor_packet`，不替代最终 verdict 或 canonical 写回。
