# Type Package: user-title-locked

## Purpose

当用户显式给出标题文字时，本包固定标题优先级，防止技能按模板擅自改写核心语义。

## Fixed Context

- `user_title_text` 是 `text_system.hook_title.text` 的主来源。
- 只允许为海报排版做最小必要压缩、断句或标点调整。
- 不得把用户标题改写成另一句“更爽”的标题。
- 若用户标题与本集事实冲突，必须报告冲突并提出最小修正，不得静默替换。

## Review Focus

- 输出标题是否与用户输入可逐字或同义比对？
- 调整是否只服务排版，不改变钩子？
- 该标题是否仍能被代表性画面承接？
