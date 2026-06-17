# Drafting Type Map

本文件辅助 `story-drafting` 判定任务模式、题材路由、跨类型融合和平台适配；主路由仍以 `SKILL.md` 的 Type Routing Matrix 为准。

---

## Package Index

本索引用于把题材信号解析到真实可加载路径。命中题材或类型化场面时，执行报告必须生成 `type_package_manifest`，列出 `matched_signal`、`loaded_paths`、`owner_node`、`applied_scene_function`、`platform_profile` 和 `skipped_reason`。

### 武侠与动作

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `wuxia_core` | `types/网文/武侠/武侠.md` | 武侠、江湖、门派、侠义、港式武侠、高武武侠语境 | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` |
| `wuxia_combat_design` | `types/网文/武侠/武侠之战斗设计.md` | 武戏、打斗、决斗、围杀、追逐、兵器交锋、动作细节不足 | `N5-CREATIVE-DRAFT` |
| `wuxia_blade_qi_flow` | `types/网文/武侠/白刃剑气流.md` | 白刃剑气流、剑气、刀气、剑风、刀剑风压、内力余波、港式武侠破坏感、90 年代香港新浪潮武侠、徐克/程小东式高飞剑侠、旧港片实物爆点、刀剑气质区分 | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` |
| `wuxia_jianghu_order` | `types/网文/武侠/武侠之江湖秩序.md` | 江湖规矩、门派秩序、武林声望、恩怨规约 | `N5-CREATIVE-DRAFT` |
| `wuxia_relationship` | `types/网文/武侠/武侠之情感关系.md` | 武侠语境下的师徒、同门、侠侣、恩义与背叛 | `N5-CREATIVE-DRAFT` |
| `wuxia_history_thread` | `types/网文/武侠/武侠之历史串联.md` | 江湖史、前代恩怨、旧案、门派源流 | `N5-CREATIVE-DRAFT` |

### 言情与女性向

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `romance_tropes` | `types/网文/狗血言情/romance-tropes.md` | 言情、狗血、误会、替身、破镜、甜虐关系、追妻火葬场、先婚后爱 | `N5-CREATIVE-DRAFT` |
| `romance_emotional_tension` | `types/网文/狗血言情/emotional-tension.md` | 关系拉扯、欲望/回避、情绪张力不足、暧昧推拉、吃醋 | `N5-CREATIVE-DRAFT` |
| `romance_character_archetypes` | `types/网文/狗血言情/character-archetypes.md` | 霸总、白月光、替身、绿茶、忠犬、疯批人设 | `N5-CREATIVE-DRAFT` |
| `romance_plot_templates` | `types/网文/狗血言情/plot-templates.md` | 追妻、带球跑、契约婚姻、掉马甲 | `N5-CREATIVE-DRAFT` |
| `romance_pacing` | `types/网文/狗血言情/romance-pacing.md` | 甜虐比例、情绪曲线、章节卡点 | `N5-CREATIVE-DRAFT` |
| `romance_sweet_moments` | `types/网文/狗血言情/sweet-moments.md` | 甜宠场景、心动瞬间、暧昧升温 | `N5-CREATIVE-DRAFT` |
| `romance_torture_points` | `types/网文/狗血言情/torture-points.md` | 虐点设计、误会升级、情感爆发、复仇爽感 | `N5-CREATIVE-DRAFT` |
| `ancient_romance` | `types/网文/古言剧/historical-setting.md` | 古言、宫廷、宅院、礼制言情 | `N5-CREATIVE-DRAFT` |
| `ancient_dialogue` | `types/网文/古言剧/ancient-dialogue.md` | 古言、宫廷、礼制、古代对白 | `N5-CREATIVE-DRAFT` |
| `palace_intrigue` | `types/网文/古言剧/palace-intrigue.md` | 宫斗、宅斗、后宫、礼制博弈 | `N5-CREATIVE-DRAFT` |
| `qingchun_tianchong` | `types/网文/青春甜宠/青春甜宠.md` | 校园、青梅竹马、双向暗恋、甜宠日常 | `N5-CREATIVE-DRAFT` |
| `haomen_zongcai` | `types/网文/豪门总裁/豪门总裁.md` | 豪门、总裁、契约、先婚后爱、家族恩怨 | `N5-CREATIVE-DRAFT` |
| `huanxiang_yanqing` | `types/网文/幻想言情/幻想言情.md` | 仙侠言情、奇幻言情、跨种族恋爱 | `N5-CREATIVE-DRAFT` |
| `minguo_yanqing` | `types/网文/民国言情/民国言情.md` | 民国、乱世、军阀、世家爱恋 | `N5-CREATIVE-DRAFT` |
| `zhichang_hunlian` | `types/网文/职场婚恋/职场婚恋.md` | 职场、婚恋、办公室、精英爱情 | `N5-CREATIVE-DRAFT` |
| `nupin_xuanyi` | `types/网文/女频悬疑/女频悬疑.md` | 女频+悬疑、女性视角探案、惊悚言情 | `N5-CREATIVE-DRAFT` |
| `tishen_wen` | `types/网文/替身文/替身文.md` | 替身、白月光替身、容貌相似、身份替代 | `N5-CREATIVE-DRAFT` |
| `gongdou_zhai_dou` | `types/网文/宫斗宅斗/宫斗宅斗.md` | 宫斗、宅斗、后院权谋、妻妾较量 | `N5-CREATIVE-DRAFT` |

