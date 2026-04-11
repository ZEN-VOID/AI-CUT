# aigc 3-明细 / 5-摄影美学 / 摄影参数 / Type Strategies

本文件承载 `aigc 3-明细 / 5-摄影美学 / 摄影参数` 的路由策略、VSM 与局部回退规则。

## Local Route Note

- 本技能是父级裁定后的唯一 leaf 入口，不在本层再分叉。
- 进入前提以主 `SKILL.md` 的 `When to Use / When Not to Use` 与父级路由结果为准。
- 若当前问题跨 sibling、输入前提不齐或边界不清，先回退父技能重新判路。

## Unknown Fallback

- unknown 默认路由：停止在父级判路层，不直接写本层产物。
- 若共享终稿、上游 handoff 或父级判路缺失，先补前提再恢复本层。
