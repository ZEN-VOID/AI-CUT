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

## Prompt Compression

- 先保留：single prop subject、material、signature detail、wear/history、lighting/camera、global style anchor、negative constraints。
- 再删除：解释性从句、重复风格词、过多同义形容词、剧情摘要、角色心理。
- 英文 prompt 中不要塞多个并列道具主体；多主体会破坏后续生成锁定。

## Init Synthesis Integration

- 初始化综合中的摄影倾向优先落到光线、镜头距离、反光控制和画面识别方式。
- 初始化综合中的美术/设计倾向优先落到材质、形制、年代混搭、手工痕迹和颜色克制。
- 初始化综合中的导演/动作倾向优先落到使用方式、冲突状态、道具与身体的关系。
- 如果 `team.yaml.init_synthesis` 没有明确设计相关综合，就使用 north_star 和项目记忆，不强行编造顾问或监制角色。
