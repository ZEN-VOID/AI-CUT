# /master-check

用于围绕一个明确评审对象，调用 `.agents/skills/team/` 下的一个或多个“大师视角”技能包组成评审团，执行定向评审，并在适合时直接做文件级优化。

## 语法

```text
/master-check
<指定大师视角技能包>
<评审对象>

[可选附加行]
mode: auto|parallel-council|serial-refine|independent-only
output: auto|review-only|synthesize-only|synthesize-and-patch
```

### 合法的“大师技能包”写法

- 单个 skill 名称，例如：`黑泽明`
- 单个 skill 路径，例如：`.agents/skills/team/导演组/黑泽明/SKILL.md`
- 多个 skill，使用逗号分隔，例如：`黑泽明, 杜可风, 叶锦添`
- 一个 `team.yaml` 路径，例如：`projects/aigc/滴滴滴/team.yaml`

### 评审对象

- 默认应是一个文件路径。
- 若给的是图片、视频、二进制或其他不可直接 patch 的对象，允许只生成优化建议，不强行编辑源文件。

## 何时使用

- 用户已经知道要请哪些“大师视角”来审。
- 用户要把一个具体文本、脚本、JSON、Markdown、分镜稿、设计稿做多视角会诊。
- 用户希望评审后直接对目标文件做一轮收束优化，而不是只收集点评。

## 输入约定

1. 第一行非空内容视为 reviewer selector。
2. 第二行非空内容视为 review target。
3. 后续可选行只接受：
   - `mode: ...`
   - `output: ...`
4. 若 reviewer selector 是 `team.yaml`，先按 team 配置解析 reviewer，再决定模式。

## 根因优先

- 若评审失败、skill 无法匹配、输出空泛或汇总失真，固定按以下链路上溯：
  - `Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`
- `Rule Source` 优先检查：
  - `.agents/skills/team/SKILL.md`
  - 命中的子 skill `SKILL.md` / `CONTEXT.md`
  - 传入的 `team.yaml`
- `Meta Rule Source` 优先检查：
  - 根 `AGENTS.md`
  - team skill 的根治理合同
- 先修路由、skill 选择、汇流和上下文加载问题，再决定是否只补表层点评。

## Reviewer 解析顺序

### A. 显式 skill 路径

- 若 selector 是存在的 `SKILL.md` 路径，直接使用。
- 若 selector 是某个人物技能目录，自动补到该目录下的 `SKILL.md`。

### B. skill 名称或别名

- 在 `.agents/skills/team/**/SKILL.md` 中匹配：
  - frontmatter `name`
  - 目录名
  - 中文人物名
  - 常见英文别名
- 若同名命中多个 skill，停止并要求用户只保留一个明确候选。

### C. `team.yaml`

若 selector 是 `team.yaml`，按以下优先级抽取 reviewer：

1. `team_setup.shared_agents`
2. `roles.*.members`
3. `roles.*.source_skill_refs`

处理规则：

- 优先保留 `.agents/skills/team/` 下的 skill。
- 若某个条目指向目录，则补到其 `SKILL.md`。
- 若显式条目不足以形成有效评审团，再根据启用的 role 和评审对象类型，补 1-2 个最必要的 `.agents/skills/team/` skill。
- 补选时必须显式说明这是推断，不是 `team.yaml` 中的显式声明。

## 评审对象分析

读取目标文件后先锁定：

- `target_type`: 剧本、分镜、设定、设计、镜头方案、代码/规则文档、报告、其他
- `editability`: 是否可直接 patch
- `stability`: 是成熟稿、半成稿还是草稿
- `goal`: 只评审、评审后汇总、评审后直接优化

默认不做无边界扩展：

- 不因目标文件在某个项目目录中，就自动扫描整个项目。
- 除非 reviewer 解析依赖 `team.yaml` 或目标缺少必要上下文，否则只补读与该目标强相关的上游文件。

## Subagent Dispatch Gate

- 本命令的默认执行语义不是“本地主 agent 模拟多位顾问”，而是“一个 reviewer skill 对应一个 subagent，由主 agent 汇流”。
- 只要命中 reviewer skill，且当前环境真实支持 subagents、又不存在更高优先级策略阻断，就应实际启动 subagents，而不是留在本地主 agent 顺序扮演。
- 当 reviewer 为 `2` 个及以上时，subagent 分发默认生效；若 reviewer 较多，可按批次并行或按层串行，但不得因为人数超过某个固定阈值就自动跳过 subagent 路径。
- 仅在以下情况允许降级为本地顺序纪要：
  - 当前环境无法真实使用 subagents
  - 更高优先级策略明确阻断 subagent 调度
  - 用户显式要求不要启用 subagents
- 一旦降级，必须在结论中显式说明降级原因，不能把降级执行表述成正常 council 执行。

## 模式裁决

默认一个 subagent 对应一个 skill。

### `parallel-council`

满足以下条件时优先：

- reviewer 为 `2` 个及以上，且当前资源允许并行
- 各 reviewer 对同一目标做相对独立的判断
- 不需要先由前一个 reviewer 改完，后一个 reviewer 才能继续

执行方式：

- 并行启动多个 subagent
- 每个 subagent 只负责一个 skill 的局部评审
- 主 agent 负责最终 synthesis

### `serial-refine`

满足以下条件时优先：

- reviewer 之间存在明显依赖链
- 目标需要一轮一轮 refine，而不是一次性平行会诊
- 例如先编剧，再导演，再摄影/设计

