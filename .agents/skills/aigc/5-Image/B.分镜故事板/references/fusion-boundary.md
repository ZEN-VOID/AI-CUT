# Fusion Boundary

## Source Packages

本包融合以下旧技能包的业务能力，原包暂不移除：

1. `.agents/skills/aigc/5-Image/1-提示词蒸馏/分镜故事板`
2. `.agents/skills/aigc/5-Image/2-参照引用`
3. `.agents/skills/aigc/5-Image/3-图像生成`

## Ownership

- `B.分镜故事板` 拥有组级 storyboard 端到端融合路由、三段汇流门与完成口径。
- 旧 `分镜故事板` 继续作为蒸馏规则和兼容脚本来源。
- 旧 `2-参照引用` 继续作为严格绑定规则、runner 和 provider-neutral 引用真源来源。
- 旧 `3-图像生成` 继续作为 provider handoff、submit-plan runner 与输出路径合同来源。

## Runtime Write Slots

本包不新增项目输出根。所有业务产物继续写入既有槽位：

- 请求对象：`projects/aigc/<项目名>/5-Image/分镜故事板/第N集/第N集.json`
- 参照绑定：`projects/aigc/<项目名>/5-Image/2-参照引用/<mode>/<source_tranche>/第N集/`
- 生成 handoff：`projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/第N集/`

## Mutual Exclusion

- 单一 `分镜ID` 的画面准备进入 `A.分镜画面`。
- 单个 `分镜组ID` 的多格 storyboard 准备进入本包。
- 漫画页、气泡文字、旁白框和阅读节奏进入 repo-local `comic` workflow。

## Compatibility Rule

若旧三包与本包规则冲突：

1. 保留旧包不动。
2. 本包按融合入口裁决当前任务。
3. 将差异记录到 `legacy-upgrade-migration-matrix.md` 或 `CONTEXT.md`。
