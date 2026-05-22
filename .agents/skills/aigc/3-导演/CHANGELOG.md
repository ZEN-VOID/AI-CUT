# CHANGELOG

## 2026-05-22

- 吸收“场景身份先行”学习：导演阶段新增 `scene_identity_seed` 源层口径，为下游摄影、图像和视频提供年代、空间功能、社会语境、环境声底色和材质光影基底。
- 同步 `SKILL.md`、`directorial-authorship-contract.md`、review 与经验层，避免同一动作被下游生成到泛化空间或依赖泛化 BGM。
- 吸收“角色活人感行为动机”学习：导演阶段新增 `lived_in_behavior_seed` 口径，为表演层提供当前小事、生活压力/目标/阻碍、下意识反应方向、情绪落点和多人动作-反应分工。
- 同步 `directorial-authorship-contract.md`、`SKILL.md`、review 与经验层，避免下游凭空给角色找事做或把所有角色写成同强度表演。
- 新增人物动作链优先源层：导演阶段的氛围、道具、受控增强和尾钩必须先锁定人物 entry_state、action_vector、reachable_target 与 exit_state，再决定环境或物件承托。
- 同步 `SKILL.md`、`directorial-authorship-contract.md`、`controlled-enrichment-contract.md`、review 与经验层，避免把无互动对象或氛围细节硬写成导演干货并打断下游动作衔接。

## 2026-05-13

- 从旧合并阶段拆分初始化 `3-导演` 技能包。
- 承接编导创作内核、高潮画面、整集视觉主轴、画面美学、终结画面、氛围意境和受控增强。
- 搬入 references：directorial-authorship-contract、climax-visual-treatment-contract、episode-visual-spine-contract、visual-aesthetic-contract、episode-final-image-contract、atmosphere-and-mood-contract、controlled-enrichment-contract。
- 搬入 types：episode-final-image-type-map、cross-episode-continuity-type-map。
