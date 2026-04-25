# CHANGELOG.md

## 2026-04-24

- 初始化 `A.分镜画面` Skill 2.0 融合包。
- 将原 `分镜帧`、`2-参照引用`、`3-图像生成` 的入口语义、执行拓扑、provider handoff 和经验层融合进新包分区。
- 保留原三个技能包，不移动、不删除。
- 固定本包不创建新的项目 runtime 真源，继续写入旧三段兼容落点。
- 将旧 `分镜帧` 的完整蒸馏方法消化进 `references/request-distillation.md` 与 `steps/frame-image-workflow.md`，覆盖 prompt 装配、节点细则、字段门禁、压缩等级、输出模式和蒸馏审计。
