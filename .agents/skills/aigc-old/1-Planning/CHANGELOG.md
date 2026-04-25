# CHANGELOG.md

本文件记录 `aigc/1-Planning` 的结构性改动与迁移索引，不参与默认预加载。

## 2026-04-24

- `Case-20260424-AIGC-PLANNING-SCRIPT-STANDARD-ONLY`
  - 按用户确认移除 `2-格式` 的标准剧/解说剧/双案分支区分，统一 canonical 出口为标准剧格式投影。
  - `validate_script_output.py` 的旧 `--variant` 参数改为兼容入口；任意非 `standard` 值只提示归一，不再触发独立解说剧校验逻辑。
  - 同步更新父 `SKILL.md`、`script-format-contract.md`、模板、类型映射、经验层与《诡校》项目执行报告。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/scripts/validate_script_output.py`
    - `.agents/skills/aigc/1-规划/references/script-format-contract.md`
    - `.agents/skills/aigc/1-规划/templates/script-format-report.template.md`
    - `projects/aigc/诡校/1-Planning/2-格式/执行报告.md`

## 2026-04-25

- `Case-20260425-AIGC-PLANNING-SCRIPT-DISPLAY-NAME`
  - 按用户确认将源层中 `2-格式` 的业务表述口径调整为 `2-剧本`，以避免误解为“只处理格式字段”。
  - 具体执行规则不变：内部 mode id 仍为 `script_format`，历史 runtime 路径仍为 `projects/aigc/<项目名>/1-Planning/2-格式/`，脚本接口、字段合同、validator 与下游分组路径均不重命名。
  - 同步更新父 `SKILL.md`、`script-format-contract.md`、planning I/O、grouping 继承口径、模板、经验层、入口元数据和 manifest display metadata。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/references/script-format-contract.md`
    - `.agents/skills/aigc/1-规划/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-规划/references/grouping-contract.md`
    - `.agents/skills/aigc/1-规划/templates/script-format-report.template.md`
    - `.agents/skills/aigc/1-规划/skill_manifest.json`

- `Case-20260425-AIGC-PLANNING-SOUND-VISUAL-PAIR`
  - 按用户反馈为 `2-剧本` 增设 `音效画面`，并将 `音效 -> 音效画面` 固化为和 `对白 -> 对白画面`、`独白 -> 独白画面`、`旁白 -> 旁白画面` 同级的声画配对规则。
  - 明确字段纯度：对白/独白/旁白/音效只承载文本或声音本体；对应 `*画面` 只承载可见画面、表演、空间或承托。
  - validator 新增 `音效画面` 字段解析与就近配对门禁；分组 quantizer/postprocess 同步纳入 `音效画面`，避免下游退入 fallback。
  - 《诡校》前三集 `2-格式` 与 `3-分组` 已同步补入音效画面，并重新生成分组量化报告与尾钩。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/references/script-format-contract.md`
    - `.agents/skills/aigc/1-规划/scripts/validate_script_output.py`
    - `.agents/skills/aigc/1-规划/scripts/grouping_quantizer.py`
    - `.agents/skills/aigc/1-规划/scripts/postprocess_grouping_output.py`
    - `projects/aigc/诡校/1-Planning/2-格式/第1集.md`
    - `projects/aigc/诡校/1-Planning/3-分组/第1集.md`

- `Case-20260425-AIGC-PLANNING-GROUPING-FORMAL-FIELD-SYNC`
  - 按用户反馈将 `3-分组` 同步到新版 `2-格式` 的正式影视剧本字段体系：分组阶段只插入组标题、组元数据与尾钩，不得把 `环境描写`、`角色动作`、`系统画面`、`规则显影` 等字段压缩回旧式 `动作画面` 摘要。
  - `grouping_quantizer.py` 的统计口径从单一 `action_visual` 扩展为 `visual_field`，覆盖正式画面字段；`postprocess_grouping_output.py` 的尾钩借焰同步允许从正式视觉字段中借取下一组单行。
  - 修复 `render_grouping_report.py` 对目录批处理时覆盖 `执行报告.md` 的问题，改为按集 merge 报告块。
  - 《诡校》前三集 `3-分组` 已从新版 `2-格式` 重新逐行投影，当前分组数为第1集 8 组、第2集 10 组、第3集 13 组，并通过 validator。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/references/grouping-contract.md`
    - `.agents/skills/aigc/1-规划/scripts/grouping_quantizer.py`
    - `.agents/skills/aigc/1-规划/scripts/postprocess_grouping_output.py`
    - `.agents/skills/aigc/1-规划/scripts/render_grouping_report.py`
    - `projects/aigc/诡校/1-Planning/3-分组/第1集.md`
    - `projects/aigc/诡校/1-Planning/3-分组/第2集.md`
    - `projects/aigc/诡校/1-Planning/3-分组/第3集.md`

