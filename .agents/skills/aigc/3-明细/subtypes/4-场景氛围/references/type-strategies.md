# aigc 3-明细 / 4-场景氛围 / Type Strategies

本文件承载 `aigc 3-明细 / 4-场景氛围` 的路由策略、VSM 与局部回退规则。

## 策略路由矩阵

| 路线 | kind | 默认调度 | 触发条件 | 主职责 | 输出焦点 |
| --- | --- | --- | --- | --- | --- |
| `景镜` | `conceptual` | dominant-first | 已有情绪跃迁，且自然/天气/空气信号能与戏核同向 | 让景物成为情绪显影剂 | 风、雨、雾、树影、水面、湿度、声场、冷暖体感 |
| `境镜` | `conceptual` | dominant-first | 场景更需要空间压力、迟滞、空旷/拥挤失衡、公共冷感 | 让环境成为存在压力场 | 空间尺度、秩序、距离、噪声、静默、时间停滞 |
| `物镜` | `conceptual` | dominant-first | 场景里有可追溯物件，且它能承担时间/关系回声 | 让物件承担回收或错位暗示 | 旧物、残留、磨损、滴落、融化、生锈、变质、反复出现 |
| `留白` | `conceptual` | override-high | 余波、失语、等待、缺席、告别后静场 | 用最小环境信号维持张力 | 环境音、空镜感、无动于衷的日常物象、反差日常声源 |

硬规则：

1. 单一段落默认只允许一个 dominant route，最多再带一个 support route。
2. `留白` 一旦命中高优先级，不得再把 `景 / 境 / 物` 三条路线全部堆满。
3. 本层允许写环境语义，不允许写摄影参数、镜头焦段、色彩分级等摄影层术语。
4. 禁止把策略名直接写进正文，例如 `景镜：`、`物镜：`、`氛围环境：`。
5. `景镜` 只接受可见自然信号，不接受抽象意境词堆叠。
6. `境镜` 必须落到具体空间状态，不接受哲思化空话。
7. `物镜` 默认要求时间刻度与暗喻链并存；只好看、不随时间变化的物件优先降级为普通环境细节。
8. `留白` 不是空白；若保留静默，也必须留下最小但有效的环境张力。

## 预设护栏与题材相容

1. 题材与环境语气优先读取 `writer.story` bundle 的 `世界卡 / 风格卡`。
2. 若 bundle 缺失，再回退 canonical `project_preset.json`；两者都缺失时必须显式记录输入缺口。
3. 粗裁决先回答“环境任务是什么”，优选层才回答“哪条路线更美”。
4. route 决策若与题材主色冲突，应优先降级到 `BASELINE` 或改走更稳的 dominant route，而不是硬写华丽风格。