### 玄幻与修炼

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `xianxia_core` | `types/网文/修仙/修仙.md` | 修仙、宗门、境界、灵气、渡劫、长生、仙侠 | `N5-CREATIVE-DRAFT` |
| `xuanhuan_power_systems` | `types/网文/玄幻剧/power-systems.md` | 玄幻、修炼体系、能力规则、资源代价 | `N5-CREATIVE-DRAFT` |
| `xuanhuan_cool_points` | `types/网文/玄幻剧/xuanhuan-cool-points.md` | 玄幻爽点、能力兑现、升级收益 | `N5-CREATIVE-DRAFT` |
| `xuanhuan_plot_patterns` | `types/网文/玄幻剧/xuanhuan-plot-patterns.md` | 玄幻经典套路、打脸升级、秘境夺宝 | `N5-CREATIVE-DRAFT` |
| `xuanhuan_cultivation_levels` | `types/网文/玄幻剧/cultivation-levels.md` | 修炼境界、等级体系、突破机制 | `N5-CREATIVE-DRAFT` |
| `gaowu_core` | `types/网文/高武/高武.md` | 高武、武道等级、气血、现代武道训练 | `N5-CREATIVE-DRAFT` |
| `xitong_liu` | `types/网文/系统流/系统流.md` | 系统、面板、任务、签到、奖励机制 | `N5-CREATIVE-DRAFT` |
| `western_fantasy_core` | `types/网文/西幻/西幻.md` | 西幻、魔法、神祇、骑士、异族、龙与地下城 | `N5-CREATIVE-DRAFT` |
| `sci_fi_core` | `types/网文/科幻/科幻.md` | 科幻、未来技术、星际、科技伦理 | `N5-CREATIVE-DRAFT` |
| `dushi_yineng` | `types/网文/都市异能/都市异能.md` | 都市异能、现代超能力、隐藏身份 | `N5-CREATIVE-DRAFT` |

### 悬疑与恐怖

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `horror_cthulhu` | `types/网文/克苏鲁/克苏鲁.md` | 克苏鲁、不可名状、认知污染、未知崇拜、宇宙恐怖 | `N5-CREATIVE-DRAFT` |
| `horror_suspense_supernatural` | `types/网文/悬疑灵异/悬疑灵异.md` | 灵异、惊悚、恐怖、阴宅、怪异事件、捉鬼 | `N5-CREATIVE-DRAFT` |
| `horror_rule_talk` | `types/网文/规则怪谈/规则怪谈.md` | 规则怪谈、禁忌、逃生规则、异常空间、怪谈副本 | `N5-CREATIVE-DRAFT` |
| `mystery_core` | `types/网文/侦探剧/core-elements.md` | 侦探、推理、案件、本格、社会派、刑侦 | `N5-CREATIVE-DRAFT` |
| `mystery_clue_design` | `types/网文/侦探剧/clue-design.md` | 侦探、案件、线索、公平误导、证据复盘 | `N5-CREATIVE-DRAFT` |
| `mystery_trick_design` | `types/网文/侦探剧/trick-design.md` | 诡计、密室、作案手法、揭晓设计 | `N5-CREATIVE-DRAFT` |
| `mystery_detective_design` | `types/网文/侦探剧/detective-design.md` | 侦探人设、搭档关系、探案风格 | `N5-CREATIVE-DRAFT` |
| `mystery_revelation` | `types/网文/侦探剧/revelation-design.md` | 真相揭示、推理秀、对质场景 | `N5-CREATIVE-DRAFT` |
| `mystery_structure` | `types/网文/侦探剧/structure-pacing.md` | 探案节奏、章节悬念、案情推进 | `N5-CREATIVE-DRAFT` |
| `mystery_suspect` | `types/网文/侦探剧/suspect-management.md` | 嫌疑人管理、红鲱鱼、误导设计 | `N5-CREATIVE-DRAFT` |
| `xuanyi_lingyi` | `types/网文/悬疑灵异/悬疑灵异.md` | 灵异、惊悚、恐怖、阴宅、怪异事件 | `N5-CREATIVE-DRAFT` |
| `xuanyi_naodong` | `types/网文/悬疑脑洞/悬疑脑洞.md` | 悬疑+脑洞、设定反转、认知颠覆 | `N5-CREATIVE-DRAFT` |