执行方式：

- 逐个运行 reviewer
- 后一个 reviewer 可以读取前一个 reviewer 的结论或已落地 patch
- 每一轮都收束，避免累计无效意见

### `independent-only`

满足以下条件时优先：

- 用户只要独立意见，不要统一结论
- 目标不适合被 main agent 改写
- 需要保留互相冲突的观点供用户自行裁决

执行方式：

- 可以并行，也可以串行
- 但不强制形成统一 patch

### `auto`

若用户未显式给 `mode:`：

1. 单 reviewer -> 单 reviewer 直审
2. 多 reviewer 且互相独立 -> `parallel-council`
3. 多 reviewer 且有强依赖链 -> `serial-refine`
4. 用户明确说“只看法不改稿” -> `independent-only`

## `output:` 裁决

- `review-only`: 只输出评审，不改文件
- `synthesize-only`: 输出统一结论和优化方案，但不落盘
- `synthesize-and-patch`: 在目标可编辑时直接改文件
- `auto`:
  - 目标可编辑且用户要“评审并优化” -> 直接 patch
  - 目标不可编辑或风险高 -> 只给 synthesis

## 标准流程

1. 解析 reviewer selector 和 review target。
2. 校验目标文件存在且可读取。
3. 加载 `.agents/skills/team/SKILL.md`，锁定 council 根合同。
4. 解析 reviewer：
   - 显式路径优先
   - 名称匹配次之
   - `team.yaml` 再按显式映射和必要推断补齐
5. 确认 reviewer 集合，不设硬上限：
   - 用户显式给定或 `team.yaml` 显式映射出的 reviewer 默认保留。
   - 若 reviewer 明显重复、与目标无关或超出当前资源预算，可按必要性裁剪，并说明裁剪理由。
   - 当 reviewer 较多时，优先按问题域分组后分批并行或分层串行执行，而不是直接硬裁到固定人数。
6. 读取每个命中 reviewer 的 `SKILL.md`，再读取其同目录 `CONTEXT.md`。
7. 读取目标文件，并只补充最必要的相邻上下文。
8. 判定 `mode` 和 `output`。
9. 只要命中 reviewer skill 且无上层阻断，就为每个 reviewer 启动一个 subagent：
   - 并行模式下并发执行
   - 串行模式下按顺序执行
10. 仅当当前环境不支持 subagents，或被更高优先级策略阻断时：
   - 显式说明降级
   - 顺序读取各 reviewer 合同，模拟顾问纪要
11. 收集每个 reviewer 的局部输出，要求至少包含：
   - 核心判断
   - 主要问题
   - 可执行优化建议
   - 是否建议直接修改目标
12. 主 agent 执行 synthesis：
   - 合并共识
   - 标记冲突
   - 裁决优先级
   - 形成单一建议或 patch 计划
13. 若 `output` 允许且目标可编辑：
   - 直接对目标文件实施最小必要优化
   - 不扩大到无关文件
14. 输出结论，并注明 reviewer、模式、是否已落盘。

## Subagent 合同

- 默认一个 subagent 对应一个 skill。
- 每个 subagent 只拥有该 skill 的局部评审职责，不拥有最终写回权。
- 主 agent 仍是 canonical owner，负责：
  - reviewer 选择
  - 模式选择
  - synthesis
  - 最终 patch 或结论
- 不让 subagent 各自生成完整平行总稿。
- 不因 reviewer 多就自动扩大评审范围。
- 对 `master-check` 而言，显式调用本命令本身可视为用户已授权执行 reviewer 级 subagent 分发；若存在更高优先级策略限制，则必须显式报告该限制。

## 输出模板

### 口头总结

1. `评审团`: 本轮使用的 reviewer 与选择理由
2. `执行模式`: 并行/串行/独立
3. `关键问题`: 最重要的 3-5 个问题或亮点
4. `收束结论`: 主 agent 的统一判断
5. `优化动作`: 已改哪些内容，或建议下一步改什么
6. `未决分歧`: 仅在确实存在冲突时保留

### 结构化摘要

```yaml
master_check_result:
  target: "<path>"
  reviewers: []
  mode: "parallel-council|serial-refine|independent-only|single-reviewer"
  output_mode: "review-only|synthesize-only|synthesize-and-patch"
  used_subagents: true
  patched_target: false
  key_findings: []
  synthesis: ""
  unresolved_conflicts: []
```

## Error Handling

- reviewer 一个都无法解析时：
  - 停止
  - 报告无法命中的 selector
  - 提示用户改成明确 skill 路径、明确人物名或 `team.yaml`
- 目标文件不存在时：
  - 停止
  - 报告不存在的路径
- `team.yaml` 存在但没有任何可用 reviewer 映射时：
  - 先检查是否能从启用 role + 目标类型补出必要 reviewer
  - 若仍无法补出，停止并说明 `team.yaml` 缺少可执行 reviewer 映射
- 多 reviewer 结论冲突严重时：
  - 不伪造共识
  - 输出冲突点和主 agent 裁决依据

## 稳定经验

- council mode 的价值来自“必要视角 + 汇流裁决”，不是人数越多越好。
- 显式 reviewer 路径永远优先于自动推断。
- `team.yaml` 只能作为 reviewer 真源的一部分，不能被拿来替代 `.agents/skills/team/` 根合同。
- 对可编辑文本，评审后直接做最小 patch，通常比只给建议更有用；但对图片、视频和二进制对象，应以优化 brief 为主。
