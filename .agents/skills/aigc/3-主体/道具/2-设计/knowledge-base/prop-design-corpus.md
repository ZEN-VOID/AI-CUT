# AIGC Prop Design Corpus

本文件是 `道具/2-设计` 的高质量语料库，用于把“道具也要有可见设计价值，而不是简单平凡”的要求转化为可执行的形制、材料、工艺、结构、条件性文化/身份符号、使用/保存状态和 prompt 词组。它是知识库，不替代 `SKILL.md` 的入口、门禁和输出合同；纹样、铭文、徽记和装饰不是默认必选项。

## Usage Boundary

```yaml
usage_boundary:
  - "语料用于启发和原创转译，不逐字套用。"
  - "文化/身份符号必须受项目时代、地域、阶层、职业、宗教/族群禁区和 north_star.yaml 约束；无依据时采用功能主导或极简细节。"
  - "道具可以风格化、精致化、符号化，但不能变成时代错配的廉价装饰堆砌。"
  - "使用/保存状态必须按证据选择；磨损、污渍、包浆、锈蚀、破损不是默认设计感。"
  - "危险物、武器、机关和医疗器具只能保留美术外观和叙事功能，不输出现实可操作结构。"
```

## Universal Design Rules

| rule | design action | prompt action |
| --- | --- | --- |
| 不做普通物件 | 每个道具至少有一个独特轮廓、一个材质记忆点、一个工艺/结构细节或一个有依据的符号细节 | 写 `unique silhouette`, `signature detail`, `crafted surface` 等可见词 |
| 文化元素条件可见 | 仅在有依据时，把地域、时代、信仰、家族、职业、阶层转成纹样、铭文、符号、器型或工艺；无依据时采用极简、洁净、功能主导或材料主导细节 | 写具体 motif；无依据时写 function-led detail，不写空泛 `cultural elements` |
| 细节服务功能 | 装饰、状态证据、接口、开合、封缄、绑带、铆钉都应解释功能或叙事 | prompt 中保留 functional detail，不堆无意义 ornament |
| 美感与状态并存 | 道具可全新、洁净、封存、高维护、轻度使用、破损或古旧，但状态必须有设计秩序和视觉吸引力 | `pristine crafted surface`, `sealed ceremonial finish`, `aged but elegant`, `weathered crafted detail` |
| 时代语境优先 | 先锁定时代/技术/地域母体，再做风格化和文化元素 | 避免 modern luxury / tactical / cyberpunk 乱入历史道具 |

## Design Axes

| axis | required questions | usable tokens |
| --- | --- | --- |
| `silhouette` | 远看是否有独特轮廓？比例、开口、把手、边角、可动件是否可辨认？ | crescent silhouette, squared ritual form, asymmetrical handle, layered rim |
| `material_memory` | 主材、副材、反光、透明度、重量感是否清楚？ | oxidized bronze, lacquered wood, frosted jade, cracked enamel, brushed steel |
| `craft_detail` | 它如何被制造？铸造、锻打、雕刻、嵌银、漆艺、缝制、编织是否可见？ | hand-carved relief, inlaid silver linework, hammered edge, stitched leather wrap |
| `cultural_motif` | 是否确有文化/身份/机构/功能符号依据？纹样、铭文、图腾、封印、家徽、祭祀符号是否合规；无依据时是否改用克制功能细节？ | cloud-and-thunder motif, lotus engraving, seal-script inscription, family crest, function-led surface detail |
| `condition_state` | 使用/保存状态如何可见？是全新、未启封、洁净、抛光维护、展陈级、仪式封存、轻度使用、重度磨损、修补、氧化、污染还是损伤？ | pristine polished surface, sealed label, clean machined edges, maintained shine, light handling marks, repaired crack, patina in grooves |
| `wear_trace` | 旧化是否确有依据？磨损、包浆、划痕、修补、污渍、焦痕、折痕是否服务叙事而非默认添加？ | polished worn edges, repaired crack, patina in grooves, ink stains |
| `function_mechanism` | 使用方式如何暗示？开合、锁扣、机关、容器、接口、握持点是否清楚？ | visible hinge, sealed clasp, sliding ring, recessed grip, latch mechanism |
| `story_signature` | 为什么它在故事里必须被看见？有何身份、权力、秘密、诅咒、记忆或交易痕迹？ | talismanic detail, oath-marked surface, hidden compartment, owner-worn texture |

## Prop Type Corpus

### 关键剧情道具 / Key Prop

| design target | details | avoid |
| --- | --- | --- |
| 远看可识别，近看有信息 | 独特外轮廓、核心符号、隐藏结构、材料反差、手工痕迹、专属状态证据 | 只写“神秘物件”“重要道具”，没有可见 signature |
| 可跨镜头复现 | 固定主体 ID、固定 silhouette、固定主材、固定文化 motif、固定损伤点 | 每次生成都换形状、换材质、换符号 |

