# Review Contract

## Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-01` | 是否有可观察证据、时间码、截图或明确描述 | `FAIL-SBS-EVIDENCE` | 回到 `N1-INTAKE` 补证 |
| `GATE-SBS-02` | 镜头边界是否能复查 | `FAIL-SBS-SHOT-MAP` | 回到 `N2-SHOT-MAP` |
| `GATE-SBS-03` | 分析是否覆盖任务相关 craft 维度 | `FAIL-SBS-OBSERVATION` | 回到 `N3-OBSERVE` |
| `GATE-SBS-04` | 临摹原则是否脱离具体表达 | `FAIL-SBS-IMITATION` | 回到 `N4-PRINCIPLE` |
| `GATE-SBS-05` | `全局风格解析.md` 是否完整包含叙事/类型承诺/视觉母题/年代质感/情绪曲线/路由/媒介/美学/节奏/审计/提示词候选，默认无污染且不直接改写 north star / style contract | `FAIL-SBS-STYLE-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-06` | `编剧风格解析.md` 是否完整包含潜台词层/情绪脉冲/声音叙事/副线编织，无摄影越权 | `FAIL-SBS-DIRECTING-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-07` | `摄影风格解析.md` 是否完整包含视点/焦深语义/光源叙事/运动/切点/长镜头结构，能转成 `分镜明细：` | `FAIL-SBS-CINE-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-08` | `设计风格解析.md` 是否完整包含角色色调材质/空间叙事/道具层级/世界观视觉语法，按角色/场景/道具拆分且遵守画面合同 | `FAIL-SBS-DESIGN-BRIDGE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-09` | `分镜脚本.md` 是否含 Numbers 示例 19 列、顺序一致、每镜一行、提示词编排合规 | `FAIL-SBS-STORYBOARD-SCRIPT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-10` | 是否存在版权表达复制、项目不适配或 AIGC 不可执行风险 | `FAIL-SBS-RIGHTS` | 回到 `N4-PRINCIPLE` 或阻断 |
| `GATE-SBS-11` | 输出是否含 `思考过程`、路径统一、阶段解析与分镜脚本可消费 | `FAIL-SBS-OUTPUT` | 回到 `N7-WRITE` |

