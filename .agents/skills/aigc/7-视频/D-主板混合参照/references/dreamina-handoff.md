# Dreamina Handoff Contract

本文件定义 `D-主板混合参照` 与 `.agents/skills/cli/dreamina-cli` 的交接规则。

## Command Selection

| condition | command |
| --- | --- |
| `reference_images` 非空 | `dreamina multimodal2video --image <path> ... --prompt <prompt>` |
| `reference_images` 为空 | `dreamina text2video --prompt <prompt>` |
| Dreamina CLI 不可用或未登录 | 写入 `blocked`，不得伪造 submit_id |

故事板与主体图片都是参照图，不是首帧。默认不得使用 `image2video`，除非用户显式要求首帧图生视频并接受路线变更。

## Submit Plan Shape

```json
{
  "project": "<项目名>",
  "episode": "第1集",
  "output_root": "projects/aigc/<项目名>/7-视频/D-主板混合参照/第1集",
  "jobs": [
    {
      "group_id": "1-1-1",
      "command_type": "multimodal2video",
      "prompt_path": "projects/aigc/<项目名>/7-视频/D-主板混合参照/第1集/prompts/1-1-1.txt",
      "reference_images": [
        {
          "role": "storyboard_total_reference",
          "marker": "@图1",
          "path": "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png"
        },
        {
          "role": "subject_reference",
          "subject_type": "角色",
          "subject_name": "林夏",
          "marker": "@图2",
          "path": "projects/aigc/<项目名>/5-设计/角色/3-生成/林夏/多视图.png"
        }
      ],
      "download_dir": "projects/aigc/<项目名>/7-视频/D-主板混合参照/第1集/videos",
      "expected_output": "projects/aigc/<项目名>/7-视频/D-主板混合参照/第1集/videos/1-1-1.mp4"
    }
  ]
}
```

## Preflight

1. 提交前必须运行 `dreamina user_credit`。
2. 读取 dreamina-cli 当前图片上限、duration、ratio、resolution 支持范围。
3. 图片路径必须存在；空数组不传 `--image`。
4. 每个 job 写入 queue ledger 后再提交。

## Queue Ledger

`第N集-dreamina-queue.md` 至少包含：

| queue_id | group_id | command_type | submit_id | local_status | remote_status | reference_count | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Concurrency

- 默认 worker 数为 `min(4, job_count)`，除非用户指定。
- worker 只写独立提交结果；最终 `第N集-dreamina-results.json` 与 `执行报告.md` 由主流程汇流写入。
- `--poll` 只作短等待；超时必须保留 submit_id 并用 `query_result` 后续查询。