中文短语：

- 远看一眼可辨，近看层层有细节。
- 主体轮廓像被故事本身雕出来，而不是临时摆设。
- 文化纹样不是贴花，而是嵌进结构、用途和主人身份里。

### 仪式/宗教/权力道具 / Ritual Object

| design target | details | avoid |
| --- | --- | --- |
| 庄重、神秘、有制度感 | 对称构图、礼制尺度、符号位置、封缄、供奉痕迹、金属/玉石/漆木质感 | 伪造具体宗教或族群事实 |
| 文化元素有来源边界 | 云雷纹、莲纹、太阳/月相、封印、铭文、祭器器型、家族徽记 | 多文化符号随机混搭 |

Prompt tokens:

- ceremonial object, symmetrical ritual silhouette, carved seal-script band, oxidized metal grooves, sacred but weathered surface

### 武器/危险物 / Weapon Or Hazard Prop

| design target | details | avoid |
| --- | --- | --- |
| 美术外观强，现实操作弱 | 独特刃形/护手/鞘口/铆钉/包缠/维护或磨损状态/仪式标记 | 可复现伤害结构、制造步骤、现实教程 |
| 危险但好看 | 冷光金属、磨蚀边缘、克制装饰、权力徽记、旧血痕只作叙事痕迹 | 简单脏乱、廉价尖刺堆砌 |

Prompt tokens:

- ornate guard, worn grip wrap, cold metal sheen, ceremonial scabbard detail, non-operational fantasy mechanism

### 文书/信物/契约 / Document Or Token

| design target | details | avoid |
| --- | --- | --- |
| 薄物件也要有层次 | 纸张边缘、折痕、封蜡、绳结、印章、墨迹、编号、暗纹水印 | 一张普通白纸 |
| 信息可见但不泄密 | 局部铭文、符号化文字、封缄结构、保存状态或边角痕迹 | 真实个人信息或长段可读文本 |

Prompt tokens:

- folded parchment layers, wax seal, frayed cord binding, ink-stained edge, embossed watermark

### 容器/盒匣/钥匙 / Container Or Key

| design target | details | avoid |
| --- | --- | --- |
| 开合逻辑可见 | 锁扣、铰链、嵌片、边框、暗格暗示、接触点状态 | 光滑盒子没有结构 |
| 文化元素嵌入结构 | 纹样沿边框走、铭文绕锁孔、家徽压在封片上 | 贴一张符号图案当文化元素 |

Prompt tokens:

- hinged lacquer box, carved border motif, tarnished lock plate, hidden-compartment seam, worn key teeth

### 工具/生活器物 / Tool Or Everyday Object

| design target | details | avoid |
| --- | --- | --- |
| 平凡物也要有手作和生活记忆 | 握持磨亮、边缘修补、材质分区、局部污渍、绳结、铭刻 | 灰扑扑、普通、无设计 |
| 功能决定美感 | 重心、把手、接口、接触点状态、便携方式 | 只堆装饰，不说明用途 |

Prompt tokens:

- hand-worn handle, repaired rim, practical crafted shape, subtle carved maker mark, everyday patina

### 饰物/随身小物 / Ornament Or Wearable Prop

| design target | details | avoid |
| --- | --- | --- |
| 小物件需要轮廓和材质记忆 | 吊坠外形、链节、镶嵌、流苏、缝线、佩挂方式、保存或佩戴状态 | 只写漂亮首饰 |
| 文化元素微型化 | 家徽、护符、花鸟纹、文字、图腾、身份色 | 过度现代奢牌化 |

Prompt tokens:

- miniature talisman pendant, inlaid gemstone, braided cord, tiny engraved crest, aged gold filigree

### 科技/机关/装置 / Device

| design target | details | avoid |
| --- | --- | --- |
| 机制暗示而非工程教程 | 外壳、接口、灯点、刻度、旋钮、封闭结构、维护或使用状态区 | 真实可复现电路/武器/危险机制 |
| 技术时代一致 | 蒸汽、机械、赛博、古代机关、法器科技都要先定母体 | 机械表、芯片、符咒乱混无逻辑 |

Prompt tokens:

- sealed mechanical casing, visible dial marks, brass hinge array, softly glowing indicator, non-operational display detail

## Cultural Element Bank

| cultural layer | designable elements | guardrail |
| --- | --- | --- |
| 王权/官署 | 徽记、印章、等级色、规整对称、封缄、铭牌 | 不伪造真实官制，除非项目已声明 |
| 家族/门派 | 家徽、私印、重复纹样、专属配色、修补传统 | 不让所有组织都用同一套龙纹/云纹 |
| 民间手作 | 粗细不均的线迹、手工刻痕、竹木编织、布包边、泥金修补 | 不写成廉价脏乱 |
| 商贸/城市 | 编号、票据、封条、维护金属、运输痕迹、商号标识 | 避免现代品牌 logo |
| 宗教/仪式 | 对称、供奉痕迹、香灰、封印、象征纹样、礼制尺度 | 不随机混搭真实宗教符号 |
| 异域/边地 | 几何纹样、皮革、骨角、金属片、编绳、风沙环境痕迹 | 避免刻板化族群符号 |
| 科幻/未来 | 模块接缝、哑光复合材料、发光指示、编号、维护状态或受控磨损 | 不脱离项目技术水平 |