### 历史与年代

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `history_ancient` | `types/网文/历史古代/历史古代.md` | 历史、古代、朝代、权谋、争霸、科举 | `N5-CREATIVE-DRAFT` |
| `history_naodong` | `types/网文/历史脑洞/历史脑洞.md` | 历史脑洞、穿越改变、规则历史 | `N5-CREATIVE-DRAFT` |
| `kangzhan_diezhan` | `types/网文/抗战谍战/抗战谍战.md` | 抗战、谍战、卧底、情报战、抗日 | `N5-CREATIVE-DRAFT` |
| `niandai` | `types/网文/年代/年代.md` | 年代文、六七八十年代、知青、改革开放 | `N5-CREATIVE-DRAFT` |
| `minguo_yanqing` | `types/网文/民国言情/民国言情.md` | 民国、乱世、军阀、世家爱恋 | `N5-CREATIVE-DRAFT` |

### 现实与都市

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `realism_reality_anchoring` | `types/网文/现实题材/reality-anchoring.md` | 现实、职场、家庭、制度、社会压力 | `N5-CREATIVE-DRAFT` |
| `realism_character_depth` | `types/网文/现实题材/character-depth.md` | 人物深度、心理刻画、成长弧光 | `N5-CREATIVE-DRAFT` |
| `realism_plot_logic` | `types/网文/现实题材/plot-logic.md` | 剧情逻辑、因果关系、现实约束 | `N5-CREATIVE-DRAFT` |
| `realism_social_issues` | `types/网文/现实题材/social-issues.md` | 社会议题、阶层、价值观冲突 | `N5-CREATIVE-DRAFT` |
| `realism_dialogue` | `types/网文/现实题材/dialogue-authenticity.md` | 现实题材对白、身份语言、社会关系声口 | `N5-CREATIVE-DRAFT` |
| `dushi_richang` | `types/网文/都市日常/都市日常.md` | 都市日常、生活流、温馨治愈 | `N5-CREATIVE-DRAFT` |
| `dushi_naodong` | `types/网文/都市脑洞/都市脑洞.md` | 都市+脑洞、日常反转、设定新奇 | `N5-CREATIVE-DRAFT` |
| `xianyan_naodong` | `types/网文/现言脑洞/现言脑洞.md` | 现言+脑洞、现代言情设定创新 | `N5-CREATIVE-DRAFT` |

### 生存与末世

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `apocalypse_core` | `types/网文/末世/末世.md` | 末世、生存、灾难、资源危机、丧尸、废土 | `N5-CREATIVE-DRAFT` |
| `infinite_flow_core` | `types/网文/无限流/无限流.md` | 无限流、副本、规则空间、任务生存、轮回 | `N5-CREATIVE-DRAFT` |

### 细分/特殊题材

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `zhongtian` | `types/网文/种田/种田.md` | 种田、经营、田园、养殖、发家致富 | `N5-CREATIVE-DRAFT` |
| `zhibo_wen` | `types/网文/直播文/直播文.md` | 直播、网红、弹幕、主播、打赏 | `N5-CREATIVE-DRAFT` |
| `dianjing` | `types/网文/电竞/电竞.md` | 电竞、游戏竞技、战队、职业选手 | `N5-CREATIVE-DRAFT` |
| `youxi_tiyu` | `types/网文/游戏体育/游戏体育.md` | 游戏、体育竞技、网游、运动 | `N5-CREATIVE-DRAFT` |
| `duozi_duofu` | `types/网文/多子多福/多子多福.md` | 多子多福、家族兴旺、子女养成 | `N5-CREATIVE-DRAFT` |
| `heian_ticai` | `types/网文/黑暗题材/黑暗题材.md` | 黑暗、复仇、反英雄、残酷现实 | `N5-CREATIVE-DRAFT` |
| `zhihu_short` | `types/网文/知乎短篇/genre-templates.md` | 知乎短篇、盐选、短篇爽文、高赞故事 | `N5-CREATIVE-DRAFT` |

### 全局上下文

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `web_novel_context` | `types/网文/README.md` | `north_star.genre_contract`、章级 planning 或用户请求命中网文题材语境 | `N1-INTAKE` / `N5-CREATIVE-DRAFT` |

---

## Genre Directory Registry

当具体文件级 package 未覆盖目标题材，但 `north_star.genre_contract`、planning 或用户请求命中下列目录时，必须加载对应目录的核心文件或 README；目录内多文件只按当前场景功能选择 1-3 个真实文件，不全量灌入。

