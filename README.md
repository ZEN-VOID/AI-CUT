# AI-VCR

AI-VCR 是一个本地 AI 视频工作流与技能仓库，不是单一应用程序。它把课程/直播/录屏素材、视频生成与剪辑技能、HyperFrames 工程、执行报告和版本记录放在同一个工作区里，方便 Codex 按任务自动选择技能并产出可复核的视频交付物。

本仓库的默认主入口是 `.agents/skills/workflow/`。它面向直播课、录屏课、AIGC 创作教学、讲座、demo 或长视频素材，默认目标是把原始素材理解、重组、剪辑成一条完整教学长片和一组可独立观看的切片系列，并交付与最终视频时间轴匹配、画面可见的字幕。

## 目录结构

```text
.
├── .agents/
│   └── skills/                         # 仓库内 Codex 技能包
│       ├── workflow/                   # AI-VCR 主工作流：教学视频长片 + 切片系列
│       ├── hyperframes/                # HTML/CSS/JS 视频生成与渲染技能族
│       ├── media/                      # 通用媒体处理技能：下载、剪辑、时间戳、Remotion、GIF
│       ├── cli/mmx-cli/                # MiniMax / mmx 媒体生成命令封装
│       ├── video-editing-skill/        # 小红书/抖音/视频号短视频流水线子模块
│       ├── wis/                        # 王建硕个人工作流技能族
│       ├── wangjianshuo-perspective/   # 王建硕表达与思维框架
│       └── version-sync/               # VERSION.md 版本展示与同步机制
├── .codex/
│   ├── config.toml                     # Codex 本仓库运行配置
│   └── hooks/                          # Codex 事件钩子，含 github-push 版本同步入口
├── projects/
│   ├── 内容/                           # 文案、字幕、脚本、文章等内容输入
│   ├── 素材/                           # 长期素材池：视频、图片、音频、参考素材
│   ├── 示例/                           # 参考样片和演示素材
│   └── output/                         # 默认过程产物和最终输出
├── PRPs/                               # 规划、需求和任务设计文档
├── reports/                            # 执行报告、审计结果和验证记录
├── AGENTS.md                           # 仓库级 Agent 操作约定
├── VERSION.md                          # 仓库版本展示与更新历史
├── README.md                           # 本说明文档
└── .gitmodules                         # 子模块配置
```

`projects/素材/` 是长期素材池，不是一次性输出目录。真实视频、音频和大文件提交前需要确认授权和隐私边界。`projects/output/` 是默认输出位置，完整工作流通常会按任务名建立阶段目录，例如 `01-understanding/`、`03-edit-plan/`、`05-hyperframes/`、`final/`。

## 安装与同步

推荐连同子模块一起克隆：

```bash
git clone --recurse-submodules <repo-url>
cd AI-VCR
```

如果已经普通克隆过，再补拉子模块：

```bash
git submodule update --init --recursive
```

当前子模块：

```text
.agents/skills/video-editing-skill -> https://github.com/maxazure/video-editing-skill.git
```

常见本地依赖按实际任务安装：`ffmpeg`、`python3`、Node.js、HyperFrames CLI、Whisper/ASR 后端、Remotion 依赖等。不要提交 `.env`、API key、访问令牌、账号配置或私密素材。

## 技能包如何使用

Codex 会根据用户请求和每个 `SKILL.md` 的描述自动触发技能。你也可以在提示词中直接点名技能，例如 `/workflow`、`/hyperframes`、`/video-editing`、`/wjs-transcribing-audio`。

每个技能包通常包含：

```text
SKILL.md         # 技能触发条件、执行合同、完成门
CONTEXT.md 或 CONTEXT/  # 可复用经验、正反例和长期边界
scripts/         # 机械辅助脚本：抽取、校验、渲染、格式转换
templates/       # 输出模板或报告模板
tests/           # 技能本地回归测试
agents/          # 子 agent 或路由配置
references/      # 稳定规则、细则、审查合同或知识库
```

使用原则：

- 先让任务落到最窄合适技能，不要把所有视频任务都交给一个泛化流程。
- 内容判断、剪辑取舍、教学结构、提示词和创意正文由 LLM 直接完成；脚本只做读取、校验、渲染、转码和报告等机械辅助。
- 完整视频任务默认要有可复核过程产物、最终视频、字幕/sidecar 和报告；只做计划或只做审计时需要在提示词中说明。
- 修改某个技能包前，先完整读取它的 `SKILL.md`；技能默认合同变更要同步 `CONTEXT/`、模板、测试或 README 中的引用面。