- `Case-20260425-AIGC-PLANNING-SCRIPT-VISUAL-FIELDS`
  - 按用户反馈修复 `2-格式` 中 `动作画面` 直接承载小说叙述句的问题，新增正式影视剧本字段分流：环境描写、角色动作、音效、道具特写、角色造型、群像画面、系统画面、规则显影、现实灾难画面、心理反应、表演提示等。
  - 明确对白尽量冻结；各类画面字段允许剧本化改写，但不得删减事实、改变顺序或改写剧情因果。
  - validator 新增字段解析与 `WARN-ACTION-PROSE-LIKE` 提示；《诡校》前三集 `2-格式` 已完成画面字段剧本化分流并重算字数。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/references/script-format-contract.md`
    - `.agents/skills/aigc/1-规划/scripts/validate_script_output.py`
    - `.agents/skills/aigc/1-规划/knowledge-base/script-format-heuristics.md`
    - `projects/aigc/诡校/1-Planning/2-格式/第1集.md`
    - `projects/aigc/诡校/1-Planning/2-格式/第2集.md`
    - `projects/aigc/诡校/1-Planning/2-格式/第3集.md`

## 2026-04-24

- `Case-20260424-AIGC-PLANNING-SKILL2-FUSION`
  - 按 Skill 2.0 规范将原 `1-分集`、`2-格式`、`3-分组` 三个 sibling skill 包融合为 `.agents/skills/aigc/1-规划` 单一 Skill 2.0 包。
  - 原三包 `SKILL.md` 细则完整迁入 `references/episode-splitter-contract.md`、`references/script-format-contract.md`、`references/grouping-contract.md`，并补充融合后的 mode owner 说明。
  - 原三包 `CONTEXT.md` 经验层迁入 `knowledge-base/`；原 `_shared/IO_CONTRACT.md` 晋升为 `references/planning-io-contract.md`。
  - 原脚本与模板统一迁入父级 `scripts/`、`templates/`，产品入口收敛到 `$aigc-planning`。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/CONTEXT.md`
    - `.agents/skills/aigc/1-规划/references/legacy-migration-matrix.md`
    - `.agents/skills/aigc/1-规划/steps/planning-workflow.md`
    - `.agents/skills/aigc/1-规划/types/planning-type-map.md`
    - `.agents/skills/aigc/1-规划/review/planning-review-contract.md`
    - `reports/skill-upgrade-aigc-1-planning-20260424.md`

## 2026-04-12

- `Case-20260412-AIGC-PLANNING-GROUPING-ZXY-SINGLE-SKILL`
  - 将 `3-分组` 从“stage-local parent skill + shared 分组 specialist”收敛为知行合一单技能直达执行真源，并同步删除 `规划组/team.md` 中的 `分组` 角色及审计脚本中的对应硬依赖。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/references/grouping-contract.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-GROUPING-STAGE-LOCAL-OWNERSHIP`
  - 将 `3-分组` 升格为真正的 stage-local parent skill，并把 `规划组/team.md` 收回 shared dispatch plane 定位；同时新增 quantizer 作为本阶段计算真源。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/CONTEXT.md`
    - `.agents/skills/aigc/1-规划/references/grouping-contract.md`
    - `.agents/skills/aigc/1-规划/scripts/grouping_quantizer.py`

- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-DIRECT-LEAF`
  - 将 `1-分集` 从“规划组单 subagent 投影”收敛为 direct leaf skill，删除孤立的旧分集 subagent 载体，并同步修正父 skill、入口元数据与 audit。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/CONTEXT.md`
    - `.agents/skills/aigc/1-规划/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-规划/references/legacy-episode-splitter-openai.yaml`
    - `scripts/aigc_skill_audit.py`