| genre_signal | directory | deterministic_entry |
| --- | --- | --- |
| 侦探剧、推理、案件 | `types/网文/侦探剧/` | `core-elements.md`；线索命中时加 `clue-design.md`；诡计命中加 `trick-design.md` |
| 修仙、仙侠 | `types/网文/修仙/` | `修仙.md` |
| 克苏鲁、不可名状、宇宙恐怖 | `types/网文/克苏鲁/` | `克苏鲁.md` |
| 历史古代、权谋争霸、朝代 | `types/网文/历史古代/` | `历史古代.md` |
| 历史脑洞、穿越改变、规则历史 | `types/网文/历史脑洞/` | `历史脑洞.md` |
| 古言剧、古代言情、宫廷 | `types/网文/古言剧/` | `historical-setting.md`；对白命中时加 `ancient-dialogue.md`；权谋命中加 `palace-intrigue.md` |
| 宫斗宅斗、后院权谋 | `types/网文/宫斗宅斗/` | `宫斗宅斗.md` |
| 幻想言情、仙侠言情 | `types/网文/幻想言情/` | `幻想言情.md` |
| 悬疑灵异、惊悚捉鬼 | `types/网文/悬疑灵异/` | `悬疑灵异.md` |
| 悬疑脑洞、认知反转 | `types/网文/悬疑脑洞/` | `悬疑脑洞.md` |
| 抗战谍战、卧底情报 | `types/网文/抗战谍战/` | `抗战谍战.md` |
| 无限流、副本生存、轮回 | `types/网文/无限流/` | `无限流.md` |
| 替身文、白月光替身 | `types/网文/替身文/` | `替身文.md` |
| 末世、生存灾难、丧尸废土 | `types/网文/末世/` | `末世.md` |
| 武侠、江湖 | `types/网文/武侠/` | `武侠.md`；武戏命中时加 `武侠之战斗设计.md`；白刃命中加 `白刃剑气流.md` |
| 民国言情、乱世爱恋 | `types/网文/民国言情/` | `民国言情.md` |
| 游戏体育、网游竞技 | `types/网文/游戏体育/` | `游戏体育.md` |
| 狗血言情、甜虐关系 | `types/网文/狗血言情/` | `romance-tropes.md`；情绪拉扯命中时加 `emotional-tension.md` |
| 玄幻剧、修炼体系 | `types/网文/玄幻剧/` | `power-systems.md`；爽点命中加 `xuanhuan-cool-points.md` |
| 现实题材、社会写实 | `types/网文/现实题材/` | `reality-anchoring.md` |
| 现言脑洞 | `types/网文/现言脑洞/` | `现言脑洞.md` |
| 电竞、职业选手 | `types/网文/电竞/` | `电竞.md` |
| 直播文 | `types/网文/直播文/` | `直播文.md` |
| 知乎短篇、盐选 | `types/网文/知乎短篇/` | `genre-templates.md`；钩子命中时加 `hook-techniques.md` |
| 种田、经营田园 | `types/网文/种田/` | `种田.md` |
| 科幻、星际科技 | `types/网文/科幻/` | `科幻.md` |
| 系统流、面板任务 | `types/网文/系统流/` | `系统流.md` |
| 职场婚恋 | `types/网文/职场婚恋/` | `职场婚恋.md` |
| 西幻、魔法异族 | `types/网文/西幻/` | `西幻.md` |
| 规则怪谈、禁忌逃生 | `types/网文/规则怪谈/` | `规则怪谈.md` |
| 豪门总裁 | `types/网文/豪门总裁/` | `豪门总裁.md` |
| 都市异能 | `types/网文/都市异能/` | `都市异能.md` |
| 都市日常 | `types/网文/都市日常/` | `都市日常.md` |
| 都市脑洞 | `types/网文/都市脑洞/` | `都市脑洞.md` |
| 青春甜宠、校园 | `types/网文/青春甜宠/` | `青春甜宠.md` |
| 高武、武道末世 | `types/网文/高武/` | `高武.md` |
| 黑暗题材、复仇反英雄 | `types/网文/黑暗题材/` | `黑暗题材.md` |
| 多子多福、家族养成 | `types/网文/多子多福/` | `多子多福.md` |
| 年代、知青改革 | `types/网文/年代/` | `年代.md` |

---

## Cross-Genre Fusion Routing

当项目 `north_star.type_stack` 存在多个题材信号，或用户明确要求跨类型融合时，按以下矩阵加载：

### 融合配方矩阵

