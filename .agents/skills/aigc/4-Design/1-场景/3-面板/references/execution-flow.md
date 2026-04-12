# 输入与上下文装配

## 必需输入

1. `projects/<项目名>/4-Design/1-场景/2-设计/第N集/场景设计.json`
2. `templates/scene-panel-layout.template.json`

## 补充输入

1. `projects/<项目名>/4-Design/1-场景/2-设计/第N集/<scene_key>.md`
2. `projects/<项目名>/2-Global/全局风格.md`
3. `projects/<项目名>/2-Global/类型指导.md`
4. `projects/<项目名>/2-Global/导演意图.md`

## 默认执行流程

1. 读取 `场景设计.json`，锁定本轮命中 `scene_designs[]`。
2. 为每个命中场景提取：
   - `scene_key`
   - `scene_name`
   - `scene_variant`
   - `source_scene_ids`
   - `final_scene_prompt`
   - `panel_handoff`
   - `reverse_taboos`
3. 加载 `scene-panel-layout.template.json`，固定 `16:9 + 3x3` 面板合同。
4. 组装：
   - `identity_badge`
   - `panel_prompt`
   - `negative_prompt`
5. 写出逐场景 `<scene_key>-layout.json`。
6. 聚合 episode 级 `场景面板.json`。
7. 按需写 `_manifest.json`。
8. 返回默认下一入口：
   - 若要继续图像生成 -> `5-Image`
   - 若要审稿/校验 -> 当前 carrier + review 流

## 命名合同

- episode 目录：`projects/<项目名>/4-Design/1-场景/3-面板/第N集/`
- episode carrier：`场景面板.json`
- per-scene layout：`<scene_key>-layout.json`
- optional manifest：`_manifest.json`

## CLI 合同

```bash
python3 .agents/skills/aigc/4-Design/1-场景/3-面板/scripts/generate_scene_panels.py \
  --project "<项目名>" \
  --episode "第1集"
```

可选参数：

- `--scene-key <scene_key>`：只生成单个场景面板
- `--design-file <path>`：显式指定 `场景设计.json`
- `--output-root <path>`：覆盖默认输出根
- `--dry-run`：只打印将写出的目标文件，不落盘
- `--force`：覆盖已存在输出

## 硬规则

1. 脚本只承接模板装配与落盘，不得替代 `2-设计` 的结构化思考。
2. 若 `scene_designs[]` 缺少 `scene_key` 或 `final_scene_prompt`，必须失败退出，不得静默补空。
3. 若输出已存在，默认不覆盖；除非显式传 `--force`。
4. 本阶段不得自动调用图片生成或视频生成脚本。
