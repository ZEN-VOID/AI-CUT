# 道具 2-设计

`$aigc-prop-design` 将上游 `5-设计/道具/1-清单/道具清单.md` 扩展为每个道具主体一个细目设计 Markdown，并结合 `0-初始化/north_star.yaml` 与 `team.yaml` 中的全局风格和设计相关大师监制上下文。

## Directory Tree

```text
2-设计/
├── references/
│   └── prop-design-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── prop-design-workflow.md
├── knowledge-base/
│   └── prop-design-heuristics.md
├── types/
│   └── prop-design-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

1. 读取 `SKILL.md + CONTEXT.md`。
2. 读取项目 `MEMORY.md`、相关 `CONTEXT/`、`1-清单/道具清单.md`、`north_star.yaml`、`team.yaml`。
3. 按单道具主体执行 `steps/prop-design-workflow.md`。
4. 将研究转成 `source cue -> confidence -> visual translation -> design lock -> prompt evidence token`。
5. 使用 `templates/output-template.md` 输出到 `projects/aigc/<项目名>/5-设计/道具/2-设计/<安全文件名>.md`。
6. 按 `review/review-contract.md` 执行 subagent reviewer 或降级 review。

## Visual Entry Points

- 根入口图：`SKILL.md#visual-maps`，用于确认输入、模式、LLM-first 创作、review 和落盘主链。
- 业务来源图：`references/prop-design-contract.md#design-source-map`，用于确认清单、north_star、team、项目记忆如何汇入设计判断。
- 类型分流图：`types/prop-design-type-map.md#routing-topology`，用于确认关键道具、普通道具、冷门考据、多状态和安全敏感道具如何进入不同强调点。
- 审查汇流图：`review/review-contract.md#review-flow-map`，用于确认真实 reviewer subagent 与上层阻断时的降级路径。

## Boundaries

- 核心研究、物语、解构和提示词设计必须 LLM-first。
- 脚本只做机械读取、路径、安全文件名和格式检查。
- 本包不修改 registry、父级目录、角色设计、场景设计、`1-清单` 或 `3-生成`。
- 研究必须转译为形制、材料、工艺、年代、使用痕迹、功能逻辑、风险/不确定性和 prompt evidence chain。
- 固定为纯色背景单道具近景特写、45 度视角。
- 不置身剧情场景、桌面环境、室内陈设、街景或人物手持情境。
- 英文 prompt 必须包含 `close-up prop shot, 45-degree view, solid color background, no scene environment` 等等价约束。