## VSM

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SAT-SOURCE | 输入 | grouped source 与当前终稿是否可读 | `ready/missing/invalid` | 路径与结构检查 | P0 |
| V-SAT-PRESET-SOURCE | 输入 | `writer.story` bundle / legacy preset 可用性 | `bundle/legacy/missing` | manifest 与文件检查 | P0 |
| V-SAT-ANCHOR | 叙事 | 锚点卡完整度 | `full/partial/missing` | 六项锚点完整度检查 | P0 |
| V-SAT-ATMOS-GAP | 叙事 | 环境氛围信息是否偏薄 | `rich/partial/missing` | 段落抽检 | P0 |
| V-SAT-SCENE-SIGNAL | 风格 | 景镜信号强度 | `high/medium/low` | 自然/天气/温差与情绪耦合检测 | P1 |
| V-SAT-PRESSURE-SIGNAL | 风格 | 境镜信号强度 | `high/medium/low` | 空间压力、秩序感、疏离感检测 | P1 |
| V-SAT-OBJECT-SIGNAL | 结构 | 物镜候选是否可追溯 | `ready/weak/missing` | 物件出现与回收线检查 | P0 |
| V-SAT-TEMPORAL-OBJECT | 结构 | 物镜是否自带时间刻度 | `ready/weak/missing` | 物件状态变化检查 | P1 |
| V-SAT-MOTIF-TRACE | 结构 | 景/境/物母题是否可回收 | `clear/weak/missing` | 重复信号与回收位检查 | P1 |
| V-SAT-SILENCE-NEED | 节奏 | 是否应走留白路径 | `high/medium/low` | 余波、失语、等待、缺席检测 | P1 |
| V-SAT-GENRE-FIT | 风格 | 当前路线与题材/风格卡相容度 | `fit/risk/conflict` | bundle 与正文交叉检查 | P1 |
| V-SAT-DENSITY | 节奏 | 当前氛围注入密度 | `balanced/sparse/overload` | 场景级计数 | P0 |
| V-SAT-SIBLING-BOUNDARY | 边界 | 是否越权到运镜/摄影/转场 | `pass/fail` | 术语与句式检查 | P0 |
| V-SAT-CONTINUITY | 连续性 | 注入后段落是否连读 | `low/high` | 前后句语义检查 | P0 |
| V-SAT-LABEL | 文体 | 是否出现标签式写法 | `pass/fail` | 行首模式匹配 | P0 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SAT-01 | `V-SAT-SOURCE in {missing,invalid}` | 1.0 | 无 | 无 |
| C-SAT-01A | `V-SAT-PRESET-SOURCE=missing` | 1.0 | 无 | 可并发 C-SAT-02~C-SAT-11 |
| C-SAT-02 | `V-SAT-ANCHOR in {partial,missing}` | 1.0 | 无 | 可并发 C-SAT-03 |
| C-SAT-03 | `V-SAT-ATMOS-GAP in {partial,missing}` | 0.95 | 无 | 可并发 C-SAT-04~C-SAT-07 |
| C-SAT-04 | `V-SAT-SCENE-SIGNAL in {high,medium}` | 0.9 | 无 | 可并发 C-SAT-03/C-SAT-07/C-SAT-07A |
| C-SAT-05 | `V-SAT-PRESSURE-SIGNAL in {high,medium}` | 0.9 | 无 | 可并发 C-SAT-03/C-SAT-07/C-SAT-07A |
| C-SAT-06 | `V-SAT-OBJECT-SIGNAL=ready` | 0.95 | 无 | 可并发 C-SAT-03/C-SAT-04/C-SAT-05/C-SAT-06A |
| C-SAT-06A | `V-SAT-TEMPORAL-OBJECT in {weak,missing}` | 0.9 | 无 | 可并发 C-SAT-06 |
| C-SAT-07 | `V-SAT-SILENCE-NEED=high` | 0.95 | 与过密补写冲突时优先 | 可并发 C-SAT-03/C-SAT-04/C-SAT-05/C-SAT-06 |
| C-SAT-07A | `V-SAT-GENRE-FIT in {risk,conflict}` | 0.9 | 无 | 可并发 C-SAT-04/C-SAT-05/C-SAT-06 |
| C-SAT-07B | `V-SAT-MOTIF-TRACE in {weak,missing}` | 0.9 | 无 | 可并发 C-SAT-04/C-SAT-05/C-SAT-06 |
| C-SAT-08 | `V-SAT-SIBLING-BOUNDARY=fail` | 1.0 | 无 | 可并发全部 |
| C-SAT-09 | `V-SAT-DENSITY=overload` | 1.0 | 与 `sparse` 互斥 | 可并发 C-SAT-04~C-SAT-08 |
| C-SAT-10 | `V-SAT-CONTINUITY=high` | 0.9 | 无 | 可并发 C-SAT-08/C-SAT-09 |
| C-SAT-11 | `V-SAT-LABEL=fail` | 1.0 | 无 | 可并发全部 |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SAT-01 | S-SAT-INPUT | 回退并锁定合法 grouped source 与当前终稿 | 输入唯一且可读 | S-SAT-PAUSE | 两轮仍找不到源文本 |
| C-SAT-01A | S-SAT-PRESET | 优先补读 `writer.story` bundle，缺失时记录并回退 legacy preset | 预设来源明确且可追溯 | S-SAT-BASELINE | 结构化预设长期缺失 |
| C-SAT-02 | S-SAT-ANCHOR | 先补齐锚点卡，再决定环境任务 | 锚点达到最低完整度 | S-SAT-MINIMAL | 仍无法锁定戏核 |
| C-SAT-03 | S-SAT-BASELINE | 先补基础环境气场，不急着强风格 | 每场景至少有一个有效环境信号 | S-SAT-MINIMAL | 上游证据持续不足 |
| C-SAT-04 | S-SAT-SCENE | 走 `景镜` 主路线 | 景物与情绪同向且可拍摄 | S-SAT-BASELINE | 景物信号不足 |
| C-SAT-05 | S-SAT-PRESSURE | 走 `境镜` 主路线 | 空间压力可见且不抽象 | S-SAT-BASELINE | 空间信号不足 |
| C-SAT-06 | S-SAT-OBJECT | 走 `物镜` 主路线 | 物件链可追溯、可回收 | S-SAT-BASELINE | 物件证据偏弱 |
| C-SAT-06A | S-SAT-OBJECT-TIME | 给物件补时间刻度；若补不出来则降级成普通环境细节 | 物件具状态变化与叙事映射 | S-SAT-BASELINE | 时间刻度仍虚弱 |
| C-SAT-07 | S-SAT-BLANK | 收敛到留白写法 | 高留白段新增不超过 1 条 | S-SAT-BASELINE | 留白不成立 |
| C-SAT-07A | S-SAT-GENRE-GUARD | 收紧到题材兼容路线或降级基线增强 | 路线与题材相容 | S-SAT-BASELINE | 风格冲突持续存在 |
| C-SAT-07B | S-SAT-MOTIF | 把可复现信号补成“首次 -> 变体 -> 回收”，不成立则取消母题宣称 | 母题链可追溯 | S-SAT-BASELINE | 回收位仍不存在 |
| C-SAT-08 | S-SAT-BOUNDARY | 回滚摄影/运镜/转场越权表述 | 句内不再出现 sibling 专属术语 | S-SAT-PAUSE | 连续两轮仍越权 |
| C-SAT-09 | S-SAT-TRIM | 裁掉低增益句，只保留主任务句 | 密度恢复 `balanced` | S-SAT-BLANK | 裁剪后仍噪声过高 |
| C-SAT-10 | S-SAT-BRIDGE | 调整注入位点或补桥接句 | 前后句连读自然 | S-SAT-TRIM | 连读仍断裂 |
| C-SAT-11 | S-SAT-DETAG | 去标签并改为段内自然融写 | 标签命中数归零 | S-SAT-TRIM | 去标签后仍不自然 |