- `Case-20260412-AIGC-PLANNING-AGENTS-PLAN-SHIFT`
  - 将 `1-Planning` 系列从“硬性 thinking sidecar”收敛为“subagents 返回 `agents plan`，skills 负责执行与按需留痕”，并同步修正 shared I/O、入口元数据、leaf 合同与 `规划组` team。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-规划/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-规划/references/script-format-contract.md`
    - `.agents/skills/aigc/1-规划/references/grouping-contract.md`

- `Case-20260412-AIGC-PLANNING-SUBAGENT-EXECUTION-BOUNDARY`
  - 将“subagents 负责思考与 plan，skill 负责统筹与执行”的硬规则同步到 `1-Planning` 父级、已完成 leaf skills 的经验层与入口元数据，避免入口摘要与主合同再度分叉。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/CONTEXT.md`
    - `.agents/skills/aigc/1-规划/agents/openai.yaml`
    - `.agents/skills/aigc/1-规划/knowledge-base/episode-splitter-heuristics.md`
    - `.agents/skills/aigc/1-规划/references/legacy-episode-splitter-openai.yaml`
    - `.agents/skills/aigc/1-规划/knowledge-base/script-format-heuristics.md`
    - `.agents/skills/aigc/1-规划/references/legacy-script-format-openai.yaml`
    - `.agents/skills/aigc/1-规划/knowledge-base/grouping-heuristics.md`
    - `.agents/skills/aigc/1-规划/references/legacy-grouping-openai.yaml`

- `Case-20260412-AIGC-PLANNING-ANCHOR-RESTORE`
  - 为 `.agents/skills/aigc/1-规划` 建立父级 `SKILL.md / CONTEXT.md`，修复规划组 team 与 registry 对不存在 `1-规划` 路径的断链引用。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/CONTEXT.md`
    - `.codex/registry/skills.yaml`
- `Case-20260412-AIGC-PLANNING-EPISODE-SPLIT-LEAF`
  - 参照 `AIGC-ZEN-VOID` 的 `1-故事分集`，在 DREAMER runtime 下补齐 `1-分集` 的 leaf 合同、经验层与机读模板。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-规划/knowledge-base/episode-splitter-heuristics.md`
    - `.agents/skills/aigc/1-规划/templates/episode-split-plan.template.json`
    - `.agents/skills/aigc/1-规划/references/planning-io-contract.md`
- `Case-20260412-AIGC-PLANNING-GROUPING-LEAF`
  - 参照 `AIGC-ZEN-VOID` 的 `3-拍摄段落`，在 DREAMER runtime 下补齐 `3-分组` 的 leaf 合同、模板、manifest 与校验链，并同步收口父 skill / shared I/O。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/references/grouping-contract.md`
    - `.agents/skills/aigc/1-规划/knowledge-base/grouping-heuristics.md`
    - `.agents/skills/aigc/1-规划/templates/grouping-output.template.md`
    - `.agents/skills/aigc/1-规划/skill_manifest.json`
    - `.agents/skills/aigc/1-规划/references/planning-io-contract.md`
- `Case-20260412-AIGC-PLANNING-SPLIT-REPORT-COMPACTION`
  - 按当前规划阶段收口口径，把 `1-分集` 的逐集执行报告降级为最多一份全剧集 `执行报告.md`，避免证据侧车按集爆炸。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/SKILL.md`
    - `.agents/skills/aigc/1-规划/references/episode-splitter-contract.md`
    - `.agents/skills/aigc/1-规划/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-规划/knowledge-base/episode-splitter-heuristics.md`
- `Case-20260412-AIGC-PLANNING-SCRIPT-SINGLE-PACKAGE`
  - 参照 `AIGC-ZEN-VOID` 的 `2-对白·独白·旁白`，在 DREAMER `1-Planning` 下补齐 `2-格式` 单技能包合同，并把 `标准剧 / 解说剧` 收敛为包内 subagents 路由。
  - 同步修正 `1-分集 -> 2-格式` 的共享 I/O：`1-分集` 只写逐集原文真源，`2-格式` 才写 canonical 主稿。
  - 证据路径：
    - `.agents/skills/aigc/1-规划/references/script-format-contract.md`
    - `.agents/skills/aigc/1-规划/knowledge-base/script-format-heuristics.md`
    - `.agents/skills/aigc/1-规划/scripts/validate_script_output.py`
    - `.agents/skills/aigc/1-规划/references/planning-io-contract.md`
    - `.agents/skills/aigc/1-规划/references/episode-splitter-contract.md`