| 主类型 | 融合类型 | 融合加载路径 | 融合要点 |
| --- | --- | --- | --- |
| 修仙 + 悬疑 | `xianxia_core` + `mystery_core` + `mystery_clue_design` | 修仙.md + core-elements.md + clue-design.md | 修炼规则即推理规则；突破线索化 |
| 修仙 + 言情 | `xianxia_core` + `romance_tropes` + `huanxiang_yanqing` | 修仙.md + romance-tropes.md + 幻想言情.md | 仙凡恋、道侣羁绊、修炼瓶颈与情感关联 |
| 武侠 + 历史 | `wuxia_core` + `history_ancient` + `wuxia_history_thread` | 武侠.md + 历史古代.md + 武侠之历史串联.md | 江湖在历史框架内；真实历史事件驱动 |
| 武侠 + 悬疑 | `wuxia_core` + `mystery_core` + `mystery_clue_design` | 武侠.md + core-elements.md + clue-design.md | 武功即作案工具；江湖恩怨即动机 |
| 历史 + 系统流 | `history_ancient` + `xitong_liu` + `history_naodong` | 历史古代.md + 系统流.md + 历史脑洞.md | 系统干预历史进程；历史人物应对系统 |
| 末世 + 修仙 | `apocalypse_core` + `xianxia_core` | 末世.md + 修仙.md | 末世灵气复苏；修仙即生存手段 |
| 末世 + 种田 | `apocalypse_core` + `zhongtian` | 末世.md + 种田.md | 末世基地建设；资源经营即生存 |
| 末世 + 系统流 | `apocalypse_core` + `xitong_liu` | 末世.md + 系统流.md | 末日系统；任务=生存挑战 |
| 无限流 + 悬疑 | `infinite_flow_core` + `mystery_core` + `mystery_clue_design` | 无限流.md + core-elements.md + clue-design.md | 副本即案件；规则破译即推理 |
| 无限流 + 恐怖 | `infinite_flow_core` + `horror_suspense_supernatural` + `horror_rule_talk` | 无限流.md + 悬疑灵异.md + 规则怪谈.md | 副本即恐怖空间；san值系统 |
| 无限流 + 科幻 | `infinite_flow_core` + `sci_fi_core` | 无限流.md + 科幻.md | 科幻副本；技术即规则 |
| 都市 + 异能 | `dushi_richang` + `dushi_yineng` | 都市日常.md + 都市异能.md | 日常隐藏异能；双重身份张力 |
| 都市 + 系统流 | `dushi_richang` + `xitong_liu` + `dushi_naodong` | 都市日常.md + 系统流.md + 都市脑洞.md | 都市日常被系统打破 |
| 电竞 + 系统流 | `dianjing` + `xitong_liu` | 电竞.md + 系统流.md | 游戏系统化为现实系统 |
| 直播 + 系统流 | `zhibo_wen` + `xitong_liu` | 直播文.md + 系统流.md | 直播+系统任务双线 |
| 直播 + 悬疑 | `zhibo_wen` + `mystery_core` + `mystery_suspect` | 直播文.md + core-elements.md + suspect-management.md | 直播探案；观众即陪审团 |
| 规则怪谈 + 无限流 | `horror_rule_talk` + `infinite_flow_core` | 规则怪谈.md + 无限流.md | 规则副本；破译即通关 |
| 规则怪谈 + 校园 | `horror_rule_talk` + `qingchun_tianchong` | 规则怪谈.md + 青春甜宠.md | 校园怪谈；青春+恐怖双线 |
| 言情 + 替身文 | `romance_tropes` + `tishen_wen` + `romance_torture_points` | romance-tropes.md + 替身文.md + torture-points.md | 替身梗×情感漩涡；白月光替换结构 |
| 言情 + 职场 | `romance_tropes` + `zhichang_hunlian` | romance-tropes.md + 职场婚恋.md | 职场爱情；职业身份×情感关系 |
| 言情 + 豪门 | `romance_tropes` + `haomen_zongcai` + `romance_sweet_moments` | romance-tropes.md + 豪门总裁.md + sweet-moments.md | 豪门背景下的甜虐关系 |
| 科幻 + 末世 | `sci_fi_core` + `apocalypse_core` | 科幻.md + 末世.md | 科技末世；技术灾难 |
| 科幻 + 无限流 | `sci_fi_core` + `infinite_flow_core` | 科幻.md + 无限流.md | 科幻世界副本；虚拟现实 |
| 西幻 + 种田 | `western_fantasy_core` + `zhongtian` | 西幻.md + 种田.md | 魔法领主经营；异世界开拓 |
| 西幻 + 言情 | `western_fantasy_core` + `romance_tropes` | 西幻.md + romance-tropes.md | 西幻背景言情；不同种族恋爱 |
| 黑暗题材 + 悬疑 | `heian_ticai` + `mystery_core` + `mystery_trick_design` | 黑暗题材.md + core-elements.md + trick-design.md | 暗黑推理；道德灰色地带 |
| 黑暗题材 + 末世 | `heian_ticai` + `apocalypse_core` | 黑暗题材.md + 末世.md | 人性黑暗在末世放大 |
| 高武 + 都市 | `gaowu_core` + `dushi_richang` + `dushi_naodong` | 高武.md + 都市日常.md + 都市脑洞.md | 现代武道；都市中的武者 |
| 高武 + 末世 | `gaowu_core` + `apocalypse_core` | 高武.md + 末世.md | 武道末世；气血对抗灾难 |
| 年代 + 种田 | `niandai` + `zhongtian` | 年代.md + 种田.md | 年代经营文；改革开放致富 |
| 克苏鲁 + 都市 | `horror_cthulhu` + `dushi_richang` | 克苏鲁.md + 都市日常.md | 都市中的不可名状；日常恐怖 |
| 克苏鲁 + 侦探 | `horror_cthulhu` + `mystery_core` | 克苏鲁.md + core-elements.md | 克系侦探；真相即是污染 |