## 预设优质语料与类型化模板

### 悬疑 / 犯罪 / 心理惊悚

- `景镜` 优先潮湿、阴雨、低云、拉长的影子、水洼中的霓虹倒影。
- `境镜` 优先狭窄过道、剥落墙皮、闪烁荧光灯、深夜空站、带工业回音的地下车库。
- `物镜` 优先燃尽烟头、沾泥鞋底、停摆怀表、融化冰块、反复出现的半杯冷咖啡。
- 融写方向：让环境像倒计时，而不是像装饰。

### 史诗 / 权谋 / 历史正剧

- `景镜` 优先飞雪、狂风、残阳、大漠烟尘、深宫阴影。
- `境镜` 优先空旷大殿、高耸阶梯、压抑对称、回声长廊。
- `物镜` 优先熄灭烛火、积灰王座、残局、未出鞘的剑、被反复摩挲的玉扳指。
- 融写方向：让秩序、权力与宿命压到空间表面，而不是直接讲大道理。

### 细腻情感 / 现言 / 意识流

- `景镜` 优先斑驳光影、黄昏微风、雨后空气、车窗外流光。
- `境镜` 优先人群中的孤独、带回忆的旧屋、夕照阳台、静谧洗衣房。
- `物镜` 优先遗落外套、失味香水瓶、并排牙刷、半枯花束、循环老唱片。
- 融写方向：让细节先碰到身体或旧关系，再把情绪缓慢带出来。

### 科幻 / 赛博朋克 / 废土

- `景镜` 优先酸雨、人造雾霾、看不见星空的穹顶、被全息投影切碎的光斑。
- `境镜` 优先垃圾山、密集管线、合成电子音幽闭舱室、无菌实验室。
- `物镜` 优先漏电义体接口、发黄纸书、故障电子眼、浑浊营养液。
- 融写方向：让技术环境本身成为生存压力，而不是只当背景设定。
