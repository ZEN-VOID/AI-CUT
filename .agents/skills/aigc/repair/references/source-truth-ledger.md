# Source Truth Ledger

本文件定义 `aigc-repair` 的真源 owner、写回顺序和禁止越权边界。

## Truth Owners

| layer | owns | repair rule |
| --- | --- | --- |
| `MEMORY.md` | 项目长期偏好、稳定禁区、持续口味 | 用户明确长期要求或多阶段持续生效时才写回 |
| `CONTEXT/` | 项目共享参考、运行期附加事实、参考片解析 | 项目补充事实写这里，不替代阶段合同 |
| `0-初始化` | north_star、项目风格、团队和初始治理 | 全局方向、题材元素、风格锚点错误先修此层 |
| `1-分集` | 原文分集、集边界、零改写源文本 | 漏段、错集、原文边界问题先修此层 |
| `2-编剧` | 剧情事实字段化、对白保真、slugline、声画配对 | 可拍事实和对白错误先修此层 |
| `3-导演` | 戏剧问题、视觉主轴、氛围、高潮与终结画面 | 意境、美学、导演判断错误先修此层 |
| `4-表演` | 表演动作、心理反应可见化、潜台词和调度 | 演员可执行性错误先修此层 |
| `5-摄影` | 景别、运镜、焦点、光影、时长、连续性锚点 | 镜头和 AI 视频可执行性错误先修此层 |
| `6-分组` | 组边界、组间桥接、入场/出场、统计、组级 prompt 基础 | 分镜组消费单位错误先修此层 |
| `7-设计` | 场景、角色、道具清单/设计/生成请求 | 资产身份、造型、物件逻辑和引用错误先修此层 |
| `8-图像` | 帧图、故事板、图像 prompt、reference manifest、生成报告 | 图像任务与成图证据由对应 leaf 持有 |
| `9-视频` | 视频任务、reference 绑定、生成结果、MP4 证据 | 视频生成证据由对应 leaf/provider 持有 |
| `10-审片` | 实际视频缺陷证据、review finding、repair route | 只拥有审查和路由，不直接拥有上游正文 |
| `review/` | checkpoint/stage/package gate、aggregate verdict | 不直接改写业务产物 |
| `STATE.json` / `governance-state.yaml` | runtime 状态、断点、治理桥接 | 记录状态，不制造创作事实 |

## Writeback Order

默认顺序：

1. 用户授权的新长期记忆或禁区：`MEMORY.md`。
2. 最早 canonical source owner：`0-初始化` 到 `7-设计` 中对应最早层。
3. 同层相邻或投影：同集前后场、同分镜组、同一资产 alias 或同一阶段报告。
4. 下游文本产物：后续阶段文本、prompt、handoff、manifest。
5. 生成资产状态：保留、失效、重建任务或重跑 provider。
6. review aggregate、`10-审片` finding、`STATE.json`、`governance-state.yaml`。
7. 后续生成 guardrail 和项目 `CONTEXT/` 补充。

## Authorship Boundary

- `aigc-repair` 持有 diagnosis、impact map、source owner、repair plan、doubao task packet、汇流和验收。
- 创作性文本改写由 owning stage 的合同和豆包执行 lane共同约束：豆包可以生成分析、润色、repair brief 或候选改写，但写回前必须按 owning stage review gate 裁决。
- 图像和视频结果由 image/video provider skill 或对应 leaf 持有；repair 不伪造生成结果。
- 脚本可读取、diff、统计、格式转换和校验，不得生成 canonical creative truth。
- 若用户显式切换模型或禁用豆包，最终报告必须记录模型切换、降级路径和未执行 provider。

## Source Rule Review Record

每次执行型修复至少记录：

```yaml
source_rules_reviewed:
  - skill_path: ""
    context_path: ""
    loaded_references:
      - ""
    loaded_steps:
      - ""
    loaded_types:
      - ""
    loaded_review:
      - ""
    rule_summary: ""
    owner_decision: ""
```
