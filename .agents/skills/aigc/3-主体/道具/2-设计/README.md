# 道具 2-设计

`$aigc-prop-design` 将上游 `3-主体/道具/1-清单/道具清单.md` 扩展为每个道具主体一个细目设计 Markdown，并结合 `2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/道具风格/道具风格协议.md`、`0-初始化/north_star.yaml` 与 `team.yaml.init_synthesis` 中的设计约束、启发和风险。

## Directory Tree

```text
2-设计/
├── references/
│   ├── prop-design-contract.md
│   ├── design-output-contract.md
│   ├── design-slot-review-contract.md
│   └── workflow-supervision-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   ├── prop-design-corpus.md
│   └── prop-design-heuristics.md
├── types/
│   └── prop-design-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
└── README.md
```

## Quick Entry

1. 读取 `SKILL.md + CONTEXT.md`。
2. 读取项目 `MEMORY.md`、相关 `CONTEXT/`、`1-清单/道具清单.md`、`2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/道具风格/道具风格协议.md`、`north_star.yaml`、`team.yaml.init_synthesis`。
3. 按 `SKILL.md` 的 Thinking-Action Node Map 执行单道具主体设计；旧 workflow 语义已并入 runtime spine，不再作为第二规则源。
4. 将研究转成 `source cue -> confidence -> visual translation -> design lock -> prompt evidence token`。
5. 触发道具审美、文化/身份符号、工艺/结构细节、功能结构、使用/保存状态或 prompt 短语时加载 `knowledge-base/prop-design-corpus.md`，并原创转译为符合项目时代语境的设计细节。
6. 使用 `templates/output-template.md` 输出到 `projects/aigc/<项目名>/3-主体/道具/2-设计/PROP-###-<安全文件名>.md`。
7. 按 `review/review-contract.md` 执行初始化综合消费检查或本地 review；不得调用 team 身份或旧 stage profile。

## Visual Entry Points

- 根入口图：`SKILL.md#visual-maps`，用于确认输入、模式、LLM-first 创作、review 和落盘主链。
- 业务来源图：`references/prop-design-contract.md#design-source-map`，用于确认清单、north_star、team、项目记忆如何汇入设计判断。
- 类型分流图：`types/prop-design-type-map.md#routing-topology`，用于确认关键道具、普通道具、冷门考据、多状态和安全敏感道具如何进入不同强调点。
- 审查汇流图：`review/review-contract.md#review-flow-map`，用于确认外部 reviewer provider 与不可用时的本地路径。

## Boundaries

- 核心研究、物语、解构和提示词设计必须 LLM-first。
- 脚本只做机械读取、路径、安全文件名和格式检查。
- 不得用脚本批量生成、批量插入、正则套句或映射投影研究、物语、Photography、Prop Design、prompt evidence chain 或英文提示词。
- 本包不修改 registry、父级目录、角色设计、场景设计、`1-清单` 或 `3-生成`。
- 研究必须转译为形制、材料、工艺、年代、使用/保存状态、功能逻辑、风险/不确定性和 prompt evidence chain。
- 道具必须有可见设计价值；不得只是简单功能还原或平凡物件。普通功能道具也至少需要材质、比例、使用/保存状态、结构或工艺上的设计美感；不得把“设计感”默认写成磨损、污渍、包浆、锈蚀、破损、折旧感、文化贴花或装饰纹样。
- 文化/身份符号、纹样、铭文、徽记、封缄、器型、材质和装饰必须符合项目时代、地域、阶层、职业、宗教/族群禁区与功能逻辑；风格化不能脱离时代语境，无依据时采用极简、洁净或功能主导细节。
- `knowledge-base/prop-design-corpus.md` 是道具审美和文化细节的高质量语料库；触发时必须加载，但只能做原创转译，不能逐字套用或覆盖上游清单、道具风格协议、`north_star.yaml` 和用户禁区。
- 固定为纯色背景单道具完整全貌展示、45 度视角，完整展示道具全貌、完整轮廓和主要结构；不得做局部特写、裁切特写或半截道具画面。
- 仅展示道具本体，不置身剧情场景、桌面环境、室内陈设、街景或人物手持情境，不出现人物或背景元素。
- `## 4. 解构` 下方必须先写 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID、英文 prompt 开头保持一致。
- 输出文档文件名必须带同一主体 ID 前缀，例如 `PROP-001-<安全文件名>.md`；若上游已有主体 ID，则沿用该 ID。
- 最终英文整合 prompt 的整合对象是 `## 4. 解构` 的全部有效 Photography 与 Prop Design 信息；只拼主体 ID、画面基调、道具风格、固定画面词或负向词等前缀/后缀不算完成。
- 英文 prompt 必须控制在 1300 characters 内，并使用自然语言负向约束，不得使用 Midjourney `--no` 参数。
- 英文 prompt 必须以主体 ID 号开头，并包含 `full-view prop shot, 45-degree view, full prop in view, entire prop fully visible, uncropped full silhouette, prop only, solid color background, no people, no background elements, no scene environment` 等等价约束。
- `design-output-contract.md`、`design-slot-review-contract.md` 和 `workflow-supervision-contract.md` 必须进入入口加载、执行节点和 review gate，不得作为旁路文档漂移。
