# AIGC Character Design Corpus

本文件是 `角色/2-设计` 的高质量语料库，用于把“好看、有型、有镜头魅力”的要求转化为可执行的容貌、妆容、身形、服装和 prompt 词组。它是知识库，不替代 `SKILL.md` 的入口、门禁和输出合同。

## Source Basis

```yaml
source_basis:
  lexical_anchors:
    - "汉典：剑眉，直而末尾翘起略呈剑形的眉毛。用于男性英气、锋利、少年侠气或武将感的眉形锚点。"
    - "汉典：楚楚动人，形容姿态娇柔美好、令人心动。用于女性柔美、易碎、清透、怜爱感的审美锚点。"
  makeup_and_period_context:
    - "传统妆容资料显示，古典妆容常重眉妆、眼妆、唇妆；唐代妆容更浓郁、多样、外向，宋代趋于收敛精致，明代更低调并强调复杂头饰。"
  costume_period_context:
    - "中国文化研究院资料显示，明代以袍衫、补服、乌纱帽、四方平定巾、比甲等为重要服饰语境；清代制度繁杂，长袍、马褂、马甲、马蹄袖和旗袍等具有时代特征。"
  visual_design_context:
    - "服装视觉研究可作为经验支撑：style、color、texture 都是服装时尚识别要素，角色设计中应同时处理廓形、色彩和材质。"
source_urls:
  - "https://www.zdic.net/hant/%E5%89%91%E7%9C%89"
  - "https://www.zdic.net/hans/%E6%A5%9A%E6%A5%9A%E5%8B%95%E4%BA%BA"
  - "https://fushiyi.cn/24569.html"
  - "https://chiculture.org.hk/sc/china-five-thousand-years/2487"
  - "https://arxiv.org/abs/1608.07444"
usage_boundary:
  - "语料用于启发和转译，不逐字套用。"
  - "服装风格化必须受项目时代、地域、阶层、职业、2-美学输出和项目 MEMORY.md 约束。"
  - "真实人物灵感默认不用或泛化处理；只有用户/项目允许且有必要时，才抽象为骨相、眼神、妆发和镜头魅力，不生成可识别现实人物。"
  - "服装磨损、污渍、补丁和做旧只在清单证据、职业逻辑或项目风格支持时使用。"
  - "多服装、战斗、战损、受伤、少年、老年等必须作为同一 base character 的变体处理；语料库只能帮助写状态 delta，不能把变体写成新的脸、新的身形或新的角色身份。"
  - "眼尾压暗、低调反差和危险感只允许作为局部气质修饰；不得扩写成重面部阴影、暗脸、遮眼阴影、半脸阴影或低调剪影。角色定妆照必须保留清晰五官、骨相、肤色层次和表情意图。"
```

## Universal Aesthetic Rules

| rule | design action | prompt action |
| --- | --- | --- |
| 不做平淡还原 | 清单关键词先转为来源匹配审美目标，再转为脸、妆、身形、服装 | 使用可见名词和材质词，不只写 beautiful / handsome |
| 美丽动人路线 | 仅当年龄、身份、项目调性和角色功能支持时，明确眼神、眉形、唇色、肤质、发型、身形比例和服装曲线 | `delicate yet striking beauty`, `luminous eyes`, `soft sculpted makeup` |
| 英俊不凡路线 | 仅当年龄、身份、项目调性和角色功能支持时，明确眉骨、鼻梁、颌线、肩颈、站姿、服装线条 | `sharp brows`, `clear jawline`, `commanding posture` |
| 主角必须帅/美 | 主角、核心情感线角色和长期复用角色必须达到 `lead_beauty_handsomeness_floor=required`；男主通常要有英俊/清峻/锋利/贵气等来源匹配吸引力，女主通常要有美丽/清透/明艳/清冷等来源匹配吸引力，其他性别表达、年龄或物种用主角级好看等价策略 | `lead-character beauty`, `heroic handsomeness`, `cinematic lead attractiveness` |
| 主角必须有整体气质 | 主角、核心情感线角色和长期复用角色必须达到 `lead_presence_temperament_floor=required`；整体气质要从身份压力、精神状态、眼神意图、头颈肩背、重心姿态、动作节奏和服装承托中形成，不能只写漂亮脸、好身材或“有气质” | `lead-character presence`, `heroic temperament`, `magnetic protagonist aura` |
| 主角更强 | 主角必须有高记忆点脸部、妆发、服装 signature 和整体镜头存在感，并达到 `charisma_floor=high`；路线必须来源匹配，不做模板脸、网红脸、成人化、性化或空泛气场 | `lead-character presence`, `cinematic leading-face quality` |
| 大反派必须有魅力 | 大反派、主要对抗者、长线威胁和终局 Boss 必须达到 `charisma_floor=high`；危险、阴郁、病态、锋利、怪诞都要转成可控的镜头吸引力和压迫性，不只写丑、脏、乱或恐怖 | `charismatic menace`, `controlled dark elegance`, `magnetic villain presence` |
| 普通反派也要可识别 | 短登场或功能性反派可以不做高魅力，但至少要有脸部/妆发/姿态/服装钩子 | `distinctive antagonist silhouette`, `sharp readable visual hook` |
| 服装不脱离时代语境 | 先锁定时代/地域/阶层，再做廓形、色彩、材质风格化 | 避免现代高定词硬塞古代制度服饰 |
| 脸部先可读再氛围化 | 阴郁、危险、压迫感优先落在眉眼、骨相、姿态、服装材质和受控边缘光；重阴影不能遮住五官 | `clear readable facial features`, `soft frontal fill light`, `subtle rim light` |

