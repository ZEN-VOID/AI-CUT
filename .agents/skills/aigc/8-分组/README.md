# aigc 8-分组

`8-分组` 将 `projects/aigc/<项目名>/7-摄影/第N集.md` 的逐集摄影稿切成完整分镜组；用户显式指定其他文稿、粘贴文本或要求跳过摄影稿时，以指定 source 优先并在报告中记录 `source_override=true`。每组重复当前场景标题，在场景标题下方输出 `全局风格：`，随后进入普通分镜正文和 YAML 统计；相邻分镜组的连续性由下一组第一个普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 时间码分镜行承担，这个内部口径称为 `回龙帧`。回龙帧必须复现上一组尾帧状态锚点：可见主体、动作余势、关键道具/介质、光声残留和空间关系，再只调整景别和镜头视角；若该点来自对白、独白、旁白或音效画面，必须同步带入对应声音内容；不生成 `## A~B` 组间连接件，也不输出 `增补首帧：` 或 `回龙帧：` 字段。

## 目录树

```text
8-分组/
├── references/
├── scripts/
├── templates/
├── review/
├── knowledge-base/
├── types/
│   ├── type-map.md
│   └── grouping-type-map.md
├── agents/
│   └── openai.yaml
├── test-prompts.json
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## 快速入口

- 技能入口：`SKILL.md`
- 运行上下文：`CONTEXT.md`
- 项目级必读：`projects/aigc/<项目名>/MEMORY.md`
- 美学上下文：`projects/aigc/<项目名>/2-美学/类型风格.md`、`projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `2-美学/<风格>/风格协议.md`
- 初始化上下文：项目 `MEMORY.md` / `project_memory_init_context`
- 边界规则：`references/group-boundary-contract.md`
- 类型索引：`types/type-map.md`
- 画面基调风格整理：`references/visual-tone-projection-contract.md`
- YAML 统计：`references/statistics-yaml-contract.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`
- 机械校验：`scripts/validate_storyboard_groups.py`
- 回归 prompts：`test-prompts.json`

## 输出

- 输入：优先 `projects/aigc/<项目名>/7-摄影/第N集.md`；也接受用户显式指定的分镜稿、摄影稿、剧本/编导稿或粘贴文本
- 风格真源：`projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md` 的 `Global Style Prompt`；题材与下游边界来自 `2-美学/类型风格.md`、`美学总览.md` 和对应风格协议
- 分组综合：只读消费项目 `MEMORY.md` / `project_memory_init_context`，不调用 team 身份、旧 stage profile、旧初始化风格载体或新顾问问答
- 时长口径：标准摄影路径按 `7-摄影` 正文中的完整 `分镜N（起始秒-结束秒）：...` 行或兼容 `[起始秒-结束秒]` 行作为 atomic unit 累计；direct screenplay / 无显式时长 source 路径由 LLM 按剧本声画 atomic unit 规划约 14.5 秒/组，通常 10-11.5 秒，硬上限 14.5 秒；落盘后使用当前分镜组基准下连续递增的 `分镜N（N-N秒）：` 或 `[N-N秒]` 时间码，后一个时间段起点接前一个终点，组内 `时长估算` 取最终结束秒；最终累计结束秒必须以 `.5` 结尾，若自然相加不是 `.5` 结尾则在组尾上调 0.5 秒；组头、场景标题、全局风格和 YAML 不计入时长
- 输出：`projects/aigc/<项目名>/8-分组/第N集.md`
- 报告：`projects/aigc/<项目名>/8-分组/执行报告.md`
- YAML 主体统计：`角色`、`场景`、`道具` 的非空项必须写成 `id + name`，并命中 `projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `id` 与 `canonical_name`
