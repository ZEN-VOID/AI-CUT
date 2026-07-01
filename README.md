# AI-CUT

AI-CUT 是一个面向 Codex 的视频工作流与技能仓库，不是单一应用程序。它把视频创作、素材整理、执行报告和可复用技能放在同一个工作区里，重点服务于基于 Codex 的自动成片流程。

仓库的核心入口是 `.agents/skills/workflow/`。这个技能用于把文案、旁白、素材、参考样片和输出要求组织成一个 HyperFrames-native 视频工程，并默认完成预览、校验、渲染和报告。

## 目录说明

```text
.
├── .agents/skills/           # Codex 本地技能
│   └── workflow/             # 主要视频工作流技能
├── .codex/                   # Codex 路由、规则、模板和运行约定
├── projects/                 # 素材池、示例和输出目录
├── PRPs/                     # 规划、需求和任务设计文档
├── reports/                  # 执行报告、审计结果和验证记录
└── AGENTS.md                 # 仓库级 Agent 操作约定
```

`projects/素材/` 和 `projects/示例/` 是长期素材池。它们可以存放视频、图片、音频、文案、参考样例和素材分类目录。`projects/output/` 是默认输出位置。

## 安装

推荐连同子模块一起克隆：

```bash
git clone --recurse-submodules https://github.com/ZEN-VOID/AI-CUT.git
cd AI-CUT
```

如果已经普通克隆过，再补拉子模块：

```bash
git submodule update --init --recursive
```

## workflow 是什么

`.agents/skills/workflow/` 是本仓库的主视频工作流。它负责：

- 读取用户给出的文案、旁白、素材目录、参考视频或目标平台要求。
- 建立素材证据和视觉计划，而不是随机拼接素材。
- 生成 HyperFrames 工程，用 HTML/CSS/JS 管理字幕、背景视频、画中画、大字报、转场和音频。
- 执行字幕同步、视觉合同、预览、渲染和最终报告。
- 默认输出 16:9、1920x1080 的 final MP4；除非用户明确指定其他比例。

典型输出包括：

- `workflow_intake.json`
- `asset_evidence.json`
- `dialogue_alignment.json`
- `STORYBOARD.md`
- `workflow_composition_plan.json`
- HyperFrames project 文件
- final MP4
- `reports/workflow-execution-report-YYYYMMDD-HHMM.md`

## 在 Codex 界面中使用 `/workflow`

1. 在 Codex 桌面端或 Codex 工作区中打开本仓库目录。
2. 确认当前工作区根目录是 `AI-CUT`。
3. 在聊天输入框中以 `/workflow` 开头描述任务。
4. 附上或写明文案、旁白、素材目录、参考视频、目标平台和输出要求。
5. Codex 会加载 `.agents/skills/workflow/SKILL.md` 和 `CONTEXT/` 经验文件，再按任务需要调用 HyperFrames 相关能力。

最小调用示例：

```text
/workflow
根据 projects/素材 里的素材，帮我把这段文案做成一条 16:9 视频。
文案：……
输出到 projects/output/今天日期/
```

带参考和素材的调用示例：

```text
/workflow
用 projects/素材/漫剧素材 和 projects/素材/收益素材 做一条爆款口播视频。
参考节奏看 projects/示例/reference.mp4，只学习节奏、字幕和转场，不复制内容。
旁白音频在 projects/input/voice.wav。
最终输出 1920x1080，生成可检查的执行报告。
```

批量任务示例：

```text
/workflow
根据 projects/文案/batch.md 里的多条文案批量生成视频。
素材从 projects/素材 中选择，避免连续视频重复使用同一组素材。
最终成片统一放到 projects/output/今天日期/成片/
```

修复任务示例：

```text
/workflow
检查 projects/output/2026-06-30/过程/demo/ 里的 HyperFrames 工程。
重点修复字幕不同步、画中画遮挡字幕、背景素材不贴合的问题。
修复后重新验证并渲染 final。
```

## 提示词建议

为了让 `/workflow` 更稳定，建议一次性说明这些信息：

- 成片目标：广告、教程、口播、漫剧混剪、产品介绍、批量获客等。
- 输入内容：文案、文章、字幕、旁白音频、源视频、图片、参考样片。
- 输出要求：横屏或竖屏、时长、语言、字幕风格、目标平台。
- 素材边界：哪些素材必须用、哪些素材禁止用、是否允许生成新素材。
- 验收重点：字幕同步、节奏、转场、素材匹配、引流段、品牌露出。

如果没有指定输出比例，`workflow` 默认使用 `16:9`、`1920x1080`。如果要做抖音、小红书、Shorts 等竖屏视频，请明确写出 `9:16` 或目标尺寸。

## workflow 的核心原则

`workflow` 不只是把文案逐句配素材。它会先规划视频结构，再把素材放到对应层级：

- `hook_opening`：开头 3-5 秒建立反差、结果或利益点。
- `content_body`：主体内容，覆盖漫剧、工具演示、收益证明等证据。
- `private_traffic_cta`：引流或下一步行动。

每个段落默认包含四层：

- `background_video`：连续背景视频或主视觉承托。
- `semantic_pip`：跟随文案 cue 出现的画中画证据。
- `dialogue_caption`：严格跟随旁白或字幕主时钟。
- `editorial_overlay`：大字报，用短词或短句概括当前段落。

## 验证和渲染

`workflow` 普通任务默认要产出 final MP4。只有用户明确要求只做计划、只做审计、只生成素材证据，或运行环境缺少依赖时，才会停在中间产物。

常见验证包括：

```bash
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final <project-root> --write-report <project-root>/dialogue_sync_validation.json
python3 .agents/skills/workflow/scripts/validate_visual_contract.py <project-root> --write-report <project-root>/visual_contract_validation.json
npx hyperframes lint
npx hyperframes validate
npx hyperframes render
```

## 注意事项

- 不要把 `.env`、API key、私密素材或账号信息提交到仓库。
- `projects/素材/` 是素材池，不是一次性输出目录。
- 空目录通过 `.gitkeep` 保留；真实视频、音频和大文件应确认授权后再提交。
- 如果公开分享仓库，公开期间别人可能 clone 或 fork，之后再改回私有也无法保证已经公开的内容被收回。