### 融合加载优先级

1. 主类型核心文件 → 2. 融合类型核心文件 → 3. 共享场景功能文件 → 4. subtype 文件
2. 同一关键场面最多加载 1 个主题材核心包、1 个融合题材核心包、1 个场面功能包和 1 个 subtype 包
3. 当主类型和融合类型的某些规则冲突时（如修仙的"打脸升级"与悬疑的"信息渐进"），以场景当前主导功能为准

---

## Platform Profile Routing

当项目 `north_star` 或用户指定目标平台时，加载对应平台的读者期待和创作约束。

| platform | profile_package | key_expectations | forbidden_patterns |
| --- | --- | --- | --- |
| 番茄小说 | `platform_tomato` | 开头300字抓人、爽点密集（每3章至少1个小爽点）、节奏快、字数多（150万+）、标题党友好 | 慢热开局、大段设定说明、文艺腔开场、主角长期弱势 |
| 起点中文网 | `platform_qidian` | 设定硬核、逻辑自洽、读者耐心较好、精品化趋势、200-500万字 | 逻辑漏洞、战力崩坏、水文凑字、草率收尾 |
| 晋江文学城 | `platform_jinjiang` | 感情线优先、人设鲜明、文笔细腻、30-80万字、HE倾向 | 感情线模糊、配角抢戏、男主油腻、BE结局无预警 |
| 七猫/免费平台 | `platform_free_app` | 短平快、信息流标题、每章结尾钩子必须强、爽点频率极高 | 慢节奏、文艺风、长段落、信息密度低 |
| 知乎盐选 | `platform_zhihu` | 开篇300字内出核心冲突、全文8000-20000字、反转密集、第一人称优先 | 长篇铺垫、背景说明堆砌、节奏平缓 |
| 豆瓣阅读 | `platform_douban` | 文学性强、人物深度、社会议题、中短篇、严肃文学风格 | 商业化注水、套路化严重、人物扁平 |

### 平台加载规则

- 单平台：以对应 `platform_*` profile 为第一优先级滤镜，题材包为第二层
- 多平台：取交集约束（同时满足两个平台的底线要求）
- 平台与题材冲突时：先满足平台底线（如番茄的快节奏 > 历史古代的传统慢热写法）
- 未指定平台时：默认不加载平台 profile，仅以题材包为准

---

## Reader Psychology & Retention Routing

根据项目核心读者体验目标，加载对应的追读心理引导。

| retention_goal | trigger | loaded_context | prose_target |
| --- | --- | --- | --- |
| `hook_addiction` | 目标平台为免费阅读/番茄；用户要求"提高追读率" | 钩子设计原则、每章结尾悬念类型、预期违背节奏 | 每章3-5个信息缺口；结尾至少1个"必须看下一章"的理由 |
| `identity_projection` | 主角穿越/重生/系统获取；读者代入感要求高 | 身份认同锚点、渐进式权力获取、读者自我投射路径 | 主角困境共情；升级节奏符合读者预期；不过度拔高主角使之疏离 |
| `power_fantasy` | 男频爽文；升级打脸主线 | 权力增长曲线、碾压爽感的执行细节、围观群众的震惊描写 | 升级场景必须有可感知的对比变化；打脸必须有"说出去的话收不回来"的结构 |
| `emotional_catharsis` | 女频言情；虐文/甜文；情感主线 | 情绪积累→释放曲线、虐点甜点分布、读者情绪管理 | 虐不过三章必给甜；甜不过五章必埋伏笔；高潮必须有情绪出口 |
| `mystery_curiosity` | 悬疑/侦探/恐怖；读者好奇心驱动 | 信息缺口设计、线索释放节奏、好奇心-满足循环 | 每章给出1-2个新线索，回收0-1个旧线索；全局至少保持3个未解之谜 |
| `wish_fulfillment` | 种田/日常/治愈；读者寻求心理慰藉 | 渐进式正反馈、日常中的微小成就、舒适区设定 | 每章至少1个可感知的正面变化；冲突存在但不威胁核心舒适感 |
| `power_progression` | 修仙/玄幻/高武；读者为升级和成长付费 | 升级路径可视化、突破场景的仪式感、能力变现的即时性 | 每次升级必须有"肉眼可见"的能力变化；不能隔章不认得自己 |
| `relationship_drama` | 言情/狗血/宅斗；读者为关系拉扯付费 | 关系动态图、误会结构、和解/破裂的节奏 | 关系不能静止超过3章；每次互动必须有推进或反转 |

---

## AI Generation Guidance

面向 LLM 写作的专项约束，防止 AI 常见写作陷阱。