## Reference Detail Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-METHOD-01` | 最小镜头记录是否包含 `shot_id`、时间码/推断标记、可观察事件、入口、出口和镜头功能 | `FAIL-SBS-METHOD-SHOT-RECORD` | 回到 `N2-SHOT-MAP` |
| `GATE-SBS-METHOD-02` | 分析是否覆盖任务相关的口播、导演、表演、摄影、构图、光色、剪辑、声音、类型母题和 AIGC 可行性 | `FAIL-SBS-METHOD-DIMENSION` | 回到 `N3-OBSERVE` |
| `GATE-SBS-METHOD-03` | 是否先写观察再写解释，无证据解释是否降级为 `inference` | `FAIL-SBS-METHOD-OBS-FIRST` | 回到 `N3-OBSERVE` |
| `GATE-SBS-METHOD-04` | 教程/拆解/经验视频是否先抽口播论点，再用画面例证校验 | `FAIL-SBS-METHOD-SPOKEN-CLAIM` | 回到 `N3-OBSERVE` |
| `GATE-SBS-METHOD-05` | 长镜头是否只拆 phase、不伪造剪辑点；快切是否先看注意力接力和声音接口 | `FAIL-SBS-METHOD-RHYTHM` | 回到 `N2-SHOT-MAP` 或 `N3-OBSERVE` |
| `GATE-SBS-METHOD-06` | 技法是否从镜头功能推出，而不是从技法名倒推意义 | `FAIL-SBS-METHOD-FUNCTION` | 回到 `N3-OBSERVE` |
| `GATE-SBS-METHOD-07` | 分析判断是否由 LLM 基于证据完成，脚本仅做统计或格式辅助 | `FAIL-SBS-METHOD-LLM-FIRST` | 回到 `N3-OBSERVE` |
| `GATE-SBS-RIGHTS-01` | 每条结论是否标注 `confirmed`、`partial`、`inferred` 或 `insufficient` 证据等级 | `FAIL-RIGHTS-EVIDENCE-GRADE` | 回到 `N1-INTAKE` |
| `GATE-SBS-RIGHTS-02` | `insufficient` 状态下是否停止逐镜强结论并要求补视频/截图/时间码 | `FAIL-RIGHTS-INSUFFICIENT` | 回到 `N1-INTAKE` |
| `GATE-SBS-RIGHTS-03` | 临摹建议是否抽象为 craft principle，而非复制台词、角色、剧情、构图、镜头数量或剪辑顺序 | `FAIL-RIGHTS-COPY` | 回到 `N4-PRINCIPLE` |
| `GATE-SBS-RIGHTS-04` | 替换角色、空间、道具和剧情后，原则是否仍能服务目标项目 | `FAIL-RIGHTS-PROJECT-FIT` | 回到 `N4-PRINCIPLE` |
| `GATE-SBS-RIGHTS-05` | 不可学、证据不足、项目不适配和 AIGC 不可执行项是否进入 forbidden-copy / risk ledger | `FAIL-RIGHTS-LEDGER` | 回到 `N4-PRINCIPLE` |
| `GATE-SBS-ADAPT-01` | 桥接输出是否只作为 side context，不改写 `north_star.yaml`、`style_contract.json` 或 2/3/5 阶段 canonical 文件 | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-ADAPT-02` | 输出路径和文件名是否统一为 `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/` 与五个 canonical 解析文件 | `FAIL-SBS-ADAPT-PATH` | 回到 `N7-WRITE` |
| `GATE-SBS-ADAPT-03` | 旧文件名是否只作为 legacy mirror，不冒充主输出合同 | `FAIL-SBS-ADAPT-LEGACY-NAME` | 回到 `N7-WRITE` |
| `GATE-SBS-ADAPT-04` | 全局风格包是否只给叙事/类型/母题/媒介/节奏/去污染/提示词候选，不导入下游对象细节 | `FAIL-SBS-ADAPT-GLOBAL-PACKET` | 回到 `N5-BRIDGE` |
| `GATE-SBS-ADAPT-05` | 编剧包是否只给戏剧问题、观众位置、表演任务、调度、潜台词、声音叙事和可拍承托，无摄影越权 | `FAIL-SBS-ADAPT-SCREEN-PACKET` | 回到 `N5-BRIDGE` |
| `GATE-SBS-ADAPT-06` | 摄影包是否给 `visual_unit`、`beat_map`、`camera_grammar_plan` 和 payload，且不改写编导正文 | `FAIL-SBS-ADAPT-CINE-PACKET` | 回到 `N5-BRIDGE` |
| `GATE-SBS-ADAPT-07` | 设计包是否按角色/场景/道具拆分可迁移资产原则，并保留各自画面合同 | `FAIL-SBS-ADAPT-DESIGN-PACKET` | 回到 `N5-BRIDGE` |
| `GATE-SBS-ADAPT-08` | 分镜脚本是否严格继承 Numbers 示例 19 列和内容编排，而不是复制示例表达 | `FAIL-SBS-ADAPT-STORYBOARD-PACKET` | 回到 `N5-BRIDGE` |
| `GATE-SBS-ADAPT-09` | `imitation_unit` 是否能回指 source shots、迁移原则、项目适配、阶段桥接、禁止照搬和风险检查 | `FAIL-SBS-ADAPT-FUSION-SHAPE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-01` | `全局风格解析.md` 是否包含叙事与世界约束，且信息不足时标记推导补位 | `FAIL-GLOBAL-NARRATIVE-WEAK` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-02` | 类型叙事承诺是否说明核心契约、高光类型和承诺兑现节奏 | `FAIL-GLOBAL-GENRE-PROMISE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-03` | 视觉母题是否提炼为可迁移语法，而不是复制参考片具体符号 | `FAIL-GLOBAL-VISUAL-MOTIF` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-04` | 年代质感是否说明信号来源、密度、现代干扰和时间感构建 | `FAIL-GLOBAL-TEMPORAL-TEXTURE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-05` | 情绪曲线是否给出结构、幕锚点、高点类型和余震设计 | `FAIL-GLOBAL-EMOTION-CURVE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-06` | 路由决议是否在 `R1/R2/R3/R4` 中单选并给证据 | `FAIL-GLOBAL-ROUTE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-07` | 媒介技术栈和美学范式是否服务叙事，且不空泛 | `FAIL-GLOBAL-MEDIUM` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-07A` | 美学范式是否明确流派、气质和叙事服务理由 | `FAIL-GLOBAL-PARADIGM` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-08` | 叙事节奏锚定是否给慢/中/快判断依据和拍摄段落执行字窗 | `FAIL-GLOBAL-PACING` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-09` | 去污染审计是否清除颜色、材质、构图、摄影越权和下游对象细节；`R4` 是否声明 exact | `FAIL-GLOBAL-POLLUTION` | 回到 `N5-BRIDGE` |
| `GATE-SBS-GLOBAL-10` | 全局风格提示词候选是否 200 字以内、纯中文、无污染，或在 `R4` 明确保真原因 | `FAIL-GLOBAL-PROMPT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-01` | 编剧包是否建立戏剧问题、观众位置、角色压力和状态差 | `FAIL-SCREEN-DRAMATIC-Q` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-01A` | 观众位置是否说明知道、误解、等待、担心或延迟满足的内容 | `FAIL-SCREEN-AUDIENCE-POS` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-01B` | 角色压力是否包含目标、阻碍、隐藏信息、外显策略和关系压力 | `FAIL-SCREEN-CHAR-PRESSURE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-01C` | 场景状态差是否说明关系、信息权力或局势如何改变 | `FAIL-SCREEN-SCENE-DELTA` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-02` | 表演任务和场面调度是否可执行，并以角色身体、空间权力和障碍物承托戏剧 | `FAIL-SCREEN-PERF-TASK` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-02A` | 空间调度是否说明站坐、高低、远近、入口、障碍物和权力位置 | `FAIL-SCREEN-BLOCKING` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-03` | 对白策略、潜台词层和情绪脉冲是否可拍、可听、可表演 | `FAIL-SCREEN-SUBTEXT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-03A` | 对白策略是否说明密度、沉默、反问、威胁、信息释放或潜台词节奏 | `FAIL-SCREEN-DIALOGUE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-03B` | 情绪脉冲是否说明压抑、爆发、余震或过渡的场内节奏 | `FAIL-SCREEN-EMOTION-PULSE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-04` | controlled enrichment、次要情节和声音叙事是否只做承托，不新增剧情事实 | `FAIL-SCREEN-ENRICHMENT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-04A` | 次要情节是否说明对主线的压力输送、伏笔埋收和收束方式 | `FAIL-SCREEN-SUBPLOT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-04B` | 声音叙事是否说明音乐主题、环境音、静默、提前/滞后和声画对位 | `FAIL-SCREEN-SOUND` | 回到 `N5-BRIDGE` |
| `GATE-SBS-SCREEN-05` | 编剧包是否明确禁用机位、景别、焦段、运镜、分镜编号和具体台词复制 | `FAIL-SCREEN-DO-NOT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-01` | 摄影包是否定义观看任务、换镜理由和节奏画像，而非参数堆叠 | `FAIL-CINE-VISUAL-UNIT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-01A` | `beat_map_seed` 是否说明注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由 | `FAIL-CINE-BEAT-MAP` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-01B` | `rhythm_profile_seed` 是否给出收敛、展开、强化或断裂停顿的节奏建议 | `FAIL-CINE-RHYTHM` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-02` | 连续性、视点、焦深和光源语义是否能服务叙事与注意力交接 | `FAIL-CINE-CONTINUITY` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-02A` | 视点归属、切换逻辑和主客观边界是否清楚 | `FAIL-CINE-POV` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-02B` | 焦深语义是否说明前景/后景/清晰/虚化和拉焦触发的叙事功能 | `FAIL-CINE-DOF-SEMANTIC` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-02C` | 光源语义是否说明方向、自然/人工、冷暖和可见光源的叙事含义 | `FAIL-CINE-LIGHT-SEMANTIC` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-03` | 切点、运动类型、长镜头 phase 和画幅语法是否从参考证据抽象，而非照抄镜头顺序 | `FAIL-CINE-CUT-GRAMMAR` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-03A` | 运动类型系统是否说明类型清单、语义、切换逻辑、手持使用和速度节奏 | `FAIL-CINE-MOVE-TYPE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-03B` | 长镜头结构是否说明阈值、phase、机位运动层级、空间揭示和情绪功能 | `FAIL-CINE-LONG-TAKE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-03C` | 画幅和构图比例是否说明叙事功能、比例变化和下游约束 | `FAIL-CINE-FORMAT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-04` | `camera_grammar_plan_seed`、`functional_projection_payload` 和 `shot_detail_style_seed` 是否能被 `4-摄影` 消费 | `FAIL-CINE-PAYLOAD` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-04A` | 摄影语法计划是否给出景别、视角、景深、焦点、镜头类型、构图、光影和运镜迁移策略 | `FAIL-CINE-GRAMMAR-PLAN` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-04B` | `shot_detail_style_seed` 是否能转成自然中文 `分镜明细：` 写法参考 | `FAIL-CINE-SHOT-DETAIL` | 回到 `N5-BRIDGE` |
| `GATE-SBS-CINE-05` | 摄影包是否避免改写 `2-编导` 正文、固定参考片镜头数量或导入不可执行空泛词 | `FAIL-CINE-DO-NOT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-01` | 角色、场景、道具三类解析是否分区完整且对齐对应设计 leaf | `FAIL-DESIGN-ROLE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-01A` | 场景解析是否提供空镜空间秩序、环境压力、装置关系和无人画面约束 | `FAIL-DESIGN-SCENE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-01B` | 道具解析是否提供完整主体、功能压力、细节层级和 45 度近摄约束 | `FAIL-DESIGN-PROP` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-02` | 角色色调材质、空间叙事、道具功能层级和世界观视觉语法是否可迁移 | `FAIL-DESIGN-WORLD` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-02A` | 角色色调与材质语法是否说明身份色彩系统、材质词汇和磨损纹理叙事 | `FAIL-DESIGN-CHAR-COLOR` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-02B` | 空间叙事语法是否说明环境权力、残留物件、空镜和地理文化信号 | `FAIL-DESIGN-SPACE` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-02C` | 道具功能层级是否区分叙事核心、氛围、转场、象征和细节层级 | `FAIL-DESIGN-PROP-HIERARCHY` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-03` | 视觉转译是否把参考片具体美术表达转成目标项目自有设定 | `FAIL-DESIGN-TRANSLATION` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-04` | 角色全身试装、场景空镜、道具 45 度近摄三类画面合同是否没有混淆 | `FAIL-DESIGN-DO-NOT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-DESIGN-05` | 设计包是否没有直接生成正式提示词终稿或复制人物脸、纹样、构图、纹章、文字 | `FAIL-DESIGN-DO-NOT` | 回到 `N5-BRIDGE` |
| `GATE-SBS-STORY-01` | `分镜脚本.md` 是否使用 Numbers 示例 19 列和固定顺序 | `FAIL-STORYBOARD-19-COLUMNS` | 回到 `N5-BRIDGE` |
| `GATE-SBS-STORY-02` | 每行是否对应一个镜头，未用剧情段落冒充镜头 | `FAIL-STORYBOARD-ROW-PER-SHOT` | 回到 `N2-SHOT-MAP` 或 `N5-BRIDGE` |
| `GATE-SBS-STORY-03` | `镜号` 是否连续，正式四段式 ID 只放参考或说明，不替代表头 | `FAIL-STORYBOARD-ID` | 回到 `N5-BRIDGE` |
| `GATE-SBS-STORY-04` | 角色图、参考列是否不臆造素材路径；无素材时留空 | `FAIL-STORYBOARD-ASSET-PATH` | 回到 `N5-BRIDGE` |
| `GATE-SBS-STORY-05` | 分镜提示词和视频运动提示词是否按功能块组织，并以时长收束 | `FAIL-STORYBOARD-PROMPT-BLOCK` | 回到 `N5-BRIDGE` |
| `GATE-SBS-STORY-06` | 是否只学习示例字段组织和信息密度，不复制示例角色、剧情、台词、场景或视觉表达 | `FAIL-STORYBOARD-EXAMPLE-COPY` | 回到 `N4-PRINCIPLE` |

## Verdict

- `pass`: 所有 gate 通过，可作为 AIGC 阶段附加上下文。
- `needs_rework`: 有局部字段、证据或桥接问题，必须直接修复后复审。
- `blocked`: 素材不可见、版权边界无法处理、或用户要求具体复制。
