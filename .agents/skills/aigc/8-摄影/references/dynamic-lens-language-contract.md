# Dynamic Lens Language Contract

本文件定义 `8-摄影` 内联注入的动态语言标准。运镜句要表现时间中的变化；该静止时也必须显式说明静止的观看理由。

## Normal Shot Rule

普通模式下，每条 `分镜N（N-N秒）：` 后追加一段综合运镜句。综合句必须包含：

1. 镜头角度及变化。
2. 镜头类型或运动方式。
3. 镜头速度或速度曲线。
4. 焦点静止或变化。

四项必须融合成一句自然中文，不写成标签清单。

## One-Take Rule

当用户、source 或 `7-分镜` 明确要求“一镜到底、长镜头、不中断跟拍、连续穿行”时，以画面点为单位处理：

- 不为每条分镜设计彼此独立的切镜。
- 先为该画面点内全部分镜建立一条连续运动链。
- 输出一段 `一镜到底运镜（覆盖分镜A-B，N-N秒）：...`，放在该画面点全部分镜之后。
- 跨画面点或跨分镜组时必须检查运动方向、主体位置、焦点交接和速度过渡是否可连续。

## Bad Patterns

- 只写“镜头推进”“镜头跟随”“特写压迫”，没有起点、路径、速度、焦点。
- 每条分镜都机械使用慢推或环绕。
- 静止镜头没有观看理由。
- 一镜到底仍写成多个互相硬切的镜头。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 普通分镜是否逐条有综合运镜句且四项齐全？ | `GATE-CAM-08-DYN-01` | `FAIL-CAM-DYNAMIC-MISSING` | `N7-CAM-INJECT` | missing_component_table |
| 运镜句是否读得出起点、变化、速度和落点？ | `GATE-CAM-08-DYN-02` | `FAIL-CAM-DYNAMIC-FLAT` | `N6-CAM-MOVEMENT-DESIGN` | dynamic_sample_review |
| 一镜到底是否以画面点为单位形成连续链？ | `GATE-CAM-08-DYN-03` | `FAIL-CAM-ONETAKE-SPLIT` | `N6B-CAM-ONETAKE-CHAIN` | one_take_chain_map |