| ai_trap | detection_signal | fix_package | fix_rule |
| --- | --- | --- | --- |
| `tell_not_show` | 直接说明情绪/状态/关系，无具体行为/细节支撑 | — | 用行为、对白、场景细节替代抽象陈述 |
| `flattened_pacing` | 所有段落节奏一致，无快慢变化 | — | 武戏切短句、快节奏；文戏放慢、心理活动充分；每章至少1次节奏切换 |
| `adjective_horror` | 恐怖场景用"恐怖""阴森""诡异"等形容词堆砌 | `genre_scene_horror` | 用信息缺失、感官扭曲、规则违背制造恐惧，不用形容词喊恐怖 |
| `power_point_combat` | 打斗写成"先出XX，再出YY，然后ZZ"的技能流水账 | `genre_scene_action` | 写动作路径、空间关系、身体代价和材质响应 |
| `dialogue_as_exposition` | 对话变成信息灌输，角色说"你难道不知道XX吗？"来科普 | — | 对话服务角色关系和当前场景冲突；信息通过冲突中的缝隙漏出 |
| `emotion_lexicon` | 角色情绪全都用"开心/难过/愤怒/紧张"等词直接标注 | — | 用微动作、微表情、生理反应、行为选择表现情绪 |
| `smooth_protagonist` | 主角一路顺风，无实质挫折 | — | 每卷至少1次重大挫折；挫折必须改变主角接下来的行动策略 |
| `flat_antagonist` | 反派只有"坏"这一个属性，无动机、无背景、无智商 | — | 反派必须有可理解的动机和独立于主角存在的行动逻辑 |
| `paragraph_bloat` | 单段超过200字，读者视觉疲劳 | — | 控制段落长度：动作<80字、对白单句<30字、叙述<150字 |
| `info_dump_opening` | 开篇大量背景设定、世界观说明 | — | 第一章只给读者"必须知道"的信息；其余通过剧情渐次释放 |

### AI 写作质量自检表

每完成一章起草后，执行以下快速自检：

1. **可读性**：是否有超过200字的段落？是否有连续5段以上无对白？→ 有则拆分
2. **节奏感**：本章是否有至少一次节奏变化（快→慢或慢→快）？→ 无则调整
3. **画面感**：每个关键场景是否有至少2个感官细节（视觉+听觉/触觉/嗅觉）？→ 无则补充
4. **情绪值**：本章读者情绪是否有起伏（至少1次变化）？→ 无则增加冲突或惊喜
5. **钩子力**：本章结尾是否让读者产生"必须知道后面"的冲动？→ 无则重新设计结尾
6. **信息密度**：是否有超过300字的纯说明/设定段落？→ 有则拆入对话或场景
7. **角色辨识度**：每个重要角色是否有独特的说话方式或行为习惯？→ 检查对白声口差异化

---

## Default Package Rule

- 默认不加载题材包；只有题材、风格、读者预期或用户请求明确命中时才加载。
- 题材包只提供上下文提醒和风险过滤，不替代 `SKILL.md` 的 Type Routing Matrix、Thinking-Action Node Map、Output Contract 或 review gate。
- 类型化场面强化优先走根共享合同和 `references/genre-scene-drafting-contract.md`，不得由题材包直接生成正文。
- 命中具体 subtype 时，必须优先加载文件级 package；文件级 package 不存在时才回退目录核心文件，并在 `type_package_manifest.skipped_reason` 写明原因。
- `wuxia_blade_qi_flow` 只在白刃气流、剑气/刀气、刀剑风压、港式武侠破坏感、90 年代香港新浪潮武侠、徐克/程小东式高飞剑侠、旧港片实物爆点、刀剑气质区分或项目记忆明确要求时加载；普通动作戏只加载 `wuxia_combat_design` 或对应非武侠动作上下文。
- 跨类型融合加载时，必须生成 `fusion_manifest` 记录融合配方、主次类型和冲突裁决。

---

## Loading Flow

1. 先由 `SKILL.md#Type Routing Matrix` 判定 `chapter_draft / chapter_continue / chapter_rewrite / local_repair / dry_run`。
2. 再按 `north_star.genre_contract`、项目 `MEMORY.md`、章级 planning、用户请求、监制包和验收 finding 判定是否加载题材包或类型化场面合同。
3. 如有平台指定，叠加 `Platform Profile Routing`。
4. 如有跨类型融合信号，叠加 `Cross-Genre Fusion Routing`。
5. 如有读者留存目标，叠加 `Reader Psychology & Retention Routing`。
6. 生成 `type_package_manifest`：

   ```yaml
   type_package_manifest:
     matched_signal:
     selected_packages: []
     loaded_paths: []
     owner_node: "N2-SOURCE-LOCK | N5-CREATIVE-DRAFT"
     applied_scene_function:
     subtype:
     platform_profile:
     fusion_manifest:
       primary_genre:
       secondary_genre:
       conflict_resolution:
     reader_retention_goal:
     skipped_packages: []
     skipped_reason:
   ```

7. 最后回到 `N5-CREATIVE-DRAFT` 统一主创，不产生平行题材草稿。

---

## Mode Map

