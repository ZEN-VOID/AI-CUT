# Execution Flow

## 输入合同

- 首选输入：`projects/<项目名>/3-Detail/第N集.json`
- 兼容输入：`projects/<项目名>/3-Detail/第N集.json`
- 输入内容必须符合 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 的主结构，尤其是：
  - `metadata.episode_id`
  - `final_output.main_content.分镜组列表[]`
  - `分镜组列表[].分镜明细[]`
  - `分镜明细[].角色及站位和穿搭`

## 默认流程

1. 解析输入路径。
2. 若用户给的是 `3-Detail/第N集.json` 且对应 `3-Detail/第N集.json` 不存在，则直接消费该文件。
3. 若用户给的路径不存在，但同项目下存在等价别名路径，允许自动回退并在 manifest 记录。
4. 逐组遍历 `分镜组列表[]`。
5. 逐镜遍历 `分镜明细[]`，解析 `角色及站位和穿搭`。
6. 聚合 `roles[]` 与 `group_role_map[]`。
7. 写出 `角色清单.json` 与 `_manifest.json`。

## 默认落点

- `projects/<项目名>/4-Design/2-角色/1-清单/第N集/角色清单.json`
- `projects/<项目名>/4-Design/2-角色/1-清单/第N集/_manifest.json`

## 命令示例

```bash
python3 .agents/skills/aigc/4-Design/2-角色/1-清单/scripts/extract_role_list.py \
  --input "projects/项目名/3-Detail/第1集.json"
```

```bash
python3 .agents/skills/aigc/4-Design/2-角色/1-清单/scripts/extract_role_list.py \
  --input "projects/项目名/3-Detail/第1集.json" \
  --dry-run
```

```bash
python3 .agents/skills/aigc/4-Design/2-角色/1-清单/scripts/extract_role_list.py \
  --project "项目名" \
  --episode "第1集"
```
