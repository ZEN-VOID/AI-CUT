# aigc 3-明细 / 1-分镜表现 / 分镜构图 / Type Strategies

本文件承载 `aigc 3-明细 / 1-分镜表现 / 分镜构图` 的路由策略、VSM 与局部回退规则。

## Upstream Ownership Boundary

- 候选整数帧数枚举、`single_panel_long_take` 特例判断、`panel_count -> template_id` 映射与模板矩阵真源，统一继承 `../分镜密度/references/type-strategies.md` 与 `../分镜密度/references/output-template.md`。
- 本层不重复定义“几镜”；本层负责回答“这几镜怎么真正成立、怎么切时间、哪一镜成为审美峰值、如何回写成 canonical shot 与父级单行”。
- 当模板门槛不成立时，回退顺序固定为：
  1. 重排功能位、景别、角度、遮挡与层次；
  2. 在上游 `refined_range` 内申请 `+1/-1` 微调；
  3. 若两轮后仍失败，升级回上游最近的更高合法值，并显式记录原因。

## VSM

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SBC-PANEL | 输入 | 上游 `panel_count/template_id` 是否可消费 | `ready/missing/unjustified` | 读取密度结果 | P0 |
| V-SBC-RHYTHM | 输入 | 上游组节奏标签是否可继承 | `ultra_slow/slow/mid/fast/ultra_fast/unknown` | 读取密度结果 | P0 |
| V-SBC-DURATION-SOURCE | 结构 | 当前组总时长来源是否可追溯 | `resolved/missing/drift` | 读取 `分镜组时长映射 -> 默认组时长 -> 切分时长策略` | P0 |
| V-SBC-SCENE-TYPE | 叙事 | 当前组主场景类型 | `dialogue/action/crowd/inner/emotion/unknown` | 关键词与上下文判定 | P0 |
| V-SBC-TIME | 输出 | 帧级时间是否连续且和组总时长一致 | `pass/fail` | 时间字段扫描 | P0 |
| V-SBC-FRAME-FIELDS | 输出 | canonical shot 字段是否齐全 | `complete/missing/invalid` | 字段检查 | P0 |
| V-SBC-TEMPLATE | 质量 | 实际镜头设计是否满足模板门槛 | `pass/fail/pending` | 对照上游 `template_id` 检查 | P0 |
| V-SBC-PEAK | 质量 | 是否存在真正落地的构图审美峰值镜 | `pass/fail` | 组内构图差异检查 | P0 |
| V-SBC-ECHO | 连续性 | 是否需要并满足组间回溯 | `exempt/pass/fail/verbatim` | 同场景相邻组首尾对照 | P1 |
| V-SBC-SEQUENCE | 集级 | 本集是否出现序列塌缩 | `pass/fail/pending` | 统计“景别+角度”序列重复率 | P1 |
| V-SBC-SCOPE | 边界 | 是否越界到其他阶段 | `clean/overreach` | 词项扫描 | P1 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SBC-01 | `V-SBC-PANEL in {missing,unjustified}` | 1.0 | 无 | 无 |
| C-SBC-02 | `V-SBC-DURATION-SOURCE in {missing,drift}` | 1.0 | 无 | 可并发 C-SBC-03 |
| C-SBC-03 | `V-SBC-SCENE-TYPE=unknown` | 0.9 | 无 | 可并发 C-SBC-02 |
| C-SBC-04 | `V-SBC-TIME=fail` | 1.0 | 无 | 可并发 C-SBC-05 |
| C-SBC-05 | `V-SBC-FRAME-FIELDS in {missing,invalid}` | 1.0 | 无 | 可并发 C-SBC-06 |
| C-SBC-06 | `V-SBC-TEMPLATE=fail` | 1.0 | 无 | 可并发 C-SBC-07 |
| C-SBC-07 | `V-SBC-PEAK=fail` | 1.0 | 无 | 可并发 C-SBC-06 |
| C-SBC-08 | `V-SBC-ECHO in {fail,verbatim}` | 1.0 | 无 | 无 |
| C-SBC-09 | `V-SBC-SEQUENCE=fail` | 1.0 | 无 | 无 |
| C-SBC-10 | `V-SBC-SCOPE=overreach` | 1.0 | 无 | 无 |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SBC-01 | S-SBC-UPSTREAM-PANEL | 回退到 `分镜密度` 补齐或校正 `panel_count/template_id` | 上游镜数裁决可解释 | S-SBC-PAUSE | 仍无上游镜数真源 |
| C-SBC-02 | S-SBC-DURATION-CHAIN | 重新按 `分镜组时长映射 -> 默认组时长 -> 切分时长策略` 解析组总时长 | 组总时长可追溯 | S-SBC-PAUSE | frontmatter 仍缺真源 |
| C-SBC-03 | S-SBC-SCENE-TYPE | 回退为 `emotion`，并记录 `V-SCENE-TYPE=unknown` | 类型判定可解释 | S-SBC-DURATION-CHAIN | unknown 连续过高 |
| C-SBC-04 | S-SBC-TIME-REALLOCATE | 依据 `scene_type + rhythm` 重分配单帧时长 | 时间连续且总和正确 | S-SBC-DURATION-CHAIN | 仍无法闭合总时长 |
| C-SBC-05 | S-SBC-FIELDS | 补齐 canonical shot 字段，并生成父级八字段投影 | 字段全集完整 | S-SBC-PAUSE | 两轮后仍缺字段 |
| C-SBC-06 | S-SBC-TEMPLATE-RELAYOUT | 先重排景别/角度/功能位，再必要时在 `refined_range` 内微调镜数 | 模板门槛成立 | S-SBC-UPSTREAM-PANEL | 连续两轮仍无法成立 |
| C-SBC-07 | S-SBC-PEAK-PUSH | 指定一帧为全组最大胆构图，并围绕它重排前景、角度、焦点或负空间 | 至少一帧形成审美峰值 | S-SBC-TEMPLATE-RELAYOUT | 全组仍平庸 |
| C-SBC-08 | S-SBC-ECHO-COMPRESS | 将上一组尾帧核心动作/状态压缩复述到本组首帧 `角色及站位` | 回溯成立且不逐字复制 | S-SBC-PAUSE | 前序尾帧本身缺关键动作 |
| C-SBC-09 | S-SBC-SEQUENCE-DIVERSIFY | 重新分散本集高频“景别+角度”序列 | 最高重复占比 `<=60%` | S-SBC-PAUSE | 同集整体模板塌缩 |
| C-SBC-10 | S-SBC-SCOPE | 移除运镜、光影、色彩、转场正文等越界内容 | 只保留本层静态构图字段 | S-SBC-PAUSE | 越界项无法剥离 |

