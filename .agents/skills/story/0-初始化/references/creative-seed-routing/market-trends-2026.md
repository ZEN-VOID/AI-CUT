# 网文市场扫描模板 (Market Scan Template)

> 更新日期: {YYYY-MM-DD}
> 数据来源: {列出搜索来源或平台页面名}
> 注意: 必须联网更新；仅记录标签/方向，不要摘录具体作品情节。

## 目录
- 一、平台榜单信号
- 二、题材生命周期
- 三、热门标签组合
- 四、读者偏好变化
- 五、平台差异
- 六、可执行建议

---

## 一、平台榜单信号

- 起点：{高频题材/标签/钩子}
- 番茄：{高频题材/标签/钩子}
- 其他：{可选补充}

---

## 二、题材生命周期

| 题材 | 阶段 | 风险 | 机会 | 备注 |
|------|------|------|------|------|
| {题材A} | {成熟/成长期/衰退} | {简述} | {简述} | {可选} |
| {题材B} | {成熟/成长期/衰退} | {简述} | {简述} | {可选} |

---

## 三、热门标签组合

| 组合 | 化学反应 | 空白度 | 难度 |
|------|----------|--------|------|
| {标签A + 标签B} | {简述} | {高/中/低} | {高/中/低} |

---

## 四、读者偏好变化

| 偏好 | 变化 | 观察依据 |
|------|------|----------|
| {偏好A} | {↑/↓} | {来源摘要} |

---

## 五、平台差异

| 平台 | 核心读者 | 偏好 | 创新接受度 |
|------|----------|------|------------|
| 起点 | {简述} | {简述} | {低/中/高} |
| 番茄 | {简述} | {简述} | {低/中/高} |

---

## 六、可执行建议
- 低风险创新：{视角/机制微调等}
- 中风险创新：{叙事结构/多主角等}
- 高风险创新：{全新题材/实验叙事等}

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 趋势资料是否只在用户显式请求或市场缺口阻断时加载，而非默认固定上下文？ | `creative_seed` | `FAIL-INIT-CREATIVE-ROUTE` | `references/creative-seed-routing/module-spec.md` Phase 2 | trend_gate decision、loaded_leaf_references |
| 趋势标签是否联网更新并保留来源时间，而非沿用过期静态判断？ | `security` / `integration` | `FAIL-INIT-SECURITY` | `guardrails/guardrails-contract.md`、本文件更新提示 | WebSearch/WebFetch evidence、source timestamps |
| 趋势判断是否只形成风险/机会提示，不越权决定 `2-卷章` 的 canonical 规划？ | `handoff` | `FAIL-INIT-HANDOFF` | `references/creative-seed-routing/module-spec.md` Phase 3 | risk_notes、deferred_to_planning |