## Role Type Corpus

### 男主 / Male Lead

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 剑眉星目、英俊不凡、清峻朗逸 | 剑形上扬眉、眉骨清晰、眼神明亮有压迫感、挺直鼻梁、干净颌线、低饱和修容、清爽发际 | 修长纵向线条、利落领口、肩线明确、低调贵气材质、时代合规外袍/长衫/制服 | 只写“帅哥”“冷峻”，缺少五官和服装 signature |
| 少年侠气、明亮锋利 | 眉尾上挑、眼尾干净、唇色自然、皮肤清透、发束有风感 | 窄袖、束腰、轻便层次、靴履利落、可行动面料 | 过度油腻、现代偶像发型脱离时代 |
| 帝王/权贵男主 | 眉目沉稳、鼻梁高直、颧骨克制、唇线薄而坚定、发冠或发髻整洁 | 礼制层次、深色主调、金属/刺绣克制点缀、符合身份等级 | 把权贵写成满身现代奢牌或过度奇幻盔甲 |

可用中文短语：

- 剑眉星目、眉骨如削、目光清亮、鼻梁挺直、薄唇含锋、肩背挺拔、清峻朗逸、英气逼人、贵而不浮。
- 冷白皮不等于无血色；可写“冷调底妆下保留淡淡血色”，避免蜡像感。

### 女主 / Female Lead

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 楚楚动人、清透动人 | 雾感弯眉、含水眼、卧蚕微亮、柔和鼻影、花瓣唇、轻透底妆、泪痣或小痣点睛 | 柔软面料、顺垂线条、轻盈层次、局部亮色或珠光点缀 | 只写“漂亮”“温柔”，没有妆容和轮廓 |
| 明艳大女主 | 上扬眉眼、饱满唇色、立体颧骨、干净高光、发髻/卷发有体量 | 强轮廓外衣、明确腰线、饱和但时代合规色彩、金属或珠饰重点 | 把明艳写成廉价浓妆或现代红毯礼服硬套古代 |
| 清冷女主 | 细长眉、眼妆收敛、唇色偏淡、骨相清晰、发丝整齐 | 冷色系、窄长线条、低装饰密度、精致纹理 | 写成苍白无表情，缺少可记忆的美感 |

可用中文短语：

- 楚楚动人、明眸善睐、眉眼含雾、肤若凝光、唇色如花、鬓发轻贴、清丽不弱、柔中带刃。
- 女主柔弱时也要有主体性：用眼神、站姿、服装层次表现内在韧性。

### 反派男 / Male Antagonist

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 邪魅锋利 | 眉峰高、眼窝深、眼尾压暗、唇线窄、颌线硬、局部阴影增强 | 深色纵向廓形、窄袖、硬挺材质、金属小面积冷光 | 简单写丑、脏、乱 |
| 病态贵气 | 皮肤偏冷、眼下微青、薄唇、精致发型、克制修容 | 细密纹样、冷色锦缎、层次整齐但带压迫感 | 失去时代身份，变成现代哥特模板 |

### 反派女 / Female Antagonist

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 危险美人 | 上挑眼线、清晰眉峰、唇色偏深、颧骨高光、发髻锐利 | 强腰线、窄长轮廓、深色或高对比配色、首饰有锋利感 | 把反派女性只写成妖艳刻板印象 |
| 阴郁权谋型 | 眉眼压低、底妆雾面、唇色暗红或豆沙、眼神克制 | 暗纹面料、低饱和华丽、礼制合规首饰 | 服装过度奇幻、脱离身份制度 |