## Period And Context Guardrails

| context | stylize through | avoid |
| --- | --- | --- |
| 古代/历史 | 器型、铸造/漆艺/雕刻/织物/封缄、手工误差、礼制符号 | 现代塑料、高定 logo、战术导轨、赛博灯条 |
| 民国/近代 | 金属铆钉、皮革、纸张印刷、机械表面、封条状态、城市使用痕迹 | 过度古风纹样或现代潮牌 |
| 现代现实 | 工业设计、品牌去标识化、塑料/玻璃/金属复合、使用或维护状态 | 空泛“未来感”或无来源古代符号 |
| 架空/玄幻 | 先定真实或项目母体，再叠加符号、材质和异质结构 | 云纹、符文、宝石、尖刺无逻辑堆砌 |
| 科幻 | 技术层级、模块结构、维护痕迹、接口语言、显示逻辑 | 不可解释的魔法符号乱入硬科幻 |

## Phrase Transformation Patterns

| bland input | better Chinese design phrase | prompt-ready English |
| --- | --- | --- |
| 一把钥匙 | 细长齿形不对称的旧铜钥匙，钥匙柄内嵌家徽小孔，齿根有磨亮包浆 | asymmetrical aged brass key, crest cutout in the bow, polished patina around the teeth |
| 一本书 | 深色皮革封面的旧书，书脊有裂纹和压印符号，边角被反复翻阅磨白 | dark leather-bound book, cracked spine, embossed symbol, worn pale corners |
| 一个盒子 | 漆木盒匣，四角有铜包边，锁片周围有细小云纹和反复开合留下的接触痕迹 | lacquered wooden box, brass corner guards, fine cloud motif around the lock plate, subtle opening contact marks |
| 一枚新制徽章 | 镜面抛光的合金徽章，边缘干净锐利，背面封蜡完整，编号清晰无污损 | polished alloy badge, crisp clean edge, intact wax seal on the back, clear serial mark |
| 一个无菌试剂盒 | 半透明硬壳试剂盒，封签未撕、接口洁净、内部格槽规整，只有制造编号和冷光反射 | sterile translucent reagent case, unbroken seal label, clean ports, orderly inner slots, cool reflective surface |
| 一枚戒指 | 内侧刻有家族短铭，外圈镶嵌暗色石，金属边缘因长期佩戴被磨圆 | ring with inner family inscription, dark inset stone, rounded worn metal edges |
| 一把刀 | 弯月形短刃，护手有克制纹样，皮革握把磨亮，鞘口有旧裂痕 | crescent short blade, restrained guard motif, polished leather grip, cracked scabbard mouth |
| 一个罗盘 | 黄铜外壳、玻璃面微裂，刻度有手工误差，边框嵌入细密方向符号 | brass compass casing, cracked glass face, imperfect hand-marked scale, dense directional symbols |

## Prompt Assembly Rules

1. 先写主体 ID，再写单道具主体和独特轮廓：`PROP-001: full-view prop shot, 45-degree view of ...`
2. 至少写入四类设计细节：形制、材质、工艺/结构、文化/身份/功能符号适用性、使用/保存状态、功能结构、尺度中的四项；旧化词和文化贴花只在证据支持时使用。
3. 文化元素若被采用必须具体：纹样、铭文、徽记、封缄、器型、工艺来源或地域暗示，不使用空泛 `cultural elements`；若不采用，必须说明极简/洁净/功能主导的设计理由。
4. 风格化必须回到时代/地域/阶层/职业母体；不确定时写 `project-era-consistent crafted prop design`。
5. 保留固定画面约束：full-view prop shot、45-degree view、full prop in view、entire prop fully visible、uncropped full silhouette、prop only、solid color background、no people、no background elements、no scene environment。

## Negative Examples

| bad output | failure reason | repair |
| --- | --- | --- |
| “一个普通盒子，木头材质。” | 平凡、无轮廓、无工艺、无设计判断 | 补盒匣器型、锁片、边框、漆面、开合结构和状态证据；纹样只在时代/身份/功能有依据时加入 |
| “神秘法器，充满仪式感。” | 抽象词堆叠 | 补对称结构、铭文、供奉痕迹、材质、封缄、尺度 |
| “古代道具但有赛博灯条。” | 时代语境错配 | 改为项目时代合规的嵌银、夜光矿物、漆面反光或符号化材料 |
| “破旧钥匙。” | 只有状态，没有设计 | 补齿形、柄孔、金属氧化、家徽、磨亮位置 |
