# Changelog

## 2026-06-11

- 新增 `Output Object Scope Contract`：`画面基调` 固定为项目级 `global_singleton`，不得创建逐集 `画面基调`；场景、道具、分镜、角色、摄影五类风格在单集任务中写入 `3-美学/第N集/<风格>/`，整季/项目基线才写项目级风格目录。
- 同步父级输出合同、子技能路由矩阵、下游 handoff 与审查门；逐集父级总览写入 `3-美学/第N集/美学总览.md` 和 `执行报告.md`。
- 同步 root AIGC、5-9 阶段、10 分组、11-主体设计、registry、README 与 agent prompt 的 episode-first / fallback 读取规则。

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求父级证明同一剧本源、项目记忆和参考资料如何约束 6 路风格协议。
- 新增 `FAIL-AES-UPSTREAM-CONTEXT`、`GATE-AES-10-UPSTREAM-CONTEXT` 和父级报告 `Upstream Context Application Map`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-04

- 修正 3-美学父级 handoff 的旧阶段引用：下游继承目标从旧 `4-摄影` 收敛到当前 `4-导演`、`5-表演`、`6-氛围`、`7-分镜`、`8-摄影`、`9-光影`、`11-主体`、`12-图像`、`13-画布` 阶段链。