## 主技能：workflow

路径：`.agents/skills/workflow/`

`workflow` 是 AI-VCR 的主链路，用于把直播教学、录屏课、AIGC 创作教学、讲座或 demo 素材重组成教学视频包。默认交付不是单条短视频，而是：

- 一条完整连贯长片：覆盖核心学习步骤，去除寒暄、等待、重复、跑题和操作失败空转。
- 一组可独立观看的切片系列：每条切片有上下文、核心讲解和自然收束。
- 与最终剪辑时间轴匹配、经过语义纠错和术语统一的字幕；完整渲染模式下字幕必须在最终 MP4 画面可见。
- 可复核的输出报告，说明素材依据、剪辑取舍、验证结果和遗留问题。

适合任务：

```text
/workflow
把 projects/素材/课程录屏 和 projects/内容/学习步骤.md 做成一条完整教学长片，
再切出 3-6 条可以单独发布的教学切片。字幕要烧进画面，同时保留 SRT。
输出到 projects/output/今天日期/。
```

不适合任务：

- 只转写音频或只翻译字幕：用 `wjs-transcribing-audio`、`wjs-translating-subtitles` 或媒体工具。
- 只做产品广告、纯情绪短片、音乐可视化：优先走 HyperFrames 对应工作流。
- 只上传发布：用发布类技能。

## HyperFrames 技能族

路径：`.agents/skills/hyperframes/`

HyperFrames 用 HTML/CSS/JS 构建可渲染视频。任何“做一个视频、动画、动效、字幕包装、图形覆盖、产品片、网页转视频、PR 讲解视频”等任务，通常先读 `/hyperframes` 作为路由入口，再进入具体技能。

| 技能 | 适用场景 |
| --- | --- |
| `hyperframes` | 视频/动画请求的总入口和路由器。先判断该走产品片、网页片、解释片、字幕、动效、音乐视频、幻灯片还是通用视频。 |
| `hyperframes-core` | 编写 HyperFrames HTML composition：`data-*` 时间轴、clip、track、媒体播放、变量、验证规则。 |
| `hyperframes-animation` | 动画和运动设计：GSAP、Lottie、Three.js、CSS keyframes、Web Animations API 等。 |
| `hyperframes-creative` | 视觉方向：配色、字体、分镜节奏、品牌风格、叙事节拍和画面密度。 |
| `hyperframes-media` | TTS、BGM、SFX、转写、字幕、背景移除和媒体资产处理。 |
| `media-use` | 查找、冻结和登记 BGM、音效、图片、icon 等媒体资产。 |
| `hyperframes-cli` | `npx hyperframes init/lint/validate/preview/render/doctor` 等 CLI 开发循环。 |
| `hyperframes-registry` | 安装和接入 HyperFrames registry blocks/components。 |
| `general-video` | 自定义长视频、多场景视频、品牌片、片头、循环动画等兜底视频工作流。 |
| `motion-graphics` | 短、无旁白、动效即信息的 motion graphic：大字报、数字增长、logo sting、lower-third、新闻/推文动效。 |
| `faceless-explainer` | 从文章、笔记、主题或 brief 生成无真人出镜解释视频。 |
| `product-launch-video` | 产品发布、功能介绍、SaaS promo、公司宣传和营销视频。 |
| `website-to-video` | 把一般网站或 URL 捕获成站点展示、导览或社媒视频。 |
| `pr-to-video` | 把 GitHub PR、代码变更或提交差异做成讲解视频。 |
| `embedded-captions` | 给已有 talking-head 视频加电影化/样式化字幕。 |
| `graphic-overlays` | 给已有访谈、播客、口播视频叠加 lower-third、数据卡、引用卡、图形包装。 |
| `music-to-video` | 以音乐为主时钟，生成卡点歌词、幻灯、节奏视觉或素材混剪。 |
| `slideshow` | 构建演示文稿、pitch deck、交互式 deck，而不是直接渲染成视频。 |
| `remotion-to-hyperframes` | 把已有 Remotion React composition 迁移成 HyperFrames HTML。 |

常用提示词：

```text
/hyperframes
根据这个产品 URL 做一个 45 秒产品发布视频，输出 16:9 MP4，并保留工程文件和渲染报告。
```

```text
/motion-graphics
做一个 8 秒的数字增长动效，透明背景，用作视频里的 overlay。
```

## 媒体处理技能

路径：`.agents/skills/media/`

这些技能更偏工具型，适合处理已有素材或生成剪辑辅助产物。

