# Review Contract

本 review gate 只裁决 `C-主体参照` 的组级视频 prompt、主体参照、LibTV 计划、队列和项目持久化，不改写 `4-分组` 主真源。

## Review Verdicts

| verdict | meaning |
| --- | --- |
| `pass` | 所有必需门禁通过，可交付或执行 LibTV |
| `pass_with_todo` | 主输出可用，但存在明确记录的缺图、排队、下载或外部阻塞 |
| `needs_rework` | 存在会污染 prompt、参照、提交命令或结果追踪的问题，必须返工 |

## Gate Checklist

| gate_id | check | fail_code | rework |
| --- | --- | --- | --- |
| `G1-SOURCE` | 每个 `group_id` 可回指 `4-分组` 源标题、组正文和 YAML | `FAIL-VIDSUBJ-GROUP` | `references/group-source-extraction.md` |
| `G2-CONTENT` | prompt 主体直接使用现有组正文，分镜顺序完整 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G3-SUBJECTS` | Characters / Scene / Props 只来自组底 YAML | `FAIL-VIDSUBJ-REF` | `references/reference-slot-binding.md` |
| `G4-SLOTS` | 只绑定存在图片，多视图优先，缺图不留空路径；多候选必须有视觉消歧证据或进入 ambiguous | `FAIL-VIDSUBJ-REF` | `references/reference-slot-binding.md` |
| `G5-PATH-SUFFIX` | 每个已绑定主体的信息后都有 `@<图片路径>`，且与 `images[]` 顺序一致；不得使用抽象 `@图N` 替代真实路径 | `FAIL-VIDSUBJ-PROMPT` | `references/video-prompt-assembly-contract.md` |
| `G6-PROVIDER-ROUTE` | 有图或视觉消歧已唯一解决时远端 handoff 锁 `modeType=mixed2video` 和 `mixedList`，无图锁 `modeType=text2video`，未解决 ambiguous 不提交且不传空图片槽 | `FAIL-VIDSUBJ-LIBTV` | `references/libtv-handoff.md` |
| `G7-SELF-CHECK` | 生成前有 `LIBTV_ACCESS_KEY credential check` 自检策略或结果 | `FAIL-VIDSUBJ-LIBTV` | `.agents/skills/cli/libTV/SKILL.md` |
| `G8-QUEUE` | 每个 submitted / pending 任务都有 group package 内的 `queue.md`、sessionId 或 blocked reason；集级 queue 只作汇总 | `FAIL-VIDSUBJ-LIBTV` | `references/libtv-handoff.md` |
| `G9-PERSIST` | prompt、manifest、plan、queue、results、report 和视频下载路径位于 `groups/<分镜组ID>/`；集级文件只作派生 summary | `FAIL-VIDSUBJ-LIBTV` | `templates/output-template.md` |
| `G10-REPORT` | 执行报告列出 submitted / queued / downloaded / skipped / failed 与返工入口 | `FAIL-VIDSUBJ-REPORT` | `templates/output-template.md` |
| `G11-POST-SUBMIT` | create_session 后已 query 一次并执行 ask_user stall 检测；`ask_user` / 等待下一条消息 / 请稍候不得被标为 `pending_remote_generation` | `FAIL-VIDSUBJ-LIBTV-STALL` | `references/libtv-handoff.md` |

## Review Output

审查结果应写入 `执行报告.md` 或 final note：

```yaml
review:
  verdict: pass
  checked_gates:
    - G1-SOURCE
    - G2-CONTENT
    - G3-SUBJECTS
    - G4-SLOTS
    - G5-PATH-SUFFIX
    - G6-PROVIDER-ROUTE
    - G7-SELF-CHECK
    - G8-QUEUE
    - G9-PERSIST
    - G10-REPORT
    - G11-POST-SUBMIT
  todos: []
```