### 书生 / Scholar

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 温润清贵 | 平直细眉、眼神温和、鼻梁秀挺、唇色浅、发冠整洁 | 宽袍、交领/圆领按时代选择、素雅纹理、袖口整洁 | 一律白衣飘飘，不管时代和阶层 |
| 藏锋谋士 | 眉眼清淡但目光锐、唇线克制、面部少修饰 | 深灰、墨绿、茶褐等低饱和色，细密纹样 | 没有视觉记忆点 |

### 武将 / Warrior

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 雄健英武 | 浓眉、眼神直、鼻梁硬、下颌宽、肤色有户外质感 | 盔甲或劲装需符合时代兵制，护腕、腰封、靴履按职业逻辑选择维护良好、轻度使用或有依据磨损 | 现代战术服硬套古代武将 |
| 女将锋芒 | 眉眼上扬、妆容干净、颧骨光感、发束利落 | 护甲与裙/袍结构协调，便于行动，色彩有身份标识 | 把女将写成纯性感战衣 |

### 少年 / Girl Or Boy Youth

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 少年感 | 眉形自然、眼睛明亮、脸部留圆润、唇色健康 | 轻便、干净、色彩明快，配饰少 | 成人化、性化、过度成熟妆 |
| 少女感 | 圆润脸颊、清透底妆、淡唇、发饰轻巧 | 柔软短层次、活泼色彩、时代合规发髻/发辫 | 过度艳俗或现代网红妆 |

### 成熟女性 / Mature Woman

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 雍容沉静 | 眉眼舒展、唇色稳重、轮廓柔和、发髻体面 | 面料厚重、层次稳、首饰讲究位置和等级 | 简单用年龄削弱美感 |
| 权力女性 | 眼神稳定、眉峰有力度、妆面整洁无杂乱 | 轮廓庄重、色彩低饱和但有权力标记 | 过度年轻化或现代职场套装乱入 |

### 平民 / Servant / Background Anchor

| aesthetic target | face and makeup tokens | costume tokens | avoid |
| --- | --- | --- | --- |
| 质朴但好看 | 肤色自然、眉眼干净、发丝收束、表情有生活感 | 粗细材质有对比，服装状态受资源限制；补丁/磨损只在职业或叙事有依据时出现 | 写成脏乱、灰扑扑、没有设计 |
| 机灵市井 | 眼神亮、眉形活、唇色健康、发型轻便 | 短打、围裙、袖口、腰间小物符合职业 | 用现代街头潮牌替代时代服饰 |

## Makeup Stylization Bank

| makeup mode | use case | concrete design tokens |
| --- | --- | --- |
| 清透底妆 | 女主、少年、纯净型角色 | 轻透肤质、微光高点、淡粉唇、自然卧蚕、雾面弯眉 |
| 锋利修容 | 男主、反派、权力角色 | 眉骨阴影、鼻梁高光、颌线清晰、眼尾压暗、唇线克制 |
| 唐风浓郁 | 唐代或开放繁华语境 | 花钿、斜红、面靥、饱满胭脂、圆润脸部、华丽发饰 |
| 宋风收敛 | 宋代或文雅礼制语境 | 细长眉、低调眼妆、三白提亮、淡唇、珍珠妆用于礼仪场景 |
| 明风低调华贵 | 明代贵族或礼制场景 | 妆面克制、发髻和头面复杂、珠饰点睛、唇色稳重 |
| 现代影视精修 | 现代/架空可用 | 干净底妆、骨相修饰、镜头友好高光、发型有 silhouette |

## Costume Period Context Guardrails

