# 6-视频输出契约细则

## 阶段级交付

1. 视频请求 JSON
2. 可读文本视图
3. 最小 manifest 或说明
4. 下一步执行入口
5. 若进入真实生成阶段，则额外包含 provider handoff 包

## 当前最低要求

1. 不得只剩一段 prompt，没有请求字段。
2. 所有请求对象都必须能回链 `编导/第N集.json` 的分镜组或分镜。
3. `6-视频` 结束时必须能说明下一步是继续补参照，还是进入 `3-视频生成` / 具体 provider skill。
4. 共享 JSON 模板必须允许叶子子技能同时表达组级来源与帧级来源；至少应支持 `meta.group_id + meta.source_shot_ids + meta.shot_level`。

## 当前共享模板真源

- `.agents/skills/aigc/6-视频/_shared/video-generation-input.template.json`
- `.agents/skills/aigc/6-视频/_shared/视频生成入参.template.txt`

共享规则：

1. 多个视频子技能包若共用同一入参骨架，应统一回指该共享模板。
2. 多个视频子技能包若共用同一提示词阅读视图，应统一回指共享 txt 模板。
3. 叶子子技能可以补局部输出规则，但不应在各自 `templates/` 中平行维护第二份同类模板真源。
