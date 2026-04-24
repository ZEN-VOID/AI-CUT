# CHANGELOG.md

## 2026-04-24

- 创建 `.agents/skills/aigc/6-Video/A.分镜画面参照/` Skill 2.0 融合包。
- 将旧三段能力映射进新包分区：
  - `1-提示词蒸馏/首帧参照` -> prompt/TXT 蒸馏合同、共享提示原则、workflow `N2`
  - `2-参照引用` -> `Assets/` 引用绑定合同、workflow `N3`
  - `3-视频生成` -> provider handoff 合同、workflow `N4`
- 保留原三个技能包，不移动、不删除。
- 新增 `agents/openai.yaml`，默认提示显式唤起 `$aigc-video-frame-visual-reference`。