| context | stylize through | must respect | avoid |
| --- | --- | --- | --- |
| 先秦/汉感 | 交领、曲裾/直裾感、宽袖、带饰、庄重色 | 礼制、层次、布料重心 | 现代露肩礼服、机能外套 |
| 唐感 | 圆领袍、襦裙、半臂、披帛、胡风元素、饱满色彩 | 开放繁华但要区分初唐/盛唐/晚唐 | 把所有唐代女性都写成晚唐巨大发髻 |
| 宋感 | 窄袖、褙子、素雅层次、文人气 | 收敛、精致、理性、低饱和 | 过度华丽、明艳到失去宋代克制 |
| 明感 | 袍衫、比甲、圆领、补服、四方平定巾、头面 | 等级、礼制、身份差异 | 清代马褂/旗袍乱入明代 |
| 清感 | 长袍、马褂、马甲、马蹄袖、旗袍早期宽大轮廓 | 满汉制度、发式、袖口、礼服语境 | 现代紧身旗袍直接套早清 |
| 民国感 | 长衫、中山装、学生装、早期旗袍、西式外套混合 | 城市、阶层、年份差异 | 现代晚礼服替代民国剪裁 |
| 现代感 | 职业服、街装、礼服、制服、亚文化造型 | 职业真实性、维护状态、品牌泛化风险；生活磨损只在证据支持时写入 | 只有潮牌词，没有角色身份 |
| 架空/玄幻 | 先定真实时代母体，再叠加材质、纹样和符号 | 母体时代和项目 worldbuilding | 时代元素随机混搭，没有制度逻辑 |

## Phrase Transformation Patterns

| bland input | better Chinese design phrase | prompt-ready English |
| --- | --- | --- |
| 男主很帅 | 剑眉上扬、眼神如寒星，鼻梁挺直，颌线干净，肩背有压迫性的挺拔 | sharp upward brows, bright star-like eyes, straight nose bridge, clean jawline, commanding shoulders |
| 女主很漂亮 | 眉眼含雾、肤质清透，花瓣唇带一点血色，发丝贴颊形成柔软轮廓 | misty eyes, translucent skin, petal-tinted lips, soft face-framing hair |
| 主角有气质 | 先定身份压力和精神状态，再落到稳定眼神、头颈肩背、重心姿态、动作节奏和服装承托，形成能撑住镜头的主角感 | focused gaze, composed neck and shoulders, grounded stance, restrained movement rhythm, protagonist presence |
| 反派很邪 | 眉峰锋利、眼尾压暗，薄唇收紧，暗纹服装带冷金属细节 | sharp brow peaks, shadowed outer eyes, narrow lips, dark patterned costume with cold metallic accents |
| 书生温柔 | 平直细眉、眼神温润，衣料素雅但袖口整洁，整体清贵 | refined straight brows, gentle eyes, plain elegant robe fabric, neat cuffs, restrained nobility |
| 女将很飒 | 上扬眉眼、干净修容，束发利落，护甲与裙袍层次适合行动 | lifted brows and eyes, clean contouring, tied-back hair, action-ready armor and robe layers |
| 平民朴素 | 肤色自然、眉眼干净，粗布层次有资源限制下的穿着状态；磨损只在有依据时出现 | natural complexion, clean brows and eyes, resource-limited coarse fabric layers with restrained colors |

## Prompt Assembly Rules

1. 先写 asset ID，再写角色核心审美；默认稿使用 `base_subject_id`：`C001: cinematic full-body costume fitting photo of ...`
   - 变体稿先写变体资产 ID：`C001-V02: ...`，并保留 base character 的核心脸部骨相、眼神、身形比例和气质。
2. 容貌写到眉、眼、鼻、唇、骨相、肤质或妆面中的至少三项。
3. 服装写到廓形、材质、色彩、时代母体、配件或服装状态/维护状态中的至少四项；磨损只在证据支持时使用。
4. 妆容化处理必须可见：眉形、眼妆、唇色、修容、肤质、发型或头饰至少两项。
5. 服装风格化必须先过时代语境：如果时代不明，用“project-era-consistent costume silhouette”占位，不强行写具体朝代服制。
6. 真实人物灵感默认不进入；只有用户/项目允许且有必要时才进入中间设计说明。英文 prompt 优先写原创化特征，不直接点名现实人物。

## Negative Examples

| bad output | failure reason | repair |
| --- | --- | --- |
| “男主很帅，穿黑衣，很冷峻。” | 平淡、抽象、无妆发、无服装时代 | 补剑眉/眼神/鼻梁/颌线/肩背，补黑衣的材质、时代廓形、领口、腰封 |
| “女主楚楚动人，白裙飘飘。” | 只套成语，无具体面部与妆容 | 补雾眉、含水眼、花瓣唇、发丝轮廓，白裙需说明时代母体和材质 |
| “反派丑陋阴森。” | 反派丑化，缺个性魅力 | 改为危险美感：高眉峰、暗眼尾、薄唇、冷色纹样、克制金属 |
| “古代女主穿现代高定礼服。” | 服装脱离时代语境 | 找时代母体：襦裙/褙子/比甲/旗袍等，再做材质和配色风格化 |
