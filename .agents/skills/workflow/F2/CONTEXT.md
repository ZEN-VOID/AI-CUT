# Context: F2

本文件是 F2 的经验层知识库，不是执行流水。F2 的规范真源在 `SKILL.md`；本文件只沉淀可复用失败模式、修复打法和 HyperFrames-native 工作流经验。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
recommended_action: keep-focused-on-hyperframes-native-lessons
last_checked_at: 2026-06-29
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-F2-01` | 任务又回到 F1 scripts、EDL 或 ffmpeg 滤镜链 | 实现真源漂移 | 回到 `N2-HYPERFRAMES-LOAD`，把实现收束到 HyperFrames 子技能 | Review gate 固定 `FAIL-F2-HYPERFRAMES-ONLY` | module list 中无 F1 runtime 依赖 |
| `TM-F2-02` | HTML 写出来了，但画面选择和字幕没有证据 | 计划前置缺失 | 回 `N3/N4/N5` 补 `asset_evidence`、`dialogue_alignment` 和 storyboard | 先证据、再计划、再 authoring | 每个 plan item 有 cue/source anchor |
| `TM-F2-03` | 字幕看似同步但语义和旁白不一致 | 主时钟不严 | 重新转写或人工复核，按语义拆 cue | 禁止全片比例字幕 | `dialogue_alignment.json` 能回指音频/脚本 |
| `TM-F2-04` | PiP、大字报或字幕挡住关键 UI | 安全区未验证 | 回 `N7` 截图检查并回 `N6` 调整布局 | Preview gate 必须抽查首/中/尾和强调段 | snapshot 显示叠层安全 |
| `TM-F2-05` | 参考片内容误入成片 | 参考边界失败 | 移除参考素材，只保留 rhythm/style evidence | `reference_media` 不进入 source pool | asset manifest 不含 reference-only 素材 |
| `TM-F2-06` | final MP4 缺音轨或时长漂移 | render 验证不足 | 回 `N8` 检查 render log 和 media tracks | final 必须做文件/音轨/时长检查 | final 非空、可播放、有音轨 |
| `TM-F2-07` | CLI 不可用却宣称完成 | 验证门自我声明 | 降级为 project/plan 交付，报告阻断 | `C6/C7` 不通过不得说 final pass | 报告中有阻断和下一步 |
| `TM-F2-08` | F2 普通任务停在可预览工程，用户随后要求“需要最终成片” | 完成态定义过低 | 立即回 `N8` render 并做 ffprobe/抽帧检查 | `SKILL.md` 明确 F2 默认完成态是 final MP4；project build 只作显式 no-render 或阻断降级 | 普通 F2 任务报告中有 final MP4 或明确 no-render 豁免 |
| `TM-F2-09` | F2 普通任务未指定比例却产出竖屏 | 默认画幅未锁定 | 回 `N1/N6/N8` 改为 16:9、1920x1080 并重新 render/ffprobe | `SKILL.md` 明确默认 16:9；非 16:9 必须有用户/项目显式依据 | `f2_intake.json` 与 final ffprobe 尺寸一致 |
| `TM-F2-10` | 成片出现 `F2 HyperFrames / 文案X` 这类流程标识 | authoring 把工程标签误当内容标签 | 回 `N5/N6` 删除工具/流程水印，只保留内容内生的标题、证据标签和品牌露出 | `SKILL.md` 禁止默认工具/流程水印；需要署名必须用户显式要求 | snapshots/final frames 无 F2/HyperFrames/文案编号水印 |
| `TM-F2-11` | 最终成片字幕和台词音频不同步，或报告只写 manual duration | Dialogue Sync Contract 缺证据 | 回 `N4` 做 ASR 或逐 cue 人工校时，区分台词字幕和编辑性大字报 | `SKILL.md` 明确台词字幕必须满足同步容差；无转写时人工校时不能省略音频锚点 | `dialogue_alignment.json` 有 per-cue audio anchors 和 sync notes |
| `TM-F2-12` | 规则写了严格同步，但最终成片仍能带着预览级 cue 过关 | 缺机械门禁 | 运行 `scripts/validate_dialogue_sync.py --strict-final`，按 fail code 回 `N4` | `SKILL.md` 把 validator 接到 C3/C7；模板报告 `dialogue_sync_validation.json` | validator JSON 为 pass，且报告记录 fail/warn count |
| `TM-F2-13` | 社媒广告成片像动态 PPT，背景只是渐变/卡片/静态图，缺少影像承托 | 视觉计划把信息结构当成最终画面语言 | 回 `N3/N5/N6`，默认逐段用源视频/影像内容/工具实录做 `video_background`；静态资产改为 PiP 或短促 punch-in；图片背景只作逐段 fallback | `SKILL.md` 的 Social Ad Visual Contract；计划必须区分 background_layer、background_video、image_background_fallback、pip_asset、editorial_overlay | snapshot/final frame 有视频背景承托；如有图片背景，必须有 fallback_reason |
| `TM-F2-14` | 成片出现“证据推进”“痛点爆破”“pipeline”等内部思考路径或 logo-like 水印 | Storyboard/HTML 把执行节点名误当观众可见文案 | 回 `N5/N6`，删除内部标签；大字报改成钩子、反差、结果或 CTA | `FAIL-EDITORIAL-OVERLAY`、`FAIL-WORKFLOW-WATERMARK` | frame check 不含内部节点名、F2/HyperFrames/pipeline/文案编号 |
| `TM-F2-15` | 大字报和主字幕说同一句话，PiP 单调或多窗不齐 | editorial overlay 没有和 dialogue_caption 分工 | 回 `N5` 重写 overlay 计划：主字幕负责台词，大字报负责提炼；多 PiP 用统一网格和安全区 | Social Ad Visual Contract；`f2_composition_plan.json` 明确 overlay/pip 分工 | 大字报与字幕非逐句重复；PiP 对齐且不挡字幕 |
| `TM-F2-16` | 为了规避 render/inspect 超时，把全片背景一次性降级为图片 | 技术兜底没有类型边界，导致创意机制被性能问题覆盖 | 回 `N5/N6/N7`，改成短视频背景片段、低码率代理、少量并发或逐段 fallback；不得全局替换为图片 | `FAIL-BACKGROUND-LAYER-TYPE`；计划记录每段 background type 和 fallback reason | video_background 段可预览/渲染；image_background 段数量和理由可审计 |
| `TM-F2-17` | 背景视频高度重复，或和台词语义只是泛泛相关 | 背景层只做固定轮换，没有使用结构化素材说明和 segment 语义 | 回 `N3/N5` 读取 `素材/视频/视频说明.yaml`，按 segment 的 `semantic_tags`、`visual_content`、`best_for`、category 选段；同条成片和批量生成都惩罚重复 | `FAIL-BACKGROUND-DIVERSITY-MATCH`；background selection map 必须可审计 | 每个背景段有 segment_id、match_reason；同条 final 内重复源视频/segment 尽量降到最低 |
| `TM-F2-18` | 画中画高度重复，或平台截图、角色设定、场景资产和台词 cue 不匹配 | PiP 层只做固定图片轮播，没有读取 `图片说明.yaml` 的 role/tags/best_for/avoid_for/text_overlay | 回 `N3/N5` 读取 `素材/图片/图片说明.yaml`，按图片 role 和语义匹配 cue；同条成片和批量生成都惩罚同图/同角色重复，高文字截图只在平台/收益/工具证明 cue 中优先使用 | `FAIL-PIP-DIVERSITY-MATCH`；pip selection map 必须可审计 | 每个 PiP 有 image_id、role、match_reason；单片内不再由少数图片反复轮播 |
| `TM-F2-19` | 多条文案语义相近时，成片被短视频平台判重或限流 | 只按粗标签匹配素材，未建立同批使用台账和复用冷却 | 回 `N3` 补 `semantic_vector/trigger_profile/visual_signature/variation_profile`，回 `N5` 按 `asset_usage_ledger.json` 重排素材 | `FAIL-ASSET-USAGE-LEDGER` / `FAIL-PLATFORM-DEDUP-DIVERSITY` | ledger before/after 可追踪；相邻输出 hook 背景和首屏 PiP 不重复 |
| `TM-F2-20` | 同义文案批量输出看起来只是轻微换顺序或换字 | storyboard 没有强制变化轴，只改文本不改视觉机制 | 回 `N5` 至少变化 2 个轴：背景组合、PiP、首屏构图、转场节奏、大字报、BGM/SFX 节点、色彩/版式 | `asset_diversity_audit.json` 必填 variation_axes | 每条成片的 variation_axes 与 snapshot/frame evidence 对应 |
| `TM-F2-21` | 长视频素材被反复选中同一视觉段，其他可用段未进入候选 | `video-to-manifest` 只看整条长视频摘要，没有 60 秒内 analysis slices | 回共享 `video-to-manifest` 的 `N2/N3`，补 `analysis_slices[]` 和 slice 级标签，再回 F2 `N3/N5` 重选 | `FAIL-DEEP-TAG-CONSUMPTION` | asset evidence 能看到 analysis_slice_id 与 segment 级选择理由 |

## Repair Playbook

1. 先判断失败在输入、模块、素材证据、主时钟、计划、HyperFrames authoring、preview 还是 render。
2. 任何“画面不贴文案”的问题，先看 `asset_evidence.json` 和 `f2_composition_plan.json`，不要直接改 HTML。
3. 任何“字幕不贴声音”的问题，先看 `dialogue_alignment.json`，不要只移动 CSS 或 caption layer。
4. 任何“转场/大字报不好看”的问题，先检查触发 cue、参考节奏和安全区，再调整 motion preset。
5. HyperFrames lint/validate 报错时，先修 DOM/timing/media 引用；不要绕过 CLI gate。
6. final render 失败时，先保留 preview/project/report，明确报告当前完成层级。
7. F2 普通任务不得把 `project_validated` 当最终交付；除非用户明确 no-render、plan/audit/evidence-only，或 render 依赖阻断，否则必须继续到 `N8`。
8. F2 普通任务默认 16:9；竖屏素材、竖屏参考片或短视频语境不能自动改写比例，除非用户/项目规格明确要求。
9. 成片画面里不要默认加工具/流程水印；`F2`、`HyperFrames`、文案编号、参考边界说明只进报告或工程元数据，不进 final 画面。
10. final 成片的台词字幕必须严格跟随音频；`manual_script_audio_duration` 只能作为草稿/conditional，不能作为严格同步 pass。
11. final 路线如果包含台词字幕，必须有 `dialogue_sync_validation.json`；validator fail 代表 C3/C7 不可 pass。
12. 新增 F2 规则时优先改 `SKILL.md`；只有执行经验和可复用修复手法写本文件。
13. 社媒广告型 F2 不要把“结构清楚”误做成“会议汇报”：优先让真实视频/工具实录/影像结果占据背景，PPT-like 卡片只做短促强调。
14. 大字报是编辑层，不是字幕层；如果它能和主字幕逐字互换，就应重写为更短的钩子、结果或 CTA。
15. 多 PiP 要先定网格和边距，再定内容；宁可少窗清楚，也不要随机散落造成廉价感。
16. 背景层遇到 render/inspect 超时时，优先生成短视频代理片段、降低码率或减少同屏视频数量；只有单段仍不适合视频时，才把该段标为 `image_background_fallback`。
17. 批量社媒广告视频不要用少数背景素材循环铺满；优先从 `影像内容/aigc_content` 中按 cue 语义组合拼接，工具界面和操作展示只在强工具语义段或证据需要时进入背景。
18. 批量社媒广告视频的 PiP 不要用少数图片循环铺满；优先从 `图片说明.yaml` 读取 `role`、`semantic_tags`、`best_for`、`avoid_for` 和 `text_overlay`，把截图、角色图、场景图、风格图按 cue 分工，并记录选择理由。
19. 批量 F2 每条新成片规划前先读 `asset_usage_ledger.json`；没有 ledger 就先创建空账本，不要凭记忆判断“好像没用过”。
20. 同义文案批量任务不能只换素材顺序；至少换两个观众可感知的视觉轴，并把变化轴写进 `asset_diversity_audit.json`。
21. 素材不足时可以重复，但重复必须是显式 `forced_reuse`，并说明替代候选为什么不合适；不要把重复伪装成“最佳匹配”。

## Reusable Heuristics

- F2 的核心优势不是“用 HTML 复刻 F1”，而是把字幕、PiP、大字报、转场、BGM 和布局都放进可预览的 composition。
- 参考样片最有价值的是 rhythm map：开头钩子密度、切点速度、强调文字位置、视觉层级和转场动机。
- HyperFrames authoring 前必须有 storyboard；没有 plan 的 HTML 很容易变成不可审计的视觉拼贴。
- BGM 默认服务段落推进，旁白永远是主音轨；如果音频计划无法证明 ducking 或音量边界，就不混入 final。
- 对已有 final 的修复，如果没有 HyperFrames project 或源素材，F2 应优先给重建/审计建议，避免承诺无损局部修复。
- 社媒广告视频的背景应优先“活”：全屏视频或影像内容提供动势，大字报和 PiP 提供信息密度，底部台词字幕只负责和旁白同步。图片背景是逐段设计/技术兜底，不是默认执行路径。
- 当项目已有 `视频说明.yaml` 时，背景选段要从“素材路径轮换”升级为“segment 语义匹配”：用 `semantic_tags`、`visual_content`、`best_for` 与台词 cue 对齐，并在 `asset_evidence.json` 记录选择理由和重复惩罚结果。
- 当项目已有 `图片说明.yaml` 时，PiP 选图要从“文件名轮换”升级为“图片角色语义匹配”：平台/工具截图只在证明平台、收益、评论区、工具操作时出现；角色设定图对应人物/统一/跑偏；场景道具资产图对应场景/资产/世界观；reference still 对应风格/画面质感。
- 平台判重风险的核心不是文案字面重复，而是“首屏、背景段、PiP、节奏、版式”组合重复；F2 选材时要先保证语义贴合，再用 usage ledger 和 visual_signature 拉开组合距离。
- 长素材必须先被切成可观察的短分析窗口，才适合进入批量选材；整条长视频一个粗标签会把所有文案都吸到同一个高分片段。