## 叙事意图与场景类型识别（Mandatory）

| 场景类型 | 主判定信号 | 构图偏压 |
| --- | --- | --- |
| `dialogue` | 命中 `说/问/答/喊/道` | 优先处理权力关系、轴线与主反位背景极点 |
| `action` | 命中 `冲/跑/追/撞/闯/猛地/突然/转身` | 优先处理力量方向、前后帧动作咬合与低角冲击 |
| `crowd` | 命中 `人群/街坊/围观/众人/喝彩` | 优先处理群体信息位、空间再建立与层次穿透 |
| `inner` | 命中 `系统/内心/心声/V.O` | 优先处理主观压迫、负空间与焦点异化 |
| `emotion` | 其余以情绪推进为主的场景 | 优先处理留白、迟疑、爆发与关系拆解 |

裁决规则：

1. 多类型并存时，取“信息主导动作”为主类型；次类型只进入构图与站位补偿。
2. 无法稳定判定时默认 `emotion`，并记录 `V-SCENE-TYPE=unknown`。

## 构图决策启发（Strategy-level Guidance）

1. 叙事优先：画面里每个显眼元素都必须能服务人物、关系或情绪；无关元素要移出画面、压暗或虚化。
2. 视觉焦点优先：每帧至少要有一个明确焦点，可通过亮度、清晰度、对比、位置、运动或面积建立，不得把观众丢进平均信息海。
3. 角度与平衡是有语义的：仰角默认偏权威，俯角默认偏脆弱；平衡偏秩序，不平衡偏不安。若要翻转默认语义，必须让上下文支持这种翻转。
4. Z 轴必须服务叙事：前景遮挡、主体重叠、远近尺度差只能在能增强偷窥感、压迫感、纵深穿透或焦点引导时使用，不得无意义堆杂物。
5. 对话组优先守连续性：涉及稳定互动时，优先守 `180°` 轴线与背景极点一致性，再追求变化。
6. 焦段与景深是叙事选择：广角负责纳入环境与拉开纵深，长焦负责压缩空间与锁定情绪；不要把所有特写都默认配广角。
7. 开放/封闭景框都要可读：若把关键要素留在画外，必须明确指向哪一侧画外以及观众为何要紧张；否则只是含糊。

## 帧级时间分配策略（Mandatory）

### 时间字段格式

- 格式固定为 `X-Y秒`。
- 第一个分镜必须从 `0` 开始。
- 最后一个分镜必须覆盖到组总时长结束。
- 相邻分镜必须连续无间隙。

### 单帧时长类型表

| 场景类型 | 单帧时长范围 | 分配策略 |
| --- | --- | --- |
| `dialogue` | `2-5秒` | 说话帧偏长，反应帧偏短 |
| `action` | `1-3秒` | 以高密度短帧为主，关键动作帧可拉长 |
| `crowd` | `1-4秒` | 建立帧偏长，局部快切偏短 |
| `inner` | `3-6秒` | 意象帧偏长，允许超 `5秒` 营造沉浸 |
| `emotion` | `2-5秒` | 情绪蓄力帧渐长，爆发帧骤短 |

### 节奏联动

- `超慢 / 慢节奏`：单帧均值偏向区间上限。
- `中节奏`：均匀分配，允许 `±1秒` 波动。
- `快 / 超快节奏`：单帧均值偏向区间下限，允许 `1秒` 极短帧。

### 硬约束

1. 单帧最短 `1秒`，普通组单帧最长 `8秒`。
2. 若 `panel_count=1` 且命中上游 `single_panel_long_take` 特例，则允许覆盖整组总时长，但必须沿用上游证据链说明理由。
3. 所有帧时长之和必须等于组总时长。

## 同场景组间画面回溯契约（Mandatory）

1. 只适用于同一 Scene Heading 下的相邻分镜组。
2. 下一组首帧 `角色及站位` 必须压缩复述上一组尾帧的“主体 + 核心动作/状态”。
3. 可省略次要角色和背景细节，但不得丢掉核心动作。
4. 禁止逐字复制上一组尾帧整段 `角色及站位`。
5. 跨场景相邻组豁免，由 `6-转场特效` 处理场景间过渡。
