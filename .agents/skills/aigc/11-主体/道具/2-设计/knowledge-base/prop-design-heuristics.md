# Prop Design Heuristics

本文件保存 `道具/2-设计` 的稳定经验和可复用打法；强制合同仍以根 `SKILL.md` 与分区规范为准。

## Research To Visual Translation

- 把事实转成可见词：材质、形制、年代、工艺、磨损、握持方式、尺度、重量感。
- 考据越冷门，越要区分“确定史实”和“视觉灵感”；不要让 uncertain fact 变成剧情真源。
- 有真实工艺参照时，优先提炼外观和制作痕迹，而不是解释完整制作流程。

## Story Pressure

- 物语写“这件物在人物和情境中承受了什么”，不是写背景百科。
- 关键道具至少有一个可跨镜头复现的识别点。
- 支撑道具应克制，避免抢走角色或场景的叙事焦点。

## Design Appeal And Cultural Detail

- 道具不能只满足“像这个东西”；它还要在轮廓、比例、材质、工艺、磨损、文化符号或功能结构上有可见设计。
- 关键道具的 `signature detail` 应该能被一句 prompt 锁定，例如特殊封缄、非对称轮廓、独特材质记忆点、铭文、徽记、修补痕或开合结构。
- 普通功能道具也要有克制设计：通过材质对比、手作痕迹、旧损、比例、接口、缝线、铆钉、包浆、折痕或封缄变得好看，而不是加随机装饰。
- 文化元素必须有语境：纹样、铭文、徽记、器型、封缄和材质选择要能回到时代、地域、阶层、职业、宗教/族群禁区或功能逻辑。
- `knowledge-base/prop-design-corpus.md` 适合在设计前选取“设计轴”和“文化母题”，再原创转译；不要把语料词条当模板句直接塞进输出。

## Prompt Compression

- 先保留：single prop subject、material、signature detail、wear/history、lighting/camera、global style anchor、negative constraints。
- 再删除：解释性从句、重复风格词、过多同义形容词、剧情摘要、角色心理。
- 英文 prompt 中不要塞多个并列道具主体；多主体会破坏后续生成锁定。

## Init Synthesis Integration

- 初始化综合中的摄影倾向优先落到光线、镜头距离、反光控制和画面识别方式。
- 初始化综合中的美术/设计倾向优先落到材质、形制、年代混搭、手工痕迹和颜色克制。
- 初始化综合中的导演/动作倾向优先落到使用方式、冲突状态、道具与身体的关系。
- 如果 `team.yaml.init_synthesis` 没有明确设计相关综合，就使用 north_star 和项目记忆，不强行编造顾问或监制角色。