| 技能 | 适用场景 |
| --- | --- |
| `video-downloader` | 下载在线视频，用于离线查看、归档、剪辑或源素材处理。 |
| `timestamp-extraction` | 提取时间戳、剪辑点、静音段、语音段、场景边界或 frame-accurate edit points。 |
| `video-editing` | 用 MoviePy 计划批量剪辑、cut、overlay、音频处理和导出。 |
| `remotion` | 构建 Remotion React 视频 composition、时间轴、媒体和字幕。 |
| `slack-gif-creator` | 生成适合 Slack 的动画 GIF，控制大小、循环和时长。 |

## 短视频技能：video-editing-skill

路径：`.agents/skills/video-editing-skill/`

这是一个作为子模块接入的短视频内容引擎，面向小红书、抖音、微信视频号。它适合从口播音频、无声 B-roll、长视频或录屏素材出发，完成转写、粗剪、脚本重组、平台规则 lint、B-roll 调度、字幕、封面、三平台导出和发布包整理。

典型用途：

- 每日口播短视频：转写 -> 5 段式重组 -> 平台规则检查 -> 自动补 B-roll/章节卡/贴纸/BGM -> 渲染。
- 长视频提炼：根据 brief 或 query 找高光候选，并生成可审计 cut list。
- 平台适配：从一个 master 导出小红书 3:4、抖音 9:16、视频号 60 秒内版本。
- 剪辑交接：导出 EDL/FCPXML 给 Premiere、Final Cut Pro 或 Resolve。

常用提示词：

```text
/video-editing
用这段口播音频和 projects/素材/broll 生成一条小红书短视频，
需要字幕、BGM、封面、标题文案和发布包。
```

## mmx-cli

路径：`.agents/skills/cli/mmx-cli/`

`mmx-cli` 封装 MiniMax 平台能力，用于生成文本、图片、视频、语音和音乐，也可执行 MiniMax 模型对话、搜索或 API 资源管理。它通常作为 `workflow` 或其他视频技能的辅助能力，用来补充 TTS、音频或生成素材。

使用前通常需要在本地环境中配置 MiniMax 相关凭据；凭据只能放在本地环境或 `.env`，不得提交到仓库。

## 王建硕 / WIS 技能族

路径：`.agents/skills/wis/` 和 `.agents/skills/wangjianshuo-perspective/`

这组技能服务王建硕个人内容、发布、视频本地化、X/Twitter 增长和项目自动化。它们大多有明确触发词，适合直接点名使用。

### 视频与音频本地化

| 技能 | 适用场景 |
| --- | --- |
| `wjs-transcribing-audio` | 音频/视频转写成源语言 SRT。中文默认走 Volcano ASR，其他语言走 Whisper API。 |
| `wjs-translating-subtitles` | 翻译 SRT 或 transcript，输出目标语言或双语字幕。 |
| `wjs-dubbing-video` | 根据目标语言 SRT 生成时间对齐 TTS 配音。 |
| `wjs-burning-subtitles` | 把字幕烧进视频或软封装字幕轨，可与配音最终合成。 |
| `wjs-localizing-video` | 完整本地化编排：转写 -> 翻译 -> 配音 -> 烧字幕。 |

### 视频剪辑与后期

| 技能 | 适用场景 |
| --- | --- |
| `wjs-syncing-multicam` | 多机位或多音轨素材对齐，输出 `.sync.json` sidecar。 |
| `wjs-editing-multicam` | 基于同步结果自动切多机位，可加画中画。 |
| `wjs-reframing-video` | 横竖屏互转，跟踪说话人保持主体在画面内。 |
| `wjs-segmenting-video` | 长访谈/讲座/播客按主题切成 3-6 条短片原始包。 |
| `wjs-overlaying-video` | 给切片加封面、字幕、动效、章节条、CTA 和最终后期包装。 |
| `wjs-converting-text-to-video` | 把王建硕风格文章做成竖屏讲解视频。 |
| `wjs-teaching-english` | 把一个英文单词做成 HLS supercut 学习视频。 |
| `wjs-uploading-video` | 上传一个或多个视频到 YouTube，支持读取 `UPLOAD_META.md`。 |

### 写作、发布与分发

