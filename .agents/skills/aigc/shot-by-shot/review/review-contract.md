# Review Contract

## Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-01` | 是否有可观察证据、时间码、截图、口播转写或明确描述 | `FAIL-SBS-EVIDENCE` | 回到 `N1-INTAKE` / `N2-EVIDENCE-LOCK` |
| `GATE-SBS-02` | 镜头或 observation unit 边界是否能复查 | `FAIL-SBS-SHOT-MAP` | 回到 `N3-SHOT-MAP` |
| `GATE-SBS-03` | 分析是否覆盖任务相关 craft 维度，且先观察后解释 | `FAIL-SBS-OBSERVATION` | 回到 `N4-CRAFT-OBSERVE` |
| `GATE-SBS-04` | 临摹原则是否脱离参考片具体表达 | `FAIL-SBS-IMITATION` | 回到 `N4-CRAFT-OBSERVE` / `N6-RIGHTS-FEASIBILITY` |
| `GATE-SBS-05A` | 3-美学风格解析是否按画面基调、角色、场景、道具、摄影、分镜六子技能拆分，并只作为 side context | `FAIL-SBS-AESTHETIC-BRIDGE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-05B` | 旧 `全局风格解析.md` / `设计风格解析.md` 是否只作 legacy，不继续作为新主输出合同 | `FAIL-SBS-LEGACY-STYLE-PACK` | 回到 `R2-SYNC-REPAIR` |
| `GATE-SBS-06` | 非美学 stage 解析是否不越权改写 `2-编剧`、`4-导演`、`5-表演`、`7-分镜`、`8-摄影`、`9-光影` 或 `11-主体` canonical 文件 | `FAIL-SBS-STAGE-BRIDGE` | 回到 `N5B-STAGE-BRIDGE` |
| `GATE-SBS-07` | 摄影风格解析是否对齐 `3-美学/摄影风格` 的构图秩序、景别、机位、运动、连续性，而不写具体分镜正文 | `FAIL-SBS-CINE-BRIDGE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-08` | 分镜风格解析是否对齐 `3-美学/分镜风格` 的节奏、组合和连接语法，而不替代 `分镜脚本.md` | `FAIL-SBS-STORYBOARD-STYLE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-09` | `分镜脚本.md` 是否含 Numbers 示例 19 列、顺序一致、每镜一行、提示词编排合规 | `FAIL-SBS-STORYBOARD-SCRIPT` | 回到 `N5B-STAGE-BRIDGE` |
| `GATE-SBS-10` | 是否存在版权表达复制、项目不适配或 AIGC 不可执行风险 | `FAIL-SBS-RIGHTS` | 回到 `N6-RIGHTS-FEASIBILITY` 或阻断 |
| `GATE-SBS-11` | 输出是否含执行证据、路径统一、解析文档与分镜脚本可消费 | `FAIL-SBS-OUTPUT` | 回到 `N7-WRITE-PACKAGE` |
| `GATE-SBS-12` | 执行报告是否包含 Reference Execution Matrix、Execution Decision Trace、Rule Evidence Map、N/A Justification 和 Repair Log | `FAIL-SBS-REPORT-EVIDENCE` | 回到 `N7-WRITE-PACKAGE` |

## Aesthetic Detail Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-AES-01` | `画面基调解析.md` 是否只提炼媒介、渲染、光影、美学范式、锚点候选和无污染 prompt 候选 | `FAIL-SBS-TONE-BRIDGE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-AES-02` | `角色风格解析.md` 是否只提炼角色层视觉风格，不写具体角色卡或完整定装 | `FAIL-SBS-CHARACTER-STYLE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-AES-03` | `场景风格解析.md` 是否只提炼空间风格、空镜秩序和世界地理视觉信号，不写具体场景清单 | `FAIL-SBS-SCENE-STYLE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-AES-04` | `道具风格解析.md` 是否只提炼道具功能层级、材质体系和符号边界，不写具体道具清单 | `FAIL-SBS-PROP-STYLE` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-AES-05` | 角色/场景/道具是否分三份解析，不混成旧设计总包 | `FAIL-SBS-DESIGN-SPLIT` | 回到 `N5A-AESTHETIC-BRIDGE` |
| `GATE-SBS-AES-06` | 是否没有参考片具体人物、构图、镜头顺序、纹章、文字或对象细节进入 style seeds | `FAIL-SBS-STYLE-POLLUTION` | 回到 `N6-RIGHTS-FEASIBILITY` |

## Storyboard Script Gates

| gate_id | question | fail code | repair |
| --- | --- | --- | --- |
| `GATE-SBS-STORY-01` | `分镜脚本.md` 是否使用 Numbers 示例 19 列和固定顺序 | `FAIL-STORYBOARD-19-COLUMNS` | 回到 `N5B-STAGE-BRIDGE` |
| `GATE-SBS-STORY-02` | 每行是否对应一个镜头，未用剧情段落冒充镜头 | `FAIL-STORYBOARD-ROW-PER-SHOT` | 回到 `N3-SHOT-MAP` / `N5B-STAGE-BRIDGE` |
| `GATE-SBS-STORY-03` | `镜号` 是否连续，正式四段式 ID 只放参考或说明，不替代表头 | `FAIL-STORYBOARD-ID` | 回到 `N5B-STAGE-BRIDGE` |
| `GATE-SBS-STORY-04` | 角色图、参考列是否不臆造素材路径；无素材时留空 | `FAIL-STORYBOARD-ASSET-PATH` | 回到 `N5B-STAGE-BRIDGE` |
| `GATE-SBS-STORY-05` | 分镜提示词和视频运动提示词是否按功能块组织，并以时长收束 | `FAIL-STORYBOARD-PROMPT-BLOCK` | 回到 `N5B-STAGE-BRIDGE` |
| `GATE-SBS-STORY-06` | 是否只学习示例字段组织和信息密度，不复制示例角色、剧情、台词、场景或视觉表达 | `FAIL-STORYBOARD-EXAMPLE-COPY` | 回到 `N6-RIGHTS-FEASIBILITY` |

## Verdict

- `pass`: 所有 gate 通过，可作为 AIGC 阶段附加上下文。
- `needs_rework`: 有局部字段、证据或桥接问题，必须直接修复后复审。
- `blocked`: 素材不可见、版权边界无法处理、或用户要求具体复制。