| mode | trigger | required_context | gate |
| --- | --- | --- | --- |
| `chapter_draft` | 目标章不存在，用户要求起草 | planning、north_star、对象卡、同卷前文、MEMORY/CONTEXT | 写出完整初稿 |
| `chapter_continue` | 目标章已存在，用户要求续写/补完 | 既有正文、续写边界、上游真源 | 保留已成立内容，补足缺口 |
| `chapter_rewrite` | 用户明确要求重写/覆盖 | 既有正文、重写授权、上游真源 | 不静默覆盖，保留必要事实 |
| `local_repair` | review 或用户指出局部问题 | finding、受影响段落、上游真源 | 只修问题及必要上下文 |
| `dry_run` | 只检查或装配上下文 | 目标章路径和上游真源 | 不写正文 |

---

## Genre Context Packages

- `types/网文/` 保留一组网文题材上下文包，供 `north_star.yaml.genre_contract`、项目 `MEMORY.md`、章级 planning 或用户请求命中时按题材选择性加载。
- 题材包只提供固定上下文、风格风险和常见结构提醒，不得替代 `SKILL.md` 的主创节点、Output Contract 或 review gate。
- 命中多个题材信号时可多选加载，但最终正文仍由 `N5-CREATIVE-DRAFT` 统一汇流，不为题材包生成平行草稿。
- 加载多包时先按 `项目题材轴 -> 场景功能轴 -> subtype` 收束；除非用户明确要求综合诊断，否则同一关键场面最多加载 1 个主题材核心包、1 个场面功能包和 1 个 subtype 包。
- 跨类型融合场景可额外加载1个融合题材核心包，但必须在 `fusion_manifest` 中记录融合决策和冲突裁决。

---

## Genre Scene Function Routing

类型化场面强化使用根共享合同 `.agents/skills/story/_shared/genre-scene-strengthening-contract.md`，再回到 `references/genre-scene-drafting-contract.md` 落到初稿 prose。

| scene_signal | scene_function | required_context | gate |
| --- | --- | --- | --- |
| 武戏、打斗、追逐、搏斗、战斗、巷战、兵器或能力交锋 | `action_combat` | `north_star.genre_contract`、当前章 planning、人物/场景/道具真源、空间与材质信号；武侠打斗加载 `wuxia_combat_design`，白刃气流命中时加 `wuxia_blade_qi_flow` | 攻防节拍、站位距离、动作代价和材质响应服务当前戏 |
| 言情、关系拉扯、亲密试探、误读、告白、破镜、甜宠或虐恋 | `romance_relationship` | 关系线、人物欲望/回避、当前压力、项目禁区 | 对白潜台词、边界和选择推进关系，不写占有奖励 |
| 玄幻、修仙、奇幻、高武、异能、规则兑现 | `xuanhuan_power` | 能力/规则真源、资源代价、世界约束、升级阶段 | 规则显影、能力边界和代价清楚，不新造规则 |
| 恐怖、灵异、克苏鲁、规则怪谈、惊悚逃亡 | `horror_suspense` | 威胁来源、视角限制、空间退路、感官信号 | 威胁遮蔽和信息延迟成立，不靠形容词喊恐怖 |
| 悬疑、侦探、案件、谍战、信息博弈 | `mystery_clue` | 线索/伏笔区别、证据状态、视角限制 | 线索可见且公平误导，不提前作者讲解 |
| 现实、职场、家庭、制度、年代、社会关系 | `realism_pressure` | 制度/社会关系约束、物件证据、后果链 | 现实压力有代价，不写无后果爽点 |

命中多个 scene signals 时，必须选 1 个 primary scene function，secondary functions 不超过 2 个；无法安全裁决时回退 `generic_scene_pressure`。

---

## Wuxia Action Subtype Routing

| signal | required_packages | prose target | forbidden |
| --- | --- | --- | --- |
| 普通武侠打斗、比武、围杀、追逐 | `wuxia_core`, `wuxia_combat_design` | 招路、拆招、变招、代价、胜负余波 | 只写快狠强 |
| 白刃剑气流、剑气、刀气、剑风、刀剑风压、港式武侠破坏感、90 年代香港新浪潮武侠、徐克/程小东式高飞剑侠、旧港片实物爆点、刀剑气质区分 | `wuxia_core`, `wuxia_combat_design`, `wuxia_blade_qi_flow` | 出刃路径、实体接触、材质破坏、人物反震、余波留痕、刀剑气质和动作戏剧功能 | 修仙法术、激光光束、现代 CG 光效、无源爆炸、分镜/prompt 化 |
| 江湖规矩或门派秩序主导的冲突 | `wuxia_core`, `wuxia_jianghu_order` | 武林身份、规矩代价、声望变化 | 把制度冲突写成纯打斗 |
| 武侠关系或恩义主导的冲突 | `wuxia_core`, `wuxia_relationship` | 留手、失手、承诺、背叛、恩义债 | 把情义写成脸色模板 |

---

## Execution Environment Notes

用户给出执行环境偏好时，不改变 `mode`，只追加执行备注。
