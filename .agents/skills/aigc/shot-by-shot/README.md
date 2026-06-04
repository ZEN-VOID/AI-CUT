# aigc shot-by-shot

`shot-by-shot` 是 `.agents/skills/aigc` 的临摹型卫星技能，用于把参考影片或视频逐镜拆解成可回指证据、可迁移原则和 AIGC 项目 side context。风格解析输出对齐 `.agents/skills/aigc/3-美学` 六个子技能关注点；`分镜脚本.md` 保持 Numbers 示例 19 列合同不变。

## 目录树

```text
shot-by-shot/
├── references/
├── scripts/
├── templates/
├── review/
├── knowledge-base/
├── types/
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
- 典型评估 prompts：`test-prompts.json`
- 基础解析维度：`references/analysis-method.md`
- 3-美学风格解析细则：`references/aesthetic-style-analysis-contract.md`
- 非美学 stage 输出融合：`references/adaptation-output-contract.md`
- 编剧风格解析细则：`references/screenwriter-style-analysis-contract.md`
- 摄影解析兼容细则：`references/cinematography-style-analysis-contract.md`
- 旧设计聚合兼容细则：`references/design-style-analysis-contract.md`
- 分镜脚本细则：`references/storyboard-script-contract.md`
- 证据与版权边界：`references/evidence-and-rights-boundary.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`

## 输出

所有文档统一落点在 `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/`：

- 主报告：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/shot-by-shot.md`
- 画面基调解析：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/画面基调解析.md`
- 角色风格解析：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/角色风格解析.md`
- 场景风格解析：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/场景风格解析.md`
- 道具风格解析：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/道具风格解析.md`
- 摄影风格解析：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/摄影风格解析.md`
- 分镜风格解析：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/分镜风格解析.md`
- 分镜脚本：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/分镜脚本.md`
- 执行报告：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/执行报告.md`

`分镜脚本.md` 只在用户要求或任务需要表格式分镜脚本时输出；表头与列顺序仍以 `references/storyboard-script-contract.md` 为准。