| 技能 | 适用场景 |
| --- | --- |
| `wjs-mining-articles` | 从视频 SRT 中挖掘多篇独立微信公众号文章。 |
| `wjs-mining-voicedrop` | 处理 VoiceDrop 录音，转写并挖掘文章。 |
| `wjs-publishing-wechat` | 微信公众号文章润色、题图、解释图和发布准备。 |
| `wjs-publishing-hugo` | 给 Hugo 静态博客新增或编辑文章、图片和类目并发布。 |
| `wjs-syndicating-articles` | 把最新微信公众号文章分发到 X、Bluesky、Threads、LinkedIn 等平台。 |
| `wjs-tweeting-from-articles` | 从最近文章中生成并发布每日 X/Twitter tweet。 |
| `wjs-polishing-x-engagement` | 改写中文推文，让事实支撑和互动钩子更强。 |

### 项目、App 与增长自动化

| 技能 | 适用场景 |
| --- | --- |
| `wjs-auditing-project` | 审计项目卡点：分支、PR、CI、build、计划漂移、日志错误。 |
| `wjs-looping-feedback` | 给网站加“提个建议”反馈闭环，自动生成 issue、PR、部署和回滚入口。 |
| `wjs-publishing-testflight` | 为 iOS 项目配置 fastlane 和 GitHub Actions 自动上传 TestFlight。 |
| `wjs-publishing-appstore` | 准备截图、文案和 metadata，并提交 App Store 审核。 |
| `wjs-cleaning-spam` | 清理 X/Twitter 推文下的垃圾回复。 |
| `wjs-promoting-skills` | 自动化推广 Claude/Codex skills。 |
| `wjs-x-improving-content` | 通过版本化 prompt 实验系统改进 X 内容质量。 |
| `wjs-x-increasing-follower` | 运行 X 涨粉实验，跟踪 profile visit -> follower 转化率。 |
| `wjs-eating-and-growing` | 个人复盘训练：从一次挫折抽象成新行为参数。 |
| `wjs-converting-wp-to-hugo` | 从 WordPress WXR 和 uploads 迁移到 Hugo 静态站。 |

`wangjianshuo-perspective` 是表达和思维框架技能，适合在写作、内容转述、文章挖掘和口吻校准时作为风格参考。

## 版本同步机制

路径：`.agents/skills/version-sync/`

`VERSION.md` 是展示页，不是规则页。版本递增、最后更新时间和更新明细由 `version-sync` 脚本维护：

```bash
python3 .agents/skills/version-sync/scripts/sync_version.py --level small
```

推荐先 dry-run：

```bash
python3 .agents/skills/version-sync/scripts/sync_version.py --dry-run --level small
```

github-push 版本钩子入口在：

```text
.codex/hooks/update_version_for_github_push.py
.codex/hooks/hooks.json
```

钩子配置在会话启动时加载；修改后通常需要重启 Codex/Claude 会话才会作为事件钩子生效。

## 常用检查

本仓库没有统一 root build 命令。改哪个技能，就跑哪个技能附近的测试或 dry-run。

```bash
python3 -m pytest .agents/skills/version-sync/tests
python3 -m pytest .agents/skills/video-editing-skill/tests
python3 .agents/skills/version-sync/scripts/sync_version.py --dry-run --level small
```

HyperFrames 或 Remotion 项目应在生成的项目目录内运行对应的 `npx hyperframes lint/validate/render` 或 Remotion 命令，不在仓库根目录硬跑。

## 提示词建议

为了让技能路由更稳定，建议一次性说明：

- 输入：文案、SRT、旁白音频、源视频、图片、参考样片、URL 或 PR。
- 目标：教学长片、切片系列、短视频、产品片、字幕、本地化、上传发布等。
- 输出：横屏/竖屏、时长、平台、语言、字幕形式、是否需要 sidecar。
- 素材边界：哪些素材必须用、哪些素材禁止用、是否允许生成新素材。
- 验收重点：字幕同步、教学完整性、节奏、转场、素材匹配、品牌露出、平台规则。

最小示例：

```text
/workflow
把 projects/素材/录屏课 和 projects/内容/课程步骤.md 做成教学长片 + 5 条切片。
最终视频要有可见字幕，保留 SRT，输出到 projects/output/课程名/。
```

## 注意事项

- 严禁提交 `.env`、API key、访问令牌、个人账号配置和未授权私密素材。
- 真实素材和生成产物提交前先确认体积、授权、隐私和复用边界。
- `CONTEXT/` 记录经验和边界，不承载规范真源；默认合同应写在对应 `SKILL.md` 或更高层级规则中。
- 公开分享仓库前先清查素材和历史记录；仓库公开期间别人可能 clone 或 fork，之后改回私有也不能保证已公开内容被收回。
