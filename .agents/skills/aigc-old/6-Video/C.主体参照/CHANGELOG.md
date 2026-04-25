# Changelog

## 2026-04-24

- 创建 `.agents/skills/aigc/6-Video/C.主体参照/` Skill 2.0 融合包。
- 融合旧 `全能参照`、`2-参照引用` 与 `3-视频生成` 的核心语义，并将 `2-参照引用` 特化为主体识别向绑定。
- 新增 `subject-index.json`、`subject-report.md` 与 `subject-match-report.md` 作为主体识别和绑定证据。
- 新增 `agents/openai.yaml`，默认提示显式唤起 `$aigc-video-subject-reference`。
- 原三个旧技能包保留不删除。
