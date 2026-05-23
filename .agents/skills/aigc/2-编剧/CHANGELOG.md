# CHANGELOG

## 2026-05-22

- 新增 `表情特写` 作为 `2-编剧` 正式可选字段，用于关键面部表演 beat 的源层落点，避免面部变化长期散落在 `心理反应`、`对白画面` 或泛化“微表情”描述中。
- 明确 `表情特写` 只写眉、眼、嘴、鼻翼、咬肌、下颌、喉头、眨眼频率或皮肤状态等具体面部变化；不得写情绪标签、心理解释、摄影机位、景别或镜头运动。
- 同步字段路由、模板、review gate、workflow、经验层和机械校验；`4-表演` 保留并精修上游 `表情特写`，不再吞回泛化心理反应。

## 2026-05-13

- 从旧合并阶段拆分初始化 `2-编剧` 技能包。
- 承接保真规则、字段格式化、对白冻结、声画配对、slugline 稳定、小说表述二次画面化和好莱坞质量规范。
- 搬入 references：script-adaptation-contract、field-routing-and-audio-visual-contract、novel-to-screen-language-contract、hollywood-quality-spec。
- 搬入 types：source-to-script-type-map、type-map。
- 搬入 scripts：validate_script_projection.py。
