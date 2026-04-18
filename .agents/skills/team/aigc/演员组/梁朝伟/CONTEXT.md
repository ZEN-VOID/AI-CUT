# 梁朝伟表演视角 CONTEXT

## Context Health

- last_checked: 2026-04-15
- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- maintenance_policy: 知识库模式；优先更新 Type Map、Repair Playbook、Reusable Heuristics。详细过程和低频材料外置到 `CHANGELOG.md` 或 `reports/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 输出变成“眼神杀”粉丝赞美 | `SKILL.md` 模型被标签化 | 删除粉丝词，改写为听、呼吸、停顿、重心和镜头距离 | 保留 `silence_eye` 与 `body_pressure` 字段 | 答案含至少一个身体动作和一个镜头处理 |
| 沉默被滥用 | `hidden_pressure` 未区分动机 | 写清沉默是防御、欲望、观察还是羞耻 | 决策启发式中保留“沉默必须有任务” | 每段沉默都有行动目的 |
| 王家卫化过度 | 外部评价压过作品跨度 | 加入《无间道》《色，戒》《一代宗师》《尚气》类型约束 | 研究维度要求先识别导演和类型 | 不把所有建议写成慢镜头怀旧 |
| 表演建议空泛 | 字段没有落到可执行动作 | 补眼神、呼吸、手、肩颈、步伐、空间距离 | Step 3 固定输出身体方案 | 演员可直接排练 |
| 高风险戏缺安全边界 | `risk_boundary` 漏填 | 增加同意、动作边界、停机词、替代拍法 | 高心理暴露场景强制边界提醒 | 答案先写边界再写情绪 |
| 事实或奖项错误 | source_check 缺失 | 回到 `references/research/` 或联网核对 | 对奖项、年份、作品事实使用机构来源 | 不确定事实标注待核对 |
| 非 ASCII 路径下工具脚本缺失 | 脚本复制后未读回验证 | 用带引号路径重新复制并 `find/ls` 读回 | 新建演员 skill 后把脚本目录纳入结构校验 | `scripts/quality_check.py` 可直接运行 |

## Repair Playbook

1. 先识别失败是否来自粉丝化、王家卫化、空泛化、安全边界缺失或事实错误。
2. 回读 `SKILL.md` 的轻量字段映射，定位对应 `field_id`。
3. 需要事实时优先查 `references/research/06-timeline.md` 与机构来源 URL。
4. 修输出时先写“这场戏的秘密”，再写身体，最后写镜头。
5. 新建或迁移 skill 时，先读回 `scripts/`、`references/research/`、`agents/openai.yaml`，避免非 ASCII 路径下复制遗漏。
6. 如果新增经验只适用于梁朝伟，写入本 `CONTEXT.md`；若跨演员组复用，向演员组主合同或共享模板晋升。

## Reusable Heuristics

- 梁朝伟式表演不是“少演”，而是“让观众看见你在压住什么”。减法必须有压力源。
- 眼神不应作为第一个动作设计。先设计听见、呼吸、身体微移，再让眼睛成为最后泄露点。
- 处理王家卫相关类比时，必须同时检查导演、摄影、剪辑和叙事留白；不要把影像风格误归因给演员个人。
- 商业类型片中的梁朝伟式方法是“保留人的细节”，不是把类型节奏拖慢。
- 对《色，戒》、亲密戏、暴力戏和羞辱戏的迁移必须先写职业边界；不能浪漫化消耗演员。

## Source Notes

- 机构来源优先：香港电影资料馆、Venice Biennale、Festival de Cannes、香港演艺学院、Asian Film Awards Academy。
- 媒体长访谈可用于表达 DNA 与工作习惯，但不能替代机构事实。
- 粉丝剪辑、百科、论坛、二次转述默认低权重；只作为发现线索，不作为最终证据。

## Promotion Candidates

- “沉默必须有任务”“眼神是最后泄露点”若在其他演员 skill 中复用，可提升为演员组共享表演模板。
- “导演语言决定表演大小”适合晋升为演员组跨导演项目的前置研究门槛。
