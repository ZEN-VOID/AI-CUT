# CHANGELOG

## 2026-06-04

### Skill 2.0 runtime-spine 升级

- 按最新 `$skill-2.0` 规范升级 `SKILL.md`：补齐 Runtime Spine Contract、Type Routing Matrix、Thinking-Action Node Map、Module Loading Matrix、Module Trigger Matrix、Convergence Contract、Review Gate Binding、Quantifiable Execution Criteria、Attention Concentration Protocol、Checkpoint Contract、Evaluation Prompt Contract 与 Learning / Context Writeback。
- 新增 `test-prompts.json`，覆盖 3-美学六路解析、分镜脚本 19 列保留和旧聚合风格包修复三类回归场景。
- 移除 `steps/shot-by-shot-workflow.md`，将节点真源收回 `SKILL.md`；同步更新 README、类型说明、模板、review gate、validator 和脚本说明。

### 风格解析对齐 3-美学

- 新增 `references/aesthetic-style-analysis-contract.md`，把风格解析调整为对齐 `.agents/skills/aigc/3-美学` 六个子技能：`画面基调解析.md`、`角色风格解析.md`、`场景风格解析.md`、`道具风格解析.md`、`摄影风格解析.md`、`分镜风格解析.md`。
- 将旧 `全局风格解析.md` / `设计风格解析.md` 聚合口径降为 legacy 修复与兼容审查对象，不再作为新主输出合同。
- `分镜脚本.md` 仍保持 `input/苍穹裂缝·战神降维.numbers` 的 19 列字段和内容编排方式不变。

## 2026-05-24

### 输出路径统一化
- 所有解析文档与分镜脚本统一落点为 `shot-by-shot/<reference_slug>/`；旧路径 `CONTEXT/shot-by-shot/<reference_slug>/` 停止使用。
- 同步更新 SKILL.md、README.md、templates/output-template.md、steps/shot-by-shot-workflow.md、scripts/validate_shot_by_shot_package.py 中所有路径引用。

### 解析维度扩充

**全局风格解析.md** 新增 5 个字段：
- `genre_promise` — 类型叙事承诺（类型核心契约、高光时刻类型、承诺兑现节奏）
- `visual_motif_seed` — 视觉母题系统（重复符号、色调节点、母题语法）
- `temporal_texture` — 年代质感语法（质感来源、信号密度、时间感构建）
- `emotion_curve_profile` — 情绪曲线轮廓（曲线结构、幕情绪档位、高潮情绪类型、情绪余震设计）
- Required Markdown Shape 从 9 区块扩充为 13 区块

**编剧风格解析.md** 新增 4 个字段：
- `subtext_layer_seed` — 潜台词层（表面意图/隐藏信息层/潜台词弧线）
- `emotion_pulse_seed` — 情绪脉冲（积累/爆发/余震/共情连接）
- `subplot_weave_seed` — 次要情节编织（伏笔埋收、副线对主线的压力输送）
- `sound_narrative_seed` — 声音叙事接口（音乐主题、环境音、静默、对位）
- Required Markdown Shape 从 6 区块扩充为 9 区块

**摄影风格解析.md** 新增 6 个字段：
- `point_of_view_profile` — 视点轮廓（归属/切换逻辑/主观vs客观边界）
- `depth_of_field_semantic` — 焦深语义（叙事模式/前景/后景/焦点切换）
- `light_source_semantic` — 光源叙事语义（方向权力映射/冷暖光情绪功能）
- `cut_grammar_seed` — 切点语法（类型/情绪同步/时机/反应镜头模式）
- `camera_movement_taxonomy` — 运动类型系统（类型清单/语义/手持/速度节奏）
- `long_take_structure_seed` — 长镜头结构（阈值/相位组织/空间揭示/情绪功能）
- `format_grammar_seed` — 格式语法（画幅比/比例/构图逻辑）
- Required Markdown Shape 从 6 区块扩充为 10 区块

**设计风格解析.md** 新增 4 个区块：
- `## 角色色调与材质语法` — 色彩身份系统/材质词汇/磨损纹理叙事/细节层级
- `## 空间叙事语法` — 空间作为角色隐喻/环境权力映射/残留物件叙事/空镜语法
- `## 道具功能层级` — 叙事核心道具/氛围道具/转场触发物/象征性道具系统
- `## 世界观视觉语法` — 符号系统/色彩规则/材质体系/文化视觉标记/世界观一致性

同步更新：
- `SKILL.md` Field Master — `FIELD-SBS-05` 至 `FIELD-SBS-08` content requirement 更新
- `SKILL.md` Pass Table — `PASS-SBS-04` 至 `PASS-SBS-07` pass standard 更新
- `review/review-contract.md` — GATE-SBS-05 至 GATE-SBS-08 question 更新
- `templates/output-template.md` — 全部 4 个 skeleton 更新，新字段逐一代入表格
- `references/adaptation-output-contract.md` — 4 个 Packet 的允许字段表扩充 + Fusion Output Shape 更新

## 2026-05-11

- 将执行后 canonical 解析输出调整为 `全局风格解析.md`、`编剧风格解析.md`、`摄影风格解析.md`、`设计风格解析.md` 与 `分镜脚本.md`。
- 新增五份解析细则：全局风格参照 `global-style-director` 字段逻辑，编剧/摄影/设计分别绑定 2/3/5 阶段边界，分镜脚本固定参照 `input/苍穹裂缝·战神降维.numbers` 的 19 列字段和内容编排方式。
- 同步更新输出模板、review gate、workflow、validator 与 README；旧 `画面风格解析.md`、`编导解析.md`、`摄影解析.md`、`设计解析.md` 仅保留为 legacy mirror 语义。
- 源层同步阶段解析落点：阶段可消费文档归入 `projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/`。

## 2026-05-04

- 初始化 `.agents/skills/aigc/shot-by-shot` Skill 2.0 包。
- 明确其为 AIGC 根下临摹型卫星技能，服务 `0-初始化`、`2-编导`、`3-运动`、`4-摄影` 与 `11-主体`，不替代主链阶段 canonical 写回。
- 建立逐镜证据、解析维度、临摹原则、禁止照搬清单、`画面风格解析.md`、`编导解析.md`、`摄影解析.md` 与 `设计解析.md` 的项目 `CONTEXT/` 输出合同。
- 按 `$skill-知行合一` 要求建立思行网络、Mermaid 拓扑、Field Master、Thought Pass Map、Pass Table 与 `思考过程` 输出槽位。
- 源层同步阶段解析落点：阶段可消费文档归入 `projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/`。
